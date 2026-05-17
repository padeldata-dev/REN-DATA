#!/usr/bin/env python3
"""Batch 3: descarga 15 panoramicas adicionales de Wikimedia Commons."""
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
    ("valladolid-hero", "Valladolid",
     "https://upload.wikimedia.org/wikipedia/commons/9/90/Panor%C3%A1mica_de_Valladolid_desde_la_Universidad_UNO.jpg"),
    ("gijon-hero", "Gijón",
     "https://upload.wikimedia.org/wikipedia/commons/1/17/Atardecer_en_el_puerto_deportivo._Gij%C3%B3n._-_Flickr_-_David_A.L..jpg"),
    ("vigo-hero", "Vigo",
     "https://upload.wikimedia.org/wikipedia/commons/c/cc/Vigo_-_Panor%C3%A1mica_07.jpg"),
    ("a-coruna-hero", "A Coruña",
     "https://upload.wikimedia.org/wikipedia/commons/4/41/A_Coru%C3%B1a%2C_vista_panor%C3%A1mica_-_panoramio.jpg"),
    ("vitoria-hero", "Vitoria",
     "https://upload.wikimedia.org/wikipedia/commons/a/af/Panor%C3%A1mica_Vitoria-Gasteiz.jpg"),
    ("merida-hero", "Mérida",
     "https://upload.wikimedia.org/wikipedia/commons/7/79/Puente_Romano_sobre_El_Guadiana%2C_M%C3%A9rida.jpg"),
    ("huelva-hero", "Huelva",
     "https://upload.wikimedia.org/wikipedia/commons/9/9c/Panor%C3%A1mica_puerto_de_Huelva_02.JPG"),
    ("jaen-hero", "Jaén",
     "https://upload.wikimedia.org/wikipedia/commons/2/2f/Ja%C3%A9n_-_Panor%C3%A1mica_desde_el_Castillo-Parador_02.jpg"),
    ("almeria-hero", "Almería",
     "https://upload.wikimedia.org/wikipedia/commons/2/28/Panor%C3%A1mica_de_Almer%C3%ADa.jpg"),
    ("castellon-hero", "Castellón",
     "https://upload.wikimedia.org/wikipedia/commons/5/57/Ciudad_de_Castell%C3%B3n_de_la_Plana_%28Espa%C3%B1a%29._Panor%C3%A1mica_urbana_2025.jpg"),
    ("albacete-hero", "Albacete",
     "https://upload.wikimedia.org/wikipedia/commons/1/16/Vista_panor%C3%A1mica_sureste_de_la_plaza_de_toros_de_Albacete.jpg"),
    ("badajoz-hero", "Badajoz",
     "https://upload.wikimedia.org/wikipedia/commons/0/09/Vista_de_la_Badajoz_desde_la_Alcazaba.JPG"),
    ("leon-hero", "León",
     "https://upload.wikimedia.org/wikipedia/commons/b/bc/Panor%C3%A1mica_de_la_Plaza_Mayor_de_Le%C3%B3n_%28Espa%C3%B1a%29.JPG"),
    ("lleida-hero", "Lleida",
     "https://upload.wikimedia.org/wikipedia/commons/1/12/Pano_Lleida.jpg"),
    ("tarragona-hero", "Tarragona",
     "https://upload.wikimedia.org/wikipedia/commons/2/25/Tarragona_-_Panor%C3%A1mica_01.jpg"),
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
            print(f"> {name}: descargando...", flush=True)
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
