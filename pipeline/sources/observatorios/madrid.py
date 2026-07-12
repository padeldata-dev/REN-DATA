"""
Observatorio de la Vivienda — Comunidad de Madrid.

Dos fuentes complementarias:

1) CSV/Excel manual con precios por municipio (datos.comunidad.madrid, sección
   Vivienda). Sirve para enriquecer cities con precio €/m² y alquiler.

2) API CKAN del portal de datos abiertos (datastore_search) con series
   regionales agregadas (compraventas, superficie media, duración e interés
   medio de hipotecas, % tipo fijo/variable). Resource id por defecto:
   a13f02f2-e236-4a79-a50c-30364fe2436d — 2004 a 2025, 15 series, sin
   desagregación municipal. Se guarda snapshot en data/raw/.
"""
import re
import csv
import json
import unicodedata
from datetime import date
from pathlib import Path
import requests
from openpyxl import load_workbook
from ...config import RAW_DIR, USER_AGENT

API_BASE = "https://datos.comunidad.madrid/api/3/action/datastore_search"
OBSERVATORIO_RESOURCE_ID = "a13f02f2-e236-4a79-a50c-30364fe2436d"

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

def fetch_observatorio_api(resource_id: str = OBSERVATORIO_RESOURCE_ID,
                           timeout: int = 30) -> dict:
    """Descarga las series regionales del Observatorio de la Vivienda vía
    CKAN datastore_search y guarda un snapshot crudo.

    Devuelve un dict {concepto: {anio: {'valor': float, 'unidad': str}}} con
    los 15 indicadores agregados de la Comunidad de Madrid (2004-2025).
    Estos datos NO están desagregados por municipio: el recurso publicado
    sólo trae el total regional ("Tipo territorio" = "Otros"). No se usa para
    enriquecer cities por municipio, pero queda disponible para análisis CCAA.
    """
    params = {"resource_id": resource_id, "limit": 5000}
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    try:
        r = requests.get(API_BASE, params=params, headers=headers, timeout=timeout)
        r.raise_for_status()
        payload = r.json()
    except Exception as e:
        print(f"[MADRID-API] error: {e}")
        return {}
    if not payload.get("success"):
        print(f"[MADRID-API] respuesta no-success: {payload}")
        return {}

    snap = RAW_DIR / f"madrid_observatorio_{date.today().isoformat()}.json"
    try:
        snap.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"[MADRID-API] no se pudo escribir snapshot {snap}: {e}")

    records = payload.get("result", {}).get("records", [])
    series: dict = {}
    for row in records:
        concepto = (row.get("Concepto") or "").strip()
        anio = row.get("Año") or row.get("Ano")
        valor_raw = (row.get("Valor") or "").strip()
        unidad = (row.get("Unidad") or "").strip()
        if not concepto or anio in (None, ""):
            continue
        try:
            valor = float(valor_raw.replace(",", "."))
        except (ValueError, AttributeError):
            continue
        series.setdefault(concepto, {})[int(anio)] = {"valor": valor, "unidad": unidad}
    print(f"[MADRID-API] obtenidos {len(records)} registros en {len(series)} series "
          f"({sum(len(v) for v in series.values())} puntos)")
    return series


def latest_values(series: dict) -> dict:
    """Devuelve {concepto: {anio_max, valor, unidad}} con el último dato de cada serie."""
    out = {}
    for concepto, anios in series.items():
        if not anios:
            continue
        amax = max(anios)
        out[concepto] = {"anio": amax, **anios[amax]}
    return out


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
    print(f"CSV municipios: {len(d)} entradas")
    if not d:
        print(f"\nINSTRUCCIONES MANUALES (precios por municipio):")
        print(f"1. Visita https://datos.comunidad.madrid/dataset?theme=Vivienda")
        print(f"2. Descarga 'Precios de vivienda por municipio' (CSV)")
        print(f"3. Guárdalo en {RAW_DIR}/madrid_vivienda_2026.csv")

    print(f"\nAPI Observatorio (series regionales agregadas):")
    api = fetch_observatorio_api()
    if api:
        latest = latest_values(api)
        for concepto, info in latest.items():
            print(f"  · {concepto[:90]:90s}  {info['anio']}  {info['valor']:>10.2f} {info['unidad']}")
