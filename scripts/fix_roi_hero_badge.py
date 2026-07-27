#!/usr/bin/env python3
"""Mass-fix idempotente: liga a DATA[] los 4 bloques de ROI que quedaron sueltos.

CAUSA RAÍZ
----------
Las fichas nacen de un generador ya archivado y desde entonces se mantienen con
fixers en masa. Convivían DOS autoridades contradictorias:

  * `fix_all.py`  -> trata el bloque HERO como fuente de verdad y propaga hacia
                     el editorial.
  * sync posterior -> trata DATA[] (index.html) como fuente de verdad, pero solo
                     escribe en <title>, sticky y ed-stat, que son exactamente
                     los tres huecos que vigila qa_check[8].

Resultado: el HERO, el badge "Media España" y el título del desplegable de
gastos se quedaron con el ROI ANTIGUO del municipio, invisibles para el QA.
Además el badge nunca estuvo ligado a ninguna media: nació con el literal 6,5%
(media nacional de la edición de 209 ciudades) y en las fichas resincronizadas
se sobrescribió con el ROI del propio municipio, etiquetado "Media España".

Este script fija UNA sola autoridad -> DATA[] de index.html:
  1. HERO  "Rentabilidad bruta estimada"  = roi del municipio (y normaliza el
     marcado roto de las fichas que perdieron el <div class="sv">).
  2. BADGE "Media España X%"              = media real de DATA[], una constante.
  3. GASTOS "Del X% bruto al Y% neto"     = X del municipio (Y NO se toca: sale
     de la fila "Rentabilidad neta estimada" de la propia tabla).
  4. INFO-BOX "Posición nacional"         = media real + roi + dirección coherente.
  5. META/OG description                  = roi y precio de DATA[] si desvían.
  6. Benahavís: % de comprador extranjero (ver nota abajo).

Uso:  python scripts/fix_roi_hero_badge.py
Re-ejecutarlo no produce cambios adicionales.
"""
import glob
import os
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "rendata_beta")

stats = Counter()


# --------------------------------------------------------------------------
# Fuente de verdad: DATA[] de index.html
# --------------------------------------------------------------------------
def load_data():
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    mm = re.search(r"const DATA=\[(.*?)\n\];", idx, re.S)
    if not mm:
        sys.exit("No se encontró DATA[] en index.html")
    out = {}
    for bm in re.finditer(r"\{[^{}]*\}", mm.group(1)):
        b = bm.group(0)
        sl = re.search(r'sl:"([^"]+)"', b)
        n = re.search(r'n:"([^"]+)"', b)
        roi = re.search(r"roi:([-\d.]+)", b)
        p = re.search(r"p:(\d+)", b)
        alq = re.search(r"alq:(\d+)", b)
        if not (sl and roi and p):
            continue
        out[sl.group(1)] = {
            "n": n.group(1) if n else sl.group(1),
            "roi": float(roi.group(1)),
            "p": int(p.group(1)),
            "alq": int(alq.group(1)) if alq else None,
        }
    return out


def pct(v):
    return f"{v:.1f}".replace(".", ",")


def eu(v):
    return f"{v:,}".replace(",", ".")


# --------------------------------------------------------------------------
# Fix 1 — HERO
# --------------------------------------------------------------------------
HERO_OK = re.compile(
    r'(<div class="sl">Rentabilidad bruta estimada</div>\s*<div class="sv"[^>]*>)([\d,]+)(%</div>)'
)
# variante rota: el valor va suelto y el </div> del wrapper cierra antes de tiempo
HERO_BROKEN = re.compile(
    r'<div class="sl">Rentabilidad bruta estimada</div>([\d,]+)%</div>'
    r'(\s*)<div class="ss">Media ciudad · Q1 2026</div></div>'
)


def fix_hero(text, want):
    new, n = HERO_BROKEN.subn(
        lambda m: (
            '<div class="sl">Rentabilidad bruta estimada</div>'
            f'<div class="sv">{want}%</div>'
            f'{m.group(2)}<div class="ss">Media ciudad · Q1 2026</div></div>'
        ),
        text,
    )
    if n:
        stats["hero_markup_reparado"] += 1
        return new

    def rep(m):
        if m.group(2) != want:
            stats["hero_valor"] += 1
        return m.group(1) + want + m.group(3)

    return HERO_OK.sub(rep, text)


# --------------------------------------------------------------------------
# Fix 2 — BADGE "Media España"
# --------------------------------------------------------------------------
BADGE = re.compile(r'(<span class="badge badge-n">Media España )([\d,]+)(%</span>)')


def fix_badge(text, natl):
    def rep(m):
        if m.group(2) != natl:
            stats["badge"] += 1
        return m.group(1) + natl + m.group(3)

    return BADGE.sub(rep, text)


# --------------------------------------------------------------------------
# Fix 3 — título del desplegable de gastos (solo el BRUTO)
# --------------------------------------------------------------------------
GASTOS = re.compile(r'(<span class="coll-trigger-title">Del )([\d,]+)(% bruto al [\d,]+% neto)')


def fix_gastos(text, want):
    def rep(m):
        if m.group(2) != want:
            stats["gastos_bruto"] += 1
        return m.group(1) + want + m.group(3)

    return GASTOS.sub(rep, text)


# --------------------------------------------------------------------------
# Fix 4 — info-box "Posición nacional"
# --------------------------------------------------------------------------
INFOBOX = re.compile(
    r"(La rentabilidad media de España es el )([\d,]+)(%\. )(.+?)"
    r"( se sitúa en el )([\d,]+)(%, )(por encima de|por debajo de|en línea con)"
    r"( la media nacional\.)"
)


def fix_infobox(text, want, natl, roi, natl_f):
    def rep(m):
        if roi > natl_f + 1e-9:
            direction = "por encima de"
        elif roi < natl_f - 1e-9:
            direction = "por debajo de"
        else:
            direction = "en línea con"
        if m.group(2) != natl or m.group(6) != want or m.group(8) != direction:
            stats["infobox"] += 1
        return (
            m.group(1) + natl + m.group(3) + m.group(4)
            + m.group(5) + want + m.group(7) + direction + m.group(9)
        )

    return INFOBOX.sub(rep, text)


# --------------------------------------------------------------------------
# Fix 5 — meta description / og:description
# --------------------------------------------------------------------------
DESC = re.compile(
    r'(<meta (?:name="description"|property="og:description") content="[^"]*?: )'
    r'([\d,]+)(% ROI, precio m² )([\d.]+)(€)'
)


def fix_desc(text, want, precio_fmt):
    def rep(m):
        if m.group(2) != want or m.group(4) != precio_fmt:
            stats["meta_desc"] += 1
        return m.group(1) + want + m.group(3) + precio_fmt + m.group(5)

    return DESC.sub(rep, text)


# --------------------------------------------------------------------------
# Fix 6 — Benahavís: % de comprador extranjero
# --------------------------------------------------------------------------
# El 48% era el valor genérico heredado de la plantilla (el mismo que llevan
# Casares y Manilva, donde SÍ es correcto: el dossier fija "~48%" para ambos).
# Para Benahavís la cifra que sostiene el análisis provincial y su propio
# editorial es ">60%". Se deja como ">60%" y no como un número inventado
# porque el dossier advierte que solo la cifra provincial (~1/3) es medida.
FOREIGN_OVERRIDE = {"benahavis": (">60", "más del 60%")}


def fix_foreign(text, slug):
    if slug not in FOREIGN_OVERRIDE:
        return text
    val, _ = FOREIGN_OVERRIDE[slug]
    new, n1 = re.subn(
        r'(<div class="tend-desc">)(?:>?\d{1,3})(% de compradores internacionales\.)',
        rf"\g<1>{val}\g<2>",
        text,
    )
    new, n2 = re.subn(
        r"(presencia de compradores extranjeros \()\d{1,3}%(\))",
        rf"\g<1>{val}%\g<2>",
        new,
    )
    if n1 or n2:
        stats["extranjero_benahavis"] += 1
    return new


# --------------------------------------------------------------------------
def main():
    data = load_data()
    natl_f = sum(c["roi"] for c in data.values()) / len(data)
    natl = pct(natl_f)
    natl_r = round(natl_f, 1)
    print(f"DATA[]: {len(data)} municipios · media nacional real = "
          f"{natl_f:.4f}% -> badge '{natl}%'")

    files = sorted(glob.glob(os.path.join(SITE, "rentabilidad-*.html")))
    touched = 0
    skipped = []
    for path in files:
        slug = os.path.basename(path)[len("rentabilidad-"):-len(".html")]
        city = data.get(slug)
        if not city:
            skipped.append(slug)
            continue
        original = open(path, encoding="utf-8", errors="ignore").read()
        want = pct(city["roi"])
        text = original
        text = fix_hero(text, want)
        text = fix_badge(text, natl)
        text = fix_gastos(text, want)
        text = fix_infobox(text, want, natl, city["roi"], natl_r)
        text = fix_desc(text, want, eu(city["p"]))
        text = fix_foreign(text, slug)
        if text != original:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            touched += 1

    print(f"\nFichas reescritas: {touched}/{len(files)}")
    if skipped:
        print(f"Sin entrada en DATA[] (no tocadas): {skipped}")
    print("Correcciones por bloque:")
    for k in ("hero_valor", "hero_markup_reparado", "badge", "gastos_bruto",
              "infobox", "meta_desc", "extranjero_benahavis"):
        print(f"  {k:24s} {stats[k]}")


if __name__ == "__main__":
    main()
