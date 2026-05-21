// Genera rendata_beta/vivir-en-espana.html — índice de las 50 guías Vivir en…
const fs = require('fs');
const path = require('path');
const list = require('../data/vivir-list.json');
const OUT = path.join(__dirname,'..','rendata_beta','vivir-en-espana.html');
const IMG_DIR = path.join(__dirname,'..','rendata_beta','img');

const CCAA_SLUG = {
  'C. de Madrid':'madrid','Cataluña':'cataluna','C. Valenciana':'comunitat-valenciana',
  'Andalucía':'andalucia','Aragón':'aragon','Islas Baleares':'baleares','Canarias':'canarias',
  'País Vasco':'pais-vasco','R. de Murcia':'murcia','Castilla y León':'castilla-y-leon',
  'Galicia':'galicia','Asturias':'asturias','Cantabria':'cantabria','Navarra':'navarra',
  'Castilla-La Mancha':'castilla-la-mancha','Extremadura':'extremadura','La Rioja':'la-rioja',
};
const fmtNum = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.');
const escape = (s) => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

// Ordenar por población descendente
const cities = [...list].sort((a,b)=>b.pob-a.pob);

const cards = cities.map(c=>{
  const hasImg = fs.existsSync(path.join(IMG_DIR, c.slug+'.webp'));
  const img = hasImg ? `<img src="img/${c.slug}.webp" alt="${escape(c.n)}" loading="lazy" width="320" height="180">` : `<div class="ve-noimg" aria-hidden="true"></div>`;
  return `      <a class="ve-card" href="vivir-en-${c.slug}.html">
        <div class="ve-imgwrap">${img}</div>
        <div class="ve-body">
          <div class="ve-h"><span class="ve-name">${escape(c.n)}</span><span class="ve-ccaa">${escape(c.ccaa)}</span></div>
          <div class="ve-row"><span class="ve-k">Precio m²</span><span class="ve-v">${fmtNum(c.p)}€</span></div>
          <div class="ve-row"><span class="ve-k">Alquiler</span><span class="ve-v">${fmtNum(c.alq)}€/mes</span></div>
          <div class="ve-row"><span class="ve-k">ROI alquiler</span><span class="ve-v">${c.roi}%</span></div>
          <div class="ve-row"><span class="ve-k">Población</span><span class="ve-v">${fmtNum(c.pob)}</span></div>
          <div class="ve-cta">Ver guía →</div>
        </div>
      </a>`;
}).join('\n');

const itemListLD = {
  "@context":"https://schema.org",
  "@type":"ItemList",
  "name":"Vivir en España — Guías por ciudad",
  "itemListElement": cities.map((c,i)=>({
    "@type":"ListItem","position":i+1,
    "url":`https://rendata.es/vivir-en-${c.slug}.html`,
    "name":`Vivir en ${c.n}`
  }))
};
const breadcrumbLD = {
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {"@type":"ListItem","position":1,"name":"Inicio","item":"https://rendata.es/"},
    {"@type":"ListItem","position":2,"name":"Vivir en España","item":"https://rendata.es/vivir-en-espana.html"},
  ]
};

const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Guías "Vivir en…" para las 50 ciudades más grandes de España: barrios reales, coste de vida, transporte, empleo, educación y sanidad. Datos actualizados 2026.">
<title>Vivir en España — Guías de 50 ciudades para mudarte 2026 | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="Vivir en España — Guías de 50 ciudades para mudarte 2026">
<meta property="og:description" content="Guías "Vivir en…" para las 50 ciudades más grandes de España: barrios, coste de vida, transporte, empleo y sanidad. Datos 2026.">
<meta property="og:url" content="https://rendata.es/vivir-en-espana.html">
<meta property="og:image" content="https://rendata.es/img/logo-rendata-transparente.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Vivir en España — Guías de 50 ciudades para mudarte 2026">
<meta name="twitter:description" content="50 ciudades, guías completas con barrios, coste de vida, transporte, empleo y sanidad. Datos 2026.">
<link rel="canonical" href="https://rendata.es/vivir-en-espana.html">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">${JSON.stringify([itemListLD,breadcrumbLD])}</script>
<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
<link rel="stylesheet" href="/css/nav.css">
<style>
.bc{max-width:1200px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}
.bc a{color:var(--muted);text-decoration:none;font-weight:500}.bc a:hover{color:var(--blue);text-decoration:underline}
.bc-sep{color:#cbd5e1}.bc-cur{color:var(--text);font-weight:600}
.ve-hero{background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:2.5rem 1.5rem;text-align:center}
.ve-hero-inner{max-width:880px;margin:0 auto}
.ve-hero h1{color:#fff;font-size:clamp(1.9rem,4vw,2.7rem);line-height:1.15;letter-spacing:-.025em;margin:0 0 .65rem;font-weight:800}
.ve-hero-tag{display:inline-flex;align-items:center;gap:.45rem;font-size:.75rem;font-weight:600;letter-spacing:.04em;background:rgba(255,255,255,.18);backdrop-filter:blur(6px);padding:.4rem .85rem;border-radius:99px;margin-bottom:.85rem}
.ve-hero .lead{font-size:1.05rem;line-height:1.55;color:rgba(255,255,255,.92);max-width:720px;margin:.4rem auto 0}
.ve-main{max-width:1200px;margin:1.6rem auto;padding:0 1.5rem}
.ve-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;margin:1rem 0 2rem}
.ve-card{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}
.ve-card:hover{transform:translateY(-3px);box-shadow:0 8px 24px rgba(15,23,42,.08);border-color:var(--blue,#1a56db)}
.ve-imgwrap{aspect-ratio:16/9;background:#e2e8f0;overflow:hidden;position:relative}
.ve-imgwrap img{width:100%;height:100%;object-fit:cover;display:block}
.ve-noimg{width:100%;height:100%;background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%)}
.ve-body{padding:.95rem 1.05rem 1.05rem;display:flex;flex-direction:column;gap:.3rem}
.ve-h{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.35rem;gap:.5rem}
.ve-name{font-weight:800;font-size:1.05rem;color:var(--text,#0e1828);letter-spacing:-.015em}
.ve-ccaa{font-size:.7rem;color:var(--muted,#64748b);font-weight:600;text-align:right}
.ve-row{display:flex;justify-content:space-between;font-size:.82rem;color:var(--text2,#475569);padding:.1rem 0}
.ve-k{color:var(--muted,#64748b)}
.ve-v{font-weight:700;color:var(--text,#0e1828);font-variant-numeric:tabular-nums}
.ve-cta{margin-top:.55rem;font-size:.84rem;font-weight:700;color:var(--blue,#1a56db);letter-spacing:-.01em}
.ve-card:hover .ve-cta{color:#0e2a6b}
.ve-intro{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:12px;padding:1.2rem 1.4rem;margin:1.2rem 0 1.4rem;font-size:.95rem;line-height:1.65;color:var(--text2,#475569)}
.ve-intro strong{color:var(--text,#0e1828)}
.ve-filtros{display:flex;flex-wrap:wrap;gap:.4rem;margin:.5rem 0 1.2rem}
.ve-chip{font-size:.78rem;font-weight:600;background:#f1f5f9;color:var(--text2,#475569);padding:.4rem .85rem;border-radius:99px;border:1px solid var(--border,#e2e8f0);cursor:pointer;transition:all .15s}
.ve-chip:hover,.ve-chip.active{background:var(--blue,#1a56db);color:#fff;border-color:var(--blue,#1a56db)}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-0M57323B51');</script>
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
  <span class="bc-cur">Vivir en España</span>
</nav>

<section class="ve-hero">
  <div class="ve-hero-inner">
    <div class="ve-hero-tag">🏡 Guía residencial · Q2 2026</div>
    <h1>Vivir en España — 50 ciudades, una guía por cada una</h1>
    <p class="lead">Barrios reales, coste de vida, transporte, empleo, educación y sanidad. Información práctica con datos verificados para decidir dónde mudarte en España.</p>
  </div>
</section>

<main class="ve-main">

  <div class="ve-intro">
    <strong>50 ciudades, ordenadas por población.</strong> Cada guía incluye barrios con perfil (céntrico, familiar, económico, premium), análisis del transporte público y conexiones, sectores de empleo dominantes, universidades y hospitales principales, pros y contras honestos, y la ficha de rentabilidad inmobiliaria con datos por barrio. Pensado tanto para quien busca dónde comprar como para quien se plantea alquilar.
  </div>

  <div class="ve-grid">
${cards}
  </div>

  <div class="ve-intro" style="margin-top:1.6rem">
    <strong>¿Buscas datos económicos puros?</strong> Cada guía enlaza a la <a href="ranking.html">ficha de rentabilidad de la ciudad</a> con ROI bruto, evolución de precio, mejores barrios para invertir y comparativas. También puedes ir directamente al <a href="comparador.html">comparador de ciudades</a> o al <a href="simulador-comprar-vs-alquilar.html">simulador comprar vs alquilar</a>.
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
</html>
`;

fs.writeFileSync(OUT, html, 'utf8');
console.log('OK vivir-en-espana.html ('+cities.length+' ciudades)');
