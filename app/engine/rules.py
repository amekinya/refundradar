"""Deterministic routing: one customs entry in, one refund route out.

Rules are evaluated in order (first match wins), mirroring the decision table R0-R20 in
docs/refund_rules_research.md §(a). No model is involved here: money, dates and routes are code.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

from app.engine import catalog as C
from app.engine import entry_number as EN
from app.engine.headings import ALL_IN_15, is_dutiable_ieepa, is_section_122, normalize_hts, program_of
from app.engine.interest import estimate_interest
from app.engine.models import Entry, Profile, Route

UNLIQUIDATED = {"", "not liquidated", "unliquidated", "open", "extended", "suspended", "pending", "under review"}
COURIERS = ("UPS", "UNITED PARCEL", "FEDEX", "FEDERAL EXPRESS", "DHL")
KNOWN_TYPES = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", "21", "22", "23", "31", "32", "34", "38", "47"}


def _norm_id(s: str) -> str:
    return re.sub(r"[^0-9A-Z]", "", (s or "").upper())


def _make(entry: Entry, rule_id: str, **kw) -> Route:
    r = C.RULES[rule_id]
    return Route(
        entry_number=EN.display(entry.entry_number),
        rule_id=r.id,
        bucket=kw.pop("bucket", r.bucket),
        title=kw.pop("title", r.title),
        action=kw.pop("action", r.action),
        tag=r.tag,
        sources=r.sources,
        **kw,
    )


def route_entry(entry: Entry, profile: Profile, today: date) -> Route:
    etype = (entry.entry_type or "01").strip()[:2].zfill(2)
    ieepa_lines = [l for l in entry.lines if is_dutiable_ieepa(l.hts) and l.duty > 0]
    principal = round(sum(l.duty for l in ieepa_lines), 2)
    s122 = round(sum(l.duty for l in entry.lines if is_section_122(l.hts) and l.duty > 0), 2)
    programs = tuple(sorted({program_of(l.hts) or "" for l in ieepa_lines} - {""}))
    all_in = any(normalize_hts(l.hts) in ALL_IN_15 for l in ieepa_lines)

    # Liquidation: actual if known, else estimated from the entry date (flagged).
    status = (entry.liquidation_status or "").strip().lower()
    liq = entry.liquidation_date
    estimated = False
    if etype in {"11", "12"} and liq is None:
        liq = entry.deposit_date or entry.entry_date  # informal entries liquidate when duty is paid
        estimated = True
    elif liq is None and status in {"", "unknown", "liquidated"} and entry.entry_date:
        guess = entry.entry_date + timedelta(days=C.NORMAL_LIQUIDATION_DAYS)
        if status == "liquidated":
            liq, estimated = min(guess, today), True
        elif guess <= today:
            liq, estimated = guess, True
    liquidated = liq is not None and status not in UNLIQUIDATED - {""}
    if status in UNLIQUIDATED - {""} and entry.liquidation_date is None:
        liquidated = False
    days = (today - liq).days if (liquidated and liq) else None

    base = dict(
        principal=principal,
        programs=programs,
        all_in_overstated=all_in,
        liquidation_date=liq if liquidated else None,
        liquidation_estimated=estimated and liquidated,
    )

    def finish(r: Route) -> Route:
        # Who holds the claim?
        mine, theirs = _norm_id(profile.importer_number), _norm_id(entry.importer_number)
        if mine and theirs and mine != theirs:
            r.holder = "someone_else"
            r.notes.append("The importer of record on this entry isn't you, so the refund belongs to them.")
        if any(c in (entry.importer_name or "").upper() for c in COURIERS):
            r.holder = "someone_else"
            r.notes.append("A courier is the importer of record. Use the courier's refund program; it passes refunds to whoever paid.")
        if etype == "06":
            r.notes.append("Foreign-trade-zone entry: verify the Chapter 99 lines (no FTZ-specific CAPE rule found).")
        if etype in {"11", "12"}:
            r.notes.append("Informal entry: liquidated on the date duty was paid (19 CFR 159.10), so windows run from then.")
        if r.liquidation_estimated:
            r.notes.append("Liquidation date estimated from the entry date. Confirm in ACE before acting.")
        if all_in:
            r.notes.append("Includes a '15% all-in' deal line: only the part above the normal duty is refundable, so this estimate runs high.")
        if r.deadline:
            r.days_left = (r.deadline - today).days
        r.entry_problems = EN.validate(entry.entry_number)
        r.source = entry.source
        r.interest = _interest(entry, r, today, profile.corporate)
        return r

    # --- Gates ---------------------------------------------------------------------------
    if entry.on_cape_declaration:
        return finish(_make(entry, "R18", **base))
    if not ieepa_lines:
        if s122 > 0:
            r = _make(entry, "R0b", **{**base, "principal": 0.0})
            if liquidated and liq:
                r.deadline, r.deadline_type = liq + timedelta(days=C.PROTEST_WINDOW_DAYS), "PROTEST_180"
            r.notes.append(f"${s122:,.2f} of Section 122 surcharge is on this entry.")
            return finish(r)
        return finish(_make(entry, "R0", **base))
    if entry.entry_date and entry.entry_date >= C.IEEPA_COLLECTION_END:
        return finish(_make(entry, "R1", **{**base, "principal": 0.0}))
    if entry.surety_paid:
        return finish(_make(entry, "R2", **base))
    if entry.not_in_ace:
        return finish(_make(entry, "R3", **base))
    if etype in {"08", "09", "23", "47"}:
        return finish(_make(entry, "R4", **base))
    if etype in {"21", "22"}:
        return finish(_make(entry, "R5", **base))
    if etype not in KNOWN_TYPES:
        return finish(_make(entry, "R20", **base))
    if entry.drawback:
        return finish(_make(entry, "R6", **base))
    if entry.recon_flag and entry.recon_09_filed:
        return finish(_make(entry, "R7", **base))

    # --- Protests ------------------------------------------------------------------------
    p = (entry.protest_status or "").lower()
    if p == "denied":
        return finish(_make(entry, "R8b", **base))
    if p in {"open", "suspended"}:
        r = _make(entry, "R8", **base)
        if days is not None and days <= C.CAPE_WINDOW_DAYS and entry.protest_solely_ieepa:
            r.deadline, r.deadline_type = liq + timedelta(days=C.CAPE_WINDOW_DAYS), "CAPE_80"
            r.action = "Withdraw the IEEPA-only protest (ask the Center to lift any suspension), then file in CAPE before day 80."
        elif days is not None and days > C.CAPE_WINDOW_DAYS:
            r.action = "Keep the protest. CAPE rejects protested entries and CBP's protest functionality has no date yet."
        return finish(r)

    # --- AD/CVD ----------------------------------------------------------------------------
    if entry.ad_cvd or etype in {"03", "07", "34", "38"}:
        if not liquidated and (status == "suspended" or entry.suspension_record):
            return finish(_make(entry, "R10", **base))
        if not liquidated and status == "pending":
            return finish(_make(entry, "R9", **base))

    # --- Unliquidated ----------------------------------------------------------------------
    if not liquidated:
        if status == "under review" or entry.suspension_record:
            r = _make(entry, "R11", **base, bucket="review",
                      action="CAPE lists errors for entries under review or with a suspension record. Ask your broker before filing.")
            return finish(r)
        if entry.needs_psc:
            return finish(_make(entry, "R19", **base))
        if entry.recon_flag:
            return finish(_make(entry, "R7b", **base))
        r = _make(entry, "R11", **base)
        if etype == "06":
            r = _make(entry, "R17", **base)
        return finish(r)

    # --- Liquidated ----------------------------------------------------------------------
    assert days is not None and liq is not None
    if days <= C.CAPE_WINDOW_DAYS:
        rid = "R19" if entry.needs_psc else ("R7b" if entry.recon_flag else "R12")
        r = _make(entry, rid, **base)
        r.deadline, r.deadline_type = liq + timedelta(days=C.CAPE_WINDOW_DAYS), "CAPE_80"
        if estimated:
            r.bucket = "review"
            r.action = "This may still be inside the 80-day CAPE window, but the liquidation date is estimated. Check ACE today."
        return finish(r)
    if profile.cit_plaintiff:
        rid = "R15" if profile.plaintiff_ior_submitted_by_cutoff else "R15b"
        return finish(_make(entry, rid, **base))
    if days <= C.PROTEST_WINDOW_DAYS:
        r = _make(entry, "R13", **base)
        r.deadline, r.deadline_type = liq + timedelta(days=C.PROTEST_WINDOW_DAYS), "PROTEST_180"
        return finish(r)
    r = _make(entry, "R14", **base)
    r.deadline, r.deadline_type = C.EARLIEST_CIT_DEADLINE, "CIT_2YR"
    return finish(r)


def _interest(entry: Entry, r: Route, today: date, corporate: bool) -> float:
    if r.principal <= 0 or r.bucket in {"not_eligible"}:
        return 0.0
    start = entry.deposit_date or (entry.entry_date + timedelta(days=C.DEPOSIT_LAG_DAYS) if entry.entry_date else None)
    if start is None:
        return 0.0
    accept = today + timedelta(days=C.CAPE_ACCEPTANCE_LAG_DAYS)
    if r.bucket == "cape_now" and r.liquidation_date is None:
        end = accept + timedelta(days=C.CAPE_LIQUIDATION_AFTER_ACCEPT_DAYS)
    elif r.bucket in {"cape_now", "fix_first"}:
        end = accept
    else:
        end = today  # accrued to date; the real end is the eventual (re)liquidation
    return estimate_interest(r.principal, start, end, corporate=corporate)
