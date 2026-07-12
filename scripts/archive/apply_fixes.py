"""
FIX 1 — Dropdown click toggle (CSS + script en HTML)
FIX 2 — Favicon links en todos los HTML
FIX 3 — Eliminar CSS muerto .ccaa-analysis
"""
import re, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

# ============================================================
# FIX 1.a — Añadir regla CSS .nav-dropdown.open al final de ficha.css y ccaa.css
# ============================================================
DROPDOWN_CSS = "\n.nav-dropdown.open .nav-drop-menu{display:grid;grid-template-columns:1fr 1fr;gap:2px}\n"

for css_path in [ROOT/"css"/"ficha.css", ROOT/"css"/"ccaa.css"]:
    txt = css_path.read_text(encoding="utf-8")
    if ".nav-dropdown.open" not in txt:
        css_path.write_text(txt.rstrip() + DROPDOWN_CSS, encoding="utf-8")
        print(f"[1a] Regla añadida a {css_path.name}")
    else:
        print(f"[1a] {css_path.name} ya contiene la regla")

# ============================================================
# FIX 3 — Eliminar bloque .ccaa-analysis de ccaa.css (dead CSS)
# ============================================================
ccaa_css = ROOT/"css"/"ccaa.css"
txt = ccaa_css.read_text(encoding="utf-8")
# Eliminar todas las reglas que empiezan por .ccaa-analysis
new_txt = re.sub(r'^\.ccaa-analysis[^\n]*\n', '', txt, flags=re.MULTILINE)
removed = txt.count("ccaa-analysis") - new_txt.count("ccaa-analysis")
ccaa_css.write_text(new_txt, encoding="utf-8")
print(f"[3] Reglas .ccaa-analysis eliminadas de ccaa.css (líneas borradas: {removed})")

# ============================================================
# FIX 1.b — Inyectar regla CSS también en los <style> inline (index, sobre, glosario, 404)
# ============================================================
INLINE_RULE = ".nav-dropdown.open .nav-drop-menu{display:grid;grid-template-columns:1fr 1fr;gap:2px}"
for fname in ["index.html", "sobre.html", "glosario.html", "404.html"]:
    fp = ROOT/fname
    if not fp.exists(): continue
    h = fp.read_text(encoding="utf-8")
    if ".nav-dropdown.open" in h:
        continue
    # Buscar el bloque <style> con .nav-drop y añadir antes de </style>
    m = re.search(r'(\.nav-drop-menu\{[^}]*\})', h)
    if m:
        # Añadir la nueva regla justo después de la regla .nav-drop-menu existente
        new_h = h[:m.end()] + INLINE_RULE + h[m.end():]
        fp.write_text(new_h, encoding="utf-8")
        print(f"[1b] Regla añadida inline a {fname}")
    else:
        print(f"[1b] {fname}: no encontré .nav-drop-menu inline")

# ============================================================
# FIX 1.c — Inyectar <script src="/js/nav-dropdown.js" defer> en todos los HTML con .nav-dropdown
# ============================================================
SCRIPT_TAG = '<script src="/js/nav-dropdown.js" defer></script>\n'
n_added_js = 0
for fp in glob.glob(str(ROOT/"*.html")):
    h = open(fp, encoding="utf-8").read()
    if 'class="nav-dropdown"' not in h:
        continue
    if 'js/nav-dropdown.js' in h:
        continue
    # Insertar antes de </head>
    new_h, n = re.subn(r'</head>', SCRIPT_TAG + '</head>', h, count=1)
    if n:
        Path(fp).write_text(new_h, encoding="utf-8")
        n_added_js += 1
print(f"[1c] script nav-dropdown.js añadido a {n_added_js} HTML")

# ============================================================
# FIX 2 — Favicon links en TODOS los HTML
# ============================================================
FAV_TAGS = (
    '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n'
    '<link rel="icon" type="image/x-icon" href="/favicon.ico">\n'
)
n_fav = 0
n_fav_skipped = 0
for fp in glob.glob(str(ROOT/"*.html")):
    h = open(fp, encoding="utf-8").read()
    # Saltar si ya hay <link rel="icon">
    if re.search(r'<link[^>]*rel="(?:icon|shortcut icon)"', h):
        n_fav_skipped += 1
        continue
    # Insertar tras <title>...</title> si existe; si no, tras <meta charset>
    m = re.search(r'(</title>)', h)
    if m:
        new_h = h[:m.end()] + "\n" + FAV_TAGS.rstrip() + h[m.end():]
    else:
        m = re.search(r'(<meta charset[^>]*>)', h)
        if not m:
            continue
        new_h = h[:m.end()] + "\n" + FAV_TAGS.rstrip() + h[m.end():]
    Path(fp).write_text(new_h, encoding="utf-8")
    n_fav += 1
print(f"[2] favicon links añadidos a {n_fav} HTML | saltados {n_fav_skipped} (ya tenían)")

print("\n--- DONE ---")
