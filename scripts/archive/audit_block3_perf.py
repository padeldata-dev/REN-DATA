"""Block 3: performance audit + fixes.

Targets:
 1. _headers: cache rules for /img/*, /css/*, /js/* static assets
 2. Hero images in city pages: loading="eager" + fetchpriority="high"
 3. Other images: loading="lazy" if missing
 4. Verify Analytics/AdSense have async (already verified — both have it)
 5. Defer non-critical scripts in <head>

NOT auto-removing unused CSS — risky without DOM-level analysis tool. Reported.
"""
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

# ---------- 1. _headers ----------
print("[1] Updating _headers with static-asset cache rules...")
headers_file = ROOT / "_headers"
headers_content = headers_file.read_text(encoding="utf-8") if headers_file.exists() else ""

STATIC_RULES = """
/img/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=2592000

/js/*
  Cache-Control: public, max-age=2592000

/favicon.ico
  Cache-Control: public, max-age=2592000

/favicon.svg
  Cache-Control: public, max-age=2592000

/apple-touch-icon.png
  Cache-Control: public, max-age=2592000
"""

if "/img/*" not in headers_content:
    headers_content = headers_content.rstrip() + "\n" + STATIC_RULES.strip() + "\n"
    headers_file.write_text(headers_content, encoding="utf-8")
    print("   Added static-asset cache rules to _headers")
else:
    print("   Already has /img/* rule, skipping")

# ---------- 2. Hero image loading attrs ----------
# In city pages (rentabilidad-*.html), the first <img> after <h1> is usually the hero.
# Mark it loading="eager" fetchpriority="high". Mark all other images as loading="lazy".
print("[2] Updating image loading attributes...")

RE_IMG = re.compile(r'<img\b([^>]*)>', re.IGNORECASE)
RE_LOADING = re.compile(r'\bloading\s*=\s*"[^"]*"', re.IGNORECASE)
RE_FETCHPR = re.compile(r'\bfetchpriority\s*=\s*"[^"]*"', re.IGNORECASE)

# Identify hero images: imgs with class "hero" or src="*hero*"
def is_hero_img(attrs):
    return ('class="hero' in attrs.lower() or 'class="ficha-hero' in attrs.lower()
            or '-hero.jpg' in attrs.lower() or 'logo-rendata-transparente' in attrs.lower())

modified_files = 0
hero_marked = 0
lazy_marked = 0
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    orig = txt
    # Walk imgs
    matches = list(RE_IMG.finditer(txt))
    # Identify first hero per file (in city pages first one matching is the hero)
    first_hero_idx = None
    for i, m in enumerate(matches):
        if is_hero_img(m.group(1)) and "logo-rendata" not in m.group(1).lower():
            first_hero_idx = i
            break

    # Build new text by re-emitting
    out = []
    last = 0
    for i, m in enumerate(matches):
        out.append(txt[last:m.start()])
        attrs = m.group(1)
        is_logo = 'logo-rendata' in attrs.lower()
        if i == first_hero_idx:
            # Hero: ensure loading="eager" and fetchpriority="high"
            attrs = RE_LOADING.sub('', attrs)
            attrs = RE_FETCHPR.sub('', attrs)
            attrs = attrs.rstrip() + ' loading="eager" fetchpriority="high"'
            hero_marked += 1
        elif is_logo:
            # Logo in nav: don't mess with it (browser handles fine)
            pass
        else:
            # Other images: ensure loading="lazy" if not already set
            if not RE_LOADING.search(attrs):
                attrs = attrs.rstrip() + ' loading="lazy"'
                lazy_marked += 1
        out.append('<img' + attrs + '>')
        last = m.end()
    out.append(txt[last:])
    new_txt = ''.join(out)
    if new_txt != orig:
        f.write_text(new_txt, encoding="utf-8")
        modified_files += 1

print(f"   {modified_files} files modified | {hero_marked} hero imgs marked eager | {lazy_marked} imgs marked lazy")

# ---------- 3. Verify async on Analytics/AdSense ----------
print("[3] Verifying async on third-party scripts...")
missing_async_count = 0
RE_GTAG = re.compile(r'<script\s+(?!async)[^>]*src="https://www\.googletagmanager\.com/[^"]*"', re.IGNORECASE)
RE_ADSENSE = re.compile(r'<script\s+(?!async)[^>]*src="https://pagead2\.googlesyndication\.com/[^"]*"', re.IGNORECASE)
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    if RE_GTAG.search(txt) or RE_ADSENSE.search(txt):
        missing_async_count += 1
print(f"   Pages with non-async third-party scripts: {missing_async_count}")

# ---------- 4. Defer the local nav-dropdown.js — already has defer ----------
# Verified earlier: <script src="/js/nav-dropdown.js" defer></script>

print("\nDone block 3.")
