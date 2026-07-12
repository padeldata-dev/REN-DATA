"""
Unifica la superficie de cálculo del ROI a 100m² en todo el sitio.
- DATA[] de index.html: recalcula roi = (alq*12)/(p*100)*100
- Cada ficha: actualiza sticky-bar, ed-highlight, meta tags, FAQ JSON-LD
- Reemplaza menciones "Un piso de 70 m² costaría XXX€" → 100 m² con precio coherente
"""
import re, sys, glob
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"
INDEX = ROOT / "index.html"
SUP = 100  # doctrina oficial

# ============ HELPERS ============

def fmt_es(roi):
    return f"{roi:.1f}".replace(".", ",")

def fmt_num(v):
    return f"{v:,}".replace(",", ".") if v >= 1000 else str(v)

def calc_roi(p, alq, sup=SUP):
    return round(alq * 12 / (p * sup) * 1000) / 10

# ============ 1. RECALCULAR DATA[] ============

content = INDEX.read_text(encoding="utf-8")
m = re.search(r'(const DATA=\[\n)(.*?)(\n\];)', content, re.DOTALL)
prefix, block, suffix = m.group(1), m.group(2), m.group(3)

city_changes = {}  # sl -> (old_roi, new_roi, p, alq)
new_lines = []
for line in block.split("\n"):
    sline = line.strip().rstrip(",")
    if not sline.startswith("{"):
        new_lines.append(line); continue
    p_m = re.search(r'p:(\d+)', line)
    alq_m = re.search(r'alq:(\d+)', line)
    roi_m = re.search(r'roi:([\d.]+)', line)
    sl_m = re.search(r'sl:"([^"]+)"', line)
    if not all([p_m, alq_m, roi_m, sl_m]):
        new_lines.append(line); continue
    p = int(p_m.group(1)); alq = int(alq_m.group(1))
    old_roi = float(roi_m.group(1))
    new_roi = calc_roi(p, alq)
    sl = sl_m.group(1)
    if abs(new_roi - old_roi) >= 0.05:
        city_changes[sl] = (old_roi, new_roi, p, alq)
        new_line = re.sub(r'(roi:)[\d.]+', f"roi:{new_roi}", line, count=1)
        new_lines.append(new_line)
    else:
        # Marcar para actualizar también las fichas, aunque DATA no cambie
        city_changes[sl] = (old_roi, old_roi, p, alq)
        new_lines.append(line)

new_block = "\n".join(new_lines)
new_content = content[:m.start()] + prefix + new_block + suffix + content[m.end():]
INDEX.write_text(new_content, encoding="utf-8")

n_changed = sum(1 for v in city_changes.values() if abs(v[1]-v[0]) >= 0.05)
print(f"[1] DATA[] procesado: {len(city_changes)} ciudades | ROIs cambiados: {n_changed}")

# ============ 2. ACTUALIZAR CADA FICHA ============

n_files = 0; n_total_changes = 0
for sl, (old_roi, new_roi, p, alq) in city_changes.items():
    fp = ROOT / f"rentabilidad-{sl}.html"
    if not fp.exists(): continue
    h = fp.read_text(encoding="utf-8")
    h0 = h
    old_es = fmt_es(old_roi)
    new_es = fmt_es(new_roi)
    new_neto = round(new_roi * 0.75 * 10) / 10
    new_neto_es = fmt_es(new_neto)
    p_total_100 = p * SUP  # precio total a 100m²

    # 2.1) Si el ROI cambió, actualizar:
    if abs(new_roi - old_roi) >= 0.05:
        # Sticky-bar ROI bruto
        h = re.sub(
            r'(<span class="sb-label">ROI bruto</span><span class="sb-val[^>]*>)' + re.escape(old_es) + r'%(</span>)',
            lambda m_: f"{m_.group(1)}{new_es}%{m_.group(2)}", h, count=1)
        # Sticky-bar ROI neto
        h = re.sub(
            r'(<span class="sb-label">ROI neto</span><span class="sb-val[^>]*>)([\d,]+)%(</span>)',
            lambda m_: f"{m_.group(1)}{new_neto_es}%{m_.group(3)}", h, count=1)
        # ed-highlight rentabilidad bruta
        h = re.sub(
            r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(old_es) + r'(%</div><div class="ed-stat-lbl">rentabilidad bruta</div></div>)',
            lambda m_: f"{m_.group(1)}{new_es}{m_.group(2)}", h, count=1)
        # Meta title, og:title (formato ROI X,X% / Rentabilidad X,X%)
        h = re.sub(r'(ROI )' + re.escape(old_es) + r'%', lambda m_: f"{m_.group(1)}{new_es}%", h)
        h = re.sub(r'(Rentabilidad )' + re.escape(old_es) + r'%', lambda m_: f"{m_.group(1)}{new_es}%", h)
        # ROI estimado X,X% en descripciones
        h = re.sub(r'(ROI estimado )' + re.escape(old_es) + r'%', lambda m_: f"{m_.group(1)}{new_es}%", h)
        # JSON-LD FAQ: "rentabilidad bruta estimada del alquiler en X en 2026 se sitúa en el 6.3%."
        # Acepta formato con punto o coma decimal
        for txt_old in [old_es, old_es.replace(",", ".")]:
            h = re.sub(r'(se\s+sit[uú]a\s+en\s+el\s+)' + re.escape(txt_old) + r'%',
                       lambda m_, ne=new_es: f"{m_.group(1)}{ne}%", h)
        # ROI X.X% (formato anglo) en JSON-LD
        h = re.sub(r'(\bROI\b\s+(?:bruto\s+)?(?:del\s+)?)' + re.escape(old_es.replace(",", ".")) + r'%',
                   lambda m_: f"{m_.group(1)}{new_es.replace(',', '.')}%", h)

    # 2.2) Reemplazar SIEMPRE "Un piso de 70 m² costaría XXX€" → "Un piso de 100 m² costaría {p*100}€"
    h = re.sub(
        r'(Un piso de )(\d+)(\s*m[²2]?\s*costar[íi]a\s+aproximadamente\s+)([\d.]+)(€)',
        lambda m_: f"{m_.group(1)}{SUP}{m_.group(3)}{fmt_num(p_total_100)}{m_.group(5)}", h)

    if h != h0:
        fp.write_text(h, encoding="utf-8")
        n_files += 1
        n_total_changes += 1

print(f"[2] Fichas actualizadas: {n_files}/{len(city_changes)}")

# ============ 3. VERIFICACIÓN ============
# Recontar ROIs implícitos en DATA[] tras la unificación
content_final = INDEX.read_text(encoding="utf-8")
m = re.search(r'const DATA=\[\n(.*?)\n\];', content_final, re.DOTALL)
block_final = m.group(1)
buckets = {}
for line in block_final.split("\n"):
    sline = line.strip().rstrip(",")
    if not sline.startswith("{"): continue
    p = int(re.search(r'p:(\d+)', line).group(1))
    alq = int(re.search(r'alq:(\d+)', line).group(1))
    roi = float(re.search(r'roi:([\d.]+)', line).group(1))
    sup = (alq * 12) / (p * roi / 100)
    s = round(sup)
    buckets[s] = buckets.get(s, 0) + 1

print("\n[3] Distribución de superficies implícitas tras unificación:")
for s in sorted(buckets):
    print(f"   {s} m²: {buckets[s]} ciudades")
