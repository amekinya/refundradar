"""CBP entry numbers: normalization and the check digit from the CBP Form 7501 Instructions, Appendix 1."""
from __future__ import annotations

import re


def normalize(raw: str) -> str:
    """Strip dashes/spaces/punctuation and uppercase. CAPE strips special characters before validating."""
    return re.sub(r"[^0-9A-Za-z]", "", str(raw or "")).upper()


def display(entry: str) -> str:
    e = normalize(entry)
    return f"{e[:3]}-{e[3:10]}-{e[10:]}" if len(e) == 11 else e


def _char_value(c: str) -> int:
    if c.isdigit():
        return int(c)
    v = ord(c) - ord("A") + 1  # A=1 ... Z=26
    while v > 9:  # two-digit letter values reduce to the sum of their digits (R=18 -> 9)
        v = sum(int(d) for d in str(v))
    return v


def check_digit(first10: str) -> int:
    """Luhn-style: double every even-position digit (1-based), subtract 9 if > 9, sum, (10 - sum%10) % 10."""
    total = 0
    for pos, ch in enumerate(normalize(first10)[:10], start=1):
        v = _char_value(ch)
        if pos % 2 == 0:
            v *= 2
            if v > 9:
                v -= 9
        total += v
    return (10 - total % 10) % 10


def validate(raw: str) -> list[str]:
    """Return problems a CAPE upload would hit (errors) or that deserve a warning."""
    e = normalize(raw)
    problems: list[str] = []
    if len(e) != 11:
        problems.append("Entry number must be 11 characters without dashes")
        return problems
    if not e[3:].isdigit():
        problems.append("Characters 4-11 should be digits")
        return problems
    if check_digit(e[:10]) != int(e[10]):
        problems.append("Check digit doesn't match (warning only: some filers use an authorized check-digit factor)")
    return problems


# Characters a camera or a vision model confuses on printed forms.
_LOOKALIKE = {"0": "QOD", "Q": "0O", "O": "0Q", "D": "0", "2": "Z", "Z": "2", "1": "IL", "I": "1", "L": "1",
              "5": "S", "S": "5", "8": "B", "B": "8", "6": "G", "G": "6", "K": "M", "M": "K", "7": "T", "T": "7"}
_TO_DIGIT = {"O": "0", "Q": "0", "D": "0", "I": "1", "L": "1", "Z": "2", "S": "5", "B": "8", "G": "6"}


def repair(raw: str, known_filers: set[str] | frozenset[str] = frozenset()) -> tuple[str, bool]:
    """Fix a misread entry number using the check digit: try look-alike characters in the 3-character filer code
    (and letters read in the digit part). Accept a fix only if exactly one candidate passes the check digit, and
    (when the importer's other entries tell us its filer codes) that candidate uses a known filer code.
    Returns (entry number, changed). A dropped or extra digit can't be fixed; validate() still flags it for review."""
    from itertools import product

    e = normalize(raw)
    if len(e) != 11 or not validate(e):
        return e, False
    serial = "".join(_TO_DIGIT.get(c, c) for c in e[3:])
    if not serial.isdigit():
        return e, False
    cands = {"".join(f) + serial for f in product(*[[c, *_LOOKALIKE.get(c, "")] for c in e[:3]])}
    cands = {c for c in cands if check_digit(c[:10]) == int(c[10])}
    if known_filers:
        cands = {c for c in cands if c[:3] in known_filers}
    if len(cands) == 1:
        fixed = cands.pop()
        return fixed, fixed != e
    return e, False
