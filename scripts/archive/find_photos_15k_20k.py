#!/usr/bin/env python3
"""Busca fotos en Wikimedia Commons para las 110 ciudades 15k-20k."""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "data" / "cities_15k_20k_metadata.json"

USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"

ALT_QUERIES = ["{name}", "{name} {prov}", "panorámica {name}", "vista {name}", "{name} centro"]


def search_wmc(query, limit=10):
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
        w = info.get("width", 0); h = info.get("height", 0)
        if h == 0:
            continue
        ratio = w / h
        if ratio < 1.2:
            continue
        title = p.get("title", "").lower()
        skip_words = ["coat", "escudo", "bandera", "flag", "logo", "mapa", "map", "ortof", "blason"]
        if any(s in title for s in skip_words):
            continue
        score = 0
        if w >= 2400: score += 10
        elif w >= 1800: score += 6
        elif w >= 1200: score += 2
        if ratio >= 2.0: score += 5
        elif ratio >= 1.5: score += 2
        boost = ["panoram", "vista", "skyline", "aerial", "view", "cityscape", "centro", "ayuntamiento", "casco", "pueblo", "plaza"]
        if any(b in title for b in boost): score += 3
        candidates.append((score, w, h, info["url"], p.get("title", "")))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0]


def find_for_city(name, prov):
    queries = [q.format(name=name, prov=prov) for q in ALT_QUERIES]
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
        if best_score >= 13:
            break
        time.sleep(0.15)
    return best, used_query


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    out_path = ROOT / "data" / "city_photos_15k_20k.json"
    results = {}
    if out_path.exists():
        try:
            results = json.loads(out_path.read_text(encoding="utf-8"))
        except Exception:
            results = {}

    for c in cities:
        slug = c["slug"]
        if slug in results and results[slug]:
            print(f"[skip] {slug}", flush=True)
            continue
        name = c["name"]; prov = c["prov"]
        print(f"[search] {slug} ({name}, {prov})", flush=True)
        result, q = find_for_city(name, prov)
        if result:
            score, w, h, url, title = result
            results[slug] = {"url": url, "width": w, "height": h, "title": title, "query": q, "score": score}
            print(f"  -> [{score}] {w}x{h}", flush=True)
        else:
            results[slug] = None
            print(f"  -> NONE FOUND", flush=True)
        out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
