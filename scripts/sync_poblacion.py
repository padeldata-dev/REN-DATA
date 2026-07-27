#!/usr/bin/env python3
"""Sincroniza el campo `pob` de DATA[] (index.html) y RANK[] (ranking.html).

POR QUÉ
-------
`pob` nunca se pobló con padrón: lleva marcadores redondeados a millar en 176
municipios (59 de ellos un `30000` genérico). Además, `DATA[]` solo tiene el
campo en 448 de 597, mientras que `RANK[]` lo tiene en los 597.

PERO LAS FICHAS TAMPOCO SON FIABLES DEL TODO
--------------------------------------------
Sincronizar a ciegas "desde la ficha" corrompería datos. Comprobado:
  * 34 fichas comparten su población con otra ficha distinta. El valor `50.021`
    aparece en 7 municipios (Adeje, Cangas do Morrazo, Luarca, Mairena del
    Aljarafe, Mislata, Rincón de la Victoria, Utrera) — es un copiar-pegar.
  * Varias fichas traen valores absurdos: Granada 2.287 hab., Torrent 182,
    Mieres 369, Calahorra 680 (su propio texto dice "25.000 habitantes").
  * En algún caso es al revés: Castellón muestra 172.000 redondeado y RANK
    trae 180.379, que es el fino.

Por eso este script NO hace un volcado: clasifica y deja en cuarentena todo lo
que no supera las salvaguardas, para revisión humana.

SALVAGUARDAS (se toma la ficha solo si las pasa todas)
  1. Su valor no está repetido en ninguna otra ficha.
  2. Si RANK NO es un marcador redondo, la ficha debe estar entre 0,5x y 2x.
  3. La ficha no puede ser redonda a millar cuando RANK trae un valor más fino.
Cuando DATA no tiene `pob` y no hay ficha utilizable, se rellena desde RANK.

CONGELACIÓN
-----------
Escribir exige tocar `ranking.html`. Mientras esté en frozen_files.json el
script NO escribe: DATA[] y RANK[] se actualizan a la vez o no se actualizan
(desincronizarlos sería peor que el estado actual).

Uso:
    python scripts/sync_poblacion.py            # informe, no escribe
    python scripts/sync_poblacion.py --apply    # escribe (falla si hay congelación)
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
INDEX = os.path.join(SITE, "index.html")
RANKING = os.path.join(SITE, "ranking.html")


def parse_block(blob):
    out = {}
    for bm in re.finditer(r"\{[^{}]*\}", blob):
        b = bm.group(0)
        s = re.search(r'sl:"([^"]+)"', b)
        p = re.search(r"pob:(\d+)", b)
        if s:
            out[s.group(1)] = int(p.group(1)) if p else None
    return out


def read_sources():
    idx = open(INDEX, encoding="utf-8").read()
    rnk = open(RANKING, encoding="utf-8").read()
    dm = re.search(r"const DATA=\[(.*?)\n\];", idx, re.S)
    i = rnk.find("const RANK=[")
    j = rnk.find("];", i)
    if not dm or i == -1:
        sys.exit("No se pudo localizar DATA[] o RANK[]")
    D = parse_block(dm.group(1))
    R = parse_block(rnk[i + len("const RANK=["):j])
    F = {}
    for f in sorted(glob.glob(os.path.join(SITE, "rentabilidad-*.html"))):
        slug = os.path.basename(f)[len("rentabilidad-"):-len(".html")]
        h = open(f, encoding="utf-8", errors="ignore").read()
        m = re.search(r'<div class="demo-val">([\d.]+)</div>\s*'
                      r'<div class="demo-label">Habitantes', h)
        if m:
            F[slug] = int(m.group(1).replace(".", ""))
    return idx, rnk, D, R, F


def plan(D, R, F):
    """Devuelve (seguros{slug:(origen,valor)}, cuarentena[(slug,d,r,f,motivo)])."""
    dup = {v for v, n in Counter(F.values()).items() if n > 1}
    seguros, cuarentena = {}, []
    for slug in D:
        d, r, f = D[slug], R.get(slug), F.get(slug)
        if f is None:
            if d is None and r is not None:
                seguros[slug] = ("RANK->DATA", r)
            continue
        if d == f and r == f:
            continue                                   # ya coherente
        if f in dup:
            cuarentena.append((slug, d, r, f, "ficha con valor duplicado")); continue
        if r and f % 1000 == 0 and r % 1000 != 0:
            cuarentena.append((slug, d, r, f, "ficha redondeada, RANK más fino")); continue
        if r and r % 1000 != 0 and not (0.5 <= f / r <= 2.0):
            cuarentena.append((slug, d, r, f, "ficha implausible vs RANK no-marcador")); continue
        if r and f / r < 0.5:
            cuarentena.append((slug, d, r, f, "ficha implausible")); continue
        seguros[slug] = ("ficha", f)
    return seguros, cuarentena


def set_pob(blob, slug, valor):
    """Fija pob:<valor> en la entrada de `slug`; lo inserta si no existía."""
    def repl(m):
        b = m.group(0)
        if not re.search(r'sl:"' + re.escape(slug) + r'"', b):
            return b
        if re.search(r"pob:\d+", b):
            return re.sub(r"pob:\d+", f"pob:{valor}", b)
        return re.sub(r'(,sl:"' + re.escape(slug) + r'")', f",pob:{valor}\\1", b)
    return re.sub(r"\{[^{}]*\}", repl, blob)


def filtro_50k(D, R, seguros):
    def val(slug):
        if slug in seguros:
            return seguros[slug][1]
        return D[slug] if D[slug] is not None else R.get(slug)
    antes = sum(1 for s in D if (R.get(s) or 0) >= 50000)
    despues = sum(1 for s in D if (val(s) or 0) >= 50000)
    entran = sorted(s for s in D if (val(s) or 0) >= 50000 and (R.get(s) or 0) < 50000)
    salen = sorted(s for s in D if (val(s) or 0) < 50000 and (R.get(s) or 0) >= 50000)
    return antes, despues, entran, salen


def main():
    apply_ = "--apply" in sys.argv
    idx, rnk, D, R, F = read_sources()
    seguros, cuarentena = plan(D, R, F)

    conflictos = [s for s in D if D[s] is not None and R.get(s) is not None and D[s] != R[s]]
    print(f"DATA[]: {len(D)} entradas ({sum(1 for v in D.values() if v is not None)} con pob) · "
          f"RANK[]: {len(R)} ({sum(1 for v in R.values() if v is not None)} con pob) · "
          f"fichas con población: {len(F)}")
    print(f"conflictos DATA[] vs RANK[] (ambos con valor y distinto): {len(conflictos)}")

    print(f"\nSINCRONIZABLES CON SEGURIDAD: {len(seguros)}")
    for k, n in Counter(o for o, _ in seguros.values()).items():
        print(f"   {n:4d}  origen: {k}")
    print(f"EN CUARENTENA (revisión manual): {len(cuarentena)}")
    for motivo, n in Counter(x[4] for x in cuarentena).most_common():
        print(f"   {n:4d}  {motivo}")

    antes, despues, entran, salen = filtro_50k(D, R, seguros)
    print(f"\nFiltro '>50.000 hab.' de ranking.html: {antes} -> {despues} municipios "
          f"(+{len(entran)} entran, -{len(salen)} salen)")

    frozen = set(json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"])
    bloqueado = "ranking.html" in frozen
    if not apply_:
        print("\n(modo informe: no se ha escrito nada. Usa --apply para aplicar)")
        return
    if bloqueado:
        print("\nNO SE APLICA: ranking.html está CONGELADO en frozen_files.json.")
        print("DATA[] y RANK[] se actualizan a la vez o no se actualizan. "
              "Descongela primero y vuelve a ejecutar.")
        sys.exit(1)

    dm = re.search(r"(const DATA=\[)(.*?)(\n\];)", idx, re.S)
    new_data = dm.group(2)
    i = rnk.find("const RANK=["); j = rnk.find("];", i)
    head, body, tail = rnk[:i + len("const RANK=[")], rnk[i + len("const RANK=["):j], rnk[j:]
    new_rank = body
    for slug, (_, v) in seguros.items():
        new_data = set_pob(new_data, slug, v)
        new_rank = set_pob(new_rank, slug, v)
    open(INDEX, "w", encoding="utf-8", newline="\n").write(
        idx[:dm.start(2)] + new_data + idx[dm.end(2):])
    open(RANKING, "w", encoding="utf-8", newline="\n").write(head + new_rank + tail)
    print(f"\nAplicado a {len(seguros)} municipios en index.html Y ranking.html.")


if __name__ == "__main__":
    main()
