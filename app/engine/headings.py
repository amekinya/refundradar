"""IEEPA Chapter 99 headings (HTS 2026 Rev. 21), grouped by program.

Only *dutiable* headings can carry refundable IEEPA duty. Exception headings mark exemptions.
The refund estimate always uses the duty actually paid on the line, never the heading's rate.
Source: docs/refund_rules_research.md §(e) (USITC HTS REST API, Rev. 21, Oct 9 2026).
"""
from __future__ import annotations

import re

_PROGRAMS: dict[str, str] = {}


def _add(program: str, *headings: str) -> None:
    for h in headings:
        _PROGRAMS[h] = program


# Fentanyl / trafficking tariffs
_add("Mexico (fentanyl/border)", "9903.01.01", "9903.01.05")
_add("Canada (fentanyl/border)", "9903.01.10", "9903.01.13", "9903.01.15", "9903.01.16")
_add("China/Hong Kong (fentanyl)", "9903.01.20", "9903.01.24")
# Reciprocal baseline + April 9, 2025 country rates
_add("Reciprocal baseline", "9903.01.25")
_add("Reciprocal (Apr 2025 country rate)", *[f"9903.01.{n}" for n in range(43, 77)])
# Reciprocal August 7, 2025 country rates (9903.02.19 is an exception; .20 is EU 15% all-in)
_add("Reciprocal (Aug 2025 country rate)", *[f"9903.02.{n:02d}" for n in range(2, 72) if n != 19])
# Trade-framework "15% all-in" headings
_add("Reciprocal (15% all-in deal)", "9903.02.73", "9903.02.80", "9903.02.83", "9903.02.88")
# Other IEEPA programs
_add("Transshipment", "9903.02.01")
_add("Brazil", "9903.01.77")
_add("India (Russian oil)", "9903.01.84")

DUTIABLE_IEEPA: frozenset[str] = frozenset(_PROGRAMS)

# Headings where only the portion above the general duty is IEEPA, so duty-on-the-line overstates the refund.
ALL_IN_15: frozenset[str] = frozenset({"9903.02.20", "9903.02.73", "9903.02.80", "9903.02.83", "9903.02.88"})

# Section 122 surcharge (Feb 24 - Jul 23, 2026): not IEEPA, not refundable via CAPE.
SECTION_122_PREFIX = "9903.03."

_NOT_IEEPA_PREFIXES = ("9903.80", "9903.81", "9903.82", "9903.83", "9903.84", "9903.85", "9903.88", "9903.03")


def normalize_hts(raw: str) -> str:
    """'9903010025' / '9903.01.25' / '9903.01.25.00' -> '9903.01.25' for Chapter 99; 10-digit dotted otherwise."""
    digits = re.sub(r"\D", "", str(raw or ""))
    if len(digits) < 8:
        return digits
    if digits.startswith("9903"):
        return f"{digits[0:4]}.{digits[4:6]}.{digits[6:8]}"
    d = digits.ljust(10, "0")[:10]
    return f"{d[0:4]}.{d[4:6]}.{d[6:10]}"


def program_of(hts: str) -> str | None:
    return _PROGRAMS.get(normalize_hts(hts))


def is_dutiable_ieepa(hts: str) -> bool:
    return normalize_hts(hts) in DUTIABLE_IEEPA


def is_section_122(hts: str) -> bool:
    return normalize_hts(hts).startswith(SECTION_122_PREFIX)


def is_chapter_99(hts: str) -> bool:
    return normalize_hts(hts).startswith("9903")
