#!/usr/bin/env python3
"""Descarga e optimiza panoramicas de Wikimedia Commons para el hero rotativo."""
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

# (slug, nombre, URL de Wikimedia Commons)
CITIES = [
    ("toledo-hero", "Toledo",
     "https://upload.wikimedia.org/wikipedia/commons/3/3b/Panor%C3%A1mica_del_Tajo_ba%C3%B1ando_Toledo_-_panoramio.jpg"),
    ("segovia-hero", "Segovia",
     "https://upload.wikimedia.org/wikipedia/commons/4/4d/Segovia_-_02_edited.jpg"),
    ("sevilla-hero", "Sevilla",
     "https://upload.wikimedia.org/wikipedia/commons/2/26/Panoramica_de_los_alrededores_de_Sevilla_desdel_el_Mirador_01.jpg"),
    ("granada-hero", "Granada",
     "https://upload.wikimedia.org/wikipedia/commons/c/cf/Alhambra_evening_panorama_Mirador_San_Nicolas_sRGB-1.jpg"),
    ("san-sebastian-hero", "San Sebastián",
     "https://upload.wikimedia.org/wikipedia/commons/f/fa/San_Sebasti%C3%A1n_-_panoramio.jpg"),
    ("bilbao-hero", "Bilbao",
     "https://upload.wikimedia.org/wikipedia/commons/0/05/Bilbao_-_Panor%C3%A1mica_desde_el_Mirador_de_Artxandaa_%28mayo_2025%29_04.jpg"),
    ("barcelona-hero", "Barcelona",
     "https://upload.wikimedia.org/wikipedia/commons/8/83/Panor%C3%A1mica_desde_el_parque_G%C3%BCell_de_Barcelona_-_panoramio.jpg"),
    ("valencia-hero", "Valencia",
     "https://upload.wikimedia.org/wikipedia/commons/e/e8/Vista_panor%C3%A1mica_de_Valencia_desde_las_Torres_de_Cuart%2C_Espa%C3%B1a%2C_2014-06-30%2C_DD_101-104_PAN.JPG"),
    ("salamanca-hero", "Salamanca",
     "https://upload.wikimedia.org/wikipedia/commons/1/12/Panor%C3%A1mica_de_Salamanca_-_panoramio.jpg"),
    ("cordoba-hero", "Córdoba",
     "https://upload.wikimedia.org/wikipedia/commons/9/90/C%C3%B3rdoba%2C_panor%C3%A1micas_1990_03.jpg"),
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
    # Iterative quality reduction to stay under target_kb
    target_bytes = target_kb * 1024
    for q in (88, 85, 82, 78, 75, 72, 68, 65, 60, 55):
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) <= target_bytes:
            return data
    return data  # devuelve la última (puede ser >250KB pero es la más comprimida)


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
            print(f"  OK guardado en {out_path.relative_to(ROOT)} ({len(data)//1024} KB)", flush=True)
        except Exception as e:
            print(f"  ERR: {e}", file=sys.stderr, flush=True)
            results.append((name, slug, 0))

    print("\n=== RESUMEN ===")
    for name, slug, kb in results:
        status = "OK" if kb > 0 and kb <= TARGET_KB else ("WARN" if kb > TARGET_KB else "FAIL")
        print(f"  [{status}] {name}: {kb} KB  ({slug}.jpg)")


if __name__ == "__main__":
    main()
