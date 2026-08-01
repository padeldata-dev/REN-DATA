#!/usr/bin/env python3
"""
Regenera rendata_beta/sitemap.xml a partir del árbol de ficheros.

Historia: la versión anterior se escribió cuando el sitio era plano y solo
recorría `BETA.glob("*.html")`, la raíz. Con `academia/` y `en/` en juego se
dejaba fuera 51 páginas, y además reescribía TODOS los `<lastmod>` con la fecha
de ejecución, borrando la fecha real del último cambio de cada página. Estaba
bloqueado con un abort desde el 2026-08-01; esto lo arregla.

Principio: **el sitemap manda sobre el script**. Los `<lastmod>`, `<changefreq>`
y `<priority>` de una URL que ya está en el sitemap se conservan tal cual — son
valores afinados a mano a lo largo de meses y el script no tiene forma de
recuperarlos. El script solo:

  - añade las páginas nuevas (fecha de hoy y los valores por familia de más
    abajo, tomados de lo que ya usan sus hermanas),
  - quita las URLs cuya página ha dejado de existir,
  - respeta el orden y el formato del fichero actual, para que regenerarlo sin
    cambios en el árbol no produzca ni un byte de diferencia.

Uso:
    python scripts/regenerate_sitemap.py           # reescribe sitemap.xml
    python scripts/regenerate_sitemap.py --check   # solo compara, exit 1 si difiere
"""
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# clean_url es la traducción fichero -> URL que sirve Workers Assets; se comparte
# con gen_redirects.py para que redirecciones y sitemap no puedan discrepar.
# qa_check.py mantiene a propósito su propia copia: es el guardián y no debe
# validar al generador con la lógica del generador.
from gen_redirects import clean_url, rel  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("RENDATA_SITE") or os.path.join(ROOT, "rendata_beta")
SITEMAP = os.path.join(SITE, "sitemap.xml")
DOMAIN = "https://rendata.es"
TODAY = date.today().isoformat()

# Nunca entran en el sitemap.
EXCLUDE = {"404.html"}
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex',
                     re.I)

# Valores para páginas NUEVAS, por familia. Salen de lo que ya usan sus hermanas
# en el sitemap actual, así una ficha nueva nace con los mismos que las otras 588.
FAMILIAS = [
    (re.compile(r"^/$"),                      "daily",   "1.0"),
    (re.compile(r"^/academia/"),              "yearly",  "0.6"),
    (re.compile(r"^/en/"),                    "monthly", "0.7"),
    (re.compile(r"^/rentabilidad-"),          "monthly", "0.8"),
    (re.compile(r"^/ccaa-"),                  "monthly", "0.7"),
    (re.compile(r"^/barrios-"),               "monthly", "0.6"),
    (re.compile(r"^/vivir-en-"),              "monthly", "0.6"),
    (re.compile(r"^/mercado-inmobiliario-"),  "monthly", "0.7"),
]
POR_DEFECTO = ("monthly", "0.6")

ENTRY = re.compile(
    r"<url>\s*<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>\s*"
    r"<changefreq>(.*?)</changefreq>\s*<priority>(.*?)</priority>\s*</url>", re.S)


def paginas():
    """{ruta URL: fichero} de todas las páginas indexables del árbol."""
    out = {}
    for base, _, files in os.walk(SITE):
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            p = rel(os.path.join(base, f))
            if p in EXCLUDE:
                continue
            txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
            if NOINDEX.search(txt):
                continue
            out[clean_url(p)] = p
    return out


def actual():
    """(entradas del sitemap en su orden, salto de línea del fichero, texto crudo)."""
    if not os.path.exists(SITEMAP):
        return [], "\n", ""
    crudo = open(SITEMAP, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in crudo else "\n"
    entradas = [(re.sub(r"^https?://[^/]+", "", loc) or "/", lm, cf, pr)
                for loc, lm, cf, pr in ENTRY.findall(crudo)]
    return entradas, nl, crudo


def defecto(ruta):
    for rx, cf, pr in FAMILIAS:
        if rx.match(ruta):
            return cf, pr
    return POR_DEFECTO


def construir(previas, quiero):
    """Entradas finales: conserva las que siguen existiendo, añade las nuevas."""
    vistas, salida = set(), []
    for ruta, lm, cf, pr in previas:
        if ruta in quiero and ruta not in vistas:
            salida.append((ruta, lm, cf, pr))
            vistas.add(ruta)
    nuevas = sorted(set(quiero) - vistas)
    for ruta in nuevas:
        cf, pr = defecto(ruta)
        salida.append((ruta, TODAY, cf, pr))
    return salida, nuevas, [r for r, *_ in previas if r not in quiero]


def render(entradas, nl):
    bloques = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for ruta, lm, cf, pr in entradas:
        bloques += [
            "  <url>",
            f"    <loc>{DOMAIN}{ruta}</loc>",
            f"    <lastmod>{lm}</lastmod>",
            f"    <changefreq>{cf}</changefreq>",
            f"    <priority>{pr}</priority>",
            "  </url>",
        ]
    bloques += ["</urlset>", ""]
    return nl.join(bloques)


def main():
    previas, nl, crudo = actual()
    quiero = paginas()
    entradas, nuevas, retiradas = construir(previas, quiero)
    out = render(entradas, nl)

    if "--check" in sys.argv:
        if out == crudo:
            print(f"regenerate_sitemap: sitemap.xml al dia ({len(entradas)} URLs)")
            return 0
        print(f"regenerate_sitemap: sitemap.xml DESACTUALIZADO "
              f"({len(entradas)} URLs esperadas, {len(previas)} en el fichero)")
        if nuevas:
            print(f"  faltan {len(nuevas)}: {nuevas[:8]}")
        if retiradas:
            print(f"  sobran {len(retiradas)}: {retiradas[:8]}")
        if not nuevas and not retiradas:
            print("  mismas URLs pero el fichero difiere (formato, orden o metadatos)")
        print("  Ejecuta: python scripts/regenerate_sitemap.py")
        return 1

    with open(SITEMAP, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"regenerate_sitemap: {len(entradas)} URLs escritas en {rel(SITEMAP)}")
    print(f"  nuevas: {len(nuevas)}{' ' + str(nuevas[:5]) if nuevas else ''}")
    print(f"  retiradas: {len(retiradas)}{' ' + str(retiradas[:5]) if retiradas else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
