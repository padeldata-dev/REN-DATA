#!/usr/bin/env python3
"""Mass-fix idempotente: liga a DATA[] TODOS los huecos de precio/alquiler de la ficha.

CAUSA RAÍZ
----------
Continuación de `fix_roi_hero_badge.py`, que en julio de 2026 ligó a DATA[] los
bloques de **ROI**. El mismo problema seguía vivo para **precio, alquiler y sus
variaciones anuales**: las fichas nacen de un generador archivado y desde
entonces se mantienen con fixers en masa, y los sucesivos syncs solo escribían
en los huecos que vigilaba `qa_check[8]` (`<title>`, sticky-ROI, `ed-stat`,
meta-ROI, meta-precio). Todo lo demás —hero, barra sticky, gráfico de
evolución, "Pulso del mercado", FAQ JSON-LD y la prosa editorial— se quedó con
el precio y el alquiler ANTIGUOS del municipio, invisibles para el QA.

Que DATA[] es la autoridad está verificado: sus 477 municipios cubiertos por el
pipeline coinciden al 100% con `data/processed/cities_2026Q3.csv` (0 desviaciones
en precio, alquiler, roi, vp, va y días).

Este script fija UNA sola autoridad -> DATA[] de index.html, en 24 huecos:

  META/OG   meta description y og:description: alquiler + tipo de ITP
  JSON-LD   "description" (precio, alquiler, ROI) y las 3 FAQ con cifras
  STICKY    barra inferior: precio y alquiler
  HERO      precio + % anual (vp), alquiler + % anual (va), flecha y clase
  ITP       tipo, importe y badge de la tarjeta, desde ITP_CCAA (ver abajo)
  EVO       precio actual, badge de % anual y la SERIE HISTÓRICA
  PULSO     días de media en mercado
  PROSA     días, precio, subida de precio, ROI, subida y nivel del alquiler

FICHEROS CONGELADOS
-------------------
`frozen_files.json` está activo (campaña de prensa). Las 7 fichas congeladas se
SALTAN y se listan al final para anotarlas en PENDIENTES_DESCONGELACION.md.

SERIE HISTÓRICA (decisión explícita, 2026-07-29)
------------------------------------------------
El gráfico "Evolución del precio" NO tiene fuente: el pipeline solo produce
valores actuales, no series anuales. 74 fichas dibujaban una serie DESCENDENTE
con la etiqueta "↑ X%", y en 263 el último punto no era ni siquiera el precio
de DATA[]. Invertir la flecha (lo primero que se pensó) habría hecho que la
página contradijera a DATA[], que dice que el precio SUBE en las 597.

Se reconstruye la serie por retroproyección a tipo constante:

    v(año) = p / (1 + vp/100) ** (2026 - año)      años: 2019, 2021, 2023, 2024, 2026

redondeada a 10 €. Es una serie MODELIZADA, no medida: por eso este script
también corrige el pie del gráfico, que atribuía la serie al Ministerio de
Vivienda. Solo se reconstruyen las series rotas (último punto != precio de
DATA[], o no monótona); las coherentes no se tocan, para no generar churn.

TIPOS DE ITP (decisión explícita, 2026-07-29)
---------------------------------------------
El repo tenía TRES tablas de ITP que se contradecían (Baleares 9 vs 11, Galicia
9 vs 10, País Vasco 4 vs 7). Se adopta como canónica `ITP_CCAA` de
`rendata_beta/comparador.html`, que es la única fechada ("vigente 2026") y la
única que cubre Ceuta y Melilla.

Uso:  python scripts/fix_ficha_sync.py [--dry-run]
Re-ejecutarlo no produce cambios adicionales.
"""
import glob
import json
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
FROZEN_JSON = os.path.join(ROOT, "frozen_files.json")

DRY = "--dry-run" in sys.argv
stats = Counter()

# Tabla canónica de ITP — copiada de rendata_beta/comparador.html (ITP_CCAA).
ITP_CCAA = {
    "C. de Madrid": 6.0, "Navarra": 6.0, "Canarias": 6.5, "País Vasco": 4.0,
    "Andalucía": 7.0, "La Rioja": 7.0, "Aragón": 8.0, "Asturias": 8.0,
    "Castilla y León": 8.0, "R. de Murcia": 8.0, "Cantabria": 9.0,
    "Castilla-La Mancha": 9.0, "Galicia": 9.0, "Cataluña": 10.0,
    "C. Valenciana": 10.0, "Extremadura": 8.0, "Islas Baleares": 9.0,
    "Ceuta": 0.5, "Melilla": 0.5,
}
SUP_DEFAULT = 76          # m² de referencia de la tarjeta ITP (moda del corpus)
EVO_YEARS = (2019, 2021, 2023, 2024, 2026)
EVO_H_MIN, EVO_H_MAX = 62, 92
EVO_FUENTE = "Serie modelizada sobre el precio actual y su variación anual · Ren Data"


# --------------------------------------------------------------------------
# Fuente de verdad
# --------------------------------------------------------------------------
def load_data():
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    mm = re.search(r"const DATA=\[(.*?)\n\];", idx, re.S)
    if not mm:
        sys.exit("No se encontró DATA[] en index.html")
    out = {}
    for bm in re.finditer(r"\{[^{}]*\}", mm.group(1)):
        b = bm.group(0)
        g = lambda k, pat=r"([-\d.]+)": (re.search(k + r":" + pat, b) or [None, None])
        sl = re.search(r'sl:"([^"]+)"', b)
        cc = re.search(r'cc:"([^"]+)"', b)
        if not sl:
            continue
        rec = {"sl": sl.group(1), "cc": cc.group(1) if cc else ""}
        ok = True
        for k, cast in (("roi", float), ("p", int), ("alq", int),
                        ("vp", float), ("va", float), ("d", int)):
            m = re.search(k + r":([-\d.]+)", b)
            if not m:
                ok = False
                break
            rec[k] = cast(m.group(1))
        if ok:
            out[rec["sl"]] = rec
    return out


def eu(v):
    """1300 -> '1.300' (separador de miles español)."""
    return "{:,}".format(int(round(v))).replace(",", ".")


def pct(v, sep=","):
    return ("%.1f" % v).replace(".", sep)


def itp_fmt(v):
    return ("%d" % v) if float(v).is_integer() else ("%.1f" % v).replace(".", ",")


def itp_badge(rate):
    if rate <= 6.5:
        return "itp-low", "Favorable"
    if rate <= 8.0:
        return "itp-med", "Medio"
    return "itp-high", "Elevado"


# --------------------------------------------------------------------------
# Sustituciones. Cada una recibe el texto y el municipio y devuelve el texto.
# `sub1` sustituye SOLO el grupo 1 de cada match y contabiliza los cambios.
# --------------------------------------------------------------------------
def sub1(text, rx, want, key, gi=1):
    """Sustituye SOLO el grupo `gi` de cada match y contabiliza los cambios."""
    def rep(m):
        if m.group(gi) != want:
            stats[key] += 1
        return m.group(0)[:m.start(gi) - m.start(0)] + want + m.group(0)[m.end(gi) - m.start(0):]
    return rx.sub(rep, text)


R = re.compile


def fix_meta(t, c):
    a, i = eu(c["alq"]), itp_fmt(ITP_CCAA.get(c["cc"], 8.0))
    t = sub1(t, R(r'<meta name="description" content="[^"]*?€, alquiler ([\d.]+)€/mes'), a, "meta_alq")
    t = sub1(t, R(r'<meta property="og:description" content="[^"]*?€, alquiler ([\d.]+)€/mes'), a, "og_alq")
    t = sub1(t, R(r'(?:name="description"|property="og:description") content="[^"]*?€/mes\. ITP ([\d,.]+)% en'), i, "meta_itp")
    return t


def fix_jsonld(t, c):
    p, a, r = eu(c["p"]), eu(c["alq"]), pct(c["roi"])
    t = sub1(t, R(r'"description":"Análisis de rentabilidad inmobiliaria en [^"]*?\. Precio m² ([\d.]+)€'), p, "jsonld_p")
    t = sub1(t, R(r'"description":"Análisis de rentabilidad inmobiliaria en [^"]*?alquiler medio ([\d.]+)€/mes'), a, "jsonld_alq")
    t = sub1(t, R(r'"description":"Análisis de rentabilidad inmobiliaria en [^"]*?ROI estimado ([\d,.]+)%'), r, "jsonld_roi")
    # FAQ 1 — ROI de la ciudad (NO el de la zona, que va después en la misma frase)
    t = sub1(t, R(r'La rentabilidad bruta estimada del alquiler en [^"]*? en 2026 se sitúa en el ([\d,.]+)%'), r, "faq_roi")
    # FAQ 2 — precio, piso de 100 m² y subida anual
    t = sub1(t, R(r'El precio medio del metro cuadrado en [^"]*? es de ([\d.]+)€/m²'), p, "faq_p")
    t = sub1(t, R(r'Un piso de 100 m² costaría aproximadamente ([\d.]+)€'), eu(c["p"] * 100), "faq_piso")
    t = sub1(t, R(r'En los últimos 12 meses el precio ha subido un ([\d,.]+)%'), pct(c["vp"]), "faq_vp")
    # FAQ 3 — alquiler, derivados (x0,72 y x1,30) y subida anual
    t = sub1(t, R(r'El alquiler medio en [^"]*? es de ([\d.]+)€/mes para un piso estándar'), a, "faq_alq")
    t = sub1(t, R(r'Un piso de una habitación puede alcanzar los ([\d.]+)€/mes'), eu(round(c["alq"] * 0.72)), "faq_alq1")
    t = sub1(t, R(r'uno de tres habitaciones puede superar los ([\d.]+)€/mes'), eu(round(c["alq"] * 1.30)), "faq_alq3")
    t = sub1(t, R(r'Los alquileres en [^"]*? han subido un ([\d,.]+)% en el último año'), pct(c["va"]), "faq_va")
    return t


def fix_sticky(t, c):
    t = sub1(t, R(r'<span class="sb-label">Precio m²</span><span class="sb-val[^"]*">([\d.]+)€'), eu(c["p"]), "sticky_p")
    t = sub1(t, R(r'<span class="sb-label">Alquiler</span><span class="sb-val[^"]*">([\d.]+)€/mes'), eu(c["alq"]), "sticky_alq")
    return t


HERO_P = R(r'(<div class="sl">Precio m²</div><div class="sv"[^>]*>)([\d.]+)(€</div><div style="[^"]*"><span class="badge badge-)(up|down)(">)([↑↓])( )([\d,]+)(% anual</span>)')
HERO_A = R(r'(<div class="sl">Alquiler medio</div><div class="sv"[^>]*>)([\d.]+)(€</div><div style="[^"]*"><span class="badge badge-)(up|down)(">)([↑↓])( )([\d,]+)(% anual</span>)')


def _hero(t, rx, val, var, key):
    def rep(m):
        cls = "up" if var >= 0 else "down"
        arr = "↑" if var >= 0 else "↓"
        v, p_ = eu(val), pct(abs(var))
        if m.group(2) != v or m.group(4) != cls or m.group(6) != arr or m.group(8) != p_:
            stats[key] += 1
        return m.group(1) + v + m.group(3) + cls + m.group(5) + arr + m.group(7) + p_ + m.group(9)
    return rx.sub(rep, t)


def fix_hero(t, c):
    t = _hero(t, HERO_P, c["p"], c["vp"], "hero_precio")
    t = _hero(t, HERO_A, c["alq"], c["va"], "hero_alquiler")
    return t


ITP_VAL = R(r'(<div class="itp-val">)([\d,.]+)(<span class="itp-pct">%</span></div>)')
ITP_BADGE = R(r'(<span class="itp-badge )(itp-\w+)(">)([^<]+)(</span>)')
ITP_DESC = R(r'(<div class="itp-desc">Para un piso de )([\d.]+)(€ pagarás <strong>)([\d.]+)(€ de (?:ITP|IGIC|IPSI)</strong></div>)')


def fix_itp(t, c):
    rate = ITP_CCAA.get(c["cc"])
    if rate is None:
        stats["itp_ccaa_desconocida"] += 1
        return t
    cls, lbl = itp_badge(rate)
    want = itp_fmt(rate)
    t = sub1(t, ITP_VAL, want, "itp_tipo", gi=2)

    def repb(m):
        if m.group(2) != cls or m.group(4) != lbl:
            stats["itp_badge"] += 1
        return m.group(1) + cls + m.group(3) + lbl + m.group(5)
    t = ITP_BADGE.sub(repb, t)

    def repd(m):
        piso_old = int(m.group(2).replace(".", ""))
        # conserva la superficie de la tarjeta si sigue siendo coherente con el
        # precio actual; si no (o si es la de plantilla), usa la de referencia
        sup = piso_old // c["p"] if (piso_old % c["p"] == 0 and 60 <= piso_old // c["p"] <= 110) else SUP_DEFAULT
        piso = c["p"] * sup
        imp = int(round(piso * rate / 100))
        if m.group(2) != eu(piso) or m.group(4) != eu(imp):
            stats["itp_importe"] += 1
        return m.group(1) + eu(piso) + m.group(3) + eu(imp) + m.group(5)
    return ITP_DESC.sub(repd, t)


EVO_NOW = R(r'(Precio actual</span><div style="[^"]*">)([\d.]+)( €/m²)')
EVO_PCT = R(r'(<span class="badge badge-)(up|down)(">)([↑↓])( )([\d,]+)(% último año</span>)')
EVO_COL = R(r'<div class="evo-col"><span class="evo-v( cur)?">([\d.]+)€</span>'
            r'<div class="evo-bar( cur)?" style="height:(\d+)%"></div>'
            r'<span class="evo-l( cur)?">(\d{4})([^<]*)</span></div>')
EVO_SRC = R(r'(<p>Precio medio de venta por m² · 2019–2026 · )(Fuente: Ministerio de Vivienda)(</p>)')


def fix_evo(t, c):
    t = sub1(t, EVO_NOW, eu(c["p"]), "evo_precio", gi=2)

    def repp(m):
        cls = "up" if c["vp"] >= 0 else "down"
        arr = "↑" if c["vp"] >= 0 else "↓"
        v = pct(abs(c["vp"]))
        if m.group(2) != cls or m.group(4) != arr or m.group(6) != v:
            stats["evo_badge"] += 1
        return m.group(1) + cls + m.group(3) + arr + m.group(5) + v + m.group(7)
    t = EVO_PCT.sub(repp, t)

    cols = EVO_COL.findall(t)
    if len(cols) == 5:
        vals = [int(x[1].replace(".", "")) for x in cols]
        roto = vals[-1] != c["p"] or any(vals[i + 1] < vals[i] for i in range(4))
        if roto:
            g = 1.0 + c["vp"] / 100.0
            new = [int(round(c["p"] / (g ** (2026 - y)) / 10.0)) * 10 for y in EVO_YEARS]
            new[-1] = c["p"]
            for i in range(3, -1, -1):          # garantiza monotonía tras redondear
                new[i] = min(new[i], new[i + 1])
            lo, hi = new[0], new[-1]
            span = (hi - lo) or 1
            hs = [int(round(EVO_H_MIN + (EVO_H_MAX - EVO_H_MIN) * (v - lo) / span)) for v in new]
            it = iter(zip(new, hs))

            def repc(m):
                v, h = next(it)
                cur = m.group(1) or ""
                return ('<div class="evo-col"><span class="evo-v%s">%s€</span>'
                        '<div class="evo-bar%s" style="height:%d%%"></div>'
                        '<span class="evo-l%s">%s%s</span></div>'
                        % (cur, eu(v), m.group(3) or "", h, m.group(5) or "", m.group(6), m.group(7)))
            t = EVO_COL.sub(repc, t)
            stats["evo_serie"] += 1
    else:
        stats["evo_serie_ilegible"] += 1

    def reps(m):
        stats["evo_fuente"] += 1
        return m.group(1) + EVO_FUENTE + m.group(3)
    t = EVO_SRC.sub(reps, t)
    return t


def fix_pulso(t, c):
    return sub1(t, R(r'<div class="ival">(\d+)</div><div class="ilabel">Días de media en mercado'),
                str(c["d"]), "pulso_dias")


def fix_prosa(t, c):
    t = sub1(t, R(r'con los pisos vendiéndose en tan solo (\d+) días de media'), str(c["d"]), "prosa_dias")
    # el precio de la prosa llevaba separador de miles anglosajón en algunas fichas
    t = sub1(t, R(r'El precio del metro cuadrado ha alcanzado los ([\d.,]+)€'), eu(c["p"]), "prosa_precio")
    t = sub1(t, R(r'ha alcanzado los [\d.]+€, tras una subida del ([\d,.]+)% en el último año'), pct(c["vp"], "."), "prosa_vp")
    t = sub1(t, R(r'La rentabilidad bruta del alquiler se sitúa en el ([\d,.]+)%'), pct(c["roi"]), "prosa_roi")
    t = sub1(t, R(r'El alquiler medio ha subido un ([\d,.]+)% en los últimos 12 meses'), pct(c["va"], "."), "prosa_va")
    t = sub1(t, R(r'en los últimos 12 meses, alcanzando los ([\d.,]+)€ mensuales'), eu(c["alq"]), "prosa_alq")
    return t


FIXERS = (fix_meta, fix_jsonld, fix_sticky, fix_hero, fix_itp, fix_evo, fix_pulso, fix_prosa)


def main():
    data = load_data()
    frozen = set(json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"])
    print("DATA[]: %d municipios · tabla ITP: %d CCAA · congelados: %d"
          % (len(data), len(ITP_CCAA), len(frozen)))
    if DRY:
        print("*** DRY-RUN: no se escribe nada ***")

    touched, skipped_frozen, sin_data = 0, [], []
    for path in sorted(glob.glob(os.path.join(SITE, "rentabilidad-*.html"))):
        name = os.path.basename(path)
        slug = name[len("rentabilidad-"):-len(".html")]
        c = data.get(slug)
        if not c:
            sin_data.append(slug)
            continue
        if name in frozen:
            skipped_frozen.append(name)
            continue
        original = open(path, encoding="utf-8", errors="ignore").read()
        text = original
        for f in FIXERS:
            text = f(text, c)
        if text != original:
            touched += 1
            if not DRY:
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(text)

    print("\nFichas reescritas: %d" % touched)
    print("Correcciones por hueco:")
    for k in sorted(stats):
        print("  %-24s %d" % (k, stats[k]))
    if skipped_frozen:
        print("\nCONGELADAS (no tocadas, anotar en PENDIENTES_DESCONGELACION.md):")
        for n in skipped_frozen:
            print("  - %s" % n)
    if sin_data:
        print("\nSin entrada en DATA[] (no tocadas): %s" % sin_data)


if __name__ == "__main__":
    main()
