# RefundRadar benchmark results

Run 2026-10-27 01:27 UTC. Synthetic data only (invented importer, fake identifiers).

## 1. Routing 49 entries (stratified across all rule paths; run 2026-10-27 01:27 UTC)

| System | Right route | Right rule | Exact deadline | Time | Cost |
|---|---|---|---|---|---|
| Rule engine | 100% | 100% | 100% | 0.01s | $0.000 |
| Nemotron 3 Ultra (model only) | 86% | 84% | 26% | 357.61s | $0.498 |
| Nemotron 3.5 Lightning (model only) | 57% | 57% | 45% | 1930.83s | $0.124 |

## 2. Reading 30 photographed Form 7501s (Nemotron 3.5 Super VL)

| Field | Accuracy |
|---|---|
| entry_number | 57% |
| entry_type | 100% |
| entry_date | 100% |
| importer_number | 83% |
| chapter99_lines | 100% |
| ieepa_duty | 87% |
| total_duty | 100% |
| entry_number_after_check_digit | 80% |

`entry_number_after_check_digit`: when the reading fails the CBP check digit, code tries look-alike characters against the importer's known filer codes, then asks Super VL (reasoning on) to re-read Block 1 once. Entry numbers still wrong that fail validation, so the app flags them for review: 5/6.

All fields correct on 40% of photos; by photo quality (light/medium/heavy distortion): 0.2: 50%, 0.5: 50%, 0.9: 20%. Avg 11.71s per photo, total $0.052.

## 3. Offer check (20 offers: 10 scams, 10 legitimate)

Both rows use the same code rule for the verdict. The first adds Nemotron 3 Ultra: it reads the fee terms (percent, flat, per entry, minimum) to price the offer on your numbers, and proposes red flags that code keeps only if they quote the offer and match the flag's definition. The flag definitions and these 20 offers were written by the same author, so treat this as a sanity check, not field accuracy.

| Reader | Right verdict | Scams caught | Legitimate offers flagged as scams |
|---|---|---|---|
| Nemotron 3 Ultra reading + code rules | 100% | 10/10 | 0/10 |
| Keyword rules only (no model) | 95% | 10/10 | 0/10 |

Red-flag recall: 96%. Model-proposed flags rejected by code: 30. Errors: 0.

## 4. Cost and latency by model tier

| Tier | Model | Calls | Avg seconds | Avg tokens in/out | Cost |
|---|---|---|---|---|---|
| nano | nvidia/Nemotron-3_5-Lightning | 92 | 20.99 | 1801/5170 | $0.124 |
| super_vl | nvidia/Nemotron-3.5-Super-VL | 41 | 8.57 | 1614/864 | $0.052 |
| ultra | nvidia/Nemotron-3-Ultra-550b-a55b | 74 | 5.16 | 1394/1867 | $0.518 |
