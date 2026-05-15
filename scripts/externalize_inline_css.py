"""
Externaliza el CSS inline de las páginas principales.
- index.html → /css/index.css
- sobre.html → /css/general.css
- privacidad.html y aviso-legal.html → /css/legal.css (son idénticos)
- contacto.html → /css/contacto.css (combina los 2 bloques style)
- glosario.html → /css/glosario.css
- comparador.html → /css/comparador.css
- ranking.html → /css/ranking.css
- top10-ciudades-rentables-2026.html → /css/top10.css
"""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"
CSS_DIR = ROOT / "css"
CSS_DIR.mkdir(exist_ok=True)

# (page, css_filename) — pages se procesan en este orden
MAPPING = [
    ("index.html",                          "index.css"),
    ("sobre.html",                          "general.css"),
    ("privacidad.html",                     "legal.css"),
    ("aviso-legal.html",                    "legal.css"),
    ("contacto.html",                       "contacto.css"),
    ("glosario.html",                       "glosario.css"),
    ("comparador.html",                     "comparador.css"),
    ("ranking.html",                        "ranking.css"),
    ("top10-ciudades-rentables-2026.html",  "top10.css"),
]

PAT_STYLE = re.compile(r'<style>(.*?)</style>', re.DOTALL)

# Para evitar duplicar el archivo legal.css, recordamos cuáles ya hemos escrito
written = set()

for page, css_name in MAPPING:
    fp = ROOT / page
    if not fp.exists():
        print(f"!! {page} no existe"); continue
    h = fp.read_text(encoding="utf-8")
    blocks = PAT_STYLE.findall(h)
    if not blocks:
        print(f"!! {page} sin <style>"); continue

    # Combinar todos los bloques de la página
    combined = "\n\n".join(b.strip() for b in blocks)
    css_path = CSS_DIR / css_name

    if css_name not in written:
        css_path.write_text(combined + "\n", encoding="utf-8")
        written.add(css_name)
        print(f"[+] {css_name} ({len(combined)} chars) ← {page}")
    else:
        # Para legal.css: el primer write ya cubre privacidad. aviso-legal salta y solo hace el reemplazo en HTML
        print(f"[=] {css_name} ya escrito, reutilizando para {page}")

    # Reemplazar TODOS los bloques <style>...</style> por nada
    new_h = PAT_STYLE.sub("", h)
    # Eliminar líneas vacías excesivas que quedan tras la eliminación
    new_h = re.sub(r'\n{3,}', '\n\n', new_h)
    # Insertar el link justo antes de </head>
    link_tag = f'<link rel="stylesheet" href="/css/{css_name}">\n'
    if f'href="/css/{css_name}"' not in new_h:
        new_h = re.sub(r'</head>', link_tag + '</head>', new_h, count=1)
    fp.write_text(new_h, encoding="utf-8")

print(f"\n{len(MAPPING)} páginas procesadas, {len(written)} archivos CSS creados.")
