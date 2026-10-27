"""Parse an ACE ES-003 'Entry Summary Line Tariff Details' export (or a broker spreadsheet) into entries.

Column names follow the published ES-003 headers (Flexport/Gaia/GingerControl docs). Optional extra
columns (protest, drawback, surety, importer number...) are accepted so a broker or the user can add
status the ES-003 doesn't carry. Unknown headers can be mapped by the model layer (Nemotron 3.5 Lightning)
and passed in as `header_map`.
"""
from __future__ import annotations

import csv
import io
import re
from datetime import date, datetime, timedelta

from app.engine import entry_number as EN
from app.engine.models import Entry, Line

# canonical field -> accepted header spellings (lowercased, punctuation-insensitive)
CANON: dict[str, tuple[str, ...]] = {
    "entry_number": ("entry summary number", "entry number", "entry no", "entry"),
    "entry_date": ("entry date",),
    "entry_type": ("entry type code", "entry type"),
    "line_no": ("entry summary line number", "line number", "line no"),
    "ordinal": ("tariff ordinal number", "ordinal"),
    "hts": ("hts number full", "hts number", "htsus number", "hts", "tariff number"),
    "value": ("line tariff goods value amount", "entered value", "value"),
    "duty": ("line tariff duty amount", "duty amount", "duty"),
    "liquidation_date": ("liquidation date",),
    "liquidation_status": ("liquidation status",),
    "country_of_origin": ("country of origin code", "country of origin"),
    "importer_number": ("importer number", "importer of record number", "ior number"),
    "importer_name": ("importer of record name", "importer name", "ior name"),
    "deposit_date": ("deposit date", "payment date", "statement payment date"),
    "protest_status": ("protest status",),
    "protest_solely_ieepa": ("protest solely ieepa",),
    "drawback": ("drawback", "drawback designated"),
    "recon_flag": ("recon flag", "reconciliation flag"),
    "recon_09_filed": ("recon 09 filed", "reconciliation entry filed"),
    "surety_paid": ("surety paid", "surety paid ieepa"),
    "suspension_record": ("suspension record",),
    "ad_cvd": ("ad cvd", "adcvd", "ad/cvd"),
    "on_cape_declaration": ("on cape declaration", "cape filed"),
    "needs_psc": ("needs psc",),
}
REQUIRED = ("entry_number", "hts", "duty")
DATE_FIELDS = ("entry_date", "liquidation_date", "deposit_date")


def _key(h: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]", " ", (h or "").lower())).strip()


_LOOKUP = {_key(alias): k for k, als in CANON.items() for alias in als}


def auto_map(headers: list[str]) -> dict[str, str]:
    """header -> canonical field for every header we recognize."""
    out = {}
    for h in headers:
        k = _key(h)
        if k in _LOOKUP:
            out[h] = _LOOKUP[k]
    return out


def missing_required(mapping: dict[str, str]) -> list[str]:
    have = set(mapping.values())
    return [f for f in REQUIRED if f not in have]


# A trailing time of day ("2025-03-01 00:00:00" from pandas, "3/1/2025 0:00" from Excel, "2025-03-01T00:00:00Z").
_TIME = re.compile(r"[ T]\d{1,2}:\d{2}(?::\d{2}(?:\.\d+)?)?\s*(?:[AaPp]\.?[Mm]\.?)?\s*(?:Z|[+-]\d{2}:?\d{2}|UTC|GMT)?$")
_DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y%m%d", "%d-%b-%Y", "%d-%b-%y", "%b %d, %Y", "%B %d, %Y",
                 "%d %b %Y", "%d %B %Y", "%Y/%m/%d", "%m-%d-%Y", "%m-%d-%y", "%m.%d.%Y")


def parse_date(s: str) -> date | None:
    """US-order dates in the formats ACE, Excel, pandas and brokers write, with or without a time of day.
    Returns None if blank or unreadable; parse_csv records unreadable non-blank values so they're never silently lost."""
    s = (s or "").strip()
    if not s:
        return None
    core = _TIME.sub("", s).strip() or s
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(core, fmt).date()
        except ValueError:
            continue
    if core.isdigit() and len(core) == 5 and 36526 <= int(core) <= 54789:  # an Excel serial day number (2000-2049)
        return date(1899, 12, 30) + timedelta(days=int(core))
    return None


def parse_money_or_none(s: str) -> float | None:
    """'$1,234.50', '1234.5', 'USD 500', '(12.00)' -> number; blank -> 0.0; anything else -> None."""
    s = re.sub(r"(?i)^(?:US\$|USD|\$)|USD$|[\s,$]", "", (s or "").strip())
    if not s:
        return 0.0
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def parse_money(s: str) -> float:
    v = parse_money_or_none(s)
    return 0.0 if v is None else v


def _bool(s: str) -> bool:
    return (s or "").strip().lower() in {"y", "yes", "true", "1", "x"}


def parse_csv(text: str, header_map: dict[str, str] | None = None) -> tuple[list[Entry], dict]:
    """Returns (entries, info). info has the mapping used and any problems."""
    reader = csv.DictReader(io.StringIO(text.lstrip("﻿")))
    headers = reader.fieldnames or []
    mapping = auto_map(headers)
    if header_map:
        mapping.update({h: f for h, f in header_map.items() if h in headers and f in CANON})
    info = {"headers": headers, "mapping": mapping, "missing": missing_required(mapping), "rows": 0}
    if info["missing"]:
        return [], info

    inv: dict[str, str] = {}
    for h, f in mapping.items():
        inv.setdefault(f, h)
    entries: dict[str, Entry] = {}
    for row in reader:
        info["rows"] += 1
        g = lambda f: (row.get(inv[f], "") if f in inv else "") or ""
        num = EN.normalize(g("entry_number"))
        if not num:
            continue
        e = entries.get(num)
        if e is None:
            dates = {f: g(f).strip() for f in DATE_FIELDS}
            e = Entry(
                entry_number=num,
                entry_type=(g("entry_type") or "01").strip().zfill(2)[:2],
                entry_date=parse_date(dates["entry_date"]),
                importer_number=g("importer_number").strip(),
                importer_name=g("importer_name").strip(),
                country_of_origin=g("country_of_origin").strip(),
                liquidation_status=g("liquidation_status").strip(),
                liquidation_date=parse_date(dates["liquidation_date"]),
                deposit_date=parse_date(dates["deposit_date"]),
                protest_status=g("protest_status").strip().lower(),
                protest_solely_ieepa=_bool(g("protest_solely_ieepa")) if g("protest_solely_ieepa") else None,
                drawback=_bool(g("drawback")),
                recon_flag=_bool(g("recon_flag")),
                recon_09_filed=_bool(g("recon_09_filed")),
                surety_paid=_bool(g("surety_paid")),
                suspension_record=_bool(g("suspension_record")),
                ad_cvd=_bool(g("ad_cvd")),
                on_cape_declaration=_bool(g("on_cape_declaration")),
                needs_psc=_bool(g("needs_psc")),
            )
            e.unparsed = {f: v for f, v in dates.items() if v and parse_date(v) is None}
            entries[num] = e
        line_no = g("line_no") or str(len(e.lines) + 1)
        duty = parse_money_or_none(g("duty"))
        if duty is None:
            e.unparsed[f"duty (line {line_no})"] = g("duty").strip()
        e.lines.append(Line(line_no=line_no, hts=g("hts"), duty=duty or 0.0, value=parse_money(g("value"))))
    info["unparsed"] = sum(len(e.unparsed) > 0 for e in entries.values())
    return list(entries.values()), info
