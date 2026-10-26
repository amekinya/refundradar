"""Rule catalog: dates, pathways and the human-facing text for every routing rule.

Logic lives in rules.py; everything a court order or CBP message could change lives here.
Confidence tags: P = primary source read directly, S = secondary (law firm/broker/press),
U = unconfirmed or engineering inference. Full citations: docs/refund_rules_research.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

RULES_VERIFIED_AS_OF = date(2026, 10, 25)

# --- Key dates -------------------------------------------------------------------------
IEEPA_COLLECTION_END = date(2026, 2, 24)  # entries on/after this date carry no IEEPA duty (CSMS #67834313) [P]
PHASE1_OPEN = date(2026, 4, 20)  # [P]
PHASE2_OPEN = date(2026, 6, 29)  # reconciliation-flagged entries [P]
PHASE3_OPEN = date(2026, 10, 6)  # CIT plaintiffs with reliquidation order [P]
WAREHOUSE_REJECT_FROM = date(2026, 7, 7)  # types 21/22 rejected (CSMS #69127837) [P]
PLAINTIFF_IOR_CUTOFF = date(2026, 7, 30)  # first-wave Phase 3 access [P]
EARLIEST_CIT_DEADLINE = date(2027, 2, 1)  # counsel cite Feb 1-4, 2027 for 2-yr limit (28 USC 2636(i)) [S]
CLASS_SCHEDULING_ORDER_DUE = date(2026, 11, 5)  # Freestyle World class, no relief ordered yet [P]

CAPE_WINDOW_DAYS = 80  # CAPE acceptance must occur within 80 days of liquidation [P]
PROTEST_WINDOW_DAYS = 180  # 19 USC 1514(c)(3) [P]
ALERT_FROM_DAY = 70  # warn when an entry is within 10 days of the CAPE cutoff [U buffer]
NORMAL_LIQUIDATION_DAYS = 314  # typical CBP liquidation lag, used only as a fallback estimate [S]
CAPE_ACCEPTANCE_LAG_DAYS = 10  # practitioners report ~10 days to acceptance [S]
CAPE_LIQUIDATION_AFTER_ACCEPT_DAYS = 45  # unliquidated entries set to liquidate 45 days after acceptance [P]
DEPOSIT_LAG_DAYS = 10  # estimated gap between entry date and duty deposit (ACH statement) [U]

MAX_ENTRIES_PER_DECLARATION = 9999  # CSMS/TIN say 9,999; QRG says 10,000 & 1 MB -> use the stricter [P/U]


# --- User-facing pathway buckets ---------------------------------------------------------
@dataclass(frozen=True)
class Bucket:
    key: str
    label: str
    tone: str  # good | warn | bad | neutral
    blurb: str


BUCKETS: dict[str, Bucket] = {
    "cape_now": Bucket("cape_now", "File in CAPE now", "good", "Eligible for CBP's refund tool today."),
    "fix_first": Bucket("fix_first", "Fix, then file", "warn", "A correction (PSC) must come before the CAPE filing."),
    "protest": Bucket("protest", "Protest before the deadline", "warn", "No CAPE path today; a protest preserves your rights."),
    "litigation": Bucket("litigation", "Court route only", "bad", "Liquidation is final; only a court case or class relief can recover it."),
    "blocked": Bucket("blocked", "Blocked for now", "bad", "CBP has no process for this situation yet."),
    "waiting": Bucket("waiting", "Waiting on CBP", "neutral", "Accepted or pending; the refund comes later."),
    "not_eligible": Bucket("not_eligible", "Not eligible", "neutral", "No refundable IEEPA duty on this entry."),
    "review": Bucket("review", "Ask your broker", "warn", "The rules for this case aren't settled; don't guess."),
}


@dataclass(frozen=True)
class Rule:
    id: str
    title: str
    bucket: str
    action: str
    tag: str  # P / S / U
    sources: tuple[str, ...]


R = Rule
RULES: dict[str, Rule] = {r.id: r for r in [
    R("R0", "No refundable IEEPA duty on this entry", "not_eligible",
      "Nothing to claim. The entry has no dutiable IEEPA Chapter 99 line.", "P",
      ("CBP CAPE Quick Reference Guide (June 2026)",)),
    R("R0b", "Section 122 surcharge only (not IEEPA)", "protest",
      "Section 122 duties are not refundable through CAPE. A protest within 180 days of liquidation preserves rights; ask your broker or counsel.", "S",
      ("19 U.S.C. 1514(c)(3)", "Snell & Wilmer / Troutman client alerts")),
    R("R1", "Entered after IEEPA collection ended", "not_eligible",
      "IEEPA duties stopped on Feb 24, 2026. Nothing to claim.", "P", ("CSMS #67834313",)),
    R("R2", "Duties paid by a surety", "blocked",
      "CBP says not to file these in CAPE; no surety refund process exists yet. Tell your surety.", "P",
      ("CSMS #68340863", "ITSA letter, CIT ECF 56 (Sept 25, 2026)")),
    R("R3", "Not filed in ACE (e.g., postal/mail)", "blocked",
      "CAPE can't accept entries outside ACE. CBP lists this as unresolved; consider counsel.", "P",
      ("CBP Trade Information Notice (July 10, 2026)",)),
    R("R4", "Entry type CAPE doesn't accept", "not_eligible",
      "Types 08, 09, 23 and 47 are rejected by CAPE.", "P", ("CAPE QRG", "CSMS #68340863")),
    R("R5", "Warehouse entry (type 21/22)", "review",
      "Since July 7, 2026 CAPE rejects warehouse entries. File the withdrawal entries (types 31/32/34/38) instead.", "P",
      ("CSMS #69127837",)),
    R("R6", "Entry is on a drawback claim", "blocked",
      "CAPE rejects entries on drawback; CBP plans a later phase. If drawback isn't filed yet, file CAPE first.", "P",
      ("CSMS #68340863", "CAPE QRG")),
    R("R7", "Reconciliation entry (type 09) already filed", "blocked",
      "CAPE rejects these until a future phase.", "P", ("CSMS #69035485",)),
    R("R7b", "Reconciliation-flagged, no 09 filed yet", "cape_now",
      "File in CAPE (Phase 2), then file the reconciliation. Prioritize the reconciliation if it's due within 30 days.", "P",
      ("CSMS #69035485",)),
    R("R8", "Open protest on the entry", "review",
      "CAPE rejects protested entries. If the protest was only about IEEPA and it's within 80 days of liquidation, withdraw it and file CAPE; otherwise keep the protest.", "P",
      ("CSMS #68340863", "CIT order July 15, 2026")),
    R("R8b", "Protest denied", "litigation",
      "Court action at the CIT within 180 days of the denial notice. Refer to counsel.", "P", ("28 U.S.C. 2636(a)",)),
    R("R9", "AD/CVD entry pending liquidation", "waiting",
      "Not accepted yet. After it liquidates, file within 80 days.", "P", ("CSMS #68340863",)),
    R("R10", "AD/CVD entry suspended", "cape_now",
      "File in CAPE now; IEEPA duties come off, but the refund is paid only after Commerce lifts the suspension.", "P",
      ("Lord Decl. Mar 30, 2026", "Thomas Decl. June 4, 2026")),
    R("R11", "Unliquidated", "cape_now",
      "File in CAPE (Phase 1) now. Every day it waits risks liquidating with IEEPA duty and starting the 80-day clock.", "P",
      ("CSMS #68340863", "CBP TIN")),
    R("R12", "Liquidated within the last 80 days", "cape_now",
      "File in CAPE urgently. CBP must accept it by day 80 after liquidation.", "P",
      ("CSMS #68340863", "CAPE QRG", "Lord Decl. Mar 30, 2026")),
    R("R13", "Liquidated 81-180 days ago (not a court plaintiff)", "protest",
      "No CAPE path today. File a protest before day 180 to preserve rights, and/or talk to counsel about a CIT case.", "P",
      ("19 U.S.C. 1514", "CIT orders", "Thompson Coburn")),
    R("R14", "Liquidated over 180 days ago (not a court plaintiff)", "litigation",
      "Liquidation is final. Only a CIT case (then CAPE Phase 3) or class relief can recover it. Earliest suit deadlines are cited as Feb 1-4, 2027.", "S",
      ("19 U.S.C. 1514(a)", "28 U.S.C. 2636(i)", "Davis Wright Tremaine", "Leyton")),
    R("R15", "Court plaintiff, finally liquidated", "cape_now",
      "File in CAPE Phase 3 (open since Oct 6, 2026).", "P", ("Lord Decl. Oct 6, 2026", "CIT order July 17, 2026")),
    R("R15b", "Court plaintiff, IOR number sent after July 30", "waiting",
      "Phase 3 access pending; CBP will provide instructions.", "P", ("Lord Decl. Oct 6, 2026",)),
    R("R16", "Informal entry (type 11/12)", "review",
      "Informal entries liquidate on the date duty is paid, so most are already past 80-180 days. Confirm in ACE.", "U",
      ("19 CFR 159.10(a)",)),
    R("R17", "Foreign-trade-zone entry (type 06)", "cape_now",
      "Routed like a regular consumption entry; verify the Chapter 99 lines.", "U", ("CSMS #69035485",)),
    R("R18", "Already on an accepted CAPE declaration", "waiting",
      "Don't refile. Track it in ACE reports ES-022 and REV-603.", "P", ("CBP TIN",)),
    R("R19", "Needs a correction (PSC) before CAPE", "fix_first",
      "File the Post Summary Correction first, then CAPE. A PSC can never claim the IEEPA refund itself, and it's blocked once CAPE accepts the entry.", "P",
      ("CSMS #68340863", "CSMS #68397097", "CSMS #69056483")),
    R("R20", "Entry type not covered by any guidance", "review",
      "No source addresses this entry type. Ask your broker.", "U", ()),
    R("RX", "Liquidation date unknown", "review",
      "We estimated the liquidation date from the entry date. Confirm it in ACE (report ES-003 or ES-022) before acting.", "U",
      ("Troutman (314-day typical liquidation)",)),
]}
