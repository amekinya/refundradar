"""Ledger-level analysis: routes every entry, then builds the headline, deadline radar, blockers,
cost comparison and broker handoff files. Pure code; no model calls."""
from __future__ import annotations

import csv
import io
from collections import Counter, defaultdict
from dataclasses import asdict, replace
from datetime import UTC, date, datetime, timedelta

from app.engine import catalog as C
from app.engine import costs
from app.engine import entry_number as EN
from app.engine.models import Entry, Profile, Route
from app.engine.rules import route_entry

ACTIONABLE = {"cape_now", "fix_first"}


def analyze(entries: list[Entry], profile: Profile, today: date | None = None) -> dict:
    today = today or date.today()
    # Duplicate entry numbers would sink a CAPE file; route each once and flag the rest. An entry number that couldn't
    # be read at all isn't a duplicate of another unreadable one: each keeps its own row, with a placeholder name.
    seen: Counter[str] = Counter(k for k in (EN.normalize(e.entry_number) for e in entries) if k)
    unique: dict[str, Entry] = {}
    blank = 0
    for e in entries:
        k = EN.normalize(e.entry_number)
        if not k:
            blank += 1
            k, e = f"\0{blank}", replace(e, entry_number=f"Unreadable entry {blank}")
        unique.setdefault(k, e)
    routes = [route_entry(e, profile, today) for e in unique.values()]
    for r in routes:
        if r.entry_number.startswith("Unreadable entry"):
            r.flags.append("unreadable_number")
            r.notes.append("The entry number couldn't be read. Copy it from box 1 of the form before anything is filed.")

    by_bucket: dict[str, dict] = {k: {"count": 0, "principal": 0.0, "interest": 0.0} for k in C.BUCKETS}
    for r in routes:
        b = by_bucket[r.bucket]
        b["count"] += 1
        b["principal"] = round(b["principal"] + r.principal, 2)
        b["interest"] = round(b["interest"] + r.interest, 2)

    mine = [r for r in routes if r.holder == "you"]
    theirs = [r for r in routes if r.holder != "you" and r.principal > 0]
    reachable = [r for r in mine if r.bucket in ACTIONABLE]
    total_principal = round(sum(r.principal for r in routes if r.bucket != "not_eligible"), 2)
    total_interest = round(sum(r.interest for r in routes if r.bucket != "not_eligible"), 2)

    # "Leaves the refund tool within 3 weeks" is part of what's claimable now; entries that need a decision first
    # (estimated dates, open protests) are counted separately so the urgent amount never exceeds the claimable one.
    near = lambda r: r.deadline_type == "CAPE_80" and r.days_left is not None and 0 <= r.days_left <= 21  # noqa: E731
    urgent = sorted([r for r in reachable if near(r)], key=lambda r: r.days_left)
    urgent_other = sorted([r for r in mine if near(r) and r.bucket not in ACTIONABLE], key=lambda r: r.days_left)
    headline = {
        "total_principal": total_principal,
        "total_interest": total_interest,
        "reachable_now": _sum(reachable),
        # Range: low assumes '15% all-in' lines refund nothing and simple (not daily-compounded) interest;
        # high assumes the higher non-corporate overpayment rate (7% vs 6%). See README "Estimates".
        "reachable_low": round(sum(r.principal - r.all_in_duty + 0.97 * r.interest for r in reachable), 2),
        "reachable_high": round(sum(r.principal + r.interest * (7 / 6 if profile.corporate else 1.0) for r in reachable), 2),
        "reachable_now_count": len(reachable),
        "urgent_count": len(urgent),
        "urgent_amount": _sum(urgent),
        "urgent_soonest_days": urgent[0].days_left if urgent else None,
        "urgent_needs_decision_count": len(urgent_other),
        "urgent_needs_decision_amount": _sum(urgent_other),
        "urgent_needs_decision_soonest_days": urgent_other[0].days_left if urgent_other else None,
        "protest_amount": _sum([r for r in mine if r.bucket == "protest"]),
        "litigation_amount": _sum([r for r in mine if r.bucket == "litigation"]),
        "blocked_amount": _sum([r for r in mine if r.bucket == "blocked"]),  # waiting on CBP (surety, drawback, warehouse...)
        "review_amount": _sum([r for r in mine if r.bucket == "review"]),  # ask your broker / confirm in ACE first
        "someone_else_amount": _sum(theirs),
        "someone_else_count": len(theirs),
        "entries": len(routes),
        "duplicates": sum(c - 1 for c in seen.values() if c > 1),
    }

    blockers = _blockers(routes, profile, seen, reachable)
    radar = _radar(routes, today)
    options = costs.compare(len(reachable), headline["reachable_now"])
    return {
        "today": today.isoformat(),
        "rules_verified_as_of": C.RULES_VERIFIED_AS_OF.isoformat(),
        "headline": headline,
        "buckets": by_bucket,
        "bucket_meta": {k: asdict(v) for k, v in C.BUCKETS.items()},
        "blockers": blockers,
        "radar": radar,
        "costs": [asdict(o) for o in options],
        "routes": [_route_json(r) for r in sorted(routes, key=_sort_key)],
    }


def _sum(rs: list[Route]) -> float:
    return round(sum(r.principal + r.interest for r in rs), 2)


def _sort_key(r: Route):
    order = ["cape_now", "fix_first", "protest", "review", "waiting", "blocked", "litigation", "not_eligible"]
    return (order.index(r.bucket), r.days_left if r.days_left is not None else 10**6, -r.principal)


def _route_json(r: Route) -> dict:
    d = asdict(r)
    for k in ("deadline", "liquidation_date"):
        d[k] = d[k].isoformat() if d[k] else None
    d["sources"] = list(r.sources)
    d["programs"] = list(r.programs)
    return d


def _blockers(routes: list[Route], p: Profile, seen: Counter, reachable: list[Route]) -> list[dict]:
    out: list[dict] = []
    stake = _sum(reachable)

    def add(key, severity, title, detail, fix):
        out.append({"key": key, "severity": severity, "title": title, "detail": detail, "fix": fix})

    if p.has_ace_account is not True and reachable:
        add("ace", "high", "No ACE Portal account confirmed",
            "Every CAPE filing and every refund report runs through ACE. Setup has taken anywhere from 1 day to 6 weeks, and entries keep aging meanwhile.",
            "Apply for an ACE Portal importer account now (or have your broker file CAPE for the entries they filed).")
    if p.ach_refund_enrolled is not True and (reachable or stake > 0):
        add("ach", "high", "Refund bank account not confirmed",
            f"CBP pays refunds only electronically. As of Oct 2, 2026 it was holding 20,362 approved refunds (~$1.1B) for missing bank details. Your ${stake:,.0f} could sit there too.",
            "In ACE: Importer sub-account → ACH Refund Authorization tab (separate from ACH payment). If a refund was already held, email frn-achrefundsupport@cbp.dhs.gov.")
    if p.contact_email_current is False:
        add("5106", "medium", "Importer contact details out of date",
            "CBP uses your Form 5106 record for account setup and notices.", "Update your 5106 point of contact through your broker or ACE.")
    groups = defaultdict(list)
    for r in routes:
        groups[r.rule_id].append(r)
    if groups.get("R2"):
        add("surety", "high", f"{len(groups['R2'])} surety-paid entries", "CBP says don't file these; no surety process exists yet.", "Tell your surety; keep records.")
    if groups.get("R8"):
        add("protest", "medium", f"{len(groups['R8'])} entries with an open protest", "CAPE rejects protested entries.", "Decide per entry: withdraw (IEEPA-only, within 80 days) or keep.")
    if groups.get("R6"):
        add("drawback", "medium", f"{len(groups['R6'])} entries on drawback", "CAPE rejects these for now.", "If drawback isn't filed yet on other entries, file CAPE first.")
    if groups.get("R19"):
        add("psc", "medium", f"{len(groups['R19'])} entries need a correction first", "A PSC is blocked once CAPE accepts the entry.", "File PSCs before the CAPE declaration.")
    theirs = [r for r in routes if r.holder != "you" and r.principal > 0]
    if theirs:
        add("holder", "high", f"{len(theirs)} entries where someone else holds the claim",
            f"${_sum(theirs):,.0f} in IEEPA duty sits on entries where you weren't the importer of record (courier, forwarder or supplier).",
            "Ask that party to file and pass the refund through; couriers run their own programs. There's no federal pass-through rule, so check your contract.")
    bad_nums = [r for r in routes if any("must be 11" in p_ or "digits" in p_ for p_ in r.entry_problems) and "unreadable_number" not in r.flags]
    if bad_nums:
        add("format", "high", f"{len(bad_nums)} entry numbers in the wrong format", "CAPE rejects anything that isn't 11 characters.", "Fix these before your broker files.")
    flagged = lambda key: [r for r in routes if key in r.flags]  # noqa: E731
    if flagged("unparsed"):
        n = len(flagged("unparsed"))
        add("unparsed", "high", f"{n} entr{'ies' if n > 1 else 'y'} with dates or amounts we couldn't read",
            "We didn't guess them. Entries with an unreadable date are set aside for you to confirm in ACE instead of being "
            "routed as claimable; an unreadable duty counts as $0.",
            "Fix those cells (dates like 2025-03-01 or 03/01/2025, amounts like 1234.50) and upload again, or check the entries in ACE.")
    if flagged("duty_mismatch"):
        n = len(flagged("duty_mismatch"))
        add("dutycheck", "high", f"{n} form photo{'s' if n > 1 else ''} where the duties don't add up",
            "The tariff-line duties read from the photo don't add up to the form's own total (Block 37), so a digit was "
            "probably misread or a line missed. The refund amounts for those entries may be off.",
            "Open the photo and compare the duty column with what we read before relying on the amount.")
    if flagged("check_digit_photo") or flagged("unreadable_number"):
        n = len(flagged("check_digit_photo")) + len(flagged("unreadable_number"))
        add("photonum", "high", f"{n} entry number{'s' if n > 1 else ''} from photos to check",
            "These don't pass CBP's check digit (or couldn't be read), so they're probably misread. They're left out of the "
            "broker entry list.", "Read the entry number off box 1 of the form and correct it before your broker files.")
    dups = sum(c - 1 for c in seen.values() if c > 1)
    if dups:
        add("dupes", "medium", f"{dups} duplicate entry numbers removed", "Duplicates are rejected within a file and across declarations.", "Keep each entry once.")
    if any(r.all_in_overstated for r in routes):
        add("allin", "low", "Some estimates run high", "'15% all-in' deal lines (EU, Japan, Korea, Switzerland) refund only the part above normal duty.", "Expect CBP's figure to be lower on those entries.")
    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(out, key=lambda b: order[b["severity"]])


def _radar(routes: list[Route], today: date) -> dict:
    """Group deadlines by week for the timeline, plus the key fixed dates."""
    weeks: dict[str, dict] = {}
    for r in routes:
        if not r.deadline or r.holder != "you" or r.days_left is None or r.days_left < 0:
            continue
        monday = r.deadline - timedelta(days=r.deadline.weekday())
        w = weeks.setdefault(monday.isoformat(), {"week_of": monday.isoformat(), "CAPE_80": [0, 0.0], "PROTEST_180": [0, 0.0], "CIT_2YR": [0, 0.0]})
        if r.deadline_type in w:
            w[r.deadline_type][0] += 1
            w[r.deadline_type][1] = round(w[r.deadline_type][1] + r.principal + r.interest, 2)
    return {
        "weeks": [weeks[k] for k in sorted(weeks)],
        "milestones": [
            {"date": C.CLASS_SCHEDULING_ORDER_DUE.isoformat(), "label": "Class action scheduling order due (no relief ordered yet)"},
            {"date": C.EARLIEST_CIT_DEADLINE.isoformat(), "label": "Earliest court-filing deadlines cited (Feb 1-4, 2027)"},
        ],
    }


# --- Exports -----------------------------------------------------------------------------
def handoff_entry_list(report: dict) -> list[str]:
    """Pre-checked entry numbers for the broker: actionable, yours, valid format, de-duplicated."""
    out = []
    for r in report["routes"]:
        if r["bucket"] in ACTIONABLE and r["holder"] == "you":
            e = EN.normalize(r["entry_number"])
            if len(e) == 11 and e[3:].isdigit() and "check_digit_photo" not in r.get("flags", ()):
                out.append(e)
    return out


def handoff_csv(report: dict) -> str:
    """Worksheet for the broker. Same single column CBP's template uses, so it can be reviewed and reused."""
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Entry Number"])
    for e in handoff_entry_list(report)[: C.MAX_ENTRIES_PER_DECLARATION]:
        w.writerow([e])
    return buf.getvalue()


def worksheet_csv(report: dict) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Entry Number", "Route", "Rule", "IEEPA duty (est.)", "Interest (est.)", "Deadline", "Deadline type",
                "Days left", "Liquidation date", "Liquidation estimated", "Holder", "Action", "Notes"])
    for r in report["routes"]:
        w.writerow([r["entry_number"], C.BUCKETS[r["bucket"]].label, r["rule_id"], f"{r['principal']:.2f}", f"{r['interest']:.2f}",
                    r["deadline"] or "", r["deadline_type"], "" if r["days_left"] is None else r["days_left"],
                    r["liquidation_date"] or "", "yes" if r["liquidation_estimated"] else "", r["holder"], r["action"],
                    " | ".join(r["notes"])])
    return buf.getvalue()


def deadlines_ics(report: dict) -> str:
    now = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//RefundRadar//EN", "CALSCALE:GREGORIAN"]
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in report["routes"]:
        if r["deadline"] and r["holder"] == "you" and (r["days_left"] or 0) >= 0:
            groups[(r["deadline"], r["deadline_type"])].append(r)
    names = {"CAPE_80": "CAPE window closes", "PROTEST_180": "Protest deadline", "CIT_2YR": "Court-filing decision point"}
    for i, ((d, t), rs) in enumerate(sorted(groups.items())):
        ds = d.replace("-", "")
        amount = sum(x["principal"] + x["interest"] for x in rs)
        nums = ", ".join(x["entry_number"] for x in rs[:20]) + (" ..." if len(rs) > 20 else "")
        lines += [
            "BEGIN:VEVENT", f"UID:refundradar-{ds}-{t}-{i}@refundradar", f"DTSTAMP:{now}",
            f"DTSTART;VALUE=DATE:{ds}", f"SUMMARY:{names.get(t, t)}: {len(rs)} entries (~${amount:,.0f})",
            f"DESCRIPTION:Entries: {nums}. Estimates only; confirm in ACE.",
            "BEGIN:VALARM", "TRIGGER:-P7D", "ACTION:DISPLAY", "DESCRIPTION:Refund deadline in 7 days", "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"
