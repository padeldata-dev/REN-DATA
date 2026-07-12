#!/usr/bin/env python3
"""Aplica background-image inline al <section class="hero"> de cada ccaa-*.html."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "rendata_beta"

# Mapeo CCAA -> ruta imagen
MAPPING = {
    "ccaa-andalucia.html": "/img/sevilla-hero.jpg",
    "ccaa-aragon.html": "/img/zaragoza-hero.jpg",
    "ccaa-asturias.html": "/img/asturias-hero.jpg",
    "ccaa-baleares.html": "/img/palma-hero.jpg",
    "ccaa-canarias.html": "/img/canarias-hero.jpg",
    "ccaa-cantabria.html": "/img/cantabria-hero.jpg",
    "ccaa-castilla-la-mancha.html": "/img/toledo-hero.jpg",
    "ccaa-castilla-y-leon.html": "/img/salamanca-hero.jpg",
    "ccaa-cataluna.html": "/img/barcelona-hero.jpg",
    "ccaa-comunitat-valenciana.html": "/img/valencia-hero.jpg",
    "ccaa-extremadura.html": "/img/caceres-hero.jpg",
    "ccaa-galicia.html": "/img/santiago-de-compostela-hero.jpg",
    "ccaa-la-rioja.html": "/img/la-rioja-hero.jpg",
    "ccaa-madrid.html": "/img/madrid.webp",
    "ccaa-murcia.html": "/img/murcia-hero.jpg",
    "ccaa-navarra.html": "/img/pamplona-hero.jpg",
    "ccaa-pais-vasco.html": "/img/bilbao-hero.jpg",
}

# Reemplaza la apertura del hero. Patron tolerante: opcionalmente con style ya inyectado.
HERO_OPEN_RE = re.compile(r'<section\s+class="hero"(\s+style="[^"]*")?\s*>', re.IGNORECASE)


def process(fname: str, img: str) -> bool:
    path = ROOT / fname
    text = path.read_text(encoding="utf-8")
    new_open = f'<section class="hero" style="background-image:url(\'{img}\')">'
    new_text, n = HERO_OPEN_RE.subn(new_open, text, count=1)
    if n == 0:
        print(f"WARN: hero open not found in {fname}", file=sys.stderr)
        return False
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    changed = 0
    for fname, img in MAPPING.items():
        if process(fname, img):
            changed += 1
            print(f"OK {fname} -> {img}")
        else:
            print(f"-- {fname} (no change)")
    print(f"\n{changed}/{len(MAPPING)} files updated")


if __name__ == "__main__":
    main()
