"""
FASE 2 — Bloque '¿Puedo permitirme comprar en {ciudad}?' para las 587 fichas.

Datos reales utilizados:
  - precio_m2, alquiler_medio: data/processed/cities_2026Q2.csv (fuente original
    de la ficha, idéntico al sticky bar).
  - salario_medio_anual: extraído de la propia ficha
    (<div class="demo-val">X€</div><div class="demo-label">Salario medio anual</div>)
    fuente AEAT 2024.

Cálculos:
  - Años de sueldo necesarios = precio_piso_100m² / salario_anual_bruto
  - Esfuerzo % = cuota_mensual / (salario_anual × 0,80 / 12) × 100
      cuota_mensual: hipoteca 80% LTV, 3,2% TAE, 25 años sobre piso de 100 m²
      0,80: factor neto/bruto aproximado (IRPF medio para rentas 20-30k)
  - Punto de equilibrio (price-to-rent) = precio_piso_100m² / (alquiler × 12)

Comparativa nacional: media simple de los 587 valores (no ponderada por población,
para reflejar 'la ciudad mediana' y no estar dominada por Madrid+Barcelona).

'Estimado provincial': si un valor de salario aparece en ≥4 fichas distintas,
se asume fallback provincial y se etiqueta en la nota de fuente.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT        = Path(__file__).resolve().parents[1]
FICHAS_DIR  = ROOT / "rendata_beta"
CSV_PATH    = ROOT / "data" / "processed" / "cities_2026Q2.csv"

# ---------- Regex --------------------------------------------------------

RE_CITY       = re.compile(r'<div class="banner-title">([^<]+)</div>')
RE_SALARIO    = re.compile(
    r'<div class="demo-val">([\d.]+)€</div>\s*'
    r'<div class="demo-label">Salario medio anual</div>'
)
RE_PRECIO_M2  = re.compile(
    r'<span class="sb-label">Precio m²</span><span class="sb-val">([\d.,]+)€</span>'
)
RE_ALQUILER   = re.compile(
    r'<span class="sb-label">Alquiler</span><span class="sb-val">([\d.,]+)€/mes</span>'
)
# anchor where we insert the new block: just before the CASOS DE USO section
RE_INSERT_ANCHOR = re.compile(r'(\s*<!-- CASOS DE USO -->)')

# detect already-inserted block
HAS_BLOCK_TOKEN = 'id="afford"'


# ---------- Helpers ------------------------------------------------------

def euro(n: float) -> str:
    return f"{int(round(n)):,}".replace(",", ".")


def numparse(s: str) -> float:
    """Parse '21.200' or '5.960' or '21200' as Spanish-formatted int."""
    return float(s.replace(".", "").replace(",", "."))


def cuota_hipoteca(precio: float, ltv: float = 0.80,
                   tipo: float = 0.032, plazo_anios: int = 25) -> float:
    capital = precio * ltv
    r = tipo / 12.0
    n = plazo_anios * 12
    return capital * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


# ---------- Per-metric thresholds + verdict ------------------------------

def color_anos(v: float) -> str:
    if v < 8:  return "var(--green)"
    if v < 12: return "#d97706"  # ámbar
    return "var(--red)"


def color_esfuerzo(v: float) -> str:
    if v < 30:  return "var(--green)"
    if v < 40:  return "#d97706"
    return "var(--red)"


def color_prr(v: float) -> str:
    if v < 15:  return "var(--green)"   # comprar
    if v <= 20: return "#d97706"        # equilibrio
    return "var(--red)"                 # alquilar


def vs_nat(v: float, nat: float, lower_is_better: bool = True) -> tuple[str, str]:
    diff = v - nat
    pct = (diff / nat * 100) if nat else 0
    if abs(pct) < 5:
        return "eq", f"≈ media España ({nat:.1f})"
    favourable = (lower_is_better and diff < 0) or (not lower_is_better and diff > 0)
    cls = "up" if favourable else "down"
    arrow = "↓" if diff < 0 else "↑"
    return cls, f"{arrow} {abs(pct):.0f}% vs media España ({nat:.1f})"


def overall_verdict(anos: float, esfuerzo: float, prr: float) -> tuple[str, str, str, str]:
    """Return (verdict_class, icon, title, text)."""
    n_ok = sum([anos < 8, esfuerzo < 30, prr < 15])
    n_bad = sum([anos >= 12, esfuerzo >= 40, prr > 20])
    if n_bad >= 2:
        return ("bad", "🚧",
                "Compra exigente",
                "Los tres indicadores señalan tensión: alto precio/salario, esfuerzo "
                "elevado y price-to-rent por encima del rango de equilibrio. "
                "Recomendado revisar plazos, entrada mayor o alquilar.")
    if n_ok >= 2:
        return ("ok", "✅",
                "Mercado accesible",
                "Al menos dos de los tres indicadores están en zona favorable. "
                "Buen punto de partida para comprador con financiación cerrada.")
    return ("warn", "⚖️",
            "Zona de equilibrio",
            "Indicadores mixtos: la compra es viable pero requiere ajustar plazo, "
            "entrada o presupuesto. Compara con la calculadora de hipoteca de "
            "esta misma página.")


# ---------- Precompute ---------------------------------------------------

def load_csv() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with CSV_PATH.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                out[row["slug"]] = {
                    "ccaa":      row["ccaa"],
                    "precio_m2": float(row["precio_m2"]),
                    "alquiler":  float(row["alquiler_medio"]),
                    "poblacion": int(row["poblacion"]),
                }
            except (ValueError, KeyError):
                pass
    return out


def precompute(threshold_shared: int = 4) -> dict:
    """Extract per-ficha data directly from HTML (CSV doesn't cover all 587)."""
    csv_data = load_csv()  # used only for ccaa/poblacion enrichment when present
    ficha_data: dict[str, dict] = {}

    for path in sorted(FICHAS_DIR.glob("rentabilidad-*.html")):
        slug = path.stem.removeprefix("rentabilidad-")
        html = path.read_text(encoding="utf-8")
        m_city = RE_CITY.search(html)
        m_sal  = RE_SALARIO.search(html)
        m_p    = RE_PRECIO_M2.search(html)
        m_a    = RE_ALQUILER.search(html)
        if not (m_city and m_sal and m_p and m_a):
            continue
        ccaa_pob = csv_data.get(slug, {})
        ficha_data[slug] = {
            "city":      m_city.group(1).strip(),
            "salary":    numparse(m_sal.group(1)),
            "precio_m2": numparse(m_p.group(1)),
            "alquiler":  numparse(m_a.group(1)),
            "ccaa":      ccaa_pob.get("ccaa", ""),
            "poblacion": ccaa_pob.get("poblacion", 0),
        }

    # Detect shared salary values (provincial fallback heuristic)
    counts = Counter(round(d["salary"]) for d in ficha_data.values())
    shared_values = {v for v, n in counts.items() if n >= threshold_shared}
    for slug, d in ficha_data.items():
        d["salary_estimated"] = round(d["salary"]) in shared_values

    # National averages — simple mean over the 587 fichas
    n = len(ficha_data) or 1
    nat_precio_m2 = sum(d["precio_m2"] for d in ficha_data.values()) / n
    nat_alquiler  = sum(d["alquiler"] for d in ficha_data.values()) / n
    nat_salary    = sum(d["salary"] for d in ficha_data.values()) / n

    nat_anos     = (nat_precio_m2 * 100) / nat_salary
    nat_cuota    = cuota_hipoteca(nat_precio_m2 * 100)
    nat_esfuerzo = nat_cuota / (nat_salary * 0.80 / 12) * 100
    nat_prr      = (nat_precio_m2 * 100) / (nat_alquiler * 12)

    return {
        "ficha_data": ficha_data,
        "nationals": {
            "precio_m2": nat_precio_m2,
            "alquiler":  nat_alquiler,
            "salary":    nat_salary,
            "anos":      nat_anos,
            "esfuerzo":  nat_esfuerzo,
            "prr":       nat_prr,
        },
        "shared_values": sorted(shared_values),
        "n_cities":      n,
    }


# ---------- Block builder ------------------------------------------------

CSS_BLOCK = """<style>
.afford-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.25rem 0}
.afford-card{background:var(--white,#fff);border:1px solid var(--border,#e2e8f0);border-radius:14px;padding:1.2rem 1.15rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.afford-icon{font-size:1.4rem;margin-bottom:.5rem}
.afford-val{font-size:1.95rem;font-weight:800;letter-spacing:-.03em;line-height:1}
.afford-unit{font-size:.9rem;color:var(--muted,#64748b);font-weight:600;margin-left:.3rem}
.afford-lbl{font-size:.78rem;color:var(--text2,#475569);margin-top:.5rem;line-height:1.4;font-weight:600}
.afford-sub{font-size:.7rem;color:var(--muted,#64748b);margin-top:.4rem;font-family:ui-monospace,monospace}
.afford-cmp{font-size:.72rem;font-weight:600;margin-top:.7rem;padding-top:.6rem;border-top:1px dashed var(--border,#e2e8f0)}
.afford-cmp.up{color:var(--green,#059669)}
.afford-cmp.down{color:var(--red,#dc2626)}
.afford-cmp.eq{color:var(--muted,#64748b)}
.afford-verdict{display:flex;align-items:center;gap:.95rem;padding:1.05rem 1.2rem;border-radius:12px;margin:.9rem 0 .55rem;border:1px solid}
.afford-verdict.ok{background:#ecfdf5;border-color:#a7f3d0}
.afford-verdict.ok .afford-vd-tit,.afford-verdict.ok .afford-vd-txt{color:#065f46}
.afford-verdict.warn{background:#fffbeb;border-color:#fde68a}
.afford-verdict.warn .afford-vd-tit,.afford-verdict.warn .afford-vd-txt{color:#92400e}
.afford-verdict.bad{background:#fef2f2;border-color:#fecaca}
.afford-verdict.bad .afford-vd-tit,.afford-verdict.bad .afford-vd-txt{color:#991b1b}
.afford-vd-icon{font-size:1.55rem}
.afford-vd-tit{font-weight:800;font-size:.95rem}
.afford-vd-txt{font-size:.78rem;margin-top:.18rem;line-height:1.45}
.afford-note{font-size:.72rem;color:var(--muted,#64748b);background:var(--white,#fff);border:1px solid var(--border,#e2e8f0);border-radius:8px;padding:.85rem 1rem;line-height:1.6;margin-top:.55rem}
@media(max-width:760px){.afford-grid{grid-template-columns:1fr}}
</style>
"""


def build_block(city: str, anos: float, esfuerzo: float, prr: float,
                precio_100: float, salary: float, cuota: float, alquiler: float,
                neto_mes: float, salary_estimated: bool,
                nats: dict) -> str:
    cmp1_cls, cmp1_txt = vs_nat(anos, nats["anos"])
    cmp2_cls, cmp2_txt = vs_nat(esfuerzo, nats["esfuerzo"])
    cmp3_cls, cmp3_txt = vs_nat(prr, nats["prr"])
    vd_cls, vd_icon, vd_tit, vd_txt = overall_verdict(anos, esfuerzo, prr)

    salary_src = (
        "estimación provincial AEAT 2024"
        if salary_estimated else
        "municipal AEAT 2024"
    )

    return f'''
{CSS_BLOCK}<!-- ¿PUEDO PERMITIRME COMPRAR EN {city.upper()}? -->
  <div class="section" id="afford">
    <div class="sec-hdr">
      <div class="sec-eye">Capacidad de compra</div>
      <h2>¿Puedo permitirme comprar en {city}?</h2>
      <p>Cruzamos el precio de un piso de 100 m² en {city} con el salario medio anual ({euro(salary)}€ · {salary_src}) y el alquiler local para responder a las tres preguntas clave del comprador.</p>
    </div>
    <div class="afford-grid">
      <div class="afford-card">
        <div class="afford-icon">📅</div>
        <div class="afford-val" style="color:{color_anos(anos)}">{anos:.1f}<span class="afford-unit">años</span></div>
        <div class="afford-lbl">de sueldo bruto para comprar un piso de 100 m²</div>
        <div class="afford-sub">{euro(precio_100)}€ ÷ {euro(salary)}€/año</div>
        <div class="afford-cmp {cmp1_cls}">{cmp1_txt}</div>
      </div>
      <div class="afford-card">
        <div class="afford-icon">💸</div>
        <div class="afford-val" style="color:{color_esfuerzo(esfuerzo)}">{esfuerzo:.0f}<span class="afford-unit">%</span></div>
        <div class="afford-lbl">de tu nómina mensual neta iría a la cuota de hipoteca</div>
        <div class="afford-sub">{euro(cuota)}€/mes ÷ {euro(neto_mes)}€/mes neto est.</div>
        <div class="afford-cmp {cmp2_cls}">{cmp2_txt}</div>
      </div>
      <div class="afford-card">
        <div class="afford-icon">⚖️</div>
        <div class="afford-val" style="color:{color_prr(prr)}">{prr:.1f}<span class="afford-unit">años</span></div>
        <div class="afford-lbl">de alquiler equivalen al precio del piso (price-to-rent)</div>
        <div class="afford-sub">{euro(precio_100)}€ ÷ {euro(alquiler * 12)}€/año alquiler</div>
        <div class="afford-cmp {cmp3_cls}">{cmp3_txt}</div>
      </div>
    </div>
    <div class="afford-verdict {vd_cls}">
      <span class="afford-vd-icon">{vd_icon}</span>
      <div>
        <div class="afford-vd-tit">{vd_tit}</div>
        <div class="afford-vd-txt">{vd_txt}</div>
      </div>
    </div>
    <p class="afford-note"><strong>Cómo leer estos datos:</strong> "Años de sueldo" es la ratio precio/ingresos bruta (ideal &lt;8, sostenible &lt;12). "Esfuerzo" sigue el estándar bancario del Banco de España: &lt;30% saludable, 30-40% ajustado, &gt;40% no viable. "Price-to-rent" indica si conviene comprar (&lt;15), equilibrio (15-20) o seguir alquilando (&gt;20). <strong>Fuentes:</strong> salario medio anual — {salary_src}; precio del m² y alquiler de {city} — datos Q1 2026 de Ren Data (origen INE · Ministerio de Vivienda). La cuota mensual asume hipoteca al 80% LTV, 3,2% TAE, 25 años. El salario neto se aproxima como 80% del bruto.</p>
  </div>

'''


# ---------- Per-file transform -------------------------------------------

def transform_ficha(html: str, slug: str, fdata: dict, nats: dict) -> tuple[str, dict]:
    info = {"slug": slug, "ok": False}

    if HAS_BLOCK_TOKEN in html:
        info["status"] = "already-present"
        info["ok"] = True
        return html, info

    d = fdata[slug]
    precio_100 = d["precio_m2"] * 100
    salary = d["salary"]
    alquiler = d["alquiler"]

    anos = precio_100 / salary
    cuota = cuota_hipoteca(precio_100)
    neto_mes = salary * 0.80 / 12
    esfuerzo = cuota / neto_mes * 100
    prr = precio_100 / (alquiler * 12)

    info.update(anos=anos, esfuerzo=esfuerzo, prr=prr)

    block = build_block(
        city=d["city"], anos=anos, esfuerzo=esfuerzo, prr=prr,
        precio_100=precio_100, salary=salary, cuota=cuota, alquiler=alquiler,
        neto_mes=neto_mes, salary_estimated=d["salary_estimated"], nats=nats,
    )

    new, n = RE_INSERT_ANCHOR.subn(block + r"\1", html, count=1)
    info["inserted"] = n
    info["ok"] = (n == 1)
    return (new if n == 1 else html), info


# ---------- Driver -------------------------------------------------------

def main(argv: list[str]) -> int:
    only = set(argv[1:])

    pre = precompute()
    fdata = pre["ficha_data"]
    nats = pre["nationals"]

    # Persist a summary so changes are auditable
    audit_path = ROOT / "data" / "fase2_summary.json"
    audit_path.write_text(json.dumps({
        "n_cities":      pre["n_cities"],
        "nationals":     nats,
        "shared_values": pre["shared_values"],
        "samples":       {s: {**fdata[s], "salary_estimated": fdata[s]["salary_estimated"]}
                          for s in list(fdata)[:6]},
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Precompute OK · {pre['n_cities']} ciudades · "
          f"medias: precio_m2={nats['precio_m2']:.0f}€ · alquiler={nats['alquiler']:.0f}€/mes · "
          f"salario={nats['salary']:.0f}€ · "
          f"años={nats['anos']:.1f} · esfuerzo={nats['esfuerzo']:.0f}% · "
          f"price-to-rent={nats['prr']:.1f}")
    print(f"Valores salario compartidos (>=4 ciudades): {pre['shared_values']}")

    files = sorted(FICHAS_DIR.glob("rentabilidad-*.html"))
    if only:
        files = [f for f in files if f.stem in only or f.name in only]

    ok = 0
    skipped = []
    fail = []
    for path in files:
        slug = path.stem.removeprefix("rentabilidad-")
        if slug not in fdata:
            skipped.append(slug)
            continue
        html = path.read_text(encoding="utf-8")
        new, info = transform_ficha(html, slug, fdata, nats)
        if info["ok"] and new != html:
            path.write_text(new, encoding="utf-8")
            ok += 1
        elif info["ok"]:
            ok += 1  # already-present, no write
        else:
            fail.append(info)

    print(f"Processed: {ok}/{len(files)} fichas OK")
    if skipped:
        print(f"Skipped (no CSV row or no salary): {len(skipped)} — {', '.join(skipped[:5])}")
    if fail:
        print(f"FAILURES ({len(fail)}):")
        for f in fail[:20]:
            print("  ", f)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
