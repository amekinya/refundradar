"""20 synthetic refund-recovery offers (10 predatory/scam, 10 legitimate) for the offer-check benchmark.
All company names are invented. Labels: likely_scam | expensive | reasonable."""
from __future__ import annotations

import json
import random
from pathlib import Path

rng = random.Random(568)
OUT = Path(__file__).parent / "offers"

SCAM = [
    ("Federal Refund Release Center", "We are authorized by U.S. Customs and Border Protection to release your pending IEEPA refund. Reply with your ACE Portal username and password so we can complete the release today.", ["claims_to_be_cbp_or_government", "asks_for_ace_login", "urgency_pressure"]),
    ("TariffCash Express", "Your refund of $86,400 is approved. To receive it, confirm your bank routing and account number and pay the $350 release fee by card within 24 hours.", ["asks_for_bank_details", "upfront_payment", "urgency_pressure"]),
    ("Customs Recovery Bureau", "FINAL NOTICE: unclaimed tariff refunds will be forfeited Friday. Scan the QR code to verify your company and claim your funds.", ["urgency_pressure", "qr_code_or_link_to_pay"]),
    ("RefundNow Trade Group", "We guarantee 100% recovery. Our team processes refunds directly with Customs outside the slow ACE system. Fee: 35% plus $750 onboarding, due upfront.", ["guarantees_refund", "processes_refunds_outside_ace", "upfront_payment"]),
    ("US Import Refund Office", "Our records from CBP show you paid $112,900 in IEEPA duties. Send a copy of your EIN letter and bank statement to start the refund transfer.", ["claims_to_be_cbp_or_government", "asks_for_bank_details"]),
    ("Liberty Duty Reclaim", "Act now — only 48 hours left to secure your refund. Provide ACE login access and we will handle everything. 40% success fee.", ["urgency_pressure", "asks_for_ace_login"]),
    ("Patriot Tariff Partners", "Click the link below to enter your banking details and receive your tariff refund deposit directly. No paperwork needed.", ["qr_code_or_link_to_pay", "asks_for_bank_details"]),
    ("Global Customs Settlement", "Pay a one-time $1,200 filing fee and we guarantee your refund within 10 days, bypassing the CBP queue.", ["upfront_payment", "guarantees_refund", "processes_refunds_outside_ace"]),
    ("Refund Assurance LLC", "Congratulations, you qualify for an expedited refund. Wire the $500 processing fee today to lock in your place.", ["upfront_payment", "urgency_pressure"]),
    ("Customs Rebate Center", "We are the official refund processing partner. Send your ACE credentials and we'll file for you. 30% fee, refund guaranteed.", ["claims_to_be_cbp_or_government", "asks_for_ace_login", "guarantees_refund"]),
]
LEGIT = [
    ("Harborline Customs Brokerage", "As your licensed customs broker, we can file a CAPE declaration for the entries we filed for you. Our fee is $150 per declaration. You'll need your own ACE account with refund bank details; we never need your login.", "reasonable"),
    ("Kestrel Trade Law PLLC", "Our firm reviews whether a protest or a Court of International Trade action makes sense for entries outside the CAPE window. Initial consultation is free; engagement terms are a 15% contingency with no upfront fee, detailed in a written engagement letter.", "reasonable"),
    ("Meridian Customs Services", "We prepare CAPE entry lists for importers at $90 per entry, check each entry's liquidation date, and confirm your ACH refund enrollment before you submit in ACE.", "reasonable"),
    ("Northgate Brokerage", "For our existing clients, we will submit CAPE declarations at no charge for entries under $5,000 in IEEPA duty, and $200 per declaration above that. You file nothing yourself unless you prefer to.", "reasonable"),
    ("Bluewater Trade Advisors", "We offer a fixed-fee review of your ES-003 report for $450, identifying CAPE-eligible entries and deadlines. Filing is done by you or your broker in ACE.", "reasonable"),
    ("Sterling Recovery Partners", "We handle CAPE, protests and litigation end to end for a 30% contingency fee on all amounts recovered, with a $5,000 minimum fee. No upfront cost.", "expensive"),
    ("Apex Tariff Recovery", "Full-service IEEPA refund recovery for 28% of the refund, including interest. We work with licensed brokers to file in ACE on your behalf.", "expensive"),
    ("Cedar Customs Brokerage", "We file CAPE for importers we represent with a power of attorney. Pricing: 2% of the refund with a $10,000 minimum and $100,000 cap.", "expensive"),
    ("Pinecrest Trade Compliance", "Our licensed brokers file your CAPE declaration and track refunds through ACE reports. Fee: $200 plus $125 per additional entry. We never ask for ACE passwords or bank details.", "reasonable"),
    ("Lakeview Customs Law", "We represent importers in Court of International Trade actions to preserve refunds on finally liquidated entries. Hourly rates apply; we'll estimate total cost after reviewing your entries.", "reasonable"),
]


def main():
    OUT.mkdir(exist_ok=True)
    labels = []
    for i, (name, body, flags) in enumerate(SCAM):
        text = f"Subject: Your IEEPA tariff refund\n\nDear importer,\n\n{body}\n\nSincerely,\n{name}\n(Fictional example for testing.)"
        (OUT / f"offer_{i:02d}.txt").write_text(text)
        labels.append({"file": f"offer_{i:02d}.txt", "label": "likely_scam", "flags": flags})
    for j, (name, body, label) in enumerate(LEGIT):
        i = j + len(SCAM)
        text = f"Subject: IEEPA refund support\n\nHello,\n\n{body}\n\nBest regards,\n{name}\n(Fictional example for testing.)"
        (OUT / f"offer_{i:02d}.txt").write_text(text)
        labels.append({"file": f"offer_{i:02d}.txt", "label": label, "flags": []})
    (OUT / "labels.json").write_text(json.dumps(labels, indent=1))
    print(f"wrote {len(labels)} offers")


if __name__ == "__main__":
    main()
