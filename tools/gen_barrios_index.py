# -*- coding: utf-8 -*-
"""Genera rendata_beta/barrios.html: índice con grid de las 50 ciudades."""
import os, re, json
from barrios_data import CITIES
from gen_barrios import PROFILES, price_of, eur, esc

OUT = os.path.join(os.path.dirname(__file__), "..", "rendata_beta")

# Orden por población: reutiliza el orden del índice vivir-en-espana.html
with open(os.path.join(OUT, "vivir-en-espana.html"), encoding="utf-8") as f:
    src = f.read()
m = re.search(r'"ItemList".*?"itemListElement":(\[.*?\])\}', src, re.S)
order = [re.search(r'vivir-en-(.*?)\.html', it["url"]).group(1)
         for it in json.loads(m.group(1))]
# añade cualquier ciudad que faltara, por si acaso
order += [s for s in CITIES if s not in order]
order = [s for s in order if s in CITIES]

CCAA_NAME = {
    "C. de Madrid": "C. de Madrid", "Cataluña": "Cataluña", "Andalucía": "Andalucía",
    "C. Valenciana": "C. Valenciana", "Galicia": "Galicia", "País Vasco": "País Vasco",
    "Castilla y León": "Castilla y León", "Canarias": "Canarias", "Asturias": "Asturias",
    "R. de Murcia": "R. de Murcia", "Aragón": "Aragón", "Navarra": "Navarra",
    "Cantabria": "Cantabria", "La Rioja": "La Rioja", "Islas Baleares": "Islas Baleares",
    "Castilla-La Mancha": "Castilla-La Mancha", "Extremadura": "Extremadura",
}

HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Barrios de las 50 mayores ciudades de España: dónde vivir y comprar en 2026. Mapa de barrios por ciudad con perfil, precio medio €/m² por zona, transporte y recomendaciones por perfil de comprador.">
<title>Barrios de España 2026 — Dónde vivir y comprar por ciudad | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="Barrios de España 2026 — Guía por ciudad">
<meta property="og:description" content="Mapa de barrios de las 50 mayores ciudades de España: perfil, precio €/m² por zona, transporte y dónde comprar según tu perfil.">
<meta property="og:url" content="https://rendata.es/barrios.html">
<meta property="og:image" content="https://rendata.es/img/madrid.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Barrios de España 2026 — Guía por ciudad">
<meta name="twitter:description" content="Mapa de barrios de las 50 mayores ciudades de España: perfil, precio €/m² por zona, transporte y dónde comprar según tu perfil.">
<meta name="twitter:image" content="https://rendata.es/img/madrid.webp">
<link rel="canonical" href="https://rendata.es/barrios.html">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">{jsonld}</script>
<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
<link rel="stylesheet" href="/css/nav.css">
<style>
.bc{{max-width:1200px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}}
.bc a{{color:var(--muted);text-decoration:none;font-weight:500}}.bc a:hover{{color:var(--blue);text-decoration:underline}}
.bc-sep{{color:#cbd5e1}}.bc-cur{{color:var(--text);font-weight:600}}
.ve-hero{{background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:2.5rem 1.5rem;text-align:center}}
.ve-hero-inner{{max-width:880px;margin:0 auto}}
.ve-hero h1{{color:#fff;font-size:clamp(1.9rem,4vw,2.7rem);line-height:1.15;letter-spacing:-.025em;margin:0 0 .65rem;font-weight:800}}
.ve-hero-tag{{display:inline-flex;align-items:center;gap:.45rem;font-size:.75rem;font-weight:600;letter-spacing:.04em;background:rgba(255,255,255,.18);backdrop-filter:blur(6px);padding:.4rem .85rem;border-radius:99px;margin-bottom:.85rem}}
.ve-hero .lead{{font-size:1.05rem;line-height:1.55;color:rgba(255,255,255,.92);max-width:720px;margin:.4rem auto 0}}
.ve-main{{max-width:1200px;margin:1.6rem auto;padding:0 1.5rem}}
.ve-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;margin:1rem 0 2rem}}
.ve-card{{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}}
.ve-card:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(15,23,42,.08);border-color:var(--blue,#1a56db)}}
.ve-imgwrap{{aspect-ratio:16/9;background:#e2e8f0;overflow:hidden;position:relative}}
.ve-imgwrap img{{width:100%;height:100%;object-fit:cover;display:block}}
.ve-body{{padding:.95rem 1.05rem 1.05rem;display:flex;flex-direction:column;gap:.3rem}}
.ve-h{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.35rem;gap:.5rem}}
.ve-name{{font-weight:800;font-size:1.05rem;color:var(--text,#0e1828);letter-spacing:-.015em}}
.ve-ccaa{{font-size:.7rem;color:var(--muted,#64748b);font-weight:600;text-align:right}}
.ve-row{{display:flex;justify-content:space-between;font-size:.82rem;color:var(--text2,#475569);padding:.1rem 0}}
.ve-k{{color:var(--muted,#64748b)}}
.ve-v{{font-weight:700;color:var(--text,#0e1828);font-variant-numeric:tabular-nums}}
.ve-cta{{margin-top:.55rem;font-size:.84rem;font-weight:700;color:var(--blue,#1a56db);letter-spacing:-.01em}}
.ve-card:hover .ve-cta{{color:#0e2a6b}}
.ve-intro{{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:12px;padding:1.2rem 1.4rem;margin:1.2rem 0 1.4rem;font-size:.95rem;line-height:1.65;color:var(--text2,#475569)}}
.ve-intro strong{{color:var(--text,#0e1828)}}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){{dataLayer.push(arguments);}}gtag('js', new Date());gtag('config', 'G-0M57323B51');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6236025065305645" crossorigin="anonymous"></script>
</head>
<body>

<header>
  <a href="/" class="logo"><img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA"></a>
  <nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="mob-nav-links">
      <a href="/">🏠 Ciudades</a>
      <a href="/ranking.html">📊 Ranking</a>
      <a href="/analisis.html">📈 Análisis</a>
      <a href="/vivir-en-espana.html">🏡 Vivir en…</a>
      <a href="/barrios.html">🗺️ Barrios</a>
      <a href="/comparador.html">⚖️ Comparar</a><a href="/simulador-comprar-vs-alquilar.html">🔄 Comprar vs alquilar</a><a href="/calculadora-hipoteca.html">💶 Calculadora hipoteca</a>
      <a href="/metodologia.html">📊 Metodología</a>
      <a href="/glosario.html">📖 Glosario</a>
      <a href="/guia-inversor.html">🎯 Guía inversor</a>
      <a href="/sobre.html">ℹ️ Sobre</a>
    </div>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/vivir-en-espana.html">Vivir en…</a>
    <a href="/comparador.html">Comparador</a><a href="/simulador-comprar-vs-alquilar.html">Comprar vs alquilar</a><a href="/calculadora-hipoteca.html">Calculadora hipoteca</a>
    <a href="/metodologia.html">Metodología</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/guia-inversor.html">Guía</a>
    <a href="/sobre.html">Sobre</a>
  </nav>
</header>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">Inicio</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">Barrios</span>
</nav>

<section class="ve-hero">
  <div class="ve-hero-inner">
    <div class="ve-hero-tag">🗺️ Mapa de barrios · Q2 2026</div>
    <h1>Barrios de España — el mapa de cada ciudad en 2026</h1>
    <p class="lead">Dónde vivir y dónde comprar en las 50 mayores ciudades de España. Barrios reales por perfil, precio medio €/m² por zona, transporte y recomendaciones según tu perfil de comprador.</p>
  </div>
</section>

<main class="ve-main">

  <div class="ve-intro">
    <strong>50 ciudades, más de 500 barrios reales.</strong> Para cada ciudad analizamos entre 10 y 13 barrios por perfil —céntrico, familiar, premium, económico, universitario y emergente—, con una estimación del precio por m² de cada zona, su transporte y puntos de interés, una tabla comparativa y recomendaciones de en qué barrio comprar según seas joven, familia, inversor o jubilado. Elige tu ciudad:
  </div>

  <div class="ve-grid">
"""

CARD = """      <a class="ve-card" href="barrios-{slug}.html">
        <div class="ve-imgwrap"><img src="img/{slug}.webp" alt="Barrios de {name_attr}" loading="lazy" width="320" height="180"></div>
        <div class="ve-body">
          <div class="ve-h"><span class="ve-name">{name}</span><span class="ve-ccaa">{ccaa}</span></div>
          <div class="ve-row"><span class="ve-k">Barrios</span><span class="ve-v">{n}</span></div>
          <div class="ve-row"><span class="ve-k">Precio €/m²</span><span class="ve-v">{pmin}–{pmax}€</span></div>
          <div class="ve-row"><span class="ve-k">Más caro</span><span class="ve-v">{top}</span></div>
          <div class="ve-row"><span class="ve-k">Más económico</span><span class="ve-v">{cheap}</span></div>
          <div class="ve-cta">Ver barrios →</div>
        </div>
      </a>
"""

FOOT = """  </div>

  <div class="ve-intro" style="margin-top:1rem">
    ¿Buscas algo más? Consulta las guías <a href="vivir-en-espana.html">Vivir en… (coste de vida por ciudad)</a>, el <a href="ranking.html">ranking de rentabilidad</a> o el <a href="comparador.html">comparador de ciudades</a> para ver precio, alquiler y ROI lado a lado.
  </div>

</main>

<footer>
  <div class="footer-inner">
    <div class="footer-col">
      <a href="/" class="logo" style="margin-bottom:.6rem;display:inline-flex">
        <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
        <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
      </a>
      <p>Análisis de mercado inmobiliario gratuito para 587 ciudades de España. Datos Q2 2026.</p>
    </div>
    <div class="footer-col">
      <h4>Análisis</h4>
      <a href="ranking.html">Ranking completo</a>
      <a href="analisis.html">Análisis</a>
      <a href="vivir-en-espana.html">Vivir en…</a>
      <a href="barrios.html">Barrios</a>
      <a href="comparador.html">Comparador</a>
      <a href="guia-inversor.html">Guía del inversor</a>
    </div>
    <div class="footer-col">
      <h4>Recursos</h4>
      <a href="glosario.html">Glosario</a>
      <a href="widget-demo.html">🧩 Widget gratuito para tu web</a>
      <a href="sobre.html">Sobre Ren Data</a>
      <a href="contacto.html">Contacto</a>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <a href="privacidad.html">Privacidad</a>
      <a href="aviso-legal.html">Aviso legal</a>
    </div>
  </div>
  <div class="footer-bottom">© 2026 rendata.es · Datos: INE · Ministerio de Vivienda · Ministerio de Hacienda</div>
</footer>

</body>
</html>"""


def main():
    items = []
    cards = []
    for i, slug in enumerate(order, 1):
        c = CITIES[slug]
        prices = [price_of(c["price"], b) for b in c["barrios"]]
        bs = sorted(zip(prices, c["barrios"]), key=lambda x: -x[0])
        top = bs[0][1]["name"].split(" · ")[0].split(" (")[0]
        cheap = bs[-1][1]["name"].split(" · ")[0].split(" (")[0]
        items.append({"@type": "ListItem", "position": i,
                      "url": f"https://rendata.es/barrios-{slug}.html",
                      "name": f"Barrios de {c['name']}"})
        cards.append(CARD.format(slug=slug, name=esc(c["name"]),
            name_attr=c["name"].replace('"', ''), ccaa=esc(CCAA_NAME[c["ccaa"]]),
            n=len(c["barrios"]), pmin=eur(min(prices)), pmax=eur(max(prices)),
            top=esc(top), cheap=esc(cheap)))

    jsonld = json.dumps([
        {"@context": "https://schema.org", "@type": "ItemList",
         "name": "Barrios de España — guías por ciudad", "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList",
         "itemListElement": [
             {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://rendata.es/"},
             {"@type": "ListItem", "position": 2, "name": "Barrios", "item": "https://rendata.es/barrios.html"}]},
    ], ensure_ascii=False)

    html = HEAD.format(jsonld=jsonld) + "".join(cards) + FOOT
    with open(os.path.join(OUT, "barrios.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"barrios.html escrito con {len(order)} ciudades")


if __name__ == "__main__":
    main()
