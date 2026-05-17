#!/usr/bin/env python3
"""Verifica que las 110 nuevas ciudades 15k-20k esten en index, sitemap y CCAA."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_15k_20k_metadata.json"

cities = json.loads(META.read_text(encoding="utf-8"))
index_html = (BETA / "index.html").read_text(encoding="utf-8")
sitemap = (BETA / "sitemap.xml").read_text(encoding="utf-8")

CCAA_FILES = {
    "pais-vasco":"ccaa-pais-vasco.html","cataluna":"ccaa-cataluna.html",
    "andalucia":"ccaa-andalucia.html","baleares":"ccaa-baleares.html",
    "canarias":"ccaa-canarias.html","galicia":"ccaa-galicia.html",
    "comunitat-valenciana":"ccaa-comunitat-valenciana.html",
    "castilla-la-mancha":"ccaa-castilla-la-mancha.html",
    "madrid":"ccaa-madrid.html","cantabria":"ccaa-cantabria.html",
    "murcia":"ccaa-murcia.html","extremadura":"ccaa-extremadura.html",
    "navarra":"ccaa-navarra.html","castilla-y-leon":"ccaa-castilla-y-leon.html",
    "aragon":"ccaa-aragon.html","asturias":"ccaa-asturias.html",
    "la-rioja":"ccaa-la-rioja.html",
}
ccaa_htmls = {k:(BETA/v).read_text(encoding="utf-8") for k,v in CCAA_FILES.items()}

err = 0
for c in cities:
    slug = c["slug"]
    if f'sl:"{slug}"' not in index_html:
        print(f"[ERR] {slug}: not in index"); err+=1
    if f"/rentabilidad-{slug}.html" not in sitemap:
        print(f"[ERR] {slug}: not in sitemap"); err+=1
    cs = c["ccaa_slug"]
    if cs in ccaa_htmls:
        if f"rentabilidad-{slug}.html" not in ccaa_htmls[cs]:
            print(f"[ERR] {slug}: not in ccaa-{cs}.html"); err+=1
    else:
        print(f"[ERR] {slug}: no ccaa mapping for {cs}"); err+=1
print(f"\nErrors: {err} / {len(cities)} cities")
