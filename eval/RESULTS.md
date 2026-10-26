# RefundRadar benchmark results

Run 2026-10-26 18:57 UTC. Synthetic data only (invented importer, fake identifiers).

## 1. Routing 46 entries (stratified across all rule paths; run 2026-10-26 18:57 UTC)

| System | Right route | Right rule | Exact deadline | Time | Cost |
|---|---|---|---|---|---|
| Rule engine | 100% | 100% | 100% | 0.0s | $0.000 |
| Nemotron 3 Ultra (model only) | 89% | 89% | 26% | 272.83s | $0.342 |
| Nemotron 3 Nano (model only) | 87% | 85% | 48% | 323.07s | $0.026 |

## 2. Reading 30 photographed Form 7501s (Nemotron 3.5 Super VL)

| Field | Accuracy |
|---|---|
| entry_number | 63% |
| entry_type | 100% |
| entry_date | 70% |
| importer_number | 93% |
| chapter99_lines | 100% |
| ieepa_duty | 90% |
| total_duty | 100% |

All fields correct on 30% of photos; by photo quality (light/medium/heavy distortion): 0.2: 0%, 0.5: 40%, 0.9: 50%. Avg 1.82s per photo, total $0.023.

## 3. Offer check (20 offers: 10 scams, 10 legitimate)

Both rows use the same code rule for the verdict; they differ in who reads the offer.

| Reader | Right verdict | Scams caught | Legitimate offers flagged as scams |
|---|---|---|---|
| Nemotron 3 Ultra (flags must quote the offer) | 45% | 9/10 | 10/10 |
| Keyword rules only (no model) | 80% | 8/10 | 1/10 |

Red-flag recall (Ultra): 68%. Errors: 1.

## 4. Cost and latency by model tier

| Tier | Model | Calls | Avg seconds | Avg tokens in/out | Cost |
|---|---|---|---|---|---|
| nano | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B | 47 | 6.87 | 1800/1834 | $0.026 |
| super_vl | nvidia/Nemotron-3.5-Super-VL | 30 | 1.82 | 1607/308 | $0.023 |
| ultra | nvidia/Nemotron-3-Ultra-550b-a55b | 68 | 5.93 | 1306/1809 | $0.458 |
