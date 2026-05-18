#!/usr/bin/env python3
"""Update stale numbers in the 13 existing articles to reflect 587 cities total."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"

EXISTING_ARTICLES = [
    "top10-ciudades-rentables-2026.html",
    "ciudades-baratas-comprar-piso-espana-2026.html",
    "ciudades-alquiler-caro-espana-2026.html",
    "invertir-vivienda-costa-espana-2026.html",
    "rentabilidad-madrid-vs-barcelona-2026.html",
    "mejores-ccaa-rentabilidad-inmobiliaria-2026.html",
    "invertir-vivienda-canarias-2026.html",
    "precio-vivienda-espana-evolucion-2026.html",
    "ciudades-interior-vs-costa-rentabilidad-2026.html",
    "castilla-leon-rentabilidad-inmobiliaria-2026.html",
    "municipios-pequenos-alta-rentabilidad-2026.html",
    "ciudades-universitarias-rentabilidad-alquiler-2026.html",
    "mercado-inmobiliario-pais-vasco-2026.html",
    "analisis.html",  # also has stale "329"
    "guia-inversor.html",
    "ranking.html",
]


def main():
    fixed = 0
    json_errs_total = 0
    for fn in EXISTING_ARTICLES:
        p = BETA / fn
        if not p.is_file():
            print(f"  [skip] {fn} missing")
            continue
        html = p.read_text(encoding="utf-8")
        original = html

        # Replace "329 ciudades" / "329 plazas" with "587"
        html = re.sub(r"\b329\s+ciudades\b", "587 ciudades", html)
        html = re.sub(r"\b329\s+plazas\b", "587 plazas", html)
        html = re.sub(r"\b329\s+municipios\b", "587 municipios", html)
        # Replace "más de 300" with "más de 580"
        html = re.sub(r"más de 300 ciudades", "más de 580 ciudades", html)
        # Replace footer "329 ciudades de España"
        html = html.replace("329 ciudades de España", "587 ciudades de España")
        # Replace "datos reales de 329" with "datos reales de 587"
        html = html.replace("datos reales de 329", "datos reales de 587")
        html = html.replace("ranking completo de 329 plazas", "ranking completo de 587 plazas")
        html = html.replace("Ranking completo de 329 plazas", "Ranking completo de 587 plazas")

        # Validate JSON-LD
        errs = 0
        for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.DOTALL):
            try:
                json.loads(blk)
            except json.JSONDecodeError:
                errs += 1
        json_errs_total += errs

        if html != original:
            p.write_text(html, encoding="utf-8")
            print(f"  [updated] {fn} (JSON-LD errs: {errs})")
            fixed += 1
        else:
            print(f"  [no change] {fn} (JSON-LD errs: {errs})")

    print(f"\nUpdated: {fixed} / {len(EXISTING_ARTICLES)}")
    print(f"JSON-LD errors total: {json_errs_total}")


if __name__ == "__main__":
    main()
