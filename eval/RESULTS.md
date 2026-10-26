# RefundRadar benchmark results

Run 2026-10-26 18:22 UTC. Synthetic data only (invented importer, fake identifiers).

## 1. Routing 46 entries (stratified across all rule paths)

| System | Right route | Right rule | Exact deadline | Time | Cost |
|---|---|---|---|---|---|
| Rule engine | 100% | 100% | 100% | 0.01s | $0.000 |
| Nemotron 3 Ultra (model only) | 91% | 89% | 35% | 226.24s | $0.356 |
| Nemotron 3 Nano (model only) | 85% | 85% | 39% | 805.69s | $0.024 |

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

All fields correct on 30% of photos; by photo quality (light/medium/heavy distortion): 0.2: 0%, 0.5: 40%, 0.9: 50%. Avg 1.89s per photo, total $0.023.

## 3. Offer check (20 offers)

Verdict accuracy 10%; scams caught 1/10; legitimate offers wrongly flagged 8/10; red-flag recall 20%.

## 4. Cost and latency by model tier

| Tier | Model | Calls | Avg seconds | Avg tokens in/out | Cost |
|---|---|---|---|---|---|
| nano | nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B | 46 | 17.52 | 1799/1720 | $0.024 |
| super_vl | nvidia/Nemotron-3.5-Super-VL | 30 | 1.89 | 1607/308 | $0.023 |
| ultra | nvidia/Nemotron-3-Ultra-550b-a55b | 66 | 5.93 | 1317/2082 | $0.499 |
