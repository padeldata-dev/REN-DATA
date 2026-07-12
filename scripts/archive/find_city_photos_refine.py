#!/usr/bin/env python3
"""Segunda pasada: ciudades con resultados pobres - probar nuevas queries."""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"

# Ciudades con resultados malos en la primera pasada y queries alternativas
REFINE = {
    "errenteria": ["Errenteria casco", "Rentería Gipuzkoa", "Errenteria iglesia", "Errenteria plaza"],
    "salt": ["Salt Catalunya", "Salt municipi Girona", "Salt vell", "Salt poble"],
    "arteixo": ["Arteixo concello", "Arteixo Galicia ria", "Inditex Arteixo", "Arteixo plaza"],
    "coria-del-rio": ["Coria del Río ayuntamiento", "Coria del Río Guadalquivir", "Coria del Río Sevilla", "Coria Sevilla iglesia"],
    "crevillent": ["Crevillent Alicante", "Crevillente", "Crevillent panoramica", "Crevillent vista"],
    "villaviciosa-de-odon": ["Villaviciosa de Odón Madrid", "Villaviciosa de Odón centro", "Villaviciosa de Odón vista"],
    "barbera-del-valles": ["Barberà del Vallès ajuntament", "Barberà del Vallès centre", "Barbera del Valles"],
    "el-vendrell": ["El Vendrell Tarragona", "El Vendrell centre", "El Vendrell Casa Pau Casals"],
    "los-palacios-y-villafranca": ["Los Palacios y Villafranca Sevilla", "Los Palacios Villafranca ayuntamiento", "Los Palacios iglesia"],
    "puerto-real": ["Puerto Real ayuntamiento", "Puerto Real Cádiz centro", "Puerto Real iglesia"],
    "manises": ["Manises Valencia centro", "Manises ayuntamiento", "Manises Iglesia"],
    "aldaia": ["Aldaia centro", "Aldaia Valencia", "Aldaia iglesia"],
    "alaquas": ["Alaquàs castell", "Alaquas Valencia", "Alaquas centre"],
    "sant-joan-despi": ["Sant Joan Despí ajuntament", "Sant Joan Despí centre", "Sant Joan Despí Torre Jujol"],
    "camargo": ["Maliaño Camargo", "Muriedas Camargo", "Camargo ayuntamiento Cantabria"],
    "leioa": ["Leioa centro", "Leioa Bilbao", "Leioa udaletxea"],
    "san-roque": ["San Roque Cádiz centro", "San Roque municipal", "Sotogrande San Roque"],
}


def search_wmc(query, limit=8):
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


def best_image(data, slug_terms=None):
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
        if ratio < 1.2:
            continue
        title = p.get("title", "").lower()
        skip = ["coat", "escudo", "bandera", "flag", "logo", "mapa", "mtn25", "ortof"]
        if any(s in title for s in skip):
            continue
        score = 0
        if w >= 2400:
            score += 10
        elif w >= 1800:
            score += 6
        elif w >= 1200:
            score += 2
        if ratio >= 2.0:
            score += 5
        elif ratio >= 1.5:
            score += 2
        boost = ["panoram", "vista", "skyline", "ayuntamiento", "ajuntament", "udaletxea", "centro", "centre", "casco", "casa", "iglesia", "torre", "castell", "ria"]
        if any(b in title for b in boost):
            score += 3
        # Penalize off-topic
        off = ["dead sea", "petroglif", "mtn25", "industrial", "polígon", "cementeri", "salt formation", "rio turia"]
        if any(o in title for o in off):
            score -= 8
        if slug_terms:
            for st in slug_terms:
                if st.lower() in title:
                    score += 4
        candidates.append((score, w, h, info["url"], p.get("title", "")))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0]


def main():
    existing_path = ROOT / "data" / "city_photos_results.json"
    existing = json.loads(existing_path.read_text(encoding="utf-8"))

    for slug, queries in REFINE.items():
        print(f"[refine] {slug}", flush=True)
        slug_terms = [t for t in slug.split("-") if len(t) > 2]
        best = None
        best_score = -1
        used_query = None
        for q in queries:
            data = search_wmc(q, limit=8)
            sel = best_image(data, slug_terms=slug_terms)
            if sel and sel[0] > best_score:
                best = sel
                best_score = sel[0]
                used_query = q
            time.sleep(0.2)
        if best:
            score, w, h, url, title = best
            current = existing.get(slug)
            current_score = current["score"] if current else -1
            if score > current_score:
                existing[slug] = {"url": url, "width": w, "height": h, "title": title, "query": used_query, "score": score}
                print(f"  -> NEW [{score}] {w}x{h} {title}")
            else:
                print(f"  -> kept old (new {score} <= old {current_score}): {title}")
        else:
            print(f"  -> nothing better")

    existing_path.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nUpdated {existing_path}")


if __name__ == "__main__":
    main()
