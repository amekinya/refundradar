# RefundRadar — Product Plan v0.2 (Sun Oct 25 2026, evening)

> **One line a judge can repeat:** *"Before you pay anyone to chase your tariff refund, RefundRadar tells you what you're owed, which entries are about to expire, what will block the money, and what it should cost to recover it."*

**Decision: GO.** The refund rules are pinned down from primary CBP and court sources (21 routing rules, each tagged by confidence). The pain is documented. The gaps are real. The legal boundary is clear. Details in §11.

Research behind this plan (all with sources):
- `docs/refund_rules_research.md` — CBP rules, decision table R0–R20, CAPE file format, interest, Chapter 99 headings
- `docs/research/competitors.md` — 17 players reverse-engineered, 6 deep teardowns
- `docs/research/complaints.md` — 16 complaint categories, ranked
- `docs/research/feasibility_legal_market.md` — legal limits, data access, couriers, market size

---

## 1. What changed since v0.1 (and why)

| v0.1 assumption | What the research found | v0.2 decision |
|---|---|---|
| "No free self-serve tool exists" | **Wrong.** 8+ brokers offer free calculators. Freight Right reads the ACE export in-browser and outputs a CAPE-ready file. GingerControl sorts entries by route and deadline. | Don't compete as "a free calculator." Compete as the **honest second opinion**: everything they split across products, plus what none of them do. |
| Generate a ready-to-submit CAPE file | Preparing refund filings for someone else is **"customs business"** that requires a broker license (19 U.S.C. 1641; CBP ruling HQ 114199). A Jan 2026 ruling (HQ H350722) says even a non-broker's OCR tool that decides filing data counts. | **Self-service triage tool for the importer's own data.** Outputs are "worksheets" and a "broker handoff packet," never "your filing." Form photos pre-fill a review grid the user confirms. |
| Main blocker is ACH enrollment | Confirmed and bigger: **20,362 approved refunds (~$1.1B) held for missing bank details** as of Oct 2. But the #1 and #2 pains are **entries aging out** and **"I'm not the importer of record."** | Deadline radar is the core. Claim-holder detection is a headline feature. ACH/ACE is part of a broader blocker checklist. |
| Simple phase logic | Rules are intricate: 80-day CAPE cutoff per entry, Phase 3 only for court plaintiffs, protest needed at 81–180 days, excluded entry types, surety-paid entries blocked, warehouse entries rerouted to withdrawals. | Encode R0–R20 as a versioned rules config. Anything tagged unconfirmed routes to **"Ask your broker"**, never a guess. |

## 2. The problem, in numbers

| Fact | Source (tag) |
|---|---|
| ~$166B in IEEPA duties, 53M+ entries, 330K+ importers | CBP declaration, June 4 2026 [P] |
| ~$136.6B accepted in CAPE by Oct 2; **~51% of entries vs ~81% of dollars** — the unfiled remainder is a long tail of small entries | CBP declaration Oct 6 [P]; feasibility notes |
| 300K+ smaller importers share ~$46B (~$150K each); only ~8% had registered by late March | TPM [S] |
| 20,362 approved refunds (~$1.1B) held for missing refund bank details (Oct 2) | CBP declaration Oct 6 [P] |
| ~15% of early CAPE filings rejected; a single bad line can sink a declaration | CBS [S]; Grayhawk [S] |
| Broker fees can eat 30–68% of small refunds (e.g., $750 minimum on a ~$1,100 refund) | Financial Wire, broker price pages [S] |
| CBP fraud warning: outside parties offering to "process refunds" are likely fraudulent | CSMS #68569567, May 7 2026 [P] |
| Deadlines run into 2027: 80-day CAPE windows (rolling), 180-day protests, CIT suit deadlines from ~Feb 1–4 2027 | Rules research [P]/[S] |

## 3. Who it's for

| | |
|---|---|
| **Primary** | Small US importers of record (roughly 20–2,000 formal entries) whose **broker filed entries under the importer's own number**, with no trade staff. They know they paid tariffs; they don't know what's left, what's expiring, or what a fair fee is. |
| **Routed, not served** | Businesses whose courier (UPS/FedEx/DHL), forwarder, or supplier was the importer of record; postal shipments. RefundRadar tells them **who holds the claim and exactly what to do next.** |
| **Future/commercial** | Small customs brokers running it on client data (their license covers customs business). Out of scope for the hackathon beyond a mention. |

## 4. Competitor reverse-engineering — what exists, and how good it is

| Player (type) | What it actually does | Price | Strength | Weakness for a small importer |
|---|---|---|---|---|
| **CBP ACE / CAPE** (government) | Accepts a list of entry numbers; CBP computes refund | Free | Authoritative | Needs ACE account (1 day–6 weeks setup), no triage, no deadline help |
| **Freight Right** (broker calculator) | In-browser ES-003 parse → eligibility, 7% simple interest, CAPE-ready CSV | "We collect when you collect" (% unpublished) | Closest functional match | Needs ACE export; Phase 1 only; details gated behind a sales call |
| **GingerControl** (prep + partner files) | Sorts entries into CAPE / protest / court by deadline | Unpublished | Closest positioning match | ES-003 only; no blocker or claim-holder checks; opaque pricing |
| **Gateway Lines** (AI estimator) | Reads PDFs/photos of paperwork, separates IEEPA from other duties | Free, 3 analyses/day | Only photo intake found | Estimate only; launched pre-CAPE; cap makes it useless at 20+ entries |
| **KlearNow** (paid service) | Full prep incl. ACH check, PSC housekeeping, CAPE CSV | $100–200 per entry | Only one that verifies ACH | Per-entry fees can exceed the refund; no protest; no interest |
| **UPS / DHL / FedEx** (carrier programs) | File for entries they brokered | DHL $2.10/entry; UPS $300–500/declaration | Cheapest for courier entries | Require ACE + ACH already; own entries only; 2025 parcel gap |
| **Clearit / Alliance / UNIS / JFS** (broker calculators) | Estimate → sell filing | Clearit $200+$125/entry; Alliance 2%, $10K min | Easy | Estimates ignore liquidation, deadlines, interest |
| **Grayhawk TRP / Leyton / TariffRefundHQ** (contingency) | Full service incl. protest and litigation | 10–30% contingency (mostly unpublished) | Covers every route | Expensive; asks for shared ACE access (clashes with CBP fraud guidance) |
| **ONESOURCE, Gaia, Reform, Wove, Tandom** (software) | Audit/calculator features | Enterprise | — | Not built for small importers; ONESOURCE says it doesn't support CAPE |

**What nobody does (verified gaps):**
1. **Works before the importer has ACE access** — everything else needs the ES-003 export.
2. **Tells you who actually holds the claim** (you vs courier vs forwarder/supplier) and what to do.
3. **Sorts every route** — CAPE Phase 1/2/3, PSC-first, protest, litigation-only, blocked, not eligible. Free tools stop at Phase 1.
4. **Correct interest** — per quarter, daily compounding estimate. Competitors use flat 7% or nothing.
5. **"Is it worth it?" cost comparison** — net refund under self-file vs courier vs flat broker vs contingency.
6. **Checks a refund offer you received** against CBP's fraud red flags and computes its real fee on your numbers.

## 5. What people complain about (ranked)

| Rank | Pain | Evidence strength | Existing fix? | Quality / awareness | RefundRadar answer |
|---|---|---|---|---|---|
| 1 | **Entries aging out** (80-day cutoff, Phase 3 plaintiff-only, slow ACE approval) | High — CBP filings, congressional letter Sept 9, ~37% of entries excluded from Phase 1 | Partial (GingerControl deadline sort; brokers) | Low awareness; ES-003 only | **Deadline radar** per entry + "at risk this week" + protest/litigation packets |
| 2 | **"I'm not the importer of record"** (courier, forwarder, supplier, DDP) | High — many news sources; most small retailers | Carriers' own programs | Confusing; no pass-through law | **Claim-holder detection** + next step per holder |
| 3 | **"How much am I owed — is it worth paying someone?"** | High — ~30 named owners in press; senators' letter | Broker calculators | Funnels into sales; ignore fees | **Estimate + cost-to-recover comparison** |
| 4 | **ACE / refund-ACH setup gaps** strand approved money | High — CBP: 20K refunds held | KlearNow (paid) | Fix exists but doesn't reach people | **Blocker checklist** with setup lead times |
| 5 | **Courier refund opacity** (2025 parcels gap, fees not refunded) | Medium — 80+ class actions, 17 fee suits | Carrier FAQs | Poor | Routing + "no path today" honesty |
| — | **Scams & predatory fees** | Medium — CBP warning; fake letters circulating | None | — | **Offer check** |
| — | **CAPE file rejections** | Medium — ~15% early | Brokers, KlearNow | OK for paying clients | **Pre-check** the entry list (check digit, duplicates, excluded types) |

Limits of this evidence: Reddit/Seller Central volume couldn't be measured directly (blocked); counts are distinct named sources, not upvotes. No real user interviewed yet — **your broker/importer outreach fills this.**

## 6. The product (v0.2)

### Inputs (any combination)
1. **ACE ES-003 export** (primary) — parsed by its published column names.
2. **Any other spreadsheet** from a broker or courier — Nemotron Nano maps unfamiliar columns.
3. **Photos/PDFs of Entry Summaries (CBP Form 7501)** — Nemotron Super VL pre-fills a **review grid**; the user confirms each field (keeps us on the right side of the customs-business line and catches misreads).
4. **Five readiness questions** — ACE portal account? refund bank account enrolled? who files your customs? any open protests/drawback? are you a court plaintiff?
5. **Optional: paste a refund offer** (email/letter) you received.

### Outputs
| Output | What it shows | Built from |
|---|---|---|
| **Headline** | Estimated IEEPA refund + interest, split into: reachable now · act before a deadline · blocked · litigation only · not eligible | Rule engine |
| **Deadline radar** | Timeline of entries crossing the 80-day CAPE cutoff and 180-day protest deadline; Feb 2027 court decision point; .ics calendar export | Rule engine |
| **Per-entry route** | Route, rule ID (R0–R20), deadline, plain-English reason, source link, confidence tag | Rule engine + templates; Ultra only for unconfirmed/complex cases |
| **Blocker checklist** | ACE account, refund ACH, contact email (Form 5106), surety, open protest, drawback, reconciliation | Rules + readiness answers |
| **Who holds the claim** | You / courier (with their program) / forwarder or supplier (with a request-letter template) | Engine + Super VL (importer-of-record field) |
| **Cost to recover** | Net refund under self-file, courier, flat broker, contingency 10/20/30% | Engine + published fee schedules |
| **Offer check** | Red flags vs CBP's fraud guidance, real fee on your numbers, what the web says about the firm | Ultra + Tavily |
| **Broker handoff packet** | Eligible entry list (pre-checked), deadlines, protest-prep list, questions to ask — worded as a worksheet | Engine |
| **Rules freshness** | "Rules verified as of [date]" + alert if CBP/court guidance changed since | Tavily |

### What we deliberately will NOT build (and why)
| Not building | Why |
|---|---|
| Filing, connecting to ACE, or "submit" buttons | Customs business; CBP: only ACE is valid |
| Collecting ACE logins or bank details | Mirrors scam red flags; never needed |
| HTS classification / reclassification advice | Clearest customs-business line (HQ H350722); not needed |
| Ready-to-sign protests or court complaints | Legal work — hand off to broker/attorney |
| Contingency or per-entry fees | Regulatory risk (19 CFR 111.36(b)) and scam optics |
| "Claim your refund now!" urgency marketing | CBP fraud red flag |

Disclaimer, on every screen footer and export: *"A self-check tool for importers reviewing their own entries. Not a customs broker or law firm. Does not file with CBP. Refund requests are filed only in ACE, by you or your licensed customs broker."*

## 7. Where NVIDIA models and Nebius do real work

| Job | Why code alone can't | Model | Why this tier |
|---|---|---|---|
| Read photos/PDFs of 7501 forms into a review grid | Scans, skew, handwriting, varied layouts | **Nemotron 3.5 Super VL** (strict JSON schema) | Vision + reliable structured output |
| Map a broker's or courier's odd spreadsheet to our schema | Every broker exports differently | **Nemotron 3 Nano**, reasoning off | Fast, ~free; one call per file |
| Explain the importer's whole situation as an action plan | Needs judgment across hundreds of entries, deadlines, blockers and the rules text | **Nemotron 3 Ultra**, reasoning on, long context | Holds the full entry summary + rules + readiness answers in one prompt |
| Review entries hitting unconfirmed rules | Ambiguous cases (informal entries, FTZ, suspension records) | **Ultra** | Hard reasoning, cites the rule text |
| Offer check | Reading persuasive letters for red flags is a language task | **Ultra** + **Tavily search** | Reasoning + live web evidence |
| Rules freshness | CBP and courts change rules on no fixed schedule | **Tavily Search + Extract** → **Nano** classifies "changed / not" | Cheap daily check |

Money math, dates and routing **never** come from a model. We'll measure that this hybrid beats a model-only approach (§9).

Nebius depth: all inference on **Token Factory** (live model IDs verified with `GET /v1/models`); **Batch API** for big ledgers (stretch); prompt caching on the rules text; spend cap + demo mode.

## 8. Demo (< 3 min) — synthetic importer, no real data

**"Prairie Lantern Home Goods"** (invented): 312 entries from 2025 (China, Vietnam, India), a broker-filed ES-003 export, 3 phone photos of 7501s for UPS-handled shipments, and an unsolicited "we'll recover your refund for 25%" email.

| Time | Shows |
|---|---|
| 0:00–0:30 | **Aha:** "$61K owed + ~$4K interest. 41 entries worth $18K leave the CAPE window in 21 days. Your refund bank account isn't set up — CBP would hold every dollar. That 25% offer would cost you $16K; your broker's flat fee would cost ~$1.6K." *(numbers illustrative)* |
| 0:30–1:30 | How: photo → review grid (Super VL), deadline radar, a tricky entry explained (Ultra), the rule ID + source, the rules-freshness stamp (Tavily) |
| 1:30–2:15 | **Measured results table** (§9) |
| 2:15–2:45 | Who it's for + a real broker/importer quote; the self-service boundary |
| 2:45–3:00 | Stack: Nemotron Nano / Super VL / Ultra on Token Factory, Tavily |

## 9. How we prove it works

| Test set (synthetic, labeled from the written rules — not from our engine) | Metric | Baseline |
|---|---|---|
| ~120 entries spanning all routes R0–R20 | Route accuracy; deadline exactness (days) | Ultra-only and Nano-only given the same rules text |
| ~30 rendered 7501 photos (blur, skew, glare) | Field accuracy; % fields the user had to correct | — |
| ~20 offers (10 scammy/predatory, 10 legitimate) | Red-flag detection rate | — |
| Full 312-entry run | Cost per 1,000 entries; seconds per ledger | Per model tier |

## 10. Architecture & trust

- **Stateless server**: files processed in memory, nothing stored, no accounts. Importer numbers/EINs masked before any model call.
- **Rules as config** (`rules.yaml`): every rule has an ID, condition, route, deadline formula, action text, source URL and confidence tag — so a court ruling means editing config, not code.
- **Python** rule engine with a pytest suite; **FastAPI**; single-page front end (no build step); deployed on a free host; demo mode with precomputed results; daily spend cap.
- **Keys** live only in GitHub Secrets and the host's settings.

## 11. Go / no-go

| Criterion (set Sunday) | Result |
|---|---|
| Rules pinned down from official sources | ✅ R0–R20 from CBP CSMS, CBP's CAPE guide, court declarations/orders, statutes; unconfirmed items tagged and routed to "ask your broker" |
| Real, documented pain | ✅ CBP's own numbers, congressional letters, ~30 named owners in press |
| Room to be different | ✅ six verified gaps (§4) — but Freight Right and GingerControl overlap, so the demo must lead with the gaps |
| Legal path | ✅ self-service triage is the established pattern; filing stays with importer/broker |
| Buildable in 4 days | ✅ no beta access needed; all inference on Token Factory |

**Honest weaknesses:** US-only problem for a global panel; no real user yet; rules are moving (CBP status report due **Oct 26**, court conference **Oct 27**, class scheduling order **Nov 5**, appeal pending) — we re-check Tuesday and show the rules-version stamp.

## 12. Risks

| Risk | Mitigation | When |
|---|---|---|
| Rules change this week | Rules-as-config; re-check after Oct 26/27; freshness banner | Tue |
| Judges see "another refund calculator" | Lead the video with deadlines, claim holder, blocked money, offer check — things calculators don't do | Video |
| Vision model misreads forms | Review grid with confirmation; measure correction rate; CSV path unaffected | Tue |
| Ultra context/params differ from listings | Smoke test before building on it | First hour with credits |
| Legal optics | Self-service wording, worksheet outputs, no filing, disclaimer | Always |
| Credits | Demo mode, spend cap, Nano for bulk | Always |

## 13. Schedule (CT)

| Day | Build | You |
|---|---|---|
| **Sun night** | Plan v0.2 ✅ · rules config · rule engine start · synthetic data generator | Claim credits; message 3–5 brokers/importers |
| **Mon** | Engine + tests (R0–R20, interest, deadlines, cost comparison) · 312-entry dataset + labeled set · 7501 photo renderer | Create GitHub repo; add secrets; 10-min smoke test |
| **Tue** | Model layer (Super VL grid, Nano mapping, Ultra plan + edge cases + offer check, Tavily freshness) · eval harness · **re-check rules after Oct 26/27** | — |
| **Wed** | UI · demo mode · deploy · stranger test · **feature freeze 11 pm** | Click through it cold; tell me what confused you |
| **Thu** | Eval numbers final · README · Devpost text · feedback write-up · video script · **submit Thu night** | Record + upload video |
| **Fri** | Final checks only · deadline **noon CT** | Confirm submission |

## 14. Outreach questions (for brokers/importers)

1. "Which of your small clients still haven't filed for IEEPA refunds — and why?"
2. "What's the most common reason a refund gets stuck or an entry gets rejected?"
3. "If a client showed up with a one-page summary — entries by route, deadlines, blockers — would that save you time? What would make you trust it?"
4. "What do you charge small clients, and when is it not worth their while?"
