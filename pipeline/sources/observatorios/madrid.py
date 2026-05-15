"""
Observatorio de la Vivienda — Comunidad de Madrid.

Datos abiertos en https://www.comunidad.madrid/transparencia/datos-abiertos
y datos.madrid.es. Publica precios de compra y alquiler por municipio.

Estrategia: descarga manual del CSV/Excel a data/raw/madrid_vivienda_*.{csv,xlsx}
o intentar fetch directo a la URL del dataset (algunas son accesibles).
"""
import re
import csv
import unicodedata
from pathlib import Path
import requests
from openpyxl import load_workbook
from ...config import RAW_DIR, USER_AGENT

def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).lower().strip()

def find_file() -> Path | None:
    cands = sorted(RAW_DIR.glob("madrid_vivienda*.csv"), reverse=True) + \
            sorted(RAW_DIR.glob("madrid_vivienda*.xlsx"), reverse=True)
    return cands[0] if cands else None

def parse_csv(p: Path) -> dict:
    """{nombre_norm: {'precio': X, 'alquiler': Y}}."""
    out = {}
    try:
        with open(p, encoding="utf-8") as f:
            sample = f.read(2048)
            f.seek(0)
            sniff = csv.Sniffer().sniff(sample, delimiters=",;|\t")
            r = csv.DictReader(f, dialect=sniff)
            for row in r:
                muni = None
                for k in row:
                    if k and "MUNICIPIO" in k.upper():
                        muni = row[k]; break
                if not muni: continue
                entry = {}
                for k, v in row.items():
                    if not k or v is None: continue
                    ku = k.upper()
                    if "PRECIO" in ku and "M2" in ku.replace("²","2"):
                        try: entry["precio"] = round(float(v.replace(",",".")))
                        except: pass
                    elif "ALQUILER" in ku and ("M2" in ku.replace("²","2") or "MENSUAL" in ku):
                        try: entry["alquiler"] = round(float(v.replace(",",".")))
                        except: pass
                if entry:
                    out[_normalize(muni)] = entry
    except Exception as e:
        print(f"[MADRID] error parseando {p}: {e}")
    return out

def fetch():
    p = find_file()
    if not p:
        return {}
    if p.suffix == ".csv":
        return parse_csv(p)
    # Para xlsx similar a MIVAU
    return {}

def match_to_cities(data: dict, cities: list) -> dict:
    out = {}
    for c in cities:
        if c.get("ccaa") != "C. de Madrid": continue
        n = _normalize(c["nombre"])
        if n in data:
            out[c["slug"]] = data[n]
    print(f"[MADRID] match: {len(out)} ciudades de Madrid CCAA")
    return out

if __name__ == "__main__":
    d = fetch()
    print(f"Total: {len(d)}")
    if not d:
        print(f"\nINSTRUCCIONES MANUALES:")
        print(f"1. Visita https://datos.comunidad.madrid/dataset?theme=Vivienda")
        print(f"2. Descarga 'Precios de vivienda por municipio' (CSV)")
        print(f"3. Guárdalo en {RAW_DIR}/madrid_vivienda_2026.csv")
