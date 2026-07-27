#!/usr/bin/env python3
"""Mass-fix idempotente de la PROSA editorial: yield, y el cruce vp/va.

CONTEXTO
--------
Los fixers anteriores (d5f27ec5, 8441948e, 14e0511e) ligaron a DATA[] los huecos
ESTRUCTURADOS: hero, badge, ed-stat, título de gastos, info-box de posición
nacional, meta description y la frase de la FAQ "el precio del m² sube un X%
anual". qa_check[8] vigila esos huecos.

Pero las cifras que viven en TEXTO LIBRE se quedaron fuera, y ahí sobrevivían
tres patologías distintas — detectadas al verificar Ronda para prensa:

  1. "con un yield del X%" en el editorial contradecía el ROI del titular de la
     misma página (Ronda decía 5,6% con un hero de 5,5%).  -> 65 fichas

  2. CRUCE DE VARIABLE vp/va: varias frases sobre la subida del PRECIO mostraban
     `va`, que es la subida del ALQUILER. Es el mismo bug que ya se corrigió en
     la FAQ, pero en tres ubicaciones más que entonces no se tocaron:
       a) info-box "Mercado en expansión"
       b) "En los últimos 12 meses el precio ha subido un X%" (cuerpo + JSON-LD)
       c) "Si se suma la revalorización anual del inmueble (+X%)"

  3. CONSTANTE DE PLANTILLA: en el info-box, "el alquiler sube (+X%)" mostraba
     un literal **+15,0% en 182 fichas** (solo 1 tenía va=15,0 de verdad).
     Misma patología que el viejo badge "Media España 6,5%".

  4. Y un error de LÓGICA, no de cifra: la frase afirma "el alquiler sube aún
     más rápido" siempre, pero `va <= vp` en 198 municipios. Corregir solo los
     números dejaría 198 fichas diciendo "sube aún más rápido (+6,0%)" justo
     detrás de un precio que sube un 8,0%. Por eso la frase se reescribe por
     casos en vez de sustituir cifras.

RESPETA LA CONGELACIÓN: los ficheros de frozen_files.json no se tocan.

Uso:  python scripts/fix_prosa_vp_va.py
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

stats = Counter()

# 1) editorial: "con un yield del X%"  -> roi
RE_YIELD = re.compile(r"(yield del\s*(?:<strong>)?)([\d,]+)(%)")
# 2a) info-box "Mercado en expansión" (se regenera entera)
RE_EXPAN = re.compile(r"(<h3>Mercado en expansión</h3>\s*<p>)(.*?)(</p>)", re.S)
RE_CIUDAD = re.compile(r"El precio de la vivienda en (.+?) ha subido un")
# 2b) cuerpo + JSON-LD
RE_12M = re.compile(r"(En los últimos 12 meses el precio ha subido un )([\d,]+)(%)")
# 2c) recuperación de la inversión
RE_REVAL = re.compile(r"(revalorización anual del inmueble \(\+)([\d,]+)(%\))")


def pct(v):
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
        vp = re.search(r"vp:([-\d.]+)", b)
        va = re.search(r"va:([-\d.]+)", b)
        if sl and roi and vp and va:
            out[sl.group(1)] = {"roi": float(roi.group(1)),
                                "vp": float(vp.group(1)), "va": float(va.group(1))}
    return out


def frase_expansion(ciudad, vp, va):
    """La comparación se redacta según los datos, no se da por supuesta."""
    if va > vp:
        return (f"El precio de la vivienda en {ciudad} ha subido un {pct(vp)}% en el "
                f"último año. El alquiler sube aún más rápido (+{pct(va)}%), mejorando "
                f"la rentabilidad para el inversor.")
    if va < vp:
        return (f"El precio de la vivienda en {ciudad} ha subido un {pct(vp)}% en el "
                f"último año, por encima del alquiler (+{pct(va)}%), lo que comprime "
                f"la rentabilidad para el inversor.")
    return (f"El precio de la vivienda en {ciudad} ha subido un {pct(vp)}% en el "
            f"último año, al mismo ritmo que el alquiler (+{pct(va)}%).")


def fix_one(text, c):
    roi, vp, va = pct(c["roi"]), pct(c["vp"]), pct(c["va"])

    def rep_yield(m):
        if m.group(2) != roi:
            stats["yield"] += 1
        return m.group(1) + roi + m.group(3)
    text = RE_YIELD.sub(rep_yield, text)

    def rep_expan(m):
        cm = RE_CIUDAD.search(m.group(2))
        if not cm:
            return m.group(0)
        nueva = frase_expansion(cm.group(1), c["vp"], c["va"])
        if m.group(2).strip() != nueva:
            stats["info_box"] += 1
        return m.group(1) + nueva + m.group(3)
    text = RE_EXPAN.sub(rep_expan, text)

    def rep_12m(m):
        if m.group(2) != vp:
            stats["12_meses"] += 1
        return m.group(1) + vp + m.group(3)
    text = RE_12M.sub(rep_12m, text)

    def rep_reval(m):
        if m.group(2) != vp:
            stats["revalorizacion"] += 1
        return m.group(1) + vp + m.group(3)
    text = RE_REVAL.sub(rep_reval, text)

    return text


def main():
    data = load_data()
    frozen = set(json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"])
    print(f"DATA[]: {len(data)} municipios · {len(frozen)} ficheros congelados")

    touched, blocked = 0, []
    for path in sorted(glob.glob(os.path.join(SITE, "rentabilidad-*.html"))):
        base = os.path.basename(path)
        slug = base[len("rentabilidad-"):-len(".html")]
        c = data.get(slug)
        if not c:
            continue
        original = open(path, encoding="utf-8", errors="ignore").read()
        antes = dict(stats)
        text = fix_one(original, c)
        if text == original:
            continue
        if base in frozen:
            blocked.append((base, {k: v - antes.get(k, 0) for k, v in stats.items()
                                   if v - antes.get(k, 0) > 0}))
            for k in stats:                       # no contar lo que no se aplica
                stats[k] = antes.get(k, 0)
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        touched += 1

    print(f"\nFichas reescritas: {touched}")
    print(f"  1) 'yield del X%' -> ROI de DATA[]            : {stats['yield']}")
    print(f"  2) info-box 'Mercado en expansión' regenerado : {stats['info_box']}")
    print(f"  3) 'En los últimos 12 meses...' -> vp         : {stats['12_meses']}")
    print(f"  4) 'revalorización anual (+X%)' -> vp         : {stats['revalorizacion']}")
    if blocked:
        print(f"\nBLOQUEADAS POR CONGELACIÓN ({len(blocked)}) — anotar en "
              f"PENDIENTES_DESCONGELACION.md:")
        for b, d in blocked:
            print(f"  {b}: {d}")
    else:
        print("\nNinguna ficha congelada necesitaba cambios.")


if __name__ == "__main__":
    main()
