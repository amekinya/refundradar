"""Data shapes for the rule engine."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Line:
    line_no: str
    hts: str
    duty: float = 0.0
    value: float = 0.0


@dataclass
class Entry:
    entry_number: str
    entry_type: str = "01"
    entry_date: date | None = None
    lines: list[Line] = field(default_factory=list)
    importer_number: str = ""  # IOR number on the entry (Block 23 old form / 27 new form)
    importer_name: str = ""
    country_of_origin: str = ""
    liquidation_status: str = ""  # Not Liquidated / Liquidated / Pending / Extended / Suspended / Under Review
    liquidation_date: date | None = None
    deposit_date: date | None = None
    # Status flags (from ACE or the user); None = unknown
    protest_status: str = ""  # "" / open / suspended / denied
    protest_solely_ieepa: bool | None = None
    drawback: bool = False
    recon_flag: bool = False
    recon_09_filed: bool = False
    surety_paid: bool = False
    suspension_record: bool = False
    ad_cvd: bool = False
    on_cape_declaration: bool = False
    not_in_ace: bool = False
    needs_psc: bool = False  # e.g., INVALID HTS / HTS RELATIONSHIP MISMATCH known
    source: str = "csv"  # csv | photo:<file name>
    # What reading the input couldn't settle. Routing and blockers use these; nothing is guessed silently.
    unparsed: dict[str, str] = field(default_factory=dict)  # field -> raw value that isn't a readable date or amount
    duty_mismatch: tuple[float, float] | None = None  # photo: (tariff-line duties added up, Block 37) when they disagree


@dataclass
class Profile:
    """The importer's answers to the readiness questions. None = not answered."""

    importer_number: str = ""  # the user's own IOR number (to detect someone else holding the claim)
    has_ace_account: bool | None = None
    ach_refund_enrolled: bool | None = None
    contact_email_current: bool | None = None  # Form 5106 point of contact
    cit_plaintiff: bool = False
    plaintiff_ior_submitted_by_cutoff: bool = False
    corporate: bool = True  # interest rate table (corporate vs non-corporate)
    filer: str = "broker"  # broker | self | courier | forwarder | unknown


@dataclass
class Route:
    entry_number: str
    rule_id: str
    bucket: str
    title: str
    action: str
    tag: str
    sources: tuple[str, ...]
    principal: float = 0.0
    interest: float = 0.0
    deadline: date | None = None
    deadline_type: str = ""  # CAPE_80 | PROTEST_180 | CIT_2YR
    days_left: int | None = None
    liquidation_date: date | None = None
    liquidation_estimated: bool = False
    programs: tuple[str, ...] = ()
    all_in_overstated: bool = False
    all_in_duty: float = 0.0
    holder: str = "you"  # you | someone_else
    source: str = "csv"
    notes: list[str] = field(default_factory=list)
    entry_problems: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)  # machine keys for blockers: unparsed, duty_mismatch, check_digit_photo, unreadable_number
