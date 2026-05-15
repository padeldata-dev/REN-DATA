"""
Observatorio de la Vivienda — Junta de Andalucía.

Publica trimestralmente el 'Sistema de Información Multiterritorial de
Andalucía (SIMA)' con precios de compra y alquiler. Cobertura parcial
(capitales y municipios > 50k habitantes).

Acceso: descarga manual desde
https://www.juntadeandalucia.es/institutodeestadisticaycartografia
"""
import re
import csv
import unicodedata
from pathlib import Path
from ...config import RAW_DIR

def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", s).lower().strip()

def find_file() -> Path | None:
    cands = sorted(RAW_DIR.glob("andalucia_*.csv"), reverse=True)
    return cands[0] if cands else None

def parse_csv(p: Path) -> dict:
    out = {}
    try:
        with open(p, encoding="utf-8", errors="ignore") as f:
            sample = f.read(2048); f.seek(0)
            try: sniff = csv.Sniffer().sniff(sample, delimiters=",;|\t")
            except: sniff = csv.excel
            r = csv.DictReader(f, dialect=sniff)
            for row in r:
                muni = None
                for k in row:
                    if k and "MUNICIPIO" in k.upper():
                        muni = row[k]; break
                if not muni: continue
                entry = out.setdefault(_normalize(muni), {})
                for k, v in row.items():
                    if not k or v is None: continue
                    ku = k.upper()
                    try: vf = float(str(v).replace(",", "."))
                    except: continue
                    if "ALQUIL" in ku: entry["alquiler"] = round(vf)
                    elif "PRECIO" in ku or "VENTA" in ku: entry["precio"] = round(vf)
    except Exception as e:
        print(f"[ANDALUCIA] error: {e}")
    return out

def fetch():
    p = find_file()
    return parse_csv(p) if p else {}

def match_to_cities(data: dict, cities: list) -> dict:
    out = {}
    for c in cities:
        if c.get("ccaa") != "Andalucía": continue
        n = _normalize(c["nombre"])
        if n in data:
            out[c["slug"]] = data[n]
    print(f"[ANDALUCIA] match: {len(out)} ciudades de Andalucía")
    return out

if __name__ == "__main__":
    d = fetch()
    if not d:
        print(f"\nINSTRUCCIONES MANUALES:")
        print(f"1. Visita https://www.juntadeandalucia.es/institutodeestadisticaycartografia")
        print(f"2. Busca 'Estadística de Vivienda' y descarga el último CSV trimestral")
        print(f"3. Guárdalo en {RAW_DIR}/andalucia_vivienda_2026.csv")
