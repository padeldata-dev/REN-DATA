#!/usr/bin/env python3
"""Descarga 4 panoramicas de CCAA: Asturias, Canarias, Cantabria, La Rioja."""
import io
import sys
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "rendata_beta" / "img"
TARGET_WIDTH = 1440
TARGET_KB = 250
USER_AGENT = "RenData/1.0 (https://rendata.es; contact via web) Python/urllib"

CITIES = [
    ("asturias-hero", "Asturias (Oviedo)",
     "https://upload.wikimedia.org/wikipedia/commons/1/1a/Oviedo_21_by-dpc.jpg"),
    ("canarias-hero", "Canarias (Gran Canaria)",
     "https://upload.wikimedia.org/wikipedia/commons/0/04/Gran_Canaria%2C_panor%C3%A1micas_%281992%29_01.jpg"),
    ("cantabria-hero", "Cantabria (Santander)",
     "https://upload.wikimedia.org/wikipedia/commons/9/94/Santander%2C_noreste.jpg"),
    ("la-rioja-hero", "La Rioja (Logroño)",
     "https://upload.wikimedia.org/wikipedia/commons/b/b2/Logro%C3%B1o%2C_panoramica.jpg"),
]


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def optimize(raw: bytes, target_w: int, target_kb: int) -> bytes:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = img.size
    if w > target_w:
        new_h = int(h * target_w / w)
        img = img.resize((target_w, new_h), Image.LANCZOS)
    target_bytes = target_kb * 1024
    for q in (88, 85, 82, 78, 75, 72, 68, 65, 60, 55):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) <= target_bytes:
            return data
    return data


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for slug, name, url in CITIES:
        out_path = OUT_DIR / f"{slug}.jpg"
        try:
            print(f"> {name}: descargando {url[:80]}...", flush=True)
            raw = download(url)
            print(f"  - {len(raw)//1024} KB original", flush=True)
            data = optimize(raw, TARGET_WIDTH, TARGET_KB)
            out_path.write_bytes(data)
            results.append((name, slug, len(data) // 1024))
            print(f"  OK {out_path.relative_to(ROOT)} ({len(data)//1024} KB)", flush=True)
        except Exception as e:
            print(f"  ERR: {e}", file=sys.stderr, flush=True)
            results.append((name, slug, 0))

    print("\n=== RESUMEN ===")
    for name, slug, kb in results:
        status = "OK" if 0 < kb <= TARGET_KB else ("WARN" if kb > TARGET_KB else "FAIL")
        print(f"  [{status}] {name}: {kb} KB  ({slug}.jpg)")


if __name__ == "__main__":
    main()
