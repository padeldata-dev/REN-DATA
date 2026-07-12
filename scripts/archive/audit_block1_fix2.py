"""Fix #2: restore broken meta descriptions from og:description for 8 pages
with apostrophes in their city names. The previous fix script used a regex
that included \\' as a quote delimiter, so apostrophes in content broke parsing.
"""
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

# Match meta name="description" content="..."  with ONLY double quotes
RE_DESC = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"')
# Match og:description (same approach)
RE_OG_DESC = re.compile(r'<meta\s+property="og:description"\s+content="([^"]*)"')

TARGETS = [
    "rentabilidad-castello-d-empuries.html",
    "rentabilidad-l-alfas-del-pi.html",
    "rentabilidad-l-eliana.html",
    "rentabilidad-l-escala.html",
    "rentabilidad-l-hospitalet-de-llobregat.html",
    "rentabilidad-la-vall-d-uixo.html",
    "rentabilidad-llica-d-amunt.html",
    "rentabilidad-sant-joan-d-alacant.html",
]

fixed = 0
for name in TARGETS:
    p = ROOT / name
    if not p.exists(): continue
    txt = p.read_text(encoding="utf-8")
    og = RE_OG_DESC.search(txt)
    if not og: continue
    good_desc = og.group(1)
    if len(good_desc) > 160:
        # Shorten at sentence boundary
        cut = good_desc[:158]
        for sep in [". ", "; ", ", "]:
            idx = cut.rfind(sep)
            if idx > 80:
                cut = cut[:idx]
                break
        good_desc = cut.rstrip(" .;,") + "."
    new = RE_DESC.sub(f'<meta name="description" content="{good_desc}"', txt, count=1)
    if new != txt:
        p.write_text(new, encoding="utf-8")
        fixed += 1
        print(f"   Fixed: {name}  -> {good_desc[:80]}...")

print(f"\nFixed {fixed} pages.")
