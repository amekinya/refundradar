"""Precompute the sample importer's model outputs so the public demo doesn't spend credits on every visit.

Needs NEBIUS_API_KEY (+ TAVILY_API_KEY). Writes data/sample/demo_cache.json:
  forms         Super VL readings of the 3 demo photos
  plan          Ultra action plan for the sample ledger
  explanations  Ultra explanations for a few interesting entries
  offer         Ultra + Tavily check of the sample offer email
  freshness     Tavily + Nano rules-freshness snapshot
  calls         every model call with time, tokens and cost (shown in "How this was worked out")
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from app.ai import tasks
from app.ai.client import CallRecord
from app.engine.plan_check import check_plan
from app.main import build_sample

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "data/sample"


def main():
    calls: list[CallRecord] = []
    forms = {}
    for p in sorted((SAMPLE / "photos").glob("*.jpg")):
        forms[p.name] = tasks.read_form(p.read_bytes(), "image/jpeg", calls)
        print("read", p.name, forms[p.name].get("entry_number"))
    report = build_sample(forms)  # exactly what /api/sample shows visitors
    plan = tasks.action_plan(report, calls)
    print("plan:", plan["summary"])
    chk = check_plan(plan, report)["check"]  # the app applies the same check when it serves the plan
    print(f"plan check: {chk['steps_kept']}/{chk['steps_written']} steps kept, summary replaced: {chk['summary_replaced']}")
    for d in chk["dropped"]:
        print("  dropped:", d["text"][:100], "->", "; ".join(d["reasons"]))
    picks = {}
    for r in report["routes"]:
        if r["rule_id"] in {"R8", "R0b", "R5", "R19", "R10", "R13", "RX", "R16"} or r["holder"] != "you":
            picks.setdefault(r["rule_id"] + r["holder"], r)
    picks.setdefault("urgent", next(r for r in report["routes"] if r["deadline_type"] == "CAPE_80"))
    explanations = {r["entry_number"]: tasks.explain_entry(r, calls) for r in list(picks.values())[:8]}
    offer = tasks.offer_check((SAMPLE / "refund_offer_email.txt").read_text(), report["headline"]["reachable_now"],
                              report["headline"]["reachable_now_count"], calls)
    try:
        fresh = tasks.freshness(calls)
    except Exception as e:
        fresh = {"checked": False, "error": type(e).__name__}
    rules = {r["entry_number"]: r["rule_id"] for r in report["routes"]}
    out = {"forms": forms, "plan": plan, "explanations": explanations, "explanation_rules": {n: rules[n] for n in explanations},
           "offer": offer, "freshness": fresh,
           "calls": [asdict(c) | {"seconds": round(c.seconds, 2), "cost_usd": round(c.cost_usd, 5)} for c in calls]}
    (SAMPLE / "demo_cache.json").write_text(json.dumps(out, indent=1))
    print(f"wrote demo_cache.json ({len(calls)} model calls, ${sum(c.cost_usd for c in calls):.3f})")


if __name__ == "__main__":
    main()
