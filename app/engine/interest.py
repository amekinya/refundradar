"""Refund interest estimate under 19 U.S.C. 1505(c) / 19 CFR 24.36.

Interest runs from the deposit date to the liquidation/reliquidation date (not the payment date),
at the quarterly IRS overpayment rate, compounded daily (26 U.S.C. 6622). CBP doesn't publish its
day-count convention, so this is an estimate; validate against ACE report ES-022.
"""
from __future__ import annotations

from datetime import date, timedelta

# (year, quarter) -> (non-corporate, corporate) overpayment rate. CBP FR Doc. 2026-19292 [P].
RATES: dict[tuple[int, int], tuple[float, float]] = {
    (2025, 1): (0.07, 0.06),
    (2025, 2): (0.07, 0.06),
    (2025, 3): (0.07, 0.06),
    (2025, 4): (0.07, 0.06),
    (2026, 1): (0.07, 0.06),
    (2026, 2): (0.06, 0.05),
    (2026, 3): (0.07, 0.06),
    (2026, 4): (0.07, 0.06),
}
_FALLBACK = (0.07, 0.06)  # latest published rate, used for quarters beyond the table


def _rate(d: date, corporate: bool) -> float:
    q = (d.month - 1) // 3 + 1
    pair = RATES.get((d.year, q), _FALLBACK)
    return pair[1] if corporate else pair[0]


def _days_in_year(y: int) -> int:
    return 366 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 365


def estimate_interest(principal: float, start: date, end: date, *, corporate: bool = True) -> float:
    """Daily-compounded interest on `principal` for days in [start, end)."""
    if principal <= 0 or end <= start:
        return 0.0
    factor = 1.0
    d = start
    one = timedelta(days=1)
    while d < end:
        factor *= 1 + _rate(d, corporate) / _days_in_year(d.year)
        d += one
    return round(principal * (factor - 1), 2)
