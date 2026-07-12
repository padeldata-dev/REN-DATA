"""
Unifica todas las citas de fuentes en el sitio:
- Reemplaza Idealista/Fotocasa por Ministerio de Vivienda / fuentes oficiales
- Unifica el footer (180 corto + 149 largo) con cita coherente
- Actualiza trust-bar de index.html
"""
import re, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

# Cita oficial unificada
CITA = "INE · Ministerio de Vivienda · Ministerio de Hacienda · Actualizado trimestralmente"

# ============ 1. REEMPLAZOS EN FICHAS ============

# (regex_pattern, replacement)
REPLACEMENTS = [
    # JSON-LD FAQ + meta description: "según datos de Idealista Q1 2026"
    (re.compile(r'seg[uú]n datos de Idealista Q1 2026', re.IGNORECASE),
     'según datos del Ministerio de Vivienda Q1 2026'),
    # "Fuente: Ministerio de Vivienda / Idealista" → "Fuente: Ministerio de Vivienda"
    (re.compile(r'Fuente:\s*Ministerio de Vivienda\s*/\s*Idealista'),
     'Fuente: Ministerio de Vivienda'),
    # "(Ministerio de Vivienda, Idealista, Fotocasa)" → "(INE, Ministerio de Vivienda, Ministerio de Hacienda)"
    (re.compile(r'\(Ministerio de Vivienda,\s*Idealista,\s*Fotocasa\)'),
     '(INE, Ministerio de Vivienda, Ministerio de Hacienda)'),
    # Body text "portales (Idealista, Fotocasa)" → "portales inmobiliarios"
    (re.compile(r'portales\s*\(Idealista,\s*Fotocasa\)', re.IGNORECASE),
     'portales inmobiliarios'),
    # "según Idealista." (final de frase) → "según fuentes oficiales."
    (re.compile(r'seg[uú]n Idealista([\.\,])', re.IGNORECASE),
     r'según fuentes oficiales\1'),
    # "según Idealista" suelto al final de ítem
    (re.compile(r'seg[uú]n Idealista(?=\s*<)', re.IGNORECASE),
     'según fuentes oficiales'),
    # Cualquier "Idealista" residual en meta description tipo "según Idealista Q1"
    (re.compile(r'seg[uú]n Idealista Q1 2026'),
     'según el Ministerio de Vivienda Q1 2026'),
    # Catch-all: "Idealista Q1 2026" → "Ministerio de Vivienda Q1 2026"
    (re.compile(r'\bIdealista Q1 2026\b'),
     'Ministerio de Vivienda Q1 2026'),
]

# ============ 2. FOOTER UNIFICADO ============

# Footer CORTO: "© 2026 rendata.es · Datos actualizados trimestralmente" → con cita completa
FOOTER_CORTO = (
    re.compile(r'(<p>©\s*2026\s*rendata\.es)\s*·\s*Datos actualizados trimestralmente(\s*</p>)'),
    r'\1 · Datos: ' + CITA + r'\2'
)

# Footer LARGO: cambiar "(INE, Ministerio de Vivienda, Ministerio de Hacienda) ·" por formato bullet
FOOTER_LARGO_DESC = (
    re.compile(r'fuentes p[uú]blicas\s*\(INE,\s*Ministerio de Vivienda,\s*Ministerio de Hacienda\)'),
    'fuentes oficiales (' + CITA + ')'
)

# El bottom de footer LARGO: "© 2026 Ren Data · rendata.es · Datos: INE, Ministerio..."
FOOTER_LARGO_BOTTOM = (
    re.compile(r'(©\s*2026\s+Ren\s+Data\s*·\s*rendata\.es\s*·\s*)Datos:\s*INE,\s*Ministerio de Vivienda,\s*Ministerio de Hacienda'),
    r'\1Datos: ' + CITA.replace(' · Actualizado trimestralmente', '')
)

# ============ EJECUCIÓN EN FICHAS ============

n_changed = 0
for fp in sorted(glob.glob(str(ROOT / "rentabilidad-*.html"))):
    h = open(fp, encoding="utf-8").read()
    h0 = h
    for pat, rep in REPLACEMENTS:
        h = pat.sub(rep, h)
    h = FOOTER_CORTO[0].sub(FOOTER_CORTO[1], h)
    h = FOOTER_LARGO_DESC[0].sub(FOOTER_LARGO_DESC[1], h)
    h = FOOTER_LARGO_BOTTOM[0].sub(FOOTER_LARGO_BOTTOM[1], h)
    if h != h0:
        Path(fp).write_text(h, encoding="utf-8")
        n_changed += 1
print(f"[FICHAS] modificadas: {n_changed}/329")

# ============ 3. TRUST-BAR DE index.html ============

INDEX = ROOT / "index.html"
h = INDEX.read_text(encoding="utf-8")
h0 = h

# Trust bar: 3 items, los 2 primeros mencionan Idealista/Fotocasa
TRUST_OLD = re.compile(
    r'(<div class="trust-item">[^<]*<svg[^>]*>.*?</svg>)Fuente: Idealista Q1 2026(</div>\s*'
    r'<div class="trust-item">[^<]*<svg[^>]*>.*?</svg>)Fotocasa\s*·\s*Ministerio de Vivienda(</div>)',
    re.DOTALL
)
TRUST_NEW = (
    r'\1Fuente: INE · Ministerio de Vivienda\2Ministerio de Hacienda · Datos oficiales\3'
)

new_h, n = TRUST_OLD.subn(TRUST_NEW, h, count=1)
if n:
    h = new_h
    print(f"[INDEX] trust-bar actualizada")
else:
    print(f"[INDEX] AVISO: no encontré el patrón de trust-bar; revisar manualmente")

# Footer de index.html (línea 349): "Datos: INE, Ministerio de Vivienda, Ministerio de Hacienda"
INDEX_FOOTER = re.compile(
    r'(©\s*2026\s+Ren\s+Data\s*·\s*rendata\.es\s*·\s*)Datos:\s*INE,\s*Ministerio de Vivienda,\s*Ministerio de Hacienda'
)
new_h, n2 = INDEX_FOOTER.subn(
    r'\1Datos: INE · Ministerio de Vivienda · Ministerio de Hacienda', h, count=1
)
if n2:
    h = new_h
    print(f"[INDEX] footer actualizado")

if h != h0:
    INDEX.write_text(h, encoding="utf-8")

# ============ 4. AUDITORÍA POST ============

residual = 0
for fp in glob.glob(str(ROOT / "rentabilidad-*.html")):
    h = open(fp, encoding="utf-8").read()
    if re.search(r'\bIdealista\b', h) or re.search(r'\bFotocasa\b', h):
        residual += 1
print(f"\n[AUDITORÍA] fichas con 'Idealista' o 'Fotocasa' residual: {residual}")

# index.html
h = INDEX.read_text(encoding="utf-8")
matches = re.findall(r'(?:Idealista|Fotocasa)', h)
print(f"[AUDITORÍA] index.html: {len(matches)} menciones residuales de Idealista/Fotocasa")
