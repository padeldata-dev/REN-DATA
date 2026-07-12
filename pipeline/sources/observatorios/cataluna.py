"""
Observatori d'Habitatge de Catalunya — Generalitat.

Dos caminos:

1) API SoQL de analisi.transparenciacatalunya.cat (dataset qww9-bvhh,
   "Lloguers d'habitatges procedents de fiances de l'INCASOL"): da el
   alquiler medio mensual (`renda`) por municipio (`nom_territori`) y
   período (`periode`). Cobertura: ~840 municipios anuales 2019+, ~700
   en años anteriores. Pública sin API key.

2) Fallback: CSV manual en data/raw/cataluna_*.csv (formato legado).

Política: si la API responde, se usa siempre. Snapshot crudo en
data/raw/cataluna_lloguer_api_{YYYY-MM-DD}.json.
"""
import re
import csv
import json
import unicodedata
from datetime import date
from pathlib import Path
import requests
from ...config import RAW_DIR, USER_AGENT

API_URL = "https://analisi.transparenciacatalunya.cat/resource/qww9-bvhh.json"
# La v3 (POST /api/v3/views/.../query.json) exige "authentication_required" (app
# token) desde 2026. El endpoint legado SODA 2.1 (GET /resource/{id}.json con
# parámetros $select/$where/$group/$order) sigue siendo público, sin token.
# Período preferido: "gener-desembre" (año completo) → más estable.
# Si no hay datos del año completo aún, fallback al período más reciente disponible.
PREFERRED_PERIODE = "gener-desembre"
PAGE_SIZE = 5000


# Artículos en catalán que la API publica como sufijo: "Escala, l'", "Vendrell, el".
# Para que casen con los nombres del master (que llevan el artículo delante)
# movemos el artículo al principio antes de normalizar.
_CAT_ARTICLE_RE = re.compile(r"^(.+),\s*(l['’]|el|la|els|les)$", flags=re.IGNORECASE)


def _normalize(s: str) -> str:
    s = s.strip()
    m = _CAT_ARTICLE_RE.match(s)
    if m:
        body, art = m.group(1), m.group(2).lower().replace("’", "'")
        # 'l'' va pegado al nombre, 'el' va con espacio
        sep = "" if art.startswith("l'") else " "
        s = f"{art}{sep}{body}"
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


def _api_get(params: dict, timeout: int = 30) -> list | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    try:
        r = requests.get(API_URL, params=params, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[CATALUNA-API] error: {e}")
        return None


def _latest_year(timeout: int = 30) -> str | None:
    """Devuelve el último 'any' con datos a nivel Municipi."""
    params = {
        "$select": "any, count(*) as n",
        "$where": "ambit_territorial='Municipi'",
        "$group": "any",
        "$order": "any DESC",
        "$limit": 50,
    }
    rows = _api_get(params, timeout=timeout)
    if not rows: return None
    try:
        return str(rows[0]["any"])
    except (KeyError, IndexError):
        return None


def _best_periode(year: str, timeout: int = 30) -> str | None:
    """Para el año dado, devuelve 'gener-desembre' si existe; si no, el período con más registros."""
    params = {
        "$select": "periode, count(*) as n",
        "$where": f"ambit_territorial='Municipi' AND any='{year}'",
        "$group": "periode",
        "$order": "n DESC",
        "$limit": 20,
    }
    rows = _api_get(params, timeout=timeout)
    if not rows: return None
    periodes = [r.get("periode") for r in rows if r.get("periode")]
    if PREFERRED_PERIODE in periodes:
        return PREFERRED_PERIODE
    return periodes[0] if periodes else None


def fetch_api(year: str | None = None, periode: str | None = None,
              timeout: int = 30) -> dict:
    """Devuelve {nombre_norm: {'alquiler': X, 'fuente_anio': 'YYYY', 'codi': '...'}}.

    Estrategia:
      1. Si year es None, busca el más reciente con datos a nivel Municipi.
      2. Si periode es None, prefiere 'gener-desembre' (año completo); si no
         existe ese año, usa el período con más registros del año dado.
      3. Pagina la respuesta y filtra registros con `renda` numérica.
      4. Guarda snapshot crudo en data/raw/.
    """
    if year is None:
        year = _latest_year(timeout=timeout)
        if not year:
            print("[CATALUNA-API] no se pudo obtener el año más reciente")
            return {}
    if periode is None:
        periode = _best_periode(year, timeout=timeout) or PREFERRED_PERIODE
    print(f"[CATALUNA-API] usando any={year} periode={periode}")

    all_rows: list[dict] = []
    offset = 0
    while True:
        params = {
            "$select": "codi_territorial, nom_territori, any, periode, habitatges, renda",
            "$where": (f"ambit_territorial='Municipi' AND any='{year}' "
                       f"AND periode='{periode}' AND renda IS NOT NULL"),
            "$limit": PAGE_SIZE,
            "$offset": offset,
        }
        chunk = _api_get(params, timeout=timeout)
        if not chunk:
            break
        all_rows.extend(chunk)
        if len(chunk) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        if offset > PAGE_SIZE * 20:  # cortafuegos
            break

    snap = RAW_DIR / f"cataluna_lloguer_api_{date.today().isoformat()}.json"
    try:
        snap.write_text(
            json.dumps({"year": year, "periode": periode, "rows": all_rows},
                       ensure_ascii=False),
            encoding="utf-8")
        print(f"[CATALUNA-API] snapshot: {snap.name} ({len(all_rows)} filas)")
    except Exception as e:
        print(f"[CATALUNA-API] no se pudo escribir snapshot: {e}")

    out: dict = {}
    for row in all_rows:
        nom = (row.get("nom_territori") or "").strip()
        renda_raw = row.get("renda")
        if not nom or renda_raw in (None, ""):
            continue
        try:
            renda = float(str(renda_raw).replace(",", "."))
        except (ValueError, TypeError):
            continue
        out[_normalize(nom)] = {
            "alquiler": round(renda),
            "fuente_anio": year,
            "fuente_periode": periode,
            "codi": (row.get("codi_territorial") or "").strip(),
            "habitatges": row.get("habitatges"),
        }
    print(f"[CATALUNA-API] municipios con renda: {len(out)}")
    return out


def fetch():
    """Prioriza la API; si falla, cae al CSV manual."""
    data = fetch_api()
    if data:
        return data
    p = find_file()
    if p:
        print(f"[CATALUNA] fallback CSV: {p.name}")
        return parse_csv(p)
    return {}


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
    if d:
        print(f"\nTotal municipios con datos: {len(d)}")
        sample = list(d.items())[:5]
        for k, v in sample:
            print(f"  - {k:35s} -> {v}")
    else:
        print(f"\nSin datos. INSTRUCCIONES MANUALES (fallback):")
        print(f"1. Visita https://analisi.transparenciacatalunya.cat/")
        print(f"2. Busca 'preu lloguer municipi' o 'preu venda municipi'")
        print(f"3. Descarga el CSV en {RAW_DIR}/cataluna_lloguer_2026.csv")
