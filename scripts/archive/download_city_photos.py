#!/usr/bin/env python3
"""Descarga fotos de Wikimedia Commons para las 7 nuevas fichas de ciudades.

Salida: rendata_beta/img/{slug}.webp redimensionado a 1400x320 (ratio banner),
optimizado con calidad iterativa hasta <=250KB.

Idempotente: si el archivo ya existe y pesa <=250KB, se omite.
"""
import io
import sys
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "rendata_beta" / "img"
TARGET_WIDTH = 1400
TARGET_HEIGHT = 320  # banner ratio approx 4.4:1
TARGET_KB = 250
USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"

CITIES = [
    ("santa-coloma-de-gramenet",
     "https://upload.wikimedia.org/wikipedia/commons/c/c1/Ajuntament_de_Santa_Coloma_de_Gramenet_-_2014_-_01.jpg"),
    ("melilla",
     "https://upload.wikimedia.org/wikipedia/commons/0/0a/Frente_de_la_Marina%2C_Melilla_la_Vieja_%282%29.jpg"),
    ("valdemoro",
     "https://upload.wikimedia.org/wikipedia/commons/4/45/Valdemoro.jpg"),
    ("ceuta",
     "https://upload.wikimedia.org/wikipedia/commons/4/4a/Vista_de_Ceuta_001.jpg"),
    ("sant-vicent-del-raspeig",
     "https://upload.wikimedia.org/wikipedia/commons/7/74/San_Vicente_del_Raspeig_desde_el_Castillo_de_Santa_B%C3%A1rbara.JPG"),
    ("colmenar-viejo",
     "https://upload.wikimedia.org/wikipedia/commons/4/49/Colmenar_Viejo_y_Sierra_de_Guadarrama%2C_desde_la_M-607.jpg"),
    ("vila-real",
     "https://upload.wikimedia.org/wikipedia/commons/f/f6/Villarreal%2C_Castell%C3%B3n.JPG"),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def crop_to_banner(im: Image.Image) -> Image.Image:
    """Redimensiona y recorta al ratio de banner 1400x320."""
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    # Calcular el ratio objetivo
    target_ratio = TARGET_WIDTH / TARGET_HEIGHT  # 4.375
    src_ratio = im.width / im.height
    if src_ratio > target_ratio:
        # Origen mas ancho -> ajustar por altura
        new_h = TARGET_HEIGHT
        new_w = int(im.width * (new_h / im.height))
        im = im.resize((new_w, new_h), Image.LANCZOS)
        # Crop centrado a TARGET_WIDTH
        left = (new_w - TARGET_WIDTH) // 2
        im = im.crop((left, 0, left + TARGET_WIDTH, TARGET_HEIGHT))
    else:
        # Origen mas alto -> ajustar por ancho
        new_w = TARGET_WIDTH
        new_h = int(im.height * (new_w / im.width))
        im = im.resize((new_w, new_h), Image.LANCZOS)
        # Crop centrado vertical a TARGET_HEIGHT (preferir tercio superior para fachadas/skylines)
        top = max(0, (new_h - TARGET_HEIGHT) // 3)
        im = im.crop((0, top, TARGET_WIDTH, top + TARGET_HEIGHT))
    return im


def save_webp(im: Image.Image, out_path: Path) -> int:
    """Guarda con calidad iterativa hasta <=TARGET_KB. Devuelve KB final."""
    quality = 88
    while quality >= 50:
        buf = io.BytesIO()
        im.save(buf, format="WEBP", quality=quality, method=6)
        size_kb = len(buf.getvalue()) / 1024
        if size_kb <= TARGET_KB or quality == 50:
            out_path.write_bytes(buf.getvalue())
            return int(size_kb)
        quality -= 5
    return -1


def process_city(slug: str, url: str) -> str:
    out_path = OUT_DIR / f"{slug}.webp"
    if out_path.exists() and out_path.stat().st_size <= TARGET_KB * 1024:
        return f"[skip] {slug}: ya existe ({out_path.stat().st_size//1024} KB)"
    print(f"[download] {slug} <- {url}", flush=True)
    data = fetch(url)
    im = Image.open(io.BytesIO(data))
    im = crop_to_banner(im)
    kb = save_webp(im, out_path)
    return f"[ok] {slug}: {kb} KB ({im.width}x{im.height})"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for slug, url in CITIES:
        try:
            results.append(process_city(slug, url))
        except Exception as e:
            results.append(f"[ERROR] {slug}: {e}")
    print("\n".join(results))


if __name__ == "__main__":
    main()
