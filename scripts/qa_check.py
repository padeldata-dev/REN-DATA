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
  ...
 15. URLs duplicadas: cada página tiene su 301 `.html` → URL limpia en
     _redirects, ningún canonical apunta a la variante `.html` y el sitemap
     solo lista la versión canónica.

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
# RENDATA_SITE permite apuntar el guardián a una copia del sitio; lo usa
# scripts/test_qa_check.py para inyectar bugs y comprobar que cada check falla.
SITE = os.environ.get("RENDATA_SITE") or os.path.join(ROOT, "rendata_beta")
FROZEN_JSON = os.environ.get("RENDATA_FROZEN") or os.path.join(ROOT, "frozen_files.json")

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

# --- Check 11: campo `pob` coherente entre DATA[], RANK[] y la ficha ---
# INVARIANTE DURO: si DATA[] y RANK[] traen ambos `pob`, deben coincidir. Son dos
# copias del mismo dato y desincronizarlas es peor que tenerlas mal a la vez.
# DEUDA (warning): `pob` nunca se pobló con padrón — lleva marcadores redondeados
# a millar — y las fichas tampoco son fiables del todo (34 comparten valor con
# otra ficha, algunas traen valores absurdos). Ver scripts/sync_poblacion.py y
# PENDIENTES_DESCONGELACION.md.
rank_path = os.path.join(SITE, "ranking.html")
if not os.path.exists(rank_path):
    warnings.append("[11] ranking.html no encontrado")
else:
    rtxt = open(rank_path, encoding="utf-8", errors="ignore").read()
    ri = rtxt.find("const RANK=[")
    rj = rtxt.find("];", ri)
    def _pobs(blob):
        o = {}
        for bm in re.finditer(r'\{[^{}]*\}', blob):
            b = bm.group(0)
            s = re.search(r'sl:"([^"]+)"', b); p = re.search(r'pob:(\d+)', b)
            if s:
                o[s.group(1)] = int(p.group(1)) if p else None
        return o
    pob_data = _pobs(mm.group(1)) if mm else {}
    pob_rank = _pobs(rtxt[ri + len("const RANK=["):rj]) if ri != -1 else {}
    pob_ficha = {}
    for p in pages:
        if not p.startswith("rentabilidad-"):
            continue
        t = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
        m = re.search(r'<div class="demo-val">([\d.]+)</div>\s*'
                      r'<div class="demo-label">Habitantes', t)
        if m:
            pob_ficha[p[len("rentabilidad-"):-len(".html")]] = int(m.group(1).replace(".", ""))
    conflictos = [(s, pob_data[s], pob_rank[s]) for s in pob_data
                  if pob_data.get(s) is not None and pob_rank.get(s) is not None
                  and pob_data[s] != pob_rank[s]]
    sin_pob = [s for s in pob_data if pob_data[s] is None]
    vs_ficha = [s for s in pob_data
                if pob_data.get(s) is not None and s in pob_ficha
                and pob_data[s] != pob_ficha[s]]
    if conflictos:
        errors.append(f"[11] {len(conflictos)} municipios con pob distinto entre DATA[] y "
                      f"RANK[] (deben ir sincronizados): {conflictos[:6]}")
    else:
        print(f"[11] pob DATA[]==RANK[]: OK (0 conflictos en {len(pob_data)} municipios)")
    if sin_pob or vs_ficha:
        warnings.append(f"[11] deuda de población: {len(sin_pob)} sin `pob` en DATA[] y "
                        f"{len(vs_ficha)} que no cuadran con su ficha. "
                        f"Plan y cuarentena en scripts/sync_poblacion.py "
                        f"(bloqueado: ranking.html congelado).")

# --- Check 12: cifras en PROSA editorial ligadas a DATA[] ---
# [8] solo vigila huecos estructurados (hero, ed-stat, gastos, meta...). Estas tres
# frases viven en texto libre y por eso sobrevivieron a tres rondas de fixes: se
# detectaron el 2026-07-27 verificando Ronda, cuyo editorial decía "yield del 5,6%"
# con un titular de 5,5%, y cuyo info-box daba `va` (alquiler) como subida del PRECIO.
PROSA = {
    "yield": (re.compile(r"yield del\s*(?:<strong>)?([\d,]+)%"), "roi"),
    "12-meses": (re.compile(r"En los últimos 12 meses el precio ha subido un ([\d,]+)%"), "vp"),
    "revalorización": (re.compile(r"revalorización anual del inmueble \(\+([\d,]+)%\)"), "vp"),
    "info-box-precio": (re.compile(r"El precio de la vivienda en .+? ha subido un ([\d,]+)%"), "vp"),
    "info-box-alquiler": (re.compile(r"El precio de la vivienda en .+? ha subido un [\d,]+% en el "
                                     r"último año[.,] (?:El alquiler sube aún más rápido|"
                                     r"por encima del alquiler|al mismo ritmo que el alquiler) "
                                     r"\(\+([\d,]+)%\)"), "va"),
}
data_vals = {}
if mm:
    for bm in re.finditer(r'\{[^{}]*\}', mm.group(1)):
        b = bm.group(0)
        sm = re.search(r'sl:"([^"]+)"', b)
        if not sm:
            continue
        d = {}
        for k in ("roi", "vp", "va"):
            v = re.search(k + r":([-\d.]+)", b)
            if v:
                d[k] = f"{float(v.group(1)):.1f}".replace(".", ",")
        data_vals[sm.group(1)] = d
prosa_dev, prosa_frozen, prosa_ok = [], [], 0
for p in pages:
    if not p.startswith("rentabilidad-"):
        continue
    slug = p[len("rentabilidad-"):-len(".html")]
    if slug not in data_vals:
        continue
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    fallos = []
    for nombre, (rx, campo) in PROSA.items():
        want = data_vals[slug].get(campo)
        if not want:
            continue
        for m in rx.finditer(txt):
            if m.group(1) != want:
                fallos.append(f"{nombre} {m.group(1)}%!={want}%")
                break
    if fallos:
        (prosa_frozen if p in _frozen_names else prosa_dev).append((p, "; ".join(fallos)))
    else:
        prosa_ok += 1
# la frase comparativa debe decir lo que dicen los datos, no lo contrario
COMPARA = re.compile(r"ha subido un ([\d,]+)% en el último año\. El alquiler sube aún más "
                     r"rápido \(\+([\d,]+)%\)")
logica = []
for p in pages:
    if not p.startswith("rentabilidad-"):
        continue
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    m = COMPARA.search(txt)
    if m and float(m.group(2).replace(",", ".")) <= float(m.group(1).replace(",", ".")):
        (prosa_frozen if p in _frozen_names else logica).append(
            (p, f"dice 'sube aún más rápido' con alquiler +{m.group(2)}% <= precio +{m.group(1)}%"))
if prosa_frozen:
    warnings.append(f"[12] {len(prosa_frozen)} desviaciones de prosa en ficheros CONGELADOS "
                    f"(ver PENDIENTES_DESCONGELACION.md): {[f for f, _ in prosa_frozen]}")
if prosa_dev or logica:
    errors.append(f"[12] {len(prosa_dev)} fichas con cifras de prosa != DATA[] y "
                  f"{len(logica)} con la comparación precio/alquiler al revés: "
                  f"{(prosa_dev + logica)[:5]}")
else:
    print(f"[12] Prosa editorial (yield, 12 meses, revalorización, info-box) == DATA[]: "
          f"OK ({prosa_ok} fichas)")

# --- Check 13: precio y alquiler ligados a DATA[] en TODOS los huecos ---
# [8] solo vigilaba el ROI (7 slots), los días del ed-stat y el vp del ed-stat.
# El precio y el alquiler se quedaron sueltos en el hero, la barra sticky, el
# gráfico de evolución, "Pulso del mercado", la FAQ JSON-LD y la prosa: 484 de
# 597 fichas servían un precio o un alquiler distinto del de DATA[] (detectado
# el 2026-07-29; el caso de referencia era Villena, cuyo hero decía 750€/+11,0%
# y 400€/+15,0% con DATA[] en 730€/+9,4% y 389€/+7,6%).
# Lo arregla scripts/fix_ficha_sync.py; esto impide que vuelva a colarse.
def _eu(v):
    return "{:,}".format(int(round(v))).replace(",", ".")

def _pc(v, sep=","):
    return ("%.1f" % v).replace(".", sep)

SYNC_SLOTS = [
    ("meta-alquiler",  r'<meta name="description" content="[^"]*?€, alquiler ([\d.]+)€/mes', "alq", _eu),
    ("og-alquiler",    r'<meta property="og:description" content="[^"]*?€, alquiler ([\d.]+)€/mes', "alq", _eu),
    ("jsonld-precio",  r'"description":"Análisis de rentabilidad inmobiliaria en [^"]*?\. Precio m² ([\d.]+)€', "p", _eu),
    ("jsonld-alq",     r'"description":"Análisis de rentabilidad inmobiliaria en [^"]*?alquiler medio ([\d.]+)€/mes', "alq", _eu),
    ("faq-precio",     r'El precio medio del metro cuadrado en [^"]*? es de ([\d.]+)€/m²', "p", _eu),
    ("faq-alquiler",   r'El alquiler medio en [^"]*? es de ([\d.]+)€/mes para un piso estándar', "alq", _eu),
    ("faq-va",         r'Los alquileres en [^"]*? han subido un ([\d,]+)% en el último año', "va", _pc),
    ("sticky-precio",  r'<span class="sb-label">Precio m²</span><span class="sb-val[^"]*">([\d.]+)€', "p", _eu),
    ("sticky-alq",     r'<span class="sb-label">Alquiler</span><span class="sb-val[^"]*">([\d.]+)€/mes', "alq", _eu),
    ("hero-precio",    r'<div class="sl">Precio m²</div><div class="sv"[^>]*>([\d.]+)€', "p", _eu),
    ("hero-vp",        r'<div class="sl">Precio m²</div><div class="sv"[^>]*>[\d.]+€</div><div style="[^"]*"><span class="badge badge-\w+">[↑↓] ([\d,]+)% anual', "vp", _pc),
    ("hero-alquiler",  r'<div class="sl">Alquiler medio</div><div class="sv"[^>]*>([\d.]+)€', "alq", _eu),
    ("hero-va",        r'<div class="sl">Alquiler medio</div><div class="sv"[^>]*>[\d.]+€</div><div style="[^"]*"><span class="badge badge-\w+">[↑↓] ([\d,]+)% anual', "va", _pc),
    ("evo-precio",     r'Precio actual</span><div style="[^"]*">([\d.]+) €/m²', "p", _eu),
    ("evo-vp",         r'<span class="badge badge-\w+">[↑↓] ([\d,]+)% último año</span>', "vp", _pc),
    ("pulso-dias",     r'<div class="ival">(\d+)</div><div class="ilabel">Días de media en mercado', "d", lambda v: str(int(v))),
    ("prosa-dias",     r'con los pisos vendiéndose en tan solo (\d+) días de media', "d", lambda v: str(int(v))),
    ("prosa-precio",   r'El precio del metro cuadrado ha alcanzado los ([\d.]+)€', "p", _eu),
    ("prosa-alq",      r'en los últimos 12 meses, alcanzando los ([\d.]+)€ mensuales', "alq", _eu),
    # gemelo de ED_VP de [8]: solo existe en las 6 fichas de plantilla propia
    # (Alicante, Barcelona, Granada, Palma, Valencia, Sevilla) y no lo vigilaba nadie.
    ("edstat-va",      r'<div class="ed-stat-val">\+([\d,]+)%</div><div class="ed-stat-lbl">subida alquiler anual</div>', "va", _pc),
]
SYNC_RX = [(n, re.compile(r), f, fm) for n, r, f, fm in SYNC_SLOTS]
data_full = {}
if mm:
    for bm in re.finditer(r'\{[^{}]*\}', mm.group(1)):
        b = bm.group(0)
        sm = re.search(r'sl:"([^"]+)"', b)
        if not sm:
            continue
        rec, ok = {}, True
        for k in ("roi", "p", "alq", "vp", "va", "d"):
            v = re.search(k + r":([-\d.]+)", b)
            if not v:
                ok = False
                break
            rec[k] = float(v.group(1))
        if ok:
            data_full[sm.group(1)] = rec
sync_dev, sync_frozen, sync_ok = [], [], 0
for p in pages:
    if not p.startswith("rentabilidad-"):
        continue
    slug = p[len("rentabilidad-"):-len(".html")]
    if slug not in data_full:
        continue
    c = data_full[slug]
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    fallos = []
    for nombre, rx, campo, fmt in SYNC_RX:
        want = fmt(c[campo])
        for m in rx.finditer(txt):
            if m.group(1) != want:
                fallos.append(f"{nombre} {m.group(1)}!={want}")
                break
    if fallos:
        (sync_frozen if p in _frozen_names else sync_dev).append((p, "; ".join(fallos[:4])))
    else:
        sync_ok += 1
if sync_frozen:
    warnings.append(f"[13] {len(sync_frozen)} fichas CONGELADAS con precio/alquiler desincronizado "
                    f"(ver PENDIENTES_DESCONGELACION.md): {[f for f, _ in sync_frozen]}")
if sync_dev:
    errors.append(f"[13] {len(sync_dev)} fichas con precio/alquiler != DATA[] en hero/sticky/evo/"
                  f"pulso/FAQ/prosa: {sync_dev[:5]}")
else:
    print(f"[13] Precio/alquiler ficha == DATA[] en los {len(SYNC_SLOTS)} huecos: OK ({sync_ok} fichas)")

# --- Check 14: gráfico de evolución coherente + tarjeta ITP ---
# 74 fichas dibujaban una serie DESCENDENTE con la etiqueta "↑ X%" y en 263 el
# último punto no era el precio de DATA[] (p. ej. Sestao: 2.820€ en 2024 -> 1.900€
# en 2026 rotulado "↑ 4,5%"). Y 181 tarjetas de ITP arrastraban el texto de
# plantilla "piso de 68.880€ / 5.510€ de ITP", que no correspondía ni al precio
# del municipio ni al tipo de su comunidad.
ITP_CCAA_QA = {
    "C. de Madrid": 6.0, "Navarra": 6.0, "Canarias": 6.5, "País Vasco": 4.0,
    "Andalucía": 7.0, "La Rioja": 7.0, "Aragón": 8.0, "Asturias": 8.0,
    "Castilla y León": 8.0, "R. de Murcia": 8.0, "Cantabria": 9.0,
    "Castilla-La Mancha": 9.0, "Galicia": 9.0, "Cataluña": 10.0,
    "C. Valenciana": 10.0, "Extremadura": 8.0, "Islas Baleares": 9.0,
    "Ceuta": 0.5, "Melilla": 0.5,
}
data_cc = {}
if mm:
    for bm in re.finditer(r'\{[^{}]*\}', mm.group(1)):
        b = bm.group(0)
        sm = re.search(r'sl:"([^"]+)"', b)
        cm = re.search(r'cc:"([^"]+)"', b)
        if sm and cm:
            data_cc[sm.group(1)] = cm.group(1)
EVO_COL_QA = re.compile(r'<div class="evo-col"><span class="evo-v(?: cur)?">([\d.]+)€</span>')
ITP_QA = re.compile(r'<div class="itp-val">([\d,.]+)<span class="itp-pct">%</span></div>')
ITP_DESC_QA = re.compile(r'Para un piso de ([\d.]+)€ pagarás <strong>([\d.]+)€ de (?:ITP|IGIC|IPSI)</strong>')
evo_dev, evo_frozen, evo_ok = [], [], 0
for p in pages:
    if not p.startswith("rentabilidad-"):
        continue
    slug = p[len("rentabilidad-"):-len(".html")]
    if slug not in data_full:
        continue
    c = data_full[slug]
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    fallos = []
    vals = [int(v.replace(".", "")) for v in EVO_COL_QA.findall(txt)]
    if len(vals) < 2:
        fallos.append("serie ilegible")
    else:
        if vals[-1] != int(c["p"]):
            fallos.append(f"serie acaba en {vals[-1]} y DATA[] dice {int(c['p'])}")
        subida = vals[-1] >= vals[-2]
        if subida != (c["vp"] >= 0):
            fallos.append(f"serie {'sube' if subida else 'baja'} con vp {c['vp']:+.1f}%")
    rate = ITP_CCAA_QA.get(data_cc.get(slug))
    if rate is not None:
        want = ("%d" % rate) if float(rate).is_integer() else ("%.1f" % rate).replace(".", ",")
        m = ITP_QA.search(txt)
        if m and m.group(1) != want:
            fallos.append(f"ITP {m.group(1)}% != {want}%")
        md = ITP_DESC_QA.search(txt)
        if md:
            piso, imp = int(md.group(1).replace(".", "")), int(md.group(2).replace(".", ""))
            if piso % int(c["p"]) != 0:
                fallos.append(f"ITP piso {piso}€ no es múltiplo del precio {int(c['p'])}€/m²")
            elif abs(imp - piso * rate / 100) > 1:
                fallos.append(f"ITP importe {imp}€ != {rate}% de {piso}€")
    if fallos:
        (evo_frozen if p in _frozen_names else evo_dev).append((p, "; ".join(fallos[:3])))
    else:
        evo_ok += 1
if evo_frozen:
    warnings.append(f"[14] {len(evo_frozen)} fichas CONGELADAS con serie/ITP incoherente "
                    f"(ver PENDIENTES_DESCONGELACION.md): {[f for f, _ in evo_frozen]}")
if evo_dev:
    errors.append(f"[14] {len(evo_dev)} fichas con la serie histórica o la tarjeta ITP "
                  f"incoherentes: {evo_dev[:5]}")
else:
    print(f"[14] Serie histórica (acaba en DATA[] p, dirección == vp) e ITP por CCAA: "
          f"OK ({evo_ok} fichas)")

# --- Check 15: URLs duplicadas (.html vs limpia) ---
# Workers Assets sirve cada `x.html` en DOS rutas (`/x.html` y `/x`) y para la
# variante `.html` emite un 307 temporal: Google acaba indexando las dos y parte
# las señales entre ellas (16 pares con impresiones en Search Console el
# 2026-08-01, pero afectaba a las 843 paginas). El arreglo es un 301 explicito
# por pagina en _redirects, generado por scripts/gen_redirects.py. Este check
# vigila que no se cuele una pagina nueva sin su 301, ni un canonical que
# apunte a la variante .html, ni un rewrite 200 que sirva lo mismo en otra ruta.
dup_errs, dup_warns = [], []
CLEAN_EXCLUDE = {"404.html"}          # noindex, la sirve Cloudflare como error

def clean_url(page):
    if page == "index.html":
        return "/"
    if page.endswith("/index.html"):
        return "/" + page[:-len("/index.html")] + "/"
    return "/" + page[:-len(".html")]

red_file = os.path.join(SITE, "_redirects")
if not os.path.exists(red_file):
    dup_errs.append("no existe _redirects")
    red_rules = []
else:
    red_rules = []
    for ln in open(red_file, encoding="utf-8").read().splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        f = s.split()
        if len(f) >= 2:
            red_rules.append((f[0], f[1], f[2] if len(f) > 2 else "302"))

# 15a. toda pagina servible tiene su 301 .html -> limpia
red_301 = {src: dst for src, dst, code in red_rules if code == "301"}
sin_301, mal_destino = [], []
for p in pages:
    if p in CLEAN_EXCLUDE:
        continue
    src = "/" + p
    if src not in red_301:
        sin_301.append(p)
    elif red_301[src] != clean_url(p):
        mal_destino.append((p, red_301[src], clean_url(p)))
if sin_301:
    dup_errs.append(f"{len(sin_301)} paginas servidas en /x.html y /x sin 301 "
                    f"(ejecuta scripts/gen_redirects.py): {sin_301[:6]}")
if mal_destino:
    dup_errs.append(f"{len(mal_destino)} 301 que no apuntan a la URL limpia: {mal_destino[:6]}")

# 15b. reglas huerfanas: origen .html que ya no existe -> 301 a un 404
huerfanas = [src for src in red_301
             if src.endswith(".html") and src.lstrip("/") not in pageset]
if huerfanas:
    dup_errs.append(f"{len(huerfanas)} reglas 301 desde un .html inexistente: {huerfanas[:6]}")

# 15c. rewrites 200: sirven la misma pagina en una segunda ruta sin redirigir
rewrites = [(src, dst) for src, dst, code in red_rules if code == "200"]
if rewrites:
    dup_errs.append(f"{len(rewrites)} rewrites 200 sirven contenido en una ruta "
                    f"alternativa (usa 301): {rewrites[:6]}")

# 15d. el canonical de cada pagina es SU url limpia (el [4] solo mira el dominio)
canon_dup = []
for p in pages:
    if p == "404.html":
        continue
    txt = open(os.path.join(SITE, p), encoding="utf-8", errors="ignore").read()
    cans = re.findall(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', txt, re.I)
    if len(cans) != 1:
        continue                       # ya lo reporta el check [4]
    want = "https://rendata.es" + clean_url(p)
    if cans[0] != want:
        canon_dup.append((p, cans[0], want))
if canon_dup:
    dup_errs.append(f"{len(canon_dup)} canonical que no apuntan a la URL limpia "
                    f"de su propia pagina: {canon_dup[:6]}")

# 15e. el sitemap solo lista la version canonica, sin .html ni repetidos
sitemap_file = os.path.join(SITE, "sitemap.xml")
if os.path.exists(sitemap_file):
    sm_locs = re.findall(r"<loc>\s*(.*?)\s*</loc>",
                         open(sitemap_file, encoding="utf-8").read())
    con_html = [l for l in sm_locs if l.endswith(".html")]
    sm_paths = [re.sub(r"^https?://[^/]+", "", l) or "/" for l in sm_locs]
    repetidos = sorted({x for x in sm_paths if sm_paths.count(x) > 1})
    if con_html:
        dup_errs.append(f"{len(con_html)} URLs .html en sitemap.xml: {con_html[:6]}")
    if repetidos:
        dup_errs.append(f"{len(repetidos)} URLs repetidas en sitemap.xml: {repetidos[:6]}")
    fuera = sorted({clean_url(p) for p in pages if p not in CLEAN_EXCLUDE} - set(sm_paths))
    if fuera:
        dup_warns.append(f"[15] {len(fuera)} paginas fuera del sitemap "
                         f"(intencionado si son noindex): {fuera[:8]}")

warnings.extend(dup_warns)
if dup_errs:
    errors.append("[15] URLs duplicadas: " + " | ".join(dup_errs))
else:
    print(f"[15] URLs duplicadas (.html vs limpia): OK "
          f"({len(pages) - len(CLEAN_EXCLUDE)} paginas con 301, canonical y sitemap limpios)")

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
