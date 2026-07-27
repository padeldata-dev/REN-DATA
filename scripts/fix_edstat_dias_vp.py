#!/usr/bin/env python3
"""Mass-fix idempotente: liga a DATA[] el bloque ed-stat de días de venta y
subida de precio anual.

Mismo patrón de bug que el de d5f27ec5 (badge/hero): el editorial destacado
("ed-stat") arrastra valores de un import anterior mientras el cuerpo de la
ficha ya usa los de DATA[]. En Marbella convivían "16 días" en el ed-stat y
"14 días" en otros tres puntos de la misma página; DATA[] dice d:14.

  - ed-stat "días media venta"    -> campo d  de DATA[]
  - ed-stat "subida precio anual" -> campo vp de DATA[]

RESPETA LA CONGELACIÓN: los ficheros listados en frozen_files.json no se
tocan; se reportan para anotarlos en PENDIENTES_DESCONGELACION.md.

Uso:  python scripts/fix_edstat_dias_vp.py
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

DIAS = re.compile(
    r'(<div class="ed-stat-val">)(\d+)(</div><div class="ed-stat-lbl">días media venta</div>)'
)
VP = re.compile(
    r'(<div class="ed-stat-val">\+)([\d,]+)(%</div><div class="ed-stat-lbl">subida precio anual</div>)'
)


def load_data():
    idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
    mm = re.search(r"const DATA=\[(.*?)\n\];", idx, re.S)
    if not mm:
        sys.exit("No se encontró DATA[] en index.html")
    out = {}
    for bm in re.finditer(r"\{[^{}]*\}", mm.group(1)):
        b = bm.group(0)
        sl = re.search(r'sl:"([^"]+)"', b)
        d = re.search(r"d:(\d+)", b)
        vp = re.search(r"vp:([-\d.]+)", b)
        if sl and d and vp:
            out[sl.group(1)] = {"d": int(d.group(1)), "vp": float(vp.group(1))}
    return out


def fmt_vp(v):
    """+7,0%  ->  el marcado usa coma decimal; los enteros se escriben sin decimal
    solo si así estaban. Se normaliza a un decimal, que es lo mayoritario."""
    return f"{v:.1f}".replace(".", ",")


def main():
    data = load_data()
    frozen = set(json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"])
    print(f"DATA[]: {len(data)} municipios · {len(frozen)} ficheros congelados")

    touched, blocked = 0, []
    for path in sorted(glob.glob(os.path.join(SITE, "rentabilidad-*.html"))):
        base = os.path.basename(path)
        slug = base[len("rentabilidad-"):-len(".html")]
        city = data.get(slug)
        if not city:
            continue
        original = open(path, encoding="utf-8", errors="ignore").read()

        pend = []

        def rep_dias(m):
            if m.group(2) != str(city["d"]):
                pend.append(f"días {m.group(2)}->{city['d']}")
            return m.group(1) + str(city["d"]) + m.group(3)

        def rep_vp(m):
            want = fmt_vp(city["vp"])
            if m.group(2) != want:
                pend.append(f"vp +{m.group(2)}%->+{want}%")
            return m.group(1) + want + m.group(3)

        text = VP.sub(rep_vp, DIAS.sub(rep_dias, original))

        if text == original:
            continue
        if base in frozen:
            blocked.append((base, pend))
            continue
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        touched += 1
        for p in pend:
            stats[p.split()[0]] += 1

    print(f"\nFichas reescritas: {touched}")
    print(f"  días media venta corregidos : {stats['días']}")
    print(f"  subida precio anual corregida: {stats['vp']}")
    if blocked:
        print(f"\nBLOQUEADAS POR CONGELACIÓN ({len(blocked)}) — anotar en "
              f"PENDIENTES_DESCONGELACION.md:")
        for b, pend in blocked:
            print(f"  {b}: {', '.join(pend)}")
    else:
        print("\nNinguna ficha congelada necesitaba cambios.")


if __name__ == "__main__":
    main()
