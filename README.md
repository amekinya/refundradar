# RefundRadar

**Before you pay anyone to chase your tariff refund, RefundRadar tells you what you're owed, which entries are about to expire, what will block the money, and what it should cost to recover it.**

Built for the Nebius × NVIDIA Global AI Hackathon (Best Apps & Agents track) with NVIDIA Nemotron models on **Nebius Token Factory** and **Tavily**.

- Live demo: _link added at deploy_
- Demo video: _link added after recording_

> RefundRadar is a self-check tool for importers of record reviewing their own entries. It is not a customs broker or law firm and does not file with CBP. Refund requests are filed only in ACE, by the importer or its licensed customs broker. All demo data is synthetic.

---

## The problem

After the Supreme Court struck down the IEEPA tariffs on Feb 20, 2026, about **$166 billion** became refundable across **53 million entries** and **330,000+ importers**. CBP built a refund tool (CAPE) and opened it in phases. Big importers filed on day one. Small importers are being left behind:

- **Deadlines expire per entry.** An entry that liquidated more than **80 days** ago drops out of CAPE for good unless the importer is a court plaintiff. After 180 days, even a protest is too late.
- **Approved money gets stuck.** As of Oct 2, 2026, CBP was holding **20,362 approved refunds (~$1.1B)** because importers never added refund bank details in ACE.
- **Many don't hold the claim.** When a courier, forwarder or supplier was the importer of record, the refund belongs to them.
- **Help is expensive or predatory.** Broker minimums and contingency fees can take 30–68% of a small refund, and CBP has warned that outside parties offering to "process" refunds are likely fraudulent.

About 81% of refund *dollars* are already in process but only about 51% of *entries*: what's left is a long tail of small importers. Sources and the full research are in [`docs/`](docs/).

## What it does

Upload an **ACE ES-003 export** (or any broker spreadsheet) and/or **photos of Entry Summaries (CBP Form 7501)**, answer five questions, and get:

| Output | What it shows |
|---|---|
| **Verdict** | What you can claim now, and how much expires in the next 3 weeks |
| **Deadline radar** | Money leaving the CAPE window and protest windows, week by week, through the Feb 2027 court-filing decision point |
| **Where the money sits** | Every entry routed: file now · fix first · protest · ask your broker · waiting · blocked · court only · someone else holds the claim |
| **Your plan** | Dated steps, written by Nemotron 3 Ultra from the engine's numbers |
| **Blockers** | Refund bank details, ACE account, surety-paid entries, open protests, drawback, corrections, wrong-format entry numbers |
| **Photo review grid** | What Nemotron 3.5 Super VL read from each form, with "someone else is the importer of record" detection |
| **Cost to recover** | Net refund under self-filing, courier programs, flat-fee brokers, per-entry services and contingency firms |
| **Offer check** | Paste an offer: Nemotron 3 Ultra checks it against CBP's fraud warning and prices it on your numbers; Tavily looks the company up |
| **Broker handoff** | Pre-checked CAPE entry list, full worksheet, deadlines calendar (.ics) |

## How NVIDIA Nemotron and Nebius Token Factory are used

**Money, dates and routes never come from a model.** A tested rule engine (21 routing rules from CBP CSMS messages, CBP's CAPE guide, court orders and statutes, each tagged by confidence) does that. Models do the jobs code can't:

| Job | Model on Token Factory | Why this tier |
|---|---|---|
| Read photos of Form 7501 into a review grid (strict JSON schema) | **Nemotron 3.5 Super VL** | Vision + reliable structured output |
| Map an unfamiliar broker spreadsheet to our schema | **Nemotron 3 Nano** (reasoning off) | Fast, near-free, one call per file |
| Write the action plan over the whole ledger | **Nemotron 3 Ultra** (reasoning on) | Long context: all totals, blockers, deadlines and unusual entries plus the full rule set in one prompt |
| Explain an unusual entry in plain English | **Nemotron 3 Ultra** | Reasoning grounded in the rule text |
| Check a refund offer for red flags | **Nemotron 3 Ultra** + **Tavily search** | Reads persuasive letters; web evidence on the company |
| Rules freshness monitor | **Tavily search** → **Nemotron 3 Nano** | Daily check for CBP/court changes since the rules date |

Token Factory features used: OpenAI-compatible chat completions, strict JSON-schema output, per-request reasoning toggle (`chat_template_kwargs.enable_thinking`), usage accounting for per-step cost, and a daily spend cap. Rate limits and transient errors are retried, and a reply without valid JSON falls back to the rule-based output. Model IDs are configurable and verified live with `GET /v1/models` (see `scripts/smoke_test.py`).

The freshness check only sends Nemotron news published *after* the rules date; that date comparison is done in code, because Nano listed older articles as "new" when asked to do it. The public demo's sample importer replays recorded live model outputs ([`data/sample/demo_cache.json`](data/sample/demo_cache.json): 14 calls, about $0.04), so visitors don't spend credits; uploads of your own files run live.

## Design

- **The headline is a rounded range, not a false-precision number.** "About $145,300 to $146,800" (rounded to $100), because interest is an estimate and corporate interest rates differ.
- **Where the money sits** is a sorted bar chart with a three-group overview bar (refund-ready, needs action, not recoverable today): position and length are the most accurately read encodings (Cleveland & McGill 1984; Heer & Bostock 2010).
- **One alarm color.** Red only ever means money at risk: the HOLD banner, deadlines days away, money leaving the CAPE window, serious blockers, likely-scam offers. Everything else is blue and gray, so red keeps its meaning.
- Entry numbers are set in IBM Plex Mono so they're easy to read back to a broker. The pages pass an axe-core accessibility audit, including contrast and keyboard access to scrollable tables.

## Measured results

See [`eval/RESULTS.md`](eval/RESULTS.md) (generated by `python -m eval.run_eval` against live models):
1. **Routing accuracy**: rule engine vs. Nemotron models routing the same entries from the same written rules. Labels come from the scenario each synthetic entry was built from, not from the engine.
2. **Form reading accuracy**: Super VL on 30 synthetic "photographed" Form 7501s at three distortion levels.
3. **Offer check**: 20 synthetic offers (10 scams, 10 legitimate).
4. **Cost and latency per model tier.**

## Run it

```bash
pip install -r requirements.txt
export NEBIUS_API_KEY=...        # Nebius Token Factory
export TAVILY_API_KEY=...        # optional: offer check web lookup + rules freshness
uvicorn app.main:app --reload    # http://localhost:8000
```

Without keys the app still runs: the sample importer uses cached model outputs and every AI feature falls back to rule-based output, clearly labeled.

```bash
python -m pytest -q                  # rule engine tests
python -m scripts.smoke_test         # check model IDs, reasoning toggle, vision JSON, Tavily
python -m eval.run_eval              # benchmark (≈ $1 of credits)
python -m scripts.build_demo_cache   # refresh the sample importer's cached model outputs
python -m data.generate              # regenerate the synthetic importer + labels
python -m data.render_forms          # regenerate synthetic form photos + ground truth
```

Deploy: `Dockerfile` included (works on Render, Hugging Face Spaces, or any container host). Set `NEBIUS_API_KEY`, `TAVILY_API_KEY`, and optionally `DAILY_SPEND_CAP_USD` (default $2/day).

## Project layout

```
app/engine/   rule engine: catalog (rules + dates + sources), routing, interest, entry numbers, costs, ES-003 parser
app/ai/       Token Factory client (usage, spend cap, reasoning toggle) and the model tasks
app/static/   front end (vanilla HTML/CSS/JS)
data/         synthetic importer generator, form renderer, offers, sample files
eval/         benchmark harness and results
docs/         rules research (primary sources), competitor teardowns, complaint map, legal/market notes
```

## Limits and honesty

- Rules verified Oct 25, 2026; they're moving (CBP status report Oct 26, court conference Oct 27, class scheduling order Nov 5, Federal Circuit appeal pending). Rules live in `app/engine/catalog.py` so a change is a config edit.
- Interest is an estimate (CBP doesn't publish its day-count method); confirm in ACE reports ES-022 / REV-603.
- Liquidation dates read from photos are estimated until confirmed in ACE.
- Preparing refund filings *for someone else* is customs business requiring a broker license (19 U.S.C. 1641); RefundRadar is self-service and hands off to the importer's broker. A commercial launch would need a customs-counsel opinion or a licensed-broker partner.

## License

Apache 2.0
