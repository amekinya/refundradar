# RefundRadar benchmark results

Run 2026-10-26 19:07 UTC. Synthetic data only (invented importer, fake identifiers).

## 1. Routing 46 entries (stratified across all rule paths; run 2026-10-26 18:57 UTC)

| System | Right route | Right rule | Exact deadline | Time | Cost |
|---|---|---|---|---|---|
| Rule engine | 100% | 100% | 100% | 0.0s | $0.000 |
| Nemotron 3 Ultra (model only) | 89% | 89% | 26% | 272.83s | $0.342 |
| Nemotron 3 Nano (model only) | 87% | 85% | 48% | 323.07s | $0.026 |

## 2. Reading 30 photographed Form 7501s (Nemotron 3.5 Super VL)

| Field | Accuracy |
|---|---|
| entry_number | 67% |
| entry_type | 100% |
| entry_date | 100% |
| importer_number | 83% |
| chapter99_lines | 100% |
| ieepa_duty | 90% |
| total_duty | 100% |
| entry_number_after_check_digit | 83% |

`entry_number_after_check_digit`: when the reading fails the CBP check digit, code tries look-alike characters against the importer's known filer codes, then asks Super VL (reasoning on) to re-read Block 1 once. Entry numbers still wrong that fail validation, so the app flags them for review: 4/5.

All fields correct on 50% of photos; by photo quality (light/medium/heavy distortion): 0.2: 50%, 0.5: 50%, 0.9: 50%. Avg 2.78s per photo, total $0.035.

## 3. Offer check (20 offers: 10 scams, 10 legitimate)

Both rows use the same code rule for the verdict. The first adds Nemotron 3 Ultra: it reads the fee terms (percent, flat, per entry, minimum) to price the offer on your numbers, and proposes red flags that code keeps only if they quote the offer and match the flag's definition. The flag definitions and these 20 offers were written by the same author, so treat this as a sanity check, not field accuracy.

| Reader | Right verdict | Scams caught | Legitimate offers flagged as scams |
|---|---|---|---|
| Nemotron 3 Ultra reading + code rules | 100% | 10/10 | 0/10 |
| Keyword rules only (no model) | 95% | 10/10 | 0/10 |

Red-flag recall: 96%. Model-proposed flags rejected by code: 29. Errors: 0.

## 4. Cost and latency by model tier

| Tier | Model | Calls | Avg seconds | Avg tokens in/out | Cost |
|---|---|---|---|---|---|
| nano | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B | 47 | 6.87 | 1800/1834 | $0.026 |
| super_vl | nvidia/Nemotron-3.5-Super-VL | 36 | 2.32 | 1638/523 | $0.035 |
| ultra | nvidia/Nemotron-3-Ultra-550b-a55b | 46 | 5.93 | 1799/1875 | $0.342 |
