#!/usr/bin/env python3
"""Busca fotos landscape >=1800px de ancho en Wikimedia Commons para 41 ciudades."""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"

# (slug, query_name) - for searches
CITIES = [
    ("santurtzi", "Santurtzi"),
    ("portugalete", "Portugalete"),
    ("vilafranca-del-penedes", "Vilafranca del Penedès"),
    ("puerto-real", "Puerto Real Cádiz"),
    ("santa-eularia-des-riu", "Santa Eulària des Riu"),
    ("el-vendrell", "El Vendrell"),
    ("ripollet", "Ripollet"),
    ("errenteria", "Errenteria"),
    ("sant-adria-de-besos", "Sant Adrià de Besòs"),
    ("arucas", "Arucas Gran Canaria"),
    ("oleiros", "Oleiros Galicia"),
    ("los-palacios-y-villafranca", "Los Palacios y Villafranca"),
    ("los-realejos", "Los Realejos"),
    ("montcada-i-reixac", "Montcada i Reixac"),
    ("la-vila-joiosa", "Vila Joiosa"),
    ("sant-joan-despi", "Sant Joan Despí"),
    ("azuqueca-de-henares", "Azuqueca de Henares"),
    ("aldaia", "Aldaia"),
    ("salt", "Salt Girona"),
    ("arteixo", "Arteixo"),
    ("san-roque", "San Roque Cádiz"),
    ("petrer", "Petrer"),
    ("barbera-del-valles", "Barberà del Vallès"),
    ("nijar", "Níjar Almería"),
    ("ames", "Ames Galicia"),
    ("ingenio", "Ingenio Gran Canaria"),
    ("leioa", "Leioa"),
    ("sant-pere-de-ribes", "Sant Pere de Ribes"),
    ("manises", "Manises Valencia"),
    ("la-vall-d-uixo", "Vall d'Uixó"),
    ("xirivella", "Xirivella"),
    ("el-campello", "Campello Alicante"),
    ("coria-del-rio", "Coria del Río"),
    ("arcos-de-la-frontera", "Arcos de la Frontera"),
    ("culleredo", "Culleredo"),
    ("crevillent", "Crevillent"),
    ("sesena", "Seseña"),
    ("catarroja", "Catarroja"),
    ("camargo", "Camargo Cantabria"),
    ("alaquas", "Alaquàs"),
    ("villaviciosa-de-odon", "Villaviciosa de Odón"),
]

ALT_QUERIES = ["{name}", "{name} ciudad", "panorámica {name}", "vista {name}"]


def search_wmc(query, limit=10):
    """Llama a la WMC API con search en file namespace."""
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  [ERR] {query}: {e}", file=sys.stderr)
        return None


def best_image(data):
    """De los resultados WMC, escoge mejor JPEG landscape >=1800px."""
    if not data or "query" not in data or "pages" not in data["query"]:
        return None
    pages = list(data["query"]["pages"].values())
    candidates = []
    for p in pages:
        ii = p.get("imageinfo", [])
        if not ii:
            continue
        info = ii[0]
        mime = info.get("mime", "")
        if "jpeg" not in mime and "jpg" not in mime:
            continue
        w = info.get("width", 0)
        h = info.get("height", 0)
        if h == 0:
            continue
        ratio = w / h
        if ratio < 1.2:  # not landscape enough
            continue
        # Skip obvious flags/coats/logos
        title = p.get("title", "").lower()
        skip_words = ["coat", "escudo", "bandera", "flag", "logo", "mapa", "map", "ortof"]
        if any(s in title for s in skip_words):
            continue
        # Score
        score = 0
        if w >= 2400:
            score += 10
        elif w >= 1800:
            score += 6
        elif w >= 1200:
            score += 2
        if ratio >= 2.0:
            score += 5  # panoramic
        elif ratio >= 1.5:
            score += 2
        # Boost cityscape/vista words
        boost = ["panoram", "vista", "skyline", "aerial", "view", "cityscape", "centro", "ayuntamiento", "casco", "pueblo"]
        if any(b in title for b in boost):
            score += 3
        candidates.append((score, w, h, info["url"], p.get("title", "")))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0]


def find_for_city(slug, name):
    queries = [q.format(name=name) for q in ALT_QUERIES]
    best = None
    best_score = -1
    used_query = None
    for q in queries:
        data = search_wmc(q, limit=8)
        sel = best_image(data)
        if sel and sel[0] > best_score:
            best = sel
            best_score = sel[0]
            used_query = q
        if best_score >= 13:  # very good
            break
        time.sleep(0.2)
    return best, used_query


def main():
    results = {}
    for slug, name in CITIES:
        print(f"[search] {slug} ({name})", flush=True)
        result, q = find_for_city(slug, name)
        if result:
            score, w, h, url, title = result
            results[slug] = {
                "url": url,
                "width": w,
                "height": h,
                "title": title,
                "query": q,
                "score": score,
            }
            print(f"  -> [{score}] {w}x{h} {title}", flush=True)
        else:
            results[slug] = None
            print(f"  -> NONE FOUND", flush=True)
    out = ROOT / "data" / "city_photos_results.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
