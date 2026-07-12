#!/usr/bin/env python3
"""Generate rendata_beta/informe-rentabilidad-espana-q2-2026.html — a print-ready report."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
INDEX = BETA / "index.html"
OUT = BETA / "informe-rentabilidad-espana-q2-2026.html"


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def parse_data():
    html = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
                     r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
                     r'd:(\d+),sl:"([^"]+)"')
    rows = []
    for m in pat.finditer(html):
        rows.append({
            "n": m.group(1), "cc": m.group(2), "reg": m.group(3),
            "roi": float(m.group(4)), "p": int(m.group(5)), "alq": int(m.group(6)),
            "vp": float(m.group(7)), "va": float(m.group(8)),
            "d": int(m.group(9)), "sl": m.group(10),
        })
    return rows


def main():
    rows = parse_data()
    total = len(rows)
    avg_roi = sum(r["roi"] for r in rows) / total
    avg_p = sum(r["p"] for r in rows) / total
    avg_alq = sum(r["alq"] for r in rows) / total
    avg_vp = sum(r["vp"] for r in rows) / total

    # Top 10 cities
    top10 = sorted(rows, key=lambda r: -r["roi"])[:10]

    # CCAA aggregates
    by_ccaa = {}
    for r in rows:
        by_ccaa.setdefault(r["cc"], []).append(r)
    ccaa_stats = []
    for cc, cs in by_ccaa.items():
        n = len(cs)
        avg = sum(c["roi"] for c in cs) / n
        avg_pp = sum(c["p"] for c in cs) / n
        ccaa_stats.append({"cc": cc, "n": n, "roi": avg, "p": avg_pp})
    ccaa_stats.sort(key=lambda x: -x["roi"])
    top5_ccaa = ccaa_stats[:5]

    # Region heat
    by_reg = {}
    for r in rows:
        by_reg.setdefault(r["reg"], []).append(r)
    reg_stats = []
    REG_NAMES = {
        "norte": "Norte (PV, Cantabria, Asturias, La Rioja, Navarra, Galicia)",
        "centro": "Centro (Madrid, CyL, CLM, Aragón, Extremadura)",
        "levante": "Levante (CV, Murcia, Cataluña litoral)",
        "andalucia": "Andalucía",
        "islas": "Islas (Baleares + Canarias)",
        "costa": "Costa general",
        "metro": "Áreas metropolitanas",
        "interior": "Interior",
    }
    for reg, cs in by_reg.items():
        n = len(cs)
        avg = sum(c["roi"] for c in cs) / n
        avg_pp = sum(c["p"] for c in cs) / n
        reg_stats.append({"reg": reg, "name": REG_NAMES.get(reg, reg.title()), "n": n, "roi": avg, "p": avg_pp})
    reg_stats.sort(key=lambda x: -x["roi"])

    # JSON-LD
    article_json = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": "Rentabilidad Inmobiliaria en España Q2 2026 — Informe Ren Data",
        "description": (f"Informe descargable Q2 2026 con análisis de rentabilidad de "
                       f"{total} ciudades españolas: ROI medio {fmt_pct(avg_roi)}%, precio medio "
                       f"{fmt_eu(avg_p)}€/m², top 10 ciudades, top 5 CCAA y mapa de calor regional."),
        "datePublished": "2026-05-18", "dateModified": "2026-05-18",
        "author": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"},
        "publisher": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/",
                      "logo": {"@type": "ImageObject", "url": "https://rendata.es/favicon.svg"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": "https://rendata.es/informe-rentabilidad-espana-q2-2026.html"},
        "inLanguage": "es-ES",
    }

    # Top 10 rows
    top10_html = ""
    for i, c in enumerate(top10, 1):
        cls = " class='r-gold'" if i == 1 else " class='r-silver'" if i == 2 else " class='r-bronze'" if i == 3 else ""
        top10_html += (
            f'    <tr{cls}><td class="rk">{i}</td>'
            f'<td><strong><a href="rentabilidad-{c["sl"]}.html">{c["n"]}</a></strong> '
            f'<span class="cc">{c["cc"]}</span></td>'
            f'<td class="num roi-cell">{fmt_pct(c["roi"])}%</td>'
            f'<td class="num">{fmt_eu(c["p"])}€</td>'
            f'<td class="num">{fmt_eu(c["alq"])}€/mes</td>'
            f'<td class="num">+{fmt_pct(c["vp"])}%</td></tr>\n'
        )

    # CCAA top5
    ccaa_html = ""
    for i, c in enumerate(top5_ccaa, 1):
        cls = " class='r-gold'" if i == 1 else " class='r-silver'" if i == 2 else " class='r-bronze'" if i == 3 else ""
        ccaa_html += (
            f'    <tr{cls}><td class="rk">{i}</td>'
            f'<td><strong>{c["cc"]}</strong></td>'
            f'<td class="num roi-cell">{fmt_pct(c["roi"])}%</td>'
            f'<td class="num">{fmt_eu(c["p"])}€</td>'
            f'<td class="num">{c["n"]} ciudades</td></tr>\n'
        )

    # Region heatmap (text-based)
    def color(r):
        if r >= 6.2: return "#dcfce7", "#166534", "Alta"
        if r >= 5.5: return "#dbeafe", "#1e3a8a", "Media"
        return "#fee2e2", "#991b1b", "Baja"

    heat_html = ""
    for r in reg_stats:
        bg, fg, label = color(r["roi"])
        heat_html += (
            f'  <div class="heat-row" style="background:{bg};color:{fg}">\n'
            f'    <div class="heat-name">{r["name"]}</div>\n'
            f'    <div class="heat-bar"><div class="heat-fill" style="width:{int(r["roi"]*10)}%;background:{fg}"></div></div>\n'
            f'    <div class="heat-val">{fmt_pct(r["roi"])}% · {r["n"]} ciudades</div>\n'
            f'    <div class="heat-tag">{label}</div>\n'
            f'  </div>\n'
        )

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Informe Q2 2026 — Rentabilidad Inmobiliaria en España | Ren Data</title>
<meta name="description" content="Informe descargable Q2 2026 sobre rentabilidad inmobiliaria en España. {total} ciudades, ROI medio {fmt_pct(avg_roi)}%, top 10, top 5 CCAA, mapa de calor regional, metodología. Imprimible en PDF.">
<meta property="og:type" content="article">
<meta property="og:title" content="Informe Q2 2026 — Rentabilidad Inmobiliaria en España">
<meta property="og:description" content="Informe descargable con análisis completo de las {total} ciudades del DATA Ren Data. Imprimible en PDF.">
<meta property="og:url" content="https://rendata.es/informe-rentabilidad-espana-q2-2026.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="https://rendata.es/informe-rentabilidad-espana-q2-2026.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">{json.dumps(article_json, ensure_ascii=False)}</script>
<script src="/js/nav-dropdown.js" defer></script>
<style>
:root{{--bg:#f8fafc;--white:#fff;--blue:#1a56db;--navy:#0e2a6b;--green:#059669;--red:#dc2626;--gold:#fbbf24;--silver:#9ca3af;--bronze:#d97706;--text:#0f1923;--text2:#374151;--muted:#6b7a8d;--border:#e5eaf2;--font:'Plus Jakarta Sans',sans-serif}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#eef2f7;color:var(--text);font-family:var(--font);line-height:1.6;-webkit-font-smoothing:antialiased}}

/* Web header (hidden on print) */
.web-header{{background:#0e2a6b;padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}}
.web-header .logo{{text-decoration:none;color:#fff;font-size:1.1rem;font-weight:800}}
.web-header .logo span.ac{{color:#60a5fa}}
.web-header nav{{display:flex;gap:.2rem}}
.web-header nav a{{font-size:.82rem;font-weight:500;color:rgba(255,255,255,.7);text-decoration:none;padding:.42rem .8rem;border-radius:8px}}
.web-header nav a:hover{{color:#fff;background:rgba(255,255,255,.12)}}

.print-toolbar{{background:#fff;border-bottom:1px solid var(--border);padding:1rem 2rem;text-align:center;position:sticky;top:64px;z-index:50;box-shadow:0 1px 3px rgba(14,24,40,.05)}}
.btn-print{{background:#dc2626;color:#fff;border:none;padding:.75rem 1.5rem;border-radius:8px;font-family:inherit;font-weight:700;font-size:.92rem;cursor:pointer;display:inline-flex;align-items:center;gap:.5rem;transition:background .15s}}
.btn-print:hover{{background:#b91c1c}}
.print-help{{display:block;margin-top:.5rem;font-size:.78rem;color:var(--muted)}}

.report{{max-width:880px;margin:2rem auto;background:#fff;box-shadow:0 4px 24px rgba(14,24,40,.08);border-radius:12px;overflow:hidden}}
.cover{{background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:5rem 3rem;text-align:center}}
.cover-logo{{font-size:1.6rem;font-weight:800;letter-spacing:-.04em;margin-bottom:2rem;display:inline-flex;align-items:center;gap:.6rem}}
.cover-logo .blue{{color:#60a5fa}}
.cover-eyebrow{{font-size:.78rem;font-weight:700;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:1.5rem}}
.cover h1{{font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:800;letter-spacing:-.04em;line-height:1.15;margin-bottom:1.5rem}}
.cover-sub{{font-size:1rem;color:rgba(255,255,255,.8);max-width:580px;margin:0 auto 2.5rem;line-height:1.65}}
.cover-meta{{display:flex;gap:2.5rem;justify-content:center;flex-wrap:wrap;font-size:.82rem}}
.cover-meta div{{color:rgba(255,255,255,.7)}}
.cover-meta strong{{display:block;color:#fff;font-size:1.15rem;margin-top:.3rem}}

.section{{padding:3rem 3rem 2rem}}
.section h2{{font-size:1.4rem;font-weight:800;letter-spacing:-.03em;color:var(--text);margin-bottom:1.5rem;padding-bottom:.75rem;border-bottom:2px solid var(--blue);display:inline-block}}
.section p{{font-size:.92rem;color:var(--text2);line-height:1.7;margin-bottom:1rem}}

.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:1.5rem 0 2rem}}
.kpi{{background:#f8fafc;border:1px solid var(--border);border-radius:12px;padding:1.25rem 1rem;text-align:center}}
.kpi-v{{font-size:1.6rem;font-weight:800;letter-spacing:-.03em;color:var(--blue)}}
.kpi-l{{font-size:.74rem;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-top:.3rem}}

table.tbl{{width:100%;border-collapse:collapse;font-size:.86rem;margin:1rem 0 1.5rem}}
table.tbl thead th{{background:#f8fafc;font-weight:700;text-align:left;padding:.7rem .8rem;border-bottom:2px solid var(--border);font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
table.tbl tbody td{{padding:.7rem .8rem;border-bottom:1px solid var(--border)}}
table.tbl tbody tr:last-child td{{border-bottom:none}}
table.tbl .rk{{font-weight:700;text-align:center;width:40px;color:var(--muted)}}
table.tbl .r-gold .rk{{color:var(--gold);font-size:1.05rem}}
table.tbl .r-silver .rk{{color:var(--silver);font-size:1.05rem}}
table.tbl .r-bronze .rk{{color:var(--bronze);font-size:1.05rem}}
table.tbl .num{{text-align:right;font-variant-numeric:tabular-nums;font-weight:500}}
table.tbl .roi-cell{{font-weight:700;color:var(--blue)}}
table.tbl .cc{{display:block;font-size:.74rem;color:var(--muted);font-weight:500;margin-top:.15rem}}
table.tbl a{{color:var(--text);text-decoration:none}}
table.tbl a:hover{{color:var(--blue)}}

.heatmap{{display:flex;flex-direction:column;gap:.5rem;margin:1rem 0 1.5rem}}
.heat-row{{display:grid;grid-template-columns:1fr 100px 130px 60px;align-items:center;gap:1rem;padding:.7rem 1rem;border-radius:8px;font-size:.86rem}}
.heat-name{{font-weight:600}}
.heat-bar{{background:rgba(0,0,0,.08);height:8px;border-radius:4px;overflow:hidden;width:100%}}
.heat-fill{{height:100%;border-radius:4px}}
.heat-val{{font-size:.78rem;text-align:right;font-variant-numeric:tabular-nums}}
.heat-tag{{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;text-align:right;opacity:.7}}

.method-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0}}
.method-box{{background:#f8fafc;border:1px solid var(--border);border-radius:10px;padding:1.2rem}}
.method-box h3{{font-size:.95rem;font-weight:700;color:var(--text);margin-bottom:.5rem}}
.method-box p{{font-size:.82rem;margin:0;color:var(--text2)}}

.disclaimer{{background:#fef3c7;border:1px solid #fcd34d;border-radius:10px;padding:1rem 1.25rem;margin:1.5rem 0 0;font-size:.82rem;color:#78350f;line-height:1.65}}

.report-footer{{background:#f8fafc;padding:2rem 3rem;text-align:center;border-top:1px solid var(--border);font-size:.82rem;color:var(--muted)}}
.report-footer strong{{color:var(--text)}}

.web-footer{{padding:2rem;text-align:center;font-size:.78rem;color:var(--muted)}}
.web-footer a{{color:var(--blue);text-decoration:none}}

/* PRINT STYLES */
@media print {{
  body{{background:#fff;font-size:10pt;line-height:1.5}}
  .web-header, .print-toolbar, .web-footer{{display:none !important}}
  .report{{box-shadow:none;border-radius:0;max-width:100%;margin:0}}
  .cover{{padding:3rem 2rem;page-break-after:always}}
  .cover h1{{font-size:24pt}}
  .section{{padding:1.5rem 2rem;page-break-inside:avoid}}
  .section h2{{font-size:14pt}}
  .kpi-v{{font-size:14pt}}
  table.tbl{{font-size:9pt;page-break-inside:avoid}}
  table.tbl thead th{{font-size:7.5pt;padding:.4rem .5rem}}
  table.tbl tbody td{{padding:.35rem .5rem}}
  .heat-row{{padding:.4rem .7rem;font-size:9pt}}
  .heatmap{{page-break-inside:avoid}}
  .method-grid{{page-break-inside:avoid}}
  a{{color:#000;text-decoration:none}}
  .report-footer{{page-break-before:always;padding:1.5rem 2rem}}
  @page{{margin:1.2cm;size:A4}}
}}

@media (max-width:740px){{
  .section{{padding:2rem 1.4rem}}
  .cover{{padding:3rem 1.5rem}}
  .kpis{{grid-template-columns:repeat(2,1fr)}}
  .method-grid{{grid-template-columns:1fr}}
  .heat-row{{grid-template-columns:1fr;gap:.3rem;text-align:left}}
  .heat-val,.heat-tag{{text-align:left}}
}}
</style>
</head>
<body>

<header class="web-header">
  <a href="/" class="logo">Ren<span class="ac"> Data</span></a>
  <nav>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/comparador.html">Comparador</a>
    <a href="/metodologia.html">Metodología</a>
  </nav>
</header>

<div class="print-toolbar">
  <button class="btn-print" onclick="window.print()">📄 Descargar como PDF</button>
  <span class="print-help">Pulsa el botón y elige "Guardar como PDF" en el diálogo de impresión de tu navegador.</span>
</div>

<article class="report">

  <header class="cover">
    <div class="cover-logo">📊 <span>Ren<span class="blue"> Data</span></span></div>
    <div class="cover-eyebrow">Informe trimestral · Q2 2026</div>
    <h1>Rentabilidad Inmobiliaria<br/>en España Q2 2026</h1>
    <p class="cover-sub">Análisis de mercado de {total} ciudades españolas con datos del INE, Ministerio de Vivienda y Ministerio de Hacienda. Cierre de datos: mayo 2026.</p>
    <div class="cover-meta">
      <div>Publicado<strong>18 mayo 2026</strong></div>
      <div>Ciudades analizadas<strong>{total}</strong></div>
      <div>Fuente<strong>Datos oficiales</strong></div>
    </div>
  </header>

  <section class="section">
    <h2>Resumen ejecutivo</h2>
    <p>El mercado inmobiliario español Q2 2026 mantiene una <strong>dinámica alcista moderada</strong> con un ROI bruto medio del <strong>{fmt_pct(avg_roi)}%</strong> sobre vivienda estándar de 100m² para las {total} ciudades del análisis. El precio medio del m² es de <strong>{fmt_eu(avg_p)}€</strong> y el alquiler medio de <strong>{fmt_eu(avg_alq)}€/mes</strong>. La subida media de precio en los últimos 12 meses ha sido del <strong>+{fmt_pct(avg_vp)}%</strong>.</p>

    <div class="kpis">
      <div class="kpi"><div class="kpi-v">{total}</div><div class="kpi-l">Ciudades</div></div>
      <div class="kpi"><div class="kpi-v">{fmt_pct(avg_roi)}%</div><div class="kpi-l">ROI medio</div></div>
      <div class="kpi"><div class="kpi-v">{fmt_eu(avg_p)}€</div><div class="kpi-l">Precio medio m²</div></div>
      <div class="kpi"><div class="kpi-v">+{fmt_pct(avg_vp)}%</div><div class="kpi-l">Subida anual</div></div>
    </div>

    <p><strong>Lectura clave:</strong> los mercados de yield más alto se concentran en capitales menores del interior peninsular (Cuenca, Zamora, Teruel, Ciudad Real) con tickets bajos. Los mercados de revalorización más alta son grandes capitales (Madrid, Málaga, Valencia, Alicante) con yield modesto. <strong>El binomio yield + revalorización es el indicador clave para 2026</strong>.</p>
  </section>

  <section class="section">
    <h2>Top 10 ciudades más rentables</h2>
    <p>Ranking nacional ordenado por ROI bruto. La ROI bruta se calcula sobre vivienda estándar de 100m² con la fórmula: <strong>(alquiler × 12) / (precio_m² × 100) × 100</strong>.</p>
    <table class="tbl">
      <thead>
        <tr><th>#</th><th>Ciudad</th><th class="num">ROI bruto</th><th class="num">Precio m²</th><th class="num">Alquiler</th><th class="num">Var. precio</th></tr>
      </thead>
      <tbody>
{top10_html}      </tbody>
    </table>
  </section>

  <section class="section">
    <h2>Top 5 comunidades autónomas</h2>
    <p>Ranking de CCAA por ROI medio (media simple de las ciudades incluidas en el DATA Ren Data).</p>
    <table class="tbl">
      <thead>
        <tr><th>#</th><th>Comunidad autónoma</th><th class="num">ROI medio</th><th class="num">Precio medio m²</th><th class="num">Ciudades</th></tr>
      </thead>
      <tbody>
{ccaa_html}      </tbody>
    </table>
  </section>

  <section class="section">
    <h2>Mapa de calor regional</h2>
    <p>Distribución de la rentabilidad por macro-región. Las zonas en verde superan el 6,2% de ROI medio, las azules entre 5,5-6,2% y las rojas por debajo del 5,5%.</p>
    <div class="heatmap">
{heat_html}    </div>
  </section>

  <section class="section">
    <h2>Metodología (resumen)</h2>
    <div class="method-grid">
      <div class="method-box">
        <h3>📊 Fuentes</h3>
        <p>INE (población), Ministerio de Vivienda (precio m²), Ministerio de Hacienda (ITP autonómicos), observatorios autonómicos (alquiler), Notariado (validación cruzada).</p>
      </div>
      <div class="method-box">
        <h3>🧮 Cálculo ROI</h3>
        <p>ROI bruto = (alquiler anual / precio compra) × 100. Superficie estandarizada a 100m² para comparabilidad entre ciudades. Sin descontar gastos.</p>
      </div>
      <div class="method-box">
        <h3>🔄 Actualización</h3>
        <p>Trimestral. El próximo informe (Q3 2026) está previsto para agosto. Los datos se publican con 15-30 días de retraso desde el cierre del trimestre.</p>
      </div>
      <div class="method-box">
        <h3>📍 Cobertura</h3>
        <p>{total} municipios españoles con población ≥15.000 habitantes. Capitales de provincia, suburbios metropolitanos, costa turística y plazas industriales.</p>
      </div>
    </div>

    <div class="disclaimer">
      <strong>⚠️ Limitaciones:</strong> los precios de m² son medias municipales del Ministerio de Vivienda — pueden diferir de portales como Idealista o Fotocasa (que reflejan precios pedidos, no de transacción). Los datos de alquiler proceden de observatorios autonómicos con cobertura desigual. El ROI bruto no descuenta gastos (IBI, comunidad, mantenimiento, impuestos, vacancia) — el ROI neto típico está 1,5-2 puntos por debajo del bruto. <strong>Este informe es informativo, no constituye asesoramiento financiero.</strong>
    </div>
  </section>

  <footer class="report-footer">
    <strong>Ren Data</strong> · rendata.es · © 2026<br/>
    Datos abiertos · Análisis gratuito · Actualizado trimestralmente<br/>
    <a href="https://rendata.es/metodologia.html" style="color:var(--blue);text-decoration:none;font-weight:600">Ver metodología completa →</a>
  </footer>

</article>

<div class="web-footer">
  <p>¿Te ha resultado útil? Compártelo o consulta la <a href="/metodologia.html">metodología completa</a>.</p>
</div>

</body>
</html>
'''
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
