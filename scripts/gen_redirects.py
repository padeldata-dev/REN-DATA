#!/usr/bin/env python3
"""
Regenera el bloque de 301 `.html` -> URL limpia de rendata_beta/_redirects.

Contexto (2026-08-01): Cloudflare Workers Assets sirve cada fichero `x.html`
tanto en `/x.html` como en `/x`, y para la variante `.html` emite un **307**
(temporal). Google trata el 307 como "la URL original sigue siendo válida" y
acaba indexando LAS DOS, partiendo señales entre ellas. Search Console detectó
16 pares con impresiones, pero el problema afecta a las 843 páginas del sitio.

La solución es un 301 explícito por página. Como Cloudflare no acepta un
comodín fiable del tipo `/*.html`, hay que enumerarlas: este script lo hace
desde el propio árbol de ficheros, así que añadir una página nueva solo exige
volver a ejecutarlo. qa_check[15] falla si alguna página se queda sin regla.

Las secciones escritas a mano del fichero (canonicalización de dominio, alias
/rentabilidad/* y /ccaa/*) se conservan intactas: solo se reescribe lo que hay
entre los marcadores BEGIN/END.

Uso:
    python scripts/gen_redirects.py           # reescribe el bloque
    python scripts/gen_redirects.py --check   # solo comprueba, exit 1 si difiere
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("RENDATA_SITE") or os.path.join(ROOT, "rendata_beta")
REDIRECTS = os.path.join(SITE, "_redirects")

BEGIN = "# === BEGIN 301 .html -> URL limpia (generado por scripts/gen_redirects.py) ==="
END = "# === END 301 .html -> URL limpia ==="

# 404.html se queda fuera: lo sirve Cloudflare como página de error y ya lleva
# <meta name="robots" content="noindex">, así que no compite en el índice.
EXCLUDE = {"404.html"}


def rel(p):
    return os.path.relpath(p, SITE).replace("\\", "/")


def clean_url(page):
    """URL canónica que Workers Assets sirve para el fichero `page`."""
    if page == "index.html":
        return "/"
    if page.endswith("/index.html"):
        return "/" + page[: -len("/index.html")] + "/"
    return "/" + page[: -len(".html")]


def pages():
    return sorted(
        rel(p) for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)
    )


def rules():
    """[(origen, destino)] para cada página, .html -> limpia."""
    return [(f"/{p}", clean_url(p)) for p in pages() if p not in EXCLUDE]


def block():
    rs = rules()
    lines = [
        BEGIN,
        f"# {len(rs)} paginas. NO EDITAR A MANO: `python scripts/gen_redirects.py`.",
    ]
    lines += [f"{src} {dst} 301" for src, dst in rs]
    lines.append(END)
    return "\n".join(lines)


def render(current):
    """Devuelve el _redirects completo con el bloque generado al día."""
    new = block()
    if BEGIN in current and END in current:
        head, rest = current.split(BEGIN, 1)
        _, tail = rest.split(END, 1)
        return head + new + tail
    # primera vez: el bloque va al final, después de las reglas escritas a mano
    return current.rstrip("\n") + "\n\n" + new + "\n"


def main():
    current = open(REDIRECTS, encoding="utf-8", newline="").read()
    out = render(current)
    n = len(rules())
    if "--check" in sys.argv:
        if out != current:
            print(f"gen_redirects: _redirects DESACTUALIZADO ({n} paginas). "
                  f"Ejecuta: python scripts/gen_redirects.py")
            return 1
        print(f"gen_redirects: _redirects al dia ({n} reglas 301 .html -> limpia)")
        return 0
    with open(REDIRECTS, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print(f"gen_redirects: {n} reglas 301 .html -> limpia escritas en {rel(REDIRECTS)}")
    # Cloudflare: 2.000 reglas estáticas y 100 dinámicas como máximo.
    if n > 1900:
        print(f"AVISO: {n} reglas estaticas, cerca del limite de 2.000 de Cloudflare")
    return 0


if __name__ == "__main__":
    sys.exit(main())
