#!/usr/bin/env python3
"""Fix twin references in 20k-30k metadata to point only to existing cities."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "data" / "cities_20k_30k_metadata.json"

data = json.loads(META.read_text(encoding="utf-8"))
fixes = {
    "martorell": "esplugues-de-llobregat",
    "camas": "mairena-del-aljarafe",
    "sant-vicenc-dels-horts": "esplugues-de-llobregat",
    "la-pobla-de-vallbona": "paterna",
    "sant-andreu-de-la-barca": "esplugues-de-llobregat",
    "castellar-del-valles": "cerdanyola-del-valles",
    "olesa-de-montserrat": "sant-feliu-de-llobregat",
    "almonte": "isla-cristina",
    "moguer": "isla-cristina",
    "valle-de-egues": "pamplona",
    "arroyo-de-la-encomienda": "medina-del-campo",
    "esparreguera": "sant-feliu-de-llobregat",
    "aspe": "elda",
    "cartaya": "isla-cristina",
    "burlada": "pamplona",
    "san-martin-de-la-vega": "aranjuez",
    "o-porrino": "cangas-do-morrazo",
    "a-estrada": "vilagarcia-de-arousa",
}
for c in data:
    if c["slug"] in fixes:
        c["twin"] = fixes[c["slug"]]
        print(f"{c['slug']}: twin = {c['twin']}")
META.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Done")
