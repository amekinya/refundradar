"""Where the NVIDIA models do work code can't. Every function has a no-key fallback so the app always runs.

- map_headers   Nemotron 3 Nano   (fast, no reasoning): map an unfamiliar spreadsheet to our fields
- read_form     Nemotron 3.5 Super VL (vision, strict JSON): photo/PDF page of a Form 7501 -> review grid
- action_plan   Nemotron 3 Ultra  (reasoning, long context): the whole ledger + rules -> prioritized plan
- explain_entry Nemotron 3 Ultra  (reasoning): why an unusual entry routes the way it does
- offer_check   Nemotron 3 Ultra + Tavily: is this refund offer predatory or a scam, and what would it cost?
- freshness     Tavily + Nemotron 3 Nano: has CBP/court guidance changed since our rules date?

Money, dates and routes are never taken from a model: models get engine outputs as facts.
"""
from __future__ import annotations

import base64
import json
import re
import time
from datetime import date
from typing import Any

from app.ai.client import CallRecord, LiveModelUnavailable, chat, chat_json
from app.config import settings
from app.engine import catalog as C
from app.engine.costs import offer_cost
from app.engine.es003 import CANON

# ---------------------------------------------------------------------------------------
# 1. Spreadsheet header mapping (Nano)
# ---------------------------------------------------------------------------------------
HEADER_SCHEMA = {
    "type": "object",
    "properties": {
        "mapping": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {"header": {"type": "string"}, "field": {"type": "string", "enum": list(CANON) + ["ignore"]}},
                "required": ["header", "field"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["mapping"],
    "additionalProperties": False,
}


def map_headers(headers: list[str], sample_rows: list[dict], calls: list[CallRecord] | None = None) -> dict[str, str]:
    fields = {k: v[0] for k, v in CANON.items()}
    prompt = (
        "Map each spreadsheet column to one field of a US customs entry-summary schema, or 'ignore'.\n"
        f"Fields (name: meaning): {json.dumps(fields)}\n"
        "Rules: one column per field at most; 'duty' is the duty dollars on that tariff line; 'hts' is the tariff number.\n"
        f"Columns: {json.dumps(headers)}\nSample rows: {json.dumps(sample_rows[:3])}"
    )
    out = chat_json(settings.nano, [{"role": "user", "content": prompt}], schema=HEADER_SCHEMA,
                    purpose="Map spreadsheet columns", reasoning=False, max_tokens=800, calls=calls)
    return {m["header"]: m["field"] for m in out.get("mapping", []) if m.get("field") != "ignore"}


# ---------------------------------------------------------------------------------------
# 2. Form 7501 photo -> review grid (Super VL)
# ---------------------------------------------------------------------------------------
FORM_SCHEMA = {
    "type": "object",
    "properties": {
        "entry_number": {"type": "string"},
        "entry_type": {"type": "string"},
        "entry_date": {"type": "string", "description": "MM/DD/YYYY"},
        "importer_number": {"type": "string"},
        "importer_name": {"type": "string"},
        "broker_or_filer": {"type": "string"},
        "country_of_origin": {"type": "string"},
        "lines": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "line_no": {"type": "string"},
                    "hts_numbers": {"type": "array", "items": {"type": "string"}},
                    "duties": {"type": "array", "items": {"type": "number"}},
                },
                "required": ["line_no", "hts_numbers", "duties"],
                "additionalProperties": False,
            },
        },
        "total_duty": {"type": "number"},
        "unreadable_fields": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["entry_number", "entry_type", "entry_date", "importer_number", "importer_name", "broker_or_filer",
                 "country_of_origin", "lines", "total_duty", "unreadable_fields"],
    "additionalProperties": False,
}

FORM_PROMPT = (
    "This is a photo or scan of a US CBP Form 7501 (Entry Summary). Extract exactly what is printed; never guess.\n"
    "- entry_number: Block 1, format XXX-XXXXXXX-X: a 3-character filer code (letters and digits; tell the letter Q from the digit 0, "
    "Z from 2, K from M), exactly 7 digits, then 1 check digit.\n- entry_type: Block 2 (2 digits).\n"
    "- entry_date: Block 7, labeled 'Entry Date' (top right). Not Block 3 'Summary Date' and not Block 11 'Import Date'.\n"
    "- importer_number and importer_name: the Importer of Record number and name (Block 23/26 on older forms, 27/30 on the 2026 form).\n"
    "- broker_or_filer: the broker/filer named in the declarant/broker block, if visible.\n"
    "- lines: for each line number in column 27, every HTSUS number listed in column 29 for that line (Chapter 99 numbers like 9903.01.25 "
    "usually sit above or below the regular 10-digit number) and, in the same order, the duty dollars printed opposite each in column 34 (0 if blank).\n"
    "- total_duty: Block 37.\n- unreadable_fields: list any field you could not read with confidence. Use empty strings for unknown text."
)


def read_form(image_bytes: bytes, mime: str = "image/jpeg", calls: list[CallRecord] | None = None) -> dict[str, Any]:
    b64 = base64.b64encode(image_bytes).decode()
    return chat_json(
        settings.super_vl,
        [{"role": "user", "content": [
            {"type": "text", "text": FORM_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        ]}],
        schema=FORM_SCHEMA, purpose="Read Form 7501 photo", reasoning=False, max_tokens=2000, calls=calls,
    )


# ---------------------------------------------------------------------------------------
# 3. Action plan over the whole ledger (Ultra)
# ---------------------------------------------------------------------------------------
PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "when": {"type": "string"},
                    "do": {"type": "string"},
                    "why": {"type": "string"},
                    "who": {"type": "string", "enum": ["you", "your broker", "counsel", "you or your broker"]},
                },
                "required": ["when", "do", "why", "who"],
                "additionalProperties": False,
            },
        },
        "watch_outs": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "steps", "watch_outs"],
    "additionalProperties": False,
}


def _ledger_brief(report: dict) -> dict:
    """Compact facts for the model: totals, buckets, blockers, deadlines, and every non-routine entry."""
    routine = {"R11", "R12", "R13", "R14", "R0"}
    return {
        "today": report["today"],
        "headline": report["headline"],
        "buckets": {k: v for k, v in report["buckets"].items() if v["count"]},
        "blockers": [{k: b[k] for k in ("severity", "title", "detail")} for b in report["blockers"]],
        "deadline_weeks": report["radar"]["weeks"][:12],
        "milestones": report["radar"]["milestones"],
        "unusual_entries": [
            {k: r[k] for k in ("entry_number", "rule_id", "title", "principal", "deadline", "notes")}
            for r in report["routes"] if r["rule_id"] not in routine
        ][:60],
        "urgent_entries": [
            {k: r[k] for k in ("entry_number", "principal", "deadline", "days_left")}
            for r in report["routes"] if r["deadline_type"] == "CAPE_80" and r["days_left"] is not None and r["days_left"] <= 21
        ],
    }


def _rules_brief() -> str:
    return "\n".join(f"{r.id}: {r.title} -> {C.BUCKETS[r.bucket].label}. {r.action}" for r in C.RULES.values())


PLAN_SYSTEM = (
    "You are RefundRadar's planning assistant for a small US importer reviewing its own IEEPA tariff refund situation.\n"
    "You are not a customs broker or lawyer and never claim to file anything. Refunds are filed only in ACE by the importer or its licensed broker.\n"
    "Use ONLY the facts and numbers given. Never invent amounts, dates, entry numbers or rules. If something is uncertain, say so.\n"
    "Write for a busy business owner: short, concrete, ordered by urgency and money at stake."
)


def action_plan(report: dict, calls: list[CallRecord] | None = None) -> dict:
    content = (
        f"Routing rules in force (verified {report['rules_verified_as_of']}):\n{_rules_brief()}\n\n"
        f"This importer's analysis (computed by a deterministic engine; treat as facts):\n{json.dumps(_ledger_brief(report))}\n\n"
        "Write: (1) a 2-sentence summary with the key dollar figures; (2) 4-7 dated steps, most urgent first, each with who does it; "
        "(3) up to 4 watch-outs (things that could cost money or get a filing rejected)."
    )
    return chat_json(settings.ultra, [{"role": "system", "content": PLAN_SYSTEM}, {"role": "user", "content": content}],
                     schema=PLAN_SCHEMA, purpose="Write action plan", reasoning=True, max_tokens=6000, calls=calls)


def action_plan_fallback(report: dict) -> dict:
    h = report["headline"]
    steps = []
    if any(b["key"] == "ach" for b in report["blockers"]):
        steps.append({"when": "Today", "do": "Set up refund bank details in ACE (ACH Refund Authorization tab).",
                      "why": "CBP only pays refunds electronically; without it every approved refund is held.", "who": "you"})
    if h["urgent_count"]:
        steps.append({"when": f"Within {h['urgent_soonest_days']} days", "do": f"File the {h['urgent_count']} entries closest to the 80-day CAPE cutoff.",
                      "why": f"About ${h['urgent_amount']:,.0f} drops out of CAPE if they're not accepted in time.", "who": "you or your broker"})
    if h["reachable_now_count"]:
        steps.append({"when": "This week", "do": f"File the remaining CAPE-eligible entries ({h['reachable_now_count']} total).",
                      "why": f"About ${h['reachable_now']:,.0f} is claimable now.", "who": "you or your broker"})
    if h["protest_amount"]:
        steps.append({"when": "Before each protest deadline", "do": "Ask your broker about protests for entries 81-180 days past liquidation.",
                      "why": f"About ${h['protest_amount']:,.0f} has no CAPE path today.", "who": "your broker"})
    if h["litigation_amount"]:
        steps.append({"when": "Before Feb 1, 2027", "do": "Talk to counsel about entries past the protest window.",
                      "why": f"About ${h['litigation_amount']:,.0f} can only be recovered through court or class relief.", "who": "counsel"})
    return {"summary": f"About ${h['total_principal'] + h['total_interest']:,.0f} in IEEPA duty and interest is on your entries; "
                       f"${h['reachable_now']:,.0f} is claimable in CAPE now.",
            "steps": steps, "watch_outs": [], "fallback": True}


# ---------------------------------------------------------------------------------------
# 4. Explain one unusual entry (Ultra)
# ---------------------------------------------------------------------------------------
def explain_entry(route: dict, calls: list[CallRecord] | None = None) -> str:
    rule = C.RULES[route["rule_id"]]
    content = (
        f"Entry facts (from our engine): {json.dumps({k: route[k] for k in ('entry_number', 'title', 'principal', 'interest', 'deadline', 'deadline_type', 'days_left', 'liquidation_date', 'liquidation_estimated', 'programs', 'notes')})}\n"
        f"Rule applied: {rule.id} — {rule.title}. Action: {rule.action}. Sources: {', '.join(rule.sources)}. Confidence tag: {rule.tag}.\n"
        "In 3-4 plain sentences for a small business owner: what this means, what to do and by when, and what's uncertain. No new facts."
    )
    return chat(settings.ultra, [{"role": "system", "content": PLAN_SYSTEM}, {"role": "user", "content": content}],
                purpose=f"Explain entry {route['entry_number']}", reasoning=True, max_tokens=2500, calls=calls).strip()


# ---------------------------------------------------------------------------------------
# 5. Offer check (Ultra + Tavily)
# ---------------------------------------------------------------------------------------
OFFER_SCHEMA = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "fee_percent": {"type": "number", "description": "percent of refund, 0 if none"},
        "fee_flat": {"type": "number"},
        "fee_per_entry": {"type": "number"},
        "fee_minimum": {"type": "number"},
        "red_flags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "flag": {"type": "string", "enum": [
                        "asks_for_ace_login", "asks_for_bank_details", "claims_to_be_cbp_or_government", "unsolicited_contact",
                        "urgency_pressure", "upfront_payment", "guarantees_refund", "vague_fees", "processes_refunds_outside_ace",
                        "qr_code_or_link_to_pay", "other"]},
                    "evidence": {"type": "string"},
                },
                "required": ["flag", "evidence"],
                "additionalProperties": False,
            },
        },
        "green_flags": {"type": "array", "items": {"type": "string"}},
        "advice": {"type": "string"},
    },
    "required": ["company_name", "fee_percent", "fee_flat", "fee_per_entry", "fee_minimum", "red_flags", "green_flags", "advice"],
    "additionalProperties": False,
}

CBP_FRAUD_GUIDANCE = (
    "CBP CSMS #68569567 (May 7, 2026): CBP never asks importers to pay to receive a refund; refunds are requested only through ACE/CAPE "
    "by the importer of record or its licensed broker; any external website or unknown party offering to process refunds is likely fraudulent; "
    "never share ACE credentials or bank details with unknown parties."
)


def _tavily_company_check(company: str) -> list[dict]:
    if not company or not settings.live_tavily:
        return []
    from tavily import TavilyClient

    t = TavilyClient(api_key=settings.tavily_api_key)
    res = t.search(f'"{company}" tariff refund reviews OR complaints OR scam OR licensed customs broker', max_results=5)
    return [{"title": r.get("title", ""), "url": r.get("url", ""), "snippet": (r.get("content") or "")[:400]} for r in res.get("results", [])]


HARD_FLAGS = {"asks_for_ace_login", "asks_for_bank_details", "claims_to_be_cbp_or_government", "upfront_payment",
              "processes_refunds_outside_ace", "qr_code_or_link_to_pay"}  # each is something CBP says a legitimate filer never does
SOFT_FLAGS = {"urgency_pressure", "guarantees_refund"}  # two together also mean likely scam
EXPENSIVE_PCT = 20.0  # contingency firms we found charge 20-35%; licensed brokers charge flat fees of roughly $100-200 per declaration
_NEGATION = re.compile(r"\b(never|no|not|don't|doesn't|won't|cannot|can't)\b")
_W = r"\W+(?:[\w$.,'-]+\W+){0,%d}?"
# What each flag means, as a pattern over one sentence of the offer. A flag counts only if its sentence matches and isn't negated.
FLAG_RX = {
    "asks_for_ace_login": re.compile(r"\b(send|provide|share|reply with|give|enter|grant|need)\b" + _W % 6 + r"(login|password|credential|username)"),
    "asks_for_bank_details": re.compile(r"\b(send|provide|share|reply with|confirm|enter|give|email)\b" + _W % 8 + r"(bank|routing|account number|banking)"),
    "claims_to_be_cbp_or_government": re.compile(r"\b(authorized by|on behalf of|records from|partner(?:ed)? with)\b" + _W % 5
                                                 + r"(cbp|customs and border|u\.s\. customs|government|treasury)|\bofficial\b" + _W % 3 + r"(refund|partner|processing|agent)"),
    "upfront_payment": re.compile(r"\b(upfront|up-front|up front|in advance)\b|\b(release|processing|activation|filing|onboarding|setup|set-up)\s+fee\b"
                                  r"|\b(pay|wire|send)\b" + _W % 5 + r"(fee|\$\d)"),
    "processes_refunds_outside_ace": re.compile(r"\b(outside|bypass(?:ing)?|instead of)\b" + _W % 4 + r"(ace|cbp|queue|customs)|directly with customs"),
    "qr_code_or_link_to_pay": re.compile(r"\bqr code\b|\bscan the code\b|\bclick\b" + _W % 3 + r"(link|here|below)|\blink below\b"),
    "urgency_pressure": re.compile(r"\b(act now|immediately|within \d+ hours|\d+ hours left|today|final notice|last chance|urgent|forfeit\w*|expires?)\b"),
    "guarantees_refund": re.compile(r"\bguarantee"),
}


def _sentences(text: str) -> list[str]:
    """Sentences, with each bullet of a list joined to the line that introduces it ('reply with:' + '- your password')."""
    out, intro = [], ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            intro = ""
            continue
        bullet = re.match(r"^[\u2022*\-\u2013]\s*(.+)", line)
        if bullet and intro:
            out.append(f"{intro} {bullet.group(1)}")
            continue
        parts = [x.strip() for x in re.split(r"(?<=[.!?])\s+", line) if x.strip()]
        out += parts
        intro = parts[-1] if parts and parts[-1].endswith(":") else ""
    return out


def _flag_in(flag: str, sentence: str) -> str | None:
    """The matched words if the sentence does what the flag says (and doesn't say it doesn't)."""
    rx = FLAG_RX.get(flag)
    m = rx.search(sentence.lower()) if rx else None
    if m and not _NEGATION.search(sentence.lower()[: m.start()]):
        return m.group(0)
    return None


def find_flags(text: str) -> list[dict]:
    """Every red flag the patterns find, quoting its sentence."""
    out = {}
    for sent in _sentences(text):
        for flag in FLAG_RX:
            if flag not in out and _flag_in(flag, sent):
                out[flag] = {"flag": flag, "evidence": sent[:200]}
    return list(out.values())


def _verified(flag: dict, text: str) -> bool:
    """A model-proposed flag counts only if its quote is really in the offer and that sentence matches the flag's meaning."""
    norm = lambda x: re.sub(r"\s+", " ", x.lower()).strip(" .\"'")  # noqa: E731
    e = norm(flag.get("evidence", ""))
    if len(e) < 8 or e not in norm(text):
        return False
    return any(e in norm(sent) and _flag_in(flag["flag"], sent) for sent in _sentences(text))


def offer_verdict(flags: list[dict], effective_pct: float, priced: bool) -> str:
    """Code decides the verdict from the checked flags and the offer's cost on the user's own numbers."""
    names = {f["flag"] for f in flags}
    if names & HARD_FLAGS or len(names & SOFT_FLAGS) >= 2:
        return "likely_scam"
    if priced and effective_pct >= EXPENSIVE_PCT:
        return "expensive"
    return "reasonable"


def offer_check(offer_text: str, refund_estimate: float, entries: int, calls: list[CallRecord] | None = None) -> dict:
    """Nemotron 3 Ultra reads the fee terms (percent, flat, per entry, minimum: worded a hundred ways) and proposes red flags
    with quotes. Code keeps a flag only if its quote is in the offer and matches the flag's meaning, adds any the patterns find,
    prices the offer on the user's own numbers, and decides the verdict."""
    first = chat_json(
        settings.ultra,
        [{"role": "system", "content": "You analyze refund-recovery offers sent to small US importers. Be precise and fair. "
                                      "List a red flag only when the offer itself does that thing, and quote the exact sentence as evidence. "
                                      "Statements that the sender does NOT do something (e.g. 'we never ask for passwords') are green flags. "
                                      "Charging a fee is not a red flag by itself; upfront_payment means money due before any refund arrives."},
         {"role": "user", "content": f"{CBP_FRAUD_GUIDANCE}\n\nOffer text:\n\"\"\"\n{offer_text[:6000]}\n\"\"\"\n\n"
                                     "Extract the fee terms (0 when not stated) and the red and green flags. "
                                     "advice: one or two sentences on what to ask or check before replying; don't give a verdict."}],
        schema=OFFER_SCHEMA, purpose="Check refund offer", reasoning=False, max_tokens=2500, calls=calls,
    )
    proposed = first.get("red_flags", [])
    flags = {f["flag"]: f for f in proposed if _verified(f, offer_text)}
    for f in find_flags(offer_text):
        flags.setdefault(f["flag"], f)
    try:
        web = _tavily_company_check(first.get("company_name", ""))
    except Exception:  # noqa: BLE001  (the web lookup is extra evidence, never a reason to fail the check)
        web = []
    priced = any(first.get(k) for k in ("fee_percent", "fee_flat", "fee_per_entry", "fee_minimum"))
    fee, pct = offer_cost(refund_estimate, percent=first["fee_percent"] or None, flat=first["fee_flat"] or None,
                          per_entry=first["fee_per_entry"] or None, entries=entries, minimum=first["fee_minimum"] or None)
    checked = list(flags.values())
    return {**first, "red_flags": checked, "model_flags_rejected": sum(not _verified(f, offer_text) for f in proposed),
            "verdict": offer_verdict(checked, pct, priced), "cost_on_your_numbers": fee, "effective_pct": pct, "web_results": web}


def offer_check_fallback(offer_text: str, refund_estimate: float, entries: int) -> dict:
    t = offer_text.lower()
    flags = find_flags(offer_text)
    m = re.search(r"(\d{1,2}(?:\.\d+)?)\s*%", t)
    pct_in = float(m.group(1)) if m else None
    flat = re.search(r"\$\s?([\d,]+(?:\.\d\d)?)\s*(?:one-time\s+)?(?:processing|activation|setup|filing|upfront)?\s*fee", t)
    flat_v = float(flat.group(1).replace(",", "")) if flat else None
    fee, pct = offer_cost(refund_estimate, percent=pct_in, flat=flat_v)
    verdict = offer_verdict(flags, pct, bool(pct_in or flat_v))
    return {"company_name": "", "fee_percent": pct_in or 0, "fee_flat": 0, "fee_per_entry": 0, "fee_minimum": 0, "red_flags": flags,
            "green_flags": [], "verdict": verdict, "advice": CBP_FRAUD_GUIDANCE,
            "cost_on_your_numbers": fee, "effective_pct": pct, "web_results": [], "fallback": True}


# ---------------------------------------------------------------------------------------
# 6. Rules freshness (Tavily + Nano), cached for 12 hours
# ---------------------------------------------------------------------------------------
_fresh_cache: dict[str, Any] = {}

FRESH_SCHEMA = {
    "type": "object",
    "properties": {
        "changed": {"type": "boolean"},
        "items": {"type": "array", "items": {"type": "object", "properties": {
            "date": {"type": "string"}, "what": {"type": "string"}, "url": {"type": "string"},
            "affects": {"type": "string", "enum": ["cape_window", "phase3", "protest", "class_action", "appeal", "payment", "other", "none"]}},
            "required": ["date", "what", "url", "affects"], "additionalProperties": False}},
    },
    "required": ["changed", "items"],
    "additionalProperties": False,
}


def freshness(calls: list[CallRecord] | None = None) -> dict:
    now = time.time()
    if _fresh_cache.get("at", 0) > now - 12 * 3600:
        return _fresh_cache["data"]
    if not settings.live_tavily:
        return {"checked": False, "rules_verified_as_of": C.RULES_VERIFIED_AS_OF.isoformat(), "items": []}
    from tavily import TavilyClient

    t = TavilyClient(api_key=settings.tavily_api_key)
    results = []
    for q in ("CBP CAPE IEEPA refund update", "IEEPA refund Court of International Trade order", "IEEPA tariff refund Federal Circuit appeal decision"):
        res = t.search(q, topic="news", days=30, max_results=5)
        results += [{"title": r.get("title", ""), "url": r.get("url", ""), "date": r.get("published_date", ""),
                     "snippet": (r.get("content") or "")[:500]} for r in res.get("results", [])]
    data = {"checked": True, "rules_verified_as_of": C.RULES_VERIFIED_AS_OF.isoformat(), "items": [], "changed": False}
    # The date cut is code, not the model: only news published after the rules date can be a change.
    seen, newer = set(), []
    for r in results:
        d = _news_date(r["date"])
        if r["url"] in seen or (d is not None and d <= C.RULES_VERIFIED_AS_OF):
            continue
        seen.add(r["url"])
        newer.append(r | {"date": d.isoformat() if d else r["date"]})
    if not newer:
        _fresh_cache.update(at=now, data=data)
        return data
    try:
        out = chat_json(settings.nano, [{"role": "user", "content": (
            f"Our refund rules were verified on {C.RULES_VERIFIED_AS_OF}. Known pending events: CBP status report Oct 26, 2026; "
            "settlement conference Oct 27; class scheduling order due Nov 5; Federal Circuit appeal pending.\n"
            "From these news results (all published after the verification date), list only items that report a real change "
            "or new order affecting IEEPA refunds (CAPE windows, Phase 3 access, protests, class relief, the appeal, payments). "
            f"Ignore background and explainer articles. Copy each url exactly.\nResults: {json.dumps(newer)[:12000]}")}],
            schema=FRESH_SCHEMA, purpose="Check for rule changes", reasoning=False, max_tokens=1500, calls=calls)
        by_url = {r["url"]: r for r in newer}
        items = [i | {"date": by_url[i["url"]]["date"]} for i in out.get("items", []) if i["url"] in by_url and i["affects"] != "none"]
        data.update(changed=bool(items), items=items[:6])
    except LiveModelUnavailable:
        data.update(changed=None, items=[{"date": r["date"], "what": r["title"], "url": r["url"], "affects": "other"} for r in newer[:4]])
    _fresh_cache.update(at=now, data=data)
    return data


def _news_date(s: str) -> date | None:
    from email.utils import parsedate_to_datetime

    s = (s or "").strip()
    try:
        return parsedate_to_datetime(s).date()
    except (TypeError, ValueError, IndexError):
        pass
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        return None
