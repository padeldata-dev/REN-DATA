"""Añade link a top10-ciudades-rentables-2026.html en nav y footer de los HTML."""
import re, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"
TOP10 = "top10-ciudades-rentables-2026.html"

# Patrones para añadir link de Top 10 en distintos contextos
NAV_PATTERNS = [
    # 1. Nav <a href="ranking.html">Ranking</a> simple
    (re.compile(r'(<a href="ranking\.html">Ranking</a>)'),
     r'\1<a href="' + TOP10 + r'">Top 10</a>'),
    # 2. Nav con estilo activo (e.g. en ranking.html)
    (re.compile(r'(<a href="ranking\.html"[^>]*style="[^"]*color:var\(--blue\)[^"]*"[^>]*>Ranking</a>)'),
     r'\1<a href="' + TOP10 + r'">Top 10</a>'),
    # 3. Nav móvil con emoji
    (re.compile(r'(<a href="ranking\.html">📊 Ranking</a>)'),
     r'\1<a href="' + TOP10 + r'">🏆 Top 10</a>'),
]

# Footer: añadir link en columna "Herramientas" tras "Ranking de rentabilidad"
FOOTER_PATTERN = (
    re.compile(r'(<a href="ranking\.html">Ranking de rentabilidad</a>)'),
    r'\1\n      <a href="' + TOP10 + r'">Top 10 más rentables</a>'
)

stats = {"nav_added": 0, "nav_skipped": 0, "footer_added": 0}

for fp in glob.glob(str(ROOT / "*.html")):
    name = Path(fp).name
    if name == TOP10:  # No tocar el propio artículo
        continue
    h = open(fp, encoding="utf-8").read()
    h_orig = h
    # Saltar si ya tiene el link
    if TOP10 in h:
        stats["nav_skipped"] += 1
        continue
    # Aplicar patrones de nav (uno solo)
    for pat, repl in NAV_PATTERNS:
        new_h, n = pat.subn(repl, h, count=1)
        if n:
            h = new_h
            stats["nav_added"] += 1
            break
    # Footer
    new_h, n = FOOTER_PATTERN[0].subn(FOOTER_PATTERN[1], h, count=1)
    if n:
        h = new_h
        stats["footer_added"] += 1
    if h != h_orig:
        Path(fp).write_text(h, encoding="utf-8")

print(f"Nav añadido:    {stats['nav_added']}")
print(f"Nav saltados:   {stats['nav_skipped']} (ya tenían link)")
print(f"Footer añadido: {stats['footer_added']}")
