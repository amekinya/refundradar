"""RefundRadar web app (FastAPI). Stateless: uploads are processed in memory, reports are kept in memory
for one hour so follow-up questions work, and nothing is written to disk."""
from __future__ import annotations

import json
import secrets
import time
from dataclasses import asdict
from datetime import date
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from app.ai import tasks
from app.ai.client import CallRecord, LiveModelUnavailable, ledger
from app.config import settings
from app.engine import analyze as A
from app.engine import catalog as C
from app.engine import entry_number as EN
from app.engine.es003 import parse_csv, parse_date, parse_money
from app.engine.models import Entry, Line, Profile
from app.engine.plan_check import check_plan

ROOT = Path(__file__).resolve().parent.parent
STATIC = Path(__file__).resolve().parent / "static"
SAMPLE = ROOT / "data" / "sample"
DEMO_CACHE = SAMPLE / "demo_cache.json"
DEMO_TODAY = date(2026, 10, 25)  # the sample importer is evaluated as of this date so the demo stays stable

app = FastAPI(title="RefundRadar")
app.mount("/static", StaticFiles(directory=STATIC), name="static")

_reports: dict[str, tuple[float, dict]] = {}
MAX_UPLOAD = 15 * 1024 * 1024


def _store(report: dict) -> str:
    now = time.time()
    for k in [k for k, (t, _) in _reports.items() if t < now - 3600]:
        _reports.pop(k, None)
    rid = secrets.token_urlsafe(12)
    _reports[rid] = (now, report)
    return rid


def _get(rid: str) -> dict:
    if rid not in _reports:
        raise HTTPException(404, "Report expired. Run the analysis again.")
    return _reports[rid][1]


def _calls_json(calls: list[CallRecord]) -> list[dict]:
    return [asdict(c) | {"seconds": round(c.seconds, 2), "cost_usd": round(c.cost_usd, 5)} for c in calls]


def _demo_cache() -> dict:
    try:
        return json.loads(DEMO_CACHE.read_text())
    except Exception:
        return {}


def _num(x) -> float | None:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def form_to_entry(form: dict, source_name: str) -> Entry:
    lines, unparsed = [], {}
    for ln in form.get("lines", []):
        hts, duties = ln.get("hts_numbers", []), ln.get("duties", [])
        for i, h in enumerate(hts):
            d = _num(duties[i]) if i < len(duties) else 0.0
            if d is None:
                unparsed[f"duty (line {ln.get('line_no', '')} {h})"] = str(duties[i])
            lines.append(Line(line_no=ln.get("line_no", ""), hts=h, duty=d or 0.0))
    raw_date = str(form.get("entry_date") or "").strip()
    entry_date = parse_date(raw_date)
    if raw_date and entry_date is None:
        unparsed["entry_date"] = raw_date
    check = form.get("duty_check") or {}
    return Entry(
        entry_number=form.get("entry_number", ""), entry_type=(form.get("entry_type") or "01")[:2],
        entry_date=entry_date, lines=lines,
        importer_number=form.get("importer_number", ""), importer_name=form.get("importer_name", ""),
        country_of_origin=form.get("country_of_origin", ""), source=f"photo:{source_name}", unparsed=unparsed,
        duty_mismatch=(check["lines_sum"], check["block_37"]) if check.get("ok") is False else None,
    )


def _yes(v) -> bool:
    return v.strip().lower() in {"true", "yes", "y", "1"} if isinstance(v, str) else bool(v)


def _profile(raw: str) -> Profile:
    try:
        d = json.loads(raw or "{}")
    except json.JSONDecodeError:
        d = {}
    if not isinstance(d, dict):
        d = {}
    tri = lambda v: None if v in (None, "", "unknown") else _yes(v)
    return Profile(
        importer_number=str(d.get("importer_number", "")),
        has_ace_account=tri(d.get("has_ace_account")),
        ach_refund_enrolled=tri(d.get("ach_refund_enrolled")),
        contact_email_current=tri(d.get("contact_email_current")),
        cit_plaintiff=_yes(d.get("cit_plaintiff", False)),
        plaintiff_ior_submitted_by_cutoff=_yes(d.get("plaintiff_ior_submitted_by_cutoff", False)),
        corporate=_yes(d.get("corporate", True)),
        filer=str(d.get("filer", "broker")),
    )


# --- pages -------------------------------------------------------------------------------
@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/health")
def health():
    return {"live_models": settings.live_models, "live_tavily": settings.live_tavily,
            "models": {s.role: s.model_id for s in (settings.nano, settings.super_vl, settings.ultra)},
            "spend_remaining_today": round(ledger.remaining(), 4), "rules_verified_as_of": C.RULES_VERIFIED_AS_OF.isoformat()}


# --- analysis ----------------------------------------------------------------------------
def _read_upload(f: UploadFile, what: str) -> bytes:
    data = f.file.read(MAX_UPLOAD + 1)
    if len(data) > MAX_UPLOAD:
        raise HTTPException(413, f"{what} is too large (15 MB max).")
    return data


@app.post("/api/analyze")
def analyze_upload(
    profile: str = Form("{}"),
    csv_file: UploadFile | None = File(None),
    photos: list[UploadFile] | None = File(None),
):
    # A plain `def`: FastAPI runs it in a worker thread, so the blocking model calls (and a big CSV) don't stall
    # every other visitor's requests while one upload is being read.
    calls: list[CallRecord] = []
    steps: list[dict] = []
    entries: list[Entry] = []
    review_grid: list[dict] = []
    extra_blockers: list[dict] = []

    if csv_file is not None and csv_file.filename:
        text = _read_upload(csv_file, "The file").decode("utf-8-sig", errors="replace")
        parsed, info = parse_csv(text)
        step = {"step": "Read your spreadsheet", "detail": f"{info['rows']} rows", "model": None}
        if info["missing"]:
            try:
                import csv as _csv, io as _io
                rows = list(_csv.DictReader(_io.StringIO(text)))[:3]
                mapping = tasks.map_headers(info["headers"], rows, calls)
                parsed, info = parse_csv(text, header_map=mapping)
                step.update(detail=f"Unfamiliar columns mapped by Nemotron 3.5 Lightning ({len(mapping)} fields)", model=settings.nano.model_id)
            except LiveModelUnavailable:
                raise HTTPException(422, f"Couldn't find these columns: {', '.join(info['missing'])}. Use an ACE ES-003 export.")
            if info["missing"]:
                raise HTTPException(422, f"Couldn't find these columns: {', '.join(info['missing'])}.")
        if info.get("unparsed"):
            step["detail"] += f" · {info['unparsed']} with dates or amounts we couldn't read"
        entries += parsed
        steps.append(step | {"count": len(parsed)})

    known_filers = {EN.normalize(e.entry_number)[:3] for e in entries if len(EN.normalize(e.entry_number)) == 11}
    skipped = 0
    for ph in photos or []:
        if not ph.filename:
            continue
        data = _read_upload(ph, ph.filename)
        mime = ph.content_type or "image/jpeg"
        try:
            form = tasks.read_form(data, mime, calls)
        except LiveModelUnavailable:
            if not entries:
                raise HTTPException(503, "Reading photos needs the AI service, which isn't available right now. Try the CSV path or the sample.")
            skipped += 1  # keep the spreadsheet result rather than failing the whole upload
            continue
        form, changed = _checked_form(form, known_filers)
        if EN.validate(form.get("entry_number", "")):  # still fails the check digit: one focused second look
            try:
                again, _ = _checked_form(form | {"entry_number": tasks.reread_entry_number(data, mime, calls)}, known_filers)
                if not EN.validate(again["entry_number"]):
                    form, changed = again | {"entry_number_as_read": form.get("entry_number_as_read") or form["entry_number"],
                                             "entry_number_fix": "reread"}, True
            except LiveModelUnavailable:
                pass
        review_grid.append({"file": ph.filename, "fields": form, "corrected": changed})
        entries.append(form_to_entry(form, ph.filename))
    if photos:
        steps.append({"step": "Read your form photos", "detail": f"{len(review_grid)} photos", "model": settings.super_vl.model_id})
    if skipped:
        extra_blockers.append({"key": "photos", "severity": "high", "title": f"{skipped} photo{'s' if skipped > 1 else ''} not read",
                               "detail": "The AI photo reader isn't available right now, so only your spreadsheet is in this report.",
                               "fix": "Upload the photos again later."})

    if not entries:
        raise HTTPException(400, "Add an ACE ES-003 export or photos of your entry summaries.")
    prof = _profile(profile)
    report = A.analyze(entries, prof, date.today())
    report["blockers"] = extra_blockers + report["blockers"]
    steps.append({"step": "Apply the refund rules", "detail": f"{len(report['routes'])} entries routed (rules verified {C.RULES_VERIFIED_AS_OF:%b %d, %Y})", "model": None})
    report["review_grid"] = review_grid
    report["profile"] = asdict(prof)
    report["pipeline"] = steps
    report["calls"] = _calls_json(calls)
    report["report_id"] = _store(report)
    report["demo"] = False
    return JSONResponse(report)


def _checked_form(form: dict, known_filers: set[str]) -> tuple[dict, bool]:
    """Repair a look-alike misread in the entry number with the CBP check digit (Q read as 0, Z as 2...), flag a number
    that still fails it, and cross-check the duty read from each tariff line against Block 37, the form's own total."""
    form = dict(form)
    fixed, changed = EN.repair(form.get("entry_number", ""), known_filers)
    if changed:  # show both so the user can see why
        form["entry_number_as_read"], form["entry_number"] = form["entry_number"], EN.display(fixed)
        form["entry_number_fix"] = "check_digit"
    form["entry_number_problems"] = EN.validate(form.get("entry_number", "")) if form.get("entry_number") else ["Entry number not read"]
    form["duty_check"] = duty_check(form)
    return form, changed


def duty_check(form: dict) -> dict:
    """The form checks itself: the line duties (column 34) should add up to Block 37. A gap means a digit was misread
    or a line was missed, and the refund amount built from those lines is off; the user is asked to look.
    Tolerance is rounding only: 1 cent per amount, at most $1."""
    try:
        duties = [float(d or 0) for ln in form.get("lines", []) for d in ln.get("duties", [])]
        total = float(form.get("total_duty") or 0)
    except (TypeError, ValueError):
        return {"ok": None, "reason": "Duty amounts not read"}
    lines = round(sum(duties), 2)
    if not total:
        return {"ok": None, "reason": "Block 37 not read", "lines_sum": lines}
    if not duties:
        return {"ok": None, "reason": "No tariff-line duties read", "block_37": round(total, 2)}
    gap = round(total - lines, 2)
    tolerance = min(1.0, 0.01 * len(duties))
    return {"ok": abs(gap) <= tolerance + 1e-9, "lines_sum": lines, "block_37": round(total, 2), "gap": gap, "tolerance": tolerance}


def build_sample(forms: dict[str, dict]) -> dict:
    """The demo importer's report from its ES-003 export and the given photo readings (same path as /api/sample, so
    scripts/build_demo_cache.py writes its plan and explanations against exactly what visitors see)."""
    entries, info = parse_csv((SAMPLE / "prairie_lantern_es003.csv").read_text())
    review_grid = []
    known_filers = {EN.normalize(e.entry_number)[:3] for e in entries if len(EN.normalize(e.entry_number)) == 11}
    for name in sorted(forms):
        form, changed = _checked_form(forms[name], known_filers)
        review_grid.append({"file": name, "fields": form, "url": f"/api/sample/photo/{name}", "corrected": changed})
        entries.append(form_to_entry(form, name))
    prof = Profile(importer_number="00-7351942AA", has_ace_account=True, ach_refund_enrolled=False, corporate=True)
    report = A.analyze(entries, prof, DEMO_TODAY)
    report["review_grid"] = review_grid
    report["pipeline"] = [
        {"step": "Read your ES-003 export", "detail": f"{info['rows']} rows · {len(entries) - len(review_grid)} entries", "model": None},
        {"step": f"Read {len(review_grid)} form photos", "detail": "Courier-handled shipments", "model": settings.super_vl.model_id},
        {"step": "Apply the refund rules", "detail": f"{len(report['routes'])} entries routed (rules verified {C.RULES_VERIFIED_AS_OF:%b %d, %Y})", "model": None},
    ]
    report["profile"] = asdict(prof)
    return report


@app.get("/api/sample")
def sample():
    """The demo importer: ES-003 export + three courier-handled form photos. Uses cached model outputs."""
    cache = _demo_cache()
    forms = {p.name: cache.get("forms", {}).get(p.name) or json.loads(p.with_suffix(".json").read_text())
             for p in sorted((SAMPLE / "photos").glob("*.jpg"))}
    report = build_sample(forms)
    report["calls"] = cache.get("calls", [])
    report["demo"] = True
    report["report_id"] = _store(report)
    return JSONResponse(report)


@app.get("/api/sample/photo/{name}")
def sample_photo(name: str):
    p = (SAMPLE / "photos" / Path(name).name)
    if not p.exists() or p.suffix != ".jpg":
        raise HTTPException(404)
    return FileResponse(p, media_type="image/jpeg")


@app.get("/api/sample/files/{name}")
def sample_file(name: str):
    allowed = {"prairie_lantern_es003.csv": "text/csv", "refund_offer_email.txt": "text/plain"}
    if name not in allowed:
        raise HTTPException(404)
    return FileResponse(SAMPLE / name, media_type=allowed[name], filename=name)


# --- model-powered follow-ups --------------------------------------------------------------
@app.post("/api/plan")
def plan(body: dict):
    report = _get(body.get("report_id", ""))
    if report.get("demo") and _demo_cache().get("plan"):
        return check_plan(_demo_cache()["plan"], report) | {"cached": True}
    calls: list[CallRecord] = []
    try:
        out = check_plan(tasks.action_plan(report, calls), report)
        return out | {"calls": _calls_json(calls)}
    except LiveModelUnavailable:
        return tasks.action_plan_fallback(report)
    except Exception as e:  # model or schema hiccup: never leave the user empty-handed
        return tasks.action_plan_fallback(report) | {"error": type(e).__name__}


@app.post("/api/explain")
def explain(body: dict):
    report = _get(body.get("report_id", ""))
    num = body.get("entry_number", "")
    route = next((r for r in report["routes"] if r["entry_number"] == num), None)
    if not route:
        raise HTTPException(404, "Entry not found in this report.")
    cache = _demo_cache() if report.get("demo") else {}
    # A cached explanation is used only for the rule it was written for: after a rule change it would state the old route.
    cached = cache.get("explanations", {}).get(num) if cache.get("explanation_rules", {}).get(num) == route["rule_id"] else None
    if cached:
        return {"text": cached, "cached": True}
    calls: list[CallRecord] = []
    try:
        return {"text": tasks.explain_entry(route, calls), "calls": _calls_json(calls)}
    except LiveModelUnavailable:
        return {"text": f"{route['title']}. {route['action']}", "fallback": True}


@app.post("/api/offer")
def offer(body: dict):
    report = _get(body.get("report_id", ""))
    text = (body.get("text") or "").strip()
    if len(text) < 20:
        raise HTTPException(400, "Paste the offer email or letter text.")
    h = report["headline"]
    refund, entries = h["reachable_now"] or (h["total_principal"] + h["total_interest"]), max(h["reachable_now_count"], 1)
    if report.get("demo") and _demo_cache().get("offer") and body.get("use_sample"):
        return _demo_cache()["offer"] | {"cached": True}
    calls: list[CallRecord] = []
    try:
        return tasks.offer_check(text, refund, entries, calls) | {"calls": _calls_json(calls)}
    except LiveModelUnavailable:
        return tasks.offer_check_fallback(text, refund, entries)


@app.get("/api/freshness")
def freshness():
    try:
        return tasks.freshness()
    except Exception as e:
        cached = _demo_cache().get("freshness")
        return (cached | {"cached": True}) if cached else {"checked": False, "error": type(e).__name__,
                                                           "rules_verified_as_of": C.RULES_VERIFIED_AS_OF.isoformat(), "items": []}


# --- exports -----------------------------------------------------------------------------
@app.get("/api/export/{rid}/{kind}")
def export(rid: str, kind: str):
    report = _get(rid)
    if kind == "worksheet.csv":
        return Response(A.worksheet_csv(report), media_type="text/csv",
                        headers={"Content-Disposition": "attachment; filename=refundradar_worksheet.csv"})
    if kind == "broker_entry_list.csv":
        return Response(A.handoff_csv(report), media_type="text/csv",
                        headers={"Content-Disposition": "attachment; filename=refundradar_broker_entry_list.csv"})
    if kind == "deadlines.ics":
        return Response(A.deadlines_ics(report), media_type="text/calendar",
                        headers={"Content-Disposition": "attachment; filename=refundradar_deadlines.ics"})
    raise HTTPException(404)
