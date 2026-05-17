#!/usr/bin/env python3
"""Descarga las 41 fotos seleccionadas, redimensiona a 1400x320 y guarda <=250KB."""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "rendata_beta" / "img"
TARGET_WIDTH = 1400
TARGET_HEIGHT = 320
TARGET_KB = 250
USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def crop_to_banner(im):
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    target_ratio = TARGET_WIDTH / TARGET_HEIGHT
    src_ratio = im.width / im.height
    if src_ratio > target_ratio:
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
    if im.mode != "RGB":
        im = im.convert("RGB")
    return im


def save_webp(im, out_path):
    quality = 88
    while quality >= 40:
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=quality, method=6)
        size_kb = len(buf.getvalue()) / 1024
        if size_kb <= TARGET_KB or quality == 40:
            out_path.write_bytes(buf.getvalue())
            return int(size_kb)
        quality -= 5
    return -1


def process(slug, url):
    out = OUT_DIR / f"{slug}.webp"
    if out.exists() and out.stat().st_size <= TARGET_KB * 1024:
        return f"[skip] {slug}: {out.stat().st_size // 1024} KB"
    data = fetch(url)
    im = Image.open(io.BytesIO(data))
    im = crop_to_banner(im)
    kb = save_webp(im, out)
    return f"[ok] {slug}: {kb} KB"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results_path = ROOT / "data" / "city_photos_results.json"
    photos = json.loads(results_path.read_text(encoding="utf-8"))

    results = []
    for slug, info in photos.items():
        if info is None:
            results.append(f"[ERR] {slug}: no photo found")
            continue
        try:
            r = process(slug, info["url"])
            results.append(r)
            print(r, flush=True)
        except Exception as e:
            results.append(f"[ERR] {slug}: {e}")
            print(results[-1], flush=True)
    print("\n=== summary ===")
    print("\n".join(results))


if __name__ == "__main__":
    main()
