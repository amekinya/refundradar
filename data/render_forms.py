"""Render synthetic CBP Form 7501 (Entry Summary) images, then 'photograph' them (skew, shadow, blur, JPEG).

All companies and identifiers are invented. Ground truth for each image is saved next to it as JSON
so we can measure how well Nemotron 3.5 Super VL reads real-world-quality photos.

Outputs: data/forms/form_XX.jpg + form_XX.json ; data/sample/photos/ (the 3 demo photos)
"""
from __future__ import annotations

import io
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from app.engine.entry_number import check_digit

ROOT = Path(__file__).parent
rng = random.Random(7501)
W, H = 1700, 2200


def font(size: int, mono: bool = False, bold: bool = False):
    name = "DejaVuSansMono" if mono else ("DejaVuSans-Bold" if bold else "DejaVuSans")
    try:
        return ImageFont.truetype(f"{name}.ttf", size)
    except OSError:
        return ImageFont.load_default()


F_LABEL, F_VAL, F_SMALL, F_TITLE = font(17), font(24, mono=True), font(15), font(30, bold=True)

COMPANIES = [  # (IOR name, address, importer number) — all invented; '00-' EIN prefixes are never issued by the IRS
    ("PRAIRIE LANTERN HOME GOODS LLC", "1450 OGDEN AVE STE 210, NAPERVILLE IL 60540", "00-7351942AA"),
    ("SWIFTLINE EXPRESS INC", "9 AIRPORT LOOP, LOUISVILLE KY 40209", "00-4417730ZZ"),
    ("NORTHBAY KITCHEN SUPPLY CO", "77 HARBOR RD, OAKLAND CA 94607", "00-2264918AB"),
    ("MAPLEFORD OUTDOOR LLC", "301 MILL ST, BURLINGTON VT 05401", "00-9081236AA"),
]
GOODS = [("9405.41.8400", "LED TABLE LAMPS", 0.039), ("6302.31.9020", "COTTON BED LINEN", 0.067),
         ("6912.00.4810", "CERAMIC SERVEWARE", 0.098), ("4420.90.8000", "WOODEN DECOR BOXES", 0.032),
         ("7013.99.8000", "GLASS CANDLE HOLDERS", 0.06), ("6307.90.9891", "WOVEN BASKETS", 0.07)]
CH99 = [("9903.01.24", 0.20, "CN"), ("9903.01.25", 0.10, "CN"), ("9903.02.69", 0.20, "VN"), ("9903.02.26", 0.25, "IN")]
FILERS = ["Q7Z", "K4M", "T2R"]


def make_truth(company_idx: int | None = None) -> dict:
    idx = company_idx if company_idx is not None else rng.randrange(len(COMPANIES))
    name, addr, imp = COMPANIES[idx]
    consignee = COMPANIES[0][0] if idx == 1 else name  # courier as IOR: our importer is only the consignee
    filer = rng.choice(FILERS)
    seq = rng.randint(1_000_000, 9_999_999)
    num = f"{filer}-{seq:07d}-{check_digit(f'{filer}{seq:07d}')}"
    ed = date(2025, 4, 1) + timedelta(days=rng.randint(0, 320))
    ch, rate99, country = rng.choice(CH99)
    lines, total = [], 0.0
    for i in range(rng.randint(1, 3)):
        hts, desc, rate = rng.choice(GOODS)
        value = rng.randrange(900, 9000, 10)
        base = round(value * rate, 2)
        extra = round(value * rate99, 2)
        lines.append({"line_no": f"{i + 1:03d}", "desc": desc, "value": value, "hts_numbers": [ch, hts],
                      "rates": [f"+{int(rate99 * 100)}%", f"{rate * 100:.1f}%"], "duties": [extra, base]})
        total += extra + base
    return {"entry_number": num, "entry_type": "01" if rng.random() > 0.15 else "11", "entry_date": ed.strftime("%m/%d/%Y"),
            "summary_date": (ed + timedelta(days=rng.randint(3, 9))).strftime("%m/%d/%Y"), "port": rng.choice(["3901", "2704", "1001", "5301"]),
            "importer_number": imp, "importer_name": name, "importer_address": addr, "importer_label": name, "consignee": consignee,
            "broker_or_filer": rng.choice(["GREATLAKES CUSTOMS BROKERAGE", "BLUEWATER TRADE SERVICES", "SWIFTLINE EXPRESS INC"]),
            "country_of_origin": country, "lines": lines, "total_duty": round(total, 2)}


def box(d: ImageDraw.ImageDraw, x, y, w, h, label, value="", vfont=None):
    d.rectangle([x, y, x + w, y + h], outline="black", width=2)
    d.text((x + 6, y + 4), label, fill="black", font=F_LABEL)
    if value:
        d.text((x + 10, y + h - 36), value, fill=(20, 20, 60), font=vfont or F_VAL)


def render(t: dict) -> Image.Image:
    img = Image.new("RGB", (W, H), (252, 252, 248))
    d = ImageDraw.Draw(img)
    d.text((60, 40), "DEPARTMENT OF HOMELAND SECURITY", fill="black", font=F_SMALL)
    d.text((60, 62), "U.S. Customs and Border Protection", fill="black", font=F_SMALL)
    d.text((620, 50), "ENTRY SUMMARY", fill="black", font=F_TITLE)
    d.text((1380, 50), "CBP Form 7501", fill="black", font=F_SMALL)
    y = 110
    row = [(0, 420, "1. Filer Code/Entry No.", t["entry_number"]), (420, 170, "2. Entry Type", t["entry_type"]),
           (590, 230, "3. Summary Date", t["summary_date"]), (820, 170, "4. Surety No.", "457"), (990, 150, "5. Bond Type", "8"),
           (1140, 170, "6. Port Code", t["port"]), (1310, 270, "7. Entry Date", t["entry_date"])]
    for x, w, lab, val in row:
        box(d, 60 + x, y, w, 90, lab, val)
    y += 90
    row = [(0, 420, "8. Importing Carrier", "COSCO SHIPPING"), (420, 200, "9. Mode of Transport", "11"),
           (620, 300, "10. Country of Origin", t["country_of_origin"]), (920, 300, "11. Import Date", t["entry_date"]),
           (1220, 360, "12. B/L or AWB No.", f"COSU{rng.randint(10**9, 10**10 - 1)}")]
    for x, w, lab, val in row:
        box(d, 60 + x, y, w, 90, lab, val)
    y += 90
    box(d, 60, y, 760, 90, "22. Consignee No.", "SAME")
    box(d, 820, y, 760, 90, "23. Importer No.", t["importer_number"])
    y += 90
    box(d, 60, y, 760, 150, "25. Ultimate Consignee Name and Address", "")
    d.text((75, y + 40), t["consignee"][:34], fill=(20, 20, 60), font=F_VAL)
    box(d, 820, y, 760, 150, "26. Importer of Record Name and Address", "")
    d.text((835, y + 40), t["importer_label"][:34], fill=(20, 20, 60), font=F_VAL)
    d.text((835, y + 80), t["importer_address"][:40], fill=(20, 20, 60), font=font(18, mono=True))
    y += 170
    cols = [(0, 110, "27. Line No."), (110, 470, "28. Description of Merchandise"), (580, 330, "29. HTSUS No."),
            (910, 250, "32. Entered Value"), (1160, 180, "33. HTSUS Rate"), (1340, 240, "34. Duty")]
    for x, w, lab in cols:
        d.rectangle([60 + x, y, 60 + x + w, y + 50], outline="black", width=2)
        d.text((66 + x, y + 14), lab, fill="black", font=F_LABEL)
    y += 50
    for ln in t["lines"]:
        hgt = 60 * len(ln["hts_numbers"]) + 20
        for x, w, _ in cols:
            d.rectangle([60 + x, y, 60 + x + w, y + hgt], outline="black", width=1)
        d.text((80, y + 14), ln["line_no"], fill=(20, 20, 60), font=F_VAL)
        d.text((180, y + 14), ln["desc"], fill=(20, 20, 60), font=font(20, mono=True))
        for k, (h_, r_, du) in enumerate(zip(ln["hts_numbers"], ln["rates"], ln["duties"])):
            yy = y + 14 + 60 * k
            d.text((650, yy), h_, fill=(20, 20, 60), font=F_VAL)
            if k == len(ln["hts_numbers"]) - 1:
                d.text((990, yy), f"{ln['value']:,}", fill=(20, 20, 60), font=F_VAL)
            d.text((1230, yy), r_, fill=(20, 20, 60), font=F_VAL)
            d.text((1420, yy), f"{du:,.2f}", fill=(20, 20, 60), font=F_VAL)
        y += hgt
    y += 30
    box(d, 1100, y, 480, 80, "37. Duty", f"{t['total_duty']:,.2f}")
    box(d, 1100, y + 80, 480, 80, "40. Total", f"{t['total_duty']:,.2f}")
    box(d, 60, y, 1040, 160, "42. Broker/Filer Information (Name, address, phone number)", "")
    d.text((75, y + 60), t["broker_or_filer"], fill=(20, 20, 60), font=F_VAL)
    d.text((60, H - 60), "CBP Form 7501  —  SYNTHETIC SAMPLE FOR SOFTWARE TESTING. NOT A REAL ENTRY.", fill=(120, 0, 0), font=F_SMALL)
    return img


def photograph(img: Image.Image, strength: float) -> Image.Image:
    """Simulate a phone photo: perspective tilt, rotation, uneven light, blur, JPEG artifacts."""
    w, h = img.size
    m = int(60 * strength)
    src = [(rng.randint(0, m), rng.randint(0, m)), (w - rng.randint(0, m), rng.randint(0, m)),
           (w - rng.randint(0, m), h - rng.randint(0, m)), (rng.randint(0, m), h - rng.randint(0, m))]
    coeffs = _perspective_coeffs([(0, 0), (w, 0), (w, h), (0, h)], src)
    img = img.transform((w, h), Image.Transform.PERSPECTIVE, coeffs, Image.Resampling.BICUBIC, fillcolor=(90, 80, 70))
    img = img.rotate(rng.uniform(-3, 3) * strength, resample=Image.Resampling.BICUBIC, fillcolor=(90, 80, 70))
    shade = Image.linear_gradient("L").resize((w, h)).rotate(rng.choice([0, 90, 180, 270]))
    shade = shade.point(lambda p: int(255 - p * 0.35 * strength))
    img = Image.composite(img, Image.new("RGB", (w, h), (40, 35, 30)), shade)
    img = ImageEnhance.Brightness(img).enhance(rng.uniform(0.9, 1.08))
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6 + 1.2 * strength * rng.random()))
    img = img.resize((int(w * 0.6), int(h * 0.6)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=int(85 - 30 * strength))
    return Image.open(io.BytesIO(buf.getvalue())).convert("RGB")


def _perspective_coeffs(dst, src):
    import numpy as np  # noqa: PLC0415

    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return list(np.linalg.solve(np.array(A, dtype=float), np.array(B, dtype=float)))


def truth_for_eval(t: dict) -> dict:
    return {k: t[k] for k in ("entry_number", "entry_type", "entry_date", "importer_number", "importer_name", "country_of_origin", "total_duty")} | {
        "lines": [{"line_no": l["line_no"], "hts_numbers": l["hts_numbers"], "duties": l["duties"]} for l in t["lines"]]}


def main(n_eval: int = 30):
    out = ROOT / "forms"
    out.mkdir(exist_ok=True)
    for i in range(n_eval):
        t = make_truth()
        strength = [0.2, 0.5, 0.9][i % 3]
        photograph(render(t), strength).save(out / f"form_{i:02d}.jpg", quality=92)
        (out / f"form_{i:02d}.json").write_text(json.dumps(truth_for_eval(t) | {"photo_strength": strength}, indent=1))
    demo = ROOT / "sample" / "photos"
    demo.mkdir(parents=True, exist_ok=True)
    for i in range(3):  # demo: three courier-handled shipments where the courier was importer of record
        t = make_truth(company_idx=1)
        photograph(render(t), 0.45).save(demo / f"courier_entry_{i + 1}.jpg", quality=90)
        (demo / f"courier_entry_{i + 1}.json").write_text(json.dumps(truth_for_eval(t), indent=1))
    print(f"rendered {n_eval} eval forms + 3 demo photos")


if __name__ == "__main__":
    main()
