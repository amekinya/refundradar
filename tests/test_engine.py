from datetime import date, timedelta

import pytest

from app.engine import analyze as A
from app.engine import entry_number as EN
from app.engine.costs import compare, offer_cost
from app.engine.es003 import parse_csv
from app.engine.headings import is_dutiable_ieepa, is_section_122, normalize_hts, program_of
from app.engine.interest import estimate_interest
from app.engine.models import Entry, Line, Profile
from app.engine.rules import route_entry

TODAY = date(2026, 10, 25)
ME = Profile(importer_number="12-3456789AA", has_ace_account=True, ach_refund_enrolled=True)


def entry(**kw):
    base = dict(
        entry_number="B76-0324527-8",
        entry_type="01",
        entry_date=date(2025, 9, 1),
        lines=[Line("001", "9903.01.25", 1000.0), Line("001", "8517.62.0090", 0.0, 10000)],
        importer_number="12-3456789AA",
    )
    base.update(kw)
    return Entry(**base)


def route(**kw):
    profile = kw.pop("profile", ME)
    return route_entry(entry(**kw), profile, TODAY)


# --- primitives ---------------------------------------------------------------------------
def test_check_digit_matches_cbp_worked_example():
    assert EN.check_digit("B760324527") == 8
    assert EN.validate("B76-0324527-8") == []
    assert "Check digit" in EN.validate("B76-0324527-1")[0]
    assert "11 characters" in EN.validate("B76-03245")[0]


def test_interest_matches_research_worked_example():
    assert estimate_interest(10_000, date(2025, 6, 16), date(2026, 5, 4), corporate=False) == pytest.approx(627.33, abs=0.02)
    assert estimate_interest(10_000, date(2025, 6, 16), date(2026, 5, 4), corporate=True) == pytest.approx(534.00, abs=0.02)
    assert estimate_interest(10_000, date(2026, 5, 4), date(2026, 5, 4)) == 0


def test_headings():
    assert normalize_hts("9903012500") == "9903.01.25"
    assert is_dutiable_ieepa("9903.01.25") and program_of("9903.01.25") == "Reciprocal baseline"
    assert not is_dutiable_ieepa("9903.01.26")  # Canada exception
    assert not is_dutiable_ieepa("9903.02.19")  # EU base-rate exception
    assert is_dutiable_ieepa("9903.02.20")  # EU 15% all-in
    assert not is_dutiable_ieepa("9903.88.15")  # Section 301
    assert is_section_122("9903.03.01") and not is_dutiable_ieepa("9903.03.01")


# --- gates -----------------------------------------------------------------------------
def test_no_ieepa_line_is_not_eligible():
    r = route(lines=[Line("001", "8517.62.0090", 50.0), Line("001", "9903.88.15", 500.0)])
    assert (r.rule_id, r.bucket, r.principal) == ("R0", "not_eligible", 0)


def test_section_122_only_routes_to_protest():
    r = route(entry_date=date(2026, 3, 10), lines=[Line("001", "9903.03.01", 300.0)],
              liquidation_status="Liquidated", liquidation_date=date(2026, 9, 1))
    assert r.rule_id == "R0b" and r.deadline == date(2026, 9, 1) + timedelta(days=180)


def test_after_cutoff_not_eligible():
    assert route(entry_date=date(2026, 3, 1)).rule_id == "R1"


@pytest.mark.parametrize("kw,rid,bucket", [
    ({"surety_paid": True}, "R2", "blocked"),
    ({"not_in_ace": True}, "R3", "blocked"),
    ({"entry_type": "47"}, "R4", "not_eligible"),
    ({"entry_type": "08"}, "R4", "not_eligible"),
    ({"entry_type": "21"}, "R5", "review"),
    ({"entry_type": "61"}, "R20", "review"),
    ({"drawback": True}, "R6", "blocked"),
    ({"recon_flag": True, "recon_09_filed": True}, "R7", "blocked"),
    ({"on_cape_declaration": True}, "R18", "waiting"),
])
def test_gates(kw, rid, bucket):
    r = route(**kw)
    assert (r.rule_id, r.bucket) == (rid, bucket)


# --- status routing ---------------------------------------------------------------------
def test_unliquidated_files_now_with_projected_interest():
    r = route(liquidation_status="Not Liquidated")
    assert (r.rule_id, r.bucket) == ("R11", "cape_now")
    assert r.deadline is None and r.interest > 0


def test_liquidated_within_80_days_has_cape_deadline():
    r = route(liquidation_status="Liquidated", liquidation_date=date(2026, 8, 20))
    assert (r.rule_id, r.bucket) == ("R12", "cape_now")
    assert r.deadline == date(2026, 11, 8) and r.days_left == 14


def test_day_80_still_in_window_day_81_out():
    assert route(liquidation_status="Liquidated", liquidation_date=TODAY - timedelta(days=80)).rule_id == "R12"
    assert route(liquidation_status="Liquidated", liquidation_date=TODAY - timedelta(days=81)).rule_id == "R13"


def test_liquidated_81_to_180_days_needs_protest():
    r = route(liquidation_status="Liquidated", liquidation_date=date(2026, 6, 1))
    assert (r.rule_id, r.bucket, r.deadline_type) == ("R13", "protest", "PROTEST_180")
    assert r.deadline == date(2026, 11, 28)


def test_liquidated_over_180_days_is_litigation():
    r = route(liquidation_status="Liquidated", liquidation_date=date(2026, 3, 1))
    assert (r.rule_id, r.bucket, r.deadline_type) == ("R14", "litigation", "CIT_2YR")


def test_court_plaintiff_gets_phase_3():
    p = Profile(importer_number="12-3456789AA", cit_plaintiff=True, plaintiff_ior_submitted_by_cutoff=True)
    assert route(liquidation_status="Liquidated", liquidation_date=date(2026, 3, 1), profile=p).rule_id == "R15"
    p.plaintiff_ior_submitted_by_cutoff = False
    assert route(liquidation_status="Liquidated", liquidation_date=date(2026, 3, 1), profile=p).rule_id == "R15b"


def test_protests():
    r = route(protest_status="open", protest_solely_ieepa=True, liquidation_status="Liquidated", liquidation_date=date(2026, 9, 1))
    assert r.rule_id == "R8" and r.deadline_type == "CAPE_80" and "Withdraw" in r.action
    r = route(protest_status="open", liquidation_status="Liquidated", liquidation_date=date(2026, 5, 1))
    assert r.rule_id == "R8" and "Keep the protest" in r.action
    assert route(protest_status="denied", liquidation_status="Liquidated", liquidation_date=date(2026, 3, 1)).rule_id == "R8b"


def test_adcvd():
    assert route(entry_type="03", liquidation_status="Pending").rule_id == "R9"
    assert route(entry_type="03", liquidation_status="Suspended", suspension_record=True).rule_id == "R10"


def test_recon_flagged_and_psc():
    assert route(recon_flag=True, liquidation_status="Not Liquidated").rule_id == "R7b"
    assert route(needs_psc=True, liquidation_status="Not Liquidated").bucket == "fix_first"


def test_informal_entry_liquidates_at_payment():
    r = route(entry_type="11", entry_date=date(2025, 8, 1), deposit_date=date(2025, 8, 1))
    assert r.rule_id == "R14" and any("Informal" in n for n in r.notes)


def test_unknown_liquidation_estimated_and_flagged():
    r = route(entry_date=date(2025, 3, 1))  # +314 days -> liquidated ~Jan 2026 (estimated)
    assert r.liquidation_estimated and r.rule_id == "R14"
    r = route(entry_date=date(2026, 1, 15))  # +314 days is in the future -> unliquidated
    assert r.rule_id == "R11" and not r.liquidation_estimated


def test_someone_else_holds_claim():
    r = route(importer_number="98-7654321ZZ")
    assert r.holder == "someone_else"
    r = route(importer_name="UPS Customs Brokerage", importer_number="")
    assert r.holder == "someone_else"


def test_all_in_line_flags_overstatement():
    r = route(lines=[Line("001", "9903.02.20", 400.0)], liquidation_status="Not Liquidated")
    assert r.all_in_overstated and any("all-in" in n for n in r.notes)


# --- ledger -------------------------------------------------------------------------------
def test_analyze_headline_blockers_and_exports():
    entries = [
        entry(entry_number="B76-0324527-8", liquidation_status="Liquidated", liquidation_date=date(2026, 8, 20)),
        entry(entry_number="B76-0324527-8"),  # duplicate
        entry(entry_number="B760000001" + str(EN.check_digit("B760000001")), liquidation_status="Not Liquidated"),
        entry(entry_number="ABC12", liquidation_status="Not Liquidated"),  # bad format
        entry(entry_number="B760000002" + str(EN.check_digit("B760000002")), importer_number="99-0000000XX",
              liquidation_status="Not Liquidated"),
    ]
    p = Profile(importer_number="12-3456789AA", has_ace_account=None, ach_refund_enrolled=False)
    rep = A.analyze(entries, p, TODAY)
    h = rep["headline"]
    assert h["entries"] == 4 and h["duplicates"] == 1
    assert h["urgent_count"] == 1 and h["urgent_soonest_days"] == 14
    assert h["someone_else_count"] == 1
    keys = [b["key"] for b in rep["blockers"]]
    assert {"ace", "ach", "holder", "format", "dupes"} <= set(keys)
    csv_text = A.handoff_csv(rep)
    assert csv_text.splitlines()[0] == "Entry Number"
    assert "ABC12" not in csv_text and len(csv_text.splitlines()) == 3  # header + 2 valid actionable of mine
    ics = A.deadlines_ics(rep)
    assert "BEGIN:VEVENT" in ics and "CAPE window closes" in ics


def test_costs():
    opts = {o.key: o for o in compare(20, 14_000)}
    assert opts["self"].fee == 0
    assert opts["pct_broker"].fee == 10_000 and opts["pct_broker"].effective_pct == pytest.approx(71.4, abs=0.1)
    assert opts["contingency_30"].net == 9_800
    assert offer_cost(50_000, percent=25) == (12_500, 25.0)


def test_parse_es003_groups_lines_by_entry():
    text = (
        "Entry Summary Number,Entry Date,Entry Type Code,Entry Summary Line Number,Tariff Ordinal Number,"
        "HTS Number - Full,Line Tariff Goods Value Amount,Line Tariff Duty Amount,Liquidation Date,Liquidation Status\n"
        "B76-0324527-8,09/01/2025,01,001,1,8517620090,10000,0,08/20/2026,Liquidated\n"
        "B76-0324527-8,09/01/2025,01,001,2,9903012500,0,1000,08/20/2026,Liquidated\n"
    )
    entries, info = parse_csv(text)
    assert not info["missing"] and len(entries) == 1
    e = entries[0]
    assert e.liquidation_date == date(2026, 8, 20) and len(e.lines) == 2
    r = route_entry(e, ME, TODAY)
    assert r.rule_id == "R12" and r.principal == 1000


def test_news_date_parsing():
    from app.ai.tasks import _news_date

    assert _news_date("Mon, 19 Oct 2026 18:00:00 GMT") == date(2026, 10, 19)
    assert _news_date("2026-10-27T09:00:00Z") == date(2026, 10, 27)
    assert _news_date("") is None


def test_offer_verdict_is_decided_by_code():
    from app.ai.tasks import _verified, find_flags, offer_verdict

    offer = "Our fee is 15%. We never need your ACE login. Reply with your ACE Portal username and password today."
    assert _verified({"flag": "asks_for_ace_login", "evidence": "Reply with your ACE Portal username and password today"}, offer)
    assert not _verified({"flag": "asks_for_ace_login", "evidence": "We never need your ACE login"}, offer)  # negation
    assert not _verified({"flag": "upfront_payment", "evidence": "Our fee is 15%"}, offer)  # a fee isn't an upfront payment
    assert not _verified({"flag": "asks_for_bank_details", "evidence": "send us your bank account number"}, offer)  # not in the offer
    assert {f["flag"] for f in find_flags(offer)} == {"asks_for_ace_login", "urgency_pressure"}
    assert offer_verdict([{"flag": "asks_for_ace_login"}], 15, True) == "likely_scam"
    assert offer_verdict([{"flag": "urgency_pressure"}, {"flag": "guarantees_refund"}], 10, True) == "likely_scam"
    assert offer_verdict([], 30, True) == "expensive"
    assert offer_verdict([], 15, True) == "reasonable"


def test_entry_number_repair_uses_check_digit_and_known_filers():
    from app.engine import entry_number as EN

    known = {"K4M", "T2R", "Q7Z"}
    assert EN.repair("07Z-9282044-7", known) == ("Q7Z92820447", True)    # Q read as 0
    assert EN.repair("072-3954911-7", known) == ("Q7Z39549117", True)    # Q as 0 and Z as 2
    assert EN.repair("M4M-1898260-9", known) == ("K4M18982609", True)    # K as M
    assert EN.repair("K4M-970955-0", known) == ("K4M9709550", False)     # a dropped digit can't be fixed
    assert EN.repair("Q7Z-9282044-7", known) == ("Q7Z92820447", False)   # already valid
