# -*- coding: utf-8 -*-
"""Integra las páginas de barrios en el resto del sitio:
 - CTA "Ver barrios" en rentabilidad-{slug}.html y vivir-en-{slug}.html
 - Enlace "Barrios" en el footer (dos variantes de footer)
 - 51 URLs nuevas en sitemap.xml
Idempotente: se puede ejecutar varias veces sin duplicar.
"""
import os, re, glob
from barrios_data import CITIES

OUT = os.path.join(os.path.dirname(__file__), "..", "rendata_beta")
NAMES = {s: c["name"] for s, c in CITIES.items()}


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def patch_vivir(slug):
    p = os.path.join(OUT, f"vivir-en-{slug}.html")
    if not os.path.exists(p):
        return False
    h = read(p)
    if "barrios-%s.html" % slug in h:
        return False
    city = NAMES[slug]
    n = len(CITIES[slug]["barrios"])
    cta = (
        f'  <a href="barrios-{slug}.html" class="cta-ficha" style="background:linear-gradient(135deg,#7c2d92 0%,#9333ea 100%)">\n'
        f'    <div>\n'
        f'      <div class="cta-ficha-t">🗺️ Explora los {n} barrios de {city} uno a uno</div>\n'
        f'      <div class="cta-ficha-s">Precio €/m² por zona, perfil, transporte y dónde comprar según tu perfil</div>\n'
        f'    </div>\n'
        f'    <span class="cta-ficha-b">Ver barrios →</span>\n'
        f'  </a>\n\n'
    )
    anchor = '  <h2 id="transporte">'
    if anchor not in h:
        return False
    h = h.replace(anchor, cta + anchor, 1)
    write(p, h)
    return True


def patch_rentabilidad(slug):
    p = os.path.join(OUT, f"rentabilidad-{slug}.html")
    if not os.path.exists(p):
        return False
    h = read(p)
    if "barrios-cta-card" in h:
        return False
    city = NAMES[slug]
    aside = (
        f'\n<aside class="barrios-cta-card" style="max-width:1200px;margin:.6rem auto 0;padding:0 1.5rem">\n'
        f'  <a href="barrios-{slug}.html" style="display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#7c2d92 0%,#9333ea 100%);color:#fff;padding:1.1rem 1.35rem;border-radius:12px;text-decoration:none;gap:1rem;flex-wrap:wrap;box-shadow:0 4px 16px rgba(124,45,146,.15)">\n'
        f'    <div>\n'
        f'      <div style="font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#e9d5ff;margin-bottom:.25rem">Mapa de barrios</div>\n'
        f'      <div style="font-size:1.02rem;font-weight:700;letter-spacing:-.02em">🗺️ ¿Dónde comprar en {city}? Mira los barrios</div>\n'
        f'      <div style="font-size:.83rem;color:rgba(255,255,255,.82);margin-top:.25rem">Precio €/m² por zona, perfil, transporte y recomendaciones por perfil</div>\n'
        f'    </div>\n'
        f'    <div style="background:rgba(255,255,255,.18);padding:.55rem 1.05rem;border-radius:8px;font-size:.85rem;font-weight:700;white-space:nowrap">Ver barrios →</div>\n'
        f'  </a>\n'
        f'</aside>\n'
    )
    m = re.search(r'<aside class="vivir-cta-card".*?</aside>\n', h, re.S)
    if not m:
        return False
    h = h[:m.end()] + aside + h[m.end():]
    write(p, h)
    return True


def patch_footer(p):
    """Añade 'Barrios' al footer en sus dos variantes. Idempotente."""
    h = read(p)
    changed = False
    # Variante simple (páginas de artículo): columna Análisis
    simple = '<a href="vivir-en-espana.html">Vivir en…</a>'
    if simple in h and '<a href="barrios.html">Barrios</a>' not in h:
        h = h.replace(simple, simple + '\n      <a href="barrios.html">Barrios</a>', 1)
        changed = True
    # Variante rica (home / rentabilidad): columna Herramientas
    rich = '<a href="comparador.html">Comparador de ciudades</a>'
    if rich in h and 'barrios.html">Barrios de España</a>' not in h:
        h = h.replace(rich, rich + '\n      <a href="barrios.html">Barrios de España</a>', 1)
        changed = True
    if changed:
        write(p, h)
    return changed


def patch_sitemap():
    p = os.path.join(OUT, "sitemap.xml")
    h = read(p)
    if "barrios-madrid.html" in h:
        return 0
    blocks = []
    blocks.append(
        "  <url>\n    <loc>https://rendata.es/barrios.html</loc>\n"
        "    <lastmod>2026-05-29</lastmod>\n    <changefreq>monthly</changefreq>\n"
        "    <priority>0.8</priority>\n  </url>\n")
    for slug in CITIES:
        blocks.append(
            f"  <url>\n    <loc>https://rendata.es/barrios-{slug}.html</loc>\n"
            f"    <lastmod>2026-05-29</lastmod>\n    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.7</priority>\n  </url>\n")
    h = h.replace("</urlset>", "".join(blocks) + "</urlset>")
    write(p, h)
    return len(blocks)


def main():
    v = sum(patch_vivir(s) for s in CITIES)
    r = sum(patch_rentabilidad(s) for s in CITIES)
    fc = sum(patch_footer(p) for p in glob.glob(os.path.join(OUT, "*.html")))
    sm = patch_sitemap()
    print(f"vivir CTA insertados: {v}")
    print(f"rentabilidad CTA insertados: {r}")
    print(f"footers con enlace Barrios añadido: {fc}")
    print(f"URLs añadidas al sitemap: {sm}")


if __name__ == "__main__":
    main()
