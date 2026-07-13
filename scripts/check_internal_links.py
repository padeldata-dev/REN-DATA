#!/usr/bin/env python3
"""Verify all rentabilidad-*.html and article links referenced in the sitemap exist."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
SITEMAP = BETA / "sitemap.xml"

xml = SITEMAP.read_text(encoding="utf-8")
urls = re.findall(r'<loc>https://rendata\.es(/[^<]*)</loc>', xml)

missing = []
for u in urls:
    if u == "/" or u.endswith("/"):
        # Raíz o índice de subdirectorio (ej. /en/) -> {dir}/index.html
        target = BETA / u.lstrip("/") / "index.html" if u != "/" else BETA / "index.html"
    else:
        # El sitemap usa URLs limpias (sin .html); Cloudflare Workers Assets
        # las resuelve contra el fichero real, que sí lleva la extensión.
        target = BETA / (u.lstrip("/") + ".html")
    if not target.is_file():
        missing.append(u)

print(f"Sitemap URLs: {len(urls)}")
print(f"Missing: {len(missing)}")
for m in missing[:20]:
    print(f"  {m}")
