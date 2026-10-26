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


def form_to_entry(form: dict, source_name: str) -> Entry:
    lines = []
    for ln in form.get("lines", []):
        hts, duties = ln.get("hts_numbers", []), ln.get("duties", [])
        for i, h in enumerate(hts):
            lines.append(Line(line_no=ln.get("line_no", ""), hts=h, duty=float(duties[i]) if i < len(duties) else 0.0))
    return Entry(
        entry_number=form.get("entry_number", ""), entry_type=(form.get("entry_type") or "01")[:2],
        entry_date=parse_date(form.get("entry_date", "")), lines=lines,
        importer_number=form.get("importer_number", ""), importer_name=form.get("importer_name", ""),
        country_of_origin=form.get("country_of_origin", ""), source=f"photo:{source_name}",
    )


def _profile(raw: str) -> Profile:
    try:
        d = json.loads(raw or "{}")
    except json.JSONDecodeError:
        d = {}
    tri = lambda v: None if v in (None, "", "unknown") else bool(v)
    return Profile(
        importer_number=str(d.get("importer_number", "")),
        has_ace_account=tri(d.get("has_ace_account")),
        ach_refund_enrolled=tri(d.get("ach_refund_enrolled")),
        contact_email_current=tri(d.get("contact_email_current")),
        cit_plaintiff=bool(d.get("cit_plaintiff", False)),
        plaintiff_ior_submitted_by_cutoff=bool(d.get("plaintiff_ior_submitted_by_cutoff", False)),
        corporate=bool(d.get("corporate", True)),
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
@app.post("/api/analyze")
async def analyze_upload(
    profile: str = Form("{}"),
    csv_file: UploadFile | None = File(None),
    photos: list[UploadFile] | None = File(None),
):
    calls: list[CallRecord] = []
    steps: list[dict] = []
    entries: list[Entry] = []
    review_grid: list[dict] = []

    if csv_file is not None and csv_file.filename:
        raw = await csv_file.read()
        if len(raw) > MAX_UPLOAD:
            raise HTTPException(413, "File too large (15 MB max).")
        text = raw.decode("utf-8-sig", errors="replace")
        parsed, info = parse_csv(text)
        step = {"step": "Read your spreadsheet", "detail": f"{info['rows']} rows", "model": None}
        if info["missing"]:
            try:
                import csv as _csv, io as _io
                rows = list(_csv.DictReader(_io.StringIO(text)))[:3]
                mapping = tasks.map_headers(info["headers"], rows, calls)
                parsed, info = parse_csv(text, header_map=mapping)
                step.update(detail=f"Unfamiliar columns mapped by Nemotron Nano ({len(mapping)} fields)", model=settings.nano.model_id)
            except LiveModelUnavailable:
                raise HTTPException(422, f"Couldn't find these columns: {', '.join(info['missing'])}. Use an ACE ES-003 export.")
            if info["missing"]:
                raise HTTPException(422, f"Couldn't find these columns: {', '.join(info['missing'])}.")
        entries += parsed
        steps.append(step | {"count": len(parsed)})

    known_filers = {EN.normalize(e.entry_number)[:3] for e in entries if len(EN.normalize(e.entry_number)) == 11}
    for ph in photos or []:
        if not ph.filename:
            continue
        data = await ph.read()
        if len(data) > MAX_UPLOAD:
            raise HTTPException(413, f"{ph.filename} is too large.")
        try:
            form = tasks.read_form(data, ph.content_type or "image/jpeg", calls)
        except LiveModelUnavailable:
            raise HTTPException(503, "Reading photos needs the AI service, which isn't available right now. Try the CSV path or the sample.")
        form, changed = _checked_form(form, known_filers)
        review_grid.append({"file": ph.filename, "fields": form, "corrected": changed})
        entries.append(form_to_entry(form, ph.filename))
    if photos:
        steps.append({"step": "Read your form photos", "detail": f"{len(review_grid)} photos", "model": settings.super_vl.model_id})

    if not entries:
        raise HTTPException(400, "Add an ACE ES-003 export or photos of your entry summaries.")
    prof = _profile(profile)
    report = A.analyze(entries, prof, date.today())
    steps.append({"step": "Apply the refund rules", "detail": f"{len(report['routes'])} entries routed (rules verified {C.RULES_VERIFIED_AS_OF:%b %d, %Y})", "model": None})
    report["review_grid"] = review_grid
    report["profile"] = asdict(prof)
    report["pipeline"] = steps
    report["calls"] = _calls_json(calls)
    report["report_id"] = _store(report)
    report["demo"] = False
    return JSONResponse(report)


def _checked_form(form: dict, known_filers: set[str]) -> tuple[dict, bool]:
    """Repair a look-alike misread in the entry number with the CBP check digit (Q read as 0, Z as 2...)."""
    form = dict(form)
    fixed, changed = EN.repair(form.get("entry_number", ""), known_filers)
    if changed:  # show both so the user can see why
        form["entry_number_as_read"], form["entry_number"] = form["entry_number"], EN.display(fixed)
    return form, changed


@app.get("/api/sample")
def sample():
    """The demo importer: ES-003 export + three courier-handled form photos. Uses cached model outputs."""
    cache = _demo_cache()
    entries, info = parse_csv((SAMPLE / "prairie_lantern_es003.csv").read_text())
    review_grid = []
    known_filers = {EN.normalize(e.entry_number)[:3] for e in entries if len(EN.normalize(e.entry_number)) == 11}
    for p in sorted((SAMPLE / "photos").glob("*.jpg")):
        form, changed = _checked_form(cache.get("forms", {}).get(p.name) or json.loads(p.with_suffix(".json").read_text()), known_filers)
        review_grid.append({"file": p.name, "fields": form, "url": f"/api/sample/photo/{p.name}", "corrected": changed})
        entries.append(form_to_entry(form, p.name))
    prof = Profile(importer_number="00-7351942AA", has_ace_account=True, ach_refund_enrolled=False, corporate=True)
    report = A.analyze(entries, prof, DEMO_TODAY)
    report["review_grid"] = review_grid
    report["pipeline"] = [
        {"step": "Read your ES-003 export", "detail": f"{info['rows']} rows · {len(entries) - len(review_grid)} entries", "model": None},
        {"step": "Read 3 form photos", "detail": "Courier-handled shipments", "model": settings.super_vl.model_id},
        {"step": "Apply the refund rules", "detail": f"{len(report['routes'])} entries routed (rules verified {C.RULES_VERIFIED_AS_OF:%b %d, %Y})", "model": None},
    ]
    report["calls"] = cache.get("calls", [])
    report["profile"] = asdict(prof)
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
        return _demo_cache()["plan"] | {"cached": True}
    calls: list[CallRecord] = []
    try:
        out = tasks.action_plan(report, calls)
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
    cached = _demo_cache().get("explanations", {}).get(num) if report.get("demo") else None
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
