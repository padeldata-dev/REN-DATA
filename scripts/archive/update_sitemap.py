#!/usr/bin/env python3
"""Inserta las 7 nuevas URLs en sitemap.xml. Idempotente."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
SITEMAP = BETA / "sitemap.xml"

SLUGS = [
    "santa-coloma-de-gramenet",
    "melilla",
    "valdemoro",
    "ceuta",
    "sant-vicent-del-raspeig",
    "colmenar-viejo",
    "vila-real",
]
LASTMOD = "2026-05-17"


def main():
    text = SITEMAP.read_text(encoding="utf-8")
    additions = []
    for slug in SLUGS:
        if f"rentabilidad-{slug}.html" in text:
            print(f"[skip] {slug} ya en sitemap")
            continue
        entry = (
            f"  <url>\n"
            f"    <loc>https://rendata.es/rentabilidad-{slug}.html</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.7</priority>\n"
            f"  </url>\n"
        )
        additions.append(entry)
        print(f"[ok] {slug} insertada")

    if not additions:
        return

    # Insertar antes de </urlset>
    closing = "</urlset>"
    new_text = text.replace(closing, "".join(additions) + closing)
    SITEMAP.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    main()
