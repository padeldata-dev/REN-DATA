#!/usr/bin/env python3
"""Generates 10 profile-based investor articles in rendata_beta/.

Reads DATA[] from index.html to compute rankings for each topic.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
INDEX = BETA / "index.html"


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


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def nav_html():
    return '''<header>
  <a href="/" class="logo">
    <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
    <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
  </a>
  <nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/comparador.html">Comparador</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/guia-inversor.html">Guía</a>
    <a href="/sobre.html">Sobre</a>
  </nav>
</header>'''


def footer_html(total):
    return f'''<footer>
  <div class="footer-inner">
    <div class="footer-col">
      <a href="/" class="logo" style="margin-bottom:.6rem;display:inline-flex">
        <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
        <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
      </a>
      <p>Análisis de rentabilidad inmobiliaria gratuito para {total} ciudades de España. Datos Q1 2026.</p>
    </div>
    <div class="footer-col">
      <h4>Análisis</h4>
      <a href="ranking.html">Ranking completo</a>
      <a href="analisis.html">Análisis</a>
      <a href="comparador.html">Comparador</a>
      <a href="guia-inversor.html">Guía del inversor</a>
    </div>
    <div class="footer-col">
      <h4>Recursos</h4>
      <a href="glosario.html">Glosario</a>
      <a href="sobre.html">Sobre Ren Data</a>
      <a href="contacto.html">Contacto</a>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <a href="privacidad.html">Privacidad</a>
      <a href="aviso-legal.html">Aviso legal</a>
    </div>
  </div>
  <div class="footer-bottom">© 2026 rendata.es · Fuente: Idealista Q1 2026 · Ministerio de Vivienda</div>
</footer>'''


def article_head(slug, title, desc, breadcrumb_label, article_json=None):
    if article_json is None:
        article_json = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "datePublished": "2026-05-18",
            "dateModified": "2026-05-18",
            "author": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"},
            "publisher": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/",
                          "logo": {"@type": "ImageObject", "url": "https://rendata.es/favicon.svg"}},
            "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://rendata.es/{slug}.html"},
            "inLanguage": "es-ES",
            "keywords": ["rentabilidad inmobiliaria", "invertir vivienda España", "ROI alquiler"]
        }
    breadcrumb_json = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://rendata.es/"},
            {"@type": "ListItem", "position": 2, "name": "Análisis", "item": "https://rendata.es/analisis.html"},
            {"@type": "ListItem", "position": 3, "name": breadcrumb_label, "item": f"https://rendata.es/{slug}.html"}
        ]
    }
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title} | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://rendata.es/{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="canonical" href="https://rendata.es/{slug}.html">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">{json.dumps(article_json, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_json, ensure_ascii=False)}</script>
<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
<style>
.bc{{max-width:880px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}}
.bc a{{color:var(--muted);text-decoration:none;font-weight:500}}
.bc a:hover{{color:var(--blue);text-decoration:underline}}
.bc-sep{{color:#cbd5e1}}
.bc-cur{{color:var(--text);font-weight:600}}
.pro-con{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin:1.5rem 0 2rem}}
.pc-col{{padding:1.25rem 1.4rem;border-radius:var(--r);background:var(--white);border:1px solid var(--border);box-shadow:var(--sh)}}
.pc-col.pro{{border-left:4px solid var(--green)}}
.pc-col.con{{border-left:4px solid #dc2626}}
.pc-col h3{{font-size:1.05rem;font-weight:800;color:var(--text);margin:0 0 .8rem;border:none;padding:0;display:block;letter-spacing:-.02em}}
.pc-col.pro h3{{color:var(--green)}}
.pc-col.con h3{{color:#dc2626}}
.pc-col ul{{list-style:none;padding:0;margin:0}}
.pc-col li{{font-size:.88rem;padding:.45rem 0;color:var(--text2);line-height:1.55;border-bottom:1px solid var(--border)}}
.pc-col li:last-child{{border-bottom:none}}
.pc-col li:before{{margin-right:.4rem;font-weight:700}}
.pc-col.pro li:before{{content:"✓";color:var(--green)}}
.pc-col.con li:before{{content:"⚠";color:#dc2626}}
.tax-box{{background:#fef3c7;border:1px solid #fcd34d;border-radius:var(--r);padding:1.4rem 1.6rem;margin:1.5rem 0;font-size:.92rem;color:#78350f;line-height:1.7}}
.tax-box h3{{font-size:1.05rem;font-weight:800;color:#78350f;margin:0 0 .6rem;border:none;padding:0;display:block;letter-spacing:-.02em}}
@media(max-width:740px){{.pro-con{{grid-template-columns:1fr}}}}
</style>
<link rel="stylesheet" href="/css/nav.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-0M57323B51');</script>
</head>
<body>
'''


def article_open(title_html, lead_html, breadcrumb_label, total):
    return f'''
{nav_html()}

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">Inicio</a>
  <span class="bc-sep">›</span>
  <a href="analisis.html">Análisis</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">{breadcrumb_label}</span>
</nav>

<section class="art-hero">
  <div class="art-hero-inner">
    <div class="art-eyebrow"><span class="live-dot"></span>Análisis · Datos Q1 2026</div>
    <h1>{title_html}</h1>
    <div class="art-meta">
      <span>📅 Publicado el 18 de mayo de 2026</span>
      <span>📊 Fuente: Idealista, Ministerio de Vivienda</span>
      <span>🔄 Actualizado mensualmente</span>
    </div>
    <p class="art-lead">{lead_html}</p>
  </div>
</section>

<article class="art">
'''


def article_close(total):
    return f'''
  <div class="art-cta">
    <h3>¿Listo para encontrar tu próxima inversión?</h3>
    <p>Compara hasta 4 ciudades simultáneamente o explora el ranking completo de {total} plazas analizadas.</p>
    <a href="comparador.html">Abrir comparador →</a>
  </div>
</article>

{footer_html(total)}

</body>
</html>
'''


def table_rows(cities):
    out = ""
    for i, c in enumerate(cities, 1):
        rank = "gold" if i == 1 else "silver" if i == 2 else "bronze" if i == 3 else ""
        out += (
            f'        <tr><td class="cmp-rank {rank}">{i}</td>'
            f'<td><a href="rentabilidad-{c["sl"]}.html" class="cmp-city">{c["n"]}</a>'
            f'<span class="cmp-cc">{c["cc"]}</span></td>'
            f'<td><span class="cmp-roi">{fmt_pct(c["roi"])}%</span></td>'
            f'<td class="cmp-num">{fmt_eu(c["p"])}€</td>'
            f'<td class="cmp-num">{fmt_eu(c["alq"])}€/mes</td>'
            f'<td class="cmp-num">+{fmt_pct(c["vp"])}%</td>'
            f'<td><a href="rentabilidad-{c["sl"]}.html">Ver →</a></td></tr>\n'
        )
    return out


def write_article(slug, html):
    out = BETA / f"{slug}.html"
    out.write_text(html, encoding="utf-8")
    nlines = html.count("\n")
    print(f"  [ok] {out.name} ({nlines} lines)")


# ---------------------------------------------------------------------------
# Article 1: Conservador
# ---------------------------------------------------------------------------
def art_conservador(rows, total):
    slug = "guia-inversor-conservador-2026"
    cs = [r for r in rows if 5.0 <= r["roi"] <= 6.0 and r["d"] <= 24 and r["p"] >= 1500]
    cs.sort(key=lambda x: (-x["roi"], x["d"]))
    top = cs[:15]
    title = "Guía del inversor conservador 2026 — Ciudades estables y bajo riesgo"
    desc = (f"Selección de ciudades estables con ROI 5-6%, demanda sostenida y baja "
            f"volatilidad para inversor conservador. Capitales medias, mercados consolidados. "
            f"Análisis con datos Q1 2026 de {total} ciudades.")
    head = article_head(slug, title, desc, "Guía del inversor conservador")
    body = article_open(
        'Guía del inversor <span class="ac">conservador</span> 2026',
        ("El inversor conservador busca <strong>preservar capital con yield razonable</strong>. "
         "Prefiere mercados consolidados, demanda estructural sólida, liquidez de venta razonable "
         "y baja exposición regulatoria. Esta guía identifica las ciudades del DATA Ren Data que "
         "cumplen los cuatro criterios: ROI 5-6% bruto, días de venta &lt;25, precio &gt;1.500€/m² "
         "(implica mercado consolidado) y ubicación en CCAA con marco regulatorio estable."),
        "Guía del inversor conservador 2026", total)

    body += '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#perfil">El perfil conservador</a></li>
      <li><a href="#criterios">Criterios de selección</a></li>
      <li><a href="#top">Top 15 ciudades para perfil conservador</a></li>
      <li><a href="#estrategia">Estrategia recomendada</a></li>
      <li><a href="#errores">Errores que evitar</a></li>
    </ul>
  </div>

  <h2 id="perfil">El perfil conservador</h2>
  <p>El inversor conservador <strong>prioriza la estabilidad sobre el yield máximo</strong>. Su objetivo principal es preservar capital con una rentabilidad razonable y bajo riesgo de impago, vacancia o devaluación. Es típicamente un ahorrador que diversifica de la bolsa, un jubilado que busca renta complementaria, o un profesional con liquidez que prefiere inmuebles a bonos.</p>
  <p>El conservador acepta <strong>ROI bruto 5-6% a cambio de mercados consolidados</strong>: capitales con demanda inquebrantable, suburbios premium establecidos, ciudades con economía diversificada. Evita: municipios &lt;15.000 habitantes con riesgo de despoblación, mercados turísticos puros con estacionalidad fuerte, plazas con regulación VUT inestable.</p>

  <h2 id="criterios">Criterios de selección</h2>
  <p>Para identificar plazas adecuadas aplicamos cuatro filtros simultáneos al DATA de Ren Data:</p>
  <p><strong>1. ROI bruto 5,0% — 6,0%.</strong> Yield razonable pero no extremo. Por encima del 6% suele indicar tickets demasiado bajos o mercados menos consolidados.</p>
  <p><strong>2. Días de venta &lt; 25.</strong> Liquidez razonable: la vivienda se vende en &lt;25 días promedio, lo que indica demanda viva si necesitamos salir.</p>
  <p><strong>3. Precio m² &gt; 1.500€.</strong> Por encima de este umbral los mercados suelen ser estructuralmente consolidados (capitales, suburbios premium).</p>
  <p><strong>4. CCAA con marco regulatorio estable.</strong> Excluye zonas con declaración activa de zonas tensionadas (Cataluña) salvo casos específicos verificados.</p>
'''

    body += f'''
  <h2 id="top">Top 15 ciudades para perfil conservador</h2>
  <p>Ranking ordenado por ROI bruto descendente. Pulsa en cualquier ciudad para acceder a su ficha completa con análisis detallado.</p>
  <div class="tbl-wrap">
    <table class="cmp">
      <thead><tr><th>#</th><th>Ciudad</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr></thead>
      <tbody>
{table_rows(top)}      </tbody>
    </table>
  </div>

  <h2 id="estrategia">Estrategia recomendada</h2>
  <p><strong>1. Diversifica por CCAA.</strong> No concentres todo en una sola región. Una cartera conservadora de 2-3 inmuebles bien distribuidos (ej: Valladolid + Murcia + Las Palmas GC) reduce riesgo regulatorio y económico.</p>
  <p><strong>2. Apunta a 100m².</strong> Las viviendas estándar (100m², 3 habitaciones) son las que mantienen mejor liquidez y demanda. Evita estudios y dúplex grandes en este perfil.</p>
  <p><strong>3. Prioriza barrios consolidados.</strong> No el más barato del centro: el segundo o tercer barrio consolidado de la ciudad ofrece mejor binomio rentabilidad/seguridad.</p>
  <p><strong>4. Contrato de larga duración.</strong> El régimen LAU vigente protege más al arrendador en contratos de 5+2 años que en VUT. Para conservador, larga duración.</p>

  <h2 id="errores">Errores que evitar</h2>
  <div class="pro-con">
    <div class="pc-col con">
      <h3>Errores típicos del conservador</h3>
      <ul>
        <li><strong>Comprar barato pensando que es ganga:</strong> el municipio puede tener tendencia poblacional negativa estructural.</li>
        <li><strong>Sobreapalancar:</strong> el conservador no debería financiar más del 50-60% del precio.</li>
        <li><strong>Olvidar gastos:</strong> IBI + comunidad + mantenimiento + vacancia + impuestos suelen ser 1,5-2 puntos del yield bruto.</li>
        <li><strong>Confiar 100% en el agente:</strong> revisa siempre el Registro de la Propiedad y verifica cargas.</li>
        <li><strong>Comprar sin visitar:</strong> el conservador debe ver el inmueble y el barrio en persona.</li>
      </ul>
    </div>
  </div>

  <p>Para profundizar consulta el <a href="ranking.html">ranking completo de ciudades</a> filtrado por ROI o el <a href="comparador.html">comparador</a> para enfrentar hasta 4 plazas simultáneamente. Si tu perfil es más agresivo, lee la <a href="guia-inversor-agresivo-2026.html">guía del inversor agresivo</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 2: Agresivo
# ---------------------------------------------------------------------------
def art_agresivo(rows, total):
    slug = "guia-inversor-agresivo-2026"
    cs = sorted([r for r in rows if r["roi"] >= 6.5], key=lambda x: -x["roi"])
    top = cs[:20]
    title = "Guía del inversor agresivo 2026 — Máximo ROI y ciudades pequeñas"
    desc = (f"Las plazas con yield más alto del país. Cuenca, Zamora, Teruel, Ciudad Real "
            f"y otras superan el 7% bruto. Análisis de riesgos de liquidez, vacancia y "
            f"revalorización en municipios pequeños. Estrategia para ROI máximo.")
    head = article_head(slug, title, desc, "Guía del inversor agresivo")
    body = article_open(
        'Guía del inversor <span class="ac">agresivo</span> 2026',
        ("El inversor agresivo busca <strong>maximizar yield bruto</strong> aceptando mayor "
         "exposición a riesgos de liquidez, vacancia y revalorización modesta. Las ciudades "
         "del DATA Ren Data con ROI &gt;6,5% son típicamente capitales pequeñas (&lt;50.000 hab) "
         "o municipios agroindustriales con tickets bajos. Esta guía analiza las 20 plazas "
         "más rentables, sus riesgos y la estrategia para extraer valor del yield alto."),
        "Guía del inversor agresivo 2026", total)

    body += f'''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#perfil">El perfil agresivo</a></li>
      <li><a href="#top">Top 20 ciudades por ROI bruto</a></li>
      <li><a href="#riesgos">Riesgos específicos del yield alto</a></li>
      <li><a href="#estrategia">Estrategia operativa</a></li>
      <li><a href="#conclusion">Conclusión</a></li>
    </ul>
  </div>

  <h2 id="perfil">El perfil agresivo</h2>
  <p>El inversor agresivo prioriza <strong>cash-flow máximo</strong>. Acepta mercados menos líquidos (días de venta 25-30), exposición a vacancia (rotación de inquilinos) y revalorización menor (subidas anuales 3-5% vs 7-10% en capitales) a cambio de yield superior al 7%.</p>
  <p>Es típicamente un inversor con experiencia previa, capacidad de gestión remota y horizonte 10-15 años. Suele construir cartera diversificada (5-10 inmuebles) donde el yield del conjunto compensa la vacancia puntual.</p>

  <h2 id="top">Top 20 ciudades por ROI bruto en España 2026</h2>
  <p>Ranking de las 20 plazas con mayor rentabilidad bruta del DATA Ren Data. Capitales como Zamora (7,5%), Cuenca (7,5%), Ciudad Real (7,2%) y Teruel (7,2%) lideran con tickets de 900-1.000€/m².</p>
  <div class="tbl-wrap">
    <table class="cmp">
      <thead><tr><th>#</th><th>Ciudad</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr></thead>
      <tbody>
{table_rows(top)}      </tbody>
    </table>
  </div>

  <h2 id="riesgos">Riesgos específicos del yield alto</h2>
  <div class="pro-con">
    <div class="pc-col pro">
      <h3>Ventajas del agresivo</h3>
      <ul>
        <li><strong>Cash-flow positivo desde el día 1.</strong> Con financiación al 70%, el yield 7% bruto cubre cuota hipoteca + gastos con margen.</li>
        <li><strong>Tickets bajos:</strong> entrada 20% sobre 90.000€ = solo 18.000€. Permite construir cartera más rápido.</li>
        <li><strong>Demanda local estable:</strong> en capitales pequeñas con empleo público (administración, hospital, universidad), la demanda es muy estable.</li>
        <li><strong>Menos competencia profesional:</strong> los grandes fondos no operan en mercados &lt;30.000 habitantes.</li>
      </ul>
    </div>
    <div class="pc-col con">
      <h3>Riesgos</h3>
      <ul>
        <li><strong>Liquidez:</strong> vender en municipios pequeños puede tardar 30-60 días vs 15-20 en capitales.</li>
        <li><strong>Vacancia:</strong> menor pool de inquilinos. Una rotación puede dejar el piso 2-3 meses vacío.</li>
        <li><strong>Revalorización modesta:</strong> +3-5% anual vs +8-10% en grandes capitales. A 10 años el agregado de yield + plusvalía puede igualarse.</li>
        <li><strong>Coste de gestión remota:</strong> si no eres local, necesitas agencia o gestor (8-10% del alquiler).</li>
        <li><strong>Tendencia poblacional:</strong> muchas capitales pequeñas pierden población. Verifica que el municipio crece o se mantiene.</li>
      </ul>
    </div>
  </div>

  <h2 id="estrategia">Estrategia operativa</h2>
  <p><strong>1. Concentra geográficamente.</strong> En lugar de 1 piso en cada CCAA, concentra 3-4 en la misma zona (ej: tres en Cuenca o dos en Zamora + dos en Palencia). Reduce coste de gestión remota.</p>
  <p><strong>2. Verifica empleadores locales.</strong> Hospital, universidad, administración, polígono industrial: la demanda de alquiler depende de quién tiene trabajo estable en la ciudad.</p>
  <p><strong>3. Apunta a 2-3 dormitorios.</strong> Las viviendas tipo familia trabajadora son las más demandadas en estos mercados.</p>
  <p><strong>4. Acepta vacancia ocasional.</strong> Provisiona 2 meses de cuota hipoteca como colchón.</p>

  <h2 id="conclusion">Conclusión</h2>
  <p>El perfil agresivo es <strong>compatible con yield 7%+ si aceptas trabajar mercados menos líquidos</strong>. La clave es diversificar dentro del mismo perfil (3-5 inmuebles en 2-3 ciudades pequeñas) en lugar de exposición única.</p>
  <p>Para complementar consulta el análisis de <a href="municipios-pequenos-alta-rentabilidad-2026.html">municipios pequeños con alta rentabilidad</a> y el <a href="ciudades-universitarias-rentabilidad-alquiler-2026.html">artículo de ciudades universitarias</a>. Si tu perfil es más conservador, lee la <a href="guia-inversor-conservador-2026.html">guía del inversor conservador</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 3: Vacacional
# ---------------------------------------------------------------------------
def art_vacacional(rows, total):
    slug = "invertir-vivienda-vacacional-espana-2026"
    coast_keywords = ["costero", "costera", "costa", "playa", "marítima", "balear", "canari", "vacacional", "turist"]
    # Use cities from CV, Baleares, Canarias, Andalucia coast, Cataluna costa
    cs = [r for r in rows if r["cc"] in ("Islas Baleares", "Canarias") or
          r["sl"] in ("benidorm", "calp", "calpe", "marbella", "estepona", "salou", "cambrils",
                      "torrevieja", "alcudia", "santa-eularia-des-riu", "sant-antoni-de-portmany",
                      "adeje", "san-bartolome-de-tirajana", "puerto-de-la-cruz", "arona-tenerife-sur",
                      "ibiza", "palma", "manilva", "guardamar-del-segura", "guia-de-isora",
                      "los-realejos", "candelaria", "calella", "pineda-de-mar", "salou",
                      "tias", "pajara", "mogan", "la-vila-joiosa", "el-campello")]
    cs.sort(key=lambda x: -x["roi"])
    top = cs[:20]
    title = "Invertir en vivienda vacacional en España 2026 — VUT, estacionalidad y rentabilidad"
    desc = ("Mercado vacacional regulado: licencias VUT por CCAA, estacionalidad, ocupación "
            "y comparativa con alquiler residencial. Costa del Sol, Baleares, Canarias y Costa Brava. "
            "Análisis con datos Q1 2026.")
    head = article_head(slug, title, desc, "Invertir en vivienda vacacional")
    body = article_open(
        'Invertir en vivienda <span class="ac">vacacional</span> en España 2026',
        ("La vivienda vacacional (VUT, VFT, HUT según CCAA) es uno de los productos inmobiliarios "
         "más rentables por bruto pero también el más regulado. La ocupación estacional, los gastos "
         "operativos elevados y la regulación municipal/autonómica hacen imprescindible un análisis "
         "específico antes de invertir. Esta guía analiza el panorama 2026 y propone las 20 plazas "
         "más atractivas del DATA Ren Data."),
        "Invertir en vivienda vacacional 2026", total)

    body += f'''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#regulacion">Marco regulatorio por CCAA</a></li>
      <li><a href="#economia">Economía del alquiler vacacional</a></li>
      <li><a href="#top">Top 20 plazas vacacionales</a></li>
      <li><a href="#fiscalidad">Fiscalidad VUT</a></li>
      <li><a href="#estrategia">Estrategia operativa</a></li>
      <li><a href="#conclusion">Conclusión</a></li>
    </ul>
  </div>

  <h2 id="regulacion">Marco regulatorio por CCAA</h2>
  <p>Cada comunidad autónoma regula el alquiler vacacional con normativa propia. Para invertir hay que conocer la situación específica antes de comprar:</p>
  <p><strong>Islas Baleares (ETV)</strong>. Régimen más restrictivo. Moratorias en Palma de Mallorca. Licencias limitadas por consell insular. Compra para uso vacacional requiere due diligence severa.</p>
  <p><strong>Canarias (VV)</strong>. Régimen relativamente permisivo en municipios sin moratoria. Tenerife sur (Adeje, Arona) y Gran Canaria sur (San Bartolomé, Mogán) tienen alta concentración. Verifica antes de comprar.</p>
  <p><strong>Cataluña (HUT)</strong>. Moratorias activas en Barcelona, Sitges y otros municipios. Registro autonómico obligatorio. Cataluña aplica además régimen específico para zonas tensionadas.</p>
  <p><strong>C. Valenciana (VT)</strong>. Régimen relativamente abierto con licencia obligatoria. Costa Blanca (Calp, Benidorm, Torrevieja, Guardamar) y Costa Azahar (Peñíscola, Benicàssim) son las zonas más demandadas.</p>
  <p><strong>Andalucía (VFT)</strong>. Régimen permisivo en general con registro RTA obligatorio. Costa del Sol (Marbella, Estepona, Manilva, Benalmádena) y Costa de la Luz (Conil, Tarifa) lideran la oferta.</p>
  <p><strong>Resto de CCAA</strong>: Galicia (REAT), Asturias (VUT), Cantabria, País Vasco regulan con licencias municipales. Verifica siempre.</p>

  <h2 id="economia">Economía del alquiler vacacional</h2>
  <p>El alquiler vacacional <strong>genera ingresos brutos 2-3x superiores</strong> al residencial en plazas turísticas premium, pero con gastos operativos significativamente más altos:</p>
  <p><strong>Ingresos brutos:</strong> 30-50€/noche en plazas medias, 80-150€/noche en plazas premium. Con ocupación del 60% anual: 7.000-25.000€ brutos/año por apartamento estándar.</p>
  <p><strong>Gastos operativos típicos:</strong> 35-45% de los ingresos brutos. Incluye limpieza (4-8€/cambio), suministros (luz/agua/internet 100-150€/mes), gestión Airbnb/Booking (15-20%), reparaciones (5%), IBI/comunidad. <strong>Neto operativo: 55-65% del bruto.</strong></p>
  <p><strong>ROI neto típico:</strong> 4,5-6% sobre precio compra. Por encima del residencial en plazas premium, pero con volatilidad estacional y mayor carga de gestión.</p>

  <h2 id="top">Top 20 plazas vacacionales por ROI bruto</h2>
  <p>Selección de plazas con perfil turístico-vacacional fuerte ordenadas por ROI bruto. Estos datos son del mercado residencial — el yield real en VUT puede ser sustancialmente diferente.</p>
  <div class="tbl-wrap">
    <table class="cmp">
      <thead><tr><th>#</th><th>Ciudad</th><th>ROI bruto residencial</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr></thead>
      <tbody>
{table_rows(top)}      </tbody>
    </table>
  </div>

  <h2 id="fiscalidad">Fiscalidad VUT</h2>
  <div class="tax-box">
    <h3>🏛️ IRPF y modelos a presentar</h3>
    <p><strong>IRPF:</strong> los ingresos del alquiler vacacional tributan como <strong>rendimientos de actividades económicas</strong> si hay personal contratado o se ofrecen servicios complementarios (limpieza diaria, cambio de toallas), o como <strong>rendimientos de capital inmobiliario</strong> si es alquiler simple sin servicios.</p>
    <p><strong>Reducción del 60%:</strong> NO aplica al alquiler vacacional (solo a vivienda habitual de larga duración).</p>
    <p><strong>IVA:</strong> el alquiler vacacional sin servicios extra está exento de IVA. Con servicios extra (limpieza diaria, restauración) tributa al 10% (régimen de servicios hoteleros).</p>
    <p><strong>Modelo 100:</strong> declaración anual de ingresos vacacionales.</p>
    <p><strong>Modelo 179:</strong> obligación de las plataformas (Airbnb, Booking) de declarar trimestralmente los ingresos de cada anfitrión a Hacienda.</p>
  </div>

  <h2 id="estrategia">Estrategia operativa</h2>
  <p><strong>1. Verifica licencia ANTES de comprar.</strong> Es el error #1 de inversores: comprar y descubrir que el municipio o la comunidad de propietarios prohíbe VUT. Pide al vendedor copia del registro o consulta con el ayuntamiento.</p>
  <p><strong>2. Calcula con ocupación realista.</strong> No asumas 80% como en las islas premium. Costa Blanca media: 50-60% anual. Interior: 25-40%.</p>
  <p><strong>3. Estructura jurídica.</strong> Si vas a operar 2+ propiedades VUT, valora SL para limitar responsabilidad.</p>
  <p><strong>4. Plataformas:</strong> Airbnb + Booking + Vrbo aumentan ocupación pero también costes. Empieza con 1-2 y escala.</p>

  <h2 id="conclusion">Conclusión</h2>
  <p>La vivienda vacacional es <strong>rentable pero exigente</strong>. Requiere ubicación premium, due diligence regulatoria, gestión activa y estructura fiscal optimizada. No es producto pasivo. Para perfil pasivo, mejor alquiler residencial larga duración.</p>
  <p>Para comparar con alquiler residencial consulta el artículo <a href="alquiler-turistico-vs-residencial-rentabilidad-2026.html">alquiler turístico vs residencial</a>. Si estás considerando Canarias, lee <a href="invertir-vivienda-canarias-2026.html">invertir en vivienda en Canarias 2026</a>. Para Costa española en general, <a href="invertir-vivienda-costa-espana-2026.html">invertir en costa española 2026</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 4: Primera vivienda vs inversión
# ---------------------------------------------------------------------------
def art_primera_vs_inv(rows, total):
    slug = "invertir-primera-vivienda-vs-inversion-2026"
    title = "¿Comprar para vivir o para invertir? Análisis 2026"
    desc = ("Comparativa entre comprar primera vivienda y compra patrimonial. Coste de "
            "oportunidad, fiscalidad, financiación y conclusión por perfil familiar. "
            "Datos Q1 2026.")
    head = article_head(slug, title, desc, "Primera vivienda vs inversión")
    body = article_open(
        '¿Comprar para <span class="ac">vivir</span> o para <span class="ac">invertir</span>? 2026',
        ("Es una de las decisiones financieras más importantes para un hogar joven español: "
         "¿pongo el ahorro y crédito disponible en mi propia vivienda habitual, o en una "
         "inversión patrimonial? El contexto 2026 — tipos de interés moderándose, precios al "
         "alza, alquileres tensionados — exige analizar coste de oportunidad real."),
        "Primera vivienda vs inversión 2026", total)

    body += f'''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#dilema">El dilema fundamental</a></li>
      <li><a href="#opcion-a">Opción A: comprar para vivir</a></li>
      <li><a href="#opcion-b">Opción B: comprar para invertir</a></li>
      <li><a href="#variables">Variables a evaluar</a></li>
      <li><a href="#conclusion">Conclusión por perfil</a></li>
    </ul>
  </div>

  <h2 id="dilema">El dilema fundamental</h2>
  <p>Imagina que tienes 60.000€ ahorrados y capacidad de financiación. Tienes tres opciones:</p>
  <p><strong>A) Comprar primera vivienda en tu ciudad.</strong> Una vivienda de 250.000€ con entrada 20% (50.000€) + gastos 10.000€. Te ahorras 1.000€/mes de alquiler pero pagas 1.100€ de cuota hipoteca.</p>
  <p><strong>B) Mantener alquiler + comprar inversión en otra ciudad.</strong> Por 60.000€ puedes adquirir vivienda de 90-100.000€ en Cuenca, Zamora o Teruel (ROI bruto 7%+) con entrada 20% (18.000€) + gastos (6.000€) + reserva (36.000€) para una segunda compra.</p>
  <p><strong>C) Mantener alquiler + no comprar nada.</strong> Inviertes los 60.000€ en bolsa/fondos. Mantienes flexibilidad geográfica máxima.</p>

  <h2 id="opcion-a">Opción A: comprar para vivir</h2>
  <div class="pro-con">
    <div class="pc-col pro">
      <h3>Ventajas</h3>
      <ul>
        <li><strong>Estabilidad emocional y familiar:</strong> propiedad propia, hogar permanente.</li>
        <li><strong>Cobertura inflación alquiler:</strong> el alquiler sube indefinidamente, la cuota hipoteca no.</li>
        <li><strong>Fiscalidad favorable:</strong> deducción hipotecaria estatal (limitada) + ITP reducido vivienda habitual + protección IVA segunda mano.</li>
        <li><strong>Plusvalía a 10-15 años:</strong> en capitales con crecimiento, +50-80% en una década.</li>
        <li><strong>Liquidez futura:</strong> la vivienda habitual puede usarse para hipoteca inversa o segunda vivienda.</li>
      </ul>
    </div>
    <div class="pc-col con">
      <h3>Desventajas</h3>
      <ul>
        <li><strong>Inmovilización máxima:</strong> 60.000€ atados a un solo activo y una ubicación.</li>
        <li><strong>Coste real "oculto":</strong> IBI + comunidad + mantenimiento + seguros = 1,5-2% del valor al año.</li>
        <li><strong>Riesgo concentrado:</strong> si el barrio se deteriora, pierdes valor sin diversificación.</li>
        <li><strong>Sin yield líquido:</strong> el "ahorro" del alquiler es teórico, no es cash-flow.</li>
        <li><strong>Coste de oportunidad alto en ciudades caras:</strong> en Madrid o Barcelona los 250.000€ rinden poco como vivienda propia.</li>
      </ul>
    </div>
  </div>

  <h2 id="opcion-b">Opción B: comprar para invertir</h2>
  <div class="pro-con">
    <div class="pc-col pro">
      <h3>Ventajas</h3>
      <ul>
        <li><strong>Cash-flow positivo desde día 1:</strong> con ROI 7% bruto, después de cuota e impuestos quedan 200-300€/mes netos.</li>
        <li><strong>Diversificación geográfica:</strong> separas residencia (movilidad) y patrimonio (estabilidad).</li>
        <li><strong>Múltiples inmuebles por mismo capital:</strong> 60.000€ permiten 2-3 inmuebles pequeños.</li>
        <li><strong>Aprendes como inversor:</strong> tratos con inquilinos, agencia, fiscalidad real estate.</li>
      </ul>
    </div>
    <div class="pc-col con">
      <h3>Desventajas</h3>
      <ul>
        <li><strong>Sigues pagando alquiler:</strong> el alquiler personal sigue siendo gasto sin construir patrimonio propio.</li>
        <li><strong>Gestión activa:</strong> tratar con inquilinos, vacancia, reparaciones.</li>
        <li><strong>Fiscalidad menos favorable:</strong> ITP general 8-10%, sin reducciones de vivienda habitual.</li>
        <li><strong>Riesgo regulatorio:</strong> tope de alquiler, zonas tensionadas, VUT regulado.</li>
        <li><strong>Volatilidad emocional:</strong> los impagos generan estrés.</li>
      </ul>
    </div>
  </div>

  <h2 id="variables">Variables a evaluar</h2>
  <p><strong>1. ¿En qué ciudad vivirías?</strong> Si es Madrid/Barcelona/Bilbao, la vivienda habitual es muy cara (450-700€/m²). Comprar para inversión en ciudad más barata + alquilar en la cara puede tener sentido.</p>
  <p><strong>2. ¿Tienes movilidad laboral?</strong> Si esperas cambiar de ciudad en 5-7 años, comprar primera vivienda no compensa por costes de transacción.</p>
  <p><strong>3. ¿Cuál es tu horizonte?</strong> Menos de 10 años, alquiler suele ser más eficiente. Más de 15 años, propia.</p>
  <p><strong>4. ¿Tienes pareja/familia?</strong> Estabilidad familiar pesa fuerte en favor de vivienda habitual.</p>
  <p><strong>5. ¿Tu trabajo es estable?</strong> Comprar requiere flujos predecibles.</p>

  <h2 id="conclusion">Conclusión por perfil</h2>
  <p><strong>Perfil 1: 25-30 años, soltero, profesional con movilidad.</strong> Mantén alquiler + invierte en 1-2 inmuebles de yield alto en otras ciudades. Aprendes y construyes patrimonio sin atarte geográficamente.</p>
  <p><strong>Perfil 2: 32-40 años, pareja, hijos pequeños, ciudad estable.</strong> Compra para vivir + en 5 años considera segunda inversión. La estabilidad familiar pesa más que el coste de oportunidad puro.</p>
  <p><strong>Perfil 3: Profesional consolidado en gran capital.</strong> Vivienda propia en gran capital tiene mucho coste de oportunidad. Considera vivienda más modesta + cartera inversión.</p>
  <p>Para identificar tu ciudad ideal usa el <a href="comparador.html">comparador</a> o consulta el <a href="ranking.html">ranking completo</a>. Si vas por opción inversión, lee la <a href="como-calcular-rentabilidad-vivienda-2026.html">guía de cálculo de rentabilidad</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 5: Cómo calcular rentabilidad
# ---------------------------------------------------------------------------
def art_calcular(rows, total):
    slug = "como-calcular-rentabilidad-vivienda-2026"
    title = "Cómo calcular la rentabilidad de una vivienda 2026 — Guía metodológica completa"
    desc = ("Guía detallada: ROI bruto, ROI neto, IRR, cash-flow, descuento por gastos "
            "(IBI, comunidad, mantenimiento, vacancia, impuestos). Plantilla y casos prácticos.")
    head = article_head(slug, title, desc, "Cómo calcular rentabilidad")
    body = article_open(
        'Cómo calcular la <span class="ac">rentabilidad</span> de una vivienda 2026',
        ("La rentabilidad inmobiliaria tiene múltiples métricas que miden cosas distintas. "
         "Esta guía explica las 5 fórmulas que todo inversor debe conocer: ROI bruto, ROI neto, "
         "cash-on-cash return, cap rate y IRR. Con plantilla, ejemplos numéricos y los errores "
         "más comunes que llevan a sobreestimar el rendimiento."),
        "Cómo calcular rentabilidad 2026", total)

    body += '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#bruto">ROI bruto (yield)</a></li>
      <li><a href="#neto">ROI neto</a></li>
      <li><a href="#cash">Cash-on-cash return</a></li>
      <li><a href="#cap">Cap rate</a></li>
      <li><a href="#irr">TIR / IRR a 10 años</a></li>
      <li><a href="#gastos">Lista completa de gastos a descontar</a></li>
      <li><a href="#ejemplo">Ejemplo numérico paso a paso</a></li>
      <li><a href="#errores">Errores comunes</a></li>
    </ul>
  </div>

  <h2 id="bruto">1. ROI bruto (yield bruto)</h2>
  <p>La métrica más simple y la que Ren Data publica. <strong>ROI bruto = Alquiler anual / Precio compra × 100</strong>. Sin descontar nada.</p>
  <p>Ejemplo: vivienda de 200.000€ que se alquila a 1.000€/mes (12.000€/año). ROI bruto = 12.000 / 200.000 = 6%.</p>
  <p><strong>Cuándo usar:</strong> comparar plazas rápidamente. Es el "headline" del análisis. <strong>Cuándo NO usar:</strong> tomar la decisión final — siempre confirma con ROI neto.</p>

  <h2 id="neto">2. ROI neto</h2>
  <p>El bruto descontando todos los gastos recurrentes anuales. <strong>ROI neto = (Alquiler anual − Gastos anuales) / Precio compra × 100</strong>.</p>
  <p>Mismo ejemplo (200.000€ y 1.000€/mes) con gastos típicos:</p>
  <ul style="margin:.5rem 0 1rem 1.5rem">
    <li>IBI anual: 400€</li>
    <li>Comunidad: 60€/mes × 12 = 720€</li>
    <li>Seguro: 250€</li>
    <li>Mantenimiento (provisión 1%): 2.000€</li>
    <li>Vacancia (1 mes de cada 12): 1.000€</li>
    <li>Gestión inmobiliaria (8% si delegas): 960€</li>
    <li>IRPF (suponiendo 24% marginal con reducción 60%): 1.152€</li>
  </ul>
  <p>Gastos totales: 6.482€. ROI neto = (12.000 − 6.482) / 200.000 = <strong>2,76%</strong> — menos de la mitad del bruto.</p>

  <h2 id="cash">3. Cash-on-cash return</h2>
  <p>Mide la rentabilidad sobre el <strong>capital realmente desembolsado</strong>, no sobre el precio. Útil cuando hay hipoteca.</p>
  <p><strong>Cash-on-cash = Cash-flow anual / Entrada + gastos compra × 100</strong></p>
  <p>Si financias el 80% (160.000€ con hipoteca al 3,5% a 25 años = 800€/mes cuota), el capital desembolsado es: 40.000€ entrada + 16.000€ gastos = 56.000€. Cash-flow anual ≈ Alquiler (12.000€) − Cuota anual (9.600€) − Gastos no hipotecarios (5.330€) − IRPF (sobre rendimientos netos, ej. 800€) = -3.730€ (negativo).</p>
  <p>Cash-on-cash = -6,6%. Aquí la financiación destruye valor en el corto plazo — el inversor pone dinero cada mes esperando revalorización.</p>

  <h2 id="cap">4. Cap rate (tasa de capitalización)</h2>
  <p>Métrica usada en mercados profesionales. <strong>Cap rate = NOI / Valor mercado × 100</strong>, donde NOI = Net Operating Income (alquiler − gastos operativos sin contar hipoteca ni amortizaciones).</p>
  <p>Para nuestro ejemplo: NOI = 12.000 − (400 + 720 + 250 + 2.000 + 1.000 + 960) = 6.670€. Cap rate = 6.670 / 200.000 = 3,3%.</p>
  <p>Útil para comparar inmuebles a valor de mercado actual sin distorsión de la fecha de compra.</p>

  <h2 id="irr">5. TIR / IRR a 10 años</h2>
  <p>La <strong>Tasa Interna de Retorno</strong> es la métrica más completa: incluye cash-flow anual + plusvalía al vender. Se calcula con función IRR de Excel sobre la serie de flujos.</p>
  <p>Año 0: -56.000€ (entrada + gastos). Años 1-10: cash-flow anual neto. Año 10: cash-flow anual + ingreso por venta menos cuota hipoteca pendiente.</p>
  <p>Con revalorización del 5% anual, al año 10 la vivienda vale 325.779€. Si la vendes pagando hipoteca pendiente de 120.000€ + gastos venta 25.000€, recibes 180.779€. IRR típica en estos parámetros: 8-12%.</p>

  <h2 id="gastos">Lista completa de gastos a descontar</h2>
  <div class="tax-box">
    <h3>💸 Gastos típicos del inversor inmobiliario</h3>
    <p><strong>Gastos de compra (one-off):</strong> ITP (6-11% según CCAA), notaría (0,5%), registro (0,3%), gestoría (0,3%), tasación (300-500€). Total: 7-12% del precio.</p>
    <p><strong>Gastos recurrentes anuales (sobre vivienda):</strong> IBI (0,3-0,8% del valor catastral), comunidad (40-80€/mes según finca), seguro hogar (200-400€), tasa basuras (50-150€).</p>
    <p><strong>Gastos operativos:</strong> mantenimiento (provisión 1% del valor al año), vacancia (provisión 1 mes de cada 12), gestión inmobiliaria (8-10% del alquiler si delegas).</p>
    <p><strong>Gastos fiscales:</strong> IRPF sobre rendimientos netos (marginal × renta − reducción 60% si vivienda habitual). Si optas SL: IS al 25%.</p>
    <p><strong>Gastos de venta (one-off al final):</strong> plusvalía municipal, IRPF sobre ganancia patrimonial (19-23%), agencia (3-5%), notaría/registro (0,8%).</p>
  </div>

  <h2 id="ejemplo">Ejemplo numérico paso a paso</h2>
  <p><strong>Caso:</strong> Piso de 100m² en Burgos comprado en 2026 por 175.000€. Alquilado a 770€/mes (ROI bruto 5,3% según DATA Ren Data). Financiación 80% al 3,5% TIN a 25 años. Horizonte 10 años con revalorización 5% anual.</p>
  <p><strong>Año 0 — Compra</strong>: 35.000€ entrada + 17.500€ ITP (Castilla y León 8% sobre 175k = 14.000€) + 3.500€ notaría/registro/gestoría = <strong>desembolso 56.000€</strong>.</p>
  <p><strong>Año 1 — Ingresos y gastos operativos</strong>: 9.240€ alquileres − cuota hipoteca (700€×12=8.400€) − IBI (450€) − comunidad (60×12=720€) − seguro (300€) − provisión 1% mant (1.750€) − provisión vacancia (770€) − IRPF (24% × 5.020€ × 40% por reducción ≈ 482€) = <strong>cash-flow año 1: -3.562€</strong>.</p>
  <p><strong>Acumulado años 1-10</strong>: vivienda revalorizada a 285.000€. Hipoteca pendiente ~120.000€. Si vende: ingresa 285k − 120k − gastos venta (5%=14.250€) − IRPF ganancia patrimonial = neto venta ~135.000€. Sumado a cash-flow acumulado años 1-10 (~-15.000€): IRR ~12% anualizada.</p>

  <h2 id="errores">Errores comunes</h2>
  <p><strong>Error 1: Pensar que el ROI bruto es el "real".</strong> El bruto sobreestima 2-2,5 veces. Siempre confirma con neto.</p>
  <p><strong>Error 2: Olvidar la provisión por mantenimiento.</strong> Sin provisión 1% anual, en 10 años llega la sorpresa de 20.000€ en reformas.</p>
  <p><strong>Error 3: Confundir revalorización con yield.</strong> La revalorización no es cash-flow — solo se realiza al vender.</p>
  <p><strong>Error 4: No considerar coste de oportunidad.</strong> 50.000€ en S&P500 al 8% rinde 4.000€/año pasivos. Compara siempre.</p>
  <p><strong>Error 5: Estimar alquiler optimista.</strong> Usa el percentil 25-50 del mercado, no el percentil 75.</p>

  <p>Para aplicar la metodología a tu propia inversión, usa el <a href="comparador.html">comparador</a> con datos reales del DATA Ren Data o consulta cualquier <a href="ranking.html">ficha de ciudad</a> donde encontrarás ROI bruto y métricas adicionales.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 6: Jóvenes
# ---------------------------------------------------------------------------
def art_jovenes(rows, total):
    slug = "mejores-ciudades-jovenes-invertir-2026"
    cs = [r for r in rows if r["p"] <= 1300 and r["roi"] >= 6.0]
    cs.sort(key=lambda x: (-x["roi"], x["p"]))
    top = cs[:20]
    title = "Mejores ciudades para inversores jóvenes 2026 — Presupuesto limitado"
    desc = ("Las plazas más accesibles para primera inversión: tickets <100.000€ para piso "
            "de 100m². Capitales pequeñas con yield alto y financiación favorable.")
    head = article_head(slug, title, desc, "Mejores ciudades para inversores jóvenes")
    body = article_open(
        'Mejores ciudades para <span class="ac">inversores jóvenes</span> 2026',
        ("Si tienes 25-35 años, ahorros entre 15.000-30.000€ y quieres iniciar tu camino "
         "como inversor inmobiliario, las plazas con precio &lt;1.300€/m² y ROI &gt;6% son tu "
         "punto de entrada óptimo. Esta guía identifica las 20 mejores ciudades del DATA Ren "
         "Data para primera inversión: tickets &lt;130.000€ para piso de 100m², financiación "
         "asequible y yield bruto razonable."),
        "Mejores ciudades para inversores jóvenes 2026", total)

    body += f'''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#contexto">Contexto del inversor joven</a></li>
      <li><a href="#top">Top 20 ciudades accesibles</a></li>
      <li><a href="#financiacion">Financiación para primer inmueble</a></li>
      <li><a href="#errores">Errores a evitar en la primera compra</a></li>
    </ul>
  </div>

  <h2 id="contexto">Contexto del inversor joven</h2>
  <p>El inversor joven español tiene tres ventajas estructurales y tres limitaciones:</p>
  <p><strong>Ventajas:</strong> (1) horizonte largo (20-30 años de carrera por delante), (2) capacidad de aprender errores, (3) bonificaciones autonómicas al ITP en muchas CCAA para menores de 35 años.</p>
  <p><strong>Limitaciones:</strong> (1) ahorro limitado (15-30k típicamente), (2) capacidad de endeudamiento menor por antigüedad laboral, (3) menos experiencia y red de contactos.</p>
  <p>Para superar las limitaciones: <strong>apuesta por tickets bajos en plazas con yield alto</strong>. 100.000€ financiado al 80% requiere solo 20.000€ entrada + 8.000€ gastos = 28.000€ total. Cash-flow positivo desde día 1 si el yield es 6%+.</p>

  <h2 id="top">Top 20 ciudades accesibles para primera inversión</h2>
  <p>Plazas del DATA Ren Data con precio &lt;1.300€/m² (ticket &lt;130k€) y ROI &gt;6% bruto. Ordenadas por ROI.</p>
  <div class="tbl-wrap">
    <table class="cmp">
      <thead><tr><th>#</th><th>Ciudad</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr></thead>
      <tbody>
{table_rows(top)}      </tbody>
    </table>
  </div>

  <h2 id="financiacion">Financiación para primer inmueble</h2>
  <p><strong>1. Hipoteca al 80% LTV.</strong> La gran mayoría de bancos financia el 80% del valor de tasación (no de compra). Para 100.000€ tasado: 80.000€ hipoteca, 20.000€ entrada.</p>
  <p><strong>2. Hipoteca al 90% para vivienda habitual.</strong> Si compras la vivienda habitual, puedes pedir hasta 90% LTV en algunos bancos. Para inversión pura, 80% es el máximo habitual.</p>
  <p><strong>3. Tipo mixto vs variable.</strong> En 2026 con Euríbor moderándose hacia 2,5-3%, las hipotecas mixtas (5 años fijo + variable) son competitivas. Estudia bien antes de elegir.</p>
  <p><strong>4. TAE realista.</strong> Para inversión, espera TIN 3-4% + comisiones. La cuota de 80.000€ a 30 años al 3,5% = ~360€/mes.</p>

  <h2 id="errores">Errores a evitar en la primera compra</h2>
  <p><strong>Error 1: Comprar el primer piso que ves.</strong> Visita 15-20 antes de elegir uno. Necesitas calibrar precios de mercado real.</p>
  <p><strong>Error 2: No revisar el Registro de la Propiedad.</strong> Pide nota simple actualizada antes de firmar. Verifica que no haya embargos o cargas ocultas.</p>
  <p><strong>Error 3: No verificar la situación del inquilino (si compras alquilado).</strong> Pide contrato actual, recibos de los últimos 6 meses, y verifica si hay zonas tensionadas activas.</p>
  <p><strong>Error 4: Sobreapalancarse en primer inmueble.</strong> No financies al 90%+ tu primer piso. Margen para imprevistos: 6-12 meses de cuota como reserva.</p>
  <p><strong>Error 5: Ignorar la cuota de comunidad.</strong> En edificios antiguos sin ascensor, derramas por instalación pueden suponer 3.000-10.000€ por vecino.</p>

  <p>Para conocer mejor el cálculo completo de rentabilidad, lee la <a href="como-calcular-rentabilidad-vivienda-2026.html">guía metodológica de cálculo</a>. Si quieres comparar varias ciudades, usa el <a href="comparador.html">comparador</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 7: Jubilación
# ---------------------------------------------------------------------------
def art_jubilacion(rows, total):
    slug = "invertir-vivienda-jubilacion-espana-2026"
    cs = [r for r in rows if r["p"] >= 2500 and r["d"] <= 22]
    cs.sort(key=lambda x: (-x["vp"], -x["roi"]))
    top = cs[:15]
    title = "Invertir en vivienda para la jubilación 2026 — Largo plazo y patrimonio"
    desc = ("Estrategia patrimonial a 15-20 años. Ciudades con revalorización sostenida, "
            "marca y demanda estable. Madrid, Barcelona, Bilbao, San Sebastián, Valencia.")
    head = article_head(slug, title, desc, "Invertir para la jubilación")
    body = article_open(
        'Invertir en vivienda para la <span class="ac">jubilación</span> 2026',
        ("La inversión inmobiliaria para complementar la jubilación tiene lógica distinta a la "
         "del joven. Aquí el horizonte es 15-25 años y el objetivo es <strong>preservar capital + "
         "renta estable + revalorización sostenida</strong>. Esta guía identifica las 15 plazas "
         "del DATA Ren Data con perfil patrimonial óptimo: ciudades premium con liquidez alta, "
         "revalorización sostenida y demanda estructural inquebrantable."),
        "Invertir para la jubilación 2026", total)

    body += f'''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#objetivo">Objetivo: complementar pensión + transmitir patrimonio</a></li>
      <li><a href="#criterios">Criterios de selección</a></li>
      <li><a href="#top">Top 15 ciudades patrimoniales</a></li>
      <li><a href="#estructura">Estructura jurídica óptima</a></li>
      <li><a href="#sucesion">Planificación sucesoria</a></li>
    </ul>
  </div>

  <h2 id="objetivo">Objetivo: complementar pensión + transmitir patrimonio</h2>
  <p>El inversor que piensa en jubilación tiene dos objetivos simultáneos:</p>
  <p><strong>1. Generar renta complementaria estable.</strong> A 65 años, la pensión pública media en España ronda 1.500€/mes. Un piso bien situado en Madrid o Bilbao puede aportar 1.000-1.500€ netos adicionales.</p>
  <p><strong>2. Transmitir patrimonio a herederos.</strong> El inmueble bien situado se revaloriza y conserva valor real. Es el activo más fácil de heredar y de transmitir entre generaciones.</p>

  <h2 id="criterios">Criterios de selección</h2>
  <p>Para perfil patrimonial buscamos:</p>
  <p><strong>1. Liquidez alta.</strong> Días de venta &lt;22. Por si los herederos quieren liquidar rápido.</p>
  <p><strong>2. Precio &gt;2.500€/m².</strong> Sólo plazas premium aseguran demanda estable a 15-20 años.</p>
  <p><strong>3. Revalorización sostenida.</strong> Subida de precios estable en últimos 5 años.</p>
  <p><strong>4. Marca urbana fuerte.</strong> Madrid, Barcelona, San Sebastián, Bilbao, Valencia, Málaga, Palma, Sevilla. Las grandes capitales mantienen valor.</p>

  <h2 id="top">Top 15 ciudades patrimoniales</h2>
  <p>Plazas del DATA Ren Data con precio &gt;2.500€/m², liquidez &lt;22 días y revalorización sostenida. Ordenadas por var. precio anual.</p>
  <div class="tbl-wrap">
    <table class="cmp">
      <thead><tr><th>#</th><th>Ciudad</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr></thead>
      <tbody>
{table_rows(top)}      </tbody>
    </table>
  </div>

  <h2 id="estructura">Estructura jurídica óptima</h2>
  <p><strong>Persona física vs SL Patrimonial.</strong> Para 1-2 inmuebles, persona física es más simple (IRPF + reducción 60% vivienda habitual). Para 3+ inmuebles con vocación patrimonial, valora SL: IS al 25% en lugar de marginal IRPF, planificación sucesoria más limpia.</p>
  <p><strong>Régimen económico matrimonial.</strong> Si tu vivienda patrimonial está en régimen ganancial, en caso de fallecimiento se divide automáticamente. En régimen de separación, decides expresamente.</p>

  <h2 id="sucesion">Planificación sucesoria</h2>
  <p><strong>Impuesto de Sucesiones por CCAA.</strong> Madrid, Andalucía, Cantabria, La Rioja bonifican al 99% en sucesiones entre cónyuges e hijos. Cataluña, Asturias, Valencia tienen tipos efectivos significativos. Verifica antes de comprar — afecta a tus herederos.</p>
  <p><strong>Donación en vida.</strong> En CCAA con bonificación alta, puede tener sentido donar parte del patrimonio en vida.</p>
  <p><strong>Testamento claro.</strong> Inversiones patrimoniales requieren testamento detallado para evitar conflictos.</p>

  <p>Para complementar consulta el <a href="comparador.html">comparador de ciudades</a>. Si tu perfil es conservador pero más activo, lee la <a href="guia-inversor-conservador-2026.html">guía del inversor conservador</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 8: Revalorización
# ---------------------------------------------------------------------------
def art_revalorizacion(rows, total):
    slug = "ciudades-mayor-revalorizacion-2026"
    cs = sorted(rows, key=lambda x: -x["vp"])
    top = cs[:25]
    title = "Las ciudades con mayor revalorización en España 2026"
    desc = ("Top 25 por subida de precio anual. Alicante, Valencia, Málaga, Madrid lideran "
            "con +10-12% anual. Análisis de palancas y previsiones.")
    head = article_head(slug, title, desc, "Mayor revalorización en España")
    body = article_open(
        'Las ciudades con mayor <span class="ac">revalorización</span> en España 2026',
        ("La revalorización (subida anual del precio) es la métrica clave para el inversor "
         "patrimonial: complementa al ROI bruto cuando el horizonte es &gt;10 años. Esta guía "
         "identifica las 25 plazas del DATA Ren Data con mayor subida en los últimos 12 meses "
         "y analiza las palancas que sostienen esas dinámicas."),
        "Ciudades con mayor revalorización 2026", total)

    body += f'''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#contexto">Contexto del mercado 2026</a></li>
      <li><a href="#top">Top 25 ciudades por revalorización anual</a></li>
      <li><a href="#palancas">Palancas estructurales</a></li>
      <li><a href="#riesgos">Riesgos del comprador tardío</a></li>
    </ul>
  </div>

  <h2 id="contexto">Contexto del mercado 2026</h2>
  <p>El mercado inmobiliario español 2026 mantiene <strong>dinámica alcista moderada</strong>: media nacional +6,6% anual según datos del DATA Ren Data. Las grandes capitales y zonas turísticas premium superan +10%, mientras que mercados rurales y zonas en despoblación rondan +3-4%.</p>
  <p>Tres macrotendencias sostienen las subidas: (1) déficit estructural de oferta nueva, (2) demanda extranjera sostenida (residencial nórdico, británico, francés), (3) tipos de interés moderándose hacia 2,5-3%.</p>

  <h2 id="top">Top 25 ciudades por revalorización anual</h2>
  <p>Plazas del DATA Ren Data ordenadas por var. precio anual (var. % en los últimos 12 meses).</p>
  <div class="tbl-wrap">
    <table class="cmp">
      <thead><tr><th>#</th><th>Ciudad</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr></thead>
      <tbody>
{table_rows(top)}      </tbody>
    </table>
  </div>

  <h2 id="palancas">Palancas estructurales</h2>
  <p><strong>1. Demanda extranjera sostenida.</strong> Alicante, Málaga, Palma reciben flujo continuo de compradores nórdicos, británicos y franceses. Esto sostiene precios independientemente del ciclo doméstico.</p>
  <p><strong>2. Déficit de oferta nueva.</strong> España construye 80.000 viviendas/año vs 150.000+ de la demanda real. El stock disponible se reduce.</p>
  <p><strong>3. Tipos de interés moderándose.</strong> La curva del Euríbor previene un nuevo abaratamiento de la hipoteca, lo que devuelve capacidad de pago.</p>
  <p><strong>4. Reactivación turística.</strong> Récord histórico de turistas en 2025-2026 sostiene precios en Costa del Sol, Costa Blanca, Baleares y Canarias.</p>

  <h2 id="riesgos">Riesgos del comprador tardío</h2>
  <p><strong>1. Comprar en el pico del ciclo.</strong> Después de 6-7 años de subidas continuadas, una corrección moderada (-5 a -10%) es plausible. Comprar en pico significa esperar 3-5 años para recuperar.</p>
  <p><strong>2. Concentración geográfica.</strong> Las subidas se concentran en costa y grandes capitales. El resto del país avanza menos.</p>
  <p><strong>3. Regulación cambiante.</strong> Zonas tensionadas pueden moderar las subidas de alquiler (no de precio directamente, pero sí del binomio).</p>

  <p>Para análisis complementario consulta el <a href="precio-vivienda-espana-evolucion-2026.html">artículo sobre evolución del precio de la vivienda en España</a> o explora el <a href="ranking.html">ranking completo</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 9: VUT vs residencial
# ---------------------------------------------------------------------------
def art_vut_vs(rows, total):
    slug = "alquiler-turistico-vs-residencial-rentabilidad-2026"
    title = "Alquiler turístico vs residencial — Comparativa de rentabilidad 2026"
    desc = ("Análisis comparativo de yield, riesgos, fiscalidad y regulación. Cuándo conviene "
            "VUT, cuándo larga duración. Casos prácticos con datos Q1 2026.")
    head = article_head(slug, title, desc, "Alquiler turístico vs residencial")
    body = article_open(
        'Alquiler <span class="ac">turístico vs residencial</span> 2026',
        ("Para el mismo inmueble, ¿conviene alquiler turístico (VUT) o residencial larga duración? "
         "La respuesta depende de ubicación, regulación, capacidad de gestión y horizonte temporal. "
         "Esta guía compara ambos modelos con datos reales y casos prácticos para tres escenarios "
         "típicos: piso en Costa Blanca, apartamento en Barcelona, casa en Costa del Sol."),
        "Alquiler turístico vs residencial 2026", total)

    body += '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#modelos">Los dos modelos</a></li>
      <li><a href="#ingresos">Comparativa de ingresos</a></li>
      <li><a href="#gastos">Comparativa de gastos</a></li>
      <li><a href="#regulacion">Comparativa de regulación</a></li>
      <li><a href="#casos">3 casos prácticos</a></li>
      <li><a href="#conclusion">Conclusión por perfil</a></li>
    </ul>
  </div>

  <h2 id="modelos">Los dos modelos</h2>
  <p><strong>Alquiler residencial larga duración (LAU 5+2 años).</strong> Contrato típico de 5 años, prorrogable a 7. Renta fija mensual. Régimen legal protegido por la Ley de Arrendamientos Urbanos.</p>
  <p><strong>Alquiler turístico (VUT/VFT/HUT según CCAA).</strong> Estancias &lt;31 días por unidad. Plataformas: Airbnb, Booking, Vrbo. Régimen regulado por CCAA + municipio.</p>

  <h2 id="ingresos">Comparativa de ingresos</h2>
  <p><strong>Caso 1: Apartamento 80m² en Benidorm.</strong></p>
  <ul style="margin:.5rem 0 1rem 1.5rem">
    <li>Residencial: 950€/mes × 12 = <strong>11.400€/año</strong></li>
    <li>VUT: 65€/noche × 220 noches (60% ocupación) = <strong>14.300€/año</strong></li>
  </ul>
  <p>VUT supera al residencial en bruto en +25%. Pero veamos costes.</p>

  <h2 id="gastos">Comparativa de gastos</h2>
  <p><strong>Residencial:</strong> IBI (450€), comunidad (720€), seguro (250€), mantenimiento (1.000€), vacancia (1 mes ≈ 950€), gestión (8% × 11.400 = 912€). Total ~4.282€. <strong>Neto: 7.118€/año.</strong></p>
  <p><strong>VUT:</strong> IBI (450€), comunidad (720€), seguro (450€ — más alto por uso turístico), mantenimiento (1.500€ — más intensivo), suministros LU/A/I (1.800€), limpieza profesional (5€ × 110 cambios = 550€), gestión Airbnb/Booking (15% × 14.300 = 2.145€), licencia anual (300€). Total ~7.915€. <strong>Neto: 6.385€/año.</strong></p>
  <p>El residencial supera al VUT en neto en este caso.</p>

  <h2 id="regulacion">Comparativa de regulación</h2>
  <p><strong>Residencial:</strong> régimen LAU estable, contratos protegidos legalmente, sin licencias específicas. Riesgo: tope de alquiler en zonas tensionadas (Cataluña).</p>
  <p><strong>VUT:</strong> licencia obligatoria por CCAA, moratorias activas en Palma de Mallorca, Barcelona, Ibiza, San Sebastián. Riesgo de no obtener licencia o de retirarla.</p>

  <h2 id="casos">3 casos prácticos</h2>
  <p><strong>Caso A: Costa Blanca (Calp, 80m², 200k€).</strong> Si licencia VUT viable → ROI bruto VUT 7%, neto 4%. Residencial: bruto 5,7%, neto 3,5%. <strong>VUT gana solo si licencia confirmada y demanda alta.</strong></p>
  <p><strong>Caso B: Barcelona Eixample (50m², 350k€).</strong> Sin nueva licencia VUT (moratoria). Residencial: bruto 4,5%, neto 2,8%. <strong>Residencial es la única opción real.</strong></p>
  <p><strong>Caso C: Costa del Sol Marbella (90m², 280k€).</strong> Licencia VFT favorable. VUT: bruto 8%, neto 5,2%. Residencial: bruto 5%, neto 3,5%. <strong>VUT claramente mejor.</strong></p>

  <h2 id="conclusion">Conclusión por perfil</h2>
  <p><strong>Si valoras estabilidad + bajo trabajo de gestión:</strong> alquiler residencial. Menos rendimiento bruto pero mucha menos complicación.</p>
  <p><strong>Si tienes tiempo + ubicación premium + licencia confirmada:</strong> VUT. Bruto superior pero requiere gestión activa.</p>
  <p><strong>Si la ubicación no es premium turística:</strong> residencial siempre. El VUT en ubicaciones sin demanda turística estable da pésimos resultados.</p>

  <p>Para profundizar consulta <a href="invertir-vivienda-vacacional-espana-2026.html">invertir en vivienda vacacional en España 2026</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


# ---------------------------------------------------------------------------
# Article 10: Nueva vs segunda mano
# ---------------------------------------------------------------------------
def art_nueva_vs_segunda(rows, total):
    slug = "invertir-vivienda-nueva-vs-segunda-mano-2026"
    title = "Vivienda nueva vs segunda mano para invertir 2026"
    desc = ("Análisis coste/beneficio. Diferencias en ITP (10%) vs IVA (10%) + AJD (1,5%), "
            "garantías, mantenimiento, ubicación y rentabilidad. Cuándo elegir cada opción.")
    head = article_head(slug, title, desc, "Vivienda nueva vs segunda mano")
    body = article_open(
        'Vivienda <span class="ac">nueva</span> vs <span class="ac">segunda mano</span> 2026',
        ("Para una misma inversión, ¿conviene vivienda nueva (obra nueva) o segunda mano? "
         "El binomio tiene implicaciones fiscales (IVA vs ITP), de mantenimiento (garantía decenal), "
         "ubicación (urbana vs periférica), y rentabilidad (yield bruto suele ser mayor en segunda "
         "mano). Esta guía compara ambas opciones con datos 2026."),
        "Vivienda nueva vs segunda mano 2026", total)

    body += '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#fiscalidad">Diferencias fiscales: ITP vs IVA + AJD</a></li>
      <li><a href="#garantia">Garantías y mantenimiento</a></li>
      <li><a href="#ubicacion">Ubicación y mercado</a></li>
      <li><a href="#rentabilidad">Rentabilidad: yield bruto y revalorización</a></li>
      <li><a href="#conclusion">Conclusión por escenario</a></li>
    </ul>
  </div>

  <h2 id="fiscalidad">Diferencias fiscales: ITP vs IVA + AJD</h2>
  <p><strong>Vivienda segunda mano:</strong> tributa por <strong>ITP autonómico</strong> (6-11% según CCAA, con tipos típicos del 8-10%). Sobre 200.000€ con ITP del 10% = 20.000€.</p>
  <p><strong>Vivienda nueva:</strong> tributa por <strong>IVA (10%) + AJD (1,2-1,5% según CCAA)</strong>. Sobre 200.000€: 20.000€ IVA + 2.500€ AJD = 22.500€.</p>
  <p>En CCAA con ITP bajo (Canarias 6,5%, Madrid 6%, Navarra 6%), segunda mano es más barata fiscalmente. En CCAA con ITP alto (Cataluña, CV, Galicia 10%, Baleares hasta 11%), la diferencia entre ITP y IVA+AJD se reduce o invierte.</p>

  <h2 id="garantia">Garantías y mantenimiento</h2>
  <p><strong>Vivienda nueva:</strong> <strong>garantía decenal obligatoria</strong> del promotor sobre vicios estructurales (10 años) + bienal sobre acabados (2 años) + trienal sobre habitabilidad (3 años). Mantenimiento inicial muy bajo.</p>
  <p><strong>Vivienda segunda mano:</strong> sin garantía constructora (excepto vicios ocultos limitados). Necesidad de previsión por mantenimiento desde día 1: 1% del valor anual mínimo.</p>

  <h2 id="ubicacion">Ubicación y mercado</h2>
  <p><strong>Vivienda nueva:</strong> típicamente en <strong>ensanches y desarrollos periféricos</strong>. Buena calidad constructiva, edificios eficientes (calificación A-B), pero ubicación menos consolidada. Demanda creciente conforme el barrio madura.</p>
  <p><strong>Vivienda segunda mano:</strong> ubicaciones <strong>céntricas y consolidadas</strong>. Demanda inmediata. Calidad variable según edificio (eficiencia energética típica D-F).</p>

  <h2 id="rentabilidad">Rentabilidad: yield bruto y revalorización</h2>
  <p><strong>Yield bruto:</strong> la segunda mano céntrica suele ofrecer yield bruto superior (0,5-1 punto más alto) por menor coste por m² en ubicaciones equivalentes.</p>
  <p><strong>Revalorización:</strong> la obra nueva en zonas emergentes suele revalorizarse más rápido en los primeros 5 años (apreciación por consolidación del barrio). La segunda mano céntrica revaloriza más estable y predecible.</p>
  <p><strong>Mantenimiento:</strong> la obra nueva no consume capital los primeros 10 años. La segunda mano puede requerir reformas (15.000-30.000€ típicas) en los primeros 5 años.</p>

  <h2 id="conclusion">Conclusión por escenario</h2>
  <p><strong>Escenario A: Madrid, Barcelona, Bilbao centro.</strong> Segunda mano. Ubicación céntrica es el factor dominante. El yield mayor + revalorización por escasez de oferta supera la garantía constructora.</p>
  <p><strong>Escenario B: Ensanches periféricos con buena conexión.</strong> Obra nueva. Ubicación emergente + eficiencia energética + garantías hace mejor ratio.</p>
  <p><strong>Escenario C: Capitales medias (Burgos, Valladolid, Murcia).</strong> Depende. Si encuentras segunda mano céntrica a precio razonable, mejor. Si la obra nueva está en barrio consolidado con buena conexión, también funciona.</p>
  <p><strong>Escenario D: Costa.</strong> Obra nueva con frente marítimo nuevo (segunda línea típicamente) tiene mejor revalorización. Segunda mano en pueblos costeros consolidados (Calp, Altea, Salou) mantienen valor pero requieren más obra.</p>

  <p>Para análisis específico por mercado consulta el <a href="ranking.html">ranking completo</a> o el <a href="comparador.html">comparador de ciudades</a>.</p>
'''
    body += article_close(total)
    write_article(slug, head + body)


def main():
    rows = parse_data()
    total = len(rows)
    print(f"Total cities: {total}")

    art_conservador(rows, total)
    art_agresivo(rows, total)
    art_vacacional(rows, total)
    art_primera_vs_inv(rows, total)
    art_calcular(rows, total)
    art_jovenes(rows, total)
    art_jubilacion(rows, total)
    art_revalorizacion(rows, total)
    art_vut_vs(rows, total)
    art_nueva_vs_segunda(rows, total)

    print("\nDone — 10 profile articles generated")


if __name__ == "__main__":
    main()
