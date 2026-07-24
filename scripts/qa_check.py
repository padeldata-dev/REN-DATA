#!/usr/bin/env python3
"""
Guardián de calidad de Ren Data — verificación local en una sola pasada.

Comprueba, sobre rendata_beta/ (incluidos subdirectorios academia/ y en/):
  1. Enlaces internos rotos (0 tolerados).
  2. sitemap.xml: todas sus URLs resuelven a una página existente.
  3. Slugs únicos en el DATA[] de index.html.
  4. canonical presente, absoluto y en el dominio rendata.es; og:url coherente.
  5. JSON-LD parseable en todas las páginas.
  6. SHA256 de los ficheros CONGELADOS == frozen_files.json (si cambia → FALLA).

Uso:
    python scripts/qa_check.py
Sale con código 0 si todo pasa; 1 si algún check crítico falla.
Ejecútalo SIEMPRE antes de cada deploy.
"""
import os, re, sys, json, glob, hashlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "rendata_beta")
FROZEN_JSON = os.path.join(ROOT, "frozen_files.json")

errors = []   # críticos → exit 1
warnings = []

def rel(p):
    return os.path.relpath(p, SITE).replace("\\", "/")

# --- enumerar páginas ---
pages = [rel(p) for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True)]
pageset = set(pages)
# también aceptamos clean-URL (sin .html) y "/" -> index.html
def page_exists(relpath):
    return relpath in pageset

href_re = re.compile(r'href="([^"]+)"', re.I)

def resolve_link(href, from_page):
    h = href.strip()
    if h.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "data:", "#")):
        return None
    if "$" in h or "{" in h:          # plantillas JS (href="...${x}...")
        return None
    h = h.split("#", 1)[0].split("?", 1)[0]
    if h == "" :
        return None
    if h in ("/",):
        return "index.html"
    if h.startswith("/"):
        base = h.lstrip("/")
    else:
        # relativo al directorio de la página de origen
        d = os.path.dirname(from_page)
        base = (d + "/" + h) if d else h
        base = os.path.normpath(base).replace("\\", "/")
    if base.endswith("/") or base == "":
        base = base + "index.html"          # índice de directorio (/en/ -> en/index.html)
    if base.endswith(".html"):
        return base if base in pageset else ("__MISSING__:" + base)
    # clean URL -> base.html
    if base + ".html" in pageset:
        return base + ".html"
    # directorios "/" servidos como index? o assets (img/css/js) -> ignorar no-página
    if re.search(r'\.(png|jpg|jpeg|webp|svg|css|js|xml|ico|txt|woff2?|json|pdf)$', base, re.I):
        return None
    # podría ser clean URL de subdir
    return "__MISSING__:" + base + ".html"

# --- Check 1: enlaces internos rotos ---
broken = []
for p in pages:
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    for m in href_re.finditer(txt):
        r = resolve_link(m.group(1), p)
        if r and r.startswith("__MISSING__:"):
            broken.append((p, m.group(1)))
if broken:
    errors.append(f"[1] {len(broken)} enlaces internos rotos. Ejemplos: {broken[:8]}")
else:
    print(f"[1] Enlaces internos: OK (0 rotos en {len(pages)} páginas)")

# --- Check 2: sitemap ---
sm = os.path.join(SITE, "sitemap.xml")
if os.path.exists(sm):
    smtxt = open(sm, encoding="utf-8").read()
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", smtxt)
    sm_broken = []
    for loc in locs:
        path = re.sub(r"^https?://[^/]+/", "", loc).split("#")[0].split("?")[0]
        if path in ("", "/"):
            path = "index.html"
        if path.endswith("/"):
            cand = path + "index.html"       # índice de directorio
        elif not path.endswith(".html"):
            cand = path + ".html"
        else:
            cand = path
        if cand not in pageset:
            sm_broken.append(loc)
    if sm_broken:
        errors.append(f"[2] {len(sm_broken)} URLs del sitemap no resuelven. Ejemplos: {sm_broken[:8]}")
    else:
        print(f"[2] Sitemap: OK ({len(locs)} URLs, todas resuelven)")
else:
    warnings.append("[2] sitemap.xml no encontrado")

# --- Check 3: slugs únicos en DATA[] ---
idx = open(os.path.join(SITE, "index.html"), encoding="utf-8").read()
mm = re.search(r"const DATA=\[(.*?)\n\];", idx, re.S)
if mm:
    slugs = re.findall(r'sl:"([^"]+)"', mm.group(1))
    dups = {s for s in slugs if slugs.count(s) > 1}
    if dups:
        errors.append(f"[3] Slugs duplicados en DATA[]: {sorted(dups)}")
    else:
        print(f"[3] Slugs DATA[]: OK ({len(slugs)} únicos)")
else:
    errors.append("[3] No se encontró DATA[] en index.html")

# --- Check 4: canonical / og:url ---
canon_issues = []
for p in pages:
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    cans = re.findall(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', txt, re.I)
    if p == "404.html":
        continue
    if len(cans) != 1:
        canon_issues.append((p, f"{len(cans)} canonical"))
        continue
    c = cans[0]
    if not c.startswith("https://rendata.es/"):
        canon_issues.append((p, f"canonical no rendata.es: {c}"))
    og = re.findall(r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"', txt, re.I)
    if og and not og[0].startswith("https://rendata.es"):
        canon_issues.append((p, f"og:url host raro: {og[0]}"))
if canon_issues:
    errors.append(f"[4] {len(canon_issues)} problemas canonical/og:url. Ejemplos: {canon_issues[:8]}")
else:
    print(f"[4] canonical/og:url: OK")

# --- Check 5: JSON-LD parseable ---
jsonld_bad = []
for p in pages:
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    for blk in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', txt, re.S | re.I):
        try:
            json.loads(blk)
        except Exception as e:
            jsonld_bad.append((p, str(e)[:60]))
            break
if jsonld_bad:
    errors.append(f"[5] {len(jsonld_bad)} páginas con JSON-LD inválido. Ejemplos: {jsonld_bad[:8]}")
else:
    print(f"[5] JSON-LD: OK (parseable en todas)")

# --- Check 6: hashes de congelados ---
frozen = json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"]
frz_bad = []
for f, expected in frozen.items():
    fp = os.path.join(SITE, f)
    if not os.path.exists(fp):
        frz_bad.append((f, "NO EXISTE")); continue
    got = hashlib.sha256(open(fp, "rb").read()).hexdigest()
    if got != expected:
        frz_bad.append((f, "HASH CAMBIADO"))
if frz_bad:
    errors.append(f"[6] {len(frz_bad)} ficheros CONGELADOS alterados: {frz_bad}")
else:
    print(f"[6] Congelados: OK ({len(frozen)} ficheros con hash intacto)")

# --- resumen ---
print("-" * 60)
for w in warnings:
    print("WARN", w)
if errors:
    print(f"QA FAILED — {len(errors)} check(s) crítico(s):")
    for e in errors:
        print("  [X]", e)
    sys.exit(1)
print("QA OK — todos los checks críticos pasan.")
sys.exit(0)
