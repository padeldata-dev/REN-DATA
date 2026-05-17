#!/usr/bin/env python3
"""Find cities present in index.html DATA[] but missing from cities_master.csv."""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "pipeline" / "data" / "cities_master.csv"
INDEX = ROOT / "rendata_beta" / "index.html"

with MASTER.open(encoding="utf-8") as f:
    master_slugs = {r["slug"] for r in csv.DictReader(f)}

html = INDEX.read_text(encoding="utf-8")
pat = re.compile(
    r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
    r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
    r'd:(\d+),sl:"([^"]+)"'
)
data_entries = []
for m in pat.finditer(html):
    data_entries.append({
        "n": m.group(1), "cc": m.group(2), "reg": m.group(3),
        "roi": float(m.group(4)), "p": int(m.group(5)), "alq": int(m.group(6)),
        "vp": float(m.group(7)), "va": float(m.group(8)),
        "d": int(m.group(9)), "sl": m.group(10),
    })

data_slugs = {e["sl"] for e in data_entries}
orphans = [e for e in data_entries if e["sl"] not in master_slugs]
not_in_data = master_slugs - data_slugs

print(f"DATA[] entries: {len(data_entries)}")
print(f"Master CSV entries: {len(master_slugs)}")
print(f"Orphans (in DATA, NOT in master): {len(orphans)}")
for o in orphans:
    print(f"  {o['sl']:<35} {o['n']:<30} {o['cc']:<20} roi={o['roi']} p={o['p']} alq={o['alq']}")
print(f"\nIn master but not in DATA[]: {len(not_in_data)}")
for s in sorted(not_in_data):
    print(f"  {s}")
