"""Long-context probe for platform feedback: does Nemotron 3 Ultra on Token Factory find one fact in a long prompt?
Varies filler (repetitive vs varied), length and reasoning, with the fact at 10%, 50% and 90% depth.
Prints a markdown table. Costs roughly $1 of credits."""
from __future__ import annotations

import random
import time

from openai import OpenAI

from app.config import settings

ACTIONS = ["cleared", "held for exam", "released", "liquidated", "bonded", "re-weighed", "rerouted", "sampled"]
PORTS = ["Chicago", "Savannah", "Long Beach", "Newark", "Houston", "Seattle", "Miami", "Detroit"]


def filler(kind: str, n_lines: int, rng: random.Random) -> list[str]:
    if kind == "repetitive":
        return ["The quarterly shipment log entry was routine and contained no anomalies."] * n_lines
    return [f"Entry {rng.randint(100, 999)}-{rng.randint(1000000, 9999999)}-{rng.randint(0, 9)} at {rng.choice(PORTS)} was "
            f"{rng.choice(ACTIONS)} on day {rng.randint(1, 365)} with {rng.randint(1, 900)} cartons." for _ in range(n_lines)]


def main():
    c = OpenAI(base_url=settings.nebius_base_url, api_key=settings.nebius_api_key, timeout=600)
    try:
        meta = next(m for m in c.models.list().data if m.id == settings.ultra.model_id)
        print("model metadata:", {k: v for k, v in meta.model_dump().items() if k not in ("object",)})
    except Exception as e:  # noqa: BLE001
        print("model metadata unavailable:", e)
    rng = random.Random(7)
    needle = "Special instruction: the refund pathway for entry QQQ-7777777-1 is PHASE-TWO-BLUE."
    q = "\n\nQuestion: what is the refund pathway for entry QQQ-7777777-1? Answer with the pathway code only."
    rows = ["| filler | prompt tokens | depth | reasoning | found | answer (start) | seconds |", "| --- | --- | --- | --- | --- | --- | --- |"]
    plan = [("repetitive", 12000, d, False) for d in (0.1, 0.5, 0.9)] + [("repetitive", 12000, 0.5, True)] + \
           [("varied", 6500, d, False) for d in (0.1, 0.5, 0.9)] + [("varied", 6500, 0.5, True)] + \
           [("varied", 2500, 0.5, False), ("varied", 1000, 0.5, False)]
    for kind, n, depth, think in plan:
        lines = filler(kind, n, rng)
        lines.insert(int(len(lines) * depth), needle)
        try:
            t0 = time.perf_counter()
            r = c.chat.completions.create(model=settings.ultra.model_id, messages=[{"role": "user", "content": "\n".join(lines) + q}],
                                          max_tokens=2000 if think else 100, temperature=0,
                                          extra_body={"chat_template_kwargs": {"enable_thinking": think}})
            ans = (r.choices[0].message.content or "").strip().replace("\n", " ").replace("|", "/")
            rows.append(f"| {kind} | {r.usage.prompt_tokens:,} | {int(depth * 100)}% | {'on' if think else 'off'} | "
                        f"{'yes' if 'PHASE-TWO-BLUE' in ans else 'NO'} | {ans[:60]} | {time.perf_counter() - t0:.1f} |")
        except Exception as e:  # noqa: BLE001
            rows.append(f"| {kind} | ~{n} lines | {int(depth * 100)}% | {'on' if think else 'off'} | error | {str(e)[:60]} | |")
        print(rows[-1], flush=True)
    print("\n".join(rows))


if __name__ == "__main__":
    main()
