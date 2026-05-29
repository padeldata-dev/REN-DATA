# -*- coding: utf-8 -*-
"""Generador de páginas barrios-{slug}.html para Ren Data.
Usa datos REALES de barrios por ciudad (ver barrios_data.py).
"""
import os
from barrios_data import CITIES

OUT = os.path.join(os.path.dirname(__file__), "..", "rendata_beta")

# ---- Perfiles --------------------------------------------------------------
PROFILES = {
    "premium": {
        "cls": "b-premium", "tag": "premium", "factor": 1.30,
        "ideal": "Inversores y compradores de alto poder adquisitivo",
        "pro": "Zona consolidada, prestigio y revalorización estable",
        "con": "Precios elevados y oferta muy limitada",
    },
    "céntrico": {
        "cls": "b-centric", "tag": "céntrico", "factor": 1.15,
        "ideal": "Jóvenes profesionales y quienes priorizan la ubicación",
        "pro": "Todo a mano: ocio, comercio y transporte",
        "con": "Ruido, turismo y aparcamiento complicado",
    },
    "familiar": {
        "cls": "b-family", "tag": "familiar", "factor": 1.00,
        "ideal": "Familias con hijos que buscan colegios y servicios",
        "pro": "Tranquilo, buenos colegios y zonas verdes",
        "con": "Algo alejado del centro y vida nocturna escasa",
    },
    "universitario": {
        "cls": "b-uni", "tag": "universitario", "factor": 0.98,
        "ideal": "Estudiantes e inversores en alquiler por habitaciones",
        "pro": "Alta demanda de alquiler y buena rentabilidad",
        "con": "Rotación alta de inquilinos y ambiente joven",
    },
    "emergente": {
        "cls": "b-emerging", "tag": "emergente", "factor": 0.88,
        "ideal": "Jóvenes e inversores que buscan revalorización",
        "pro": "Precios de entrada y recorrido al alza",
        "con": "Zona en transformación, servicios aún desiguales",
    },
    "económico": {
        "cls": "b-cheap", "tag": "económico", "factor": 0.75,
        "ideal": "Primeros compradores y rentistas que buscan precio",
        "pro": "El precio por m² más accesible de la ciudad",
        "con": "Más alejado y con menos servicios premium",
    },
}

# Recomendaciones "¿en qué barrio comprar?" por perfil de comprador
BUYER_MAP = {
    "joven":     ["céntrico", "emergente", "universitario"],
    "familia":   ["familiar", "premium"],
    "inversor":  ["universitario", "emergente", "céntrico"],
    "jubilado":  ["familiar", "premium", "económico"],
}
BUYER_LABELS = {
    "joven":    ("🧑‍💼 Jóvenes y primeros compradores", "Buscan ubicación, vida y precio de entrada asumible."),
    "familia":  ("👨‍👩‍👧 Familias", "Priorizan colegios, parques, seguridad y espacio."),
    "inversor": ("📈 Inversores", "Buscan rentabilidad del alquiler y recorrido de revalorización."),
    "jubilado": ("🌳 Jubilados y vida tranquila", "Valoran sosiego, servicios cercanos y buena sanidad."),
}

# ---- CCAA -----------------------------------------------------------------
CCAA = {
    "Galicia": ("ccaa-galicia.html", "Galicia"),
    "Castilla-La Mancha": ("ccaa-castilla-la-mancha.html", "Castilla-La Mancha"),
    "C. de Madrid": ("ccaa-madrid.html", "Comunidad de Madrid"),
    "C. Valenciana": ("ccaa-comunitat-valenciana.html", "Comunitat Valenciana"),
    "Andalucía": ("ccaa-andalucia.html", "Andalucía"),
    "Extremadura": ("ccaa-extremadura.html", "Extremadura"),
    "Cataluña": ("ccaa-cataluna.html", "Cataluña"),
    "País Vasco": ("ccaa-pais-vasco.html", "País Vasco"),
    "Castilla y León": ("ccaa-castilla-y-leon.html", "Castilla y León"),
    "R. de Murcia": ("ccaa-murcia.html", "Región de Murcia"),
    "Asturias": ("ccaa-asturias.html", "Asturias"),
    "Canarias": ("ccaa-canarias.html", "Canarias"),
    "La Rioja": ("ccaa-la-rioja.html", "La Rioja"),
    "Islas Baleares": ("ccaa-baleares.html", "Islas Baleares"),
    "Navarra": ("ccaa-navarra.html", "Navarra"),
    "Cantabria": ("ccaa-cantabria.html", "Cantabria"),
    "Aragón": ("ccaa-aragon.html", "Aragón"),
}


def eur(n):
    return f"{n:,}".replace(",", ".")


def price_of(city_price, b):
    factor = b.get("factor") or PROFILES[b["profile"]]["factor"]
    p = int(round(city_price * factor / 10.0)) * 10
    return p


HEADER = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{meta_desc}">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://rendata.es/barrios-{slug}.html">
<meta property="og:image" content="https://rendata.es/img/{slug}.webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://rendata.es/img/{slug}.webp">
<link rel="canonical" href="https://rendata.es/barrios-{slug}.html">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">{jsonld}</script>
<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
<link rel="stylesheet" href="/css/nav.css">
<style>
.bc{{max-width:880px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}}
.bc a{{color:var(--muted);text-decoration:none;font-weight:500;transition:color .15s}}
.bc a:hover{{color:var(--blue);text-decoration:underline}}
.bc-sep{{color:#cbd5e1}}
.bc-cur{{color:var(--text);font-weight:600}}
.vivir-hero{{position:relative;min-height:300px;display:flex;align-items:flex-end;color:#fff;padding:2rem 1.5rem;margin-bottom:1rem}}
.vivir-hero-inner{{max-width:880px;margin:0 auto;width:100%}}
.vivir-hero h1{{color:#fff;font-size:clamp(1.7rem,4vw,2.5rem);line-height:1.15;letter-spacing:-.025em;margin:0 0 .55rem;font-weight:800}}
.vivir-hero .live-dot{{background:#34d399}}
.vivir-hero-tag{{display:inline-flex;align-items:center;gap:.45rem;font-size:.75rem;font-weight:600;letter-spacing:.04em;background:rgba(255,255,255,.18);backdrop-filter:blur(6px);padding:.4rem .85rem;border-radius:99px;margin-bottom:.85rem}}
.vivir-hero .lead{{font-size:1.05rem;line-height:1.55;color:rgba(255,255,255,.95);max-width:720px;margin:.4rem 0 0}}
.callout{{background:#eff6ff;border-left:3px solid var(--blue,#1a56db);border-radius:8px;padding:.95rem 1.15rem;margin:1.2rem 0;font-size:.88rem;line-height:1.65}}
.callout strong{{color:#1a56db}}
.callout.ok{{background:#ecfdf5;border-left-color:var(--green,#059669)}}
.callout.ok strong{{color:#065f46}}
.barrios-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:.95rem;margin:1rem 0 1.4rem}}
.barrio-card{{background:#fff;border:1px solid var(--border,#e2e8f0);border-left:4px solid var(--blue,#1a56db);border-radius:10px;padding:1rem 1.1rem;font-size:.88rem;line-height:1.55}}
.barrio-card.b-premium{{border-left-color:#9333ea}}
.barrio-card.b-centric{{border-left-color:#1a56db}}
.barrio-card.b-family{{border-left-color:#059669}}
.barrio-card.b-cheap{{border-left-color:#d97706}}
.barrio-card.b-uni{{border-left-color:#0891b2}}
.barrio-card.b-emerging{{border-left-color:#db2777}}
.barrio-h{{display:flex;justify-content:space-between;align-items:center;margin-bottom:.35rem;gap:.5rem;flex-wrap:wrap}}
.barrio-name{{font-weight:700;color:var(--text,#0e1828);font-size:.98rem}}
.barrio-tag{{font-size:.66rem;text-transform:uppercase;letter-spacing:.05em;font-weight:700;color:var(--muted,#64748b);background:#f1f5f9;padding:.18rem .55rem;border-radius:99px}}
.b-premium .barrio-tag{{background:#f3e8ff;color:#6b21a8}}
.b-centric .barrio-tag{{background:#dbeafe;color:#1140a6}}
.b-family .barrio-tag{{background:#d1fae5;color:#065f46}}
.b-cheap .barrio-tag{{background:#fef3c7;color:#92400e}}
.b-uni .barrio-tag{{background:#cffafe;color:#155e75}}
.b-emerging .barrio-tag{{background:#fce7f3;color:#9d174d}}
.barrio-price{{font-size:1.15rem;font-weight:800;letter-spacing:-.02em;color:var(--blue,#1a56db);margin:.1rem 0 .4rem}}
.b-premium .barrio-price{{color:#7e22ce}}
.b-family .barrio-price{{color:#047857}}
.b-cheap .barrio-price{{color:#b45309}}
.b-uni .barrio-price{{color:#0e7490}}
.b-emerging .barrio-price{{color:#be185d}}
.barrio-card p{{margin:.35rem 0 .55rem}}
.barrio-meta{{font-size:.8rem;color:var(--muted,#64748b);line-height:1.5;border-top:1px dashed #e2e8f0;padding-top:.5rem}}
.barrio-meta div{{margin:.15rem 0}}
.barrio-valor{{display:flex;flex-direction:column;gap:.2rem;font-size:.8rem;margin-top:.5rem}}
.bv-pro{{color:#047857}}
.bv-con{{color:#b91c1c}}
.tabla-barrios{{width:100%;border-collapse:collapse;font-size:.84rem;margin:1rem 0 1.4rem;background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:10px;overflow:hidden}}
.tabla-barrios th{{background:#f8fafc;text-align:left;padding:.6rem .7rem;font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;color:var(--muted,#64748b);border-bottom:1px solid #e2e8f0}}
.tabla-barrios td{{padding:.55rem .7rem;border-bottom:1px solid #f1f5f9}}
.tabla-barrios tr:last-child td{{border-bottom:none}}
.tabla-barrios td.num{{font-weight:700;color:var(--blue,#1a56db);white-space:nowrap}}
.mini-tag{{font-size:.64rem;text-transform:uppercase;letter-spacing:.04em;font-weight:700;padding:.12rem .45rem;border-radius:99px;background:#f1f5f9;color:#475569}}
.reco-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:.85rem;margin:1rem 0 1.4rem}}
.reco-card{{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:10px;padding:1rem 1.1rem}}
.reco-h{{font-weight:700;font-size:.95rem;margin-bottom:.25rem;color:var(--text,#0e1828)}}
.reco-s{{font-size:.82rem;color:var(--muted,#64748b);margin-bottom:.5rem;line-height:1.45}}
.reco-card .picks{{font-size:.86rem;line-height:1.6}}
.reco-card .picks strong{{color:var(--blue,#1a56db)}}
.cta-ficha{{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:1.25rem 1.4rem;border-radius:12px;margin:1.4rem 0;text-decoration:none}}
.cta-ficha-t{{font-size:1.08rem;font-weight:700;letter-spacing:-.02em;color:#fff;margin-bottom:.2rem}}
.cta-ficha-s{{font-size:.85rem;color:rgba(255,255,255,.85)}}
.cta-ficha-b{{background:rgba(255,255,255,.2);padding:.55rem 1.05rem;border-radius:8px;font-weight:700;color:#fff;font-size:.88rem;white-space:nowrap}}
@media(max-width:600px){{.tabla-barrios .hide-sm{{display:none}}}}
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
  <a href="vivir-en-{slug}.html">{city}</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">Barrios</span>
</nav>

<section class="vivir-hero" style="background:linear-gradient(180deg,rgba(0,0,0,.05) 0%,rgba(0,0,0,.6) 100%),url('img/{slug}.webp') center/cover no-repeat">
  <div class="vivir-hero-inner">
    <div class="vivir-hero-tag"><span class="live-dot"></span>Mapa de barrios · Q2 2026</div>
    <h1>Barrios de {city} — Dónde vivir y comprar en 2026</h1>
    <p class="lead">{n} barrios reales analizados por perfil, precio medio €/m², transporte y puntos de interés. La guía práctica para elegir dónde vivir o invertir en {city}.</p>
  </div>
</section>

<article class="art">
"""

FOOTER = """
  <div class="callout ok" style="margin-top:1.8rem">
    <strong>¿Quieres el panorama completo de {city}?</strong> Lee la <a href="vivir-en-{slug}.html">guía Vivir en {city}</a> (coste de vida, empleo, sanidad) o consulta la <a href="rentabilidad-{slug}.html">ficha de rentabilidad</a> con ROI y precios actualizados. También puedes ver el <a href="barrios.html">índice de barrios de España</a>.
  </div>

</article>

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


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def build_jsonld(slug, city, ccaa_name, meta_desc, faqs):
    import json
    article = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": f"Barrios de {city} — Dónde vivir y comprar en 2026",
        "description": meta_desc,
        "datePublished": "2026-05-29", "dateModified": "2026-05-29",
        "author": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"},
        "publisher": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/",
                       "logo": {"@type": "ImageObject", "url": "https://rendata.es/favicon.svg"}},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://rendata.es/barrios-{slug}.html"},
        "image": f"https://rendata.es/img/{slug}.webp", "inLanguage": "es-ES",
        "about": {"@type": "Place", "name": city,
                   "containedInPlace": {"@type": "AdministrativeArea", "name": ccaa_name}},
    }
    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://rendata.es/"},
            {"@type": "ListItem", "position": 2, "name": f"Vivir en {city}", "item": f"https://rendata.es/vivir-en-{slug}.html"},
            {"@type": "ListItem", "position": 3, "name": "Barrios", "item": f"https://rendata.es/barrios-{slug}.html"},
        ],
    }
    faqpage = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }
    return json.dumps([article, breadcrumb, faqpage], ensure_ascii=False)


def render(slug, c):
    city = c["name"]
    price = c["price"]
    ccaa_href, ccaa_name = CCAA[c["ccaa"]]
    barrios = c["barrios"]
    n = len(barrios)

    # precios calculados
    for b in barrios:
        b["_price"] = price_of(price, b)
    prices = [b["_price"] for b in barrios]
    pmin, pmax = min(prices), max(prices)

    meta_desc = (f"Barrios de {city}: los {n} mejores barrios para vivir y comprar en 2026. "
                 f"Precio medio por barrio ({eur(pmin)}–{eur(pmax)}€/m²), perfil, transporte y dónde invertir según tu perfil.")
    title = f"Barrios de {city} 2026 — Dónde vivir y comprar | Ren Data"
    og_title = f"Barrios de {city} — Guía 2026"

    # FAQs reales
    cheap = sorted(barrios, key=lambda b: b["_price"])[:2]
    prem = sorted(barrios, key=lambda b: -b["_price"])[:2]
    fam = [b for b in barrios if b["profile"] == "familiar"][:2] or [b for b in barrios if b["profile"] == "céntrico"][:2]
    faqs = [
        (f"¿Cuáles son los mejores barrios de {city}?",
         f"Depende del perfil: para vivir en el centro destacan {prem[0]['name']} y {barrios[0]['name']}; "
         f"para familias, {(fam[0]['name'] if fam else barrios[1]['name'])}; y las opciones más económicas están en "
         f"{cheap[0]['name']} y {cheap[1]['name']} (desde ~{eur(pmin)}€/m²)."),
        (f"¿Cuánto cuesta el m² en los barrios de {city}?",
         f"El precio medio de {city} ronda los {eur(price)}€/m². Por barrios oscila entre ~{eur(pmin)}€/m² en las zonas "
         f"más económicas y ~{eur(pmax)}€/m² en las áreas premium, una diferencia de en torno al {int(round((pmax/pmin-1)*100))}%."),
        (f"¿Qué barrio de {city} es mejor para invertir?",
         f"Para alquiler, las zonas con más demanda y rentabilidad suelen ser los barrios céntricos y universitarios; "
         f"para revalorización, conviene mirar los barrios emergentes en transformación. Consulta la rentabilidad detallada "
         f"en la ficha de {city}."),
    ]

    out = []
    out.append(HEADER.format(
        meta_desc=esc(meta_desc), title=esc(title), og_title=esc(og_title), slug=slug,
        jsonld=build_jsonld(slug, city, ccaa_name, meta_desc, faqs), city=city, n=n))

    # Intro + TOC
    out.append(f"""
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#mapa">1. El mapa de barrios de {city}</a></li>
      <li><a href="#barrios">2. Los {n} barrios, uno a uno</a></li>
      <li><a href="#tabla">3. Tabla comparativa</a></li>
      <li><a href="#comprar">4. ¿En qué barrio comprar?</a></li>
      <li><a href="#ficha">5. Rentabilidad y precios</a></li>
      <li><a href="#faq">FAQ</a></li>
    </ul>
  </div>

  <h2 id="mapa">1. El mapa de barrios de {city}</h2>
  <p>{c['intro']}</p>
  <div class="callout"><strong>Precio de referencia:</strong> el m² medio en {city} se sitúa en <strong>{eur(price)}€/m²</strong> en 2026. En esta guía estimamos el precio de cada barrio aplicando la prima o el descuento típico de cada zona (de ~{eur(pmin)}€/m² en los barrios más económicos a ~{eur(pmax)}€/m² en los premium). Son estimaciones orientativas para comparar zonas, no tasaciones.</p>

  <h2 id="barrios">2. Los {n} barrios de {city}, uno a uno</h2>
  <p>Selección de barrios reales de {city} ordenados para cubrir todos los perfiles —céntrico, familiar, premium, económico, universitario y emergente—:</p>
  <div class="barrios-grid">""")

    for b in barrios:
        pr = PROFILES[b["profile"]]
        ideal = b.get("ideal", pr["ideal"])
        pro = b.get("pro", pr["pro"])
        con = b.get("con", pr["con"])
        out.append(f"""
    <div class="barrio-card {pr['cls']}">
      <div class="barrio-h"><span class="barrio-name">{esc(b['name'])}</span><span class="barrio-tag">{pr['tag']}</span></div>
      <div class="barrio-price">~{eur(b['_price'])}€/m²</div>
      <p>{esc(b['blurb'])}</p>
      <div class="barrio-meta">
        <div>👤 <strong>Ideal para:</strong> {esc(ideal)}</div>
        <div>🚇 <strong>Transporte:</strong> {esc(b['transporte'])}</div>
        <div>📍 <strong>De interés:</strong> {esc(b['poi'])}</div>
      </div>
      <div class="barrio-valor"><span class="bv-pro">✓ {esc(pro)}</span><span class="bv-con">✕ {esc(con)}</span></div>
    </div>""")

    out.append("""
  </div>

  <h2 id="tabla">3. Tabla comparativa de barrios</h2>
  <table class="tabla-barrios">
    <thead><tr><th>Barrio</th><th>Perfil</th><th>Precio est. €/m²</th><th class="hide-sm">Ideal para</th></tr></thead>
    <tbody>""")
    for b in sorted(barrios, key=lambda x: -x["_price"]):
        pr = PROFILES[b["profile"]]
        ideal = b.get("ideal", pr["ideal"])
        out.append(f"""
      <tr><td><strong>{esc(b['name'])}</strong></td><td><span class="mini-tag">{pr['tag']}</span></td>"""
                   f"""<td class="num">{eur(b['_price'])}€</td><td class="hide-sm">{esc(ideal)}</td></tr>""")
    out.append("""
    </tbody>
  </table>

  <h2 id="comprar">4. ¿En qué barrio comprar en """ + city + """?</h2>
  <p>Cada perfil de comprador encaja mejor en unas zonas. Estas son nuestras recomendaciones según para quién sea la vivienda:</p>
  <div class="reco-grid">""")

    used = set()
    for key, profs in BUYER_MAP.items():
        label, sub = BUYER_LABELS[key]
        picks = []
        for b in barrios:
            if b["profile"] in profs and b["name"] not in used:
                picks.append(b)
            if len(picks) >= 3:
                break
        if len(picks) < 2:
            picks = [b for b in barrios if b["profile"] in profs][:3]
        names = ", ".join(f"<strong>{esc(p['name'])}</strong>" for p in picks)
        out.append(f"""
    <div class="reco-card">
      <div class="reco-h">{label}</div>
      <div class="reco-s">{sub}</div>
      <div class="picks">{names}</div>
    </div>""")

    out.append(f"""
  </div>

  <h2 id="ficha">5. Rentabilidad y precios en {city}</h2>
  <p>Antes de decidir un barrio conviene mirar la rentabilidad del alquiler, la fiscalidad y la evolución del precio en {city}. Tienes todos los datos en la ficha completa:</p>
  <a href="rentabilidad-{slug}.html" class="cta-ficha">
    <div>
      <div class="cta-ficha-t">📊 Ficha completa: invertir o comprar en {city}</div>
      <div class="cta-ficha-s">Precio {eur(price)}€/m² · alquiler {eur(c['rent'])}€/mes · ROI y días en mercado</div>
    </div>
    <span class="cta-ficha-b">Ver ficha →</span>
  </a>

  <h2 id="faq">Preguntas frecuentes</h2>""")
    for q, a in faqs:
        out.append(f"\n  <h3>{esc(q)}</h3>\n  <p>{esc(a)}</p>")

    out.append(FOOTER.format(city=city, slug=slug))
    return "".join(out)


def main():
    os.makedirs(OUT, exist_ok=True)
    written = []
    for slug, c in CITIES.items():
        html = render(slug, c)
        path = os.path.join(OUT, f"barrios-{slug}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        written.append((slug, len(c["barrios"])))
    for slug, n in written:
        print(f"barrios-{slug}.html  ({n} barrios)")
    print(f"TOTAL: {len(written)} páginas")


if __name__ == "__main__":
    main()
