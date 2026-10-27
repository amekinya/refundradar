"""Regression tests for the Oct 26 review of RefundRadar (research_notes/review/refundradar_nebius.md, Job 1 items 1-13)."""
import inspect
import json
import random
import threading
import time
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.ai import tasks
from app.ai.client import LiveModelUnavailable
from app.engine import analyze as A
from app.engine import entry_number as EN
from app.engine.es003 import parse_csv, parse_date, parse_money
from app.engine.models import Entry, Line, Profile
from app.engine.plan_check import check_plan
from app.engine.rules import route_entry
from app import main

TODAY = date(2026, 10, 25)
ME = Profile(importer_number="12-3456789AA", has_ace_account=True, ach_refund_enrolled=True)
HDR = "Entry Number,Entry Date,Entry Type,HTS Number,Duty Amount,Liquidation Status,Liquidation Date,Importer Number\n"


def num(filer: str, serial: str) -> str:
    return f"{filer}-{serial}-{EN.check_digit(filer + serial)}"


def ieepa(n=None, **kw):
    base = dict(entry_number=n or num("B76", "0324527"), entry_type="01", entry_date=date(2025, 9, 1),
                lines=[Line("001", "9903.01.25", 1000.0)], importer_number="12-3456789AA")
    return Entry(**(base | kw))


def photo_form(entry_number="", duties=(500.0,), total=None, entry_date="09/01/2025", importer="12-3456789AA"):
    return {"entry_number": entry_number, "entry_type": "01", "entry_date": entry_date, "importer_number": importer,
            "importer_name": "ACME IMPORTS LLC", "country_of_origin": "CN",
            "lines": [{"line_no": "001", "hts_numbers": ["9903.01.25"] * len(duties), "duties": list(duties)}],
            "total_duty": sum(duties) if total is None else total, "unreadable_fields": []}


# --- 1. entry-number repair never invents a filer code ------------------------------------
def test_serial_misread_is_not_rewritten_without_known_filers():
    # The review's case: truth Q7Z-8390903-5, model reads Q7Z-8090903-5; the old code "fixed" it to QT2-8090903-5.
    assert not EN.validate("Q7Z-8390903-5") and EN.validate("Q7Z-8090903-5")
    fixed, changed = EN.repair("Q7Z-8090903-5")
    assert (fixed, changed) == ("Q7Z80909035", False) and EN.validate(fixed)  # still flagged, so it gets the re-read


def test_known_filer_as_read_is_kept():
    assert EN.repair("Q7Z-8090903-5", {"Q7Z", "K4M"}) == ("Q7Z80909035", False)


def test_lookalike_filer_repaired_only_to_a_known_code():
    assert EN.repair("07Z-8390903-5", {"Q7Z"}) == ("Q7Z83909035", True)
    assert EN.repair("07Z-8390903-5") == ("07Z83909035", False)


def test_letters_in_the_serial_still_become_digits():
    assert EN.repair("Q7Z-839O903-5") == ("Q7Z83909035", True)


def test_no_serial_misread_becomes_another_valid_number():
    rng = random.Random(7)
    wrong = 0
    for _ in range(3000):
        filer = rng.choice(["K4M", "T2R", "Q7Z", "B76", "S1G"])
        truth = num(filer, f"{rng.randrange(10**7):07d}")
        e = EN.normalize(truth)
        i = rng.randrange(3, 10)
        misread = e[:i] + str((int(e[i]) + rng.randrange(1, 10)) % 10) + e[i + 1:]
        fixed, _ = EN.repair(misread)
        wrong += fixed != EN.normalize(truth) and not EN.validate(fixed)
    assert wrong == 0


def test_photo_upload_flags_instead_of_correcting(monkeypatch):
    monkeypatch.setattr(tasks, "read_form", lambda *a, **k: photo_form("Q7Z-8090903-5"))
    monkeypatch.setattr(tasks, "reread_entry_number", lambda *a, **k: "Q7Z-8090903-5")
    c = TestClient(main.app)
    r = c.post("/api/analyze", files={"photos": ("f.jpg", b"jpg", "image/jpeg")}, data={"profile": json.dumps({"importer_number": "12-3456789AA"})})
    rep = r.json()
    f = rep["review_grid"][0]["fields"]
    assert f["entry_number"] == "Q7Z-8090903-5" and not rep["review_grid"][0]["corrected"] and f["entry_number_problems"]
    assert any(b["key"] == "photonum" for b in rep["blockers"])
    assert A.handoff_entry_list(rep) == []  # a number that fails the check digit doesn't go to the broker
    # A focused re-read that passes the check digit is used, and the card says so.
    monkeypatch.setattr(tasks, "reread_entry_number", lambda *a, **k: "Q7Z-8390903-5")
    f = c.post("/api/analyze", files={"photos": ("f.jpg", b"jpg", "image/jpeg")}).json()["review_grid"][0]["fields"]
    assert f["entry_number"] == "Q7Z83909035" or EN.normalize(f["entry_number"]) == "Q7Z83909035"
    assert f["entry_number_as_read"] == "Q7Z-8090903-5" and f["entry_number_fix"] == "reread"


# --- 2. dates in common spreadsheet formats; unreadable ones are reported -------------------
@pytest.mark.parametrize("s", ["2025-03-01", "2025-03-01 00:00:00", "3/1/2025 0:00", "01-Mar-25", "2025-03-01T00:00:00",
                               "2025-03-01T00:00:00Z", "3/1/25", "03/01/2025 12:00 AM", "Mar 1, 2025", "45717"])
def test_date_formats(s):
    assert parse_date(s) == date(2025, 3, 1)


def test_parse_money_with_currency():
    assert parse_money("USD 500") == 500 and parse_money("$1,234.50") == 1234.5 and parse_money("(12.00)") == -12


def test_liquidated_with_time_part_routes_on_its_real_date():
    n = num("B76", "0324527")
    entries, _ = parse_csv(HDR + f"{n},2025-01-01 00:00:00,01,9903.01.25,1000,Liquidated,2026-01-10 00:00:00,\n")
    r = route_entry(entries[0], ME, TODAY)
    assert r.rule_id == "R14" and r.liquidation_date == date(2026, 1, 10) and not entries[0].unparsed


def test_unreadable_date_is_a_blocker_not_cape_now():
    n = num("B76", "0324527")
    entries, info = parse_csv(HDR + f"{n},sometime in 2025,01,9903.01.25,1000,Liquidated,last winter,\n")
    assert info["unparsed"] == 1 and entries[0].unparsed == {"entry_date": "sometime in 2025", "liquidation_date": "last winter"}
    rep = A.analyze(entries, ME, TODAY)
    r = rep["routes"][0]
    assert r["rule_id"] == "RX" and r["bucket"] == "review" and "unparsed" in r["flags"]
    assert any("couldn't be read" in p for p in r["entry_problems"])
    assert any(b["key"] == "unparsed" for b in rep["blockers"]) and rep["headline"]["reachable_now"] == 0


def test_liquidated_status_without_a_date_never_routes_to_cape_now():
    assert route_entry(ieepa(entry_date=None, liquidation_status="Liquidated"), ME, TODAY).rule_id == "RX"
    assert route_entry(ieepa(liquidation_status="Liquidated"), ME, TODAY).bucket == "review"


def test_file_with_no_dates_at_all_is_not_claimable_now():
    entries, _ = parse_csv("Entry Number,HTS Number,Duty Amount\n" + f"{num('B76', '0324527')},9903.01.25,1000\n")
    assert route_entry(entries[0], ME, TODAY).rule_id == "RX"


def test_unreadable_duty_amount_is_reported():
    entries, _ = parse_csv(HDR + f"{num('B76', '0324527')},2025-09-01,01,9903.01.25,one thousand,,,\n")
    r = route_entry(entries[0], ME, TODAY)
    assert "unparsed" in r.flags and r.principal == 0


# --- 3. an estimated liquidation date never means "protest" or "court only" -------------------
def test_estimated_dates_go_to_review_not_protest_or_court():
    old = route_entry(ieepa(entry_date=date(2025, 3, 1)), ME, TODAY)   # estimated ~Jan 2026: was R14
    mid = route_entry(ieepa(entry_date=date(2025, 9, 1)), ME, TODAY)   # estimated ~Jul 2026: was R13
    assert (old.rule_id, old.bucket, mid.rule_id, mid.bucket) == ("RX", "review", "RX", "review")
    assert "Confirm the liquidation date in ACE" in mid.action and mid.deadline is None
    rep = A.analyze([ieepa(num("B76", "0324527"), entry_date=date(2025, 3, 1)), ieepa(num("B76", "0324528"))], ME, TODAY)
    h = rep["headline"]
    assert h["protest_amount"] == 0 and h["litigation_amount"] == 0 and rep["buckets"]["review"]["principal"] == 2000


def test_real_liquidation_dates_still_route_to_protest():
    r = route_entry(ieepa(liquidation_status="Liquidated", liquidation_date=date(2026, 6, 1)), ME, TODAY)
    assert r.rule_id == "R13" and r.bucket == "protest"


# --- 4. photo uploads don't block the server ----------------------------------------------------
def test_upload_endpoint_runs_in_a_worker_thread():
    assert not inspect.iscoroutinefunction(main.analyze_upload)


def test_health_answers_while_a_photo_is_being_read(monkeypatch):
    def slow(*a, **k):
        time.sleep(1.5)
        return photo_form(num("B76", "0324527"))
    monkeypatch.setattr(tasks, "read_form", slow)
    with TestClient(main.app) as c:
        t = threading.Thread(target=lambda: c.post("/api/analyze", files={"photos": ("f.jpg", b"jpg", "image/jpeg")}))
        t.start()
        time.sleep(0.3)
        t0 = time.perf_counter()
        assert c.get("/api/health").status_code == 200
        waited = time.perf_counter() - t0
        t.join()
    assert waited < 0.8


# --- 5. code checks the model's action plan ------------------------------------------------------
def _sample_report():
    forms = {p.name: json.loads(p.with_suffix(".json").read_text()) for p in sorted((main.SAMPLE / "photos").glob("*.jpg"))}
    return main.build_sample(forms)


def test_plan_steps_that_disagree_with_the_report_are_dropped():
    rep = _sample_report()
    by_rule = {}
    for r in rep["routes"]:
        by_rule.setdefault(r["rule_id"], r)
    urgent = min((r for r in rep["routes"] if r["bucket"] == "cape_now" and r["deadline_type"] == "CAPE_80"), key=lambda r: r["days_left"])
    surety, drawback, warehouse = by_rule["R2"], by_rule["R6"], by_rule["R5"]
    late = date.fromisoformat(urgent["deadline"]) + timedelta(days=1)
    plan = {"summary": f"${rep['headline']['reachable_now']:,.0f} is claimable now.", "watch_outs": [
                f"Entry {warehouse['entry_number']} (${warehouse['principal']:,.0f}) is a warehouse entry.", "Entry Q7Z-0000000-0 is risky."],
            "steps": [
        {"when": "Today", "do": f"File CAPE for {urgent['entry_number']} (${urgent['principal']:,.0f}).", "why": "Closest deadline.", "who": "your broker"},
        {"when": late.isoformat(), "do": f"File CAPE for {urgent['entry_number']}.", "why": "", "who": "your broker"},
        {"when": "This week", "do": f"Notify your surety about {drawback['entry_number']} ({'$'}{drawback['principal']:,.0f}).", "why": "", "who": "you"},
        {"when": "This week", "do": f"Notify your surety about {surety['entry_number']} (${surety['principal'] + 999:,.0f}).", "why": "", "who": "you"},
        {"when": "This week", "do": "Withdraw the open protests.", "why": "$12,345 is at stake.", "who": "your broker"},
        {"when": "This week", "do": "Confirm your refund bank account.", "why": f"Your ${rep['headline']['reachable_now']:,.0f} could be held.", "who": "you"},
    ]}
    out = check_plan(plan, rep)
    kept = [s["do"] for s in out["steps"]]
    assert kept == [plan["steps"][0]["do"], plan["steps"][5]["do"]]
    reasons = " | ".join("; ".join(d["reasons"]) for d in out["check"]["dropped"])
    assert "deadline is" in reasons and "listed under surety" in reasons and "not $" in reasons and "isn't a figure" in reasons
    assert "isn't one of your entries" in reasons
    assert out["watch_outs"] == [plan["watch_outs"][0]] and not out["check"]["summary_replaced"]
    bad = check_plan(plan | {"summary": "$999,999 is claimable."}, rep)
    assert bad["check"]["summary_replaced"] and "$999,999" not in bad["summary"]


def test_cached_demo_plan_is_checked_when_served():
    c = TestClient(main.app)
    rep = c.get("/api/sample").json()
    p = c.post("/api/plan", json={"report_id": rep["report_id"]}).json()
    assert "check" in p and p["steps"]
    routes = {EN.normalize(r["entry_number"]): r for r in rep["routes"]}
    for s in p["steps"]:
        for m in __import__("re").finditer(r"\b[A-Z0-9]{3}-\d{7}-\d\b", s["do"] + s["why"]):
            assert EN.normalize(m.group(0)) in routes


def test_blocked_and_review_amounts_are_separate():
    entries = [ieepa(num("B76", "0324527"), surety_paid=True), ieepa(num("B76", "0324528"), entry_date=date(2025, 3, 1))]
    rep = A.analyze(entries, ME, TODAY)
    amt = {r["bucket"]: r["principal"] + r["interest"] for r in rep["routes"]}
    assert rep["headline"]["blocked_amount"] == pytest.approx(amt["blocked"]) and rep["headline"]["review_amount"] == pytest.approx(amt["review"])


# --- 6. the duty cross-check is strict and its result reaches the report --------------------------
def test_duty_check_tolerance_is_rounding_only():
    assert main.duty_check(photo_form(duties=(758.0, 227.4, 288.0, 96.48)))["ok"] is True
    assert main.duty_check(photo_form(duties=(100.0, 25.5), total=125.51))["ok"] is True   # a cent of rounding
    assert main.duty_check(photo_form(duties=(758.0, 227.4, 288.0, 96.48), total=1375.88))["ok"] is False  # the review's $6 gap
    assert main.duty_check(photo_form(duties=(10750.0,), total=11350.0))["ok"] is False


def test_block_37_not_read_is_unknown_not_a_mismatch():
    for total in (0, None):
        f = photo_form(duties=(500.0,)) | {"total_duty": total}
        assert main.duty_check(f) == {"ok": None, "reason": "Block 37 not read", "lines_sum": 500.0}


def test_failed_duty_check_reaches_route_and_blockers():
    form, _ = main._checked_form(photo_form(num("B76", "0324527"), duties=(500.0,), total=900.0), set())
    e = main.form_to_entry(form, "f.jpg")
    assert e.duty_mismatch == (500.0, 900.0)
    rep = A.analyze([e], ME, TODAY)
    r = rep["routes"][0]
    assert "duty_mismatch" in r["flags"] and any("Block 37" in p for p in r["entry_problems"]) and any("Block 37" in n for n in r["notes"])
    assert any(b["key"] == "dutycheck" for b in rep["blockers"])


def test_bad_duty_values_from_a_photo_dont_crash():
    e = main.form_to_entry(photo_form(num("B76", "0324527")) | {"lines": [{"line_no": "001", "hts_numbers": ["9903.01.25"], "duties": [None]}]}, "f.jpg")
    assert e.lines[0].duty == 0.0 and e.unparsed


# --- 7. "leaves within 3 weeks" is part of what's claimable now -----------------------------------
def test_urgent_amount_only_counts_claimable_entries():
    liq = TODAY - timedelta(days=75)
    small = ieepa(num("B76", "0324527"), lines=[Line("1", "9903.01.25", 100.0)], liquidation_status="Liquidated", liquidation_date=liq)
    protest = ieepa(num("B76", "0324528"), lines=[Line("1", "9903.01.25", 10000.0)], liquidation_status="Liquidated", liquidation_date=liq,
                    protest_status="open", protest_solely_ieepa=True)
    h = A.analyze([small, protest], ME, TODAY)["headline"]
    assert h["urgent_amount"] <= h["reachable_now"] and h["urgent_count"] == 1
    assert h["urgent_needs_decision_count"] == 1 and h["urgent_needs_decision_amount"] > 10000


# --- 8. unreadable entry numbers stay separate --------------------------------------------------
def test_unreadable_entry_numbers_are_not_duplicates():
    es = [main.form_to_entry(main._checked_form(photo_form("", duties=(d,)), set())[0], f"p{i}.jpg") for i, d in enumerate((500.0, 900.0))]
    rep = A.analyze(es, ME, TODAY)
    assert len(rep["routes"]) == 2 and rep["headline"]["duplicates"] == 0 and rep["headline"]["total_principal"] == 1400
    assert {r["entry_number"] for r in rep["routes"]} == {"Unreadable entry 1", "Unreadable entry 2"}
    assert A.handoff_entry_list(rep) == [] and any(b["key"] == "photonum" for b in rep["blockers"])


# --- 9. the one-character importer tolerance is for photos only -------------------------------------
def test_importer_one_off_tolerance_only_for_photos():
    csv_e = ieepa(importer_number="12-3456788AA")
    assert route_entry(csv_e, ME, TODAY).holder == "someone_else"
    photo_e = ieepa(importer_number="12-3456788AA", source="photo:f.jpg")
    assert route_entry(photo_e, ME, TODAY).holder == "you"


# --- 11. a scheduled (future) liquidation date isn't a liquidation --------------------------------
def test_future_liquidation_date_with_blank_status():
    r = route_entry(ieepa(entry_date=date(2026, 1, 15), liquidation_date=TODAY + timedelta(days=30)), ME, TODAY)
    assert r.rule_id == "R11" and r.liquidation_date is None and any("scheduled" in n for n in r.notes)


# --- 13. informal entries ------------------------------------------------------------------------
def test_informal_entry_without_ace_date_is_r16():
    r = route_entry(ieepa(entry_type="11", entry_date=date(2025, 3, 1)), ME, TODAY)
    assert r.rule_id == "R16" and r.bucket == "review" and any("court" in n for n in r.notes)


# --- demo explanations are only replayed for the rule they were written for -----------------------
def test_stale_cached_explanation_not_replayed(monkeypatch):
    def unavailable(*a, **k):
        raise LiveModelUnavailable("test")
    monkeypatch.setattr(tasks, "explain_entry", unavailable)
    c = TestClient(main.app)
    rep = c.get("/api/sample").json()
    rules = {r["entry_number"]: r["rule_id"] for r in rep["routes"]}
    cache = main._demo_cache()
    for n, rid in cache["explanation_rules"].items():
        d = c.post("/api/explain", json={"report_id": rep["report_id"], "entry_number": n}).json()
        assert bool(d.get("cached")) == (rules[n] == rid)


def test_profile_api_input_is_robust():
    assert main._profile("[1, 2]").cit_plaintiff is False
    assert main._profile(json.dumps({"cit_plaintiff": "false", "corporate": "no"})).cit_plaintiff is False
    assert main._profile(json.dumps({"cit_plaintiff": True})).cit_plaintiff is True


def test_csv_result_kept_when_photo_reader_is_down(monkeypatch):
    def unavailable(*a, **k):
        raise LiveModelUnavailable("test")
    monkeypatch.setattr(tasks, "read_form", unavailable)
    csv_text = HDR + f"{num('B76', '0324527')},2026-02-01,01,9903.01.25,1000,Not Liquidated,,\n"
    r = TestClient(main.app).post("/api/analyze", files={"csv_file": ("x.csv", csv_text.encode(), "text/csv"),
                                                         "photos": ("f.jpg", b"jpg", "image/jpeg")})
    assert r.status_code == 200 and r.json()["blockers"][0]["key"] == "photos" and len(r.json()["routes"]) == 1
