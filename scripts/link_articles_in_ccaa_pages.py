#!/usr/bin/env python3
"""Add a banner linking to mercado-inmobiliario-{ccaa}-2026.html at the top of each ccaa-*.html."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"

CCAA = [
    ("Andalucía", "andalucia"), ("Cataluña", "cataluna"),
    ("C. Valenciana", "comunitat-valenciana"), ("Madrid", "madrid"),
    ("Galicia", "galicia"), ("Castilla y León", "castilla-y-leon"),
    ("Castilla-La Mancha", "castilla-la-mancha"), ("Canarias", "canarias"),
    ("Islas Baleares", "baleares"), ("Aragón", "aragon"),
    ("Región de Murcia", "murcia"), ("Asturias", "asturias"),
    ("Cantabria", "cantabria"), ("Navarra", "navarra"),
    ("Extremadura", "extremadura"), ("La Rioja", "la-rioja"),
    ("País Vasco", "pais-vasco"),
]


def main():
    fixed = 0
    for name, slug in CCAA:
        p = BETA / f"ccaa-{slug}.html"
        if not p.is_file():
            print(f"  [skip] no file: ccaa-{slug}.html")
            continue
        html = p.read_text(encoding="utf-8")
        article_href = f"mercado-inmobiliario-{slug}-2026.html"
        if article_href in html:
            continue

        banner = (
            f'\n<div style="max-width:1080px;margin:1.5rem auto;padding:1rem 2rem;background:#eff6ff;'
            f'border:1px solid #bfdbfe;border-radius:10px;font-size:.92rem;display:flex;'
            f'align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap">\n'
            f'  <div>📈 <strong>Análisis completo de {name} 2026</strong>: ranking, fiscalidad, '
            f'regulación y perfil del inversor con datos reales.</div>\n'
            f'  <a href="{article_href}" style="background:#1a56db;color:white;padding:.45rem 1rem;'
            f'border-radius:6px;text-decoration:none;font-weight:700;font-size:.85rem;'
            f'white-space:nowrap">Leer análisis →</a>\n'
            f'</div>\n'
        )
        # Insert right after <main> or after first <h1>
        new_html, n = re.subn(
            r'(<main[^>]*>)',
            rf'\g<1>{banner}',
            html, count=1,
        )
        if n == 0:
            new_html, n = re.subn(
                r'(</header>)',
                rf'\g<1>{banner}',
                html, count=1,
            )
        if n > 0:
            p.write_text(new_html, encoding="utf-8")
            print(f"  [ok] linked from ccaa-{slug}.html")
            fixed += 1
        else:
            print(f"  [ERR] could not find insertion point in ccaa-{slug}.html")

    print(f"\nLinked: {fixed} / {len(CCAA)} CCAA pages")


if __name__ == "__main__":
    main()
