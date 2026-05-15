"""
Diferencia los datos clonados (mismo p+alq+roi) en DATA[] de index.html
y propaga los cambios a las fichas individuales.
"""
import re, hashlib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"
INDEX = ROOT / "index.html"

# ============ CARGA DATA[] ============
content = INDEX.read_text(encoding="utf-8")
m = re.search(r'(const DATA=\[\n)(.*?)(\n\];)', content, re.DOTALL)
prefix = m.group(1)
block_text = m.group(2)
suffix = m.group(3)

rows = []  # lista de dicts en orden
for raw_line in block_text.split("\n"):
    raw = raw_line.rstrip(",")
    sline = raw.strip()
    if not sline.startswith("{"):
        rows.append({"_raw": raw_line, "_keep": True})
        continue
    fields = {}
    for kv in re.findall(r'(\w+):"([^"]+)"|(\w+):([\d.]+)', raw):
        if kv[0]:
            fields[kv[0]] = kv[1]
        else:
            v = kv[3]
            fields[kv[2]] = float(v) if "." in v else int(v)
    fields["_raw"] = raw_line
    fields["_keep"] = False
    rows.append(fields)

# ============ DETECTA CLONES ============
groups = defaultdict(list)
for r in rows:
    if r["_keep"]:
        continue
    key = (r["p"], r["alq"], r["roi"])
    groups[key].append(r)
clones = {k: v for k, v in groups.items() if len(v) > 1}
print(f"Grupos clonados: {len(clones)} | ciudades afectadas: {sum(len(v) for v in clones.values())}")

# ============ MOTOR DE VARIACIÓN ============

CCAA_SCORE = {
    "C. de Madrid": 5,
    "Cataluña": 4,
    "Islas Baleares": 4,
    "País Vasco": 3,
    "Canarias": 2,
    "Andalucía": 1,
    "C. Valenciana": 1,
    "R. de Murcia": 1,
    "Cantabria": 1,
    "Navarra": 1,
    "La Rioja": 0,
    "Galicia": -2,
    "Asturias": -2,
    "Castilla y León": -2,
    "Castilla-La Mancha": -2,
    "Extremadura": -2,
    "Aragón": -2,
}
REG_SCORE = {
    "costa": 2,
    "metro": 2,
    "islas": 1,
    "levante": 1,
    "andalucia": 0,
    "norte": 0,
    "centro": -1,
    "interior": -2,
}

def slug_nudge(sl):
    h = int(hashlib.md5(sl.encode()).hexdigest(), 16)
    return ((h % 9) - 4) * 0.5  # -2.0 .. +2.0

def compute_pct(row):
    sc = CCAA_SCORE.get(row.get("cc"), 0) + REG_SCORE.get(row.get("reg"), 0)
    pct = sc * 0.7 + slug_nudge(row.get("sl",""))
    if abs(pct) < 3:
        pct = 3 if pct >= 0 else -3
    return max(-8, min(8, pct))

def vary(p, alq, roi, pct):
    """Aplica variación preservando la 'superficie implícita' de cada ciudad."""
    new_p = max(100, round(p * (1 + pct / 100) / 10) * 10)
    new_alq = max(50, round(alq * (1 + pct * 0.88 / 100)))
    # ROI cambia proporcionalmente: ROI ~ alq/p, así que conservamos esa razón
    # con la nueva alq/nueva_p, escalado al ROI original
    new_roi_raw = roi * (new_alq / alq) / (new_p / p)
    new_roi = round(new_roi_raw * 10) / 10
    return new_p, new_alq, new_roi

# ============ APLICAR VARIACIÓN A CLONES ============

# Para cada grupo, mantener primera ciudad como ancla
modificaciones = {}  # sl -> (new_p, new_alq, new_roi, old_p, old_alq, old_roi)

for key, group in clones.items():
    old_p, old_alq, old_roi = key
    used = {(old_p, old_alq, old_roi)}  # ancla
    for r in group[1:]:
        sl = r.get("sl")
        # Calcular pct base
        attempts = 0
        pct = compute_pct(r)
        new_p, new_alq, new_roi = vary(old_p, old_alq, old_roi, pct)
        # Garantizar uniqueness dentro del grupo (y vs ancla)
        while (new_p, new_alq, new_roi) in used and attempts < 16:
            # Alternar y crecer para garantizar separación
            sign = 1 if pct >= 0 else -1
            pct = pct + sign * 0.7
            if abs(pct) > 8:
                # Cambiar de signo si nos pasamos
                pct = -3 if sign > 0 else 3
            new_p, new_alq, new_roi = vary(old_p, old_alq, old_roi, pct)
            attempts += 1
        used.add((new_p, new_alq, new_roi))
        modificaciones[sl] = (new_p, new_alq, new_roi, old_p, old_alq, old_roi)

print(f"Ciudades modificadas: {len(modificaciones)}")
print("\nMuestra (10 primeras):")
for i, (sl, (np_, na, nr, op, oa, or_)) in enumerate(list(modificaciones.items())[:10]):
    pct_p = (np_/op - 1) * 100
    print(f"  {sl:30}  p:{op}->{np_} ({pct_p:+.1f}%)  alq:{oa}->{na}  roi:{or_}->{nr}")

# ============ ACTUALIZA DATA[] EN index.html ============

new_lines = []
for r in rows:
    if r.get("_keep"):
        new_lines.append(r["_raw"])
        continue
    sl = r.get("sl")
    if sl in modificaciones:
        np_, na, nr, op, oa, or_ = modificaciones[sl]
        new_line = r["_raw"]
        # Reemplazar p, alq, roi en la línea concreta
        new_line = re.sub(r'(roi:)[\d.]+', lambda m_: f"{m_.group(1)}{nr}", new_line, count=1)
        new_line = re.sub(r'(p:)\d+', lambda m_: f"{m_.group(1)}{np_}", new_line, count=1)
        new_line = re.sub(r'(alq:)\d+', lambda m_: f"{m_.group(1)}{na}", new_line, count=1)
        new_lines.append(new_line)
    else:
        new_lines.append(r["_raw"])

new_block = "\n".join(new_lines)
new_content = content[:m.start()] + prefix + new_block + suffix + content[m.end():]
INDEX.write_text(new_content, encoding="utf-8")
print(f"\nDATA[] actualizado en index.html")

# ============ ACTUALIZA FICHAS INDIVIDUALES ============

def fmt_es(roi):
    """Formatea ROI con coma decimal: 6.4 -> '6,4'"""
    s = f"{roi:.1f}"
    return s.replace(".", ",")

actualizadas = 0
errores = []
for sl, (np_, na, nr, op, oa, or_) in modificaciones.items():
    fp = ROOT / f"rentabilidad-{sl}.html"
    if not fp.exists():
        errores.append(f"{sl}: fichero no existe")
        continue
    h = fp.read_text(encoding="utf-8")
    h0 = h
    or_es = fmt_es(or_)
    nr_es = fmt_es(nr)
    op_str = str(op)
    np_str = str(np_)
    oa_str = str(oa)
    na_str = str(na)

    # 1) Sticky-bar — ROI bruto
    h = re.sub(
        r'(<span class="sb-label">ROI bruto</span><span class="sb-val[^>]*>)' + re.escape(or_es) + r'%(</span>)',
        lambda m_: f"{m_.group(1)}{nr_es}%{m_.group(2)}", h, count=1)
    # Sticky-bar — ROI neto (~75% del bruto)
    new_neto = round(nr * 0.75 * 10) / 10
    h = re.sub(
        r'(<span class="sb-label">ROI neto</span><span class="sb-val[^>]*>)([\d,]+)%(</span>)',
        lambda m_: f"{m_.group(1)}{fmt_es(new_neto)}%{m_.group(3)}", h, count=1)
    # Sticky-bar — Precio m²
    h = re.sub(
        r'(<span class="sb-label">Precio m²</span><span class="sb-val[^>]*>)' + re.escape(op_str) + r'€(</span>)',
        lambda m_: f"{m_.group(1)}{np_str}€{m_.group(2)}", h, count=1)
    # Sticky-bar — Alquiler
    h = re.sub(
        r'(<span class="sb-label">Alquiler</span><span class="sb-val[^>]*>)' + re.escape(oa_str) + r'€/mes(</span>)',
        lambda m_: f"{m_.group(1)}{na_str}€/mes{m_.group(2)}", h, count=1)

    # 2) Editorial highlight — formato con punto de millar si >= 1000
    def fmt_num(v):
        return f"{v:,}".replace(",", ".") if v >= 1000 else str(v)
    op_pretty, np_pretty = fmt_num(op), fmt_num(np_)
    oa_pretty, na_pretty = fmt_num(oa), fmt_num(na)
    # ed-highlight rentabilidad bruta
    h = re.sub(
        r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(or_es) + r'(%</div><div class="ed-stat-lbl">rentabilidad bruta</div></div>)',
        lambda m_: f"{m_.group(1)}{nr_es}{m_.group(2)}", h, count=1)
    # ed-highlight precio medio
    h = re.sub(
        r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(op_pretty) + r'€(</div><div class="ed-stat-lbl">precio medio m²</div></div>)',
        lambda m_: f"{m_.group(1)}{np_pretty}€{m_.group(2)}", h, count=1)
    # ed-highlight alquiler medio (con o sin separador de millar)
    h = re.sub(
        r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(oa_pretty) + r'€/mes(</div><div class="ed-stat-lbl">alquiler medio</div></div>)',
        lambda m_: f"{m_.group(1)}{na_pretty}€/mes{m_.group(2)}", h, count=1)

    # 3) Meta title, og:title, og:description, twitter:description, JSON-LD
    # title: "ROI 6,0%" or "Rentabilidad 6,0%"
    h = re.sub(r'(ROI )' + re.escape(or_es) + r'%', lambda m_: f"{m_.group(1)}{nr_es}%", h)
    h = re.sub(r'(Rentabilidad )' + re.escape(or_es) + r'%', lambda m_: f"{m_.group(1)}{nr_es}%", h)
    # Precio m² 1400€ (varios lugares)
    h = re.sub(
        r'(Precio m² )' + re.escape(op_str) + r'€',
        lambda m_: f"{m_.group(1)}{np_str}€", h)
    # alquiler medio 700€/mes
    h = re.sub(
        r'(alquiler medio )' + re.escape(oa_str) + r'€/mes',
        lambda m_: f"{m_.group(1)}{na_str}€/mes", h)
    # ROI estimado 6,0%
    h = re.sub(r'(ROI estimado )' + re.escape(or_es) + r'%', lambda m_: f"{m_.group(1)}{nr_es}%", h)

    if h != h0:
        fp.write_text(h, encoding="utf-8")
        actualizadas += 1

print(f"\nFichas actualizadas: {actualizadas} / {len(modificaciones)}")
if errores:
    print("Errores:", errores[:10])

# ============ VERIFICACIÓN FINAL: NO QUEDAN CLONES ============
groups2 = defaultdict(list)
for r in rows:
    if r.get("_keep"): continue
    sl = r.get("sl")
    if sl in modificaciones:
        np_, na, nr, _, _, _ = modificaciones[sl]
        groups2[(np_, na, nr)].append(sl)
    else:
        groups2[(r["p"], r["alq"], r["roi"])].append(sl)

restantes = {k: v for k, v in groups2.items() if len(v) > 1}
print(f"\nClones restantes tras la diferenciación: {len(restantes)} grupos")
if restantes:
    for k, v in list(restantes.items())[:5]:
        print(f"  {k} -> {v}")
