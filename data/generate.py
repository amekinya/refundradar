"""Generate the synthetic demo importer "Prairie Lantern Home Goods" (invented company, fake identifiers).

Each entry is created FROM a scenario (the route the written rules say it should take), so the
labels come from the decision table in docs/refund_rules_research.md, not from running our engine.
That keeps the accuracy benchmark honest.

Outputs (data/sample/):
  prairie_lantern_es003.csv   ES-003-shaped export (+ optional status columns a broker might add)
  prairie_lantern_labels.csv  expected rule / bucket / deadline type per entry
"""
from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from app.engine.entry_number import check_digit

TODAY = date(2026, 10, 25)
OUT = Path(__file__).parent / "sample"
FILER = "Q7Z"  # invented filer code
rng = random.Random(20261025)

BASE_HTS = [  # (HTS, description, general duty rate)
    ("9405.41.8400", "LED table lamps", 0.039),
    ("9405.11.8010", "Ceiling fixtures", 0.039),
    ("6302.31.9020", "Cotton bed linen", 0.067),
    ("9403.60.8081", "Wooden side tables", 0.0),
    ("6912.00.4810", "Ceramic serveware", 0.098),
    ("4420.90.8000", "Wooden decor boxes", 0.032),
    ("6307.90.9891", "Woven storage baskets", 0.07),
    ("7013.99.8000", "Glass candle holders", 0.06),
]


@dataclass
class Scenario:
    rule: str
    bucket: str
    deadline_type: str
    count: int


SCENARIOS = [
    Scenario("R11", "cape_now", "", 44),
    Scenario("R12", "cape_now", "CAPE_80", 36),
    Scenario("R13", "protest", "PROTEST_180", 30),
    Scenario("R14", "litigation", "CIT_2YR", 28),
    Scenario("R0", "not_eligible", "", 12),
    Scenario("R0b", "protest", "", 5),
    Scenario("R18", "waiting", "", 5),
    Scenario("R6", "blocked", "", 3),
    Scenario("R2", "blocked", "", 2),
    Scenario("R8", "review", "", 3),
    Scenario("R7b", "cape_now", "", 3),
    Scenario("R7", "blocked", "", 2),
    Scenario("R19", "fix_first", "", 2),
    Scenario("R4", "not_eligible", "", 2),
    Scenario("R5", "review", "", 2),
    Scenario("R10", "cape_now", "", 2),
    Scenario("R9", "waiting", "", 2),
    Scenario("R17", "cape_now", "", 2),
    Scenario("R16", "litigation", "CIT_2YR", 3),
]


def rand_date(a: date, b: date) -> date:
    return a + timedelta(days=rng.randint(0, (b - a).days))


def ieepa_lines(entry_date: date, value: float) -> tuple[str, list[tuple[str, float]]]:
    """Pick a country and the IEEPA Chapter 99 lines that applied on that date (simplified, plausible)."""
    country = rng.choices(["CN", "VN", "IN"], weights=[6, 3, 1])[0]
    lines: list[tuple[str, float]] = []
    if country == "CN":
        fent = 0.10 if entry_date < date(2025, 3, 4) else (0.20 if entry_date < date(2025, 11, 10) else 0.10)
        if entry_date >= date(2025, 2, 4):
            lines.append(("9903.01.24", round(value * fent, 2)))
        if entry_date >= date(2025, 5, 14):
            lines.append(("9903.01.25", round(value * 0.10, 2)))
    elif country == "VN":
        if entry_date >= date(2025, 8, 7):
            lines.append(("9903.02.69", round(value * 0.20, 2)))
        elif entry_date >= date(2025, 4, 5):
            lines.append(("9903.01.25", round(value * 0.10, 2)))
    else:  # India
        if entry_date >= date(2025, 8, 7):
            lines.append(("9903.02.26", round(value * 0.25, 2)))
            if date(2025, 8, 27) <= entry_date < date(2026, 2, 7):
                lines.append(("9903.01.84", round(value * 0.25, 2)))
        elif entry_date >= date(2025, 4, 5):
            lines.append(("9903.01.25", round(value * 0.10, 2)))
    if not lines:  # e.g., early CN/VN dates: fall back to China fentanyl so the scenario keeps IEEPA duty
        country = "CN"
        lines.append(("9903.01.24", round(value * 0.20, 2)))
    return country, lines


def make_entry_number(seq: int) -> str:
    first10 = f"{FILER}{seq:07d}"
    return f"{FILER}-{seq:07d}-{check_digit(first10)}"


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    rows, labels = [], []
    seq = 4_100_000
    for sc in SCENARIOS:
        for _ in range(sc.count):
            seq += rng.randint(1, 37)
            num = make_entry_number(seq)
            etype, status, liq = "01", "", None
            extra = {k: "" for k in ("Protest Status", "Protest Solely IEEPA", "Drawback", "Recon Flag", "Recon 09 Filed",
                                     "Surety Paid", "Suspension Record", "AD CVD", "On CAPE Declaration", "Needs PSC",
                                     "Deposit Date")}
            ieepa = True
            s122 = False
            if sc.rule in {"R11", "R7b", "R19", "R10", "R9", "R17", "R18"}:
                ed = rand_date(date(2025, 12, 16), date(2026, 2, 23))
                status = "Not Liquidated"
                if sc.rule == "R7b":
                    extra["Recon Flag"] = "Y"
                if sc.rule == "R19":
                    extra["Needs PSC"] = "Y"
                if sc.rule == "R10":
                    etype, status, extra["Suspension Record"], extra["AD CVD"] = "03", "Suspended", "Y", "Y"
                if sc.rule == "R9":
                    etype, status, extra["AD CVD"] = "03", "Pending", "Y"
                if sc.rule == "R17":
                    etype = "06"
                if sc.rule == "R18":
                    extra["On CAPE Declaration"] = "Y"
            elif sc.rule == "R12":
                # ~35% land in the last 3 weeks of their window so the demo has real urgency
                if rng.random() < 0.35:
                    liq = rand_date(TODAY - timedelta(days=77), TODAY - timedelta(days=60))
                else:
                    liq = rand_date(TODAY - timedelta(days=59), TODAY - timedelta(days=1))
                ed, status = liq - timedelta(days=314), "Liquidated"
            elif sc.rule == "R13":
                liq = rand_date(TODAY - timedelta(days=180), TODAY - timedelta(days=81))
                ed, status = liq - timedelta(days=314), "Liquidated"
            elif sc.rule == "R14":
                liq = rand_date(date(2025, 12, 20), TODAY - timedelta(days=181))
                ed, status = liq - timedelta(days=314), "Liquidated"
                ed = max(ed, date(2025, 2, 4))
            elif sc.rule == "R16":
                etype = "11"
                ed = rand_date(date(2025, 3, 10), date(2025, 9, 30))
                extra["Deposit Date"] = ed.strftime("%m/%d/%Y")
            elif sc.rule == "R0":
                ieepa = False
                ed = rand_date(date(2025, 3, 1), date(2026, 2, 20))
                status = "Not Liquidated" if ed > date(2025, 12, 15) else "Liquidated"
                liq = None if status == "Not Liquidated" else ed + timedelta(days=314)
                if liq and liq > TODAY:
                    status, liq = "Not Liquidated", None
            elif sc.rule == "R0b":
                ieepa, s122 = False, True
                ed = rand_date(date(2026, 2, 24), date(2026, 4, 30))
                status = "Not Liquidated"  # normal ~314-day liquidation hasn't happened yet
            else:  # status-flag gates on otherwise CAPE-eligible entries
                ed = rand_date(date(2025, 12, 16), date(2026, 2, 23))
                status = "Not Liquidated"
                if sc.rule == "R6":
                    extra["Drawback"] = "Y"
                if sc.rule == "R2":
                    extra["Surety Paid"] = "Y"
                if sc.rule == "R7":
                    extra["Recon Flag"], extra["Recon 09 Filed"] = "Y", "Y"
                if sc.rule == "R4":
                    etype = "47"
                if sc.rule == "R5":
                    etype = "21"
                if sc.rule == "R8":
                    liq = rand_date(TODAY - timedelta(days=170), TODAY - timedelta(days=90))
                    ed, status = liq - timedelta(days=314), "Liquidated"
                    extra["Protest Status"] = "open"
            # lines
            n_lines = rng.choice([1, 1, 2, 2, 3])
            line_no = 0
            for _ in range(n_lines):
                line_no += 1
                hts, desc, rate = rng.choice(BASE_HTS)
                value = float(rng.randrange(700, 6200, 25))
                base_duty = round(value * rate, 2)
                ordinal = 1
                if ieepa:
                    country, chap99 = ieepa_lines(ed, value)
                else:
                    country = "MX" if not s122 else "CN"
                    chap99 = [("9903.01.04", 0.0)] if not s122 else [("9903.03.01", round(value * 0.10, 2))]
                rows.append(_row(num, ed, etype, line_no, ordinal, hts, value, base_duty, liq, status, country, extra))
                for c_hts, c_duty in chap99:
                    ordinal += 1
                    rows.append(_row(num, ed, etype, line_no, ordinal, c_hts, 0.0, c_duty, liq, status, country, extra))
            labels.append({"Entry Number": num, "expected_rule": "R14" if sc.rule == "R16" else sc.rule, "expected_bucket": sc.bucket,
                           "expected_deadline_type": sc.deadline_type})
    rng.shuffle(rows)
    rows.sort(key=lambda r: (r["Entry Summary Number"], r["Entry Summary Line Number"], r["Tariff Ordinal Number"]))
    with open(OUT / "prairie_lantern_es003.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "prairie_lantern_labels.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(labels[0].keys()))
        w.writeheader()
        w.writerows(labels)
    return len(labels), len(rows)


def _row(num, ed, etype, line_no, ordinal, hts, value, duty, liq, status, country, extra):
    return {
        "Entry Summary Number": num,
        "Entry Date": ed.strftime("%m/%d/%Y"),
        "Entry Type Code": etype,
        "Entry Summary Line Number": f"{line_no:03d}",
        "Tariff Ordinal Number": ordinal,
        "HTS Number - Full": hts.replace(".", "") + ("00" if hts.startswith("9903") else ""),
        "Line Tariff Goods Value Amount": f"{value:.2f}",
        "Line Tariff Duty Amount": f"{duty:.2f}",
        "Country of Origin Code": country,
        "Liquidation Date": liq.strftime("%m/%d/%Y") if liq else "",
        "Liquidation Status": status,
        **extra,
    }


if __name__ == "__main__":
    n, r = build()
    print(f"wrote {n} entries / {r} rows to {OUT}")
