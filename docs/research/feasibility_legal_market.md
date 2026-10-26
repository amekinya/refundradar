# RefundRadar: Legal, Data-Access, Segmentation and Market Constraints (as of Oct 25, 2026)

Scope note: CBP refund-rule mechanics (phase definitions, CAPE CSV columns, interest), competitor teardowns and complaint mining are covered by other researchers and are only touched here where they bear on a constraint. Evidence is cited inline. Anything under "Inferences" is my reasoning, not a sourced fact. The web-search budget ran out near the end of this session, so a few checks (IOR-number format, an FTC-specific warning, the Federal Circuit argument date) could not be done. They are listed under Gaps.

---

## 1. Legal: is preparing refund filings, classifying entries into pathways, or drafting protests "customs business" that needs a licensed broker?

### Takeaway
Under 19 U.S.C. 1641 and CBP rulings, a non-broker that prepares refund documents for another importer, or advises on that importer's specific transactions, is very likely conducting customs business. That holds even when the client signs and files the documents. A 2026 CBP ruling (H350722) also treats an unlicensed company's OCR tool as customs business when the tool decides what data goes into a CBP filing. RefundRadar's safest legal position is a self-service analysis tool that the importer of record uses for its own review: it produces worksheets and checklists, not filings prepared "for" the user, and the importer or a licensed broker or attorney makes the filing decisions. Protests are the exception: any agent holding a power of attorney may file them.

### Cited Findings
**Statute and regulation**
- 19 U.S.C. 1641(a)(2) defines "customs business" as activities "involving transactions with U.S. Customs and Border Protection" concerning entry, classification and valuation, "the payment of duties, taxes, or other charges ... or the refund, rebate, or drawback thereof." Refunds are therefore inside the definition. — [Cornell LII, 19 USC 1641](https://www.law.cornell.edu/uscode/text/19/1641)
- 1641(b)(1): "No person may conduct customs business (other than solely on behalf of that person) ... unless that person holds a valid customs broker's license." 1641(b)(6) sets a penalty of up to $10,000 per transaction for intentional unlicensed customs business. — [Cornell LII, 19 USC 1641](https://www.law.cornell.edu/uscode/text/19/1641)
- The definition covers preparing documents and transmitting them to CBP. It excludes "the mere electronic transmission of data received for transmission to Customs." — [CBP HQ H350722 (Jan 16, 2026)](https://rulings.cbp.gov/api/getdoc/hq/2026/H350722.pdf)
- 19 CFR 111.1 defines "corporate compliance activity" as activity by a business entity to ensure documents for a *related* business entity are prepared and filed with reasonable care. It "does not extend to the actual preparation or filing of the documents." — [USLegal quoting 19 CFR 111.1](https://definitions.uslegal.com/c/corporate-compliance-activity)

**Key rulings**
- **HQ 114199 (Feb 26, 1998).** A former Customs employee asked about drawback consulting. CBP held that preparing or helping prepare Customs forms is customs business "even if the client signs and files them." Unlicensed consultants "may not offer advice, or participate in discussions with Customs, on issues relating to a particular transaction." General education, such as teaching how to file and helping set up programs, is allowed. An unlicensed person may prepare, sign and file a protest if "the consultant has been issued a power of attorney to file the protest." — [HQ 114199 via open-gov.usebase.io](https://open-gov.usebase.io/rulings/114199)
- **HQ H350722 (Jan 16, 2026, made public about March 2026).** An unlicensed online platform offered:
  - OCR that extracted entry data from documents. CBP held this is customs business: "an unlicensed entity cannot decide what data should appear on an entry," whether or not an entry is ultimately filed.
  - AI classification. Output to 6 digits is not customs business; 10-digit output for goods being entered is. A disclaimer only helps if it is "meaningfully implemented." CBP also said a tool is not a "person" and cannot itself make classification decisions.
  - Form 5106 preparation for others, which is customs business.
  - Fees tied to broker-filed entries, which may violate 19 CFR 111.36(b).
  - Merely connecting importers and brokers, which is not customs business.
  — [CBP HQ H350722](https://rulings.cbp.gov/api/getdoc/hq/2026/H350722.pdf); [ST&R summary, Mar 20, 2026](https://www.strtrade.com/trade-news-resources/str-trade-report/trade-report/march/cbp-clarifies-limits-for-importer-services-tech-platforms)
- **HQ H326926 (Dec 2023).** An unlicensed offshore company extracting entry data from shipping documents and keying it into ABI "would impermissibly conduct customs business." The ruling relied on HQ H068278 (2009), which found that an unlicensed contractor's OCR extraction of entry data was customs business. — [ST&R, Jan 10, 2024](https://www.strtrade.com/trade-news-resources/str-trade-report/trade-report/january/cbp-reiterates-limitation-on-entry-preparation-work-by-non-brokers); [International Trade Insights](https://www.internationaltradeinsights.com/2023/12/cbp-further-defines-customs-business-in-new-ruling/)
- **Secondary summary of other rulings (vendor blog; I did not read the rulings themselves).** It reports that consultants may "review liquidated entries, if the review does not become classification or appraisement of future imports" (HQ 114654, H272798), and may "file ruling requests and protests as any authorized agent." — [Ginger Control, "What is customs business"](https://gingercontrol.com/blog/customs-business-definition-importers-guide)

**Who may file protests**
- 19 CFR 174.12(a) allows filing by:
  - the importer or consignee shown on the entry papers, or their sureties;
  - any person paying or receiving a refund of a charge;
  - any person seeking entry or delivery;
  - drawback claimants;
  - "any authorized agent" of the above, subject to 174.3.
- 174.12(e): the deadline is 180 days from the notice of liquidation or reliquidation for entries made on or after Dec 18, 2004. — [Cornell LII, 19 CFR 174.12](https://www.law.cornell.edu/cfr/text/19/174.12)
- 19 CFR 174.3 sets the power-of-attorney rules:
  - Attorneys need no POA; their signature declares good standing.
  - A customhouse broker needs no protest-specific POA but must hold a general POA to transact customs business for the principal.
  - Any other agent needs a POA that specifically authorizes them to "make, sign, and file the protest." — [Cornell LII, 19 CFR 174.3](https://www.law.cornell.edu/cfr/text/19/174.3)
- A law firm warns that a denied self-filed protest "may foreclose later recovery" and that arguments left off Form 19 are generally unavailable at the CIT. (This is promotional content from a contingency-fee firm.) — [Ayar Law protest guide](https://ayarlaw.com/tariff-refund-resources/cbp-protest-tariff-refund)

**Who may file CAPE declarations**
- CBP-derived fact sheet: "Only the importer or the authorized customs broker who filed the entries may submit the CAPE Declaration." — [IEEPA Duty Refunds Fact Sheet (Rep. Sykes site, reproducing CBP)](https://sykes.house.gov/imo/media/doc/ieepa_duty_refunds_fact_sheet.pdf)
- The CBP FAQ, as summarized by a law firm, says declarations are "submitted by the importer of record (IOR) or its broker." It does not address other third parties. — [HLC summary of CBP FAQs](https://hlc.com/en/publications/us-customs-and-border-protection-issues-faqs-on-ieepa-tariff-refunds)
- A licensed broker argues that "only licensed customs brokers may transact customs business for others," citing 19 CFR 111.2. This is self-interested. — [Freight Right](https://www.freightright.com/news/why-customs-brokers-are-the-better-fit-for-ieepa-tariff-refunds)

**How existing tools word their disclaimers**
- **Flexport Tariff Refunds tool:** "provided for general informational purposes only ... to assist importers of record with their own corporate compliance activities"; "does not constitute legal, tax, customs, or professional advice"; "Flexport is not acting as your Customs Broker, attorney, or advisor through the provision of this service." — [Flexport refunds help](https://tariffs.flexport.com/refunds/help)
- **Tariffs API:** "not a licensed customs broker and does not file claims on your behalf"; "not affiliated with CBP"; "Final determinations on refund eligibility are made by US Customs and Border Protection." — [TariffsAPI IEEPA refund page](https://tariffsapi.com/ieepa-refund)
- **UPS:** "provided for general awareness and is not legal advice"; "Eligibility does not guarantee a refund." UPS sells its fee-based CAPE filing only for UPS-brokered entries. For non-UPS-brokered entries, UPS Trade Advisory "reviews customer ES003 data and provides a CAPE template with eligible data only." — [UPS tariff refunds page](https://ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds)

### Inferences
- **CAPE declarations are refund filings, so preparing one for someone else is customs business.** HQ 114199 says helping prepare a form is customs business even when the client signs and files it. A hosted service that builds a specific importer's CAPE CSV, or tells them "file these entries," is close to the line.
- **The strongest defense is the "solely on behalf of that person" exception.** The importer runs the tool on its own data and decides for itself. Flexport's wording ("assist importers of record with their own ... compliance activities") is built on this theory.
- **The 7501-photo OCR feature is the riskiest part of RefundRadar.** H350722 and H068278 call OCR customs business when it decides what data appears in a CBP filing. Mitigations, which reduce but do not remove the risk:
  - Show OCR output only as an editable review aid the user must confirm field by field.
  - Never auto-produce a "ready to file" artifact from OCR alone.
  - Label outputs "worksheet" or "checklist," not "filing."
- **H350722's OCR concern was pre-entry data, and RefundRadar works on past entries.** RefundRadar's OCR reads already-filed, often liquidated entries, and the reported HQ 114654/H272798 position allows reviewing liquidated entries. Whether a CAPE list counts as "preparing" a refund filing is still unresolved. I found no ruling directly on CAPE.
- **Pathway classification looks like analysis, but the label still matters.** Sorting entries into "CAPE-eligible / protest / CIT / class / carrier" is analysis of the importer's own data. Calling it "advice on a particular transaction" for a paying third party is what HQ 114199 forbids. Present it as rule-based information, with the reasoning shown and "confirm with your broker."
- **Pricing.** A contingency or percentage-of-refund fee for a non-broker, especially one tied to broker-filed entries, risks 19 CFR 111.36(b) (per H350722) and looks like what CBP's fraud guidance warns about (see Q6). Free or flat pricing is safer.
- **Protest drafting is legally easier than CAPE preparation (agent with POA), but practically riskier.** A poor self-filed protest can foreclose recovery. A "protest-prep packet" (entries, liquidation dates, deadline, IEEPA duty amounts, cite to *Learning Resources v. Trump*) handed to a broker or attorney is lower-risk than a ready-to-sign Form 19 with legal argument.
- **Unauthorized practice of law (UPL).** I found no source. CIT suits and any legal argument are attorney territory, so a tool should not draft CIT complaints.
- **The hackathon demo is low-risk. Commercial launch is not.** A commercial product should get a customs-counsel opinion, or partner with or be operated by a licensed broker. A broker using the tool internally removes the licensing issue entirely.

### Gaps
- No CBP ruling, CSMS or FAQ found that addresses non-broker third parties or software preparing CAPE declarations.
- No source on state UPL exposure for drafting customs protests.
- I could not reach the eCFR text of 19 CFR 111.1 and 111.2 (blocked by the allowlist). The definitions are quoted from secondary sources.
- I did not read the full text of HQ 114654 and H272798 (post-entry review of liquidated entries). Only a vendor summary was available.

---

## 2. Data access: can a small importer get its own entry data?

### Takeaway
Yes, but usually only through an ACE Portal importer account. Many small importers do not have one even though they have a Form 5106 record, because they relied on brokers. Setup estimates range from 1 business day to 6 weeks. Without ACE, the fallbacks are broker-provided reports or 7501 copies, carrier duty invoices, or ITRAC requests. The ES-003 report is the standard input, and its column names are published by vendors.

### Cited Findings
**ACE account requirements**
- The importer of record or the broker filing CAPE "must have an established ACE Secure Data Portal account." Bank information for refunds is provided through ACE. — [Globalfy help center](https://help.globalfy.com/help-center/ieepa-duty-refunds-via-cape-ace); [CBP fact sheet via Sykes](https://sykes.house.gov/imo/media/doc/ieepa_duty_refunds_fact_sheet.pdf)
- A modernized web ACE Portal application was released April 1, 2026 (CSMS 68228015). It requires a Trade Account Owner (TAO) and an existing 5106 record that the application links to the new top account. "5106 without a portal account" is "the most common gap we see." — [Ginger Control, ACE access](https://gingercontrol.com/blog/ace-portal-access-ieepa-tariff-refund)
- The verification code goes to the point-of-contact email on the 5106 record, so an outdated email delays onboarding. TAOs can give a broker access through a POA without sharing credentials. Registration is free. — [Gaia Dynamics ACE data guide, Aug 13, 2026](https://www.gaiadynamics.ai/blog/the-ace-data-guide-pull-your-own-import-history-and-quantify-your-tariff-exposure); [Mohawk Global ACE FAQ, May 2026](https://mohawkglobal.com/wp-content/uploads/2026/05/ACE-FAQs-Mohawk-Global.pdf)
- **Mohawk Global ACE FAQ (May 2026)** also reports:
  - ACH refund enrollment has been required since Feb 6, 2026.
  - A user must sign in every 45 days or the account goes inactive.
  - Only the TAO or a proxy can assign roles.
  - When a broker uploads the CAPE declaration, the importer cannot see claim status in its portal "only when the importer does the upload"; it needs reports instead.
  - A U.S. bank account is required, or a third party can be designated through Form 4811.
  — [Mohawk Global ACE FAQ](https://mohawkglobal.com/wp-content/uploads/2026/05/ACE-FAQs-Mohawk-Global.pdf)
- **Approval-time estimates conflict:**

  | Estimate | Source |
  |---|---|
  | "up to two weeks" (June 22, 2026) | [UHY](https://uhy-us.com/insights/news/2026/june/tariff-refunds-are-moving-what-importers-should-know-about-ace-access-timing-and-treasury-disbursements) |
  | "4–6 weeks" | [Baker Tilly](https://www.bakertilly.com/insights/how-to-use-ace-portal-reports-for-ieepa-tariff-refunds) |
  | "3 to 5 business days" | [Ginger Control DDP article](https://gingercontrol.com/blog/ddp-shipments-courier-ior-ieepa-refund) |
  | Phase 3 CAPE access granted about 1 business day after CBP received importer info | [DWT, Oct 2026](https://www.dwt.com/insights/2026/10/cit-certifies-ieepa-duty-refund-importer-class) |

- A Sept 9, 2026 letter from 10 House Democrats (led by Reps. Stevens and Horsford) to CBP Commissioner Scott says slow CAPE and ACE account approvals push entries past the post-liquidation window. — [ShopAppy summary](https://shopappy.com/trade/tariffs-customs/congress-cbp-tariff-refund-90-day-deadline); [Leyton](https://leyton.com/us/insights/articles/cape-phase-3-set-to-launch-october-6-what-it-means-for-ieepa-tariff-refunds/)

**Which ACE reports to use**
- **Report list:**
  - ES-001 (Entry Summary Header)
  - ES-002 (Entry Summary Line)
  - ES-003 (Entry Summary Line Tariff Details, the primary report because it carries Chapter 99 overlay lines)
  - ES-006
  - ES-701 (Courtesy Notice of Liquidation) and ES-702 (Extension/Suspension)
  - TR-001 to TR-005 (Section 232/301)
  - ITRAC Entry Summary reports
  — [Gaia Dynamics](https://www.gaiadynamics.ai/blog/the-ace-data-guide-pull-your-own-import-history-and-quantify-your-tariff-exposure); [Baker Tilly](https://www.bakertilly.com/insights/how-to-use-ace-portal-reports-for-ieepa-tariff-refunds); [Ginger Control ES-003](https://gingercontrol.com/blog/es003-report-ace-ieepa-refund)
- **Path:** Accounts → Importer → Reports → Public Folders → ACE → Trade → Importer → Entry Summary → "ES-003 Entry Summary Line Tariff Details." Parameters are the Trade Account ACE ID and entry date begin/end. — [Alliance CHB ES003 Guide](https://alliancechb.com/ES003_Guide.pdf)
- **ES-003 required columns, per Flexport's upload spec:**
  - Entry Summary Number
  - Entry Date
  - Entry Summary Line Number
  - Tariff Ordinal Number
  - HTS Number - Full
  - Line Tariff Goods Value Amount
  - Line Tariff Duty Amount
- **ES-003 optional columns:**
  - Entry Type Code
  - Line SPI Code
  - Line Tariff Quantity (1) and Line Tariff UOM (1) Code
  - Line Tariff Quantity (2) and Line Tariff UOM (2) Code
  - Liquidation Date
  - Liquidation Status
  — [Flexport refunds help](https://tariffs.flexport.com/refunds/help)
- Gaia's list adds Entry Summary Date, Country of Origin Code, Country of Export Code and "Liquidation Date and Status." Export formats are Excel, CSV, PDF, HTML and TXT. Gaia also warns: "Don't sum the value field across all overlay ordinals ... Only the Chapter 1 through 97 line carries the entered value." — [Gaia Dynamics](https://www.gaiadynamics.ai/blog/the-ace-data-guide-pull-your-own-import-history-and-quantify-your-tariff-exposure)
- **Filtering:** filter HTS on 9903.01.xx and 9903.02.xx, not on 9903 alone, because Section 232, 301 and 122 lines share that prefix. Liquidation Date may need adding through the column picker. A broker-only sub-account returns no IOR data. — [Ginger Control ES-003](https://gingercontrol.com/blog/es003-report-ace-ieepa-refund)
- **Report reliability:** a report that returns "0 seconds" with no data did not execute and should be rerun. "Problems have been reported, likely due to the system being under construction." — [Baker Tilly](https://www.bakertilly.com/insights/how-to-use-ace-portal-reports-for-ieepa-tariff-refunds)

**Without ACE**
- Importers can ask their broker for a report of entries under 9903.01 or 9903.02. — [Beancount.io guide, Jul 8, 2026 (updated Sep 16)](https://beancount.io/blog/2026/07/08/ieepa-tariff-refund-cbp-cape-portal-small-importer-guide)
- Importers can request 7501s from the courier or broker for Feb 2025–Feb 2026 and match them to duty invoices. On the current 02/26 Form 7501, the Importer Number is block 27 and the IOR name and address is block 30. Older revisions use blocks 23 and 26. — [Ginger Control DDP](https://gingercontrol.com/blog/ddp-shipments-courier-ior-ieepa-refund)
- **ITRAC:** Importer Trade Activity data, provided by CBP under FOIA. In 2018 the standard turnaround was about 3 weeks, with an expedited email option "as little as one day from the date of payment" (pay.gov). CBP announced in 2019 that ITRAC was moving into ACE Reports. — [C.H. Robinson 2018 advisory](https://www.chrobinson.com/en//de-DE/-/media/ChRobinson/client-advisories/2018/111218%20Client%20Advisory%20Expedited%20ITRAC%20Option%20111218.pdf); [FreightWaves, Apr 18, 2019](https://www.freightwaves.com/news/cbp-to-make-import-data-access-easier-for-ace-users)
- CBP held webinars on May 20, 2026 ("IEEPA Duty Refunds for Small Businesses") and May 21, 2026 ("Reports for CAPE Claims – A Guide for Small Businesses"). Replays are at cbp.gov/trade/stakeholder-engagement/webinars. — [Expeditors](https://info.expeditors.com/newsflash/cbp-announce-cape-webinars-for-small-businesses)

### Inferences
- **ES-003 is a stable input contract.** Column names are consistent across Flexport, Gaia and the CBP-template guides, so RefundRadar should parse ES-003 by header name and tolerate optional columns and extra overlay ordinals.
- **The 7501-photo path is the "no ACE" fallback, and it is weaker.** It lacks liquidation status unless the user adds it, and a CAPE filing needs ACE anyway. So photos are useful for triage and estimates, but the user must still get ACE access, or have the filing broker act, before any money moves.
- **ACE setup is a hard blocker the tool should detect and plan for.** Checklist items: 5106 POC email current, TAO designated, importer sub-account linked, refund ACH enrolled (separate from payment ACH), 45-day login. Lead time is roughly 1 day to 6 weeks.
- **Current ITRAC turnaround in 2026 is unknown.** It is a plausible "I have nothing" fallback but should not be relied on.

### Gaps
- No official CBP published sample or template of an ES-003 export. Column names come from vendor documentation.
- ES-003 row or date-range limits are not documented in any source found.
- 2026 ITRAC turnaround and fees are unknown.
- No data on what share of IEEPA-paying importers lacked ACE accounts as of Oct 2026.

---

## 3. Couriers and small parcels: who is the IOR, who gets the refund, and can RefundRadar help?

### Takeaway
For express shipments, the refund flows to whoever is IOR on the entry. Carriers that were IOR file and pass money back to the duty payer under their own processes, sometimes for a fee. Where the customer was IOR and the carrier only brokered, the customer or the carrier must file through ACE. Sources disagree on whether the carrier or the consignee is the IOR on express informal entries, and on whether Type 11 informal entries are covered by CAPE Phase 1. Postal shipments have no CAPE path. RefundRadar can only triage this group ("who was your IOR, who to contact"). It cannot compute or prepare much.

### Cited Findings
**Carrier policies**
- **UPS.** Where UPS was IOR, "No action is required." Where the customer was IOR and UPS brokered, the customer self-files or buys the fee-based UPS CAPE Solution. CBP "does not evaluate private contractual arrangements or downstream cost pass-throughs." — [UPS](https://ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds)
- **FedEx.** Submits declarations for customers where it "served as customs broker."
- **DHL.** Auto-files for eligible Phase 1 entries where it was IOR. Customers who were IOR file themselves or ask DHL.
- **Launch day.** On April 20, 2026, more than 55,000 parties filed claims covering more than 4M imports.
  — [Supply Chain Dive](https://supplychaindive.com/news/fedex-ups-and-dhl-detail-tariff-refund-approach-for-customers/818057/)
- **DHL Express detail.** Where DHL was IOR, "checks will be issued to the party who originally paid the duty for US based customers." Where the customer was IOR, refunds go to the IOR's ACE ACH account ("CBP will not be issuing any checks"). DHL charges "a standard Import Paperwork Fee" when it files for a customer IOR. DHL says Phase 1 covers informal entries filed electronically in ACE within the window. Customers should check box 30 on the 7501 to confirm IOR. — [DHL](https://www.dhl.com/discover/en-us/global-logistics-advice/logistics-insights/navigating-us-trade-uncertainty/IEEPA-Trump-Tariff-Refunds)
- **Carrier totals and portals.**
  - FedEx received about $800M in IEEPA refunds, opened a portal by tracking number on July 10, 2026, and began disbursing around Aug 10, 2026. Customers who opt into sharing data "with trusted vendor partners" get priority payment.
  - UPS applied for just under $500M covering about 2.5M entries.
  - DHL estimates 30–90 days after it receives funds.
  - Class actions (e.g., *Reiser v. FedEx Logistics*) are pending.
  — [GetOutOfDebt.org, Aug 2026](https://getoutofdebt.org/268917/fedex-tariff-refunds-who-gets-paid-august-2026)

**Who is the IOR on express informal entries (conflict)**
- JetWorldwide: "The importer of record on an express informal entry is the ultimate consignee, not the carrier." It also says "Phase 1 does not currently address refunds on informal entries" and "Informal entries liquidate at clearance." — [JetWorldwide](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds)
- Zonos and Ginger Control: for DDP commercial-carrier shipments, "the carrier's brokerage is the IOR, not the merchant, and not the shopper." DDP terms do not by themselves identify the IOR, so check the entry record. — [Zonos](https://zonos.com/ieepa-tariff-refunds-cape); [Ginger Control DDP](https://gingercontrol.com/blog/ddp-shipments-courier-ior-ieepa-refund)
- Ginger Control describes three courier patterns: the courier files and remits minus a fee ("5–15% is common"), the courier never files, or the contract lets the courier keep the refund. — [Ginger Control DDP](https://gingercontrol.com/blog/ddp-shipments-courier-ior-ieepa-refund)

**Size of the informal-entry pool and postal shipments**
- JetWorldwide estimates informal entries at roughly 3–5% of IEEPA duty dollars (about $5B) but a "large share of entry count." This is an author estimate; CBP publishes no breakdown by entry type. — [JetWorldwide](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds)
- Postal shipments "were not entered into ACE." CAPE only handles ACE entries, and CBP has not announced a postal refund pathway. — [Zonos](https://zonos.com/ieepa-tariff-refunds-cape)
- The CBP FAQ excludes "Entries not filed in ACE, and entries without a liquidation status in ACE" from Phase 1. — [HLC summary of CBP FAQs](https://hlc.com/en/publications/us-customs-and-border-protection-issues-faqs-on-ieepa-tariff-refunds)

**De minimis background**
- The de minimis suspension has been in effect by executive order since Aug 29, 2025. CBP Dec. 26-12 and 26-13 codified it in 2026. The statutory repeal (OBBBA) takes effect July 1, 2027. Non-postal goods of $800 or less must now use formal or informal entry, with Type 11 the main informal method for shipments of $2,500 or less. The postal suspension rule took effect July 24, 2026. — [Greenberg Traurig, June 2026](https://www.gtlaw.com/en/insights/2026/6/us-trade-developments-ieepa-refund-processing-de-minimis-suspension-and-section-301-investigation-against-germany)

**Pass-through limits**
- Refunds go only to the IOR who paid. Vendors who added tariffs to invoices are not eligible recipients. — [Mohawk Global ACE FAQ](https://mohawkglobal.com/wp-content/uploads/2026/05/ACE-FAQs-Mohawk-Global.pdf)
- Merchants generally lack standing to file CAPE even when they absorbed IEEPA costs through DDP pricing. — [Zonos](https://zonos.com/ieepa-tariff-refunds-cape)

### Inferences
- **Many small importers live in the courier and e-commerce world:** Amazon sellers, DTC brands, consumers. Most of their entries were either carrier-IOR (money flows through the carrier's program) or consignee-IOR informal entries. CAPE treatment of the latter is disputed, and they may have liquidated at clearance, which makes them finally liquidated and outside CAPE without a court order.
- **What RefundRadar can usefully do for this group:**
  1. An IOR identification step: read 7501 block 27/30 or the carrier invoice, then branch to "carrier was IOR → use carrier portal" or "you were IOR → you need ACE."
  2. Carrier-specific next steps.
  3. A flag on carrier fees and opt-in data-sharing terms.
  4. A flag that postal duties currently have no path.
- **What it should not do for this group:** compute "your CAPE refund" on entries it cannot confirm are in ACE with a liquidation status.
- **The best-fit segment is small importers with formal (Type 01) entries filed under their own IOR number by a broker.** These are the "5106 but no ACE account" firms.

### Gaps
- No authoritative CBP statement found on (a) the IOR on express informal entries or (b) Type 11 eligibility in CAPE Phases 1 and 2. DHL and JetWorldwide conflict.
- No data on the share of small importers' entries that went through express couriers or informal entries.
- No CBP figure on how much IEEPA duty was collected on postal shipments.

---

## 4. Segmentation and market size

### Takeaway
About 330,000 importers paid IEEPA duties on about 53M entries, for about $166B. Census counts about 239,000 identified importing companies (2024 preliminary). About 97% are small or mid-sized and account for about 31% of import value. Firms with 1–19 employees are about 40% of importers but only about 6.5% of value (2021). By April 2026, only about 17–20% of IEEPA payers had completed CAPE or ACH setup. The leftover tail is many low-value importers.

### Cited Findings
**Census importer profile**
- 2024 preliminary: 239,231 identified importing companies, of which 232,804 (97.3%) are SMEs. SMEs account for $914.5B of $2,921.2B known import value (31.3%). — [Census, Profile of U.S. Importing and Exporting Companies 2024 (prelim, released Dec 11, 2025)](https://www.census.gov/foreign-trade/Press-Release/edb/2024prelimprofile.pdf)
- 2021 (226,662 importers) by employee count:

  | Employees | Share of importers | Share of known import value |
  |---|---|---|
  | 1–19 | 39.9% (90,443) | 6.5% |
  | Unknown or nonemployer | 37.9% | 9.5% |
  | 20–49 | 9.3% | 4.3% |
  | 50–99 | 4.7% | 3.8% |
  | 100–249 | 3.9% | 5.1% |
  | 250–499 | 1.7% | 5.1% |
  | 500+ | 2.5% | 65.6% |

  — [Census, Profile 2020–2021](https://census.gov/foreign-trade/Press-Release/edb/edbrel2021.pdf)

**IEEPA payers and filing rates**
- About 330,000 importers paid IEEPA duties, about $166B, across about 53M entries. As of an April 14, 2026 court filing, 56,497 importers (17%) had completed the CAPE process. About 82% of entries, worth about $127B, can be refunded electronically. — [American Action Forum, Apr 23, 2026](https://www.americanactionforum.org/shipment/its-raining-refunds/)
- CBP (Brandon Lord declaration, April 2026): about 300,000 firms eligible, about 57,000 (about 20%) signed up for electronic refunds. Foley's Greg Husisian: "A smaller company may not even know about it." — [Bloomberg Law, Apr 15, 2026](https://news.bloomberglaw.com/in-house-counsel/tariff-refunds-face-delays-over-slow-importer-opt-in-us-says); [Outlook Business](https://www.outlookbusiness.com/news/why-80-of-businesses-are-missing-trumps-166-billion-tariff-refunds)
- CIT class certification order: "Nearly 330,000 importers" paid IEEPA duties. — [DWT](https://www.dwt.com/insights/2026/10/cit-certifies-ieepa-duty-refund-importer-class)
- U.S. Chamber (Feb 23, 2026): "more than 200,000 small business importers" are due refunds. — [U.S. Chamber letter](https://www.uschamber.com/international/letter-on-tariff-refunds)
- As of June 29, 2026, approved refunds covered 30% of IEEPA entries and "mainly come from large, high-value entries." — [Cato, Jul 9, 2026](https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go)

**Refund size**
- About $8,000 average refund per entry among one LA broker's own clients. The broker warns this "should not be interpreted as a national estimate." The sample size was not disclosed. — [Freight Right, May 27, 2026](https://www.freightright.com/news/importers-receiving-almost-8000-per-entry-from-ieepa-refunds-survey-finds)
- Large importers have booked big refunds: Walmart about $2.9B, Macy's $116M. — [ShopAppy](https://shopappy.com/trade/tariffs-customs/congress-cbp-tariff-refund-90-day-deadline)

### Inferences
- **The two counts measure different things.** 330,000 IEEPA payers is more than Census's about 239,000 companies. CBP counts IOR numbers, which include non-resident importers, individuals and multiple IORs per firm. Census counts U.S. companies matched to business registers. Use 330k as the pool of refund claimants and Census only for size distribution.
- **Crude averages (my arithmetic):** $166B ÷ 53M entries ≈ $3,100 per entry; $166B ÷ 330k ≈ $500k per importer. Both are heavily skewed by large firms, so the median small importer is far smaller.
- **Rough small-firm pool.** If IEEPA duty shares tracked import-value shares, firms with 1–19 employees would hold about 6.5% ≈ $10–11B, and all SMEs about 31% ≈ $50B. This is a very rough proxy, because IEEPA rates varied by country (China far higher), which skews the mix.
- **Rough unfiled tail.** By Sept 2026, about 27.2M of about 53M entries (≈51%) were accepted, but $134.7B of $166B (≈81%) of dollars (see Q5). That leaves roughly 26M entries and about $31B, mostly small-dollar entries, which fits a long tail of small importers. A large part of that remainder is structurally outside CAPE (finally liquidated, AD/CVD, drawback, non-ACE, postal), so it is not all reachable by a CAPE-only tool.
- **The number of small importers still unfiled as of Oct 2026 is unknown.** The 80% non-signup figure is from April. Given the declaration counts below, a plausible guess is that tens of thousands to well over 100,000 small IORs remain without refunds. This is unverified.

### Gaps
- No CBP or official breakdown of IEEPA payers by size, entry count or refund value.
- No count of importers (as opposed to declarations) that had filed as of Oct 2026.
- No national estimate of typical or median small-importer refund size.

---

## 5. Remaining time-value: what is filed or paid vs. outstanding, upcoming deadlines, and appeal risk

### Takeaway
By mid-September 2026, about $134.7B (81% of $166B) had been accepted into CAPE and about $122B certified to Treasury, so the large-importer money is largely moving. The remaining value is concentrated in four places:
- late entries still rolling through liquidation into the 80-day CAPE window (through roughly Q1 2027);
- 180-day protest windows;
- a CIT limitations deadline around Feb 4, 2027 for the earliest entries;
- the new, mandatory, not-yet-effective Freestyle World class for non-litigants.

The government's Federal Circuit appeal threatens non-plaintiffs' refunds on finally liquidated entries. It does not threaten refunds already processed.

### Cited Findings
**Progress (sources conflict slightly; dates differ)**

| Date of data | Figures | Source |
|---|---|---|
| June 29, 2026 | $104.29B authorized; $71.06B paid incl. interest; about $25B outside Phases 1–3 (AD/CVD, drawback, protests, non-ACE entries); about $11.4B finally liquidated | [Cato, Jul 9](https://www.cato.org/blog/ieepa-refunds-update-good-progress-still-ways-go) |
| Aug 21, 2026 | $132.5B accepted; $106.6B sent to Treasury; 272,029 declarations; about $1.7B stuck for missing ACH (about 10,000 importers) | [ShopAppy](https://shopappy.com/trade/tariffs-customs/congress-cbp-tariff-refund-90-day-deadline) |
| Mid-Sept 2026 | More than 286,000 declarations submitted, more than 201,000 accepted, covering about 27.2M entries; about $134.7B accepted; about $122B (incl. interest) certified and transmitted to Treasury; 20,184 refunds ($1.3B) on hold for missing ACH | [C.H. Robinson, Sep 17](https://www.chrobinson.com/es-us/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/) |
| Oct 9, 2026 | "about $126 billion in duties, plus interest, has already been refunded" | [Thompson Hine](https://www.thompsonhinesmartrade.com/2026/10/cit-certifies-a-tariff-refund-class/) |

- Note the ACH-hold figures differ ($1.7B in August vs. $1.3B in mid-September). The two sources may count different things.

**Phase 3 and the class action**
- Phase 3 launched Oct 6, 2026. It is limited to finally liquidated entries of CIT plaintiffs with reliquidation orders who submitted IOR info by July 30, 2026. Non-litigants with finally liquidated entries "have no clear route under the current framework." — [Leyton (Phase 3)](https://leyton.com/us/insights/articles/cape-phase-3-set-to-launch-october-6-what-it-means-for-ieepa-tariff-refunds/); [Greenberg Traurig, Oct 19, 2026](https://www.gtlaw.com/ar/insights/2026/10/ieepa-refund-litigation-continues-as-importers-consider-individual-cit-filings)
- **Class certification, *Freestyle World v. U.S.*, Oct 8, 2026:**
  - Covers all IORs who paid under the challenged orders Feb 1, 2025 to Feb 19, 2026.
  - Excludes entities with their own suits and the Brazil/India orders.
  - Rule 23(b)(2): mandatory, no opt-out.
  - No claims process yet. Certification is "not a refund order."
  - The government is "all but sure to appeal."
  - Individual suits have moved fast: refund orders within about 4 business days of filing, and Phase 3 CAPE access about 1 business day later.
  — [DWT](https://www.dwt.com/insights/2026/10/cit-certifies-ieepa-duty-refund-importer-class); [Leyton (class), Oct 21, 2026](https://leyton.com/us/insights/articles/ieepa-refunds-cape-phase-3-and-the-freestyle-world-class-action/); [Steptoe, Oct 13, 2026](https://www.steptoe.com/en/news-publications/global-trade-and-investment-law-blog/relief-in-sight-cit-certifies-class-for-ieepa-tariff-refunds-for-certain-importers.html)

**Limitations deadlines**
- The two-year limit under 28 U.S.C. 1581(i) runs from deposit. The earliest date is Feb 4, 2027 (DWT, Troutman); Faegre conservatively uses Feb 1, 2027. — [Troutman, Aug 13, 2026](https://www.troutman.com/insights/to-sue-or-not-to-sue-that-is-the-question-for-ieepa-tariff-refunds/); [Leyton (class)](https://leyton.com/us/insights/articles/ieepa-refunds-cape-phase-3-and-the-freestyle-world-class-action/)
- GT staggers the start of the period by country: February 2027 for China entries, March 2027 for Canada/Mexico, April 2027 for all others. Tolling during the class appeal is unresolved. — [Greenberg Traurig, Oct 19, 2026](https://www.gtlaw.com/ar/insights/2026/10/ieepa-refund-litigation-continues-as-importers-consider-individual-cit-filings)
- Leyton: "For smaller claims, filing fees and legal costs may outweigh the benefit," so staying in the class may be reasonable. — [Leyton (class)](https://leyton.com/us/insights/articles/ieepa-refunds-cape-phase-3-and-the-freestyle-world-class-action/)

**Liquidation clock**
- CBP "generally liquidates entries within 314 days of the date of import." Once an entry is liquidated more than 80 days, CAPE options are limited. — [Mohawk Global, Jun 30, 2026](https://mohawkglobal.com/trade-translation/ieepa-refund-opportunities-narrow-as-entries-approach-key-liquidation-deadlines/)
- Protest deadline: 180 days from liquidation, with no CBP discretion for late protests. — [Ayar Law, Oct 22, 2026](https://ayarlaw.com/tariff-refund-resources/ieepa-tariff-refund-deadline); [19 CFR 174.12](https://www.law.cornell.edu/cfr/text/19/174.12)
- Low-value shipments, "which are liquidated almost immediately, are at the most risk." — [Livingston](https://www.livingstonintl.com/ieepa-refunds-no-longer-guaranteed-as-u-s-customs-and-cit-trade-barbs/) (Caution: this article is undated and calls the Supreme Court ruling "late January," which conflicts with Feb 20, 2026. Treat it as lower reliability.)

**Appeal risk**
- The government announced its appeal May 29, 2026 and filed its Federal Circuit opening brief Aug 10, 2026, citing *Trump v. CASA*. It contests relief for non-party importers and says it "will comply with importer-specific court orders." CAPE refunds continue. — [Cato, Jun 1, 2026](https://www.cato.org/blog/trump-administration-will-not-give-back-tariff-money-it-illegally-collected); [Thomson Reuters, Aug 18, 2026](https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/august-18th/us-doj-appellate-brief-ieepa-refunds)
- "Importers who have already filed CAPE applications and received their refunds will ultimately be unaffected." — [Livingston](https://www.livingstonintl.com/ieepa-refunds-no-longer-guaranteed-as-u-s-customs-and-cit-trade-barbs/)
- Oral argument was "expected soon" as of October. — [DWT](https://www.dwt.com/insights/2026/10/cit-certifies-ieepa-duty-refund-importer-class)

### Inferences
- **The tool still has value after Oct 30, 2026.** IEEPA duties were collected through about Feb 23–24, 2026. With the 314-day norm, entries made Dec 2025–Feb 2026 liquidate around Oct 2026–Jan 2027, so their CAPE 80-day windows run to about Jan–Apr 2027, and their 180-day protest windows into mid-2027. This is my calculation; actual liquidation dates vary.
- **Each user needs a per-entry deadline engine:** liquidation date + 80 days (CAPE), + 180 days (protest), and the Feb 2027 CIT decision point. That engine is RefundRadar's most defensible feature.
- **The value window probably narrows sharply after about April 2027.** By then the last CAPE windows close and the limitations dates pass. After that, value depends on how the class and appeal resolve.
- **Pathway rules must be data-driven and editable.** A Federal Circuit ruling or a class-wide relief order could change the finally-liquidated pathway overnight.
- **Stranded ACH refunds are a cheap, high-value fix.** About 10–20k refunds and $1.3–1.7B are stuck for missing banking details, which is a non-legal checklist item.

### Gaps
- No Oct 2026 CBP progress figures beyond mid-September.
- No Federal Circuit oral argument date found.
- No source estimating how many small-importer entries remain inside open CAPE or protest windows.
- Whether a class notice or claims process will require importer action is unknown.

---

## 6. Trust and safety

### Takeaway
CBP has explicitly warned that "any external website or unknown party offering to process refunds is likely fraudulent." Lawyers report fraudulent letters that cite real import activity, and refund-claim buyers and "pay to release" scams are circulating. A third-party refund tool starts out under suspicion. It must visibly avoid everything scams do: asking for credentials or bank details, contacting CBP, collecting fees to "release" refunds, sending unsolicited outreach, and storing data.

### Cited Findings
- **CBP CSMS #68569567 (May 7, 2026), "Best Practices for Protecting Your Information Regarding IEEPA Refunds":**
  - "No third-party shortcuts: Any external website or unknown party offering to process refunds is likely fraudulent."
  - "Only ACE is valid."
  - "CBP will not request sensitive data (e.g., SSNs, bank info, passwords) via email or text."
  - Legitimate CBP email ends in @cbp.dhs.gov.
  - "CBP will not send reports unless they have been requested by the user."
  - Red flags listed: offers to secure refunds on your behalf, urgent messaging, suspicious links.
  — [C.H. Robinson summary](https://www.chrobinson.com/en-gb/resources/insights-and-advisories/client-advisories/2026q2/05-08-2026-client-advisory-cbp-issues-guidance-to-protect-against-ieepa-refund-fraud-activity/)
- **Parker Poe (June 17, 2026).** Clients received "letters, emails, and other communications" referencing "specific import activity," with QR codes, phone numbers and websites. The firm advises not providing "ACE credentials, banking information, passwords, or other sensitive company information," and deactivating former employees' ACE access because dormant accounts can be used to infiltrate. — [Parker Poe](https://www.parkerpoe.com/news/2026/06/importers-should-exercise-caution-regarding-unsolicited-ieepa-tariff)
- **U.S. Chamber** warned of scammers offering to collect refunds for a fee or buying refund rights for "pennies on the dollar." — [U.S. Chamber letter, Feb 23, 2026](https://www.uschamber.com/international/letter-on-tariff-refunds)
- **Investors are buying refund claims "at a discount,"** with warnings about "potentially predatory arrangements with clawback provisions." — [Lewis Brisbois via Mondaq, Apr 6, 2026](https://www.mondaq.com/unitedstates/international-trade-investment/1768694/tariff-refund-claims-new-interest-in-purchasing-but-there-are-risks)
- **Never pay a fee to "release" a refund; type carrier URLs yourself.** FedEx's portal asks users to opt into sharing data with "trusted vendor partners" for faster payment. — [GetOutOfDebt.org](https://getoutofdebt.org/268917/fedex-tariff-refunds-who-gets-paid-august-2026)
- **Broker confidentiality.** Brokers owe confidentiality under 19 CFR 111.24, so sharing client records with a third-party platform needs written client consent. CBP flagged this in both H350722 and H326926. — [CBP HQ H350722](https://rulings.cbp.gov/api/getdoc/hq/2026/H350722.pdf); [ST&R Jan 2024](https://www.strtrade.com/trade-news-resources/str-trade-report/trade-report/january/cbp-reiterates-limitation-on-entry-preparation-work-by-non-brokers)
- **TAOs can grant brokers access through POA without sharing credentials.** — [Gaia Dynamics](https://www.gaiadynamics.ai/blog/the-ace-data-guide-pull-your-own-import-history-and-quantify-your-tariff-exposure)

### Inferences
- **What entry data exposes.** ES-003 and 7501s show the IOR number, supplier names, goods, values and duty paid. An IOR number is commonly the company's IRS EIN plus a suffix (I could not verify this in this session). That is sensitive, phishable data: the Parker Poe letters "referencing specific import activity" show scammers already use such details.
- **Recommended trust posture:**
  - Process files in the browser or on the device. No server upload, or ephemeral processing with nothing retained.
  - No accounts needed.
  - Never ask for ACE credentials, ACH or bank details, or SSNs.
  - Never contact CBP or file anything.
  - No percentage fees.
  - Optionally mask IOR numbers and EINs in exports.
  - Show a plain statement echoing CBP: "Refund requests are filed only in ACE by you or your broker. This tool never files, never asks for your ACE password or bank information."
- **Do not use language like "We get your refund" or "Claim your refund now."** It mirrors CBP's listed red flags and could make the product look like a scam.
- **For a broker-facing version,** require broker attestation of client consent (111.24) before uploading client data. Local processing largely removes the issue.

### Gaps
- No FTC-specific alert on IEEPA or tariff refund scams found. The FTC page that surfaced was unrelated (Publishers Clearing House, 2025).
- IOR-number format (EIN plus suffix) was not verified in this session because the search budget was exhausted.
- No published CBP guidance on third-party software handling of ACE report exports.

---

## 7. Distribution: who would use or pay, and who is already helping small importers?

### Takeaway
The realistic channels are:
- free use by small importers, reached through SBDCs, chambers and trade associations, all of which are already running refund webinars and FAQs;
- small and mid-size customs brokers, who can legally do the filing and need triage at volume;
- CPA firms, which are advising on refunds but defer filing to brokers.

Carriers, large brokers and law firms already sell paid filing help. A non-broker tool that charges importers directly runs into both the licensing and the scam-perception constraints.

### Cited Findings
**Public and nonprofit channels**
- An SBA.gov-listed webinar, "International Trade – IEEPA Tariff Refund Process, Eligibility, & General Updates," was hosted by NY SBDC with presenters from NY SBDC and MS SBDC. — [SBA.gov event 85092](https://www.sba.gov/event/85092)
- Other SBDC and small-business refund sessions appear in search results; I did not fetch them: [NYSBDC Learning Lab](https://nysbdc.org/learning-lab/ieepa-tariff-refund-process-eligibility-and-general-updates/), [CEI Maine](https://www.ceimaine.org/event/tariff-update-ieepa-refunds-maine-business-impacts-changes/), [Small Business LA](https://smallbizla.org/?p=386078), [NCBFAA listing of CBP small-business webinar](https://www.ncbfaa.org/event-details/2026/05/13/industry-events/cbp-webinar---ieepa-duty-refunds-for-small-businesses).
- Chambers have published FAQs and guides (search-result titles only): [Detroit Regional Chamber](https://www.detroitchamber.com/tariff-refunds-guide-and-faq/), [Pennsylvania Chamber on the U.S. Chamber "Tariff Refunds Guide"](https://www.pachamber.org/?p=26849). The U.S. Chamber asked Treasury for a channel to push reliable info to small importers through state and local chambers. — [U.S. Chamber](https://www.uschamber.com/international/letter-on-tariff-refunds)
- The Meng amendment, adopted unanimously in the House Appropriations Committee's FY2027 CJS bill, directs the Commerce Department to provide outreach and technical assistance to small businesses eligible for IEEPA refunds. Meng's release says "about a third of applicants have been denied their refunds due to technical errors" (a political claim I could not verify). — [Rep. Meng, May 21, 2026](https://meng.house.gov/media-center/press-releases/meng-advances-measure-help-small-businesses-access-tariff-refunds)

**Political pressure on small-business access**
- Rep. Krishnamoorthi (Apr 29, 2026) asked CBP to report refund distribution by business size, citing "website crashes, confusing interfaces, and delays." — [Krishnamoorthi](https://krishnamoorthi.house.gov/media/press-releases/krishnamoorthi-warns-cbp-tariff-refund-system-could-shut-out-small-businesses)
- Senators Markey and Wyden (June 10, 2026) also pressed CBP. — [Senate Small Business Committee](https://www.sbc.senate.gov/public/index.cfm/2026/6/ranking-members-markey-wyden-demand-complete-tariff-tax-refunds-for-small-businesses-condemn-trump-s-obstruction-of-the-refund-process)

**Commercial channels**
- **CPA firms.** CLA advises on accounting and tax for refunds (gain contingencies, COGS, taxable income) and tells importers to "work ... directly with their customs brokers" on claims. It does not claim to file. — [CLA](https://www.claconnect.com/en/resources/articles/26/tariff-refunds). UHY, Baker Tilly and BDO publish refund guidance aimed at middle-market clients. — [UHY](https://uhy-us.com/insights/news/2026/june/tariff-refunds-are-moving-what-importers-should-know-about-ace-access-timing-and-treasury-disbursements); [Baker Tilly](https://www.bakertilly.com/insights/how-to-use-ace-portal-reports-for-ieepa-tariff-refunds)
- **Brokers and carriers selling filing help:**
  - UPS CAPE Solution (fee-based) and UPS Trade Advisory ES003 review — [UPS](https://ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds)
  - DHL paperwork fee — [DHL](https://www.dhl.com/discover/en-us/global-logistics-advice/logistics-insights/navigating-us-trade-uncertainty/IEEPA-Trump-Tariff-Refunds)
  - Mohawk acting as 4811 designee with "administrative service fees" — [Mohawk](https://mohawkglobal.com/wp-content/uploads/2026/05/ACE-FAQs-Mohawk-Global.pdf)
  - Freight Right arguing brokers are "the better fit" — [Freight Right](https://www.freightright.com/news/why-customs-brokers-are-the-better-fit-for-ieepa-tariff-refunds)
- **Law firms.** Contingency-fee firms market protests and CIT suits. — [Ayar Law](https://ayarlaw.com/tariff-refund-resources/cbp-protest-tariff-refund)
- **Free calculators already exist.** Flexport's tariff refund tool is one; the existence of others is noted only, since teardowns are out of scope. — [Flexport](https://tariffs.flexport.com/refunds/help); [Alliance CHB ES003 guide for its IEEPA Refund Calculator](https://alliancechb.com/ES003_Guide.pdf)

### Inferences
- **Small brokers are the best paying channel, because they remove the licensing problem.** The licensed broker is the one conducting customs business; RefundRadar is its internal triage tool. Brokers also hold the clients' entry data and ACE linkages. Their pain is volume: many small clients and a rolling 80/180-day clock.
- **SBDCs, chambers and Commerce's possible Meng-amendment program are free-distribution partners, not buyers.** They need a neutral, non-filing, no-data-retention self-check tool they can recommend without endorsing a vendor. That fits the trust posture in Q6.
- **CPAs are a referral channel.** They see the refund in the books and need a schedule of expected refunds and interest by entry. RefundRadar's exports could double as that reconciliation schedule.
- **Charging small importers directly is the weakest model.** It is legally exposed, looks like the scams CBP warns about, and competes with free carrier, broker and Flexport tools.

### Gaps
- No evidence of any SBA or SBDC program that funds or endorses third-party refund software.
- No data on willingness to pay among small brokers or CPAs.
- Whether the Meng amendment became law, and with what funding, is unknown. It had only passed committee as of the source date.

---

## 8. Synthesis: implications for RefundRadar product scope

### Takeaway
Build RefundRadar as a free or flat-priced, local-processing, self-service triage and deadline tool for the importer of record (or its broker). It should read the importer's own ES-003 export, or 7501s with field-by-field user confirmation, and output an analysis, a deadline calendar, a blocker checklist and broker-ready prep packets. It should never present itself as filing, processing or obtaining refunds. The best-fit users are small importers with broker-filed formal entries under their own IOR number. Courier, DDP and postal users get only a routing decision tree.

### Cited Findings
These recommendations synthesize findings cited in sections 1–7:
- Refund filings are customs business; the exception is acting "solely on behalf of" oneself. — [19 USC 1641](https://www.law.cornell.edu/uscode/text/19/1641); [HQ 114199](https://open-gov.usebase.io/rulings/114199)
- OCR that determines filing data is customs business; 10-digit classification is too; entry-tied fees risk 111.36(b). — [HQ H350722](https://rulings.cbp.gov/api/getdoc/hq/2026/H350722.pdf)
- CBP fraud warning against third-party refund processors. — [CSMS 68569567 via C.H. Robinson](https://www.chrobinson.com/en-gb/resources/insights-and-advisories/client-advisories/2026q2/05-08-2026-client-advisory-cbp-issues-guidance-to-protect-against-ieepa-refund-fraud-activity/)
- Deadlines: Feb 4, 2027 CIT limitations ([Troutman](https://www.troutman.com/insights/to-sue-or-not-to-sue-that-is-the-question-for-ieepa-tariff-refunds/)); class certified Oct 8, 2026 ([DWT](https://www.dwt.com/insights/2026/10/cit-certifies-ieepa-duty-refund-importer-class)); 180-day protests ([19 CFR 174.12](https://www.law.cornell.edu/cfr/text/19/174.12)).

### Inferences: concrete product implications

**DO**
1. **Position and word the product as self-service.**
   - Example: "A self-check tool for importers of record reviewing their own entries. Not a customs broker or law firm. Does not file with CBP. Refund requests are filed only in ACE by you or your licensed customs broker."
   - Copy the Flexport and Tariffs API disclaimer patterns, plus CBP's own "only ACE is valid" line.
   - Call outputs "worksheet," "prep packet" or "checklist," never "your filing."
2. **Make ES-003 the primary input.** Parse by published header names (Entry Summary Number, Entry Date, Entry Summary Line Number, Tariff Ordinal Number, HTS Number - Full, Line Tariff Goods Value Amount, Line Tariff Duty Amount, Liquidation Date/Status). Filter 9903.01.xx and 9903.02.xx only, and do not sum value across overlay ordinals.
3. **Treat 7501 photos as a secondary, assistive path.**
   - OCR pre-fills a review grid; the user confirms each field.
   - Results are marked "estimate – confirm in ACE."
   - Read block 27/30 (current form) to answer "who was the IOR?" first.
4. **Make the deadline engine the core value.** Per entry, compute liquidation + 80 days (CAPE window), + 180 days (protest), and show the Feb 1–4, 2027 CIT decision point plus country-staggered dates. Show status relative to today and highlight entries about to fall out of a window.
5. **Run a blocker checklist:**
   - ACE importer sub-account exists and is linked to the 5106
   - 5106 POC email current
   - Refund ACH enrolled (separate from payment ACH)
   - 45-day login activity
   - Broker filed vs. self-filed (claim visibility)
   - Form 4811 designee
   - Show ACE setup lead time (about 1 day to 6 weeks).
6. **Use a pathway router with transparent rules:**
   - CAPE Phase 1/2
   - Protest (to a broker or attorney)
   - Finally liquidated: class member by default vs. individual CIT suit (to an attorney), with a "small claims may not justify suit cost" note
   - Carrier was IOR: carrier portal
   - Postal: no current path
   - Excluded: AD/CVD, drawback, recon
   Keep the rules in an editable config so they can change when the Federal Circuit rules or a class order issues.
7. **Use exports that hand off to professionals:**
   - Entry list and refund estimate for the broker
   - Protest-prep packet (entries, liquidation dates, IEEPA duty lines, deadline) for the broker or attorney
   - Expected-refund schedule for the CPA
8. **Process locally:** in the browser, no upload, no accounts, no retention. Optional IOR/EIN masking. A visible "we never ask for ACE passwords or bank details" statement.
9. **Pursue a broker mode as the commercial path.** Small brokers run it on client ES-003s, with a 111.24 consent reminder. The broker owns the customs business.

**DON'T**
1. Don't file, transmit to ACE, hold ACE credentials, or collect ACH or bank information.
2. Don't charge a percentage or contingency fee on refunds, especially one tied to broker-filed entries (111.36(b) risk and scam optics).
3. Don't give 8- or 10-digit HTS classifications or reclassification advice. They are not needed, and they are the clearest customs-business line in H350722.
4. Don't generate ready-to-sign Form 19 protests with legal argument, or CIT complaints. Hand off to a broker or attorney.
5. Don't market with "Get your refund," "Claim now" or urgency language, and don't do unsolicited outreach to importers using public import data. Those mirror CBP's fraud red flags.
6. Don't promise refunds on courier, DDP or postal entries, or on non-ACE or finally liquidated entries. Mark them "not reachable via CAPE today."

**Hackathon framing.** For the Oct 30 demo, show a real ES-003-shaped file and the deadline calendar ("N entries leave the CAPE window before Jan 31, 2027; Feb 4, 2027 CIT decision point"). The blocker checklist and the broker-ready packet are the most defensible and differentiated pieces. State openly that a commercial launch needs a customs-counsel opinion or a licensed-broker partner.

### Gaps
- No direct authority on whether software-generated CAPE entry lists, used by the importer itself, are customs business by the vendor. This is the central legal uncertainty, and only counsel or a CBP ruling request could settle it.
- The size of the reachable small-importer segment (formal entries, own IOR, still inside a CAPE or protest window) cannot be quantified from public data.
