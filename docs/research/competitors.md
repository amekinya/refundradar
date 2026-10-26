# RefundRadar: Competitor Landscape for IEEPA Tariff Refund Recovery (2026)

Scope note: research done Oct 25, 2026. CBP rule mechanics are out of scope (another researcher covers them). Only the facts needed to position competitors are included. "EVIDENCE" means it is stated in a cited source. "INFERENCE" means it is my reasoning. Pages that could not be fetched are listed in the Gaps sections.

### Background facts checked (from the brief)
- **Supreme Court ruling of Feb 20, 2026 (Learning Resources v. Trump): CONFIRMED.** Sources: [Jet Worldwide timeline](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds); [Markey/Wyden letter to CBP, Jun 10, 2026](https://www.sbc.senate.gov/public/_cache/files/1/8/182e03a9-4e59-4a39-b8f7-da02c1373101/1EC4A5C7B75D3D0E88EB385BB6C2753390CAB8F2AC06CE9427C9996F564CB1D5.6.10.26-letter-to-cbp.pdf).
- **~$166B, ~53M entries, ~330K importers: CONFIRMED** by CBP official Brandon Lord's sworn declaration (executed Mar 6, 2026): 330,566 importers, 53,173,939 entries, about $166B as of Mar 4, 2026. Source: [CIT docket 19346, doc 31](https://storage.courtlistener.com/recap/gov.uscourts.cit.19346/gov.uscourts.cit.19346.31.0_2.pdf).
- **"Fewer than 10% enrolled for ACH": CONFIRMED, but the date is early March, not late March.**
  - The same declaration (¶22) says "only 21,423 entities (mostly importers or their customs brokers) have completed the set-up process." That is about 6.5% of 330,566, which is my own calculation ([declaration](https://storage.courtlistener.com/recap/gov.uscourts.cit.19346/gov.uscourts.cit.19346.31.0_2.pdf)).
  - [tariffstool.com](https://www.tariffstool.com/guides/ace-portal-account-setup-ieepa-refund) puts it at "fewer than 10%… as of early March 2026."
  - By Apr 14, 56,497 importers had enrolled ([eCommerce Fastlane](https://ecommercefastlane.com/tariff-refund-shopify-importers-cape-portal/)).
- **"7,700+ refunds failed": CONFIRMED, with a caveat.** Declaration ¶22 says that since Feb 6, 2026, CBP "has been unable to process 7,700 refunds for 2,897 importers" who had not finished electronic refund setup ([declaration](https://storage.courtlistener.com/recap/gov.uscourts.cit.19346/gov.uscourts.cit.19346.31.0_2.pdf)). These were refunds of all kinds that came before CAPE, not IEEPA refunds specifically.
  - Later counts of refunds held for missing ACH: 1,880 as of May 11 ([ST&R](https://www.strtrade.com/trade-news-resources/str-trade-report/trade-report/may/tariffs-today-cbp-reports-further-progress-on-cape-refund-process)), 9,837 in July ([A.N. Deringer](https://www.anderinger.com/ieepa-tariff-refund-update/); [Thomson Reuters](https://www.thomsonreuters.com/en-us/help/onesource-global-trade/regulatory-insights/2026/august-3rd/cit-signals-next-phase-ieepa-tariff-refund.html)), and about 20,184 refunds worth $1.3B by mid-September ([C.H. Robinson, Sep 17](https://www.chrobinson.com/en-au/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/)).
- **CAPE phase dates of Apr 20, Jun 29 and Oct 6, 2026: CONFIRMED.** Sources: [UPS](https://www.ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds); [C.H. Robinson](https://www.chrobinson.com/en-au/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/).

---

## Q1. Solution types and named players (with URLs and launch dates)

### Takeaway
The market has seven layers:
1. CBP's free but hard-to-use ACE/CAPE.
2. Carriers and couriers that file only for their own entries (cheap, but only for their own entries).
3. Customs brokers and forwarders. Most use free ES-003 "calculators" as lead magnets, then sell filing per entry, per declaration, or as a percentage.
4. Contingency recovery firms, law firms and lead-gen affiliates (about 10–30% of the refund).
5. Trade-compliance and AI software, mostly enterprise or audit-focused. One major suite, ONESOURCE, explicitly does not support CAPE.
6. Claim buyers and lenders aimed at large claims.
7. A thin layer of free nonprofit and government help.

I found no Shopify app, PayPal/Stripe product, Product Hunt launch or Show HN built for IEEPA refunds.

### Cited Findings

**A. CBP's own tools (free)**
- **Where filing happens.** IEEPA refund requests must go through the ACE Secure Data Portal as a CAPE Declaration, not through ABI ([C.H. Robinson summary of CSMS #68569567](https://www.chrobinson.com/en-gb/resources/insights-and-advisories/client-advisories/2026q2/05-08-2026-client-advisory-cbp-issues-guidance-to-protect-against-ieepa-refund-fraud-activity/); [UPS](https://www.ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds)).
- **How a declaration works.** It is a CSV of entries, up to 9,999 per declaration. ACE returns an error file when validation fails.
  - "Currently, third parties without original filing authority cannot submit CAPE declarations" ([UPS](https://www.ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds)).
  - An accepted declaration cannot be amended ([Freight Right](https://tariffs.freightright.com/); [eCommerce Fastlane](https://ecommercefastlane.com/tariff-refund-shopify-importers-cape-portal/)).
- **ACE reports.** ES-001, ES-002 and ES-003 are in the ACE "Public reports" folder and help identify affected entries ([Thomson Reuters ONESOURCE help](https://www.thomsonreuters.com/en-us/help/onesource-global-trade/supreme-court-ruling/2026/april-13th/updates-april-13-2026.html)).
  - SCORE also points small businesses to the REV-603 and REV-613 reports ([SCORE](https://www.score.org/articles/how-apply-small-business-tariff-refunds/)).
- **What CBP does not provide (EVIDENCE of friction).**
  - ACE account setup takes about 60 minutes. Duplicate tax ID errors can force a call to CBP, and one merchant reported 4 hours on hold ([eCommerce Fastlane, Apr 23](https://ecommercefastlane.com/tariff-refund-shopify-importers-cape-portal/)).
  - New ACE portal applications take "up to 30 days" ([tariffstool.com](https://www.tariffstool.com/guides/ace-portal-account-setup-ieepa-refund)). Inventory Hero estimates 6–8 weeks for first-time setup ([Inventory Hero, May 27](https://www.inventoryhero.ai/blog/how-to-get-trump-tariff-refund)).
  - Busy Baby (MN) could not file because its "tax ID was linked to someone else's account" ([CBS News, May 1](https://www.cbsnews.com/news/tariff-refund-portal-trump-cbp/)).
- **Rejection rate.** About 15% of early requests were rejected, mainly for incorrect information or ineligible payments. CBP had more than 75,000 requests as of Apr 26 ([CBS News](https://www.cbsnews.com/news/tariff-refund-portal-trump-cbp/)).
- **Scale and progress.**
  - Day one: more than 55,000 parties filed, covering over 4M imports ([Supply Chain Dive, Apr 21](https://supplychaindive.com/news/fedex-ups-and-dhl-detail-tariff-refund-approach-for-customers/818057/)).
  - Sep 17 update: about $134.7B accepted into CAPE, about $122B certified and sent to Treasury, about 27.2M entries, and more than 286,000 declarations ([C.H. Robinson](https://www.chrobinson.com/en-au/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/)).

**B. Carriers, couriers and marketplace brokers** (most relevant to small importers who used a courier as their broker)
- **UPS** ([page](https://www.ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds); [options PDF](https://assets.ups.com/adobe/assets/urn:aaid:aem:85ad65b1-e4ce-4ad0-8824-271159434c01/original/as/IEEPA-Refund-Process-Options.pdf)):
  - Where UPS was the importer of record (IOR), no action is needed.
  - Self-file option: free guidance plus an "IEEPA Refunds in ACE" training module.
  - **UPS CAPE Solution (Option A):** $300 per declaration for 0–5,000 entries and $500 for 5,001–9,900. It covers UPS-brokered entries only. Requires an active ACE importer account with ACH, a signed 2026 Pricing Schedule, and the ACE IEEPA report or authorization for UPS to run it.
  - **UPS Trade Advisory Services (Option B, multi-broker):** $500 minimum (covers 2 hours), then $250/hr. UPS reviews the ES-003 and returns a CAPE template, and the importer files it.
- **DHL Express:**
  - Filed automatically on day one for shipments where DHL was IOR.
  - Where DHL was only the broker, the IOR signs an authorization and intake form and uploads an Excel list of entries or AWBs. The fee is an **Import Documentation Fee of $2.10 per entry**.
  - The IOR must already have an active ACE account and an ACH Refund Account ([DHL form](https://mydhl.express.dhl/us/en/forms/ieepa-dhl-to-file.html); [Supply Chain Dive](https://supplychaindive.com/news/fedex-ups-and-dhl-detail-tariff-refund-approach-for-customers/818057/)).
- **FedEx:**
  - Files for customers where FedEx acted as customs broker and will pass refunds through. "Customers need not act" ([EcomCrew](https://www.ecomcrew.com/fedex-ups-and-dhl-are-filing-for-tariff-refunds-here-is-what-customers-can-expect/); [Supply Chain Dive](https://supplychaindive.com/news/fedex-ups-and-dhl-detail-tariff-refund-approach-for-customers/818057/)).
  - I found no public FedEx fee.
  - At least 17 lawsuits seek reimbursement of carrier fees, 11 of them against FedEx ([EcomCrew](https://www.ecomcrew.com/fedex-ups-and-dhl-are-filing-for-tariff-refunds-here-is-what-customers-can-expect/)).
- **Informal (courier) entries.** On FedEx, UPS and DHL informal entries the IOR is the ultimate consignee. As of late April, Phase 1 "does not currently address refunds on informal entries." Most small consignees never registered for ACH ([Jet Worldwide, updated Apr 23](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds)).
- **Amazon Customs and Trade.** It is the broker for Amazon Global Logistics (AGL) entries and offers a survey sellers can use to authorize CAPE filing on their behalf. AGL sellers remain the IOR ([Inventory Hero, May 27](https://www.inventoryhero.ai/blog/how-to-get-trump-tariff-refund)). No fee was found.
  - Amazon itself disclosed about $600–640M in IEEPA refunds ([Supply Chain Dive, Aug 7](https://www.supplychaindive.com/news/cbp-has-paid-100-billion-in-ieepa-tariff-refunds/827257/); [roic.ai](https://www.roic.ai/news/amazon-discloses-640-million-in-ieepa-tariff-refunds-in-q2-2026-filing-07-31-2026)).
- **Zonos (cross-border e-commerce).** No filing service. It says DDP sellers generally lack standing, and it filed an amicus brief on postal refunds ([Zonos](https://zonos.com/vi/ieepa-tariff-refunds-cape)).

**C. Customs brokers and forwarders (with free calculators as lead magnets)**
- **Flexport.**
  - Launched a public Tariff Refund Calculator around Jan 20, 2026, before the ruling ([FreightWaves](https://www.freightwaves.com/news/flexport-launches-tariff-refund-calculator-as-supreme-court-weighs-tariff-authority); [BusinessWire](https://www.businesswire.com/news/home/20260120812295/en/Flexport-Launches-Tariff-Refund-Calculator-Giving-Businesses-Early-Insight-Into-Possible-Tariff-Refunds)).
  - On Feb 26, 2026 it announced AI agents, including a free "Audit Your Customs Broker" agent (tariffs.flexport.com/audit) and an automated refund process ([BusinessWire](https://www.businesswire.com/news/home/20260226536552/en); [PYMNTS](https://pymnts.com/supply-chain/2026/flexport-debuts-ai-tool-to-streamline-tariff-refunds); [Bloomberg video](https://www.bloomberg.com/news/videos/2026-02-26/flexport-rolls-out-ai-agents-to-aid-with-tariff-refunds-video)).
  - Enrollment is free with "no commitment required." No filing fee is published ([flexport.com/refunds](https://www.flexport.com/refunds)).
- **Clearit USA.** Pricing published Apr 30, 2026 ([Clearit pricing](https://clearitusa.com/ieepa-refund-pricing-what-importers-need-to-know/)):
  - Recovery under $5,000: $200 for the first entry, then $125 per additional entry.
  - Recovery over $5,000: $200 per entry plus 4% of duties recovered.
  - It also reviews ACE rejection reports and resubmits ([Clearit](https://clearitusa.com/why-use-clearit-to-handle-your-ieepa-refund-filings/)).
- **KlearNow.** Pricing is per entry with no minimum ([KlearNow](https://klearnow.ai/ieepa-refunds/)):
  - **Starter:** $100 per entry. Includes ACE access and reports, ACH enrollment verification, CAPE prep and submission, and multi-broker consolidation.
  - **Full Service:** an extra $100 per entry. Adds PSC processing, CBP information requests and document ingestion.
  - **SaaS tier:** a 10–20% discount plus a "Refund Buy Back" program.
- **Alliance Customs House Brokers.** Free browser-based ES-003 calculator. The managed service costs **2% of the IEEPA refund (before interest), with a $10,000 minimum and $100,000 cap** ([Alliance](https://alliancechb.com/ieepa-refund-calculator/)).
- **Freight Right.** Free browser estimator that reads ES-003, CargoWise or custom CSV files and outputs a CAPE-ready CSV and interest. Filing is "No upfront fee. We collect when you collect" ([Freight Right](https://tariffs.freightright.com/)). Teardown in Q3.
- **UNIS / UNISCO.** Free ES-003 analyzer that flags 9903.01/02 lines and computes 180-day protest deadlines. Pricing by quote ([UNIS](https://www.unisco.com/ieepa-refund-calculator)).
- **JFS CHB (on the Item.com marketplace).** Similar ES-003 calculator, "free to start," then protest and refund filing ([Item marketplace](https://marketplace.item.com/ieepa-refund-calculator/)).
- **Gateway Lines.** Free estimator "powered by iSight," launched Feb 21, 2026. It offers AI document analysis of PDFs, scans, photos and broker invoices, limited to 3 free analyses a day ([Gateway Lines](https://gatewaylines.com/press-releases/gateway-lines-launches-ieepa-tariff-refund-estimator-powered-by-isight)). Teardown in Q3.
- **Kuehne+Nagel.** Entry identification, liquidation alerts, protest prep, ACE setup help and refund estimates. Line-level reporting is a "billable service" ([K+N, Apr 27](https://www.kuehne-nagel.com/how-to/customs-clearance/ieepa-tariffs)).
- **Others with only advisories found (no product or pricing):**
  - C.H. Robinson ([advisory](https://www.chrobinson.com/en-gb/resources/insights-and-advisories/client-advisories/2026q2/04-13-2026-client-advisory-cbp-announces-cape-tool-ieepa-duty-refund-claims/))
  - Expeditors ([newsflash](https://info.expeditors.com/newsflash/cbp-to-deploy-phase-1-of-cape-for-ieepa-refunds))
  - Livingston ([article](https://www.livingstonintl.com/the-new-ieepa-duty-refund-process/))
  - DHL Global Forwarding ([guide](https://www.dhl.com/discover/en-us/global-logistics-advice/logistics-insights/navigating-us-trade-uncertainty/IEEPA-Trump-Tariff-Refunds))
  - JAS ([campaign page](https://www.jas.com/campaigns/ieepa-tariff-refund-support/))
  - ShipMonk ([guide](https://www.shipmonk.com/resources/content-hub/ieepa-tariff-refund-guide-2026))
  - FlavorCloud ([blog](https://flavorcloud.com/blog/ieepa-tariff-refunds-and-cape-declarations-what-importers-need-to-know-in-2026))
  - Western Overseas ([FAQ](https://www.westernoverseas.com/cape-system-faq-ieepa-refunds/))
  - GHY ([post](https://www.ghy.com/trade-compliance/cape-and-ieepa-refunds-what-we-know-ahead-of-april-20/))
- **Small independent broker (anecdote).** One quoted "my minimum fee for a CAPE submission is $750." Broker CAPE fees range "from several hundred to several thousand dollars" ([The Financial Wire, May 12](https://thefinancialwire.com/fedex-and-walmart-filed-for-tariff-refunds-on-day-one-small-businesses-say-the-cape-portal-requires-a-customs-broker-or-lawyer-just-to-navigate/)).

**D. Contingency recovery firms, law firms and lead-gen affiliates**
- **Leyton.** Success-based with "no upfront professional fees." No percentage published. Does a six-step pathway assessment including PSC versus protest, and says it works alongside brokers ([Leyton](https://leyton.com/us/ieepa-customs-tariff-refund/)).
- **Ayar Law.** Pure contingency with no percentage published. Free evaluation including interest. Uses CAPE, protest and CIT litigation ([Ayar Law](https://ayarlaw.com/tariff-refund-attorney)).
- **Tariff Refund Project (Grayhawk Law, Matthew Seligman).**
  - Contingency, with the percentage set by pathway: CAPE is cheapest, protest and litigation cost more.
  - Fee is discounted 25% if the CAPE filing is not made within 24 hours of signing and receiving ACE access.
  - Targets small and mid-sized importers ([tariffrefundproject.com](https://www.tariffrefundproject.com/)). The exact percentages are not in the fetched text.
- **Tariff Refund HQ (AAZ Consulting Group, Miami).** Sliding contingency that falls as recovery grows. No minimum entry size. Triages entries into CAPE, protest, drawback or legal review. Says it is "not a law firm" ([tariffrefundhq.com](https://www.tariffrefundhq.com/)).
- **ieepatariffrecovery.org.** Anonymous affiliate site that refers to partners charging "typically 15–30% of the recovered amount." Its buttons lead to hub.opscaleexchange.com ([site](https://www.ieepatariffrecovery.org/guides/ieepa-tariff-refunds)).
- **tariffrefundcredits.com.** Lead-gen site whose broker partners charge 10–20% contingency. It contrasts this with hourly law firms at $500–1,500/hr ([pricing](https://tariffrefundcredits.com/pricing)).
- **tariffstool.com (run by Master Plan Bookkeeping).** Free estimator. Funnels to tariffrecoverytoday.com for "no recovery no fee" CAPE filing ([tariffstool](https://www.tariffstool.com/guides/ace-portal-account-setup-ieepa-refund)).
- **GingerControl.** Free ES-003 estimator. "Sorts each entry by refund route and deadline, closest deadline first." GingerControl prepares the file and a licensed partner files it ([GingerControl service](https://gingercontrol.com/services/ieepa-refund); [guide, May 3 / upd. Oct 12](https://gingercontrol.com/blog/ieepa-tariff-refund-guide)). Teardown in Q3.
- **Capital Gurus "IEEPA Recovery."** Exists at [ieepa.capitalgurus.com](https://ieepa.capitalgurus.com/), but the page was not fetchable (robots).
- **DeMar Consulting Group.** A finance-side "Tariff Refund Readiness Review" that publishes a CAPE rejection checklist for small importers ([DeMar, May 5](https://demarconsultinggroup.com/insights/cape-rejection-errors-small-importer-checklist/)).
- **Big law and Big 4 (enterprise).**
  - Troutman's IEEPA refund practice ([overview PDF, Oct 2026](https://www.troutman.com/wp-content/uploads/2026/10/Troutman-IEEPA-Tariff-Refund-Practice-Overview-October-2026.pdf))
  - McCune Wright ([page](https://mccunewright.com/practice-areas/commercial-litigation/the-ieepa-tariff-ruling-and-your-business))
  - Quinn Emanuel ([alert](https://news.quinnemanuel.com/l/865552/2026-02-21/qqbxgl))
  - KPMG ([PDF](https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2026/IEEPA-refunds-cape.pdf)), RSM ([insight](https://rsmus.com/insights/services/business-tax/tariffs-refund-portal.html)), BDO and Aprio advisories

**E. Software (trade compliance, AI and calculators)**
- **Thomson Reuters ONESOURCE Global Trade.** Explicitly: "Our OSGT software products do not support CAPE filings or IEEPA refund requests" ([TR help, Apr 13](https://www.thomsonreuters.com/en-us/help/onesource-global-trade/supreme-court-ruling/2026/april-13th/updates-april-13-2026.html)).
- **Gaia Dynamics.** Tariff Audits Engine launched Mar 3, 2026, for existing customers. Claims analysis of "thousands or millions of entries within minutes." Founded 2025 with Andrew Ng's AI Fund ([press release](https://markets.chroniclejournal.com/chroniclejournal/article/prunderground-2026-3-3-gaia-dynamics-launches-tariff-audit-engine-to-help-importers-unlock-refund-opportunities-after-supreme-court-ieepa-decision)).
- **Reform (YC-backed freight automation).** Tariff refund calculator, Mar 2, 2026. Takes spreadsheets, PDFs or XML and outputs line-by-line estimates ready for PSC, protest or legal follow-up. Pricing not disclosed ([Reform](https://reformhq.com/blog/turn-the-tariff-ruling-into-recoverable-cash-introducing-reforms-tariff-refund-calculator)).
- **Wove.** Upload HTS, country of origin, value and date, and it reconstructs refundable IEEPA duty and the "right recovery mechanism for each" entry ([Wove](https://tariffs.wove.com/refunds)).
- **Tandom.** Tariff calculator that "splits the per-line duty stack by authority," plus an AD/CVD catalog ([Tandom](https://tandom.ai/resources/how-to-file-ieepa-tariff-refund-cape-2026)).
- **TariffLens.** HTS classification AI. Has a blog on refunds but no dedicated refund product ([TariffLens](https://www.tarifflens.ai/blog/how-to-calculate-ieepa-tariff-refund)).
- **Tarifflo (YC S26, Provo UT).** AI classification and entry filing. "AuditLive" files refunds via PSC and protest. Claims $1.3M recovered for one importer ([yespress](https://yespress.io/tarifflo-yc-s26.md)).
- **Pax AI (YC S24).** "TurboTax for import duty drawback." $4.5M seed led by Initialized (Apr 2025). Targets SMBs. Drawback, not CAPE ([YC](https://www.ycombinator.com/launches/LXv-pax-ai-turbotax-for-import-duty-rebate); [Techleap](https://finder.techleap.nl/news/feed/pax-ai-raises-4-5m-for-import-tax-ai)).
- **Zollback.** AI duty drawback platform; announced its "full commercial launch" Mar 13, 2026. Tiered contingency (percentages not stated). Does not mention CAPE or IEEPA ([Zollback](https://www.zollback.com/blog/tariff-refunds-for-smbs)). Treat its claims with caution because they are self-reported.
- **"IEEPA Duty Refund Assistant" Chrome extension.** Scans entries while logged into ACE and exports a CSV. Had 3 users and no reviews as of its Mar 18, 2026 update. The publisher names do not match ([Chrome Web Store](https://chromewebstore.google.com/detail/mcmgmmbonflhikmfeghclplagfkcihbc)).
- **Avalara.** Explainer blog only; no refund product found ([Avalara](https://www.avalara.com/us/en/blog/how-to-request-tariff-refunds.html)).
- **Inventory Hero.** Educational guide plus landed-cost calculators; no refund filing ([Inventory Hero](https://www.inventoryhero.ai/blog/how-to-get-trump-tariff-refund)).
- **Beancount.io.** Guide and tracker suggestions only ([Beancount](https://beancount.io/blog/2026/08/06/tariff-refunds-importer-of-record-cape-portal-small-business-guide)).

**F. Claim buyers and lenders ("refund advance")**
- **Outpost Capital Partners.** Buys refund proceeds directly.
- **Asset Enhancement Solutions.** Arranges loans with a $10M minimum loan and a $20M minimum backing claim.
- **Pricing.** A $500K claim sold for roughly 55–75 cents on the dollar (Reuters, Apr 2, 2026, via [Yahoo Finance](https://finance.yahoo.com/economy/policy/articles/tariff-struck-companies-exploring-loans-100227788.html)).
- **Later resale rates.** Ranged "as low as 30 percent, all the way up to 90 percent" ([Holland & Knight / Inside U.S. Trade, Aug 13](https://www.hklaw.com/en/news/intheheadlines/2026/08/tariff-litigation-boosts-novel-market-for-importers-refund-rights)).
- **Before the ruling.** Jefferies and Oppenheimer brokered deals at 20–40 cents ([Peacock Tariff Consulting, Nov 2025](https://www.peacocktariffconsulting.com/tariff-refund-gold-rush-how-wall-street-is-monetizing-trade-law-uncertainty/)).
- **KlearNow "Refund Buy Back."** Immediate cash; terms not published ([KlearNow](https://klearnow.ai/ieepa-refunds/)).

**G. Free, nonprofit and government help**
- **SCORE.** Mentor guidance plus a fraud warning ([SCORE](https://www.score.org/articles/how-apply-small-business-tariff-refunds/)).
- **Project TERRA (Liberty Justice Center).** Helps small businesses map entries ([SelfEmployed, May 29](https://www.selfemployed.com/news/tariff-refund-small-business-importer-of-record-2026/)). Details not verified.
- **Congressional office pages.** Example: [Rep. Gonzalez](https://gonzalez.house.gov/services/tariff-refund-information).
- **SBA.** Named as a partner CBP has not engaged ([The Financial Wire](https://thefinancialwire.com/fedex-and-walmart-filed-for-tariff-refunds-on-day-one-small-businesses-say-the-cape-portal-requires-a-customs-broker-or-lawyer-just-to-navigate/)).

### Inferences
- **The default funnel** is a free ES-003 calculator, then a broker conversation, then a fee. At least 8 brokers and consultants run this playbook: Flexport, Freight Right, UNIS, JFS, Alliance, GingerControl, Gateway Lines and tariffstool. "Free calculator" is a commodity. RefundRadar cannot win on that alone.
- **The cheapest legitimate filers are the couriers** (DHL $2.10/entry; UPS $300 per declaration). They only cover their own brokered entries, and they require the importer to already have an ACE account and ACH. Those are exactly the blockers small importers lack.
- **No incumbent suite fills the gap.** ONESOURCE explicitly does not do CAPE. I found no evidence that Descartes, e2open, SAP GTS, Magaya, Customs City or iCustoms ship a refund module (absence of evidence, not proof).

### Gaps
- I found no IEEPA refund pages or pricing for: Customs City, Pacific Customs Brokers, USA Customs Clearance, DSV, Expeditors, C.H. Robinson, Livingston, Descartes, e2open, SAP GTS, Magaya, iCustoms, Customs Navigator.
- No FedEx fee page for CAPE filing was found.
- No Shopify App Store app, PayPal/Stripe/fintech product, Product Hunt launch or "Show HN" post specific to IEEPA refunds was found. Searches returned only news coverage.
- Reddit was not reachable through search.
- Exact contingency percentages for Grayhawk/Tariff Refund Project, Leyton, Ayar, TariffRefundHQ and Zollback are not published or were not in the fetched text.
- Not fetched:
  - Capital Gurus (robots disallowed)
  - GingerControl's Spanish page (site error; the English page worked)
  - tariffs.flexport.com/refunds (JavaScript loader only)
  - The yespress Tarifflo HTML (the .md version worked)

---

## Q2. For each player: what it does, size target, pricing, data intake, coverage, prominence, complaints

### Takeaway
Coverage of the full chain is fragmented:
- Calculators read the ES-003 but rarely compute interest, and almost never check ACH, ACE or IOR blockers.
- Broker services cover CAPE filing, but usually Phase 1 only, and often only for their own entries.
- Contingency firms cover all pathways (CAPE, protest, CIT), but charge 10–30%.
- Only KlearNow (paid, per entry) explicitly verifies ACH enrollment.
- Only Freight Right (free estimator) outputs both a CAPE-ready CSV and interest.

### Cited Findings (comparison matrix; ✓ = stated on source, ✗ = stated not offered, ? = not stated)

| Player | Target | Price model | Data intake | Pathway sort | Protest deadlines | Interest | ACH/ACE blocker check | Files CAPE |
|---|---|---|---|---|---|---|---|---|
| CBP ACE/CAPE | All IORs | Free | IOR uploads CSV | ✗ | ✗ | CBP computes | Holds refund if missing | IOR/broker self-files |
| UPS CAPE Solution | UPS-brokered | $300–500 per declaration; TAS $500 min + $250/hr | ACE IEEPA report or UPS runs it | Phase 1/2/3 eligibility | ? | ? | Requires ACH; "supports ACH rejection resolution" | ✓ (UPS entries) |
| DHL Express | DHL-brokered | $2.10/entry | Excel of entries/AWBs | ? | ? | ? | Requires ACE + ACH already | ✓ |
| FedEx | FedEx-brokered | ? | Automatic | ? | ? | ? | ? | ✓ |
| Clearit | ? | $200 + $125/entry (<$5K); $200/entry + 4% (>$5K) | ACE history review | Phase 1 | Mentions 180-day | ? | ? | ✓ |
| KlearNow | Any; no minimum | $100/entry (+$100 full) | ES-003, ES-701, ES-010, PDFs, emails | Phase 1 + 80-day window; PSC | ✗ (no protest service stated) | ✗ | ✓ ACH verified per IOR | ✓ |
| Alliance CHB | ? | 2%; $10K min; $100K cap | ES-003 upload (browser) | ✗ (estimate ignores liquidation) | ✗ | ✗ | ✗ | ✓ (managed) |
| Freight Right | Any (free tool) | "We collect when you collect" (% not stated) | ES-003, CargoWise, custom CSV (in browser) | Eligibility + readiness | Mentions | ✓ 7% simple | ACH noted | ✓ Phase 1 |
| UNIS / JFS CHB | Any | Quote / "free to start" | ES-003 (in browser) | Tariff-type flags | ✓ 180-day calc | ✗ | ✗ | Protests (UNIS doesn't mention CAPE) |
| Gateway Lines | Any | Free (3 AI analyses a day) | PDFs, scans, **photos**, broker invoices | Liquidation status "where available" | ✓ where available | ? | ? | ✗ (not a broker) |
| GingerControl | "U.S. importers" | ? | ES-003 (browser); ERP/spreadsheet on call | ✓ CAPE / Form 19 protest / court | ✓ | ? | ✗ | Partner files |
| Grayhawk / TRP | Small and mid-size | Contingency, tiered by pathway | Entry data + shared ACE access | ✓ CAPE / protest / litigation | ✓ | ? | Helps open ACE | ✓ |
| Leyton | IORs, incl. missing records | Success-based | 7501s, ACE access, ACH | ✓ incl. PSC | ✓ | "plus interest" | Helps ACE access | Prepares/supports |
| TariffRefundHQ | Single to multi-entry | Sliding contingency, no min | 7501s, invoices, ERP | ✓ CAPE / protest / drawback | ✓ | ? | ? | Via brokers |
| Reform / Wove / Tandom | Importers and brokers | ? | Spreadsheet/PDF/XML; HTS+COO+value | "Recovery mechanism" (Wove) | ? | ? | ? | ✗ |
| Gaia Dynamics | Existing enterprise customers | ? | Historical entries | ? | ? | ? | ? | ✗ |

Sources for the rows:
- [UPS](https://assets.ups.com/adobe/assets/urn:aaid:aem:85ad65b1-e4ce-4ad0-8824-271159434c01/original/as/IEEPA-Refund-Process-Options.pdf)
- [DHL](https://mydhl.express.dhl/us/en/forms/ieepa-dhl-to-file.html)
- [FedEx via Supply Chain Dive](https://supplychaindive.com/news/fedex-ups-and-dhl-detail-tariff-refund-approach-for-customers/818057/)
- [Clearit](https://clearitusa.com/ieepa-refund-pricing-what-importers-need-to-know/)
- [KlearNow](https://klearnow.ai/ieepa-refunds/)
- [Alliance](https://alliancechb.com/ieepa-refund-calculator/)
- [Freight Right](https://tariffs.freightright.com/)
- [UNIS](https://www.unisco.com/ieepa-refund-calculator)
- [JFS/Item](https://marketplace.item.com/ieepa-refund-calculator/)
- [Gateway Lines](https://gatewaylines.com/press-releases/gateway-lines-launches-ieepa-tariff-refund-estimator-powered-by-isight)
- [GingerControl](https://gingercontrol.com/services/ieepa-refund)
- [Grayhawk/TRP](https://www.tariffrefundproject.com/)
- [Leyton](https://leyton.com/us/ieepa-customs-tariff-refund/)
- [TariffRefundHQ](https://www.tariffrefundhq.com/)
- [Reform](https://reformhq.com/blog/turn-the-tariff-ruling-into-recoverable-cash-introducing-reforms-tariff-refund-calculator)
- [Wove](https://tariffs.wove.com/refunds)
- [Gaia](https://markets.chroniclejournal.com/chroniclejournal/article/prunderground-2026-3-3-gaia-dynamics-launches-tariff-audit-engine-to-help-importers-unlock-refund-opportunities-after-supreme-court-ieepa-decision)

**Prominence and press (EVIDENCE)**
- **Flexport** has the most press: FreightWaves, BusinessWire, PYMNTS, Bloomberg video and STAT Times. It also claims "$700M in tariff refunds claimed… over the last 5 years," a historical figure that is not IEEPA-specific ([flexport.com/refunds](https://www.flexport.com/refunds)).
- **The carriers' approach** was covered by Supply Chain Dive, EcomCrew and WSB-TV ([WSB-TV](https://www.wsbtv.com/news/local/atlanta/3-delivery-companies-say-theyll-try-get-you-refund-tariff-price-increases/XA6NYO2OCBGPNC2FUUJ4OGH46E/)).
- **Grayhawk's Seligman** was quoted in Fortune ([Fortune, Apr 20](https://fortune.com/2026/04/20/cape-tariff-refund-portal-small-business-challenges/)).

**Complaints and limitations (EVIDENCE)**
- The carrier fee lawsuits: 17, of which 11 are against FedEx ([EcomCrew](https://www.ecomcrew.com/fedex-ups-and-dhl-are-filing-for-tariff-refunds-here-is-what-customers-can-expect/)).
- "For some UPS imports, the details of the entry are not always provided" ([Jet Worldwide](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds)).
- A Texas retailer using UPS and DHL as IOR must wait for the carriers to pass funds through, with "no guaranteed payout yet" ([EcomCrew](https://www.ecomcrew.com/fedex-ups-and-dhl-are-filing-for-tariff-refunds-here-is-what-customers-can-expect/)).
- Broker queues are "taking weeks," with smaller merchants waiting behind larger importers ([eCommerce Fastlane](https://ecommercefastlane.com/tariff-refund-shopify-importers-cape-portal/)).
- Freight Right's page displayed an "Internal mode · gate bypassed" banner when fetched. This suggests the gated content may be exposed, which is a quality signal ([Freight Right](https://tariffs.freightright.com/)).

### Inferences
- **Data intake converges on ES-003.** That creates a chicken-and-egg problem: you need an ACE account to export ES-003, and lacking one is the main small-importer blocker.
- **Gateway Lines is the only tool found that accepts photos of paperwork.** It uses that capability to estimate, not to sort pathways or prepare filings.
- **Interest is the least-covered output.** Only Freight Right computes it (7% simple). Others ignore it (Alliance explicitly) or mention it vaguely (Leyton, Ayar).
- **Sources disagree on the interest rate.** SCORE says 6% ([SCORE](https://www.score.org/articles/how-apply-small-business-tariff-refunds/)) and Freight Right uses 7%. The rate varies by quarter, so RefundRadar should compute it per quarter. The other researcher should confirm the method.

### Gaps
- I found no user reviews (Trustpilot, G2, Reddit) for any refund-specific provider. These services are 6 months old or less.
- I found no turnaround SLAs from brokers except vague claims ("days," KlearNow; "1–2 business days" to respond, Alliance).

---

## Q3. Deep teardowns of the closest 4–6 offerings

### Takeaway
The closest analogs are:
- **Freight Right** (in-browser ES-003 to CAPE CSV with interest)
- **GingerControl** (route and deadline sorting, "we prepare, partner files")
- **Gateway Lines** (photo/PDF AI extraction)
- **KlearNow** (per-entry service with ACH verification)
- **Carrier programs** (UPS, DHL), which are the realistic path for courier-brokered small importers
- **Grayhawk's Tariff Refund Project**, the contingency archetype that targets small and mid-size importers

None combines photo/7501 intake, full pathway sorting (CAPE phases, PSC, protest, not eligible), interest, and blocker checks in a free, transparent product.

### Cited Findings

**1. Freight Right estimator** ([tariffs.freightright.com](https://tariffs.freightright.com/)): closest functional match
- **Onboarding.** Upload an ACE ES-003 export, a CargoWise customs declaration export, or a custom Excel/CSV. Column mapping and templates are provided. Files are "parsed in the browser and not uploaded."
- **Outputs.**
  - Entries grouped by eligibility, duty, interest and "refund readiness."
  - A per-entry filing list, an HTS summary, and a CAPE-ready CSV.
  - "Full entry and code details are locked behind a broker conversation."
- **Interest.** 7% simple annual. The page itself admits CBP compounds daily under 19 USC §1505(c), so actual refunds are "typically slightly higher… by less than 1%."
- **Pathways.** CAPE Phase 1 filing end-to-end by a licensed broker. Protests (§1514, within 180 days) and CIT suits are mentioned only as "discuss with broker."
- **ACH.** Notes refunds are held if ACH is missing, but no check is offered.
- **Price.** "No upfront fee. We collect when you collect" (percentage not published).
- **Limitations (INFERENCE):**
  - Requires ES-003, so it is useless without an ACE account.
  - No photo/7501 intake.
  - No PSC or Phase 2/3 sorting.
  - Gated details push the user into a sales funnel.

**2. GingerControl IEEPA refund service** ([service](https://gingercontrol.com/services/ieepa-refund); [guide](https://gingercontrol.com/blog/ieepa-tariff-refund-guide)): closest positioning match
- **Flow.** Three steps: read the IEEPA lines, sort each entry by route, file in deadline order through a partner. It explains how to pull the ES-003 from ACE Reports.
- **Tools.** The calculator reads the ES-003 in the browser. GingerControl "does not connect to ACE." There is also a 30-minute intro call that accepts an ERP export, spreadsheet or email.
- **Outputs.**
  - Each entry is sorted into CAPE Phase 1, a Form 19 protest, or the court route, with its protest deadline, "closest deadline first."
  - GingerControl prepares a refund file entry by entry.
  - The pages do not mention CAPE CSVs, protest drafts or interest.
- **Who files.** A "licensed IEEPA refund partner." GingerControl is "not a customs broker."
- **Disclaimers and price.** "Refund amounts and CBP acceptance are never guaranteed." Pricing is not published.
- **Limitations (INFERENCE):**
  - Opaque pricing.
  - ES-003 only.
  - No ACH or IOR blocker checks found.
  - It is RefundRadar's most direct conceptual competitor ("prepares; partner files"), so RefundRadar's differentiation must be transparency, photo intake, blocker checks and broader pathways (PSC, Phase 2/3).

**3. Gateway Lines IEEPA Tariff Refund Estimator (powered by iSight)** ([press release, Feb 21, 2026](https://gatewaylines.com/press-releases/gateway-lines-launches-ieepa-tariff-refund-estimator-powered-by-isight)): closest input match
- **Two modes.**
  - "Quick Estimate" (country plus customs value plus number of entries, no account).
  - "AI Document Analysis": upload PDFs, scanned images, photos or broker invoices. It extracts HTS, country of origin, Chapter 99 codes, and liquidation status and protest deadlines "where available." It separates IEEPA duty from Section 301/232, AD/CVD and fees, and gives a total and breakdown.
- **Claim.** A test sample entry produced a $64,940 estimate.
- **Price.** Free, limited to 3 AI analyses a day. No follow-on service described. "Not a law firm, customs broker, or tax advisor."
- **Limitations (INFERENCE):**
  - Estimate only.
  - The 3-a-day cap makes it impractical for 20–2,000 entries.
  - Launched before CAPE existed, so pathway logic for the CAPE phases is likely absent. It was not verified whether it has been updated.

**4. KlearNow IEEPA Refunds** ([klearnow.ai/ieepa-refunds](https://klearnow.ai/ieepa-refunds/)): closest "full prep including blockers" paid service
- **Flow.** Three steps: know your data (ES-003, ES-701, ES-010, so you "see what CBP sees"), fix housekeeping (Section 232 splits, PSCs), then submit the CAPE Declaration.
- **Intake.** "No special format or integration": PDFs, emails, invoices, ACE exports, broker records.
- **Outputs.**
  - A tariff-stacking review and identification of missing or incorrect Chapter 99 lines.
  - Phase 1 eligibility, including entries nearing the 80-day window.
  - A CAPE CSV, with the submission guided through the ACE portal "including the legal acknowledgment checkbox."
  - Acceptance confirmation and status monitoring.
- **Blocker check.** "Verifies ACH enrollment for each IOR before submission." It also consolidates multiple brokers into one submission.
- **Pricing.** $100 per entry (Starter) plus $100 per entry (Full Service: PSC, CBP information requests, recalculation). Broker fees are passed through. No minimum.
- **Limitations (INFERENCE):**
  - Per-entry pricing scales badly for courier-heavy importers with many low-duty entries. For example, 500 entries cost $50K, likely more than the refund.
  - No protest service.
  - No interest calculation.

**5. Carrier programs: UPS and DHL** (the default path for courier-brokered small importers)
- **UPS:**
  - Three options: self-serve with training; the CAPE Solution at $300 per declaration (≤5,000 entries); Trade Advisory multi-broker data prep at $500 minimum + $250/hr.
  - Requirements: active ACE importer account with ACH, a signed pricing schedule, and the ACE IEEPA report.
  - Timeline: CBP estimates 60–90 days after acceptance, and some refunds come only at liquidation ([UPS](https://www.ups.com/us/en/supplychain/logistics-solutions/customs-brokerage/us-customs-tariff-refunds); [PDF](https://assets.ups.com/adobe/assets/urn:aaid:aem:85ad65b1-e4ce-4ad0-8824-271159434c01/original/as/IEEPA-Refund-Process-Options.pdf)).
- **DHL:**
  - Authorization and intake form: legal name, EIN, address, confirmation of an active ACE account and ACH Refund Account, a signatory certification, and an Excel list of entries or AWBs.
  - Fee: $2.10 per entry. "Not responsible for CBP processing timelines or claim outcomes" ([DHL](https://mydhl.express.dhl/us/en/forms/ieepa-dhl-to-file.html)).
- **Limitations (EVIDENCE + INFERENCE):**
  - Both require the importer to already have ACE and ACH, the documented small-importer blockers.
  - Neither helps with non-carrier entries, protests or interest.
  - Informal entries were outside Phase 1 as of April ([Jet Worldwide](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds)).

**6. Tariff Refund Project (Grayhawk Law)** ([tariffrefundproject.com](https://www.tariffrefundproject.com/)): contingency archetype aimed at small and mid-size importers
- **Flow.** Free refund analysis from shared entry data, then pricing and an engagement letter, then CAPE filing, then ACH collection, then evaluation of non-CAPE entries, then protests or litigation.
- **Inputs.** Entry data, an ACE account (they explain how to open one), and "shared access to your ACE account."
- **Price.** Contingency only, tiered by pathway. A 25% fee discount if they miss filing within 24 hours of receiving ACE access.
- **Credibility claim.** Seligman was counsel on a Supreme Court brief.
- **Rationale for professional help.** "CBP's portal rejects an entire filing if a single entry contains an error."
- **Limitations (INFERENCE):**
  - The percentages are not published.
  - It needs ACE account sharing, which conflicts with the instinct CBP's fraud guidance builds against sharing credentials (see Q5).

**Also notable (shorter):**
- **Alliance CHB.** Free calculator with a questionnaire on protests, reconciliation, drawback and PSCs. The estimate "ignores liquidation status, PSC eligibility, protest deadlines, drawback claimed, and interest." Service fee: 2% with a $10K minimum and $100K cap ([Alliance](https://alliancechb.com/ieepa-refund-calculator/)).
- **UNIS.** Sample-data demo mode. A no-file form asks for EIN, line counts and estimated exposure. Computes 180-day protest deadlines ([UNIS](https://www.unisco.com/ieepa-refund-calculator)).

### Inferences
- **The best ideas are already split across products:**
  - in-browser processing (Freight Right, UNIS, Alliance, GingerControl)
  - CAPE CSV output (Freight Right, KlearNow)
  - photo/PDF AI extraction (Gateway Lines)
  - route and deadline sorting (GingerControl, TariffRefundHQ, Leyton)
  - ACH verification (KlearNow)

  RefundRadar's pitch is to unify them, free and transparently, with blocker diagnosis first.
- **No competitor publicly computes "is it worth paying someone?"** That would mean comparing the net refund across self-file (free), courier ($2.10/entry or $300/declaration), flat broker fees and contingency. This is an open positioning angle.

### Gaps
- No public screenshots or demo videos were reviewed. Flexport's page has a demo video, but it was not viewable through fetch.
- GingerControl's and Freight Right's filing fee percentages are unknown.
- Gateway Lines' tool was not checked for post-CAPE updates.

---

## Q4. Gaps for small importers (20–2,000 entries/year, no trade staff, possibly courier-brokered)

### Takeaway
Small importers are poorly served in five ways:
1. **Account access.** Every tool assumes an ACE account and ES-003, and setup takes 30 days or more with ID errors.
2. **Fee floors.** Minimums ($750 per filing, Alliance's $10K minimum, per-entry fees) eat small refunds.
3. **IOR confusion** with couriers, forwarders and DDP.
4. **Fragmented pathways.** Free tools mostly stop at Phase 1 or a 180-day protest flag.
5. **Trust.** A sea of look-alike "recovery" sites.

I found no free, self-serve, transparent tool that sorts all pathways, computes interest, checks blockers and prepares filings.

### Cited Findings
- **Fee floors (EVIDENCE):**
  - Broker minimum of $750 per CAPE submission. One client was seeking about $1,100. For refunds of $1,000–3,000, "fees can consume much of the recovery or exceed it" ([The Financial Wire, May 12](https://thefinancialwire.com/fedex-and-walmart-filed-for-tariff-refunds-on-day-one-small-businesses-say-the-cape-portal-requires-a-customs-broker-or-lawyer-just-to-navigate/)).
  - Alliance: 2% with a $10,000 minimum ([Alliance](https://alliancechb.com/ieepa-refund-calculator/)).
  - KlearNow: $100–200 per entry ([KlearNow](https://klearnow.ai/ieepa-refunds/)).
  - Clearit: $200 + $125 per extra entry, or $200 per entry + 4% ([Clearit](https://clearitusa.com/ieepa-refund-pricing-what-importers-need-to-know/)).
  - Contingency partners at 10–30% ([tariffrefundcredits](https://tariffrefundcredits.com/pricing); [ieepatariffrecovery.org](https://www.ieepatariffrecovery.org/guides/ieepa-tariff-refunds)).
  - Pax (drawback context): "Customs brokers take 10-20% of refunds and refuse claims under $100k" ([YC](https://www.ycombinator.com/launches/LXv-pax-ai-turbotax-for-import-duty-rebate)).
- **Confusion and knowledge gap (EVIDENCE):**
  - A North Carolina furniture importer paid about $14,000 in IEEPA duties, spent about 2 hours looking for the right module, and had not filed.
  - A broker said 2 of 3 small clients "did not know what an entry summary number was," and that the CAPE guide "reads like it was written for someone who already files 500 entries a month."
  - Some importers give up after learning they need ABI access or a broker ([The Financial Wire](https://thefinancialwire.com/fedex-and-walmart-filed-for-tariff-refunds-on-day-one-small-businesses-say-the-cape-portal-requires-a-customs-broker-or-lawyer-just-to-navigate/)).
- **IOR lockout (EVIDENCE):**
  - Forwarder or supplier as IOR means "the refund legally belongs to the forwarder," with no federal pass-through mechanism ([SelfEmployed, May 29](https://www.selfemployed.com/news/tariff-refund-small-business-importer-of-record-2026/)).
  - Affected groups include forwarder users, wholesale buyers, 3PL marketplace sellers, drop-shippers ([Beancount, Aug 6](https://beancount.io/blog/2026/08/06/tariff-refunds-importer-of-record-cape-portal-small-business-guide)) and DDP sellers ([Zonos](https://zonos.com/vi/ieepa-tariff-refunds-cape)).
- **ACE and ACH blockers (EVIDENCE):**
  - About 6.5% had finished electronic refund setup in early March ([CBP declaration](https://storage.courtlistener.com/recap/gov.uscourts.cit.19346/gov.uscourts.cit.19346.31.0_2.pdf)).
  - About 20,184 refunds ($1.3B) were held for missing ACH by mid-September ([C.H. Robinson](https://www.chrobinson.com/en-au/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/)).
  - Small consignees "never registered for ACH because they did not expect to be the IOR" ([Jet Worldwide](https://www.jetworldwide.com/blog/ieepa-fedex-ups-dhl-refunds)).
  - Offset risk: CBP may apply refunds to unpaid debts ([Beancount](https://beancount.io/blog/2026/08/06/tariff-refunds-importer-of-record-cape-portal-small-business-guide); [DeMar](https://demarconsultinggroup.com/insights/cape-rejection-errors-small-importer-checklist/)).
- **Rejection risk (EVIDENCE):**
  - Common errors: missing IEEPA HTS line, liquidation outside the window, reconciliation flag, entry already on an accepted declaration, open protest or drawback, incomplete ACH, entry-number typos, duplicates ([DeMar](https://demarconsultinggroup.com/insights/cape-rejection-errors-small-importer-checklist/)).
  - About 15% rejected early ([CBS](https://www.cbsnews.com/news/tariff-refund-portal-trump-cbp/)).
- **Financial stakes (EVIDENCE):**
  - Small businesses paid an average of $306,000 in tariffs (Center for American Progress, via [Fortune](https://fortune.com/2026/04/20/cape-tariff-refund-portal-small-business-challenges/)).
  - Some owners took second mortgages (same source).
  - Busy Baby expects about $50K ([CBS](https://www.cbsnews.com/news/tariff-refund-portal-trump-cbp/)).
  - Interest accrues at about $650M a month industry-wide ([SCORE](https://www.score.org/articles/how-apply-small-business-tariff-refunds/)).
- **Senators' view.** Small businesses "often lack trade counsel" and cannot wait months ([Markey/Wyden letter, Jun 10](https://www.sbc.senate.gov/public/_cache/files/1/8/182e03a9-4e59-4a39-b8f7-da02c1373101/1EC4A5C7B75D3D0E88EB385BB6C2753390CAB8F2AC06CE9427C9996F564CB1D5.6.10.26-letter-to-cbp.pdf)).
- **Claim sales are not built for small claims.**
  - Lenders want a $10M minimum loan or a $20M claim ([Reuters via Yahoo](https://finance.yahoo.com/economy/policy/articles/tariff-struck-companies-exploring-loans-100227788.html)).
  - Sale prices of 30–90 cents give up a large share of the refund ([H&K](https://www.hklaw.com/en/news/intheheadlines/2026/08/tariff-litigation-boosts-novel-market-for-importers-refund-rights)).

### Inferences
**Effective fee rates, computed from published prices:**
- **Alliance:** a $10K minimum on a $20K refund is a 50% effective fee; on $50K, 20%. Only above $500K does it reach its 2% headline rate.
- **Clearit:** 10 entries with a $4K refund cost $200 + 9×$125 = $1,325, about 33%. 50 entries with a $40K refund cost 50×$200 + 4%×$40K = $11,600, about 29%. It is ambiguous whether "per entry" means per customs entry or per declaration, so these numbers may overstate.
- **KlearNow:** 200 entries with a $30K refund cost $20,000, about 67%. 20 entries with a $14K refund cost $2,000, about 14%.
- **Broker $750 minimum:** on $1,100 that is about 68%. On the NC importer's $14K, about 5%, which is affordable, yet she still did not file. So confusion, not only price, blocks people.
- **Contingency 15–30%:** on a $50K refund, $7.5K–15K.
- **Carriers (cheapest):** DHL at $2.10/entry is about $420 for 200 entries. UPS is $300 per declaration. Both cover only their own brokered entries and require ACE+ACH up front.

**Unserved needs RefundRadar can target:**
- **(a) Works before ACE exists.** Accept 7501 photos, PDFs and courier duty invoices (Gateway Lines is the only photo tool, capped at 3 a day). Produce an "ACE + ACH setup checklist" as step 1.
- **(b) IOR detection.** Read the IOR field and broker or filer code on each 7501 and route the entry: "you file," "UPS/DHL/FedEx files – use form X," "your forwarder holds the claim – send this letter."
- **(c) A full pathway sort,** covering Phase 1, Phase 2 (reconciliation), Phase 3 (CIT/finally liquidated), PSC (unliquidated), protest (within 180 days), and not eligible. Most free tools stop at Phase 1 plus a 180-day flag.
- **(d) Correct interest,** computed per quarter. Competitors use flat 7% or ignore interest.
- **(e) A "cost to recover" comparison** that shows the net refund under self-file, courier, flat broker and contingency.
- **(f) Pre-validation of the CAPE CSV** against known rejection causes, because "one bad line" can sink a declaration.

**A free, self-serve, transparent end-to-end tool does not appear to exist.** Free tools are estimators that funnel into sales and hide details behind a broker (Freight Right gates "full entry and code details").

### Gaps
- No data on the distribution of refund sizes among small importers (for example, the median refund for importers with fewer than 100 entries).
- No data on what share of small importers used couriers as broker versus a traditional broker.
- No user-reported reviews of specific paid services to quantify dissatisfaction.

---

## Q5. Refund scams and warnings (relevant to trust design)

### Takeaway
CBP issued a formal fraud warning (CSMS #68569567, May 7, 2026). It says any external website or unknown party offering to process refunds is "likely fraudulent," and that CBP never asks for bank data, SSNs or passwords by email or text. Law firms and brokers have echoed it. Many look-alike, anonymous "recovery" sites exist. RefundRadar's trust design should therefore be local-first, never request ACE credentials or bank details, never file, and clearly say it is unaffiliated with CBP.

### Cited Findings
- **CBP CSMS #68569567 (May 7, 2026).**
  - Red flags: requests for company, personal or banking information; offers to secure refunds on your behalf; unsolicited contact; urgency; poor grammar or suspicious links.
  - "Any external website or unknown party offering to process refunds is likely fraudulent."
  - Verify @cbp.dhs.gov senders. Scheduled ACE reports come only from the listed sender and only when a user requested them.
  - Report to CBP or the DHS OIG hotline ([C.H. Robinson summary](https://www.chrobinson.com/en-gb/resources/insights-and-advisories/client-advisories/2026q2/05-08-2026-client-advisory-cbp-issues-guidance-to-protect-against-ieepa-refund-fraud-activity/); [MICA CSMS archive PDF](https://micausa.org/sites/default/files/content-files/Past%20Alerts/2026%20May%20CSMS.pdf)).
- **Parker Poe (Jun 17, 2026).** Unsolicited letters and emails reference specific import activity with "a significant level of detail" and push recipients to call a number, visit a site or scan a QR code. Red flags include requests for ACE credentials, banking information or passwords, and fake "CAPE refund report" emails ([Parker Poe](https://www.parkerpoe.com/news/2026/06/importers-should-exercise-caution-regarding-unsolicited-ieepa-tariff)).
- **Broker echoes.**
  - Expeditors: "CBP Published Best Practices for Protecting IEEPA Refund Data" ([Expeditors](https://info.expeditors.com/newsflash/cbp-published-best-practices-for-protecting-ieepa-refund-data)).
  - A.N. Deringer: "Protect your IEEPA refund" and "Don't Fall for Fraudulent Schemes" ([Deringer alerts](https://tradealerts.anderinger.com/protect-your-ieepa-refund); [Deringer](https://www.anderinger.com/?p=6181)).
- **SCORE.** "Any time the government announces a large payment program, fraud follows." CBP "will never contact you by phone asking for bank details upfront." Work only with licensed brokers ([SCORE](https://www.score.org/articles/how-apply-small-business-tariff-refunds/)).
- **Look-alike affiliate risk (EVIDENCE of pattern, not of fraud).** ieepatariffrecovery.org:
  - Is anonymous ("Editorial Team").
  - Uses dense, government-style content.
  - Does not clearly disclose that it is unaffiliated with CBP.
  - Earns undisclosed referral fees through hub.opscaleexchange.com, uses urgency framing, and cites figures without sources ([site](https://www.ieepatariffrecovery.org/guides/ieepa-tariff-refunds)).
- **Browser-extension risk.** The ACE-scanning Chrome extension's "Offered by" name and developer field do not match ([Chrome Web Store](https://chromewebstore.google.com/detail/mcmgmmbonflhikmfeghclplagfkcihbc)).
- **Legitimate firms that still ask for access.** Grayhawk/TRP requests "shared access to your ACE account" ([TRP](https://www.tariffrefundproject.com/)). DHL collects EIN and an authorization ([DHL](https://mydhl.express.dhl/us/en/forms/ieepa-dhl-to-file.html)). These are legitimate patterns, but they look a lot like the scam warning signs.
- **The FTC.** I found no FTC-specific IEEPA refund warning in these searches.

### Inferences
- **Trust-design requirements for RefundRadar:**
  - Process files locally or in the browser (competitors already market "parsed in your browser").
  - Never ask for ACE credentials, bank account numbers or SSNs.
  - Never send unsolicited outreach.
  - Show a permanent "not CBP, not a broker, does not file" banner.
  - Link only to cbp.gov/ACE for filing.
  - Include a "how to verify a CBP email" helper.
  - Publish the calculation method (interest formula, pathway rules) so it can be audited.
- **A "scam check" feature could set RefundRadar apart.** The user pastes an offer or email, and RefundRadar checks it against CBP's red-flag list and fee benchmarks from Q4. No competitor offers this.

### Gaps
- No FTC consumer alert was found specific to IEEPA refunds; it may exist, but none appeared in these searches.
- No count of reported fraud incidents or losses was found. CBP's notice describes increased risk, not specific cases.
- The full text of CSMS #68569567 was read only through secondary summaries (C.H. Robinson). The MICA PDF archive was listed but not fetched.
