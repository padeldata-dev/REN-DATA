"""Block 1 auto-fixes for SEO audit findings.

Fixes:
  1. JSON-LD single-quote bug (keywords array using ' instead of ")
  2. Titles too long: trim intelligently
  3. Descs too long: trim to last sentence boundary ≤160
  4. Missing meta description in 3 pages
  5. Canonical mismatch in 404.html
  6. Title too short in aviso-legal.html, contacto.html
  7. Duplicate description (rentabilidad-l-* pages)

Does NOT auto-fix:
  - H hierarchy skips (would need DOM-level edits per page)
  - Image dimensions (21k flag/icon imgs — false positives mostly)
"""
import json
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")
SITE_URL = "https://rendata.es"

fixes = 0

# ------------------- 1. JSON-LD single-quote fix -------------------
# Pattern: 'string' inside keywords arrays. Convert to "string".
# Be careful: only inside JSON-LD scripts, only the value tokens.
RE_JSONLD = re.compile(r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)', re.IGNORECASE)

def fix_jsonld(block_body):
    # Try parsing first — if OK, no change.
    try:
        json.loads(block_body.strip())
        return block_body, False
    except json.JSONDecodeError:
        pass
    # Replace 'X' tokens that look like JSON strings (between , [ : after whitespace)
    # Use a careful regex: replace `'(?:[^'\\]|\\.)*'` only when surrounded by JSON-ish context.
    # Safest: replace any single-quoted token if the surrounding chars are , [ :  whitespace.
    new = re.sub(
        r"(?<=[\[,:\s])'((?:[^'\\]|\\.)*)'",
        lambda m: '"' + m.group(1).replace('"', '\\"') + '"',
        block_body,
    )
    try:
        json.loads(new.strip())
        return new, True
    except json.JSONDecodeError:
        return block_body, False

jsonld_fixed = 0
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    orig = txt
    def replacer(m):
        global jsonld_fixed
        body, changed = fix_jsonld(m.group(2))
        if changed: jsonld_fixed += 1
        return m.group(1) + body + m.group(3)
    new = RE_JSONLD.sub(replacer, txt)
    if new != orig:
        f.write_text(new, encoding="utf-8")
print(f"[1] JSON-LD blocks fixed: {jsonld_fixed}")
fixes += jsonld_fixed

# ------------------- 2. Title length normalization -------------------
RE_TITLE = re.compile(r'<title>([^<]*)</title>', re.IGNORECASE)

def shorten_title(t, max_len=60):
    """Trim title to max_len keeping ' | Ren Data' suffix if possible."""
    SUFFIX = " | Ren Data"
    if t.endswith(SUFFIX):
        core = t[:-len(SUFFIX)]
        budget = max_len - len(SUFFIX)
        if len(core) <= budget: return t
        # Cut at last sensible break
        cut = core[:budget]
        # Backtrack to space/em-dash/dot
        for sep in [" — ", " · ", " - ", " ", "."]:
            idx = cut.rfind(sep)
            if idx > budget * 0.5:
                cut = cut[:idx]
                break
        return cut.rstrip(" -—·.") + SUFFIX
    # No suffix — just trim
    return t[:max_len].rstrip(" -—·.") + "…"

titles_fixed = 0
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    m = RE_TITLE.search(txt)
    if not m: continue
    t = m.group(1)
    if len(t) > 70:
        new_t = shorten_title(t, max_len=60)
        if new_t != t:
            txt = txt[:m.start(1)] + new_t + txt[m.end(1):]
            f.write_text(txt, encoding="utf-8")
            titles_fixed += 1
print(f"[2] Titles shortened: {titles_fixed}")
fixes += titles_fixed

# ------------------- 2b. Title too short: contacto / aviso legal -------------------
SHORT_TITLE_FIX = {
    "aviso-legal.html": "Aviso legal — Información corporativa | Ren Data",
    "contacto.html": "Contacto — Ren Data, datos del mercado inmobiliario",
}
for name, new in SHORT_TITLE_FIX.items():
    p = ROOT / name
    if not p.exists(): continue
    txt = p.read_text(encoding="utf-8")
    new_txt = re.sub(r'<title>[^<]*</title>', f'<title>{new}</title>', txt, count=1)
    if new_txt != txt:
        p.write_text(new_txt, encoding="utf-8")
        fixes += 1
        print(f"   Title rewritten: {name}")

# ------------------- 3. Meta description length normalization -------------------
RE_META_DESC = re.compile(
    r'(<meta[^>]+name=["\']description["\'][^>]*content=["\'])([^"\']*)(["\'][^>]*>)',
    re.IGNORECASE,
)

def shorten_desc(d, max_len=160):
    if len(d) <= max_len: return d
    # Cut at last sentence boundary or word boundary
    cut = d[:max_len]
    for sep in [". ", "; ", " — ", ", ", " "]:
        idx = cut.rfind(sep)
        if idx > max_len * 0.5:
            cut = cut[:idx]
            return cut.rstrip(" .;,—-") + "."
    return cut.rstrip() + "…"

descs_fixed = 0
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    m = RE_META_DESC.search(txt)
    if not m: continue
    d = m.group(2)
    if len(d) > 165:
        new_d = shorten_desc(d, max_len=158)
        if new_d != d:
            txt = txt[:m.start()] + m.group(1) + new_d + m.group(3) + txt[m.end():]
            f.write_text(txt, encoding="utf-8")
            descs_fixed += 1
print(f"[3] Meta descriptions shortened: {descs_fixed}")
fixes += descs_fixed

# ------------------- 4. Missing meta description (3 pages) -------------------
MISSING_DESC_FIX = {
    "404.html": "Página no encontrada en Ren Data. Vuelve al inicio o explora las 587 ciudades, rankings y análisis del mercado inmobiliario español.",
    "aviso-legal.html": "Aviso legal de Ren Data. Información corporativa, condiciones de uso y datos de contacto del editor responsable del sitio.",
    "privacidad.html": "Política de privacidad de Ren Data. Cómo tratamos tus datos, cookies utilizadas, derechos del usuario y contacto del responsable.",
}
for name, desc in MISSING_DESC_FIX.items():
    p = ROOT / name
    if not p.exists(): continue
    txt = p.read_text(encoding="utf-8")
    if re.search(r'<meta[^>]+name=["\']description["\']', txt, re.IGNORECASE):
        continue
    new = re.sub(
        r'(<meta charset[^>]+>\s*)',
        r'\1<meta name="description" content="' + desc.replace('"', '&quot;') + '">\n',
        txt, count=1, flags=re.IGNORECASE,
    )
    if new != txt:
        p.write_text(new, encoding="utf-8")
        fixes += 1
        print(f"   Meta description added: {name}")

# ------------------- 5. Canonical mismatch in 404.html -------------------
p = ROOT / "404.html"
if p.exists():
    txt = p.read_text(encoding="utf-8")
    new = re.sub(
        r'(<link[^>]+rel=["\']canonical["\'][^>]*href=["\'])([^"\']*)(["\'])',
        r'\1https://rendata.es/404.html\3',
        txt, count=1, flags=re.IGNORECASE,
    )
    if new != txt:
        p.write_text(new, encoding="utf-8")
        fixes += 1
        print("[5] Canonical fixed in 404.html")

# ------------------- 6. Duplicate descs in rentabilidad-l-* pages -------------------
# These have the same starting prefix. Rewrite each to be unique by including the city name.
RE_L_FILES = re.compile(r'^rentabilidad-l-(.+)\.html$')
for f in ROOT.glob("rentabilidad-l-*.html"):
    m = RE_L_FILES.match(f.name)
    if not m: continue
    # Derive city display name from slug
    slug_tail = m.group(1)
    display = "L'" + slug_tail.replace("-", " ").title().replace("De ", "de ").replace("Del ", "del ").replace("La ", "la ")
    # Look at current title to get accurate city name
    txt = f.read_text(encoding="utf-8")
    tm = RE_TITLE.search(txt)
    title_text = tm.group(1) if tm else ""
    # Extract the city from title (everything up to first "—" or " | ")
    city_match = re.match(r'(.*?)(?: [—|·] | \| )', title_text)
    city = city_match.group(1).strip() if city_match else display
    # New description
    new_desc = f"Rentabilidad del alquiler en {city}: ROI bruto, precio m², alquiler medio y datos del mercado inmobiliario actualizados. Ficha completa con perspectiva inversora."
    new_desc = new_desc[:158]
    txt2 = re.sub(
        r'(<meta[^>]+name=["\']description["\'][^>]*content=["\'])([^"\']*)(["\'][^>]*>)',
        lambda mm: mm.group(1) + new_desc + mm.group(3),
        txt, count=1, flags=re.IGNORECASE,
    )
    if txt2 != txt:
        f.write_text(txt2, encoding="utf-8")
        fixes += 1
print("[6] Rewrote descriptions for rentabilidad-l-* pages")

print(f"\nTotal fixes: {fixes}")
