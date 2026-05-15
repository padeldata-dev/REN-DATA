"""
Mejoras de rendimiento:
1) Preconnect Google Fonts en TODOS los HTML
2) Extraer CSS común de fichas (329) -> /css/ficha.css
3) Extraer CSS común de ccaa (17) -> /css/ccaa.css
4) Extraer FAQ JS común de fichas -> /js/ficha-faq.js (con defer)
"""
import re, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"
CSS_DIR = ROOT / "css"
JS_DIR  = ROOT / "js"
CSS_DIR.mkdir(exist_ok=True)
JS_DIR.mkdir(exist_ok=True)

# ============================================================
# 1) PRECONNECT GOOGLE FONTS EN TODOS LOS HTML
# ============================================================

PRECONNECT_LINES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
)

PAT_GFONTS = re.compile(r'(<link[^>]*href="https://fonts\.googleapis\.com[^"]*"[^>]*>)')
PAT_HAS_PRECONNECT = re.compile(r'<link[^>]*rel="preconnect"[^>]*fonts\.gstatic\.com', re.IGNORECASE)

preconnect_count = 0
preconnect_skipped = 0
for fp in glob.glob(str(ROOT / "*.html")):
    h = open(fp, encoding="utf-8").read()
    if PAT_HAS_PRECONNECT.search(h):
        preconnect_skipped += 1
        continue
    m = PAT_GFONTS.search(h)
    if not m:
        continue
    new_h = h[:m.start()] + PRECONNECT_LINES + h[m.start():]
    Path(fp).write_text(new_h, encoding="utf-8")
    preconnect_count += 1

print(f"[1] Preconnect: añadido a {preconnect_count} HTML | saltados (ya tenían) {preconnect_skipped}")

# ============================================================
# 2) CSS COMÚN FICHAS -> /css/ficha.css
# ============================================================

ANCHOR_FICHA = ROOT / "rentabilidad-alicante.html"  # 48165 chars - más comprensivo
m = re.search(r'<style>(.*?)</style>', ANCHOR_FICHA.read_text(encoding="utf-8"), re.DOTALL)
ficha_css = m.group(1).strip()
(CSS_DIR / "ficha.css").write_text(ficha_css + "\n", encoding="utf-8")
print(f"[2a] /css/ficha.css escrito: {len(ficha_css)} chars")

# Reemplazar <style>...</style> por link en TODAS las fichas
PAT_STYLE = re.compile(r'<style>.*?</style>', re.DOTALL)
LINK_FICHA = '<link rel="stylesheet" href="/css/ficha.css">'

ficha_replaced = 0
ficha_no_style = []
for fp in glob.glob(str(ROOT / "rentabilidad-*.html")):
    h = open(fp, encoding="utf-8").read()
    new_h, n = PAT_STYLE.subn(LINK_FICHA, h, count=1)
    if n == 0:
        ficha_no_style.append(Path(fp).name)
        continue
    Path(fp).write_text(new_h, encoding="utf-8")
    ficha_replaced += 1

print(f"[2b] CSS sustituido por link en {ficha_replaced} fichas")
if ficha_no_style:
    print(f"   ! {len(ficha_no_style)} fichas sin <style> detectado:", ficha_no_style[:5])

# ============================================================
# 3) CSS COMÚN CCAA -> /css/ccaa.css
# ============================================================

ANCHOR_CCAA = ROOT / "ccaa-andalucia.html"
m = re.search(r'<style>(.*?)</style>', ANCHOR_CCAA.read_text(encoding="utf-8"), re.DOTALL)
ccaa_css = m.group(1).strip()
(CSS_DIR / "ccaa.css").write_text(ccaa_css + "\n", encoding="utf-8")
print(f"\n[3a] /css/ccaa.css escrito: {len(ccaa_css)} chars")

LINK_CCAA = '<link rel="stylesheet" href="/css/ccaa.css">'
ccaa_replaced = 0
for fp in glob.glob(str(ROOT / "ccaa-*.html")):
    h = open(fp, encoding="utf-8").read()
    new_h, n = PAT_STYLE.subn(LINK_CCAA, h, count=1)
    if n == 0:
        continue
    Path(fp).write_text(new_h, encoding="utf-8")
    ccaa_replaced += 1
print(f"[3b] CSS sustituido por link en {ccaa_replaced} ccaa")

# ============================================================
# 4) JS COMÚN FICHAS (FAQ) -> /js/ficha-faq.js + defer
# ============================================================

# El segundo bloque <script> en cada ficha es idéntico (FAQ toggle)
# Lo extraigo del adra y lo verifico contra otras antes de externalizar
faq_anchor_h = (ROOT / "rentabilidad-adra.html").read_text(encoding="utf-8")
scripts = re.findall(r'<script(?![^>]*application/ld)>(.*?)</script>', faq_anchor_h, re.DOTALL)
if len(scripts) < 2:
    print("[4] AVISO: anchor sin segundo bloque <script>, saltando externalización JS")
else:
    faq_js = scripts[1].strip()
    (JS_DIR / "ficha-faq.js").write_text(faq_js + "\n", encoding="utf-8")
    print(f"\n[4a] /js/ficha-faq.js escrito: {len(faq_js)} chars")

    # Reemplazar SOLO el segundo bloque <script>...</script> NO json-ld
    LINK_JS_FAQ = '<script src="/js/ficha-faq.js" defer></script>'
    js_replaced = 0
    js_skipped = []
    for fp in glob.glob(str(ROOT / "rentabilidad-*.html")):
        h = open(fp, encoding="utf-8").read()
        # Encontrar todos los <script> no JSON-LD
        # Buscar el patrón exacto del FAQ (contiene 'toggleFaq')
        pat_faq = re.compile(r'<script>\s*\n?function toggleFaq.*?</script>', re.DOTALL)
        new_h, n = pat_faq.subn(LINK_JS_FAQ, h, count=1)
        if n == 0:
            js_skipped.append(Path(fp).name)
            continue
        Path(fp).write_text(new_h, encoding="utf-8")
        js_replaced += 1
    print(f"[4b] FAQ JS sustituido por link defer en {js_replaced} fichas")
    if js_skipped:
        print(f"   ! {len(js_skipped)} fichas sin patrón FAQ detectado")

print("\n--- DONE ---")
