#!/usr/bin/env python3
"""Busca en Wikimedia Commons y descarga las fotos hero de los 10 municipios
de Málaga (expansión julio 2026). Genera img/{slug}.webp 1400x320 <=250KB
y anota los créditos en data/city_photos_wikimedia_credits.csv.
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
OUT_DIR = BETA / "img"
META = ROOT / "data" / "cities_malaga_metadata.json"
RESULTS = ROOT / "data" / "city_photos_malaga.json"
CREDITS = ROOT / "data" / "city_photos_wikimedia_credits.csv"

USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"
TARGET_WIDTH = 1400
TARGET_HEIGHT = 320
TARGET_KB = 250

ALT_QUERIES = ["{name} Málaga", "{name} panorámica", "vista {name}", "{name} pueblo", "{name}"]


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def search_wmc(query, limit=12):
    try:
        return api({
            "action": "query", "generator": "search", "gsrsearch": query,
            "gsrnamespace": "6", "gsrlimit": str(limit),
            "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
            "format": "json",
        })
    except Exception as e:
        print(f"  [ERR] {query}: {e}", file=sys.stderr)
        return None


def best_image(data):
    if not data or "query" not in data or "pages" not in data["query"]:
        return None
    candidates = []
    for p in data["query"]["pages"].values():
        ii = p.get("imageinfo", [])
        if not ii:
            continue
        info = ii[0]
        mime = info.get("mime", "")
        if "jpeg" not in mime and "jpg" not in mime:
            continue
        w = info.get("width", 0)
        h = info.get("height", 0)
        if h == 0 or w < 1000:
            continue
        ratio = w / h
        if ratio < 1.2:
            continue
        title = p.get("title", "").lower()
        skip = ["coat", "escudo", "bandera", "flag", "logo", "mapa", "map", "ortof", "blason", "iglesia interior", "retablo"]
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
        boost = ["panoram", "vista", "skyline", "aerial", "view", "pueblo", "village", "casco", "general", "plaza", "castillo"]
        if any(b in title for b in boost):
            score += 3
        ext = info.get("extmetadata", {})
        artist = ext.get("Artist", {}).get("value", "")
        lic = ext.get("LicenseShortName", {}).get("value", "")
        candidates.append((score, w, h, info["url"], p.get("title", ""), artist, lic))
    if not candidates:
        return None
    candidates.sort(key=lambda c: (-c[0], -c[1]))
    return candidates[0]


def crop_to_banner(im):
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    target_ratio = TARGET_WIDTH / TARGET_HEIGHT
    if im.width / im.height > target_ratio:
        new_h = TARGET_HEIGHT
        new_w = int(im.width * (new_h / im.height))
        im = im.resize((new_w, new_h), Image.LANCZOS)
        left = (new_w - TARGET_WIDTH) // 2
        im = im.crop((left, 0, left + TARGET_WIDTH, TARGET_HEIGHT))
    else:
        new_w = TARGET_WIDTH
        new_h = int(im.height * (new_w / im.width))
        im = im.resize((new_w, new_h), Image.LANCZOS)
        top = max(0, (new_h - TARGET_HEIGHT) // 3)
        im = im.crop((0, top, TARGET_WIDTH, top + TARGET_HEIGHT))
    return im.convert("RGB")


def save_webp(im, out_path):
    quality = 88
    while quality >= 40:
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=quality, method=6)
        kb = len(buf.getvalue()) / 1024
        if kb <= TARGET_KB or quality == 40:
            out_path.write_bytes(buf.getvalue())
            return int(kb)
        quality -= 5
    return -1


def strip_html(s):
    import re
    return re.sub(r"<[^>]+>", "", s).strip()


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    results = {}
    credits_rows = []
    for c in cities:
        slug = c["slug"]
        out = OUT_DIR / f"{slug}.webp"
        best = None
        for q in [q.format(name=c["name"]) for q in ALT_QUERIES]:
            data = search_wmc(q)
            cand = best_image(data)
            if cand and (best is None or cand[0] > best[0]):
                best = cand
            if best and best[0] >= 10:
                break
        if not best:
            print(f"[NONE] {slug}")
            results[slug] = None
            continue
        score, w, h, url, title, artist, lic = best
        results[slug] = {"url": url, "width": w, "height": h, "title": title, "score": score}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
            im = Image.open(io.BytesIO(data))
            im = crop_to_banner(im)
            kb = save_webp(im, out)
            page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
            credits_rows.append(f'{slug},"{title}","{strip_html(artist)}","{strip_html(lic)}",{page}')
            print(f"[ok] {slug}: {title} ({w}x{h}) -> {kb} KB")
        except Exception as e:
            print(f"[ERR] {slug}: {e}")
    RESULTS.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    if credits_rows:
        with CREDITS.open("a", encoding="utf-8", newline="") as f:
            f.write("\n".join(credits_rows) + "\n")
    print("done")


if __name__ == "__main__":
    main()
