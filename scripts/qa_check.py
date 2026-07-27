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
# El hash se calcula sobre el contenido con los saltos de línea NORMALIZADOS a LF.
# Motivo: el repo tiene core.autocrlf=true y no hay .gitattributes, así que un
# fichero puede estar en CRLF en el árbol de trabajo y en LF en producción (o al
# revés) sin que cambie ni un dato. Congelar los bytes crudos hacía que el hash
# guardase la codificación en vez del contenido, y no coincidía con lo servido.
def frozen_digest(path):
    return hashlib.sha256(open(path, "rb").read().replace(b"\r\n", b"\n")).hexdigest()

frozen = json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"]
if not frozen:
    print("[6] Congelados: OK (lista vacía, 0 congelados)")
frz_bad = []
for f, expected in frozen.items():
    fp = os.path.join(SITE, f)
    if not os.path.exists(fp):
        frz_bad.append((f, "NO EXISTE")); continue
    if frozen_digest(fp) != expected:
        frz_bad.append((f, "HASH CAMBIADO"))
if frz_bad:
    errors.append(f"[6] {len(frz_bad)} ficheros CONGELADOS alterados: {frz_bad}")
elif frozen:
    print(f"[6] Congelados: OK ({len(frozen)} ficheros con hash intacto)")

# --- Check 7: la cifra del nº de municipios coincide con len(DATA[]) ---
n_data = len(slugs) if mm else 0   # slugs viene del check 3
coherence_issues = []
for page in ("index.html", "prensa.html", "metodologia.html"):
    fp = os.path.join(SITE, page)
    if not os.path.exists(fp):
        continue
    txt = open(fp, encoding="utf-8").read()
    if str(n_data) not in txt:
        coherence_issues.append((page, f"no menciona {n_data}"))
    # 587 es un contador obsoleto inequívoco. ("209" aparece de forma legítima en
    # la nota de ampliación "de 209 a 597" / "edición de 209 ciudades", no se marca.)
    for stale in ("587 municipios", "587 ciudades"):
        if stale in txt:
            coherence_issues.append((page, f"cifra obsoleta: '{stale}'"))
if coherence_issues:
    errors.append(f"[7] {len(coherence_issues)} incoherencias de la cifra {n_data}: {coherence_issues}")
else:
    print(f"[7] Cifra municipios ({n_data}): OK y coherente en home/prensa/metodologia")

# --- Check 8: ROI de ficha == ROI de DATA[] + sin restos del módulo externo ---
data_roi = {}
data_d = {}
data_vp = {}
if mm:
    for bm in re.finditer(r'\{[^{}]*\}', mm.group(1)):
        b = bm.group(0)
        sm = re.search(r'sl:"([^"]+)"', b); rm = re.search(r'roi:([-\d.]+)', b)
        dm = re.search(r'd:(\d+)', b); vm = re.search(r'vp:([-\d.]+)', b)
        if sm and rm:
            data_roi[sm.group(1)] = f"{float(rm.group(1)):.1f}".replace(".", ",")
        if sm and dm:
            data_d[sm.group(1)] = dm.group(1)
        if sm and vm:
            data_vp[sm.group(1)] = f"{float(vm.group(1)):.1f}".replace(".", ",")
roi_ext = {
    "title": re.compile(r'<title>[^<]*?ROI (\d+,\d+)%'),
    "sticky": re.compile(r'ROI bruto</span><span class="sb-val[^"]*">(\d+,\d+)%'),
    "ed": re.compile(r'ed-stat-val">(\d+,\d+)%</div><div class="ed-stat-lbl">rentabilidad bruta'),
    # --- slots que faltaban y donde se escondió el bug de julio 2026 ---
    "hero": re.compile(r'<div class="sl">Rentabilidad bruta estimada</div>\s*<div class="sv"[^>]*>(\d+,\d+)%'),
    "gastos": re.compile(r'<span class="coll-trigger-title">Del (\d+,\d+)% bruto al'),
    "infobox": re.compile(r'se sitúa en el (\d+,\d+)%, (?:por encima de|por debajo de|en línea con) la media nacional'),
    "meta": re.compile(r'<meta name="description" content="[^"]*?: (\d+,\d+)% ROI'),
}
# ed-stat de días de venta y subida de precio anual (mismo patrón de bug)
ED_DIAS = re.compile(r'<div class="ed-stat-val">(\d+)</div><div class="ed-stat-lbl">días media venta</div>')
ED_VP = re.compile(r'<div class="ed-stat-val">\+([\d,]+)%</div><div class="ed-stat-lbl">subida precio anual</div>')
roi_dev = []
frozen_dev = []   # desviaciones en ficheros CONGELADOS -> warning, no error
external_remnants = []
EXT_HEADER = re.compile(r'alquiler residencial\s*[··]\s*Q4 2025')
EXT_MURCIA = re.compile(r'Murcia</span>[^%]{0,120}?7,4%')  # valor externo en un nb-módulo
_frozen_names = set(json.load(open(FROZEN_JSON, encoding="utf-8"))["frozen"])
for p in pages:
    if not p.startswith("rentabilidad-"):
        continue
    slug = p[len("rentabilidad-"):-len(".html")]
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    sink = frozen_dev if p in _frozen_names else roi_dev
    if slug in data_roi:
        want = data_roi[slug]
        for nm, rx in roi_ext.items():
            m = rx.search(txt)
            if m and m.group(1) != want:
                sink.append((p, nm, m.group(1), want))
    if slug in data_d:
        m = ED_DIAS.search(txt)
        if m and m.group(1) != data_d[slug]:
            sink.append((p, "ed-días", m.group(1), data_d[slug]))
    if slug in data_vp:
        m = ED_VP.search(txt)
        if m and m.group(1) != data_vp[slug]:
            sink.append((p, "ed-vp", m.group(1), data_vp[slug]))
    if EXT_HEADER.search(txt) or EXT_MURCIA.search(txt):
        external_remnants.append(p)
if frozen_dev:
    warnings.append(f"[8] {len(frozen_dev)} desviaciones en ficheros CONGELADOS "
                    f"(no se corrigen hasta levantar la congelación, ver "
                    f"PENDIENTES_DESCONGELACION.md): {frozen_dev}")
if roi_dev:
    errors.append(f"[8] {len(roi_dev)} desviaciones ficha↔DATA[]: {roi_dev[:6]}")
elif external_remnants:
    errors.append(f"[8] {len(external_remnants)} fichas con restos del módulo externo sin atribuir: {external_remnants[:6]}")
else:
    print(f"[8] ROI/días/vp ficha==DATA[] y sin módulo externo: OK ({len(data_roi)} fichas)")

# --- Check 9: el badge "Media España" == media real de DATA[] (constante única) ---
# Nació como literal 6,5% (media de la edición de 209 ciudades) y en las fichas
# resincronizadas se sobrescribió con el ROI del propio municipio etiquetado
# "Media España". Debe ser UNA sola cifra en las 597, la media real de DATA[].
data_rois = []
if mm:
    for bm in re.finditer(r'\{[^{}]*\}', mm.group(1)):
        rm = re.search(r'roi:([-\d.]+)', bm.group(0))
        if rm:
            data_rois.append(float(rm.group(1)))
badge_re = re.compile(r'<span class="badge badge-n">Media España (\d+,\d+)%</span>')
natl_ref = re.compile(r'La rentabilidad media de España es el (\d+,\d+)%')
if not data_rois:
    errors.append("[9] No se pudo calcular la media nacional desde DATA[]")
else:
    want_natl = f"{sum(data_rois) / len(data_rois):.1f}".replace(".", ",")
    badge_dev, badge_missing = [], []
    for p in pages:
        if not p.startswith("rentabilidad-"):
            continue
        slug = p[len("rentabilidad-"):-len(".html")]
        if slug not in data_roi:
            continue
        txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
        m = badge_re.search(txt)
        if not m:
            badge_missing.append(p)
        elif m.group(1) != want_natl:
            badge_dev.append((p, m.group(1), want_natl))
        m2 = natl_ref.search(txt)
        if m2 and m2.group(1) != want_natl:
            badge_dev.append((p, "info-box " + m2.group(1), want_natl))
    if badge_dev:
        errors.append(f"[9] {len(badge_dev)} badges/referencias 'Media España' != media real "
                      f"{want_natl}%: {badge_dev[:6]}")
    elif badge_missing:
        errors.append(f"[9] {len(badge_missing)} fichas sin badge 'Media España': {badge_missing[:6]}")
    else:
        print(f"[9] Badge 'Media España' == media real DATA[] ({want_natl}%): "
              f"OK (constante única en {len(data_roi)} fichas)")

# --- Check 10: la tabla "Gastos reales" cuadra consigo misma ---
# Antes del fix de 2026-07-27 la fila del neto no era la suma de la tabla que
# resumía (fallaba en 597/597) y los ingresos venían de una plantilla de
# 6.000€/año o de un trimestre anterior. Se exige: ingresos == alq*12 de DATA[]
# y neto_€ == ingresos - suma(gastos).
G_ING = re.compile(r'<div class="gasto-name">[^<]*Ingresos por alquiler</div>\s*'
                   r'<div class="gasto-val" style="color:var\(--green\)">\+([\d.]+)€')
G_NETO = re.compile(r'Rentabilidad neta estimada</div>\s*<div class="gasto-val"[^>]*>[\d,]+%'
                    r'</div>\s*<div class="gasto-val"[^>]*>([\d.]+)€/año')
G_ROWS = [re.compile(r'<div class="gasto-name">[^<]*' + re.escape(lbl) +
                     r'[^<]*</div>\s*<div class="gasto-val" style="color:var\(--red\)">-([\d.]+)€')
          for lbl in ("IBI (Impuesto sobre Bienes Inmuebles)", "Gastos de comunidad",
                      "Mantenimiento y reparaciones", "Seguro de hogar e impagos",
                      "Vacancia estimada", "IRPF sobre rendimientos")]
data_alq = {}
if mm:
    for bm in re.finditer(r'\{[^{}]*\}', mm.group(1)):
        b = bm.group(0)
        sm = re.search(r'sl:"([^"]+)"', b); am = re.search(r'alq:(\d+)', b)
        if sm and am:
            data_alq[sm.group(1)] = int(am.group(1))
_n = lambda s: int(s.replace(".", ""))
gastos_dev, gastos_frozen, gastos_ok = [], [], 0
for p in pages:
    if not p.startswith("rentabilidad-"):
        continue
    slug = p[len("rentabilidad-"):-len(".html")]
    if slug not in data_alq:
        continue
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    mi = G_ING.search(txt); mn = G_NETO.search(txt)
    if not (mi and mn):
        continue
    rows = [r.search(txt) for r in G_ROWS]
    if not all(rows):
        gastos_dev.append((p, "tabla incompleta")); continue
    ing = _n(mi.group(1)); neto = _n(mn.group(1))
    suma = sum(_n(r.group(1)) for r in rows)
    problemas = []
    if ing != data_alq[slug] * 12:
        problemas.append(f"ingresos {ing} != alq*12 {data_alq[slug] * 12}")
    if neto != ing - suma:
        problemas.append(f"neto {neto} != ingresos-gastos {ing - suma}")
    if problemas:
        (gastos_frozen if p in _frozen_names else gastos_dev).append((p, "; ".join(problemas)))
    else:
        gastos_ok += 1
if gastos_frozen:
    warnings.append(f"[10] {len(gastos_frozen)} tablas de gastos desviadas en ficheros "
                    f"CONGELADOS (ver PENDIENTES_DESCONGELACION.md): "
                    f"{[f for f, _ in gastos_frozen]}")
if gastos_dev:
    errors.append(f"[10] {len(gastos_dev)} tablas 'Gastos reales' que no cuadran: {gastos_dev[:6]}")
else:
    print(f"[10] Gastos reales (ingresos==alq*12 y neto==ingresos-gastos): OK "
          f"({gastos_ok} fichas)")

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
