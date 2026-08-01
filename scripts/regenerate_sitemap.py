#!/usr/bin/env python3
"""Regenerates rendata_beta/sitemap.xml with all current URLs.

*** OBSOLETO — NO EJECUTAR SIN ARREGLARLO ANTES (comprobado 2026-08-01) ***
Este script se escribio cuando el sitio era plano y solo mira `BETA.glob("*.html")`,
la raiz: se deja fuera las 30 paginas de `academia/` y las 21 de `en/`, que SI estan
en el sitemap actual. Ademas reescribe todos los <lastmod> con la fecha de hoy y
pierde las fechas reales de cada pagina. Ejecutarlo tal cual borra 51 URLs del
sitemap y falsea las 842 restantes.

Mientras no se haga recursivo y conserve los <lastmod> existentes, los cambios
puntuales se hacen a mano sobre sitemap.xml (asi se anadio /prensa el 2026-08-01).
El guardian avisa: qa_check[15] lista las paginas que faltan en el sitemap.

Sources:
- All rentabilidad-*.html
- All ccaa-*.html
- All mercado-inmobiliario-*-2026.html (CCAA analysis articles)
- All other top-level HTML (articles, profile guides, etc.)
"""
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
SITEMAP = BETA / "sitemap.xml"
DOMAIN = "https://rendata.es"

today = datetime.today().strftime("%Y-%m-%d")

# Top-level pages (high priority)
PRIORITY_PAGES = [
    ("/", 1.0, "daily"),
    ("/ranking.html", 0.95, "daily"),
    ("/analisis.html", 0.9, "weekly"),
    ("/actualidad.html", 0.85, "weekly"),
    ("/comparador.html", 0.85, "weekly"),
    ("/informe-rentabilidad-espana-q2-2026.html", 0.9, "monthly"),
    ("/metodologia.html", 0.85, "monthly"),
    ("/widget-demo.html", 0.7, "monthly"),
    ("/guia-inversor.html", 0.8, "monthly"),
    ("/glosario.html", 0.7, "monthly"),
    ("/sobre.html", 0.5, "monthly"),
    ("/contacto.html", 0.6, "monthly"),
    ("/privacidad.html", 0.3, "yearly"),
    ("/aviso-legal.html", 0.3, "yearly"),
]


def clean(loc):
    """Cloudflare Workers Assets sirve URLs limpias (sin .html); el sitemap
    debe apuntar a esa forma canónica, no al fichero real."""
    if loc != "/" and loc.endswith(".html"):
        loc = loc[: -len(".html")]
    return loc


def url_block(loc, lastmod, changefreq, priority):
    return (
        f'  <url>\n'
        f'    <loc>{DOMAIN}{clean(loc)}</loc>\n'
        f'    <lastmod>{lastmod}</lastmod>\n'
        f'    <changefreq>{changefreq}</changefreq>\n'
        f'    <priority>{priority}</priority>\n'
        f'  </url>'
    )


def main():
    # Seguro: mientras el recorrido no sea recursivo, ejecutarlo destruye datos.
    raiz = len([p for p in BETA.glob("*.html") if p.name != "404.html"])
    todas = len([p for p in BETA.glob("**/*.html") if p.name != "404.html"])
    if todas > raiz:
        print(f"ABORTADO: este script solo recorre la raiz ({raiz} paginas) y el sitio "
              f"tiene {todas} (faltan las de academia/ y en/). Generarlo ahora borraria "
              f"{todas - raiz} URLs del sitemap y pisaria los <lastmod> reales. "
              f"Hazlo recursivo y conserva los <lastmod> antes de usarlo.")
        return 1

    blocks = []
    seen = set()

    # 1. Priority top-level
    for loc, prio, freq in PRIORITY_PAGES:
        blocks.append(url_block(loc, today, freq, prio))
        seen.add(loc)

    # 2. CCAA pages
    for p in sorted(BETA.glob("ccaa-*.html")):
        loc = f"/{p.name}"
        blocks.append(url_block(loc, today, "weekly", 0.85))
        seen.add(loc)

    # 3. CCAA analysis articles (mercado-inmobiliario-*)
    for p in sorted(BETA.glob("mercado-inmobiliario-*-2026.html")):
        loc = f"/{p.name}"
        blocks.append(url_block(loc, today, "monthly", 0.8))
        seen.add(loc)

    # 4. Other article pages (top-level *.html not yet seen + not 404)
    excluded = {"404.html"}
    for p in sorted(BETA.glob("*.html")):
        name = p.name
        if name in excluded:
            continue
        loc = f"/{name}"
        if loc in seen:
            continue
        if name.startswith("rentabilidad-") or name.startswith("ccaa-"):
            continue
        # Article page
        blocks.append(url_block(loc, today, "monthly", 0.75))
        seen.add(loc)

    # 5. City pages (rentabilidad-*)
    for p in sorted(BETA.glob("rentabilidad-*.html")):
        loc = f"/{p.name}"
        blocks.append(url_block(loc, today, "weekly", 0.7))
        seen.add(loc)

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(blocks) + "\n"
        '</urlset>\n'
    )
    SITEMAP.write_text(xml, encoding="utf-8")
    print(f"Wrote {len(blocks)} URLs to {SITEMAP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
