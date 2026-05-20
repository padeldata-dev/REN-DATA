"""Regenerate the 8 pexels-hero-*.jpg from high-res originals at 1920px wide.

Maps originals (alphabetical) → pexels-hero-1.jpg ... pexels-hero-8.jpg.
Target: 1920px wide, JPEG quality 90, up to 500 KB.
"""
from pathlib import Path
from PIL import Image, ImageOps

SRC_DIR = Path(r"C:/Users/Usuario/REN-DATA/data/raw/fotos-hero-originales/fotos hero")
DST_DIR = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta/img")
TARGET_WIDTH = 1920
QUALITY = 90
MAX_BYTES = 500 * 1024

originals = sorted(SRC_DIR.glob("*.jpg"))
assert len(originals) == 8, f"Expected 8 originals, got {len(originals)}"

for i, src in enumerate(originals, start=1):
    dst = DST_DIR / f"pexels-hero-{i}.jpg"
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGB")
        w, h = im.size
        new_h = round(h * TARGET_WIDTH / w)
        im = im.resize((TARGET_WIDTH, new_h), Image.LANCZOS)

        q = QUALITY
        while True:
            im.save(dst, "JPEG", quality=q, optimize=True, progressive=True, subsampling=1)
            size = dst.stat().st_size
            if size <= MAX_BYTES or q <= 70:
                break
            q -= 3

    print(f"pexels-hero-{i}.jpg  <- {src.name:50s}  {TARGET_WIDTH}x{new_h}  {size//1024} KB  q={q}")

print("\nDone.")
