"""
Updater: aplica el dataset agregado a:
- DATA[] en rendata_beta/index.html
- sticky-bar y ed-highlight de cada rentabilidad-{slug}.html
- meta tags y FAQ JSON-LD

Reutiliza los patrones de los scripts/differentiate_clones.py y
scripts/unify_surface_100m2.py.
"""
import re
from pathlib import Path
from .config import RENDATA_DIR, SUP_M2

INDEX = RENDATA_DIR / "index.html"

def fmt_es(v):
    return f"{v:.1f}".replace(".", ",") if isinstance(v, float) else str(v)

def fmt_num(v):
    if v is None: return ""
    return f"{int(v):,}".replace(",", ".") if v >= 1000 else str(int(v))

def update_index_data(rows: list):
    """Reescribe DATA[] en index.html con los nuevos valores."""
    content = INDEX.read_text(encoding="utf-8")
    m = re.search(r'(const DATA=\[\n)(.*?)(\n\];)', content, re.DOTALL)
    if not m:
        print("[UPD] DATA[] no encontrado en index.html")
        return 0
    by_slug = {r["slug"]: r for r in rows}
    block = m.group(2)
    new_lines, n_changed = [], 0
    for line in block.split("\n"):
        sl = line.strip().rstrip(",")
        if not sl.startswith("{"):
            new_lines.append(line); continue
        slm = re.search(r'sl:"([^"]+)"', line)
        if not slm or slm.group(1) not in by_slug:
            new_lines.append(line); continue
        r = by_slug[slm.group(1)]
        new_line = line
        if r.get("precio_m2"):
            new_line = re.sub(r'(p:)\d+', f'p:{int(r["precio_m2"])}', new_line, count=1)
        if r.get("alquiler_medio"):
            new_line = re.sub(r'(alq:)\d+', f'alq:{int(r["alquiler_medio"])}', new_line, count=1)
        if r.get("roi"):
            new_line = re.sub(r'(roi:)[\d.]+', f'roi:{r["roi"]}', new_line, count=1)
        if r.get("var_precio_anual") is not None:
            new_line = re.sub(r'(vp:)[\d.\-]+', f'vp:{r["var_precio_anual"]}', new_line, count=1)
        if r.get("var_alquiler_anual") is not None:
            new_line = re.sub(r'(va:)[\d.\-]+', f'va:{r["var_alquiler_anual"]}', new_line, count=1)
        if new_line != line: n_changed += 1
        new_lines.append(new_line)
    new_block = "\n".join(new_lines)
    new_content = content[:m.start()] + m.group(1) + new_block + m.group(3) + content[m.end():]
    INDEX.write_text(new_content, encoding="utf-8")
    print(f"[UPD] DATA[] actualizado: {n_changed} entries")
    return n_changed

def update_ficha(slug: str, r: dict, old_p: int, old_a: int, old_roi: float) -> bool:
    """Actualiza una ficha individual. Devuelve True si cambió."""
    fp = RENDATA_DIR / f"rentabilidad-{slug}.html"
    if not fp.exists(): return False
    h = fp.read_text(encoding="utf-8")
    h0 = h
    new_p, new_a, new_roi = r.get("precio_m2"), r.get("alquiler_medio"), r.get("roi")
    if not (new_p and new_a and new_roi): return False

    old_p_str = str(old_p); new_p_str = str(int(new_p))
    old_a_str = str(old_a); new_a_str = str(int(new_a))
    old_roi_es = fmt_es(old_roi); new_roi_es = fmt_es(new_roi)
    new_neto = round(new_roi * 0.75 * 10) / 10
    new_neto_es = fmt_es(new_neto)

    # Sticky-bar
    h = re.sub(r'(<span class="sb-label">ROI bruto</span><span class="sb-val[^>]*>)' + re.escape(old_roi_es) + r'%(</span>)',
               lambda m: f'{m.group(1)}{new_roi_es}%{m.group(2)}', h, count=1)
    h = re.sub(r'(<span class="sb-label">ROI neto</span><span class="sb-val[^>]*>)([\d,]+)%(</span>)',
               lambda m: f'{m.group(1)}{new_neto_es}%{m.group(3)}', h, count=1)
    h = re.sub(r'(<span class="sb-label">Precio m²</span><span class="sb-val[^>]*>)' + re.escape(old_p_str) + r'€(</span>)',
               lambda m: f'{m.group(1)}{new_p_str}€{m.group(2)}', h, count=1)
    h = re.sub(r'(<span class="sb-label">Alquiler</span><span class="sb-val[^>]*>)' + re.escape(old_a_str) + r'€/mes(</span>)',
               lambda m: f'{m.group(1)}{new_a_str}€/mes{m.group(2)}', h, count=1)

    # ed-highlight
    op_p = fmt_num(old_p); np_p = fmt_num(new_p)
    oa_p = fmt_num(old_a); na_p = fmt_num(new_a)
    h = re.sub(r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(old_roi_es) + r'(%</div><div class="ed-stat-lbl">rentabilidad bruta</div></div>)',
               lambda m: f'{m.group(1)}{new_roi_es}{m.group(2)}', h, count=1)
    h = re.sub(r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(op_p) + r'€(</div><div class="ed-stat-lbl">precio medio m²</div></div>)',
               lambda m: f'{m.group(1)}{np_p}€{m.group(2)}', h, count=1)
    h = re.sub(r'(<div class="ed-stat"><div class="ed-stat-val">)' + re.escape(oa_p) + r'€/mes(</div><div class="ed-stat-lbl">alquiler medio</div></div>)',
               lambda m: f'{m.group(1)}{na_p}€/mes{m.group(2)}', h, count=1)

    # Meta tags y FAQ
    h = re.sub(r'(ROI )' + re.escape(old_roi_es) + r'%', lambda m: f'{m.group(1)}{new_roi_es}%', h)
    h = re.sub(r'(Rentabilidad )' + re.escape(old_roi_es) + r'%', lambda m: f'{m.group(1)}{new_roi_es}%', h)
    h = re.sub(r'(ROI estimado )' + re.escape(old_roi_es) + r'%', lambda m: f'{m.group(1)}{new_roi_es}%', h)
    h = re.sub(r'(Precio m² )' + re.escape(old_p_str) + r'€', lambda m: f'{m.group(1)}{new_p_str}€', h)
    h = re.sub(r'(alquiler medio )' + re.escape(old_a_str) + r'€/mes', lambda m: f'{m.group(1)}{new_a_str}€/mes', h)
    # FAQ "piso de 100m² costaría XXX€"
    h = re.sub(r'(piso de )100(\s*m[²2]?\s*costar[íi]a\s+aproximadamente\s+)[\d.]+(€)',
               lambda m: f'{m.group(1)}100{m.group(2)}{fmt_num(new_p * SUP_M2)}{m.group(3)}', h)
    # JSON-LD "se sitúa en el X.X%"
    for txt in (old_roi_es, old_roi_es.replace(",", ".")):
        h = re.sub(r'(se\s+sit[uú]a\s+en\s+el\s+)' + re.escape(txt) + r'%',
                   lambda m: f'{m.group(1)}{new_roi_es}%', h)

    if h != h0:
        fp.write_text(h, encoding="utf-8")
        return True
    return False

def update_fichas(rows: list, master: list) -> int:
    """Actualiza todas las fichas. master = lista anterior con valores 'previos'."""
    by_slug_master = {m["slug"]: m for m in master}
    n_updated = 0
    for r in rows:
        old = by_slug_master.get(r["slug"])
        if not old: continue
        if update_ficha(r["slug"], r,
                        int(old.get("precio_actual") or 0),
                        int(old.get("alquiler_actual") or 0),
                        float(old.get("roi_actual") or 0)):
            n_updated += 1
    print(f"[UPD] Fichas actualizadas: {n_updated}/{len(rows)}")
    return n_updated

def update_master(rows: list):
    """Reescribe cities_master.csv con los valores nuevos como 'actuales'."""
    from .cities import save_cities
    new_master = []
    for r in rows:
        new_master.append({
            "slug": r["slug"], "nombre": r["nombre"], "ccaa": r["ccaa"],
            "reg": "",  # se conserva si quieres
            "precio_actual": r.get("precio_m2") or "",
            "alquiler_actual": r.get("alquiler_medio") or "",
            "roi_actual": r.get("roi") or "",
            "var_precio_anual": r.get("var_precio_anual") or "",
            "var_alquiler_anual": r.get("var_alquiler_anual") or "",
            "dias_mercado": r.get("dias_mercado") or "",
            "ine_code": "",
        })
    save_cities(new_master)
    print(f"[UPD] cities_master.csv actualizado")
