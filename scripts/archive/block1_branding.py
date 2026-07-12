"""Block 1: logo + favicon + og:image + cleanup across all HTML pages."""
import re
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")
SRC_LOGO = ROOT / "img" / "logo-rendata-transparente.png"

# --- 1. Generate favicon.ico (multi-size), favicon.svg, apple-touch-icon.png ---
print("[1] Generating favicon assets...")
with Image.open(SRC_LOGO) as im:
    im = im.convert("RGBA")
    # Multi-size ICO
    sizes_ico = [(16,16),(32,32),(48,48),(64,64)]
    icons = [im.resize(s, Image.LANCZOS) for s in sizes_ico]
    icons[0].save(ROOT / "favicon.ico", format="ICO", sizes=sizes_ico, append_images=icons[1:])
    # apple-touch-icon 180×180
    im.resize((180,180), Image.LANCZOS).save(ROOT / "apple-touch-icon.png", "PNG", optimize=True)
    # SVG wrapper that embeds the PNG (most reliable across browsers)
    # Use a small inline PNG for the favicon.svg as well — at 64px
    favicon_svg_png_path = ROOT / "favicon-64.png"
    im.resize((64,64), Image.LANCZOS).save(favicon_svg_png_path, "PNG", optimize=True)

# favicon.svg: simple wrapper that references the PNG isn't ideal — generate a
# proper square SVG with the PNG embedded as base64 so it works standalone.
import base64
with open(favicon_svg_png_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")
favicon_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><image href="data:image/png;base64,{b64}" width="64" height="64"/></svg>'''
(ROOT / "favicon.svg").write_text(favicon_svg, encoding="utf-8")
favicon_svg_png_path.unlink()  # cleanup tmp
print(f"   favicon.ico, favicon.svg, apple-touch-icon.png generated")

# --- 2. Bulk rewrite all HTML files ---
print("[2] Rewriting HTML files...")

NEW_LOGO_TAG = '<img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA">'

# Pattern 1: text logo `<a href="/" class="logo">Ren<span class="ac"> Data</span></a>` (and similar variants)
# Pattern 2: existing img logo `<a href="/" class="logo"><img src="/img/logo-rendata.png" ...></a>`
# Both are inside `<a href="/" class="logo">...</a>` — capture and replace inner contents.
RE_LOGO_A = re.compile(r'(<a href="/" class="logo">)(.*?)(</a>)', re.DOTALL)

# Favicon: ensure both favicon.svg and favicon.ico links exist (some pages still have data: URI inline SVG)
RE_OLD_INLINE_FAV = re.compile(r'<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml,[^"]*"\s*>')
NEW_FAV_BLOCK = '<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="icon" type="image/x-icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'

# og:image: add after og:url if missing
RE_OG_URL = re.compile(r'(<meta property="og:url"[^>]*>)')
OG_IMAGE_TAG = '<meta property="og:image" content="https://rendata.es/img/logo-rendata-transparente.png"><meta property="og:image:width" content="512"><meta property="og:image:height" content="512">'

# Has og:image already?
RE_HAS_OG_IMG = re.compile(r'<meta property="og:image"')

# Has apple-touch?
RE_HAS_APPLE = re.compile(r'rel="apple-touch-icon"')

# Has favicon.svg already?
RE_HAS_FAV_SVG = re.compile(r'rel="icon"[^>]*href="/favicon\.svg"')

changed = 0
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    orig = txt

    # Replace logo
    txt = RE_LOGO_A.sub(lambda m: m.group(1) + NEW_LOGO_TAG + m.group(3), txt)

    # Replace old inline favicon with new block (only on pages that have the inline form)
    if RE_OLD_INLINE_FAV.search(txt):
        txt = RE_OLD_INLINE_FAV.sub(NEW_FAV_BLOCK, txt, count=1)
    else:
        # If already has favicon.svg but no apple-touch, add apple-touch + ensure ico exists
        if RE_HAS_FAV_SVG.search(txt) and not RE_HAS_APPLE.search(txt):
            txt = re.sub(
                r'(<link rel="icon" type="image/x-icon" href="/favicon\.ico"[^>]*>)',
                r'\1<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
                txt,
                count=1,
            )

    # Add og:image if missing and og:url present
    if not RE_HAS_OG_IMG.search(txt) and RE_OG_URL.search(txt):
        txt = RE_OG_URL.sub(lambda m: m.group(1) + OG_IMAGE_TAG, txt, count=1)

    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        changed += 1

print(f"   {changed} HTML files modified")

# --- 3. Delete typo file ---
typo = ROOT / "img" / "logo-rendata..png"
if typo.exists():
    typo.unlink()
    print("[3] Deleted logo-rendata..png (typo)")
else:
    print("[3] Typo file already absent")

print("\nBLOCK 1 done.")
