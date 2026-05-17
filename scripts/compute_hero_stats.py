#!/usr/bin/env python3
"""Compute aggregate stats from the DATA[] array in index.html so we can compare
against the hero/trust-bar shown values."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "rendata_beta" / "index.html"

html = INDEX.read_text(encoding="utf-8")

# Each entry: {n:"...",cc:"...",reg:"...",roi:X.X,p:NNNN,alq:NNN,vp:N.N,va:N.N,d:NN,sl:"...",pob:NNNN,itp:N}
pat = re.compile(
    r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
    r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
    r'd:(\d+),sl:"([^"]+)"'
)
rows = []
for m in pat.finditer(html):
    rows.append({
        "n": m.group(1), "cc": m.group(2), "reg": m.group(3),
        "roi": float(m.group(4)), "p": int(m.group(5)), "alq": int(m.group(6)),
        "vp": float(m.group(7)), "va": float(m.group(8)),
        "d": int(m.group(9)), "sl": m.group(10),
    })
n = len(rows)
print(f"Cities in DATA[]: {n}")
print(f"Unique slugs: {len(set(r['sl'] for r in rows))}")
if n == 0:
    raise SystemExit(0)

avg_roi = sum(r["roi"] for r in rows) / n
avg_p   = sum(r["p"]   for r in rows) / n
avg_alq = sum(r["alq"] for r in rows) / n
avg_vp  = sum(r["vp"]  for r in rows) / n
avg_va  = sum(r["va"]  for r in rows) / n
avg_d   = sum(r["d"]   for r in rows) / n
max_roi = max(r["roi"] for r in rows)
min_roi = min(r["roi"] for r in rows)
top = sorted(rows, key=lambda r: -r["roi"])[:5]

print(f"\nAverages (over all {n} cities):")
print(f"  ROI medio:        {avg_roi:.2f}%")
print(f"  Precio medio m²:  {avg_p:,.0f}€".replace(",", "."))
print(f"  Alquiler medio:   {avg_alq:,.0f}€".replace(",", "."))
print(f"  Subida precio:    +{avg_vp:.2f}% anual")
print(f"  Subida alquiler:  +{avg_va:.2f}% anual")
print(f"  Días venta:       {avg_d:.1f}")
print(f"  Mejor ROI:        {max_roi:.1f}%  ({top[0]['n']})")
print(f"  Peor ROI:         {min_roi:.1f}%")

print(f"\nTop 5 ROI:")
for r in top:
    print(f"  {r['roi']:.1f}%  {r['n']} ({r['cc']})")

# Hero values currently shown
print("\n=== Hero KPIs (visibles) vs reales ===")
print(f"  Ciudades:         329           vs  {n}")
print(f"  ROI medio:        6,7%          vs  {avg_roi:.2f}%")
print(f"  Mejor ROI:        7,5%          vs  {max_roi:.1f}%")
print(f"  Subida media m²:  ↑11%          vs  ↑{avg_vp:.1f}%")
