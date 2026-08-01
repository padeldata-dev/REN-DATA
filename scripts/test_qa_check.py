#!/usr/bin/env python3
"""Tests NEGATIVOS del guardián: inyecta cada bug conocido y exige que falle.

Un check que no falla cuando debe es peor que no tenerlo: da luz verde falsa.
Hasta 2026-07-29 `qa_check.py` no tenía forma de demostrar que sus checks
saltaban, y de hecho [8] llevaba meses en verde mientras 484 fichas servían un
precio distinto del de DATA[] — el hueco simplemente no estaba vigilado.

Cómo funciona
-------------
1. Copia los .html, el sitemap y _redirects a un directorio temporal (los
   binarios no hacen falta: el guardián solo lee esos ficheros y frozen_files.json).
2. Por cada caso: rompe UNA cosa en UNA ficha, ejecuta `qa_check.py` contra la
   copia vía la variable de entorno RENDATA_SITE, y comprueba que
   (a) sale con código 1 y (b) el mensaje cita el check esperado.
3. Restaura el fichero y pasa al siguiente caso.

Incluye un control POSITIVO: la copia intacta debe salir en verde. Sin él, un
guardián que fallara siempre pasaría todos los tests negativos.

Uso:  python scripts/test_qa_check.py
Sale 0 si todos los casos se comportan como se espera; 1 si alguno no.
"""
import os
import shutil
import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "rendata_beta")
QA = os.path.join(ROOT, "scripts", "qa_check.py")
FICHA = "rentabilidad-lleida.html"      # no congelada, con todos los bloques

# (nombre, check esperado, texto a buscar, texto con el que sustituirlo)
CASOS = [
    ("[13] hero: precio distinto de DATA[]", "[13]",
     '<div class="sl">Precio m²</div><div class="sv" style="font-size:1.55rem">1.300€',
     '<div class="sl">Precio m²</div><div class="sv" style="font-size:1.55rem">1.500€'),

    ("[13] hero: % anual del alquiler distinto de DATA[]", "[13]",
     '<span class="badge badge-up">↑ 16,1% anual</span>',
     '<span class="badge badge-up">↑ 9,9% anual</span>'),

    ("[13] barra sticky: alquiler distinto de DATA[]", "[13]",
     '<span class="sb-label">Alquiler</span><span class="sb-val">650€/mes',
     '<span class="sb-label">Alquiler</span><span class="sb-val">700€/mes'),

    ("[13] prosa: alquiler distinto de DATA[]", "[13]",
     "alcanzando los 650€ mensuales",
     "alcanzando los 700€ mensuales"),

    ("[14] serie histórica que no acaba en el precio de DATA[]", "[14]",
     '<span class="evo-v cur">1.300€</span>',
     '<span class="evo-v cur">1.500€</span>'),

    ("[14] serie histórica que BAJA con vp positivo", "[14]",
     '<div class="evo-col"><span class="evo-v">1.240€</span>',
     '<div class="evo-col"><span class="evo-v">2.400€</span>'),

    ("[14] tipo de ITP que no es el de la CCAA", "[14]",
     '<div class="itp-val">10<span class="itp-pct">%</span></div>',
     '<div class="itp-val">6<span class="itp-pct">%</span></div>'),

    ("[14] importe de ITP que no cuadra con su tipo", "[14]",
     "pagarás <strong>10.140€ de ITP</strong>",
     "pagarás <strong>5.510€ de ITP</strong>"),

    ("[9] badge 'Media España' con un valor inventado", "[9]",
     '<span class="badge badge-n">Media España 5,8%</span>',
     '<span class="badge badge-n">Media España 6,5%</span>'),

    ("[8] ROI del hero distinto de DATA[]", "[8]",
     '<div class="sl">Rentabilidad bruta estimada</div><div class="sv">6,0%',
     '<div class="sl">Rentabilidad bruta estimada</div><div class="sv">6,4%'),

    ("[15] canonical apuntando a la variante .html", "[15]",
     '<link rel="canonical" href="https://rendata.es/rentabilidad-lleida"',
     '<link rel="canonical" href="https://rendata.es/rentabilidad-lleida.html"'),

    ("[12] prosa: 'yield del X%' distinto del ROI", "[12]",
     "En los últimos 12 meses el precio ha subido un 7,5%",
     "En los últimos 12 meses el precio ha subido un 8,9%"),

    ("[1] enlace interno roto", "[1]",
     '<a href="ranking.html"',
     '<a href="ranking-que-no-existe.html"'),
]

# Caso extra sobre otra ficha: el ed-stat "subida alquiler anual" solo existe en las
# 6 fichas de plantilla propia, así que no se puede inyectar en Lleida.
CASOS_ALICANTE = [
    ("[13] ed-stat 'subida alquiler anual' distinto de DATA[]", "[13]",
     '<div class="ed-stat-val">+9,0%</div><div class="ed-stat-lbl">subida alquiler anual</div>',
     '<div class="ed-stat-val">+12,0%</div><div class="ed-stat-lbl">subida alquiler anual</div>'),
]

# Casos que no viven en una ficha: (nombre, check, fichero, texto viejo, nuevo).
# [15] vigila la duplicación .html/limpia, que se rompe desde _redirects y desde
# el sitemap, no desde el HTML de una ciudad.
CASOS_FICHERO = [
    ("[15] pagina servida en /x.html y /x sin su 301", "[15]", "_redirects",
     "/rentabilidad-lleida.html /rentabilidad-lleida 301\n", ""),

    ("[15] 301 que apunta a otra pagina", "[15]", "_redirects",
     "/rentabilidad-lleida.html /rentabilidad-lleida 301",
     "/rentabilidad-lleida.html /rentabilidad-girona 301"),

    ("[15] rewrite 200 que sirve la ficha en una segunda ruta", "[15]", "_redirects",
     "/ccaa/* /ccaa-:splat 301",
     "/ccaa/* /ccaa-:splat.html 200"),

    ("[15] sitemap que lista la variante .html", "[15]", "sitemap.xml",
     "<loc>https://rendata.es/rentabilidad-lleida</loc>",
     "<loc>https://rendata.es/rentabilidad-lleida.html</loc>"),
]


def copiar_sitio(dst):
    for base, _, files in os.walk(SITE):
        for f in files:
            if not (f.endswith(".html") or f in ("sitemap.xml", "_redirects")):
                continue
            src = os.path.join(base, f)
            out = os.path.join(dst, os.path.relpath(src, SITE))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy2(src, out)


def corre(site):
    env = dict(os.environ, RENDATA_SITE=site, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, QA], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main():
    tmp = tempfile.mkdtemp(prefix="rendata_qa_")
    fallos = []
    try:
        copiar_sitio(tmp)
        # --- control POSITIVO ---
        code, out = corre(tmp)
        if code == 0:
            print("  ok   CONTROL POSITIVO: la copia intacta pasa en verde")
        else:
            fallos.append("CONTROL POSITIVO: la copia intacta ya falla -> "
                          + " / ".join(l for l in out.splitlines() if l.startswith("  [X]"))[:300])
            print("  FALLO CONTROL POSITIVO — los casos negativos no son concluyentes")

        # --- casos negativos ---
        todos = [(n, c, FICHA, v, x) for n, c, v, x in CASOS]
        todos += [(n, c, "rentabilidad-alicante.html", v, x) for n, c, v, x in CASOS_ALICANTE]
        todos += list(CASOS_FICHERO)
        for nombre, check, fichero, viejo, nuevo in todos:
            ruta_f = os.path.join(tmp, fichero)
            base = open(ruta_f, encoding="utf-8", newline="").read()
            if viejo not in base:
                fallos.append(f"{nombre}: el ancla no existe en {fichero} (test obsoleto)")
                print(f"  FALLO {nombre} — ancla no encontrada")
                continue
            with open(ruta_f, "w", encoding="utf-8", newline="") as fh:
                fh.write(base.replace(viejo, nuevo, 1))
            code, out = corre(tmp)
            citado = any(l.lstrip().startswith("[X] " + check) for l in out.splitlines())
            if code == 1 and citado:
                print(f"  ok   {nombre}")
            elif code == 1:
                fallos.append(f"{nombre}: falló, pero no por {check}")
                print(f"  FALLO {nombre} — falla, pero no lo reporta {check}")
            else:
                fallos.append(f"{nombre}: NO detectado (exit 0)")
                print(f"  FALLO {nombre} — el guardián NO lo detecta")
            with open(ruta_f, "w", encoding="utf-8", newline="") as fh:
                fh.write(base)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("-" * 60)
    if fallos:
        print(f"TESTS FAILED — {len(fallos)} caso(s):")
        for f in fallos:
            print("  [X]", f)
        return 1
    n = len(CASOS) + len(CASOS_ALICANTE) + len(CASOS_FICHERO)
    print(f"TESTS OK — {n} bugs inyectados, {n} detectados por el check correcto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
