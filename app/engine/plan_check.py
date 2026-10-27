"""Code checks the action plan Nemotron 3 Ultra writes against the report it was written from.

The model writes the plan; code decides what of it is shown. A step or watch-out is dropped when it
- cites an entry number that isn't in the report,
- puts an entry under the wrong kind of action (a warehouse entry listed as an open protest, a drawback entry as surety-paid),
- states an amount for an entry, or any other dollar figure, that the report doesn't contain,
- is dated after the deadline of an entry it cites.
A summary with a figure the report doesn't contain is replaced by one written from the numbers. Pure code; no model calls.
"""
from __future__ import annotations

import re
from collections import defaultdict
from datetime import date, timedelta

from app.engine import entry_number as EN

ACTIONABLE = {"cape_now", "fix_first"}

# An entry number as written: B76-0324527-8, or 11 characters with a letter in the filer code.
ENTRY_RX = re.compile(r"\b(?:[A-Z0-9]{3}-\d{7}-\d|(?=[A-Z0-9]{0,2}[A-Z])[A-Z0-9]{3}\d{8})\b")
MONEY_RX = re.compile(r"\$\s?(\d[\d,]*(?:\.(\d+))?)(\s?(?:[kK]|[mMbB]|bn|thousand|million|billion)\b)?")
AFTER_ENTRY_AMOUNT = re.compile(r"^\s*[(:,–—-]?\s*\$\s?(\d[\d,]*(?:\.\d+)?)(?!\s?(?:[kKmMbB]|bn|thousand|million|billion)\b)")
ISO_RX = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
MONTH_RX = re.compile(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s+(20\d{2}))?\b", re.I)
MONTHS = {m: i + 1 for i, m in enumerate(("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"))}

# What kind of action a step is about (the first of these named in its "do"), and which routes fit it.
TOPICS: list[tuple[str, re.Pattern, object]] = [
    ("surety", re.compile(r"\bsurety", re.I), lambda r: r["rule_id"] == "R2"),
    ("drawback", re.compile(r"\bdrawback", re.I), lambda r: r["rule_id"] == "R6"),
    ("warehouse", re.compile(r"\bwarehouse|\btypes? 2[12]\b|\bwithdrawal entr", re.I), lambda r: r["rule_id"] == "R5"),
    ("correction", re.compile(r"\bpost[- ]summary correction|\bPSCs?\b", re.I), lambda r: r["rule_id"] == "R19"),
    ("protest", re.compile(r"\bprotest", re.I), lambda r: r["bucket"] == "protest" or r["rule_id"] in {"R8", "R8b", "R0b"}),
    ("reconciliation", re.compile(r"\breconciliation|\brecon\b", re.I), lambda r: r["rule_id"] in {"R7", "R7b"}),
    ("court", re.compile(r"\bcourt\b|\bCIT\b|\bcounsel\b|\blitigat|\bclass action", re.I),
     lambda r: r["bucket"] == "litigation" or r["rule_id"] in {"R15", "R15b", "R8b"}),
    ("cape", re.compile(r"\bCAPE\b|\brefund tool\b", re.I),
     lambda r: r["bucket"] in ACTIONABLE or r["deadline_type"] == "CAPE_80"),
]


def _amount(s: str) -> float:
    return float(s.replace(",", ""))


def _close(a: float, b: float, decimals: int = 0) -> bool:
    return abs(a - b) <= max(1.0, 0.5 * 10 ** -decimals)


def _known_amounts(report: dict) -> list[float]:
    """Every dollar figure the report itself contains or that's a plain total of its parts."""
    h = report["headline"]
    vals = [float(v) for v in h.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    vals.append(h["total_principal"] + h["total_interest"])
    for b in report["buckets"].values():
        vals += [b["principal"], b["interest"], b["principal"] + b["interest"]]
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in report["routes"]:
        groups[r["rule_id"]].append(r)
        groups["b:" + r["bucket"]].append(r)
        if r["holder"] == "you":
            groups["mine:" + r["bucket"]].append(r)
    for rs in groups.values():
        vals += [sum(r["principal"] for r in rs), sum(r["principal"] + r["interest"] for r in rs)]
    for b in report.get("blockers", []):  # figures code already wrote into the blockers
        for m in MONEY_RX.finditer(f"{b.get('title', '')} {b.get('detail', '')} {b.get('fix', '')}"):
            if not m.group(3):
                vals.append(_amount(m.group(1)))
    return vals


def _when(when: str, today: date) -> date | None:
    w = when.strip()
    d = None
    if m := ISO_RX.search(w):
        try:
            d = date(int(m[1]), int(m[2]), int(m[3]))
        except ValueError:
            return None
    elif m := MONTH_RX.search(w):
        year = int(m[3]) if m[3] else today.year
        try:
            d = date(year, MONTHS[m[1][:3].lower()], int(m[2]))
        except ValueError:
            return None
        if not m[3] and d < today - timedelta(days=60):
            d = d.replace(year=year + 1)
    elif re.search(r"\btoday\b|\bimmediately\b|\bnow\b", w, re.I):
        return today
    elif re.search(r"\btomorrow\b", w, re.I):
        return today + timedelta(days=1)
    elif m := re.search(r"\bwithin\s+(\d{1,3})\s+days?\b", w, re.I):
        return today + timedelta(days=int(m[1]))
    elif re.search(r"\bthis week\b", w, re.I):
        return today + timedelta(days=6 - today.weekday())
    if d and re.search(r"\bbefore\b", w, re.I):
        d -= timedelta(days=1)
    return d


def _problems(text: str, do: str, when: str, report: dict, routes: dict[str, dict], known: list[float], today: date) -> list[str]:
    out: list[str] = []
    cited: list[dict] = []
    spans: list[tuple[int, int]] = []
    for m in ENTRY_RX.finditer(text):
        num = EN.normalize(m.group(0))
        r = routes.get(num)
        if r is None:
            out.append(f"{m.group(0)} isn't one of your entries")
            continue
        cited.append(r)
        a = AFTER_ENTRY_AMOUNT.match(text[m.end():m.end() + 16])
        if a:
            spans.append((m.end(), m.end() + a.end()))
            v = _amount(a.group(1))
            if not any(_close(v, x, len(a.group(1).partition(".")[2])) for x in (r["principal"], r["interest"], r["principal"] + r["interest"])):
                out.append(f"{r['entry_number']} is ${r['principal']:,.2f} in the report, not ${v:,.2f}")
    # The kind of action this is, and whether each cited entry is that kind.
    hits = [(m.start(), name, fits) for name, rx, fits in TOPICS if (m := rx.search(do))]
    if hits and cited:
        _, name, fits = min(hits, key=lambda t: t[0])
        for r in cited:
            if not fits(r):
                out.append(f"{r['entry_number']} is listed under {name}, but the report routes it as: {r['title']}")
    # Every other dollar figure must be one the report contains (or a total of the entries cited).
    cited_sums = [sum(r["principal"] for r in cited), sum(r["principal"] + r["interest"] for r in cited)]
    for m in MONEY_RX.finditer(text):
        if m.group(3) or any(s <= m.start() < e for s, e in spans):
            continue  # $1.1B-style outside facts are left to the wording; entry amounts were checked above
        v = _amount(m.group(1))
        if v < 50:
            continue
        if not any(_close(v, x, len(m.group(2) or "")) for x in known + cited_sums):
            out.append(f"${m.group(1)} isn't a figure in your report")
    # Not dated after the deadline of anything it cites.
    d = _when(when, today) if when else None
    dl = [(date.fromisoformat(r["deadline"]), r) for r in cited if r.get("deadline") and (r.get("days_left") or 0) >= 0]
    if d and dl:
        first, r = min(dl, key=lambda t: t[0])
        if d > first:
            out.append(f"dated {d:%b %d} but {r['entry_number']}'s deadline is {first:%b %d, %Y}")
    return out


def check_plan(plan: dict, report: dict) -> dict:
    today = date.fromisoformat(report["today"])
    routes = {EN.normalize(r["entry_number"]): r for r in report["routes"]}
    known = _known_amounts(report)
    dropped: list[dict] = []
    steps = []
    for s in plan.get("steps", []):
        text = f"{s.get('do', '')} {s.get('why', '')}"
        probs = _problems(text, s.get("do", ""), s.get("when", ""), report, routes, known, today)
        if probs:
            dropped.append({"text": f"{s.get('when', '')}: {s.get('do', '')}", "reasons": probs})
        else:
            steps.append(s)
    watch = []
    for w in plan.get("watch_outs", []):
        probs = _problems(w, w, "", report, routes, known, today)
        if probs:
            dropped.append({"text": w, "reasons": probs})
        else:
            watch.append(w)
    summary = plan.get("summary", "")
    summary_probs = _problems(summary, "", "", report, routes, known, today)
    out = dict(plan) | {"steps": steps, "watch_outs": watch}
    from app.ai.tasks import action_plan_fallback  # code-written plan from the same report

    fb = action_plan_fallback(report)
    if summary_probs:
        out["summary"] = fb["summary"]
    if not steps:
        out["steps"] = fb["steps"]
    out["check"] = {"steps_kept": len(steps), "steps_written": len(plan.get("steps", [])), "dropped": dropped,
                    "summary_replaced": bool(summary_probs), "summary_problems": summary_probs, "steps_from_rules": not steps}
    return out
