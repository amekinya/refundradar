"""'Is it worth paying someone?' Net refund under common recovery options.

Fee models are archetypes built from prices providers published in 2026 (see docs/research/competitors.md).
Prices change and some are ambiguous (e.g., "per entry" vs "per declaration"), so the UI labels these as
examples to compare against a real quote, never as a quote.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from app.engine.catalog import MAX_ENTRIES_PER_DECLARATION


@dataclass
class Option:
    key: str
    label: str
    how: str
    fee: float
    net: float
    effective_pct: float
    caveat: str


def _opt(key, label, how, fee, refund, caveat) -> Option:
    fee = round(max(fee, 0.0), 2)
    net = round(refund - fee, 2)
    pct = round(100 * fee / refund, 1) if refund > 0 else 0.0
    return Option(key, label, how, fee, net, pct, caveat)


def compare(entries: int, refund: float) -> list[Option]:
    """`entries` = entries you'd file; `refund` = estimated refund (principal + interest) for them."""
    declarations = max(1, math.ceil(entries / MAX_ENTRIES_PER_DECLARATION))
    opts = [
        _opt("self", "File it yourself in ACE", "Free; needs an ACE account and refund bank details", 0.0, refund,
             "Budget a few hours. CBP says CAPE doesn't require a broker."),
        _opt("courier_entry", "Courier program (per entry)", "Example: $2.10 per entry", 2.10 * entries, refund,
             "Only for entries that courier brokered; you still need ACE + refund bank details."),
        _opt("courier_decl", "Courier program (per declaration)", "Example: $300 per declaration", 300.0 * declarations, refund,
             "Only for that courier's entries."),
        _opt("flat_broker", "Flat-fee broker",
             "Example: $200 + $125 per extra entry (under $5K), or $200 per entry + 4%",
             (200 + 125 * max(entries - 1, 0)) if refund < 5000 else (200 * entries + 0.04 * refund), refund,
             "Ambiguous whether 'per entry' means customs entry or declaration; this may overstate."),
        _opt("per_entry_service", "Per-entry prep service", "Example: $100 per entry", 100.0 * entries, refund,
             "Often includes extra checks (e.g., bank enrollment)."),
        _opt("pct_broker", "Percentage broker", "Example: 2% with a $10,000 minimum (capped at $100,000)",
             min(max(0.02 * refund, 10_000.0), 100_000.0), refund, "Minimums dominate small refunds."),
    ]
    for p in (10, 20, 30):
        opts.append(_opt(f"contingency_{p}", f"Contingency firm ({p}%)", f"{p}% of what's recovered", refund * p / 100, refund,
                         "Usually covers protests and litigation too."))
    return opts


def offer_cost(refund: float, *, percent: float | None = None, flat: float | None = None,
               per_entry: float | None = None, entries: int = 0, minimum: float | None = None) -> tuple[float, float]:
    """Cost of a specific offer the user received, and its effective percentage."""
    fee = 0.0
    if percent is not None:
        fee += refund * percent / 100
    if flat is not None:
        fee += flat
    if per_entry is not None:
        fee += per_entry * entries
    if minimum is not None:
        fee = max(fee, minimum)
    pct = round(100 * fee / refund, 1) if refund > 0 else 0.0
    return round(fee, 2), pct
