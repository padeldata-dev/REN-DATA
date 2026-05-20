"""Block 5: SEO cleanup, sitemap regeneration, URL validation.

1. Replace residual "329 ciudades" → "587 ciudades" (case-insensitive).
2. Regenerate sitemap.xml with all current HTML pages.
3. Verify internal links don't point to missing files.
"""
import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")
SITE = "https://rendata.es"

# --- 1. Search for "329 ciudades" ---
print("[1] Searching for '329 ciudades'...")
hits = []
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    if "329 ciudades" in txt or "329 Ciudades" in txt or "329 CIUDADES" in txt:
        hits.append(f.name)
        new = re.sub(r"\b329\s+ciudades\b", "587 ciudades", txt, flags=re.IGNORECASE)
        if new != txt:
            f.write_text(new, encoding="utf-8")
print(f"   Replaced in {len(hits)} files")

# --- 2. Build sitemap ---
print("[2] Building sitemap.xml...")

# Priority + changefreq scheme
PRIORITIES = {
    "/": ("daily", "1.0"),
    "ranking.html": ("daily", "0.95"),
    "analisis.html": ("daily", "0.9"),
    "comparador.html": ("weekly", "0.85"),
    "simulador-comprar-vs-alquilar.html": ("monthly", "0.85"),
    "calculadora-hipoteca.html": ("monthly", "0.85"),
    "metodologia.html": ("monthly", "0.7"),
    "glosario.html": ("monthly", "0.7"),
    "guia-inversor.html": ("monthly", "0.75"),
    "sobre.html": ("monthly", "0.6"),
    "404.html": (None, None),  # excluded
}

def prio(name):
    if name in PRIORITIES: return PRIORITIES[name]
    if name.startswith("rentabilidad-"): return ("weekly", "0.7")
    if name.startswith("ccaa-"): return ("weekly", "0.8")
    if name.startswith("mercado-inmobiliario-"): return ("monthly", "0.75")
    if name.endswith("-2026.html"): return ("monthly", "0.7")
    return ("monthly", "0.6")

today = datetime.now().strftime("%Y-%m-%d")

urls = []
# Homepage
urls.append(("/", *PRIORITIES["/"]))
# Other HTML pages
htmls = sorted(p.name for p in ROOT.glob("*.html") if p.name != "404.html" and p.name != "index.html")
for name in htmls:
    cf, pr = prio(name)
    if cf is None: continue
    urls.append((f"/{name}", cf, pr))

xml = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, cf, pr in urls:
    xml.append("  <url>")
    xml.append(f"    <loc>{SITE}{path}</loc>")
    xml.append(f"    <lastmod>{today}</lastmod>")
    xml.append(f"    <changefreq>{cf}</changefreq>")
    xml.append(f"    <priority>{pr}</priority>")
    xml.append("  </url>")
xml.append("</urlset>\n")
(ROOT / "sitemap.xml").write_text("\n".join(xml), encoding="utf-8")
print(f"   Wrote sitemap with {len(urls)} URLs")

# --- 3. Verify internal links ---
print("[3] Verifying internal links...")
RE_HREF = re.compile(r'href="(/[a-zA-Z0-9_\-./]+\.html)"')
RE_HREF_REL = re.compile(r'href="([a-zA-Z0-9_\-]+\.html)"')

existing_pages = {p.name for p in ROOT.glob("*.html")}
broken = Counter()
checked_files = 0

for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    for m in RE_HREF.finditer(txt):
        path = m.group(1).lstrip("/")
        if "#" in path: path = path.split("#", 1)[0]
        if path and path not in existing_pages:
            broken[path] += 1
    for m in RE_HREF_REL.finditer(txt):
        path = m.group(1)
        if "#" in path: path = path.split("#", 1)[0]
        if path and path not in existing_pages:
            broken[path] += 1
    checked_files += 1

if broken:
    print(f"   [WARN] Found {len(broken)} broken HTML link targets:")
    for path, count in broken.most_common(20):
        print(f"     {path}  (referenced {count} times)")
else:
    print(f"   [OK] All HTML links resolve ({checked_files} files scanned)")

print("\nBLOCK 5 done.")
