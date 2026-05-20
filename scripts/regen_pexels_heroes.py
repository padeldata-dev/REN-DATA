"""Regenerate the 8 pexels-hero-*.jpg from high-res originals at 1920px wide.

Maps originals (alphabetical) → pexels-hero-1.jpg ... pexels-hero-8.jpg.
Target: 1920px wide, JPEG quality 85, progressive, subsampling 4:2:0.
No size cap — hero LCP can spend bytes on quality.
"""
from pathlib import Path
from PIL import Image, ImageOps

SRC_DIR = Path(r"C:/Users/Usuario/REN-DATA/data/raw/fotos-hero-originales/fotos hero")
DST_DIR = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta/img")
TARGET_WIDTH = 1920
QUALITY = 85

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
        im.save(dst, "JPEG", quality=QUALITY, optimize=True, progressive=True, subsampling=2)

    size = dst.stat().st_size
    print(f"pexels-hero-{i}.jpg  <- {src.name:50s}  {TARGET_WIDTH}x{new_h}  {size//1024} KB")

print("\nDone.")
