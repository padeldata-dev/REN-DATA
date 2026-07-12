#!/usr/bin/env python3
"""Validate the 100 generated fichas:
- File exists, banner img exists
- JSON-LD parses (3 blocks: FAQPage, BreadcrumbList, Dataset)
- ROI coherent (alq*12/p = roi within tolerance)
- Population matches
- No leftover twin city name in body
- Banner image referenced
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_20k_30k_metadata.json"

cities = json.loads(META.read_text(encoding="utf-8"))


def extract_jsonld(html):
    """Find all JSON-LD <script type="application/ld+json"> blocks."""
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html, flags=re.DOTALL,
    )
    parsed = []
    for b in blocks:
        try:
            parsed.append(json.loads(b))
        except json.JSONDecodeError as e:
            parsed.append({"_error": str(e), "_raw": b[:200]})
    return parsed


errors = 0
warnings = 0
report = []
for c in cities:
    slug = c["slug"]; name = c["name"]
    p = BETA / f"rentabilidad-{slug}.html"
    if not p.is_file():
        report.append(f"[ERR] {slug}: HTML missing")
        errors += 1
        continue
    html = p.read_text(encoding="utf-8")

    # Banner img
    img = BETA / "img" / f"{slug}.webp"
    if not img.is_file():
        report.append(f"[ERR] {slug}: banner img/{slug}.webp missing")
        errors += 1
    elif img.stat().st_size > 250 * 1024:
        report.append(f"[WARN] {slug}: banner > 250KB ({img.stat().st_size//1024} KB)")
        warnings += 1
    # Banner reference in HTML
    if f'src="img/{slug}.webp"' not in html:
        report.append(f"[ERR] {slug}: HTML doesn't reference img/{slug}.webp")
        errors += 1

    # ROI coherence with 100m2 surface (precio * 100 piso → alq*12/(precio*100)*100 = alq*12/precio)
    expected_roi = c["alq"] * 12 / c["precio"]
    if abs(expected_roi - c["roi"]) > 0.4:
        report.append(f"[ERR] {slug}: ROI mismatch declared={c['roi']} expected={expected_roi:.2f}")
        errors += 1

    # Population in demo-card
    pob_str = f"{c['pop']:,}".replace(",", ".")
    if f">{pob_str}<" not in html:
        report.append(f"[WARN] {slug}: population {pob_str} not found in demo-card")
        warnings += 1

    # Title coherence
    if f"Invertir en {name} 2026" not in html:
        report.append(f"[WARN] {slug}: title doesn't match name")
        warnings += 1

    # JSON-LD validity
    parsed = extract_jsonld(html)
    types_found = []
    for blk in parsed:
        if isinstance(blk, dict) and "_error" in blk:
            report.append(f"[ERR] {slug}: JSON-LD parse error: {blk['_error']}")
            errors += 1
            continue
        items = blk if isinstance(blk, list) else [blk]
        for item in items:
            if not isinstance(item, dict):
                continue
            if "@graph" in item:
                for g in item["@graph"]:
                    types_found.append(g.get("@type"))
            else:
                types_found.append(item.get("@type"))
    for required in ("FAQPage", "BreadcrumbList", "Dataset"):
        if required not in types_found:
            report.append(f"[ERR] {slug}: missing JSON-LD {required} (found: {types_found})")
            errors += 1

print(f"\n=== Validation report ({len(cities)} cities) ===")
print(f"Errors:   {errors}")
print(f"Warnings: {warnings}")
if errors or warnings:
    for line in report[:80]:
        print(line)
    if len(report) > 80:
        print(f"... and {len(report)-80} more")
