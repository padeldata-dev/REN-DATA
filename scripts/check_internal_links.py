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
    if u == "/":
        target = BETA / "index.html"
    else:
        target = BETA / u.lstrip("/")
    if not target.is_file():
        missing.append(u)

print(f"Sitemap URLs: {len(urls)}")
print(f"Missing: {len(missing)}")
for m in missing[:20]:
    print(f"  {m}")
