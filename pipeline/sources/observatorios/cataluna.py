"""
Observatori d'Habitatge de Catalunya — Generalitat.

dades.gencat.cat publica el 'Índex de referència del preu del lloguer'
y 'Estadística de preus de venda' por municipio en CSV abierto.
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
    cands = sorted(RAW_DIR.glob("cataluna_*.csv"), reverse=True) + \
            sorted(RAW_DIR.glob("catalunya_*.csv"), reverse=True)
    return cands[0] if cands else None

def parse_csv(p: Path) -> dict:
    """{nombre_norm: {'alquiler': X, 'precio': Y}}."""
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
                    if k and ("MUNICIPI" in k.upper() or "MUNICIPIO" in k.upper()):
                        muni = row[k]; break
                if not muni: continue
                entry = out.setdefault(_normalize(muni), {})
                for k, v in row.items():
                    if not k or v is None or v == "": continue
                    ku = k.upper()
                    try: vf = float(str(v).replace(",", "."))
                    except: continue
                    if "LLOGUER" in ku or "ALQUIL" in ku or "RENDA" in ku:
                        entry["alquiler"] = round(vf)
                    elif "PREU" in ku or "PRECIO" in ku:
                        entry["precio"] = round(vf)
    except Exception as e:
        print(f"[CATALUNA] error: {e}")
    return out

def fetch():
    p = find_file()
    return parse_csv(p) if p else {}

def match_to_cities(data: dict, cities: list) -> dict:
    out = {}
    for c in cities:
        if c.get("ccaa") != "Cataluña": continue
        n = _normalize(c["nombre"])
        if n in data:
            out[c["slug"]] = data[n]
    print(f"[CATALUNA] match: {len(out)} ciudades de Cataluña")
    return out

if __name__ == "__main__":
    d = fetch()
    if not d:
        print(f"\nINSTRUCCIONES MANUALES:")
        print(f"1. Visita https://analisi.transparenciacatalunya.cat/")
        print(f"2. Busca 'preu lloguer municipi' y 'preu venda municipi'")
        print(f"3. Descarga los CSV y guárdalos en {RAW_DIR}/cataluna_lloguer_2026.csv")
