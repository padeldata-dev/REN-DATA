#!/usr/bin/env python3
"""Add 7 cities present in DATA[] but missing from cities_master.csv,
using values straight from index.html DATA[]."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "pipeline" / "data" / "cities_master.csv"
INDEX = ROOT / "rendata_beta" / "index.html"

with MASTER.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)
existing = {r["slug"] for r in rows}

html = INDEX.read_text(encoding="utf-8")
pat = re.compile(
    r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
    r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
    r'd:(\d+),sl:"([^"]+)"'
)
added = 0
for m in pat.finditer(html):
    slug = m.group(10)
    if slug in existing:
        continue
    rows.append({
        "slug": slug,
        "nombre": m.group(1),
        "ccaa": m.group(2),
        "reg": m.group(3),
        "precio_actual": int(m.group(5)),
        "alquiler_actual": int(m.group(6)),
        "roi_actual": float(m.group(4)),
        "var_precio_anual": float(m.group(7)),
        "var_alquiler_anual": float(m.group(8)),
        "dias_mercado": int(m.group(9)),
        "ine_code": "",
    })
    existing.add(slug)
    added += 1
    print(f"  + {slug}  {m.group(1)}  ({m.group(2)})")

with MASTER.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"\nAñadidas: {added}. Master total: {len(rows)} filas")
