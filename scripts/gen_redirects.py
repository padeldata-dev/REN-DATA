#!/usr/bin/env python3
"""
Genera rendata_beta/_redirects: un 301 `.html` -> URL limpia por cada página.

Contexto (2026-08-01): Cloudflare Workers Assets sirve cada fichero `x.html`
tanto en `/x.html` como en `/x`, y para la variante `.html` emite un **307**
(temporal). Google trata el 307 como "la URL original sigue siendo válida" y
acaba indexando LAS DOS, partiendo señales entre ellas. Search Console detectó
16 pares con impresiones, pero el problema afectaba a las 843 páginas del sitio.

La solución es un 301 explícito por página. Cloudflare no acepta un comodín
fiable del tipo `/*.html`, así que hay que enumerarlas: este script las saca del
propio árbol de ficheros, de modo que añadir una página nueva solo exige volver
a ejecutarlo. qa_check[15] falla si alguna se queda sin regla.

ORDEN: Cloudflare admite 2.000 reglas ESTÁTICAS pero solo 100 DINÁMICAS (las que
llevan `*` o `:placeholder`), y **exige que las estáticas vayan primero**. Con el
bloque generado detrás de los 4 alias dinámicos, el deploy se rechazó con
"Maximum number of dynamic _redirects rules limit of 100 exceeded" en la regla
101: todo lo que sigue a una dinámica cuenta como dinámica. Por eso el script
escribe el fichero entero — cabecera, bloque estático y cola dinámica — en vez de
parchear un trozo: así el orden no puede volver a romperse a mano.

Uso:
    python scripts/gen_redirects.py           # reescribe _redirects
    python scripts/gen_redirects.py --check   # solo comprueba, exit 1 si difiere
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("RENDATA_SITE") or os.path.join(ROOT, "rendata_beta")
REDIRECTS = os.path.join(SITE, "_redirects")

# 404.html se queda fuera: lo sirve Cloudflare como página de error y ya lleva
# <meta name="robots" content="noindex">, así que no compite en el índice.
EXCLUDE = {"404.html"}

HEADER = """\
# GENERADO POR scripts/gen_redirects.py — NO EDITAR A MANO.
# Para cambiar la cabecera o los alias, edita las constantes del script.
#
# Cloudflare Workers Assets sirve cada `x.html` en DOS rutas, `/x.html` y `/x`,
# y a la variante `.html` le da un 307 TEMPORAL: Google indexa las dos y parte
# el posicionamiento entre ellas. Estos 301 lo hacen permanente.
#
# Las reglas ESTATICAS (sin `*` ni `:placeholder`) van PRIMERO: Cloudflare solo
# admite 100 dinamicas y cuenta como dinamica todo lo que venga detras de una.
"""

# Reglas dinamicas: SIEMPRE al final del fichero (ver nota de arriba).
TAIL = """\
# === Reglas dinamicas (max. 100, obligatoriamente al final) ===
# Alias de ruta -> URL canonica. Antes eran rewrites 200 y servian la MISMA
# ficha en una segunda ruta, que es justo la duplicacion que evitamos aqui.
/rentabilidad/* /rentabilidad-:splat 301
/ccaa/* /ccaa-:splat 301

# Fuerza https + dominio canonico (sin www). En la practica no llegan a
# ejecutarse: el edge de Cloudflare ("Always Use HTTPS") resuelve el salto antes
# de que la peticion alcance al Worker. Se quedan como red de seguridad.
# El caso https://www.rendata.es -> https://rendata.es NO se puede poner aqui
# (Cloudflare rechaza origenes https:// absolutos); esta resuelto con una
# Redirect Rule de zona en el panel (www -> apex).
http://rendata.es/* https://rendata.es/:splat 301
http://www.rendata.es/* https://rendata.es/:splat 301
"""


def rel(p):
    return os.path.relpath(p, SITE).replace("\\", "/")


def clean_url(page):
    """URL canónica que Workers Assets sirve para el fichero `page`."""
    if page == "index.html":
        return "/"
    if page.endswith("/index.html"):
        return "/" + page[: -len("/index.html")] + "/"
    return "/" + page[: -len(".html")]


def rules():
    """[(origen, destino)] para cada página, .html -> limpia."""
    pages = sorted(
        rel(p) for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
    )
    return [(f"/{p}", clean_url(p)) for p in pages if p not in EXCLUDE]


def render():
    rs = rules()
    out = [HEADER, f"# === {len(rs)} reglas estaticas: .html -> URL limpia ==="]
    out += [f"{src} {dst} 301" for src, dst in rs]
    out += ["", TAIL]
    return "\n".join(out)


def main():
    out = render()
    n = len(rules())
    current = (open(REDIRECTS, encoding="utf-8", newline="").read()
               if os.path.exists(REDIRECTS) else "")
    if "--check" in sys.argv:
        if out != current:
            print("gen_redirects: _redirects DESACTUALIZADO "
                  f"({n} paginas). Ejecuta: python scripts/gen_redirects.py")
            return 1
        print(f"gen_redirects: _redirects al dia ({n} reglas 301 .html -> limpia)")
        return 0
    with open(REDIRECTS, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"gen_redirects: {n} reglas 301 .html -> limpia escritas en {rel(REDIRECTS)}")
    if n > 1900:                       # limite de Cloudflare: 2.000 estaticas
        print(f"AVISO: {n} reglas estaticas, cerca del limite de 2.000 de Cloudflare")
    return 0


if __name__ == "__main__":
    sys.exit(main())
