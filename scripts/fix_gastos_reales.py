#!/usr/bin/env python3
"""Mass-fix idempotente de la tabla "Gastos reales" (opción 1 aprobada).

DIAGNÓSTICO (informe 2026-07-27)
--------------------------------
El modelo implícito del sitio es un piso de 100 m²: roi = alq*12/(p*100). Lo
confirma DATA[] (596/597) y la metodología publicada en la comparativa
Madrid vs Barcelona. Pero la tabla de gastos estaba en tres estados:

  A) 360 fichas con la plantilla idéntica sin personalizar (ingresos 6.000€/año)
  B) 127 fichas calculadas con un `alq` de un trimestre anterior
  C) 110 fichas con los ingresos correctos

y, en las 597, la fila del neto NO cuadraba con la tabla que resume.

FÓRMULA APLICADA
----------------
  ingresos_anuales = alq(DATA) * 12          ingresos_mensuales = alq(DATA)
  cada gasto       = su % actual de la propia ficha * ingresos nuevos
  neto_€           = ingresos - suma(gastos)     <- ahora sí cuadra
  neto_%           = neto_€ / (p(DATA) * 100)
  título           = "Del {roi}% bruto al {neto_%}% neto — Gastos reales"

No se inventa ningún porcentaje: se conserva la estructura de costes propia de
cada ficha y solo se corrige la base y la aritmética. A las del grupo A se les
añade una línea discreta advirtiendo de que son parámetros medios.

También liga a DATA[] la frase de la FAQ "el precio del m² sube un X% anual",
que en 165 fichas usaba otro valor y en 101 de ellas era `va` (subida del
ALQUILER) en vez de `vp` (subida del PRECIO).

RESPETA LA CONGELACIÓN: los ficheros de frozen_files.json no se tocan.

Uso:  python scripts/fix_gastos_reales.py
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

# Firma de la tabla-plantilla sin personalizar (grupo A), pre-fix:
# ingresos, IBI, comunidad, mantenimiento, seguro, vacancia, IRPF
BOILERPLATE = (6000, 220, 408, 360, 240, 360, 720)

NOTA_EST = (
    '<p class="gastos-nota-est" style="margin:.65rem 0 0;font-size:.78rem;'
    'color:var(--muted);line-height:1.45">Estimación con parámetros medios '
    '(IBI, comunidad y vacancia pueden variar según el inmueble concreto).</p>'
)

GASTO_LABELS = [
    ("ibi", "IBI (Impuesto sobre Bienes Inmuebles)"),
    ("com", "Gastos de comunidad"),
    ("man", "Mantenimiento y reparaciones"),
    ("seg", "Seguro de hogar e impagos"),
    ("vac", "Vacancia estimada"),
    ("irpf", "IRPF sobre rendimientos"),
]

RE_ING = re.compile(
    r'(<div class="gasto-name">[^<]*Ingresos por alquiler</div>\s*'
    r'<div class="gasto-val" style="color:var\(--green\)">\+)([\d.]+)'
    r'(€</div>\s*<div class="gasto-val" style="color:var\(--green\)">\+)([\d.]+)(€</div>)'
)
RE_NETO = re.compile(
    r'(Rentabilidad neta estimada</div>\s*<div class="gasto-val"[^>]*>)([\d,]+)'
    r'(%</div>\s*<div class="gasto-val"[^>]*>)([\d.]+)(€/año</div>)'
)
RE_VAC_LBL = re.compile(r'(Vacancia estimada \()([\d,]+)(% del año\))')
RE_TITULO = re.compile(
    r'(<span class="coll-trigger-title">Del )([\d,]+)(% bruto al )([\d,]+)(% neto)'
)
RE_FAQ_VP = re.compile(r'(el precio del m² sube un )([\d,]+)(% anual)')
RE_CARD_END = re.compile(r'(\n\s*</div>\n\s*</div><!-- coll-body-inner -->)')


def gasto_re(label):
    return re.compile(
        r'(<div class="gasto-name">[^<]*' + re.escape(label) + r'[^<]*</div>\s*'
        r'<div class="gasto-val" style="color:var\(--red\)">-)([\d.]+)'
        r'(€</div>\s*<div class="gasto-val"[^>]*>)(-[\d.]+€|Variable)(</div>)'
    )


GASTO_RES = {k: gasto_re(lbl) for k, lbl in GASTO_LABELS}


def eur(v):
    return f"{int(v):,}".replace(",", ".")


def num(s):
    return int(s.replace(".", ""))


def pct1(v):
    return f"{v:.1f}".replace(".", ",")


def load_data():
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    mm = re.search(r"const DATA=\[(.*?)\n\];", idx, re.S)
    if not mm:
        sys.exit("No se encontró DATA[] en index.html")
    out = {}
    for bm in re.finditer(r"\{[^{}]*\}", mm.group(1)):
        b = bm.group(0)
        sl = re.search(r'sl:"([^"]+)"', b)
        roi = re.search(r"roi:([-\d.]+)", b)
        p = re.search(r"p:(\d+)", b)
        alq = re.search(r"alq:(\d+)", b)
        vp = re.search(r"vp:([-\d.]+)", b)
        if sl and roi and p and alq and vp:
            out[sl.group(1)] = {
                "roi": float(roi.group(1)), "p": int(p.group(1)),
                "alq": int(alq.group(1)), "vp": float(vp.group(1)),
            }
    return out


def fix_one(text, city):
    """Devuelve (texto_nuevo, grupo) o (texto, None) si no hay tabla."""
    m_ing = RE_ING.search(text)
    if not m_ing:
        return text, None
    ing_old = num(m_ing.group(2))
    if ing_old <= 0:
        return text, None

    # --- leer los gastos actuales y derivar su % sobre los ingresos actuales ---
    gastos_old, pcts = {}, {}
    for k in GASTO_RES:
        m = GASTO_RES[k].search(text)
        if not m:
            return text, None
        gastos_old[k] = num(m.group(2))
        pcts[k] = gastos_old[k] / ing_old

    grupo = "A" if (ing_old, *[gastos_old[k] for k, _ in GASTO_LABELS]) == BOILERPLATE \
        else ("C" if ing_old == city["alq"] * 12 else "B")
    if 'class="gastos-nota-est"' in text:
        grupo = "A"          # ya marcada como plantilla en una pasada anterior

    # --- recalcular con la base correcta ---
    ing_new = city["alq"] * 12
    gastos_new = {k: int(round(pcts[k] * ing_new)) for k in pcts}
    neto_eur = ing_new - sum(gastos_new.values())
    neto_pct = neto_eur / (city["p"] * 100) * 100

    # --- escribir ---
    text = RE_ING.sub(
        lambda m: m.group(1) + eur(ing_new) + m.group(3) + eur(city["alq"]) + m.group(5),
        text, count=1)

    for k in GASTO_RES:
        v = gastos_new[k]

        def rep(m, v=v):
            mes = m.group(4)
            if mes != "Variable":
                mes = "-" + eur(round(v / 12)) + "€"
            return m.group(1) + eur(v) + m.group(3) + mes + m.group(5)

        text = GASTO_RES[k].sub(rep, text, count=1)

    text = RE_VAC_LBL.sub(
        lambda m: m.group(1) + pct1(pcts["vac"] * 100) + m.group(3), text, count=1)
    text = RE_NETO.sub(
        lambda m: m.group(1) + pct1(neto_pct) + m.group(3) + eur(neto_eur) + m.group(5),
        text, count=1)
    text = RE_TITULO.sub(
        lambda m: m.group(1) + pct1(city["roi"]) + m.group(3) + pct1(neto_pct) + m.group(5),
        text, count=1)

    # --- nota de estimación solo en el grupo A ---
    if grupo == "A" and 'class="gastos-nota-est"' not in text:
        text = RE_CARD_END.sub(lambda m: "\n      " + NOTA_EST + m.group(1), text, count=1)

    return text, grupo


def main():
    data = load_data()
    frozen = set(json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"])
    print(f"DATA[]: {len(data)} municipios · {len(frozen)} ficheros congelados")

    grupos = Counter()
    touched = 0
    faq_fixed = 0
    notas = 0
    blocked = []
    sin_tabla = []

    for path in sorted(glob.glob(os.path.join(SITE, "rentabilidad-*.html"))):
        base = os.path.basename(path)
        slug = base[len("rentabilidad-"):-len(".html")]
        city = data.get(slug)
        if not city:
            continue
        original = open(path, encoding="utf-8", errors="ignore").read()

        text, grupo = fix_one(original, city)
        if grupo is None:
            sin_tabla.append(slug)

        # FAQ: "el precio del m² sube un X% anual" -> vp (precio), nunca va
        before_faq = text
        text = RE_FAQ_VP.sub(
            lambda m: m.group(1) + pct1(city["vp"]) + m.group(3), text, count=1)
        faq_changed = text != before_faq

        if text == original:
            if grupo:
                grupos[grupo] += 1
            continue
        if base in frozen:
            blocked.append((base, grupo))
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        touched += 1
        if grupo:
            grupos[grupo] += 1
        if faq_changed:
            faq_fixed += 1
        if grupo == "A" and 'class="gastos-nota-est"' in text:
            notas += 1

    print(f"\nFichas reescritas: {touched}")
    print(f"  grupo A (plantilla, con nota de estimación): {grupos['A']}")
    print(f"  grupo B (trimestre anterior)               : {grupos['B']}")
    print(f"  grupo C (ya correctas, solo se recalcula el neto): {grupos['C']}")
    print(f"  notas de estimación añadidas en esta pasada: {notas}")
    print(f"  frases FAQ 'sube un X% anual' ligadas a vp : {faq_fixed}")
    if sin_tabla:
        print(f"  sin tabla de gastos (no tocadas): {len(sin_tabla)} {sin_tabla[:5]}")
    if blocked:
        print(f"\nBLOQUEADAS POR CONGELACIÓN ({len(blocked)}) — anotar en "
              f"PENDIENTES_DESCONGELACION.md:")
        for b, g in blocked:
            print(f"  {b}  (grupo {g})")
    else:
        print("\nNinguna ficha congelada necesitaba cambios.")


if __name__ == "__main__":
    main()
