# RefundRadar: IEEPA Tariff Refund Rules Research

**As of:** October 25, 2026
**Purpose:** Rule-engine specification input for RefundRadar, covering pathway, amount, deadlines and blockers per customs entry.
**Method:** I read primary sources directly wherever possible: CBP CSMS messages, CBP Trade Information Notices and the CAPE Quick Reference Guide, CBP declarations filed at the Court of International Trade (CIT), CIT orders, the Federal Register, US Code and eCFR text, and the USITC HTS database. Law-firm and broker sources fill gaps and are labelled as such.

### Confidence tags used throughout

| Tag | Meaning |
|---|---|
| **[P]** | Primary source read directly in this research (CBP, CIT, Federal Register, statute, regulation, USITC HTS). |
| **[S]** | Secondary source: a law firm, broker or trade press. No primary text was found or readable. |
| **[U]** | Unconfirmed, conflicting, or an engineering inference by the author. Do not hard-code without review. |

> **Access limitation.** CBP's own *IEEPA Duty Refunds* web page (cbp.gov/trade/programs-administration/trade-remedies/ieepa-duty-refunds), including its refund FAQs, returned HTTP 403 to automated access. CBP PDFs were readable through a text mirror. Any rule that appears **only** on that page is therefore not captured here. Check it manually before launch.

---

## 0. Status snapshot (October 25, 2026)

| Item | Value | Source |
|---|---|---|
| Supreme Court decision | *Learning Resources, Inc. v. Trump*, 607 U.S. 229 (decided Feb 20, 2026): IEEPA "does not authorize the President to impose tariffs." | [P] CIT order, July 17, 2026 (ECF 52, Euro-Notions) |
| IEEPA collection ended | 12:00 a.m. ET, **Feb 24, 2026**, for goods entered or withdrawn for consumption on or after that time. Section 232 and Section 301 duties were not affected. | [P] CSMS #67834313 (Feb 22, 2026) |
| Total IEEPA pool | "Over 330,000 importers have made over 53 million entries… approximately **$166 billion**" (as of Mar 4, 2026). The brief's "333K+" figure was **not** confirmed; the primary source says "over 330,000". | [P] Thomas Decl. ¶5 (June 4, 2026) |
| CAPE Phase 1 | Live **Apr 20, 2026** at 7:11 a.m. ET (scheduled for 8 a.m.). Covers unliquidated entries and entries ≤80 days past liquidation. | [P] Lord Decl. Oct 6, 2026 ¶3; CSMS #68340863 |
| "Phase 2" (reconciliation-flagged entries) | Live **June 29, 2026** at 5:00 a.m. ET. | [P] CSMS #69035485; Lord Decl. ¶7 |
| CAPE Phase 3 | Live **Oct 6, 2026** at 5:10 a.m. ET. Covers finally liquidated entries of **CIT plaintiffs** that have a court reliquidation order. 477 declarations and 425,517 entries were accepted by noon on day one. | [P] Lord Decl. Oct 6, 2026 ¶8 |
| CAPE totals (Oct 2, 2026) | 297,887 declarations submitted, 209,262 passed file validation, 27.4M entries, 21.19M liquidated or reliquidated without IEEPA duties, 6.2M entries failed entry validation. **$136.6B** accepted. **$126B** (duties plus interest) certified and sent to Treasury. | [P] Lord Decl. Oct 6, 2026 ¶¶3-5 |
| Held for missing ACH information (Oct 2, 2026) | **20,362 refunds, about $1.1B** | [P] Lord Decl. Oct 6, 2026 ¶6 |
| Class action | *Freestyle World v. CBP*, CIT No. 26-01088, Slip Op. 26-123, class certified **Oct 8, 2026**. No classwide relief has been ordered yet. Proposed scheduling order now due **Nov 5, 2026**. | [P] Slip Op. 26-123; ECF 63 (Oct 23, 2026) |
| Government appeal (universal relief for non-plaintiffs) | Pending at the Federal Circuit (Nos. 2026-1895, -1897, -1899). No decision found as of mid-October 2026. | [S] Diaz (Aug 12), Husch Blackwell (Oct 9) |
| Next CBP status report | Due Oct 26, 2026, with a settlement conference on Oct 27, 2026. **Re-check after these dates.** | [P] Order, Oct 8, 2026 (ECF 60) |

### Key timeline

| Date | Event | Tag |
|---|---|---|
| Mar 2, 2026 | Federal Circuit issues mandate to the CIT. | [P] CSMS #68340863 |
| Mar 4, 2026 | CIT order in *Atmus Filtration* (No. 26-01259): liquidate unliquidated entries and reliquidate non-final liquidated entries "without regard to IEEPA duties." | [P] |
| Mar 6, 2026 | CIT suspends the order's requirement of immediate compliance so CBP can build CAPE. | [P] |
| Mar 20 / Mar 27, 2026 | Order amended. The Mar 27 amendment adds finally liquidated entries. CBP limits Phase 1 to unliquidated entries and entries inside the 90-day window of 19 U.S.C. 1501. | [P] Lord Decl. Mar 30 ¶7 |
| Apr 7, 2026 | *Euro-Notions* order (similar relief; immediate compliance suspended). | [P] CSMS #68340863 |
| Apr 13, 2026 | CSMS #68340863 publishes the Phase 1 rules. | [P] |
| Apr 17, 2026 | CIT enters "universal" injunctions covering all importers. | [S] Diaz Trade Law |
| Apr 20, 2026 | Phase 1 goes live. CSMS #68397097 adds PSC error 864. | [P] |
| June 2-3, 2026 | DOJ appeals the universal relief, citing *Trump v. CASA*. | [P] Thomas Decl. ¶12; [S] |
| June 23 / 25 / 29, 2026 | CSMS #69035485 (reconciliation-flagged entries), CSMS #69056483 (validation changes), Phase 2 deployed (CSMS #69066837 "DEPLOYED"). | [P]/[S] |
| July 2, 2026 | CSMS #69127837: warehouse entry types 21 and 22 are rejected from July 7. | [P] |
| July 17, 2026 | Eaton order, entered in about 3,700 cases: CBP shall reliquidate plaintiffs' entries "liquidated for more than 80 days," once plaintiffs submit IOR numbers and CBP accepts their CAPE declarations. | [P] ECF 52 (Euro-Notions) |
| July 30, 2026 | Cutoff for plaintiffs' IOR-number submission for first-wave Phase 3 access. | [P] Lord Decl. Sept 15 ¶8 |
| Aug 25, 2026 | CBP delays Phase 3 to build validations ensuring "no other duty adjustments are made to finally liquidated entries outside of the IEEPA duty refunds." | [P] Lord Decl. Aug 25 ¶8 |
| Sept 9, 2026 | Letter from ten House Democrats (led by Reps. Stevens and Horsford) to Commissioner Scott. They say slow ACE/CAPE access made importers miss CBP's 90-day window, meaning the 19 U.S.C. 1501 voluntary-reliquidation window measured from liquidation. | [S] IANS/NewKerala (Sept 10); shopappy. The letter text itself was not retrieved. |
| Oct 6, 2026 | Phase 3 deployed. Per DWT, **no CSMS** was issued for it. | [P] Lord Decl.; [S] DWT |
| Oct 8, 2026 | Class certified. | [P] |

---

## (a) Decision table: entry attributes → pathway → deadline → action

Evaluate the rules **in order**. The first matching rule sets the pathway. Rules R0 to R6 are gates; rules R7 onward route by entry status.
`T` = today. `L` = liquidation date (or latest reliquidation date) from ACE. `days = T − L`.

| # | Condition (entry attributes) | Pathway | Deadline / timing | Action for user | Tag |
|---|---|---|---|---|---|
| R0 | No **dutiable** IEEPA Chapter 99 line (IEEPA heading with duty > $0) on the entry. | **Not eligible (no IEEPA duty).** CAPE error "NO IEEPA HTS ON ENTRY". | none | Check whether the only extra duty is Section 122 (9903.03.xx); if so, go to R0b. Otherwise stop. | [P] QRG |
| R0b | Only Section 122 lines (9903.03.01; entries Feb 24 to July 23, 2026). | **Not refundable via CAPE.** Protest or CIT litigation. | Protest within 180 days of liquidation (19 U.S.C. 1514(c)(3)). | Flag "Section 122, not IEEPA." Suggest protest or counsel. | [P] statute; [S] Snell & Wilmer, Troutman |
| R1 | Entry date (Block 7) on or after 2026-02-24 00:00 ET. | Not eligible (IEEPA no longer collected). | none | Stop. | [P] CSMS #67834313 |
| R2 | A **surety** paid the IEEPA duties in whole or in part. | **Blocked / unresolved.** CBP: "do not submit a CAPE Declaration." No surety refund process exists yet. | none | Show as blocked. Notify the surety. | [P] CSMS #68340863; ITSA letter (ECF 56, Sept 25) |
| R3 | Entry not filed in ACE, has no liquidation status in ACE, or is a postal/mail shipment with no ACE entry. | **Unresolved.** Not accepted by CAPE. CBP has named this as a remaining category with no date. | none | Show as unresolved; suggest counsel. | [P] TIN (July 10); Thomas Decl. ¶¶13, 21 |
| R4 | Entry type **08** (duty deferral), **09** (reconciliation), **23** (TIB) or **47** (drawback). | **Not accepted** ("ENTRY TYPE NOT ALLOWED"). | none | For type 09, see R7. Otherwise show as not CAPE-eligible. | [P] QRG; CSMS #68340863 |
| R5 | Entry type **21 / 22** (warehouse / re-warehouse). | **Not accepted since July 7, 2026.** File the **withdrawals** (31/32/34/38) instead. Type 21/22 entries accepted Apr 20 to July 6 without their withdrawals **will not** be refunded. | Withdrawal refunds are paid when the warehouse entry liquidates in the normal course after final withdrawal. | Ask for the withdrawal entry numbers and route each withdrawal through R7 onward. | [P] CSMS #69127837 |
| R6 | Entry is on a **drawback claim**. | **Blocked** ("ENTRY ON DRAWBACK"). Planned for a future phase; no date. | none | If drawback is **not yet filed**: file CAPE first, then drawback. | [P] CSMS #68340863; QRG; Thomas Decl. ¶13 |
| R7 | Flagged for reconciliation (types 01/02/06) **with** a type 09 reconciliation entry already on file. | **Blocked** ("RECON ALREADY FILED FOR ENTRY SUMMARY"). Future phase; no date. | none | Show as blocked. | [P] CSMS #69035485; QRG |
| R7b | Flagged for reconciliation, **no** type 09 filed, and unliquidated or ≤80 days past liquidation. | **CAPE "Phase 2"** (open since June 29, 2026). | Same 80-day rule. If the reconciliation filing deadline is <30 days away, **prioritize filing the reconciliation**. | File CAPE, then file the 09. CBP treats the CAPE declarations as filed and accepted when the 09 is filed. | [P] CSMS #69035485 |
| R8 | Entry is under an **open or suspended protest**. | **CAPE rejects** ("PROTEST ON ENTRY"). | If the protest was solely for IEEPA and `days ≤ 80`: withdraw the protest (have the Center lift any suspension first), then file CAPE Phase 1. If `days > 80`: keep the protest (CBP is developing protest functionality, no date). A plaintiff may instead consider withdrawing and using Phase 3. | Route by `days`. | [P] CSMS #68340863; CIT order July 15; [S] Morgan Lewis (the plaintiff option) |
| R8b | Protest **denied**. QRG: "Entry cannot be in Denied status if AFR box is checked." | CIT action under 28 U.S.C. 1581(a). | **180 days** from mailing of the denial notice (28 U.S.C. 2636(a)). | Refer to counsel. | [P] statute; QRG |
| R9 | AD/CVD entry (types 03/07/34/38) whose liquidation status is **Pending**, or for which Commerce has issued liquidation instructions (pending under 1504(d)). | **Not accepted now.** | After it liquidates, file within 80 days of liquidation (R11). | Monitor the liquidation date. | [P] CSMS #68340863 (item i); TIN |
| R10 | AD/CVD entry **suspended** pending Commerce instructions. | **CAPE Phase 1.** IEEPA duties are removed now; the refund is paid only after Commerce lifts the suspension and CBP liquidates. | Indefinite (depends on Commerce). | File CAPE. Show as "accepted, refund deferred." | [P] Lord Decl. Mar 30 ¶14a; Thomas ¶19; [S] Steptoe |
| R11 | **Unliquidated** (including liquidation status Extended, Suspended or Under Review). | **CAPE Phase 1.** | Plain unliquidated entries are set to liquidate **45 days** after acceptance; refund generally **60-90 days** after acceptance. Extended, suspended and under-review entries keep their status and are refunded at liquidation. | File CAPE **now**. If ACE would liquidate the entry on its normal schedule soon, the clock in R12 starts at that point. | [P] CSMS #68340863; TIN. **[U]** QRG lists errors for "under review" and "has suspension record"; see §(g). |
| R12 | Liquidated and `days ≤ 80`. | **CAPE Phase 1** (reliquidated next business day). | **Hard deadline:** CAPE acceptance must occur by `L + 80`. As of today, that means liquidated on or after **Aug 6, 2026**. | File **urgently**. Alert at day 70 or later. | [P] CSMS #68340863; QRG; Lord Decl. Mar 30 ¶15c |
| R13 | Liquidated, `81 ≤ days ≤ 180`, no protest, **not** a CIT plaintiff. | **No CAPE path today.** File a protest under 19 U.S.C. 1514 to preserve rights, and/or sue at the CIT under 28 U.S.C. 1581(i), then use Phase 3. | Protest by **`L + 180`**. As of today, that means liquidated on or after **Apr 28, 2026**. CAPE will reject protested entries until protest functionality ships. | Generate a protest-deadline alert and counsel referral. | [P] statute; CIT orders; [S] Thompson Coburn, MF Masuda |
| R14 | Liquidated, `days > 180`, no protest, **not** a CIT plaintiff. | Liquidation is **final and conclusive** (1514(a)). **Only route:** a CIT 1581(i) action followed by a reliquidation order and Phase 3. Class membership in *Freestyle World* is the alternative, but no relief has been ordered and tolling is unresolved. | 2-year limitations period (28 U.S.C. 2636(i)) "after the cause of action first accrues." Counsel cite **Feb 1-4, 2027** as the earliest deadlines. | Refer to counsel. Show as "litigation only." | [P] statute; [S] DWT, Leyton, Faegre via Leyton |
| R15 | **CIT plaintiff**, entry liquidated more than 80 days ago, covered by the July 17, 2026 reliquidation order, and IOR number submitted to CBP **by July 30, 2026**. | **CAPE Phase 3** (open since Oct 6, 2026). | No closing date announced. Multiple declarations are allowed as further entries become final. | File a CAPE declaration (same CSV). Reliquidation occurs only after CBP accepts it. | [P] Lord Decl. Oct 6 ¶8; ECF 52 |
| R15b | CIT plaintiff whose IOR number was submitted **after** July 30, 2026. | Phase 3 pending: "CBP will provide additional instructions." | Unknown. One firm reports "rolling biweekly" access. | Show as waiting on CBP instructions. | [P] Lord Decl.; [S] Troutman |
| R16 | Informal entry, type **11** (or 12). | The same status rules apply, but informal entries are **liquidated on the date duty is paid** (19 CFR 159.10(a)). An informal IEEPA entry would therefore have passed 80 days roughly 80 days after payment, and 180 days by about late August 2026. | Usually R14 today (litigation only). | Use the ACE liquidation date if available; otherwise use the payment date. | [P] 19 CFR 159.10; Lord Decl. Mar 12 ¶11 ("formal and informal entries"); **[U]** see §(g) |
| R17 | FTZ consumption entry, type **06**. | No FTZ-specific CAPE rule was found. Treated like type 01 under R7 to R15. Type 06 is listed among the reconciliation-flag-eligible types. | Same clocks as R7-R15. | Route normally. Flag "FTZ: verify Chapter 99 lines." | [P] CSMS #69035485; **[U]** |
| R18 | Entry already on an accepted CAPE declaration. | **Duplicate.** Do not refile. | none | Track via ES-022 and REV-603. | [P] TIN ("not duplicated in same or prior declaration") |
| R19 | Entry needs a **Post Summary Correction** for a *non-IEEPA* issue, such as AGOA or Haiti HOPE/HELP for Oct 1, 2025 to Feb 3, 2026, or a fix for an INVALID HTS or HTS RELATIONSHIP MISMATCH error. | File the **PSC first**, then CAPE. A PSC can **never** be used to request an IEEPA refund. A PSC is blocked once CAPE is accepted (error 864, "PSC NOT ALLOWED – REFUND REQUESTED"). | Standard PSC timing applies. **[U]** It was not re-verified here. | Sequence: PSC, then CAPE. | [P] CSMS #68340863, #68397097, #69056483 |
| R20 | Entry types 51/52 (government) or 61-63 (transportation). | Not addressed by any source. Type 61-63 entries carry no duty. | none | Show as unknown or not applicable. | [U] |

### Date heuristics for when the actual liquidation date is unknown (use only as a fallback)

These are estimates labelled **[U]**. Always prefer the ACE liquidation date from ES-003 or ES-022.

- **Normal liquidation:** about **314 days** after entry under CBP practice [S] (Troutman, Dec 19, 2025). The statutory outer limit is 1 year, after which the entry is deemed liquidated (19 U.S.C. 1504(a); 19 CFR 159.11) [P].
- Entries on or after about **Dec 15, 2025** (that is, today minus 314 days) are probably still unliquidated (R11).
- Entries from about **Sept 26 to Dec 14, 2025** were probably liquidated within the last 80 days (R12).
- Entries from about **June 18 to Sept 25, 2025** were probably liquidated 81 to 180 days ago (R13).
- Entries before about **June 18, 2025** are probably past the protest window (R14).

### Phase summary

| Phase | Opened | Covers | Who | Closing date |
|---|---|---|---|---|
| Phase 1 | Apr 20, 2026 | Unliquidated entries; entries ≤80 days past liquidation; suspended, extended and under-review entries (refund at liquidation); warehouse withdrawals (31/32/34/38); suspended AD/CVD entries (refund after Commerce instructions). | Any IOR, or the broker that filed the entries. | None announced. The 80-day limit is a rolling per-entry clock. [P] |
| "Phase 2" | June 29, 2026 | Reconciliation-flagged 01/02/06 entries with no 09 filed, under the same 80-day rule. | Same as Phase 1. | None announced. [P] |
| Phase 3 | Oct 6, 2026 | Entries liquidated more than 80 days ago, including finally liquidated entries, of **CIT plaintiffs** covered by a reliquidation order. | Plaintiffs whose IOR numbers reached CBP via counsel by July 30, 2026; later submitters await instructions. | None announced. [P] |
| Not yet built | n/a | Reconciliation entries with 09 filed; drawback-designated entries; protested entries; non-ACE entries (including postal); surety-paid entries; finally liquidated entries of non-plaintiffs. | n/a | CBP gives no dates. Non-plaintiffs depend on the appeal or the class action. [P] Thomas ¶¶12-13 |

### Meaning of "finally liquidated" (an ambiguity the engine must handle)

- **CBP and the CIT** use "finally liquidated" to mean liquidated more than 90 days ago, that is, beyond 19 U.S.C. 1501 voluntary reliquidation. [P] (CIT order of July 17, 2026, fn. 2: "entries that have been liquidated for more than 90 days and are thus beyond the period for reliquidation set out in 19 U.S.C. § 1501.")
- **Classic customs law** treats a liquidation as final and conclusive once the 180-day protest period lapses with no protest. [P] 19 U.S.C. 1514(a), (c)(3)
- **The 80-day cutoff** is CBP's own rule, chosen so that reliquidation completes by day 90. [P] Lord Decl. Mar 30 ¶15c
- **For non-plaintiffs:** an entry 81 to 180 days past liquidation is "final" under CBP's usage, but a protest can still be filed. Store both flags: `past_1501_window` and `past_protest_window`.

### Liquidation timing (Question 6)

- **No blanket extension or suspension.** CBP did not extend or suspend liquidation of IEEPA entries generally. In *AGS Company Automotive Solutions v. US* (Slip Op. 25-154, Dec 15, 2025), the CIT refused to halt liquidation [S]. CBP told the court in June 2026 that "unliquidated entries will continue to automatically liquidate with IEEPA duties unless they have been included on a CAPE declaration" and that it cannot prevent this [P] (Thomas Decl. ¶18).
- **Individual reviews.** CBP may extend liquidation on individual entries for review [S] (Thompson Coburn FAQ 2). The Secretary's extension authority is 19 U.S.C. 1504(b) [P].
- **Effect on routing.** Each entry's phase is set by its *own* liquidation date. Every day an unliquidated entry is not filed risks it liquidating with IEEPA duty and starting the 80-day clock.
- **Effect of a CAPE filing.** CAPE resets liquidation to 45 days after acceptance. CBP processes CAPE liquidations Monday through Thursday each week [P] (Lord Decl. Mar 12 ¶7).

---

## (a.2) Legal and policy status as of October 2026 (Question 7)

1. **Universal relief appeal.** The government appealed in June 2026 the CIT's April 17 universal injunctions to the extent they reach non-plaintiffs and finally liquidated entries (Fed. Cir. Nos. 2026-1895, -1897, -1899). DOJ filed its opening brief on Aug 10, 2026, and importers filed theirs on Oct 5, 2026. No decision was found [S] (Diaz Trade Law, Aug 12; Husch Blackwell, Oct 9). One secondary source says oral argument was "scheduled for Aug 19," which does not fit with briefing still continuing in October [U].
2. **The government's position.** CBP "does not intend to refund IEEPA duties on entries of non-plaintiffs that liquidated beyond the 80-day period" while the appeal is pending [P] (Thomas Decl. ¶12). The government is **not** challenging party-specific orders [S].
3. **Plaintiff-specific reliquidation orders.** These were entered July 17, 2026 in about 3,700 cases [P]. DWT reports Judge Eaton has issued individual refund orders within about 4 business days of a new filing, and CBP has granted CAPE access within about 1 business day [S].
4. **Class action.** *Freestyle World* class certified Oct 8, 2026.
   - Definition: "All importers of record who paid duties imposed by the Challenged Tariff Orders between February 1, 2025, and February 19, 2026, excluding any entity that has separately filed an action seeking to recover IEEPA duties payments."
   - Rule 23(b)(2) class with no opt-out.
   - No relief has been ordered yet. The scheduling-order deadline was extended to **Nov 5, 2026** [P].
   - Brazil and India orders are reported to be outside the class (the *V.O.S.* class motion is still pending) [S] (DWT, Leyton).
   - A government appeal of certification is "expected." It was not seen on the CIT docket through Oct 23, 2026 [U].
   - Whether passive class membership tolls the 2-year limitations period is unresolved [S].
5. **Replacement tariffs.**
   - **Section 122:** a 10% surcharge, HTS 9903.03.01, from **Feb 24, 2026** to **July 24, 2026** (150 days) [P] HTS; [S] Snell & Wilmer.
   - The CIT held it unlawful on May 7, 2026 (*Oregon v. Trump*; *Burlap & Barrel v. Trump*), with relief limited to the plaintiffs [S]. A Federal Circuit stay is reported by different firms as May 12 and as June 11 [U].
   - Section 122 duties are **not refundable via CAPE** [S].
   - No Section 338 action was found in the sources reviewed [U].
   - Section 232 and 301 duties continue [P] (CSMS #67834313).
6. **No deadline extensions.** CBP has not announced any extension of the 80-day CAPE window or of the protest window. The Sept 9 congressional letter asked for refunds but proposed no tolling mechanism [S].
7. **Changes since Phase 3 opened.**
   - Oct 8: class certified.
   - Oct 8 order: importers whose refunds fall short should contact the CBP Centers of Excellence and Expertise [P].
   - Oct 21-23: scheduling order extended to Nov 5 [P].
   - Oct 26: next CBP CAPE report due [P].
   - No new CSMS about CAPE was found after Oct 6 [U].

---

## (b) Data dictionary: fields the engine needs per entry

### b.1 CBP Form 7501 (Entry Summary) fields

Source: the CBP Form 7501 (06/09) layout and the CBP Form 7501 Instructions, read directly [P].
**[U]** These are older copies. CBP's 2023 revision could not be retrieved, so confirm the box numbering before relying on it.

| Block | Field | Format / notes | Engine use |
|---|---|---|---|
| 1 | Filer Code / Entry No. | 11 alphanumeric characters: 3-character filer code, 7-digit number (leading zeros kept), 1 check digit. Displayed as `XXX-XXXXXXX-X` (e.g., `B76-0324527-8`). The check-digit algorithm is in Appendix 1 (see §c.4). | Primary key; CAPE CSV value. |
| 2 | Entry Type | 2-digit code (list below). May carry an ABI suffix such as `ABI/A`, `ABI/P`, `ABI/S` or `ABI/N`, plus `/L` for "live" entries. | Rules R4-R6, R9, R16, R17. |
| 3 | Summary Date | MM/DD/YYYY; the date the entry summary was filed. | Informational. |
| 4 | Surety No. | 3-digit surety code. `999` means no surety; `998` means cash in lieu of surety. | Surety flag context. |
| 5 | Bond Type | `0` government/no bond; `8` continuous; `9` single transaction. | Context. |
| 6 | Port Code | `DDPP` (Schedule D). | Center routing context. |
| 7 | Entry Date | MM/DD/YYYY; date of release (exceptions in 19 CFR 141.68). For a warehouse withdrawal, the date of withdrawal. | R1 cutoff (before Feb 24, 2026); 314-day estimate. |
| 8 | Importing Carrier | Vessel name or carrier code. | none |
| 9 | Mode of Transport | Code. | In-transit exception context (vessel only). |
| 10 | Country of Origin | ISO code, or `MULTI` with per-line `O`+ISO codes in column 27. | IEEPA program mapping. |
| 11 | Import Date | MM/DD/YYYY; date of arrival. | Context. |
| 12 | B/L or AWB No. | Text. | none |
| 13 | Manufacturer ID | MID. | none |
| 14 / 15 | Exporting Country / Export Date | ISO code / date. | Transit-exception context. |
| 16 / 17 | I.T. No. / I.T. Date | Text / date. | Determining-date context. |
| 18 | Missing Docs | Code. | none |
| 19 / 20 | Foreign Port of Lading / U.S. Port of Unlading | Codes. | none |
| 21 | Location of Goods / G.O. No. | Text. | none |
| 22 | Consignee No. | EIN `NN-NNNNNNN`, EIN with suffix `NN-NNNNNNNXX`, SSN `NNN-NN-NNNN`, or CBP-assigned `YYDDPP-NNNNN`; `SAME` allowed. | none |
| 23 | Importer No. | IRS EIN, SSN or CBP-assigned number of the IOR (same formats as Block 22). | **IOR match** (CAPE "Account Mismatch" check); ACH enrollment lookup. |
| 24 | Reference No. | Number of the party to receive refunds, bills or notices, "only when a CBP Form 4811 is on file." | **4811 notify party**: decides the refund payee. |
| 25 | Ultimate Consignee Name and Address | Text. For warehouse withdrawals, the original warehouse entry number appears here. | Links a withdrawal to its warehouse entry (R5). |
| 26 | Importer of Record Name and Address | Text. | Display / IOR. |
| 27 | Line No. (and SPI, per-line country of origin) | `001`… The SPI sits below the line number. | Line key. |
| 28 | Description of Merchandise | Text. | Display. |
| 29A | HTSUS No. | 10-digit numbers. A line may list **several**: Chapter 99 number(s) plus the Chapter 1-97 number. | **Identifies IEEPA lines (9903.01.xx / 9903.02.xx).** |
| 29B | AD/CVD Case No. | `A-000-000-000` / `C-000-000-000`. | AD/CVD flag (R9/R10). |
| 29D | Other fees | e.g., MPF, HMF on the line. | Not refundable. |
| 30A / 30B | Gross Weight / Manifest Qty | Kilograms / quantity. | none |
| 31 | Net Quantity in HTSUS Units | Number + unit. | none |
| 32A | Entered Value | Whole US dollars. Must be reported on the Chapter 1-97 line, not the Chapter 99 line. | Recalculation; the old "VALUE NOT ALLOWED" check. |
| 32B / 32C | Charges / Relationship | `C` + amount / `Y` or `N`. | none |
| 33A | HTSUS Rate | e.g., `2.8%`, `Free`, `+25%`. | Display. |
| 33B / 33C / 33D | AD/CVD Rate / IRC Rate / Visa No. | n/a | none |
| 34 | Duty and I.R. Tax | Dollar amount opposite each rate, **including the duty on Chapter 99 lines**. | **IEEPA principal = sum of column 34 amounts on dutiable IEEPA Chapter 99 lines.** |
| Block 39 summary | Fee class codes | `012` AD, `013` CVD, `499` MPF, `501` HMF, `311` informal MPF, `496` dutiable mail fee, and others. | Excluded from the IEEPA refund. |
| 35 | Total Entered Value | n/a | Validation. |
| 37 / 38 / 39 / 40 | Duty / Tax / Other / Total | Totals. Block 37 excludes AD/CVD; Block 40 = 37 + 38 + 39. | Sanity checks. |
| CBP use only | A. LIQ CODE; B-E. Ascertained Duty, Tax, Other, Total | Filled in by CBP. **The liquidation date is not a filer block on the 7501**; get it from ACE. | n/a |
| 41 | Declarant Name, Title, Signature, Date | n/a | none |
| 42 / 43 | Broker/Filer Information / Broker/Importer File No. | n/a | Identifies the filing broker (who may file CAPE). |

**Entry type codes (Block 2)** [P]:

| Group | Codes |
|---|---|
| Consumption | 01 free and dutiable; 02 quota/visa; 03 AD/CVD; 04 appraisement; 05 vessel repair; 06 FTZ consumption; 07 quota/visa plus AD/CVD; 08 duty deferral |
| Informal | 11 free and dutiable; 12 quota other than textiles |
| Warehouse | 21 warehouse; 22 re-warehouse; 23 TIB; 24 trade fair; 25 permanent exhibition; 26 FTZ admission |
| Warehouse withdrawal | 31 for consumption; 32 quota/visa; 34 AD/CVD; 38 quota/visa plus AD/CVD |
| Government | 51, 52 |
| Transportation | 61, 62, 63 |
| Other | 09 reconciliation and 47 drawback are ACE types referenced by CBP's CAPE guidance |

**How to identify IEEPA duty lines on an entry** [P]/[S]:

- On a 7501 line, the Chapter 99 number appears in **column 29A together with** the Chapter 1-97 number. The IEEPA additional duty is the column 34 amount opposite the Chapter 99 rate.
- Count only **dutiable** IEEPA headings, meaning those with "+X%" or an all-in rate in §(e). Exception headings carry only the base duty and are not refundable on their own.
- CAPE requires "at least one dutiable IEEPA HTS Chapter 99 code" [P] (TIN).
- In ACE, ES-003 (Entry Summary Line Tariff Details) "by including the IEEPA tariff indicator… displays all entry lines with assessed duties" [P] (TIN, July 10).
- CBP's internal list of which Chapter 99 codes CAPE treats as "IEEPA" was **not published** in any source found [U]. The engine should use the list in §(e).

### b.2 ACE / status fields (not on the 7501; needed for routing)

| Field | Values / format | Source | Rules |
|---|---|---|---|
| `entry_summary_status` | Accepted / Cancelled / Rejected | ACE (CAPE requires Accepted) [P] | gate |
| `control_status` | CBP / other agency ("Trade Control") | ACE (must be CBP) [P] | gate |
| `liquidation_status` | Not Liquidated / Pending / Liquidated / Extended / Suspended / Under Review / Open / Closed (TIB) | ACE [P] | R9-R12 |
| `liquidation_date`, `reliquidation_date` | date | ACE (ES-003 / ES-022); Thompson Coburn says ES-022 column I [S] | 80/90/180-day clocks |
| `suspension_record` | bool | ACE [P] QRG | R9/R10/R11 |
| `protest_status`, `protest_afr_checked`, `protest_filed_solely_ieepa` | none / open / suspended / denied / approved; bool; bool | ACE / user | R8, R8b |
| `drawback_designated` | bool | ACE | R6 |
| `recon_flag`, `recon_09_filed`, `recon_due_date` | bool; bool; date | ACE / user | R7, R7b |
| `court_injunction_flag` | bool | ACE (QRG error) | gate |
| `statement_payment_pending` | bool | ACE (QRG "STATEMENT PROCESSING NOT COMPLETE") | retry later |
| `surety_paid_ieepa` | bool | user / surety | R2 |
| `deposit_date(s)` | date(s) on which IEEPA duty was actually paid (statement payment date for PMS) | ACE / ACH statement | interest start **[U]** see §d |
| `form4811_notify_party_name`, `_number` | text | ACE ES reports: "CF 4811 Notify Party Name" and "CF 4811 Notify Party Number" [P] | payee |
| `ach_refund_enrolled_ior`, `ach_refund_enrolled_4811` | bool | user (ACE ACH Refund Authorization tab) | blocker |
| `cit_plaintiff`, `cit_case_no`, `ior_submitted_to_cbp_date` | bool; text; date | user / counsel | R15, R15b |
| `class_member_candidate` | bool: IOR paid IEEPA duties Feb 1, 2025 to Feb 19, 2026, has not sued, and the duties are not under the Brazil/India orders [S] | derived | R14 note |
| `prior_cape_claim_no`, `cape_claim_status`, `cape_entry_result` | text; Accepted / Accepted with Error(s) / Rejected; error message | ACE CAPE tab [P] | R18, error handling |
| `refund_status` | Sent to Treasury / Treasury Issued / Funds Diverted / Check/ACH Returned | REV-603 [P] | tracking |
| `refund_principal`, `refund_interest` | dollars | ES-022 / REV-615 [P] | reconciliation |

### b.3 Derived fields

| Field | Definition |
|---|---|
| `ieepa_lines[]` | Lines with a dutiable IEEPA heading and duty > 0. |
| `ieepa_programs[]` | Programs from §(e): Canada, Mexico, China fentanyl; reciprocal baseline; reciprocal country-specific; Brazil; India; transshipment. |
| `ieepa_principal` | Sum of the IEEPA column 34 amounts. This is an **estimate**. CBP's actual refund is "the difference between the duties, taxes, and fees paid … and the recalculated duties, taxes, and fees owed" [P] (CSMS #68340863). It can be lower because of offsets, bills, all-in rates on 15% "deal" headings, or Chapter 98 issues [P]/[S]. |
| `days_since_liquidation` | `T − L` |
| `past_80`, `past_1501_window`, `past_protest_window` | Booleans from `days_since_liquidation`. |
| `pathway` | R0-R20 result. |
| `next_deadline`, `deadline_type` | e.g., `CAPE_80`, `PROTEST_180`, `CIT_2636a_180`, `CIT_2636i_2yr`, `RECON_30DAY_PRIORITY`. |
| `est_interest` | See §(d). |
| `blockers[]` | See §(f). |

---

## (c) CAPE mechanics and file template (Question 3)

### c.1 What CAPE is and who can file

- **CAPE** stands for **Consolidated Administration and Processing of Entries**. It is an ACE Portal functionality with four components: Claim Portal, Mass Processing, Review and Liquidation/Reliquidation, and Refund [P] (Lord Decl. Mar 12).
- **Who may file:** "the importer of record (IOR) for the entries listed or the customs broker that filed the entries on behalf of the IOR" [P] (TIN).
  - CBP says CAPE "does not require the assistance of a broker" [P] (Thomas ¶15).
  - Sureties have no filing path; surety-paid entries must not be submitted [P].
- **Where:** the **CAPE tab** in the ACE Portal, in Importer, Filer and Organizational Broker accounts [P].
  - A Filer account whose Filer Type is *not* "Importer" sees the message "This functionality is not available for non-importer filer" [P] (QRG).
  - **ABI/EDI cannot be used** [P] (TIN).
- **Account requirements:**
  - An active ACE Portal account [P].
  - An Importer sub-account for ACH refund enrollment and for ACE Reports [P].
  - New accounts must wait 24 hours before running reports [P] (TIN July 10).

### c.2 Template, verbatim from the CBP QRG (Pub. 5612-0626, June 2026) [P]

| Item | Rule |
|---|---|
| Template file name | `ACEP_CapeEntryNumberUploadTemplate`, downloaded from the **CAPE Upload Template** link in the CAPE Upload dialog. |
| Columns | **One column.** Header text in row 1: **`Entry Number`**. Do not delete the header. |
| Data rows | Entry numbers go in **column 1, starting at row 2**, one per row. "Only the entry numbers should be included in the CSV file – no other entry-related information is needed" [P] (CSMS #68340863). |
| File type | Must be saved as **CSV (Comma delimited) (*.csv)**. |
| Entry number format | **11 alphanumeric characters.** "Dash is optional (any special characters will be stripped prior to 11-character validation)." The error text reads "Entry Number must be 11 characters without dashes." |
| Filer code check | For Filer (Filer Type Importer) and Organizational Broker accounts, the **first 3 characters must match the account's Filer Code.** |
| Duplicates | Not allowed within the file, or with any prior declaration. |
| Row limit | **Conflict.** CSMS and TIN say **9,999** entries per declaration. The QRG says the file is limited to **10,000** entries and **1 MB**. **Engine rule: at most 9,999 rows and under 1 MB.** [P] [U] on the exact figure. |
| Certification | The **Acknowledge** checkbox ("legally authorized to make the filing") must be ticked before the Upload File button is enabled. |

Example file. The entry number is CBP's own worked example from the 7501 instructions; the dash is optional and is stripped by ACE:

```csv
Entry Number
B7603245278
```

### c.3 Validation sequence and error definitions [P] (QRG; CSMS #68340863, #69056483)

**Stage 1: file-format checks.** These show a specific Reason in the upload dialog.

| Message | Meaning |
|---|---|
| CSV content is empty or missing the header | Needs the `Entry Number` header and at least one entry. |
| Not a CSV file | Wrong file type. |
| The file size exceeds 1mb… | Split the file. |
| The file is deemed unsafe… | Re-save and upload again. |
| The file exceeds the maximum 10,000 allowed entry numbers per file | Split the file. |

**Stage 2: "Failed initial validation."** These are entry-number format checks.

| Message | Meaning |
|---|---|
| Not 11 characters long | Wrong length. |
| Duplicate Entry | Same entry twice in the file. |
| Filer Code not matching | First 3 characters do not match the account's filer code. |

**Stage 3: "Rejected by batch validation."**

| Message | Meaning |
|---|---|
| Account Mismatch | The IOR number of the account must match the IOR number on the entry summary. |
| Entry Summary Not Found or Archived in ACE | Entry not found. |

If stages 1 to 3 pass, the File Upload Status shows **Accepted** and a **claim number** is assigned. The claim then shows **Rejected** (all entries failed), **Accepted with Error(s)**, or **Accepted** (all passed).

**Stage 4: entry validation errors.** A failing entry is removed; the rest of the declaration continues.

| Error | Definition |
|---|---|
| ENTRY ON DRAWBACK | Entry cannot be on a drawback entry. |
| ENTRY SUMMARY IS CANCELLED/REJECTED | Entry summary status must be "Accepted." |
| ENTRY SUMMARY IS IN FINAL LIQUIDATION STATUS | Liquidated or reliquidated **more than 80 days ago**. |
| ENTRY SUMMARY IS IN TRADE CONTROL | Control status must be CBP. |
| ENTRY SUMMARY IS SUBJECT TO COURT INJUNCTION | Entry flagged for injunction. |
| ENTRY SUMMARY NOT FOUND OR ARCHIVED IN ACE | Entry must exist. |
| ENTRY SUMMARY PENDING LIQUIDATION OR NOT LIQUIDATED AND HAS SUSPENSION RECORD | Liquidation status "Pending" or "Not Liquidated" with a suspension record. |
| ENTRY SUMMARY UNDER REVIEW | "Entry cannot be in adjusted status." |
| ENTRY TYPE NOT ALLOWED | Types 23, 08, 09 and 47; also 21 and 22 since July 7, 2026. |
| VALUE NOT ALLOWED ON HTS | Goods value above $0.00 on a Chapter 99 code. **[U] Removed** by CSMS #69056483 (June 25, 2026), although it is still listed in the June QRG. |
| NO IEEPA HTS ON ENTRY | No dutiable IEEPA heading on the entry. |
| PROTEST ON ENTRY | Open or suspended protest, or Denied status with the AFR box checked. |
| STATEMENT PROCESSING NOT COMPLETE | On a statement authorized for payment but not yet processed. Retry later. |
| HTS RELATIONSHIP MISMATCH | An add/replace/derived Chapter 99 code is missing its corresponding HTS. **Fix with a PSC**, then refile. |
| INVALID HTS | The line action date is outside an HTS code's begin and end dates. **Fix with a PSC**, then refile. |
| SPI OR ADDITIONAL HTS REQUIRED | An SPI or an additional HTS is required on at least one line. |
| UNABLE TO CALCULATE DUTY-'X' DUTY COMP CODE | ACE cannot calculate a duty computation code. |
| RECON ALREADY FILED FOR ENTRY SUMMARY | A reconciliation entry is on file. |
| UNEXPECTED ERROR-TRY AGAIN | Re-upload. |

**Primary failure reasons reported by CBP:**

- File-validation failures, in order: (1) IOR or filer mismatch; (2) entry number errors such as wrong length or entry not existing; (3) CSV not matching the template [P] (Lord Decls. Aug-Oct).
- Entry-level failures: "the entry date is past CBP's 90 day re-liquidation authority, the entry does not contain a Chapter 99 HTS number used to assess IEEPA duties, or the entry was already filed on a prior CAPE declaration" [P].

**Re-submission rule:** for file errors, fix and upload the **whole** file again. For claim (entry) errors, upload **only the corrected entries** on a new declaration [P] (QRG).

**Result files:**
- `Cape_Validation_Result.csv` (upload job), and the Claim Details file (claim number link) [P].
- **Their column layouts are not documented** in any source found [U].

### c.4 Entry-number check digit (from the CBP 7501 Instructions, Appendix 1) [P]

1. Take the first 10 characters (3-character filer code plus 7-digit number).
2. Convert letters to numbers: A=1 … I=9, J=10 … Z=26. A two-digit letter value is reduced to the sum of its digits; for example, R=18 counts as 9 in CBP's chart.
3. Double every even-position digit. If a product is greater than 9, use (product − 9).
4. Add the odd-position digits.
5. Check digit = (10 − (total mod 10)) mod 10.

Worked example: `B76-0324527` gives check digit **8**. This was verified by script against CBP's example.

Whether CAPE *validates* the check digit is not stated; CAPE only states the 11-character format check [U]. Some filers are authorized a "check digit factor" (+1 or +2), so **warn, don't reject**, on a mismatch.

### c.5 Processing, acknowledgment and payment [P] (CSMS #68340863; TIN; Lord Decls.)

1. **Upload.** The claim number is the acknowledgment. Practitioners report acceptance in about 10 days [S] (Holland & Knight).
2. **Mass processing.** All IEEPA Chapter 99 numbers are removed at line level, creating a new **minor version** of the entry summary. Duties are recalculated "as if IEEPA duties were never owed," and interest is calculated under 19 CFR 24.36.
3. **Review and liquidation.**
   - Unliquidated entries are set to liquidate **45 days** after acceptance. Extended, suspended and under-review entries keep their status.
   - Warehouse entries liquidate in the normal course.
   - Already-liquidated entries are **reliquidated the next business day**.
   - CBP runs liquidations Monday through Thursday.
   - CAPE triggers ordinary review of classification, value, origin and tariff stacking, so **bills can result** [S] (Thompson Coburn). Phase 3 is designed to make no non-IEEPA adjustments [P] (Lord Decl. Aug 25).
4. **Refund.**
   - Refunds are consolidated by **IOR or 4811 designee and liquidation date** into one lump sum, after checking for **unpaid CBP debts**.
   - One refund may combine entries from several declarations.
   - Generally paid **60-90 days** after acceptance (45 days of review plus Treasury processing), unless a compliance review intervenes.
   - Practitioners see deposits 3-5 weeks after the refund date [S].
5. **Tracking reports.**

| Report | Use |
|---|---|
| ES-003 | Identifies IEEPA lines. |
| ES-022 (CAPE Entry Summary Report) | Links declaration to entry to refund number; principal and interest shown separately. |
| REV-603 (Trade Refund) | Statuses: Sent to Treasury, Treasury Issued, Funds Diverted, Check/ACH Returned. |
| REV-613 (ACH Rejected Refunds) | Refunds rejected for missing ACH enrollment. |
| REV-615 (CAPE Details Refunds) | Requires the "Consolidated Refund ID" from REV-603. |

6. **Contacts.**

| Purpose | Contact |
|---|---|
| Technical questions on IEEPA refunds | IEEPARefunds@cbp.dhs.gov |
| General questions | traderelations@cbp.dhs.gov |
| ACE technical issues | ACE Account Service Desk, 866-530-4172, ace.support@cbp.dhs.gov |
| Refund amount disputes | CBP Centers of Excellence and Expertise [P] (Order Oct 8) |

---

## (d) Interest: rates and formula (Question 5)

### d.1 Legal basis [P]

- **19 U.S.C. 1505(c):** "Interest on excess moneys deposited shall accrue, at a rate determined by the Secretary, **from the date the importer of record deposits estimated duties**, fees, and interest … **to the date of liquidation or reliquidation** of the applicable entry or reconciliation."
- **19 U.S.C. 1505(b):** refunds plus interest "shall be paid within 30 days of liquidation or reliquidation."
- **19 U.S.C. 1505(d):** if a refund is not paid within that 30-day period, delinquency interest accrues by 30-day periods. **However,** no 1505(d) interest accrues when delivery fails solely because the recipient never provided ACH banking information [P] (Electronic Refunds IFR).
- **19 CFR 24.36(a)(1):** interest accrues "from the date the duties … were deposited … to the date of liquidation or reliquidation." CSMS #68340863 confirms CAPE interest follows 19 CFR 24.36.
- **Rate:** set under Treasury Decision 85-93. It "must be in accordance with the Internal Revenue Code rate established under **26 U.S.C. 6621 and 6622**," with separate corporate and non-corporate overpayment rates (CBP FR notice 2026-19292). See also 19 CFR 24.3a(c)(1).
- **Compounding:** 26 U.S.C. 6622(a): interest "shall be **compounded daily**." CBP's notices cite § 6622, but CBP has **not published its ACE computation method or day-count convention** [U].
  - Engine default: daily compounding, rate ÷ 365 (or 366 in leap years) for each day, applying each quarter's rate.
  - Validate against the ES-022 / REV-615 principal-vs-interest split.
- **Large-corporate rule [U]:** the IRS applies 4.5% to the portion of a corporate overpayment above $10,000 (Q4 2026). CBP's table shows only a single "corporate overpayments" column, and no source says whether CBP applies the $10K tier.

### d.2 CBP overpayment (refund) interest rates, 2025 Q1 to 2026 Q4

Source: CBP FR Doc. 2026-19292, 91 FR 60141 (Sept 22, 2026) historical table, confirmed by notices 2026-01175, 2026-09871 and 2026-13298 [P].

| Quarter | Dates | Non-corporate overpayment | Corporate overpayment | Underpayment |
|---|---|---|---|---|
| 2025 Q1 | Jan 1 - Mar 31, 2025 | 7% | 6% | 7% |
| 2025 Q2 | Apr 1 - Jun 30, 2025 | 7% | 6% | 7% |
| 2025 Q3 | Jul 1 - Sep 30, 2025 | 7% | 6% | 7% |
| 2025 Q4 | Oct 1 - Dec 31, 2025 | 7% | 6% | 7% |
| 2026 Q1 | Jan 1 - Mar 31, 2026 | 7% | 6% | 7% |
| 2026 Q2 | Apr 1 - Jun 30, 2026 | **6%** | **5%** | 6% |
| 2026 Q3 | Jul 1 - Sep 30, 2026 | 7% | 6% | 7% |
| 2026 Q4 | Oct 1 - Dec 31, 2026 | 7% | 6% | 7% |

Q4 2026 cross-check against the IRS (IR-2026-98, Aug 21, 2026): individual overpayment 7%, corporate 6%, corporate above $10K 4.5%, underpayment 7%, large-corporate underpayment 9% [P].

### d.3 Formula for the estimate

```
start = deposit_date        # date the IEEPA duty was actually deposited
                            # (for periodic monthly statements, the statement payment date) [U]
end   = liquidation_or_reliquidation_date   # NOT the payment date
rate(d) = quarterly overpayment rate for day d (corporate or non-corporate)
Y(d)  = 366 if year(d) is a leap year, else 365      # [U] convention

interest = P * ( PRODUCT over d in [start, end) of (1 + rate(d) / Y(d)) ) - P
```

- **Worked example:** $10,000 deposited 2025-06-16, reliquidated by CAPE 2026-05-04, non-corporate rate. Daily compounding gives **$627.33**; simple interest gives $608.49; the corporate rate with daily compounding gives $534.00.
- **Multiple deposits:** when an entry has several deposit dates (for example, an additional deposit after a PSC), compute interest separately per deposit (24.36(a)(1)(i)). CBP listed "complex interest calculations related to multiple collection dates" as a later-phase capability [P] (Lord Decl. Mar 30 ¶16e).

---

## (e) IEEPA Chapter 99 headings and the program each belongs to (Question 1)

**Source:** USITC HTS REST API, 2026 HTS **Revision 21** (released Oct 9, 2026), headings 9903.01.01-9903.02.91 and 9903.96, read directly [P]. Program-to-Executive-Order mapping comes from White & Case (Mar 2, 2026) [S] and BDO [S], and is consistent with CSMS #67834313's EO list [P].

**Read the table this way:**
- **Dutiable** means the heading text adds duty ("+X%") or sets an all-in rate. These lines can carry refundable IEEPA duty.
- **Exception** means the heading text is "The duty provided in the applicable subheading" or "No change." Such a line marks an exemption and carries no IEEPA duty.
- **Rates shown are the current HTS text.** Several rates changed during 2025-26; for example, the China fentanyl rate is noted as cut to 10% effective Nov 10, 2025 [S]. **The engine must use the duty actually paid (column 34), not the heading's rate.**

### e.1 Fentanyl / "trafficking" tariffs

**Mexico, EO 14194**

| Heading | Type | Rate (current text) | Description |
|---|---|---|---|
| 9903.01.01 | Dutiable | +25% | Products of Mexico. |
| 9903.01.02 | Exception | base | Donations. |
| 9903.01.03 | Exception | base | Informational materials. |
| 9903.01.04 | Exception | No change | USMCA-qualifying (General Note 11). |
| 9903.01.05 | Dutiable | +10% | Potash of Mexico. |

**Canada, EO 14193**

| Heading | Type | Rate (current text) | Description |
|---|---|---|---|
| 9903.01.10 | Dutiable | +35% | Products of Canada. |
| 9903.01.11 | Exception | base | Donations. |
| 9903.01.12 | Exception | base | Informational materials. |
| 9903.01.13 | Dutiable | +10% | Energy and critical minerals. |
| 9903.01.14 | Exception | No change | USMCA-qualifying. |
| 9903.01.15 | Dutiable | +10% | Potash. |
| 9903.01.16 | Dutiable | +40% | Canadian goods CBP determined were transshipped. |

**China and Hong Kong, EO 14195**

| Heading | Type | Rate (current text) | Description |
|---|---|---|---|
| 9903.01.20 | Dutiable | +10% | U.S. note 2(s). |
| 9903.01.21 | Exception | base | Donations. |
| 9903.01.22 | Exception | base | Informational materials. |
| 9903.01.23 | Exception | base | In transit before Feb 1, 2025. |
| 9903.01.24 | Dutiable | +10% | U.S. note 2(u). Applies on top of Section 301 duties [P] (CBP IEEPA FAQ). |

### e.2 Reciprocal tariffs, EO 14257 (as amended)

**Baseline (in effect from Apr 5, 2025) and its exceptions**

| Heading | Type | Description |
|---|---|---|
| 9903.01.25 | **Dutiable, +10%** | Baseline for any country, except products under the headings listed below and 9903.02.02-9903.02.91. Also used for China from May 14, 2025 [P] (CBP FAQ). |
| 9903.01.26 | Exception | Canada. |
| 9903.01.27 | Exception | Mexico. |
| 9903.01.28 | Exception | Loaded on a vessel before Apr 5, 2025 (vessel only). |
| 9903.01.29 | Exception | General Note 3(b) countries. |
| 9903.01.30 | Exception | Donations. |
| 9903.01.31 | Exception | Informational materials. |
| 9903.01.32 | Exception | Annex II products. |
| 9903.01.33 | Exception | Section 232 products (steel, aluminum, autos and parts, copper, wood, semiconductors, etc.). |
| 9903.01.34 | Exception | U.S. content when it is at least 20% of customs value. Reported as a separate line [P] (CBP FAQ). |

**Country-specific rates of April 9, 2025: 9903.01.43-9903.01.76 (dutiable).** HTS compiler's notes say "provision terminated" (90 FR 37963); 9903.01.63 is "suspended" (90 FR 50729).

| Heading | Rate | Country |
|---|---|---|
| .43 | +11% | Cameroon or DR Congo |
| .44 | +13% | Chad or Equatorial Guinea |
| .45 | +14% | Nigeria |
| .46 | +15% | Norway or Venezuela |
| .47 | +16% | Mozambique |
| .48 | +17% | Israel |
| .49 | +18% | Nicaragua or Zimbabwe |
| .50 | +20% | EU or Jordan |
| .51 | +21% | Côte d'Ivoire or Namibia |
| .52 | +22% | Vanuatu |
| .53 | +24% | Brunei |
| .54 | +25% | South Korea |
| .55 | +26% | India |
| .56 | +27% | Kazakhstan |
| .57 | +28% | Tunisia |
| .58 | +29% | Pakistan |
| .59 | +30% | Algeria |
| .60 | +31% | Libya |
| .61 | +32% | Angola |
| .62 | +33% | North Macedonia |
| .63 | +34% | China incl. Hong Kong and Macau. CBP FAQ: also used for **+84%** on Apr 9, 2025 and **+125%** from Apr 10 to May 13, 2025 [P]. |
| .64 | +35% | Bosnia and Herzegovina |
| .65 | +36% | Thailand |
| .66 | +37% | Bangladesh |
| .67 | +38% | Guyana |
| .68 | +39% | Iraq |
| .69 | +40% | Mauritius |
| .70 | +41% | Falkland Islands or Syria |
| .71 | +44% | Myanmar or Sri Lanka |
| .72 | +46% | Vietnam |
| .73 | +47% | Madagascar |
| .74 | +48% | Laos |
| .75 | +49% | Cambodia |
| .76 | +50% | Lesotho |

**Country-specific rates of August 7, 2025: 9903.02.02-9903.02.71 (dutiable).** Rates are as printed in Rev. 21.

| Heading | Rate | Country |
|---|---|---|
| .02 | +15% | Afghanistan |
| .03 | +30% | Algeria |
| .04 | +15% | Angola |
| .05 | +20% | Bangladesh |
| .06 | +15% | Bolivia |
| .07 | +30% | Bosnia and Herzegovina |
| .08 | +15% | Botswana |
| .09 | +10% | Brazil |
| .10 | +25% | Brunei |
| .11 | +19% | Cambodia |
| .12 | +15% | Cameroon |
| .13 | +15% | Chad |
| .14 | +15% | Costa Rica |
| .15 | +15% | Côte d'Ivoire |
| .16 | +15% | DR Congo |
| .17 | +15% | Ecuador |
| .18 | +15% | Equatorial Guinea |
| .19 | base | EU, goods whose column-1 rate is ≥15% |
| .20 | **15% all-in** | EU, goods whose column-1 rate is <15% |
| .21 | +10% | Falkland Islands |
| .22 | +15% | Fiji |
| .23 | +15% | Ghana |
| .24 | +15% | Guyana |
| .25 | +15% | Iceland |
| .26 | +25% | India |
| .27 | +19% | Indonesia |
| .28 | +35% | Iraq |
| .29 | +15% | Israel |
| .30 | +15% | Japan (terminated, 90 FR 44638) |
| .31 | +15% | Jordan |
| .32 | +25% | Kazakhstan |
| .33 | +40% | Laos |
| .34 | +15% | Lesotho |
| .35 | +30% | Libya |
| .36 | +15% | Liechtenstein (terminated, 90 FR 59281) |
| .37 | +15% | Madagascar |
| .38 | +15% | Malawi |
| .39 | +19% | Malaysia |
| .40 | +15% | Mauritius |
| .41 | +25% | Moldova |
| .42 | +15% | Mozambique |
| .43 | +40% | Myanmar |
| .44 | +15% | Namibia |
| .45 | +15% | Nauru |
| .46 | +15% | New Zealand |
| .47 | +18% | Nicaragua |
| .48 | +15% | Nigeria |
| .49 | +15% | North Macedonia |
| .50 | +15% | Norway |
| .51 | +19% | Pakistan |
| .52 | +15% | Papua New Guinea |
| .53 | +19% | Philippines |
| .54 | +35% | Serbia |
| .55 | +30% | South Africa |
| .56 | +15% | South Korea (terminated Nov 14, 2025, 90 FR 55964) |
| .57 | +20% | Sri Lanka |
| .58 | +39% | Switzerland (terminated, 90 FR 59281) |
| .59 | +41% | Syria |
| .60 | +20% | Taiwan |
| .61 | +19% | Thailand |
| .62 | +15% | Trinidad and Tobago |
| .63 | +25% | Tunisia |
| .64 | +15% | Turkey |
| .65 | +15% | Uganda |
| .66 | +10% | United Kingdom |
| .67 | +15% | Vanuatu |
| .68 | +15% | Venezuela |
| .69 | +20% | Vietnam |
| .70 | +15% | Zambia |
| .71 | +15% | Zimbabwe |

**Trade-framework headings**

| Heading | Type | Description |
|---|---|---|
| 9903.02.72 | Exception (base) | Japan, goods whose column-1 rate is ≥15%. |
| 9903.02.73 | **15% all-in** | Japan, goods whose column-1 rate is <15%. |
| 9903.02.74-.77 | Exception | EU exemptions, including civil aircraft and non-patented pharmaceuticals. |
| 9903.02.78 | Exception | Any country, U.S. note 2(v)(iii)(b). |
| 9903.02.79 | Exception (base) | South Korea, column-1 rate ≥15%. |
| 9903.02.80 | **15% all-in** | South Korea, column-1 rate <15%. |
| 9903.02.81 | Exception | South Korea civil aircraft. |
| 9903.02.82 | Exception (base) | Switzerland, column-1 rate ≥15%. |
| 9903.02.83 | **15% all-in** | Switzerland, column-1 rate <15%. |
| 9903.02.84-.86 | Exception | Switzerland exemptions. |
| 9903.02.87 | Exception (base) | Liechtenstein, column-1 rate ≥15%. |
| 9903.02.88 | **15% all-in** | Liechtenstein, column-1 rate <15%. |
| 9903.02.89-.91 | Exception | Liechtenstein exemptions. |
| 9903.96.01 / 9903.96.02 | Exception | UK and Japan civil aircraft. |

**Caution on "15% all-in" lines:** only the portion above the general duty is IEEPA. CAPE recalculates; a naive "refund = duty on the Chapter 99 line" calculation overstates the refund [S] (Great Lakes Customs Law). The engine should compute `refund ≈ (duty on Chapter 99 line + duty on the Chapter 1-97 line) − (general duty recalculated without the Chapter 99 line)` [U].

### e.3 Other IEEPA programs

| Heading | Program | Type | Description |
|---|---|---|---|
| 9903.02.01 | Transshipment, EO 14326 | **Dutiable, +40%** | Goods CBP determined were transshipped to evade duties. |
| 9903.01.77 | Brazil, EO 14323 (signed July 30, 2025; effective Aug 6, 2025) | **Dutiable, +40%** | Products of Brazil. |
| 9903.01.78-.83, 9903.01.90 | Brazil | Exceptions | In transit, donations, informational materials, Annex products, civil aircraft, Section 232 products. |
| 9903.01.84 | India "Russian oil," EO 14329 (entries after Aug 27, 2025) | **Dutiable, +25%** | Products of India. |
| 9903.01.85-.89 | India | Exceptions | n/a |

The India provisions are marked "**terminated as of February 7, 2026**" [P].

Venezuela-oil (EO 14245), Cuba (EO 14380) and Iran (EO 14382) "secondary tariff" orders existed, but White & Case reports that no such secondary tariffs were in effect at the time of the Supreme Court decision. No Chapter 99 lines for them were identified [S].

### e.4 NOT IEEPA: not refundable through CAPE

| Duty | Headings / codes | Tag |
|---|---|---|
| Section 232 | 9903.80-9903.85 and others | [S] |
| Section 301 (China) | 9903.88.xx | [S]; CSMS #67834313 says 232 and 301 are unaffected [P] |
| Section 201 | n/a | n/a |
| Section 122 | 9903.03.01-9903.03.11 (10% surcharge, entries Feb 24 to July 23, 2026) | [P] HTS |
| AD/CVD | Collection codes 012 / 013 | [P] |
| MPF | 499 (311 for informal entries) | [P] |
| HMF | 501 | [P] |
| Other user fees | n/a | n/a |
| Column 1 general duty | n/a | n/a |

Note on 9903.03.12-9903.03.16: these headings (+50% under U.S. note 51) are present in Rev. 21. The program behind them was **not identified**; they are not IEEPA as far as found [U].

---

## (f) Payment-blocker checklist (Question 4)

| # | Blocker | Detection | Effect | Fix | Tag |
|---|---|---|---|---|---|
| B1 | **No ACH refund enrollment** for the IOR, or for the 4811 designee. Electronic-only refunds since **Feb 6, 2026** under the Electronic Refunds IFR (FR Doc. 2025-24171, published Jan 2, 2026; docket USCBP-2025-1076; EO 14247). | REV-613; REV-603 status "Check/ACH Returned"; the user's ACE ACH Refund Authorization tab. | A certified refund is **rejected / not transmitted**. **No 1505(d) interest** accrues for the delay. CBP holds: 1,880 consolidated refunds (May 11); 4,185 (May 22); 9,837 (July 10); 22,170 / $1.7B (Aug 21); 20,184 / $1.3B (Sept 11); **20,362 / $1.1B (Oct 2)**. | ACE Portal, Importer sub-account, **ACH Refund Authorization** tab: submit U.S. bank details, which are **separate from ACH payment details**. Then email **frn-achrefundsupport@cbp.dhs.gov** to request reissue. A broker with a valid POA can help with ACE access (Order Sept 17). Replacement requests come from the top-level ACE account owner and take about 6-8 weeks [S]. | [P] IFR; TIN; Lord Decls.; Orders; [S] Krieger |
| B2 | No U.S. bank account. | user | Cannot enroll. | Open a U.S. account, designate a 4811 third party with one, or seek a 31 CFR 208.4 waiver (rare). | [P] IFR fn. 11 |
| B3 | **CBP Form 4811 notify party** on file and listed on the entry (Block 24). | ES reports: "CF 4811 Notify Party Name/Number". | The refund goes to the **designee, not the IOR**. If the designee is not ACH-enrolled, the refund **defaults to the IOR's ACH account**. A 4811 lapses if the importer number is not used for 3 years. | Review or revoke the 4811 (via the Center or the ACE Notify Parties tab). | [P] TIN; IFR; 19 CFR 24.36(a); [S] Thompson Coburn |
| B4 | **Debt offset.** | REV-603 "Funds Diverted" | The refund is reduced by unpaid CBP bills (19 CFR 24.72 set-off). Offsets under the Treasury Offset Program (31 U.S.C. 3716) are reported [S]. | Pay or dispute the bills. | [P] CSMS; TIN; [S] Troutman |
| B5 | **New bills from CAPE reliquidation.** CAPE re-review can find 232, 301 or 201 underpayments, or deny Chapter 98 (9817) treatment. | A CBP bill after CAPE. | The net refund is lower, or a balance is owed. | Protest within 180 days of (re)liquidation; pay to stop interest. | [S] Thompson Coburn |
| B6 | Surety-paid duties. | user / surety | Do not file. CBP is withholding refunds on surety-identified entries; 660 claims were filed by others on such entries. | Wait for a surety process (none scheduled). | [P] CSMS; ECF 56 |
| B7 | IOR / filer **account mismatch**: the top reason for file-validation failures. | CAPE "Account Mismatch" or "Filer Code not matching". | Declaration rejected. | File from the correct IOR account, or the broker that filed the entry. | [P] QRG; Lord Decls. |
| B8 | Slow ACE account creation or approval. | user | Can push entries past day 80. | Start ACE setup immediately; a broker with POA can help. | [S] Sept 9 letter; [P] Order Sept 17 |
| B9 | Entry status blockers: trade control, injunction, statement pending, protest, drawback, reconciliation 09 filed, entry types 08/09/23/47/21/22. | CAPE errors | Entry removed from the declaration. | See §(a). | [P] QRG |
| B10 | PSC conflict: a PSC is needed but CAPE is already accepted (error 864). | ACE | The PSC is blocked. | Do PSCs before CAPE. | [P] CSMS #68397097 |
| B11 | Compliance or fraud review. | Refund delayed beyond 90 days. | Delay. | Contact the Center. | [P] CSMS; Thomas ¶20 |
| B12 | Refund smaller than expected: consolidation across declarations, 15% all-in lines, offsets, bills. | ES-022 vs. estimate | n/a | Contact the CBP Center of Excellence and Expertise. | [P] Order Oct 8 |
| B13 | Entries spanning the 80-day boundary during processing. | `days` close to 80 | Rejected as "FINAL LIQUIDATION STATUS". | Submit early; alert from day 70. | [P] QRG; [U] buffer |

---

## (g) Open questions and uncertainties

1. **"7,700+ refunds failed for lack of ACH": NOT confirmed.** CBP's declared series is 1,880 (May 11), 4,185 (May 22), 9,837 (July 10), 22,170 (Aug 21), 20,184 (Sept 11) and 20,362 (Oct 2). A June value could be about 7,700, but the June 10 and July 1 declarations were not read.
2. **"333K+ importers"**: the primary source says "over 330,000."
3. **Row limit**: 9,999 (CSMS and TIN) versus 10,000 plus 1 MB (QRG). Use ≤9,999.
4. **Validation-result CSV and Claim Details file layouts** are undocumented.
5. **Does CAPE check the check digit?** Not stated.
6. **Interest computation**: daily compounding, day count, and whether CBP applies the corporate $10K tier are all unpublished. Validate against ES-022.
7. **Extended, suspended and under-review entries**: CSMS and TIN say they are accepted, but the QRG lists the errors "ENTRY SUMMARY UNDER REVIEW (adjusted status)" and "PENDING/NOT LIQUIDATED AND HAS SUSPENSION RECORD." The exact boundary between AD/CVD "Pending" and "Suspended" in ACE needs confirmation.
8. **"VALUE NOT ALLOWED ON HTS"** was removed by CSMS #69056483 (June 25) but still appears in the June 26 QRG.
9. **Informal (type 11) entries**:
   - Lord (Mar 12) says CAPE would process "the majority of formal and informal entries."
   - Jet Worldwide (Apr 23) says Phase 1 does not cover informal entries.
   - Because informal entries liquidate at payment (19 CFR 159.10), essentially all IEEPA informal entries are now past 180 days.
   - How ACE records informal-entry liquidation status (and therefore CAPE eligibility) is unconfirmed.
10. **Express courier (Part 128) entries**: who is the IOR versus the duty payer under DDP terms, and who receives the refund. Only secondary sources found.
11. **Postal shipments**: no ACE entries; CBP calls them "unique issues"; unresolved.
12. **FTZ (type 06)**: no FTZ-specific CAPE guidance found. A secondary blog reports rejections for "HTS mismatch" on type 06 entries (not read).
13. **Protests**:
    - It is unresolved whether IEEPA duties are protestable. Pre-Supreme Court CIT rulings said no, per Thompson Coburn.
    - CBP is building protest functionality with no date.
    - Denied-protest handling ("AFR box") needs clarification.
14. **Statute of limitations under 1581(i)**: the accrual date is debated. Counsel use Feb 1 or Feb 4, 2027 as the earliest deadline, and it is unclear whether the period runs per entry or per payment. Class-membership tolling is unresolved.
15. **Phase 3 for IOR numbers submitted after July 30**: CBP only says "additional instructions." Troutman reports a "rolling biweekly" process; unconfirmed.
16. **Federal Circuit appeal**: the oral argument date conflicts between sources, and the decision timing is unknown. Re-check after Oct 26-27, 2026 (CBP report and conference).
17. **Class certification appeal** (Rule 23(f)): expected but not confirmed.
18. **Section 122**: the Federal Circuit stay date (May 12 versus June 11) is unresolved. Program behind 9903.03.12-.16 is unknown.
19. **CBP's IEEPA Duty Refunds page and FAQs** (including any "updated FAQs" promised Sept 17) **were not accessible**. They may contain additional rules.
20. **PSC deadlines** (typically within 300 days of entry and before liquidation) were **not re-verified** in this research.
21. **Form 7501 box numbering** was read from the 06/09 revision. Check against CBP's current form.
22. **Government entry types (51/52), type 12 informal quota, and type 07** are not addressed.
23. **9903.01.28 / 9903.01.23 "not accepting"** is reported only by a secondary source (freightright). These are non-dutiable exception codes in any case.
24. **The Sept 9, 2026 congressional letter** was not retrieved; its content is known only via IANS and a secondary summary.
25. **Per-phase dollar split**: estimates such as Phase 3 at about $11.4B (6.9%) are secondary only.

---

## (h) Sources (URL, document date, date accessed Oct 25, 2026)

### Primary: CBP CSMS (govdelivery)

- CSMS #67834313, "Ending Collection of IEEPA Duties" (Feb 22, 2026): https://content.govdelivery.com/accounts/USDHSCBP/bulletins/40b11c9
- CSMS #68340863, "UPDATE – CAPE for IEEPA Refunds, April 20, 2026, Deployment" (Apr 13, 2026): https://content.govdelivery.com/accounts/USDHSCBP/bulletins/412cc7f
- CSMS #68397097, "Updated ACE Entry Summary Error Dictionary" (PSC error 864) (Apr 20, 2026): https://content.govdelivery.com/accounts/USDHSCBP/bulletins/413a829
- CSMS #69035485, "CAPE – Entries Flagged for Reconciliation" (June 23, 2026): https://content.govdelivery.com/accounts/USDHSCBP/bulletins/41d65dd
- CSMS #69056483, "Update to Entry-Level Validations for CAPE Declarations" (June 25, 2026): https://content.govdelivery.com/accounts/USDHSCBP/bulletins/41db7e3
- CSMS #69066837, "DEPLOYED – CAPE … Entries Flagged for Reconciliation" (June 29, 2026). Cited by Thompson Coburn; not read directly: https://content.govdelivery.com/bulletins/gd/USDHSCBP-41de055
- CSMS #69127837, "CAPE – Warehouse Entries" (July 2, 2026): https://content.govdelivery.com/accounts/USDHSCBP/bulletins/41ece9d

### Primary: CBP publications

- Trade Information Notice: CAPE Phase 1 (last updated Apr 8, 2026): https://www.cbp.gov/sites/default/files/2026-04/trade_information_notice_cape_508c.pdf
- Trade Information Notice: CAPE (last updated July 10, 2026; posted July 23, 2026): https://www.cbp.gov/sites/default/files/2026-07/26_0723_trade_information_notice_CAPE.pdf
- ACE Portal QRG, "CAPE Declarations and Error Definitions," Pub. No. 5612-0626 (June 2026): https://www.cbp.gov/sites/default/files/2026-06/ace_portal_cape_qrg_trade.pdf
- IEEPA Duty Refunds Fact Sheet, Pub. No. 5515-0426 (Apr 17, 2026): https://www.cbp.gov/sites/default/files/2026-04/ieepa_refunds_factsheet_0.pdf
- CBP IEEPA FAQ (trade-remedy FAQ on reporting; undated, accessed Oct 25, 2026): https://www.cbp.gov/trade/programs-administration/trade-remedies/IEEPA-FAQ
- CBP IEEPA Duty Refunds page (**not accessible**): https://www.cbp.gov/trade/programs-administration/trade-remedies/ieepa-duty-refunds
- CBP Form 7501 (06/09), form copy: https://stg-mva.maryland.gov/Documents/cbp_form_7501.pdf
- CBP Form 7501 Instructions, older copy hosted by ICPA: https://icpainc.org/wp-content/uploads/2012/08/ICPA%20-%20Mid%20codes%20-%20CBP%20Form%207501Instructions.doc

### Primary: Federal Register and IRS

- Electronic Refunds Interim Final Rule, FR Doc. 2025-24171 (published Jan 2, 2026; effective Feb 6, 2026): https://www.govinfo.gov/content/pkg/FR-2026-01-02/html/2025-24171.htm
- CBP Quarterly IRS Interest Rates notices:
  - 2026-01175 (Jan 22, 2026; Q1 2026): https://www.govinfo.gov/content/pkg/FR-2026-01-22/html/2026-01175.htm
  - 2026-09871 (May 18, 2026; Q2 2026): https://www.federalregister.gov/documents/full_text/xml/2026/05/18/2026-09871.xml
  - 2026-13298 (July 1, 2026; Q3 2026): https://www.federalregister.gov/api/v1/documents/2026-13298.json
  - 2026-19292, 91 FR 60141 (Sept 22, 2026; Q4 2026 plus full history table): https://www.govinfo.gov/content/pkg/FR-2026-09-22/html/2026-19292.htm
- IRS IR-2026-98, "Interest rates remain the same for the fourth quarter of 2026" (Aug 21, 2026): https://www.irs.gov/newsroom/interest-rates-remain-the-same-for-the-fourth-quarter-of-2026

### Primary: statutes and regulations

- 19 U.S.C. 1501: https://www.govinfo.gov/content/pkg/USCODE-2023-title19/html/USCODE-2023-title19-chap4-subtitleIII-partIII-sec1501.htm
- 19 U.S.C. 1504: https://www.govinfo.gov/content/pkg/USCODE-2023-title19/html/USCODE-2023-title19-chap4-subtitleIII-partIII-sec1504.htm
- 19 U.S.C. 1505: https://www.govinfo.gov/content/pkg/USCODE-2023-title19/html/USCODE-2023-title19-chap4-subtitleIII-partIII-sec1505.htm
- 19 U.S.C. 1514: https://www.govinfo.gov/content/pkg/USCODE-2023-title19/html/USCODE-2023-title19-chap4-subtitleIII-partIII-sec1514.htm
- 26 U.S.C. 6622: https://www.govinfo.gov/content/pkg/USCODE-2023-title26/html/USCODE-2023-title26-subtitleF-chap67-subchapC-sec6622.htm
- 28 U.S.C. 2636: https://www.govinfo.gov/content/pkg/USCODE-2023-title28/html/USCODE-2023-title28-partVI-chap169-sec2636.htm
- 19 CFR 24.3a, 24.36, 24.72, 159.10, 159.11 (eCFR as of Oct 1, 2026), via the eCFR API, e.g.: https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-19.xml?part=24&section=24.36

### Primary: USITC HTS (2026 Revision 21, released Oct 9, 2026)

- https://hts.usitc.gov/reststop/exportList?from=9903.01.01&to=9903.02.99&format=JSON&styles=false
- https://hts.usitc.gov/reststop/exportList?from=9903.03.01&to=9903.03.99&format=JSON&styles=false
- https://hts.usitc.gov/reststop/exportList?from=9903.96.01&to=9903.96.99&format=JSON&styles=false

### Primary: CIT filings (via CourtListener RECAP)

**Atmus Filtration v. US, No. 26-01259**
- Lord Decl. (Mar 12, 2026), ECF 39: https://storage.courtlistener.com/recap/gov.uscourts.cit.19346/gov.uscourts.cit.19346.39.0.pdf
- Lord Decl. (Mar 30, 2026; filed Mar 31), ECF 51: https://storage.courtlistener.com/recap/gov.uscourts.cit.19346/gov.uscourts.cit.19346.51.0.pdf

**Euro-Notions Florida v. CBP, No. 25-00595**
- Lord Decl. (May 26, 2026), ECF 30: https://storage.courtlistener.com/recap/gov.uscourts.cit.17610/gov.uscourts.cit.17610.30.0.pdf
- Order (June 12, 2026), ECF 35: https://storage.courtlistener.com/recap/gov.uscourts.cit.17610/gov.uscourts.cit.17610.35.0.pdf
- Order (July 2, 2026), ECF 40: https://storage.courtlistener.com/recap/gov.uscourts.cit.17610/gov.uscourts.cit.17610.40.0.pdf
- Lord Decl. (July 13, 2026), ECF 45: https://storage.courtlistener.com/recap/gov.uscourts.cit.17610/gov.uscourts.cit.17610.45.0.pdf
- Order (July 15, 2026), ECF 46: https://storage.courtlistener.com/recap/gov.uscourts.cit.17610/gov.uscourts.cit.17610.46.0.pdf
- Order *In re Tariffs Collected in Reliance on IEEPA* (dated July 17, 2026; entered July 20), ECF 52: https://storage.courtlistener.com/recap/gov.uscourts.cit.17610/gov.uscourts.cit.17610.52.0.pdf. On the Euro-Notions docket this entry is tagged "[ENTERED IN ERROR]". The same order was to be entered in each of the ~3,700 plaintiff cases, and the text quoted here is the signed order itself. Secondary sources date the related orders July 15, 17 and 21 [U].

**V.O.S. Selections v. US, No. 25-00066**
- Thomas Decl. (June 4, 2026), ECF 98-1 (scanned; text obtained by OCR): https://storage.courtlistener.com/recap/gov.uscourts.cit.17080/gov.uscourts.cit.17080.98.1.pdf

**Freestyle World v. CBP, No. 26-01088**
- Docket: https://www.courtlistener.com/docket/72304044/freestyle-world-inc-v-united-states-of-america/
- Lord Decl. (Aug 25, 2026), ECF 38: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.38.0.pdf
- ITSA amicus brief (Sept 3, 2026), ECF 43-1: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.43.1.pdf
- Lord Decl. (Sept 15, 2026), ECF 50: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.50.0.pdf
- Order (Sept 17, 2026), ECF 52: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.52.0.pdf
- ITSA letter (Sept 25, 2026), ECF 56: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.56.0.pdf
- Lord Decl. (Oct 6, 2026), ECF 58: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.58.0.pdf
- Order (Oct 8, 2026), ECF 60: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.60.0.pdf
- Slip Op. 26-123, class certification (Oct 8, 2026): https://www.cit.uscourts.gov/sites/cit/files/26-123.pdf
- Consent motion and order extending the scheduling order to Nov 5 (Oct 21 / Oct 23, 2026), ECF 62/63: https://storage.courtlistener.com/recap/gov.uscourts.cit.19175/gov.uscourts.cit.19175.62.0.pdf

### Secondary: law firms, brokers, press

- Holland & Knight, "CAPE Has Arrived" (Apr 22, 2026): https://www.hklaw.com/en/insights/publications/2026/04/cape-has-arrived-navigating-the-next-phase-of-ieepa-duty-refunds
- V. Alexander, CSMS guidance summary (Apr 14, 2026): https://www.valexander.com/?p=3814
- Willson International (Apr 1, 2026): https://www.willsonintl.com/news/protective-protest-updated-cape-0401/
- Jet Worldwide, courier informal entries (Apr 23, 2026): https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds
- Krieger Worldwide via Mann Publications (May 13, 2026): https://www.mannpublications.com/fashionmannuscript/2026/05/13/krieger-worldwide-industry-news-cbp-provides-major-cape-phase-1-refund-processing-update/
- Snell & Wilmer, Section 122 ruling (May 8, 2026): https://www.swlaw.com/publication/more-tariff-refunds-not-so-fast-court-of-international-trade-strikes-down-section-122-tariffs-but-relief-is-limited-to-plaintiffs/
- Expeditors (June 24, 2026): https://info.expeditors.com/newsflash/cbp-announces-next-phase-of-cape-ieepa-refunds
- Greenberg Traurig (June 25, 2026): https://www.gtlaw.com/en/insights/2026/6/us-trade-developments-ieepa-refund-processing-de-minimis-suspension-and-section-301-investigation-against-germany
- MF Masuda via Mondaq, "What To Do For Each Entry Category" (July 6, 2026): https://www.mondaq.com/unitedstates/export-controls-trade-investment-sanctions/1812598/ieepa-tariff-update-what-to-do-for-each-entry-category
- Thompson Coburn, "FAQ 2: IEEPA Tariffs Litigation / CAPE Developments" (July 2026): https://www.thompsoncoburn.com/wp-content/uploads/2026/07/FAQ-2-IEEPA-Tariffs-Litigation-CAPE-Developments.pdf
- Arnall Golden Gregory (July 17, 2026): https://www.agg.com/news-insights/publications/ieepa-tariff-refund-updates-trade-court-says-lawsuits-required-for-finally-liquidated-entries/
- Great Lakes Customs Law, refund tracker (July 18, 2026): https://greatlakescustomslaw.com/ieepa-refund-tracker-cape-portal-status/
- Thompson Hine (July 29, 2026): https://www.thompsonhine.com/insights/cbp-launches-phase-2-of-the-ieepa-tariff-refund-process-and-confirms-development-of-phase-3/
- Morgan Lewis (July 30, 2026): https://www.morganlewis.com/fr/pubs/2026/07/reliquidation-and-relief-trade-court-orders-ieepa-refunds-for-finally-liquidated-entries
- BDO, IEEPA Refund FAQ (Aug 11, 2026): https://www.bdo.com/insights/tax/ieepa-tariff-refunds-frequently-asked-questions
- Diaz Trade Law, "DOJ Seeks to Vacate IEEPA Refund Injunctions" (Aug 12, 2026): https://diaztradelaw.com/doj-seeks-to-vacate-ieepa-refund-injunctions/
- AP via WTOP (Aug 2026): https://wtop.com/news/2026/08/government-fights-trade-judges-order-for-tariff-refunds-to-all-importers/
- IANS via NewKerala, congressional letter (Sept 10, 2026): https://www.newkerala.com/news/a/us-lawmakers-seek-swift-tariff-refunds-658.htm
- Shopappy, summary of the congressional letter (Sept 2026): https://shopappy.com/trade/tariffs-customs/congress-cbp-tariff-refund-90-day-deadline
- C.H. Robinson (Sept 17, 2026): https://www.chrobinson.com/en-au/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/
- Leyton, Phase 3 (Sept 17, 2026): https://leyton.com/us/insights/articles/cape-phase-3-set-to-launch-october-6-what-it-means-for-ieepa-tariff-refunds/
- Freightright, CAPE error guide (updated Sept 21, 2026): https://www.freightright.com/guideline/cape-error-code-cbp-ace-guide
- Cherry Bekaert (Sept 23, 2026): https://www.cbh.com/insights/alerts/ieepa-tariff-refund-update-cape-phase-iii-set-for-october-6/
- Troutman Pepper Locke, "A CAPEable Solution" (Oct 2, 2026): https://www.troutman.com/insights/a-capeable-solution-how-we-can-help-with-cbps-cape-phase-3-rollout-for-cit-plaintiffs-seeking-ieepa-tariff-refunds/
- Husch Blackwell, internationaltradeinsights (Oct 9, 2026): https://www.internationaltradeinsights.com/2026/10/cit-universal-injunction-power-challenged-in-ieepa-refund-appeal/
- Phillips Lytle (Oct 12, 2026): https://phillipslytle.com/cbp-opens-phase-3-of-cape-for-ieepa-refunds/
- Steptoe (Oct 13, 2026): https://www.steptoe.com/en/news-publications/global-trade-and-investment-law-blog/relief-in-sight-cit-certifies-class-for-ieepa-tariff-refunds-for-certain-importers.html
- Davis Wright Tremaine (Oct 14, 2026): https://www.dwt.com/insights/2026/10/cit-certifies-ieepa-duty-refund-importer-class
- Leyton, Phase 3 and class action (Oct 21, 2026): https://leyton.com/us/insights/articles/ieepa-refunds-cape-phase-3-and-the-freestyle-world-class-action/
- White & Case, termination of IEEPA tariffs (Mar 2, 2026): https://www.whitecase.com/insight-alert/united-states-terminates-ieepa-based-tariffs-following-supreme-court-decision
- Troutman Pepper Locke, *AGS* liquidation ruling (Dec 19, 2025): https://www.troutman.com/insights/liquidate-now-litigate-later-court-rejects-bid-to-halt-liquidation-of-entries-subject-to-ieepa-tariffs/
- Gingercontrol, IEEPA HTS codes (secondary list; cross-checked against USITC): https://gingercontrol.com/blog/which-hts-codes-carry-ieepa-duties

*Research note: the web-search budget for this session ran out near the end. The last items (CBP refund FAQs, the PSC deadline re-check, and the Federal Circuit docket status) were not searched further. They are listed in §(g).*
