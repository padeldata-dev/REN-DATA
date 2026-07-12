#!/usr/bin/env python3
"""Batch 2: descarga 11 panoramicas adicionales de Wikimedia Commons."""
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
    ("zaragoza-hero", "Zaragoza",
     "https://upload.wikimedia.org/wikipedia/commons/b/b8/Zaragoza_-_Vistas_Generales_-_El_Pilar_y_el_R%C3%ADo_Ebro.jpg"),
    ("malaga-hero", "Málaga",
     "https://upload.wikimedia.org/wikipedia/commons/9/94/Vista_panor%C3%A1mica_de_M%C3%A1laga_001.jpg"),
    ("palma-hero", "Palma",
     "https://upload.wikimedia.org/wikipedia/commons/2/28/Panor%C3%A1mica_19J_Palma_de_Mallorca_%285851999454%29.jpg"),
    ("burgos-hero", "Burgos",
     "https://upload.wikimedia.org/wikipedia/commons/8/80/Panor%C3%A1mica_de_Burgos_-_Mirador_del_Castillo.jpg"),
    ("cuenca-hero", "Cuenca",
     "https://upload.wikimedia.org/wikipedia/commons/e/ed/Panor%C3%A1mica_de_Cuenca%2C_Espa%C3%B1a.jpg"),
    ("caceres-hero", "Cáceres",
     "https://upload.wikimedia.org/wikipedia/commons/4/4a/Panor%C3%A1mica_de_C%C3%A1ceres_2024.jpg"),
    ("santiago-de-compostela-hero", "Santiago de Compostela",
     "https://upload.wikimedia.org/wikipedia/commons/5/5e/Panor%C3%A1mica_de_Santiago_de_Compostela.jpg"),
    ("pamplona-hero", "Pamplona",
     "https://upload.wikimedia.org/wikipedia/commons/f/f2/Panor%C3%A1mica_de_Pamplona_-_panoramio.jpg"),
    ("alicante-hero", "Alicante",
     "https://upload.wikimedia.org/wikipedia/commons/2/28/Vista_de_Alicante%2C_Espa%C3%B1a%2C_2014-07-04%2C_DD_71-75_PAN.JPG"),
    ("murcia-hero", "Murcia",
     "https://upload.wikimedia.org/wikipedia/commons/6/6b/38_panor%C3%A1mica_murcia_20170917_122648.jpg"),
    ("cadiz-hero", "Cádiz",
     "https://upload.wikimedia.org/wikipedia/commons/6/69/Panor%C3%A1mica_Puerta_Tierra_C%C3%A1diz_1_edited.jpg"),
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
