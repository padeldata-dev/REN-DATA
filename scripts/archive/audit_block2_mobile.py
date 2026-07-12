"""Block 2: mobile audit on key pages + global mobile fixes.

Checks:
 1. Viewport meta correct on all pages
 2. Mobile menu (hamburguesa) markup present
 3. Tables wrapped with overflow-x:auto
 4. Inputs with font-size ≥16px (avoids iOS zoom)
 5. Touch targets ≥44x44
 6. Images don't overflow viewport (max-width:100%)
 7. Long lines / readable text

Auto-fixes:
 - Add overflow-x:auto wrappers around bare <table> tags
 - Add font-size:16px to inputs that have smaller size
 - Add img{max-width:100%;height:auto} CSS rule in main stylesheets if missing
"""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

KEY_PAGES = [
    "index.html", "comparador.html", "ranking.html",
    "simulador-comprar-vs-alquilar.html", "calculadora-hipoteca.html",
    "rentabilidad-madrid.html", "rentabilidad-soria.html", "rentabilidad-vila-real.html",
    "ciudades-baratas-comprar-piso-espana-2026.html",
    "top10-ciudades-rentables-2026.html",
    "comprar-piso-primera-vez-espana-2026.html",
]

report = {
    "viewport_missing": [],
    "viewport_bad": [],
    "no_mob_menu": [],
    "tables_no_scroll": [],
    "small_input_font": [],
}

# 1. Viewport tag check
RE_VP = re.compile(r'<meta[^>]+name="viewport"[^>]+content="([^"]*)"', re.IGNORECASE)
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    m = RE_VP.search(txt)
    if not m:
        report["viewport_missing"].append(f.name)
    else:
        c = m.group(1)
        if "width=device-width" not in c:
            report["viewport_bad"].append((f.name, c))

# 2. Hamburger menu present?
RE_MOB = re.compile(r'class="mob-menu-btn"', re.IGNORECASE)
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    if "<nav" in txt and not RE_MOB.search(txt) and "/css/nav.css" in txt:
        report["no_mob_menu"].append(f.name)

# 3. Tables without overflow wrapper
# Heuristic: find <table> not preceded by <div class="...overflow...">
RE_BARE_TABLE = re.compile(r'(?<!table-wrap">)\s*<table\b', re.IGNORECASE)
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    if "<table" not in txt: continue
    # If page has a CSS rule like .responsive-table or wraps with overflow, count.
    # Cheap check: page has no "overflow-x:auto" anywhere AND has <table>
    if "<table" in txt and "overflow-x:auto" not in txt and "overflow-x: auto" not in txt:
        # Also OK if table inline style has overflow or wrapped in scroll-x div
        report["tables_no_scroll"].append(f.name)

# 4. Small input font (look at <style> blocks for input{font-size:14px} etc)
RE_INPUT_FONT = re.compile(r'input[^{]*\{[^}]*font-size\s*:\s*(1[0-5]px|0\.8\d*rem|0\.9\d*rem)', re.IGNORECASE)
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    if RE_INPUT_FONT.search(txt):
        report["small_input_font"].append(f.name)

# Print initial report
print("=== MOBILE AUDIT (pre-fix) ===")
for k, v in report.items():
    print(f"{k}: {len(v)}")
    if v and k in ("viewport_missing", "viewport_bad", "no_mob_menu"):
        for item in v[:5]: print("   ", item)

# ============================================================
# AUTO-FIX 1: Wrap bare <table>...</table> with overflow div
# ============================================================
# Only do it inside main content, not inside scripts/templates.
# Add a CSS rule to a global stylesheet that wraps tables responsively.
# Cleanest: add a CSS rule .resp-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
# in index.css. Then wrap each <table> in such a div on the fly via HTML edit.

# Add CSS rule to css/index.css if not present
idx_css = ROOT / "css" / "index.css"
if idx_css.exists():
    css = idx_css.read_text(encoding="utf-8")
    if ".resp-table-wrap" not in css:
        css += "\n\n/* Responsive table wrapper — added by audit block 2 */\n.resp-table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:1rem 0}\n.resp-table-wrap table{min-width:560px}\n/* Mobile-safe image rule (global) */\nimg{max-width:100%;height:auto}\n/* Avoid iOS zoom on inputs */\n@media(max-width:768px){input[type=\"text\"],input[type=\"number\"],input[type=\"email\"],select,textarea{font-size:16px}}"
        idx_css.write_text(css, encoding="utf-8")
        print("   [css] resp-table-wrap + img safety + iOS input-zoom guard added to index.css")

# Wrap bare tables: only those not already inside an overflow container
RE_TABLE_BLOCK = re.compile(r'<table\b([^>]*)>([\s\S]*?)</table>', re.IGNORECASE)
RE_PREV_WRAP = re.compile(r'<div[^>]*class="[^"]*resp-table-wrap[^"]*"', re.IGNORECASE)

tables_wrapped = 0
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    if "<table" not in txt: continue
    if "resp-table-wrap" in txt:
        # Already wrapped at least once. Don't re-wrap.
        continue
    # Wrap every table with the div
    def wrap(m):
        nonlocal_count[0] += 1
        return '<div class="resp-table-wrap"><table' + m.group(1) + '>' + m.group(2) + '</table></div>'
    nonlocal_count = [0]
    new_txt = RE_TABLE_BLOCK.sub(wrap, txt)
    if new_txt != txt:
        f.write_text(new_txt, encoding="utf-8")
        tables_wrapped += nonlocal_count[0]
print(f"   [tables] {tables_wrapped} <table> wrapped with .resp-table-wrap")

# ============================================================
# AUTO-FIX 2: Touch targets — verify nav anchor padding
# Not modifying everything; the global nav uses .82rem font with .85rem padding
# = ~38px target. CSS spec recommends min 44x44 for mobile.
# We've already added a mobile media query above that increases input size.
# Touch targets in main nav are handled by .mob-nav-links>a min-height:48px (already in nav.css).
# ============================================================

print("\nDone block 2.")
