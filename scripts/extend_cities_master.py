#!/usr/bin/env python3
"""Extiende pipeline/data/cities_master.csv con los 148 slugs nuevos
(41 fichas 30k-50k + 100 fichas 20k-30k).

Lee los metadatos JSON ya generados y produce filas compatibles con el
formato del master (slug, nombre, ccaa, reg, precio, alq, roi, vp, va, dias,
ine_code).
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "pipeline" / "data" / "cities_master.csv"
META_30K = ROOT / "data" / "cities_30k_50k_metadata.json"
META_20K = ROOT / "data" / "cities_20k_30k_metadata.json"

with MASTER.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    existing_rows = list(reader)
existing_slugs = {r["slug"] for r in existing_rows}
print(f"Master actual: {len(existing_rows)} filas. Campos: {fieldnames}")

new_meta = json.loads(META_30K.read_text(encoding="utf-8")) + \
           json.loads(META_20K.read_text(encoding="utf-8"))
print(f"Metadatos nuevos a integrar: {len(new_meta)} entradas")

added = 0
skipped = 0
for c in new_meta:
    slug = c["slug"]
    if slug in existing_slugs:
        skipped += 1
        continue
    existing_rows.append({
        "slug": slug,
        "nombre": c["name"],
        "ccaa": c["ccaa"],
        "reg": c.get("region", "centro"),
        "precio_actual": c["precio"],
        "alquiler_actual": c["alq"],
        "roi_actual": c["roi"],
        "var_precio_anual": c["vp"],
        "var_alquiler_anual": c["va"],
        "dias_mercado": c["dias"],
        "ine_code": "",
    })
    existing_slugs.add(slug)
    added += 1

print(f"Añadidas: {added}  Saltadas (ya en master): {skipped}")

with MASTER.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(existing_rows)
print(f"Master final: {len(existing_rows)} filas escritas en {MASTER}")
