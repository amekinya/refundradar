"""RefundRadar benchmark. Needs NEBIUS_API_KEY (and TAVILY_API_KEY for the offer web lookups).

1. Routing: our rule engine vs. Nemotron models routing the same entries from the same written rules.
   Labels come from the scenario each synthetic entry was built from (data/generate.py), not from the engine.
2. Form reading: Nemotron 3.5 Super VL on 30 synthetic 'photographed' Form 7501s with ground truth.
3. Offer check: 20 synthetic offers (10 scams, 10 legitimate) -> verdict accuracy and red-flag recall.
4. Cost and latency per model tier.

Run:  python -m eval.run_eval [--routing-n 60] [--skip-offers]
Writes eval/results.json and eval/RESULTS.md
"""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
import re
import random
import statistics
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

from app.ai import tasks
from app.ai.client import CallRecord, chat_json
from app.config import settings
from app.engine import catalog as C
from app.engine import entry_number as EN
from app.engine.es003 import parse_csv
from app.engine.models import Profile
from app.engine.rules import route_entry

ROOT = Path(__file__).resolve().parent.parent
TODAY = date(2026, 10, 25)
calls: list[CallRecord] = []

ROUTE_SCHEMA = {
    "type": "object",
    "properties": {"rule_id": {"type": "string"}, "bucket": {"type": "string", "enum": list(C.BUCKETS)},
                   "deadline": {"type": "string", "description": "YYYY-MM-DD or empty"}},
    "required": ["rule_id", "bucket", "deadline"], "additionalProperties": False,
}


def rules_text() -> str:
    consts = (f"Today is {TODAY}. IEEPA collection ended {C.IEEPA_COLLECTION_END}. CAPE window: acceptance within {C.CAPE_WINDOW_DAYS} days "
              f"after liquidation. Protest window: {C.PROTEST_WINDOW_DAYS} days after liquidation. Earliest court deadline cited: {C.EARLIEST_CIT_DEADLINE}. "
              "Dutiable IEEPA headings include 9903.01.01/.05/.10/.13/.15/.16/.20/.24/.25/.43-.77/.84 and 9903.02.01-.18, .20-.71, .73, .80, .83, .88. "
              "9903.01.04 (USMCA) is an exception. 9903.03.xx is Section 122 (not IEEPA). "
              "Evaluate rules in this order; first match wins: R18, R0/R0b, R1, R2, R3, R4, R5, R20, R6, R7, R8b/R8, AD/CVD R10/R9, "
              "unliquidated (R19 if PSC needed, R7b if recon-flagged, R17 if type 06, else R11), liquidated <=80 days (R12; R19/R7b variants), "
              "court plaintiff (R15/R15b), 81-180 days (R13), >180 days (R14). Informal entries (type 11/12) liquidate on the payment date.")
    rules = "\n".join(f"{r.id}: {r.title} -> bucket '{r.bucket}'. {r.action}" for r in C.RULES.values())
    return consts + "\n\n" + rules


def entry_facts(e) -> dict:
    return {"entry_type": e.entry_type, "entry_date": str(e.entry_date), "liquidation_status": e.liquidation_status,
            "liquidation_date": str(e.liquidation_date) if e.liquidation_date else "", "deposit_date": str(e.deposit_date) if e.deposit_date else "",
            "protest_status": e.protest_status, "drawback": e.drawback, "recon_flag": e.recon_flag, "recon_09_filed": e.recon_09_filed,
            "surety_paid": e.surety_paid, "suspension_record": e.suspension_record, "ad_cvd": e.ad_cvd,
            "on_cape_declaration": e.on_cape_declaration, "needs_psc": e.needs_psc,
            "lines": [{"hts": l.hts, "duty": l.duty} for l in e.lines]}


def routing(n: int) -> dict:
    entries, _ = parse_csv((ROOT / "data/sample/prairie_lantern_es003.csv").read_text())
    labels = {r["Entry Number"].replace("-", ""): r for r in csv.DictReader(open(ROOT / "data/sample/prairie_lantern_labels.csv"))}
    by_rule = defaultdict(list)
    for e in entries:
        by_rule[labels[e.entry_number]["expected_rule"]].append(e)
    rng = random.Random(1)
    sample = []
    per = max(1, n // len(by_rule))
    for rid, es in sorted(by_rule.items()):
        sample += rng.sample(es, min(per, len(es)))
    profile = Profile(has_ace_account=True, ach_refund_enrolled=True)
    sys_prompt = "You route US customs entries to IEEPA refund pathways using ONLY the rules given. Reply with JSON."
    rt = rules_text()
    out = {"n": len(sample), "systems": {}}
    # engine
    t0 = time.perf_counter()
    res = [route_entry(e, profile, TODAY) for e in sample]
    eng_s = time.perf_counter() - t0
    out["systems"]["Rule engine"] = _score(sample, labels, [(r.rule_id, r.bucket, str(r.deadline) if r.deadline else "") for r in res], eng_s, 0.0)
    for name, spec, think in (("Nemotron 3 Ultra (model only)", settings.ultra, True), ("Nemotron 3 Nano (model only)", settings.nano, True)):
        preds, cost, secs = [], 0.0, 0.0
        for e in sample:
            local: list[CallRecord] = []
            try:
                j = chat_json(spec, [{"role": "system", "content": sys_prompt},
                                     {"role": "user", "content": f"{rt}\n\nEntry facts: {json.dumps(entry_facts(e))}\nWhich rule applies, which bucket, and the deadline date if any?"}],
                              schema=ROUTE_SCHEMA, purpose=f"routing baseline ({spec.role})", reasoning=think, max_tokens=4000,
                              calls=local, enforce_cap=False)
                preds.append((j.get("rule_id", ""), j.get("bucket", ""), j.get("deadline", "")))
            except Exception as ex:  # count failures as wrong
                preds.append(("ERR", "ERR", ""))
            calls.extend(local)
            cost += sum(c.cost_usd for c in local); secs += sum(c.seconds for c in local)
        out["systems"][name] = _score(sample, labels, preds, secs, cost)
    return out


def _score(sample, labels, preds, secs, cost) -> dict:
    ok_b = ok_r = ok_d = 0
    misses = []
    for e, (rid, bucket, dl) in zip(sample, preds):
        lab = labels[e.entry_number]
        ok_b += bucket == lab["expected_bucket"]
        ok_r += rid == lab["expected_rule"]
        exp_dl = str(route_entry(e, Profile(), TODAY).deadline or "") if lab["expected_deadline_type"] else ""
        ok_d += (dl or "") == exp_dl
        if bucket != lab["expected_bucket"]:
            misses.append({"entry": e.entry_number, "expected": lab["expected_rule"], "got": rid})
    n = len(sample)
    return {"route_accuracy": round(ok_b / n, 3), "rule_accuracy": round(ok_r / n, 3), "deadline_exact": round(ok_d / n, 3),
            "seconds_total": round(secs, 2), "cost_usd": round(cost, 4), "misses": misses[:10]}


KNOWN_FILERS = frozenset({"K4M", "T2R", "Q7Z"})  # the filer codes in the synthetic importer's ES-003 export


def forms() -> dict:
    files = sorted((ROOT / "data/forms").glob("form_*.jpg"))
    fields = defaultdict(lambda: [0, 0])
    per_photo, unrepaired = [], []
    for f in files:
        truth = json.loads(f.with_suffix(".json").read_text())
        local: list[CallRecord] = []
        try:
            got = tasks.read_form(f.read_bytes(), "image/jpeg", local)
        except Exception as ex:
            got = {}
        calls.extend(local)
        alnum = lambda x: re.sub(r"[^A-Z0-9]", "", str(x or "").upper())  # noqa: E731  (dashes/spaces are formatting, not reading)
        checks = {
            "entry_number": alnum(got.get("entry_number")) == alnum(truth["entry_number"]),
            "entry_type": got.get("entry_type", "") == truth["entry_type"],
            "entry_date": _iso(got.get("entry_date", "")) == _iso(truth["entry_date"]),
            "importer_number": alnum(got.get("importer_number")) == alnum(truth["importer_number"]),
            "chapter99_lines": sorted(h for l in got.get("lines", []) for h in l.get("hts_numbers", []) if h.startswith("9903"))
                               == sorted(h for l in truth["lines"] for h in l["hts_numbers"] if h.startswith("9903")),
            "ieepa_duty": abs(sum(d for l in got.get("lines", []) for h, d in zip(l.get("hts_numbers", []), l.get("duties", [])) if h.startswith("9903"))
                              - sum(d for l in truth["lines"] for h, d in zip(l["hts_numbers"], l["duties"]) if h.startswith("9903"))) < 0.01,
            "total_duty": abs(got.get("total_duty", -1) - truth["total_duty"]) < 0.01,
        }
        for k, v in checks.items():
            fields[k][0] += v; fields[k][1] += 1
        # The app repairs look-alike misreads with the CBP check digit, using the filer codes in the importer's own export.
        fixed, _ = EN.repair(got.get("entry_number", ""), KNOWN_FILERS)
        repaired_ok = alnum(fixed) == alnum(truth["entry_number"])
        flagged = bool(EN.validate(fixed))
        fields["entry_number_after_check_digit_repair"][0] += repaired_ok; fields["entry_number_after_check_digit_repair"][1] += 1
        if not repaired_ok:
            unrepaired.append(flagged)
        wrong = {k: [str(got.get(k, ""))[:40], str(truth.get(k, ""))[:40]] for k, v in checks.items() if not v and k in truth}
        per_photo.append({"file": f.name, "strength": truth["photo_strength"], "all_correct": all(checks.values()), "wrong": wrong,
                          "seconds": round(sum(c.seconds for c in local), 2), "cost_usd": round(sum(c.cost_usd for c in local), 5)})
    base = {k: v for k, v in fields.items() if k != "entry_number_after_check_digit_repair"}
    total_fields = sum(v[1] for v in base.values())
    return {"n": len(files), "field_accuracy": {k: round(a / b, 3) for k, (a, b) in fields.items()},
            "overall_field_accuracy": round(sum(v[0] for v in base.values()) / max(total_fields, 1), 3),
            "photos_fully_correct": round(sum(p["all_correct"] for p in per_photo) / max(len(per_photo), 1), 3),
            "by_photo_quality": {s: round(statistics.mean(p["all_correct"] for p in per_photo if p["strength"] == s), 3)
                                 for s in sorted({p["strength"] for p in per_photo})},
            "avg_seconds": round(statistics.mean(p["seconds"] for p in per_photo), 2) if per_photo else 0,
            "cost_usd": round(sum(p["cost_usd"] for p in per_photo), 4),
            "wrong_entry_numbers_flagged_for_review": f"{sum(unrepaired)}/{len(unrepaired)}", "rows": per_photo}


def _iso(d: str) -> str:
    """MM/DD/YYYY, YYYY-MM-DD or MM-DD-YYYY -> YYYY-MM-DD (format differences aren't reading errors)."""
    d = str(d or "").strip()
    m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", d)
    if m:
        return f"{m[3]}-{int(m[1]):02d}-{int(m[2]):02d}"
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", d)
    return f"{m[1]}-{int(m[2]):02d}-{int(m[3]):02d}" if m else d


def offers() -> dict:
    """Live check (Nemotron 3 Ultra reads the offer, code decides) vs. the no-model fallback (regex flags, same verdict rule)."""
    labels = json.loads((ROOT / "data/offers/labels.json").read_text())
    rows = []
    for lab in labels:
        text = (ROOT / "data/offers" / lab["file"]).read_text()
        local: list[CallRecord] = []
        try:
            r = tasks.offer_check(text, 50_000, 30, local)
            err = ""
        except Exception as e:  # noqa: BLE001
            r, err = {"verdict": "ERR", "red_flags": []}, f"{type(e).__name__}: {str(e)[:120]}"
        calls.extend(local)
        fb = tasks.offer_check_fallback(text, 50_000, 30)
        rows.append({"file": lab["file"], "expected": lab["label"], "flags_expected": lab["flags"],
                     "got": r.get("verdict"), "flags_got": sorted({f["flag"] for f in r.get("red_flags", [])}), "error": err,
                     "model_flags_rejected": r.get("model_flags_rejected", 0), "fee_pct": r.get("effective_pct"), "fallback": fb["verdict"]})

    def score(key: str) -> dict:
        n = len(rows)
        scams = [x for x in rows if x["expected"] == "likely_scam"]
        legit = [x for x in rows if x["expected"] != "likely_scam"]
        return {"verdict_accuracy": round(sum(x[key] == x["expected"] for x in rows) / n, 3),
                "scams_caught": f"{sum(x[key] == 'likely_scam' for x in scams)}/{len(scams)}",
                "legit_flagged_as_scam": f"{sum(x[key] == 'likely_scam' for x in legit)}/{len(legit)}"}

    flag_n = sum(len(x["flags_expected"]) for x in rows)
    flag_hits = sum(len(set(x["flags_expected"]) & set(x["flags_got"])) for x in rows)
    return {"n": len(rows), "live": score("got"), "fallback": score("fallback"), "red_flag_recall": round(flag_hits / max(flag_n, 1), 3),
            "errors": sum(bool(x["error"]) for x in rows), "rows": rows}


def tiers() -> dict:
    out = {}
    for role in ("nano", "super_vl", "ultra"):
        cs = [c for c in calls if c.role == role]
        if cs:
            out[role] = {"model": cs[0].model_id, "calls": len(cs), "avg_seconds": round(statistics.mean(c.seconds for c in cs), 2),
                         "avg_tokens_in": int(statistics.mean(c.tokens_in for c in cs)), "avg_tokens_out": int(statistics.mean(c.tokens_out for c in cs)),
                         "cost_usd": round(sum(c.cost_usd for c in cs), 4)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--routing-n", type=int, default=57)
    ap.add_argument("--skip-offers", action="store_true")
    ap.add_argument("--skip-forms", action="store_true")
    ap.add_argument("--reuse-routing", action="store_true", help="keep the routing results already in eval/results.json")
    a = ap.parse_args()
    prev = json.loads((ROOT / "eval/results.json").read_text()) if (ROOT / "eval/results.json").exists() else {}
    if a.reuse_routing and "routing" in prev:
        calls.extend(CallRecord(**c) for c in prev.get("routing_calls", []))
        routing_res = prev["routing"] | {"reused_from": prev.get("routing_run_at", prev.get("run_at"))}
    else:
        routing_res = routing(a.routing_n)
    res = {"run_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "routing": routing_res,
           "routing_run_at": routing_res.get("reused_from", time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()))}
    res["routing_calls"] = [asdict(c) for c in calls]  # so a later run that reuses routing still reports its cost per tier
    if not a.skip_forms:
        res["forms"] = forms()
    if not a.skip_offers:
        res["offers"] = offers()
    res["tiers"] = tiers()
    (ROOT / "eval/results.json").write_text(json.dumps(res, indent=1))
    (ROOT / "eval/RESULTS.md").write_text(render_md(res))
    print(render_md(res))


def render_md(r: dict) -> str:
    L = [f"# RefundRadar benchmark results\n\nRun {r['run_at']}. Synthetic data only (invented importer, fake identifiers).\n",
         f"## 1. Routing {r['routing']['n']} entries (stratified across all rule paths; run {r.get('routing_run_at', r['run_at'])})\n",
         "| System | Right route | Right rule | Exact deadline | Time | Cost |", "|---|---|---|---|---|---|"]
    for name, s in r["routing"]["systems"].items():
        L.append(f"| {name} | {s['route_accuracy']:.0%} | {s['rule_accuracy']:.0%} | {s['deadline_exact']:.0%} | {s['seconds_total']}s | ${s['cost_usd']:.3f} |")
    if "forms" in r:
        f = r["forms"]
        L += [f"\n## 2. Reading {f['n']} photographed Form 7501s (Nemotron 3.5 Super VL)\n", "| Field | Accuracy |", "|---|---|"]
        L += [f"| {k} | {v:.0%} |" for k, v in f["field_accuracy"].items()]
        if "wrong_entry_numbers_flagged_for_review" in f:
            L += [f"\nEntry numbers still wrong after the check-digit repair that fail validation, so the app flags them for review: {f['wrong_entry_numbers_flagged_for_review']}."]
        L += [f"\nAll fields correct on {f['photos_fully_correct']:.0%} of photos; by photo quality (light/medium/heavy distortion): "
              + ", ".join(f"{k}: {v:.0%}" for k, v in f["by_photo_quality"].items()) + f". Avg {f['avg_seconds']}s per photo, total ${f['cost_usd']:.3f}."]
    if "offers" in r:
        o = r["offers"]
        L += [f"\n## 3. Offer check ({o['n']} offers: 10 scams, 10 legitimate)\n",
              "Both rows use the same code rule for the verdict. The first adds Nemotron 3 Ultra: it reads the fee terms (percent, flat, per entry, "
              "minimum) to price the offer on your numbers, and proposes red flags that code keeps only if they quote the offer and match the flag's "
              "definition. The flag definitions and these 20 offers were written by the same author, so treat this as a sanity check, not field accuracy.\n",
              "| Reader | Right verdict | Scams caught | Legitimate offers flagged as scams |", "|---|---|---|---|",
              f"| Nemotron 3 Ultra reading + code rules | {o['live']['verdict_accuracy']:.0%} | {o['live']['scams_caught']} | {o['live']['legit_flagged_as_scam']} |",
              f"| Keyword rules only (no model) | {o['fallback']['verdict_accuracy']:.0%} | {o['fallback']['scams_caught']} | {o['fallback']['legit_flagged_as_scam']} |",
              f"\nRed-flag recall: {o['red_flag_recall']:.0%}. Model-proposed flags rejected by code: {sum(x.get('model_flags_rejected', 0) for x in o['rows'])}. Errors: {o['errors']}."]
    L += ["\n## 4. Cost and latency by model tier\n", "| Tier | Model | Calls | Avg seconds | Avg tokens in/out | Cost |", "|---|---|---|---|---|---|"]
    L += [f"| {k} | {v['model']} | {v['calls']} | {v['avg_seconds']} | {v['avg_tokens_in']}/{v['avg_tokens_out']} | ${v['cost_usd']:.3f} |" for k, v in r["tiers"].items()]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
