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
from app.engine import analyze as A
from app.engine.es003 import parse_csv
from app.engine.models import Profile
from app.main import DEMO_TODAY, form_to_entry

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "data/sample"


def main():
    calls: list[CallRecord] = []
    forms = {}
    for p in sorted((SAMPLE / "photos").glob("*.jpg")):
        forms[p.name] = tasks.read_form(p.read_bytes(), "image/jpeg", calls)
        print("read", p.name, forms[p.name].get("entry_number"))
    entries, _ = parse_csv((SAMPLE / "prairie_lantern_es003.csv").read_text())
    entries += [form_to_entry(f, n) for n, f in forms.items()]
    prof = Profile(importer_number="00-7351942AA", has_ace_account=True, ach_refund_enrolled=False, corporate=True)
    report = A.analyze(entries, prof, DEMO_TODAY)
    plan = tasks.action_plan(report, calls)
    print("plan:", plan["summary"])
    picks = {}
    for r in report["routes"]:
        if r["rule_id"] in {"R8", "R0b", "R5", "R19", "R10", "R13"} or r["holder"] != "you":
            picks.setdefault(r["rule_id"] + r["holder"], r)
    picks.setdefault("urgent", next(r for r in report["routes"] if r["deadline_type"] == "CAPE_80"))
    explanations = {r["entry_number"]: tasks.explain_entry(r, calls) for r in list(picks.values())[:8]}
    offer = tasks.offer_check((SAMPLE / "refund_offer_email.txt").read_text(), report["headline"]["reachable_now"],
                              report["headline"]["reachable_now_count"], calls)
    try:
        fresh = tasks.freshness(calls)
    except Exception as e:
        fresh = {"checked": False, "error": type(e).__name__}
    out = {"forms": forms, "plan": plan, "explanations": explanations, "offer": offer, "freshness": fresh,
           "calls": [asdict(c) | {"seconds": round(c.seconds, 2), "cost_usd": round(c.cost_usd, 5)} for c in calls]}
    (SAMPLE / "demo_cache.json").write_text(json.dumps(out, indent=1))
    print(f"wrote demo_cache.json ({len(calls)} model calls, ${sum(c.cost_usd for c in calls):.3f})")


if __name__ == "__main__":
    main()
