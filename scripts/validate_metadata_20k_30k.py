#!/usr/bin/env python3
"""Validate metadata: all twins exist, all alt slugs exist (or in batch)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "data" / "cities_20k_30k_metadata.json"
BETA = ROOT / "rendata_beta"

data = json.loads(META.read_text(encoding="utf-8"))
existing = {p.stem.replace("rentabilidad-", "") for p in BETA.glob("rentabilidad-*.html")}
batch = {c["slug"] for c in data}
errors = []

for c in data:
    if c["twin"] not in existing:
        errors.append(f"  twin missing: {c['slug']} -> {c['twin']}")
    for name, slug in c["alt"]:
        if slug not in existing and slug not in batch:
            errors.append(f"  alt missing: {c['slug']} -> {name} ({slug})")
    # ROI coherence: roi ≈ alq*12/precio
    expected_roi = c["alq"] * 12 / c["precio"]
    if abs(expected_roi - c["roi"]) > 0.4:
        errors.append(f"  roi mismatch: {c['slug']} declared={c['roi']} expected={expected_roi:.2f}")

if errors:
    print("ERRORS:")
    for e in errors:
        print(e)
    print(f"\nTotal: {len(errors)}")
else:
    print(f"OK: {len(data)} entries valid")
