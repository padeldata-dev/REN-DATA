"""Block 3 & 4: create simulator (buy vs rent) and mortgage calculator tools.

Also links them from nav (across all HTML pages) and from analisis.html.
"""
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

# ---------- Shared header block (favicons, fonts, brand) ----------
def head(title, desc, slug, body_json_ld):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title} | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://rendata.es/{slug}">
<meta property="og:image" content="https://rendata.es/img/logo-rendata-transparente.png">
<meta property="og:image:width" content="512">
<meta property="og:image:height" content="512">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="canonical" href="https://rendata.es/{slug}">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/nav.css">
<script type="application/ld+json">{body_json_ld}</script>
"""


NAV_HTML = """<header>
  <a href="/" class="logo"><img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA"></a>
  <nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="mob-nav-links">
      <a href="/">🏠 Ciudades</a>
      <a href="/ranking.html">📊 Ranking</a>
      <a href="/analisis.html">📈 Análisis</a>
      <a href="/comparador.html">⚖️ Comparar</a>
      <a href="/simulador-comprar-vs-alquilar.html">🔄 Comprar vs alquilar</a>
      <a href="/calculadora-hipoteca.html">💶 Calculadora hipoteca</a>
      <a href="/metodologia.html">📊 Metodología</a>
      <a href="/glosario.html">📖 Glosario</a>
      <a href="/guia-inversor.html">🎯 Guía inversor</a>
      <a href="/sobre.html">ℹ️ Sobre</a>
    </div>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/comparador.html">Comparador</a>
    <a href="/simulador-comprar-vs-alquilar.html">Comprar vs alquilar</a>
    <a href="/calculadora-hipoteca.html">Calculadora hipoteca</a>
    <a href="/metodologia.html">Metodología</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/sobre.html">Sobre</a>
  </nav>
</header>
"""


def breadcrumb_ld(title, slug):
    return f"""<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://rendata.es/"}},
    {{"@type": "ListItem", "position": 2, "name": "Herramientas", "item": "https://rendata.es/analisis.html"}},
    {{"@type": "ListItem", "position": 3, "name": "{title}", "item": "https://rendata.es/{slug}"}}
  ]
}}</script>
"""


# ============================================================================
#  TOOL 1 — Simulador comprar vs alquilar
# ============================================================================
SIM_TITLE = "Simulador: comprar vs alquilar vivienda en España"
SIM_DESC = "Simulador interactivo para comparar el coste real de comprar una vivienda frente a alquilarla en cualquiera de las 587 ciudades españolas. Calcula el punto de equilibrio y el coste acumulado a 30 años."
SIM_SLUG = "simulador-comprar-vs-alquilar.html"

SIM_JSON_LD = """{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Simulador comprar vs alquilar — Ren Data",
  "url": "https://rendata.es/simulador-comprar-vs-alquilar.html",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Web",
  "description": "Compara el coste de comprar una vivienda frente a alquilarla en 587 ciudades españolas. Calcula el punto de equilibrio temporal y proyecta el gasto acumulado a 30 años.",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
  "inLanguage": "es-ES",
  "publisher": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"}
}"""

SIMULADOR_HTML = head(SIM_TITLE, SIM_DESC, SIM_SLUG, SIM_JSON_LD) + breadcrumb_ld("Simulador comprar vs alquilar", SIM_SLUG) + """<style>
:root{--bg:#f8fafc;--white:#fff;--blue:#1a56db;--blue-d:#1140a6;--blue-l:#eff6ff;--text:#0e1828;--text2:#374151;--muted:#6b7a8d;--border:#e5eaf2;--border2:#d1dae8;--green:#059669;--green-bg:#ecfdf5;--red:#dc2626;--red-bg:#fef2f2;--sh:0 1px 3px rgba(14,24,40,.08),0 4px 12px rgba(14,24,40,.05);--sh-md:0 4px 16px rgba(14,24,40,.1),0 1px 4px rgba(14,24,40,.06);--font:'Plus Jakarta Sans',sans-serif;--r:14px}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:var(--font);font-weight:400;line-height:1.6;-webkit-font-smoothing:antialiased}
header{background:rgba(255,255,255,.93);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);padding:0 2.5rem;height:66px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200}
.logo img{height:32px;width:auto;display:block}
nav a{font-size:.82rem;font-weight:500;color:var(--muted);text-decoration:none;padding:.45rem .85rem;border-radius:8px;transition:all .15s}
nav a:hover{color:var(--blue);background:var(--blue-l)}
.tool-hero{background:linear-gradient(135deg,#0a1628 0%,#1a3a7a 50%,#0f1b3d 100%);color:#fff;padding:3rem 2rem 2.5rem;text-align:center}
.tool-hero h1{font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;letter-spacing:-.03em;margin:0 0 .7rem}
.tool-hero p{font-size:1.05rem;color:rgba(226,232,240,.92);max-width:680px;margin:0 auto}
.crumb{max-width:1100px;margin:1.5rem auto 0;padding:0 2rem;font-size:.78rem;color:var(--muted)}
.crumb a{color:var(--muted);text-decoration:none}
.crumb a:hover{color:var(--blue)}
.tool-wrap{max-width:1100px;margin:2rem auto;padding:0 2rem 4rem}
.tool-grid{display:grid;grid-template-columns:340px 1fr;gap:1.5rem;align-items:start}
@media(max-width:860px){.tool-grid{grid-template-columns:1fr}}
.card{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;box-shadow:var(--sh)}
.card h2{font-size:1.05rem;font-weight:800;letter-spacing:-.02em;margin-bottom:1rem}
.f-group{margin-bottom:1.1rem}
.f-label{display:block;font-size:.78rem;font-weight:700;color:var(--text2);margin-bottom:.4rem;letter-spacing:.01em}
.f-input,.f-select{width:100%;background:#fff;border:1.5px solid var(--border2);border-radius:8px;padding:.65rem .9rem;font-size:.95rem;font-family:inherit;color:var(--text);outline:none;transition:border-color .15s}
.f-input:focus,.f-select:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(26,86,219,.1)}
.f-hint{font-size:.7rem;color:var(--muted);margin-top:.3rem}
.f-row{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}
.results-card{display:flex;flex-direction:column;gap:1rem}
.kpi-row{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}
.kpi{background:var(--blue-l);border:1px solid #c7d8f6;border-radius:10px;padding:.85rem 1rem;text-align:left}
.kpi-l{font-size:.65rem;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.3rem}
.kpi-v{font-size:1.25rem;font-weight:800;letter-spacing:-.02em;color:var(--text)}
.kpi.k-rent{background:#fef9c3;border-color:#fde68a}
.kpi.k-rent .kpi-l{color:#a16207}
.kpi.k-buy{background:var(--green-bg);border-color:#a7f3d0}
.kpi.k-buy .kpi-l{color:var(--green)}
.summary{background:#0f1b3d;color:#fff;border-radius:10px;padding:1.1rem 1.3rem;font-size:.95rem;line-height:1.55}
.summary strong{color:#34d399}
canvas{width:100%;max-width:100%;height:auto;display:block;margin-top:.5rem;border-radius:8px;background:#fafbff}
.chart-legend{display:flex;gap:1.2rem;font-size:.78rem;color:var(--muted);margin-top:.6rem;flex-wrap:wrap}
.chart-legend span{display:inline-flex;align-items:center;gap:.4rem}
.chart-dot{width:10px;height:10px;border-radius:50%}
table.amort{width:100%;border-collapse:collapse;margin-top:.8rem;font-size:.85rem}
table.amort th,table.amort td{padding:.5rem .7rem;text-align:right;border-bottom:1px solid var(--border)}
table.amort th{background:#f1f5f9;color:var(--text);font-weight:700;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em}
table.amort td:first-child,table.amort th:first-child{text-align:left}
.note{font-size:.78rem;color:var(--muted);margin-top:1rem;line-height:1.55}
.loading{padding:2rem;text-align:center;color:var(--muted);font-size:.9rem}
</style>
</head>
<body>
""" + NAV_HTML + """
<section class="tool-hero">
  <h1>🔄 Simulador: comprar vs alquilar</h1>
  <p>Calcula en qué año comprar una vivienda sale más barato que alquilarla en cualquiera de las 587 ciudades de Ren Data. Datos reales de precio m² y alquiler medio.</p>
</section>

<nav class="crumb"><a href="/">Inicio</a> · <a href="/analisis.html">Herramientas</a> · Comprar vs alquilar</nav>

<div class="tool-wrap">
  <div class="tool-grid">
    <!-- INPUT CARD -->
    <div class="card">
      <h2>📋 Datos</h2>
      <div class="f-group">
        <label class="f-label" for="city">Ciudad</label>
        <select class="f-select" id="city"><option value="">Cargando...</option></select>
        <div class="f-hint" id="cityHint"></div>
      </div>
      <div class="f-group">
        <label class="f-label" for="surface">Superficie (m²)</label>
        <input class="f-input" id="surface" type="number" min="30" max="300" value="85">
      </div>
      <div class="f-row">
        <div class="f-group">
          <label class="f-label" for="rate">Interés hipoteca (%)</label>
          <input class="f-input" id="rate" type="number" step="0.1" min="0.5" max="10" value="3.5">
        </div>
        <div class="f-group">
          <label class="f-label" for="years">Plazo (años)</label>
          <input class="f-input" id="years" type="number" min="10" max="40" value="30">
        </div>
      </div>
      <div class="f-row">
        <div class="f-group">
          <label class="f-label" for="downpct">Entrada (%)</label>
          <input class="f-input" id="downpct" type="number" min="0" max="100" value="20">
        </div>
        <div class="f-group">
          <label class="f-label" for="rentinc">Subida alquiler/año (%)</label>
          <input class="f-input" id="rentinc" type="number" step="0.1" min="0" max="10" value="2.5">
        </div>
      </div>
    </div>

    <!-- RESULTS CARD -->
    <div class="card results-card">
      <h2>📊 Resultados</h2>
      <div id="results" class="loading">Selecciona una ciudad para empezar…</div>
    </div>
  </div>

  <div class="card" style="margin-top:1.5rem">
    <h2>💡 ¿Cómo se calcula?</h2>
    <p class="note">Comparamos el <strong>coste total acumulado</strong> de cada opción año a año durante 30 años. <strong>Comprar</strong> incluye: entrada inicial + ~10% de gastos de compra (ITP/IVA, notario, registro, gestoría) + cuotas hipotecarias mensuales (sistema francés). <strong>Alquilar</strong> incluye: cuota mensual del alquiler medio de la ciudad, con incremento anual ajustable. El <strong>punto de equilibrio</strong> es el primer año en que comprar acumula menos gasto que alquilar. No se descuenta la revalorización del piso (al comprar mantienes el activo, al alquilar no).</p>
  </div>
</div>

<footer style="border-top:1px solid var(--border);background:#fff;padding:1.5rem 2rem;text-align:center;font-size:.8rem;color:var(--muted)">
  © 2026 Ren Data · <a href="/" style="color:var(--blue);text-decoration:none">Inicio</a> · <a href="/metodologia.html" style="color:var(--blue);text-decoration:none">Metodología</a> · <a href="/sobre.html" style="color:var(--blue);text-decoration:none">Sobre</a>
</footer>

<script src="/js/nav-dropdown.js" defer></script>
<script>
let CITIES = [];

async function loadCities(){
  try{
    const r = await fetch('/', {cache:'force-cache'});
    const html = await r.text();
    const m = html.match(/const DATA=\\s*(\\[[\\s\\S]*?\\]);/);
    if(!m) throw new Error('DATA array not found in index.html');
    CITIES = new Function('return ' + m[1])();
    populateCities();
  }catch(e){
    document.getElementById('results').innerHTML = '<div style="color:#dc2626">Error cargando datos: ' + e.message + '</div>';
  }
}

function populateCities(){
  const sel = document.getElementById('city');
  CITIES.sort((a,b)=>a.n.localeCompare(b.n,'es'));
  sel.innerHTML = '<option value="">— Selecciona una ciudad —</option>' + CITIES.map((c,i)=>`<option value="${i}">${c.n} (${c.cc})</option>`).join('');
}

function fmt(n){ return n.toLocaleString('es-ES',{maximumFractionDigits:0}); }
function fmtEur(n){ return '€' + fmt(n); }
function fmtPct(n){ return n.toFixed(1).replace('.',',') + '%'; }

function monthlyPayment(principal, annualRate, years){
  const r = annualRate / 100 / 12;
  const n = years * 12;
  if (r === 0) return principal / n;
  return principal * (r * Math.pow(1+r,n)) / (Math.pow(1+r,n) - 1);
}

function compute(){
  const idx = document.getElementById('city').value;
  if(idx === '') {
    document.getElementById('results').innerHTML = '<div class="loading">Selecciona una ciudad para empezar…</div>';
    return;
  }
  const c = CITIES[+idx];
  const surface = +document.getElementById('surface').value || 85;
  const rate = +document.getElementById('rate').value || 3.5;
  const years = Math.min(40, Math.max(10, +document.getElementById('years').value || 30));
  const downpct = Math.min(100, Math.max(0, +document.getElementById('downpct').value || 20));
  const rentinc = Math.max(0, +document.getElementById('rentinc').value || 2.5);

  const price = c.p * surface;             // precio total piso
  const down = price * downpct / 100;
  const loan = price - down;
  const closingCosts = price * 0.10;       // ~10% de gastos
  const monthly = monthlyPayment(loan, rate, years);
  const totalBuy30 = down + closingCosts + monthly * 12 * Math.min(30, years);

  // Proyección año a año (30 años)
  const horizon = 30;
  let buyAcc = down + closingCosts;
  let rentAcc = 0;
  let rentMonthly = c.alq;
  const seriesBuy = [], seriesRent = [];
  let breakEvenYear = null;
  for(let y=1; y<=horizon; y++){
    // buy: 12 cuotas mensuales (si todavía hay hipoteca)
    if (y <= years) buyAcc += monthly * 12;
    // rent: 12 mensualidades con subida anual al inicio del año
    rentAcc += rentMonthly * 12;
    rentMonthly *= (1 + rentinc/100);
    seriesBuy.push(buyAcc);
    seriesRent.push(rentAcc);
    if (!breakEvenYear && rentAcc >= buyAcc) breakEvenYear = y;
  }

  document.getElementById('cityHint').textContent =
    `Precio m²: €${fmt(c.p)} · Alquiler medio: €${fmt(c.alq)}/mes · ROI: ${fmtPct(c.roi)}`;

  // Build results HTML
  const kpis = `
    <div class="kpi-row">
      <div class="kpi"><div class="kpi-l">Precio piso</div><div class="kpi-v">${fmtEur(price)}</div></div>
      <div class="kpi k-buy"><div class="kpi-l">Cuota hipoteca</div><div class="kpi-v">${fmtEur(monthly)}/mes</div></div>
      <div class="kpi k-rent"><div class="kpi-l">Alquiler hoy</div><div class="kpi-v">${fmtEur(c.alq)}/mes</div></div>
    </div>
    <div class="summary">
      ${breakEvenYear
        ? `🎯 <strong>Punto de equilibrio: año ${breakEvenYear}</strong> — a partir de ese momento comprar te sale más barato que alquilar, considerando una subida anual del alquiler del ${fmtPct(rentinc)}.`
        : `📉 En 30 años el coste acumulado de comprar (${fmtEur(seriesBuy[29])}) sigue siendo superior al de alquilar (${fmtEur(seriesRent[29])}). Considera mayor entrada o un plazo de hipoteca más corto.`
      }
    </div>
    <canvas id="chart" width="640" height="280"></canvas>
    <div class="chart-legend">
      <span><span class="chart-dot" style="background:#1a56db"></span>Coste acumulado COMPRAR</span>
      <span><span class="chart-dot" style="background:#f59e0b"></span>Coste acumulado ALQUILAR</span>
      ${breakEvenYear ? '<span><span class="chart-dot" style="background:#059669"></span>Punto de equilibrio</span>' : ''}
    </div>
  `;
  document.getElementById('results').innerHTML = kpis;

  drawChart(seriesBuy, seriesRent, breakEvenYear);
}

function drawChart(buy, rent, be){
  const c = document.getElementById('chart');
  if(!c) return;
  const dpr = window.devicePixelRatio || 1;
  const W = c.clientWidth || 640, H = 280;
  c.width = W * dpr; c.height = H * dpr;
  c.style.height = H + 'px';
  const ctx = c.getContext('2d');
  ctx.scale(dpr, dpr);
  ctx.clearRect(0,0,W,H);
  const padL = 56, padR = 16, padT = 12, padB = 28;
  const innerW = W - padL - padR, innerH = H - padT - padB;
  const N = buy.length;
  const max = Math.max(...buy, ...rent);
  const xs = i => padL + (i/(N-1)) * innerW;
  const ys = v => padT + innerH - (v/max) * innerH;

  // Grid
  ctx.strokeStyle = '#e5eaf2'; ctx.lineWidth = 1;
  ctx.fillStyle = '#6b7a8d'; ctx.font = '11px ' + getComputedStyle(document.body).fontFamily;
  for(let g=0; g<=4; g++){
    const y = padT + (innerH * g / 4);
    ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(padL+innerW, y); ctx.stroke();
    const v = max * (1 - g/4);
    ctx.textAlign='right'; ctx.fillText('€' + fmt(Math.round(v/1000))+'k', padL-6, y+4);
  }
  // x labels
  ctx.textAlign='center';
  [1,5,10,15,20,25,30].forEach(y=>{
    if(y<=N){ctx.fillText('año '+y, xs(y-1), padT+innerH+18);}
  });

  // Lines
  function line(arr, col){
    ctx.strokeStyle = col; ctx.lineWidth = 2.4; ctx.beginPath();
    arr.forEach((v,i)=>{ const x=xs(i), y=ys(v); i===0?ctx.moveTo(x,y):ctx.lineTo(x,y); });
    ctx.stroke();
  }
  line(buy, '#1a56db');
  line(rent, '#f59e0b');

  // Break-even marker
  if(be){
    const x = xs(be-1);
    ctx.strokeStyle = '#059669'; ctx.setLineDash([4,4]); ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(x, padT); ctx.lineTo(x, padT+innerH); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = '#059669'; ctx.beginPath();
    ctx.arc(x, ys(buy[be-1]), 5, 0, Math.PI*2); ctx.fill();
  }
}

document.querySelectorAll('#city,#surface,#rate,#years,#downpct,#rentinc').forEach(el=>{
  el.addEventListener('input', compute);
  el.addEventListener('change', compute);
});

loadCities();
</script>
</body>
</html>
"""


# ============================================================================
#  TOOL 2 — Calculadora hipoteca
# ============================================================================
CALC_TITLE = "Calculadora de hipoteca con gastos por CCAA"
CALC_DESC = "Calculadora de hipoteca con cuota mensual, total intereses, gastos de compra reales por comunidad autónoma (ITP/IVA, notario, registro) y tabla de amortización completa."
CALC_SLUG = "calculadora-hipoteca.html"

CALC_JSON_LD = """{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Calculadora de hipoteca por CCAA — Ren Data",
  "url": "https://rendata.es/calculadora-hipoteca.html",
  "applicationCategory": "FinanceApplication",
  "operatingSystem": "Web",
  "description": "Calcula tu cuota mensual de hipoteca, total intereses, gastos de compra reales por comunidad autónoma (ITP, notario, registro, gestoría) y consulta la tabla de amortización año a año.",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
  "inLanguage": "es-ES",
  "publisher": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"}
}"""

CALC_HTML = head(CALC_TITLE, CALC_DESC, CALC_SLUG, CALC_JSON_LD) + breadcrumb_ld("Calculadora de hipoteca", CALC_SLUG) + """<style>
:root{--bg:#f8fafc;--white:#fff;--blue:#1a56db;--blue-d:#1140a6;--blue-l:#eff6ff;--text:#0e1828;--text2:#374151;--muted:#6b7a8d;--border:#e5eaf2;--border2:#d1dae8;--green:#059669;--green-bg:#ecfdf5;--red:#dc2626;--red-bg:#fef2f2;--sh:0 1px 3px rgba(14,24,40,.08),0 4px 12px rgba(14,24,40,.05);--font:'Plus Jakarta Sans',sans-serif;--r:14px}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:var(--font);font-weight:400;line-height:1.6;-webkit-font-smoothing:antialiased}
header{background:rgba(255,255,255,.93);backdrop-filter:blur(16px);border-bottom:1px solid var(--border);padding:0 2.5rem;height:66px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200}
.logo img{height:32px;width:auto;display:block}
nav a{font-size:.82rem;font-weight:500;color:var(--muted);text-decoration:none;padding:.45rem .85rem;border-radius:8px;transition:all .15s}
nav a:hover{color:var(--blue);background:var(--blue-l)}
.tool-hero{background:linear-gradient(135deg,#0a1628 0%,#1a3a7a 50%,#0f1b3d 100%);color:#fff;padding:3rem 2rem 2.5rem;text-align:center}
.tool-hero h1{font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;letter-spacing:-.03em;margin:0 0 .7rem}
.tool-hero p{font-size:1.05rem;color:rgba(226,232,240,.92);max-width:680px;margin:0 auto}
.crumb{max-width:1100px;margin:1.5rem auto 0;padding:0 2rem;font-size:.78rem;color:var(--muted)}
.crumb a{color:var(--muted);text-decoration:none}
.crumb a:hover{color:var(--blue)}
.tool-wrap{max-width:1100px;margin:2rem auto;padding:0 2rem 4rem}
.tool-grid{display:grid;grid-template-columns:340px 1fr;gap:1.5rem;align-items:start}
@media(max-width:860px){.tool-grid{grid-template-columns:1fr}}
.card{background:var(--white);border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;box-shadow:var(--sh)}
.card h2{font-size:1.05rem;font-weight:800;letter-spacing:-.02em;margin-bottom:1rem}
.f-group{margin-bottom:1.1rem}
.f-label{display:block;font-size:.78rem;font-weight:700;color:var(--text2);margin-bottom:.4rem}
.f-input,.f-select{width:100%;background:#fff;border:1.5px solid var(--border2);border-radius:8px;padding:.65rem .9rem;font-size:.95rem;font-family:inherit;color:var(--text);outline:none;transition:border-color .15s}
.f-input:focus,.f-select:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(26,86,219,.1)}
.f-hint{font-size:.7rem;color:var(--muted);margin-top:.3rem}
.f-row{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}
.kpi-row{display:grid;grid-template-columns:repeat(2,1fr);gap:.7rem;margin-bottom:1rem}
.kpi-row.three{grid-template-columns:repeat(3,1fr)}
.kpi{background:var(--blue-l);border:1px solid #c7d8f6;border-radius:10px;padding:.85rem 1rem}
.kpi-l{font-size:.65rem;font-weight:700;color:var(--blue);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.3rem}
.kpi-v{font-size:1.25rem;font-weight:800;letter-spacing:-.02em;color:var(--text)}
.kpi.k-warn{background:#fef9c3;border-color:#fde68a} .kpi.k-warn .kpi-l{color:#a16207}
.kpi.k-ok{background:var(--green-bg);border-color:#a7f3d0} .kpi.k-ok .kpi-l{color:var(--green)}
.kpi.k-bad{background:var(--red-bg);border-color:#fecaca} .kpi.k-bad .kpi-l{color:var(--red)}
.summary{background:#0f1b3d;color:#fff;border-radius:10px;padding:1.1rem 1.3rem;font-size:.92rem;line-height:1.55;margin-bottom:1rem}
.summary strong{color:#34d399}
table.amort{width:100%;border-collapse:collapse;margin-top:.8rem;font-size:.85rem}
table.amort th,table.amort td{padding:.5rem .7rem;text-align:right;border-bottom:1px solid var(--border)}
table.amort th{background:#f1f5f9;font-weight:700;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--text)}
table.amort td:first-child,table.amort th:first-child{text-align:left}
.gastos-table{margin-top:1rem;width:100%;border-collapse:collapse;font-size:.88rem}
.gastos-table td{padding:.4rem .8rem;border-bottom:1px solid var(--border)}
.gastos-table td:last-child{text-align:right;font-weight:700}
.note{font-size:.78rem;color:var(--muted);margin-top:1rem;line-height:1.55}
</style>
</head>
<body>
""" + NAV_HTML + """
<section class="tool-hero">
  <h1>💶 Calculadora de hipoteca</h1>
  <p>Calcula tu cuota mensual, total de intereses pagados, gastos reales de compra según tu CCAA (ITP, notario, registro, gestoría) y consulta la tabla de amortización año a año.</p>
</section>

<nav class="crumb"><a href="/">Inicio</a> · <a href="/analisis.html">Herramientas</a> · Calculadora de hipoteca</nav>

<div class="tool-wrap">
  <div class="tool-grid">
    <div class="card">
      <h2>📋 Datos</h2>
      <div class="f-group">
        <label class="f-label" for="price">Precio vivienda (€)</label>
        <input class="f-input" id="price" type="number" min="20000" step="1000" value="200000">
      </div>
      <div class="f-group">
        <label class="f-label" for="savings">Ahorros disponibles (€)</label>
        <input class="f-input" id="savings" type="number" min="0" step="1000" value="50000">
        <div class="f-hint">Cubre entrada y gastos de compra</div>
      </div>
      <div class="f-row">
        <div class="f-group">
          <label class="f-label" for="rate">Interés (%)</label>
          <input class="f-input" id="rate" type="number" step="0.1" min="0.5" max="10" value="3.5">
        </div>
        <div class="f-group">
          <label class="f-label" for="years">Plazo (años)</label>
          <input class="f-input" id="years" type="number" min="10" max="40" value="30">
        </div>
      </div>
      <div class="f-group">
        <label class="f-label" for="ccaa">Comunidad autónoma</label>
        <select class="f-select" id="ccaa">
          <option value="Andalucía">Andalucía (ITP 7%)</option>
          <option value="Aragón">Aragón (ITP 8%)</option>
          <option value="Asturias">Asturias (ITP 8%)</option>
          <option value="Islas Baleares">Islas Baleares (ITP 11%)</option>
          <option value="Canarias">Canarias (ITP 6,5%)</option>
          <option value="Cantabria">Cantabria (ITP 9%)</option>
          <option value="Castilla-La Mancha">Castilla-La Mancha (ITP 9%)</option>
          <option value="Castilla y León">Castilla y León (ITP 8%)</option>
          <option value="Cataluña">Cataluña (ITP 10%)</option>
          <option value="C. Valenciana">C. Valenciana (ITP 10%)</option>
          <option value="Extremadura">Extremadura (ITP 8%)</option>
          <option value="Galicia">Galicia (ITP 10%)</option>
          <option value="La Rioja">La Rioja (ITP 7%)</option>
          <option value="C. de Madrid" selected>C. de Madrid (ITP 6%)</option>
          <option value="R. de Murcia">R. de Murcia (ITP 8%)</option>
          <option value="Navarra">Navarra (ITP 6%)</option>
          <option value="País Vasco">País Vasco (ITP 7%)</option>
        </select>
      </div>
      <div class="f-group">
        <label class="f-label" for="vivtype">Tipo de vivienda</label>
        <select class="f-select" id="vivtype">
          <option value="segunda" selected>Segunda mano (paga ITP)</option>
          <option value="nueva">Obra nueva (paga IVA 10% + AJD)</option>
        </select>
      </div>
    </div>

    <div class="card">
      <h2>📊 Resultados</h2>
      <div id="results"></div>
    </div>
  </div>

  <div class="card" style="margin-top:1.5rem">
    <h2>💡 Notas</h2>
    <p class="note"><strong>Cálculos.</strong> Cuota mensual con sistema francés (cuota constante). <strong>Gastos de compra de segunda mano</strong>: ITP según CCAA + notario (~0,5%) + registro (~0,4%) + gestoría (~300€). <strong>Obra nueva</strong>: IVA 10% + AJD 1,5% (excepto Madrid 0,75%, Canarias 1%) + notario + registro + gestoría. Los porcentajes ITP son los tipos generales 2026; pueden existir reducciones por jóvenes &lt;35, familia numerosa, vivienda habitual, etc. <strong>Banco</strong>: la mayoría de bancos financian hasta el 80% del valor de tasación; el 20% restante más los gastos de compra los aporta el comprador (≈30% del precio).</p>
  </div>
</div>

<footer style="border-top:1px solid var(--border);background:#fff;padding:1.5rem 2rem;text-align:center;font-size:.8rem;color:var(--muted)">
  © 2026 Ren Data · <a href="/" style="color:var(--blue);text-decoration:none">Inicio</a> · <a href="/metodologia.html" style="color:var(--blue);text-decoration:none">Metodología</a> · <a href="/sobre.html" style="color:var(--blue);text-decoration:none">Sobre</a>
</footer>

<script src="/js/nav-dropdown.js" defer></script>
<script>
// ITP/IVA por CCAA (% sobre precio vivienda)
const ITP = {
  "Andalucía": 7, "Aragón": 8, "Asturias": 8, "Islas Baleares": 11, "Canarias": 6.5,
  "Cantabria": 9, "Castilla-La Mancha": 9, "Castilla y León": 8, "Cataluña": 10,
  "C. Valenciana": 10, "Extremadura": 8, "Galicia": 10, "La Rioja": 7,
  "C. de Madrid": 6, "R. de Murcia": 8, "Navarra": 6, "País Vasco": 7
};
const AJD = { "C. de Madrid": 0.75, "Canarias": 1 };

function fmt(n){ return Math.round(n).toLocaleString('es-ES'); }
function fmtE(n){ return '€' + fmt(n); }
function fmtPct(n){ return n.toFixed(2).replace('.',',') + '%'; }

function monthlyPayment(principal, annualRate, years){
  const r = annualRate / 100 / 12;
  const n = years * 12;
  if (r === 0) return principal / n;
  return principal * (r * Math.pow(1+r,n)) / (Math.pow(1+r,n) - 1);
}

function compute(){
  const price = +document.getElementById('price').value || 0;
  const savings = +document.getElementById('savings').value || 0;
  const rate = +document.getElementById('rate').value || 3.5;
  const years = Math.min(40, Math.max(10, +document.getElementById('years').value || 30));
  const ccaa = document.getElementById('ccaa').value;
  const tipo = document.getElementById('vivtype').value;

  // Gastos de compra
  let ivaItp, ivaItpLabel, ajd = 0, ajdLabel = '—';
  if (tipo === 'segunda'){
    ivaItp = price * (ITP[ccaa] || 0) / 100;
    ivaItpLabel = `ITP ${fmtPct(ITP[ccaa])} (${ccaa})`;
  } else {
    ivaItp = price * 0.10;
    ivaItpLabel = 'IVA 10% (obra nueva)';
    const ajdRate = (AJD[ccaa] !== undefined ? AJD[ccaa] : 1.5);
    ajd = price * ajdRate / 100;
    ajdLabel = `AJD ${fmtPct(ajdRate)} (${ccaa})`;
  }
  const notario = price * 0.005;
  const registro = price * 0.004;
  const gestoria = 300;
  const tasacion = 350;
  const totalGastos = ivaItp + ajd + notario + registro + gestoria + tasacion;

  // Hipoteca: banco financia hasta 80% del precio. Entrada = 20%.
  // Entrada mínima necesaria = 20% del precio. Ahorros disponibles deben cubrir entrada + gastos.
  const entradaMin = price * 0.20;
  const ahorroNecesario = entradaMin + totalGastos;
  const loan = Math.max(0, price - entradaMin);  // 80% financiable
  const monthly = monthlyPayment(loan, rate, years);
  const totalPagado = monthly * 12 * years;
  const totalIntereses = totalPagado - loan;

  const cubreAhorros = savings >= ahorroNecesario;

  // Tabla amortización (por año)
  const r = rate / 100 / 12;
  let saldo = loan;
  const rows = [];
  for(let y=1; y<=years; y++){
    let capPagado = 0, intPagado = 0;
    for(let m=1; m<=12; m++){
      const interes = saldo * r;
      const capital = monthly - interes;
      saldo -= capital;
      capPagado += capital;
      intPagado += interes;
    }
    rows.push({y, capital:capPagado, interes:intPagado, saldo:Math.max(0,saldo)});
  }

  const showYears = [1,2,3,5,10,15,20,25,30,35,40].filter(y=>y<=years);
  const tabla = `<table class="amort">
    <thead><tr><th>Año</th><th>Capital</th><th>Intereses</th><th>Capital pendiente</th></tr></thead>
    <tbody>${showYears.map(y=>{
      const r = rows[y-1];
      return `<tr><td>Año ${y}</td><td>${fmtE(r.capital)}</td><td>${fmtE(r.interes)}</td><td>${fmtE(r.saldo)}</td></tr>`;
    }).join('')}</tbody></table>`;

  const gastosTabla = `<table class="gastos-table">
    <tr><td>Entrada (20%)</td><td>${fmtE(entradaMin)}</td></tr>
    <tr><td>${ivaItpLabel}</td><td>${fmtE(ivaItp)}</td></tr>
    ${tipo==='nueva'?`<tr><td>${ajdLabel}</td><td>${fmtE(ajd)}</td></tr>`:''}
    <tr><td>Notaría (~0,5%)</td><td>${fmtE(notario)}</td></tr>
    <tr><td>Registro (~0,4%)</td><td>${fmtE(registro)}</td></tr>
    <tr><td>Gestoría</td><td>${fmtE(gestoria)}</td></tr>
    <tr><td>Tasación</td><td>${fmtE(tasacion)}</td></tr>
    <tr style="background:#f1f5f9;font-weight:800"><td>Total ahorro necesario</td><td>${fmtE(ahorroNecesario)}</td></tr>
  </table>`;

  document.getElementById('results').innerHTML = `
    <div class="kpi-row three">
      <div class="kpi"><div class="kpi-l">Cuota mensual</div><div class="kpi-v">${fmtE(monthly)}</div></div>
      <div class="kpi k-warn"><div class="kpi-l">Total intereses</div><div class="kpi-v">${fmtE(totalIntereses)}</div></div>
      <div class="kpi"><div class="kpi-l">Total pagado banco</div><div class="kpi-v">${fmtE(loan+totalIntereses)}</div></div>
    </div>
    <div class="kpi-row">
      <div class="kpi ${cubreAhorros?'k-ok':'k-bad'}">
        <div class="kpi-l">Ahorro necesario</div>
        <div class="kpi-v">${fmtE(ahorroNecesario)}</div>
      </div>
      <div class="kpi ${cubreAhorros?'k-ok':'k-bad'}">
        <div class="kpi-l">${cubreAhorros?'Tus ahorros cubren':'Te faltan'}</div>
        <div class="kpi-v">${cubreAhorros?'✓ Cubierto':fmtE(ahorroNecesario - savings)}</div>
      </div>
    </div>
    <div class="summary">
      Para una vivienda de <strong>${fmtE(price)}</strong> en ${ccaa} necesitas
      <strong>${fmtE(ahorroNecesario)}</strong> de ahorros (20% entrada + ~${fmtPct(totalGastos/price*100)} de gastos).
      El banco te financia <strong>${fmtE(loan)}</strong> a ${years} años al ${fmtPct(rate)},
      con cuota mensual de <strong>${fmtE(monthly)}</strong>. Pagarás <strong>${fmtE(totalIntereses)}</strong>
      en intereses durante toda la hipoteca.
    </div>
    <h2 style="font-size:.92rem;font-weight:800;margin:1rem 0 .4rem">💸 Desglose de gastos</h2>
    ${gastosTabla}
    <h2 style="font-size:.92rem;font-weight:800;margin:1.2rem 0 .4rem">📅 Tabla de amortización</h2>
    ${tabla}
  `;
}

document.querySelectorAll('#price,#savings,#rate,#years,#ccaa,#vivtype').forEach(el=>{
  el.addEventListener('input', compute);
  el.addEventListener('change', compute);
});
compute();
</script>
</body>
</html>
"""

# Write the tool pages
(ROOT / SIM_SLUG).write_text(SIMULADOR_HTML, encoding="utf-8")
print(f"[1] Created {SIM_SLUG}")
(ROOT / CALC_SLUG).write_text(CALC_HTML, encoding="utf-8")
print(f"[2] Created {CALC_SLUG}")


# ============================================================================
#  Update nav across ALL pages — add tool links after Comparador
# ============================================================================
RE_DESKTOP_NAV = re.compile(
    r'(<a href="/comparador\.html">Comparador</a>)',
    re.IGNORECASE,
)
RE_MOBILE_NAV = re.compile(
    r'(<a href="/comparador\.html">⚖️ Comparar</a>)',
    re.IGNORECASE,
)
DESKTOP_ADD = '<a href="/simulador-comprar-vs-alquilar.html">Comprar vs alquilar</a><a href="/calculadora-hipoteca.html">Calculadora hipoteca</a>'
MOBILE_ADD = '<a href="/simulador-comprar-vs-alquilar.html">🔄 Comprar vs alquilar</a><a href="/calculadora-hipoteca.html">💶 Calculadora hipoteca</a>'

# Already-present guard
HAS_SIM = re.compile(r'href="/simulador-comprar-vs-alquilar\.html"')

modified = 0
for f in sorted(ROOT.glob("*.html")):
    if f.name in (SIM_SLUG, CALC_SLUG): continue
    txt = f.read_text(encoding="utf-8")
    if HAS_SIM.search(txt): continue   # already linked
    orig = txt
    if RE_DESKTOP_NAV.search(txt):
        txt = RE_DESKTOP_NAV.sub(lambda m: m.group(1) + DESKTOP_ADD, txt, count=1)
    if RE_MOBILE_NAV.search(txt):
        txt = RE_MOBILE_NAV.sub(lambda m: m.group(1) + MOBILE_ADD, txt, count=1)
    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        modified += 1
print(f"[3] Nav links added in {modified} pages")


# ============================================================================
#  Add cards to analisis.html
# ============================================================================
analisis = ROOT / "analisis.html"
txt = analisis.read_text(encoding="utf-8")

# Look for the first <article class="an-card"> or <div class="an-card"> and prepend the tool cards
# Simpler: detect a placeholder marker; if not present, insert before the first an-card occurrence.
TOOL_CARDS = """<article class="an-card">
      <div class="an-card-body">
        <span class="an-card-tag" style="background:#dbeafe;color:#1140a6">🛠 Herramienta</span>
        <h2><a href="/simulador-comprar-vs-alquilar.html">Simulador: comprar vs alquilar vivienda en España</a></h2>
        <p class="an-card-desc">Calcula en qué año comprar sale más barato que alquilar en cualquiera de las 587 ciudades. Gráfico interactivo del coste acumulado a 30 años, con datos reales de precio m² y alquiler medio.</p>
        <div class="an-card-meta">
          <span class="an-card-date">🔧 Herramienta interactiva</span>
          <a href="/simulador-comprar-vs-alquilar.html" class="an-card-link">Abrir simulador →</a>
        </div>
      </div>
    </article>
    <article class="an-card">
      <div class="an-card-body">
        <span class="an-card-tag" style="background:#dbeafe;color:#1140a6">🛠 Herramienta</span>
        <h2><a href="/calculadora-hipoteca.html">Calculadora de hipoteca con gastos por CCAA</a></h2>
        <p class="an-card-desc">Cuota mensual, total intereses, gastos reales de compra según comunidad autónoma (ITP/IVA, notario, registro, gestoría) y tabla de amortización completa año a año.</p>
        <div class="an-card-meta">
          <span class="an-card-date">🔧 Herramienta interactiva</span>
          <a href="/calculadora-hipoteca.html" class="an-card-link">Abrir calculadora →</a>
        </div>
      </div>
    </article>
    """

# Insert before the first <article class="an-card"> (only if not already inserted)
if "simulador-comprar-vs-alquilar.html" not in re.sub(r'<nav[\s\S]*?</nav>', '', txt, count=1):
    new_txt, n = re.subn(r'(<article class="an-card">)', TOOL_CARDS + r'\1', txt, count=1)
    if n > 0:
        analisis.write_text(new_txt, encoding="utf-8")
        print("[4] Inserted tool cards into analisis.html")
    else:
        print("[4] WARN: couldn't find an-card anchor in analisis.html")
else:
    print("[4] analisis.html already has tool cards")

print("\nBLOCK 3 & 4 done.")
