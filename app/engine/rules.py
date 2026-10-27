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
DATE_LABELS = {"entry_date": "entry date", "liquidation_date": "liquidation date", "deposit_date": "deposit date"}
KNOWN_TYPES = {"01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", "21", "22", "23", "31", "32", "34", "38", "47"}


def _norm_id(s: str) -> str:
    return re.sub(r"[^0-9A-Z]", "", (s or "").upper())


def _one_off(a: str, b: str) -> bool:
    """True if b is a one-character misreading of a (dropped, extra or changed character): photos do that."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    short, long_ = sorted((a, b), key=len)
    return any(long_[:i] + long_[i + 1:] == short for i in range(len(long_)))


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
    all_in_duty = round(sum(l.duty for l in ieepa_lines if normalize_hts(l.hts) in ALL_IN_15), 2)

    # Liquidation: actual if known, else estimated from the entry date (flagged).
    status = (entry.liquidation_status or "").strip().lower()
    informal = etype in {"11", "12"}
    liq = entry.liquidation_date
    estimated = False
    scheduled = None  # a liquidation date still in the future: the entry hasn't liquidated yet
    if liq is not None and liq > today and status != "liquidated":
        scheduled, liq = liq, None
    if informal and liq is None and scheduled is None:
        liq = entry.deposit_date or entry.entry_date  # informal entries liquidate when duty is paid
        estimated = liq is not None
    elif liq is None and scheduled is None and status in {"", "unknown", "liquidated"} and entry.entry_date:
        guess = entry.entry_date + timedelta(days=C.NORMAL_LIQUIDATION_DAYS)
        if status == "liquidated":
            liq, estimated = min(guess, today), True
        elif guess <= today:
            liq, estimated = guess, True
    liquidated = liq is not None and status not in UNLIQUIDATED - {""}
    if status in UNLIQUIDATED - {""} and entry.liquidation_date is None:
        liquidated = False
    days = (today - liq).days if (liquidated and liq) else None

    # Dates we can't trust send the entry to "confirm in ACE" (RX), never to "file now": a liquidated entry routed to
    # CAPE is rejected, and one routed to court-only may still be claimable.
    bad_dates = {k: v for k, v in entry.unparsed.items() if k in DATE_LABELS}
    if bad_dates:
        date_doubt = "Your file has " + " and ".join(f"a {DATE_LABELS[k]} we couldn't read ('{v}')" for k, v in bad_dates.items()) + "."
    elif status == "liquidated" and entry.liquidation_date is None and not informal:
        date_doubt = "Your file says this entry liquidated but gives no liquidation date."
    elif status == "liquidated" and entry.liquidation_date and entry.liquidation_date > today:
        date_doubt = f"Your file says this entry liquidated, but the liquidation date ({entry.liquidation_date:%b %d, %Y}) is in the future."
    elif not status and entry.liquidation_date is None and entry.entry_date is None and entry.deposit_date is None:
        date_doubt = "Your file has no entry date, liquidation status or liquidation date for this entry."
    else:
        date_doubt = ""

    base = dict(
        principal=principal,
        programs=programs,
        all_in_overstated=all_in,
        all_in_duty=all_in_duty,
        liquidation_date=liq if liquidated else None,
        liquidation_estimated=estimated and liquidated,
    )

    def finish(r: Route) -> Route:
        # Who holds the claim?
        mine, theirs = _norm_id(profile.importer_number), _norm_id(entry.importer_number)
        if mine and theirs and entry.source.startswith("photo") and _one_off(mine, theirs):  # spreadsheets are exact
            r.notes.append(f"The importer number reads {entry.importer_number}, one character off yours; treated as yours. Confirm on the form.")
        elif mine and theirs and mine != theirs:
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
        if scheduled:
            r.notes.append(f"Not liquidated yet: your file shows liquidation scheduled for {scheduled:%b %d, %Y}.")
        if all_in:
            r.notes.append("Includes a '15% all-in' deal line: only the part above the normal duty is refundable, so this estimate runs high.")
        if r.deadline:
            r.days_left = (r.deadline - today).days
        r.entry_problems = EN.validate(entry.entry_number)
        if entry.unparsed:
            r.flags.append("unparsed")
            r.entry_problems += [f"{DATE_LABELS.get(k, k).capitalize()} '{v}' couldn't be read" for k, v in entry.unparsed.items()]
            if any(k not in DATE_LABELS for k in entry.unparsed):
                r.notes.append("A duty amount in your file couldn't be read, so it counts as $0 here. Check the amount.")
        if entry.duty_mismatch:
            lines_sum, block_37 = entry.duty_mismatch
            r.flags.append("duty_mismatch")
            r.entry_problems.append(f"Tariff-line duties add up to ${lines_sum:,.2f}, not the ${block_37:,.2f} in Block 37")
            r.notes.append(f"The duties read from the photo add up to ${lines_sum:,.2f}, but the form's total (Block 37) is "
                           f"${block_37:,.2f}. A digit may be misread or a line missed, so this amount may be off. Check the photo.")
        if entry.source.startswith("photo") and r.entry_problems[:1] and r.entry_problems[0].startswith("Check digit"):
            r.flags.append("check_digit_photo")
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

    if date_doubt:
        r = _make(entry, "RX", **base, action=f"{date_doubt} Check the liquidation status and date in ACE (report ES-003 or ES-022) "
                  "before filing anything: a liquidated entry sent to CAPE is rejected, and an unliquidated one may still be claimable.")
        return finish(r)

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
    if estimated and days > C.CAPE_WINDOW_DAYS:
        # Past 80 days only on an estimated date. Keep it out of the protest and court totals until ACE confirms it.
        protest_by = liq + timedelta(days=C.PROTEST_WINDOW_DAYS)
        if informal:
            r = _make(entry, "R16", **base)
        else:
            r = _make(entry, "RX", **base, action=(
                f"We estimated liquidation on about {liq:%b %d, %Y} from the entry date, which would put it past the 80-day CAPE "
                "window. Confirm the liquidation date in ACE (report ES-003 or ES-022) before acting: if the entry hasn't "
                "liquidated (extensions are common), it can still go through CAPE."))
        if protest_by >= today:
            r.notes.append(f"If it did liquidate on about {liq:%b %d, %Y}, the protest deadline would be about {protest_by:%b %d, %Y}.")
        else:
            r.notes.append(f"If it did liquidate on about {liq:%b %d, %Y}, only a court case could recover it (earliest filing "
                           f"deadlines cited: {C.EARLIEST_CIT_DEADLINE:%b %d, %Y}).")
        return finish(r)
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
