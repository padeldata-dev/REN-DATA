#!/usr/bin/env python3
"""Generates widget.js (embeddable) + widget-data.json + widget-demo.html."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
INDEX = BETA / "index.html"

# ---------------------------------------------------------------------------
# Build widget-data.json
# ---------------------------------------------------------------------------

def parse_data():
    html = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
                     r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
                     r'd:(\d+),sl:"([^"]+)"')
    out = {}
    for m in pat.finditer(html):
        sl = m.group(10)
        out[sl] = {
            "n": m.group(1), "cc": m.group(2),
            "roi": float(m.group(4)), "p": int(m.group(5)),
            "alq": int(m.group(6)), "vp": float(m.group(7)),
        }
    return out


data = parse_data()
(BETA / "widget-data.json").write_text(
    json.dumps(data, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8",
)
print(f"widget-data.json: {len(data)} cities")

# ---------------------------------------------------------------------------
# Build widget.js — no deps, IIFE, scoped CSS, reads data-ciudad attribute
# ---------------------------------------------------------------------------

WIDGET_JS = r'''/*!
 * Ren Data widget v1.0 — Rentabilidad inmobiliaria embebible
 * https://rendata.es/widget.html
 * Uso: <script src="https://rendata.es/widget.js" data-ciudad="madrid"></script>
 *  o:   <div class="rendata-widget" data-ciudad="bilbao"></div>
 *       <script src="https://rendata.es/widget.js"></script>
 */
(function () {
  "use strict";
  var BASE = "https://rendata.es";
  var DATA_URL = BASE + "/widget-data.json";
  var STYLE_ID = "rendata-widget-style";
  var dataPromise = null;

  function loadData() {
    if (dataPromise) return dataPromise;
    dataPromise = fetch(DATA_URL, { cache: "force-cache" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      });
    return dataPromise;
  }

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var css =
      '.rendata-widget{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;max-width:380px;background:#fff;border:1px solid #e5eaf2;border-radius:14px;padding:1.2rem 1.4rem;box-shadow:0 2px 8px rgba(14,24,40,.06);color:#0f1923;line-height:1.55;text-align:left;box-sizing:border-box}' +
      '.rendata-widget *{box-sizing:border-box}' +
      '.rdw-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:.7rem;padding-bottom:.7rem;border-bottom:1px solid #f1f5f9}' +
      '.rdw-logo{font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#1a56db;text-decoration:none}' +
      '.rdw-logo span{color:#0e2a6b}' +
      '.rdw-q{font-size:.66rem;color:#94a3b8;font-weight:500}' +
      '.rdw-city{font-size:1.15rem;font-weight:800;letter-spacing:-.02em;color:#0f1923;margin-bottom:.1rem}' +
      '.rdw-cc{font-size:.78rem;color:#6b7a8d;margin-bottom:1rem}' +
      '.rdw-grid{display:grid;grid-template-columns:1fr 1fr;gap:.75rem;margin-bottom:1rem}' +
      '.rdw-kpi{background:#f8fafc;border-radius:8px;padding:.7rem .8rem}' +
      '.rdw-kpi-v{font-size:1.08rem;font-weight:800;color:#1a56db;letter-spacing:-.02em;line-height:1.15}' +
      '.rdw-kpi-l{font-size:.66rem;color:#6b7a8d;text-transform:uppercase;letter-spacing:.06em;font-weight:600;margin-top:.15rem}' +
      '.rdw-cta{display:block;background:#1a56db;color:#fff;text-decoration:none;padding:.7rem 1rem;border-radius:8px;font-weight:700;font-size:.85rem;text-align:center;transition:background .15s}' +
      '.rdw-cta:hover{background:#0e2a6b}' +
      '.rdw-err{color:#dc2626;font-size:.85rem;padding:1rem 0;text-align:center}' +
      '.rdw-loading{color:#94a3b8;font-size:.85rem;padding:1rem 0;text-align:center}';
    var s = document.createElement("style");
    s.id = STYLE_ID;
    s.appendChild(document.createTextNode(css));
    document.head.appendChild(s);
  }

  function fmtEU(n) {
    return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function fmtPct(n) {
    return n.toFixed(1).replace(".", ",");
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function renderInto(container, ciudad) {
    container.innerHTML = '<div class="rdw-loading">Cargando datos de ' + escapeHtml(ciudad) + '…</div>';
    container.classList.add("rendata-widget");
    loadData().then(function (dict) {
      var c = dict[ciudad];
      if (!c) {
        container.innerHTML =
          '<div class="rdw-head"><a class="rdw-logo" href="' + BASE + '" target="_blank" rel="noopener">Ren<span>Data</span></a></div>' +
          '<div class="rdw-err">No hay datos para la ciudad <strong>"' + escapeHtml(ciudad) + '"</strong>.<br/>Visita <a href="' + BASE + '" target="_blank" rel="noopener" style="color:#1a56db">rendata.es</a> para ver las ciudades disponibles.</div>';
        return;
      }
      var url = BASE + "/rentabilidad-" + encodeURIComponent(ciudad) + ".html";
      container.innerHTML =
        '<div class="rdw-head">' +
          '<a class="rdw-logo" href="' + BASE + '" target="_blank" rel="noopener">Ren<span>Data</span></a>' +
          '<span class="rdw-q">Q2 2026</span>' +
        '</div>' +
        '<div class="rdw-city">' + escapeHtml(c.n) + '</div>' +
        '<div class="rdw-cc">' + escapeHtml(c.cc) + '</div>' +
        '<div class="rdw-grid">' +
          '<div class="rdw-kpi"><div class="rdw-kpi-v">' + fmtPct(c.roi) + '%</div><div class="rdw-kpi-l">ROI bruto</div></div>' +
          '<div class="rdw-kpi"><div class="rdw-kpi-v">' + fmtEU(c.p) + '€</div><div class="rdw-kpi-l">Precio m²</div></div>' +
          '<div class="rdw-kpi"><div class="rdw-kpi-v">' + fmtEU(c.alq) + '€</div><div class="rdw-kpi-l">Alquiler/mes</div></div>' +
          '<div class="rdw-kpi"><div class="rdw-kpi-v">+' + fmtPct(c.vp) + '%</div><div class="rdw-kpi-l">Subida anual</div></div>' +
        '</div>' +
        '<a class="rdw-cta" href="' + url + '" target="_blank" rel="noopener">Ver análisis completo →</a>';
    }).catch(function () {
      container.innerHTML =
        '<div class="rdw-head"><a class="rdw-logo" href="' + BASE + '" target="_blank" rel="noopener">Ren<span>Data</span></a></div>' +
        '<div class="rdw-err">Error al cargar los datos. Recarga la página o visita <a href="' + BASE + '" target="_blank" style="color:#1a56db">rendata.es</a></div>';
    });
  }

  function init() {
    injectStyle();
    // 1) Script tag with data-ciudad: render in-place (after the script)
    var scripts = document.querySelectorAll('script[src*="widget.js"][data-ciudad]');
    scripts.forEach(function (s) {
      var ciudad = (s.getAttribute("data-ciudad") || "").trim().toLowerCase();
      if (!ciudad) return;
      var container = document.createElement("div");
      s.parentNode.insertBefore(container, s.nextSibling);
      renderInto(container, ciudad);
    });
    // 2) Pre-existing divs with .rendata-widget data-ciudad
    var divs = document.querySelectorAll("div.rendata-widget[data-ciudad], div[data-rendata-ciudad]");
    divs.forEach(function (d) {
      var ciudad = (d.getAttribute("data-ciudad") || d.getAttribute("data-rendata-ciudad") || "").trim().toLowerCase();
      if (!ciudad) return;
      renderInto(d, ciudad);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
'''

(BETA / "widget.js").write_text(WIDGET_JS, encoding="utf-8")
print(f"widget.js written: {len(WIDGET_JS)} bytes")

# ---------------------------------------------------------------------------
# widget-demo.html
# ---------------------------------------------------------------------------

DEMO_HTML = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Widget de rentabilidad para tu web — Ren Data</title>
<meta name="description" content="Widget JavaScript gratuito para mostrar la rentabilidad inmobiliaria de cualquier ciudad española en tu web. Sin dependencias, fácil de integrar, datos actualizados.">
<link rel="canonical" href="https://rendata.es/widget-demo.html">
<meta property="og:type" content="website">
<meta property="og:title" content="Widget embebable Ren Data — Rentabilidad por ciudad">
<meta property="og:description" content="Incrusta el yield de cualquier ciudad española en tu web con una sola línea de código.">
<meta property="og:url" content="https://rendata.es/widget-demo.html">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/nav.css">
<script src="/js/nav-dropdown.js" defer></script>
<style>
:root{--bg:#f8fafc;--white:#fff;--blue:#1a56db;--navy:#0e2a6b;--text:#0f1923;--text2:#374151;--muted:#6b7a8d;--border:#e5eaf2;--font:'Plus Jakarta Sans',sans-serif}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:var(--font);line-height:1.65;-webkit-font-smoothing:antialiased}
header{background:#0e2a6b;padding:0 2rem;height:64px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
header .logo{text-decoration:none;color:#fff;font-size:1.1rem;font-weight:800}
header .logo span.ac{color:#60a5fa}
header nav{display:flex;gap:.2rem}
header nav a{font-size:.82rem;font-weight:500;color:rgba(255,255,255,.7);text-decoration:none;padding:.42rem .8rem;border-radius:8px}
header nav a:hover{color:#fff;background:rgba(255,255,255,.12)}

.hero{background:#fff;border-bottom:1px solid var(--border);padding:4rem 2rem 3rem;text-align:center}
.hero-inner{max-width:760px;margin:0 auto}
.eyebrow{font-size:.72rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);margin-bottom:.8rem}
.hero h1{font-size:clamp(2rem,4vw,2.8rem);font-weight:800;letter-spacing:-.04em;line-height:1.15;margin-bottom:1rem}
.hero h1 .ac{color:var(--blue)}
.hero p{font-size:1.05rem;color:var(--muted);max-width:600px;margin:0 auto}

.section{max-width:960px;margin:3rem auto;padding:0 2rem}
.section h2{font-size:1.4rem;font-weight:800;letter-spacing:-.03em;margin-bottom:1.2rem;color:var(--text)}
.section p{font-size:.92rem;color:var(--text2);margin-bottom:1rem}

.demo-row{display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start;margin:2rem 0}
.demo-col h3{font-size:1rem;font-weight:700;color:var(--text);margin-bottom:.8rem}
.code-block{background:#0f1923;color:#e5eaf2;font-family:'Consolas','SF Mono','Menlo',monospace;font-size:.82rem;padding:1.2rem 1.4rem;border-radius:10px;overflow-x:auto;line-height:1.55;position:relative}
.code-block code{color:#e5eaf2;background:transparent}
.code-block .k{color:#60a5fa}
.code-block .s{color:#a3e635}
.code-block .a{color:#fbbf24}
.code-block .c{color:#94a3b8;font-style:italic}
.copy-btn{position:absolute;top:.6rem;right:.6rem;background:rgba(255,255,255,.1);color:#cbd5e1;border:1px solid rgba(255,255,255,.15);padding:.3rem .7rem;border-radius:6px;font-size:.7rem;font-weight:600;cursor:pointer;font-family:inherit;transition:all .15s}
.copy-btn:hover{background:rgba(255,255,255,.2);color:#fff}
.copy-btn.copied{background:#059669;color:#fff;border-color:#059669}

.live-demo{padding:1.5rem;background:#fff;border:1.5px dashed var(--border);border-radius:12px;display:flex;align-items:center;justify-content:center;min-height:280px}

.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin:2rem 0}
.feat{background:#fff;border:1px solid var(--border);border-radius:12px;padding:1.4rem 1.2rem;text-align:center;box-shadow:0 1px 3px rgba(14,24,40,.05)}
.feat-icon{font-size:1.8rem;margin-bottom:.6rem}
.feat h3{font-size:.95rem;font-weight:700;margin-bottom:.4rem;color:var(--text)}
.feat p{font-size:.82rem;color:var(--muted);margin:0;line-height:1.55}

.examples-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.5rem;margin:2rem 0}
.example-cell{display:flex;flex-direction:column;gap:.6rem}
.example-cell .label{font-size:.78rem;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}

.cta-block{background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:3rem 2rem;text-align:center;border-radius:14px;margin:3rem 0}
.cta-block h2{color:#fff;font-size:1.6rem;font-weight:800;letter-spacing:-.03em;margin-bottom:.8rem}
.cta-block p{color:rgba(255,255,255,.85);font-size:.95rem;max-width:520px;margin:0 auto 1.5rem}
.cta-block .cta-btn{display:inline-block;background:#fff;color:#0e2a6b;font-weight:700;padding:.9rem 1.8rem;border-radius:8px;text-decoration:none;font-size:.9rem;transition:transform .15s}
.cta-block .cta-btn:hover{transform:translateY(-2px)}

.faq-list{margin:2rem 0}
.faq{background:#fff;border:1px solid var(--border);border-radius:10px;margin-bottom:.6rem;overflow:hidden}
.faq summary{padding:1rem 1.2rem;font-size:.92rem;font-weight:600;cursor:pointer;list-style:none;display:flex;align-items:center;justify-content:space-between}
.faq summary::after{content:'+';font-size:1.3rem;color:var(--blue);font-weight:300;transition:transform .2s}
.faq[open] summary::after{transform:rotate(45deg)}
.faq-body{padding:0 1.2rem 1.2rem;font-size:.86rem;color:var(--text2);line-height:1.65}
.faq-body code{background:#f1f5f9;padding:.1rem .35rem;border-radius:4px;font-family:'Consolas',monospace;font-size:.8rem;color:#0f1923}

footer{padding:2rem;text-align:center;font-size:.8rem;color:var(--muted);border-top:1px solid var(--border);margin-top:3rem}
footer a{color:var(--blue);text-decoration:none}

@media (max-width:740px){
  .demo-row,.feat-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>

<header>
  <a href="/" class="logo">Ren<span class="ac"> Data</span></a>
  <nav>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/metodologia.html">Metodología</a>
    <a href="/contacto.html">Contacto</a>
  </nav>
</header>

<section class="hero">
  <div class="hero-inner">
    <div class="eyebrow">Widget gratuito</div>
    <h1>Incrusta el <span class="ac">yield real</span> de cualquier ciudad española en tu web</h1>
    <p>Una línea de código. Sin dependencias. Datos oficiales actualizados trimestralmente. Diseño limpio que se adapta a tu sitio.</p>
  </div>
</section>

<section class="section">
  <h2>¿Cómo se usa?</h2>
  <p>Copia esta línea, sustituye <code style="background:#f1f5f9;padding:.15rem .4rem;border-radius:4px">madrid</code> por el slug de la ciudad que quieras mostrar, y pégalo en el HTML donde aparezca el widget:</p>

  <div class="demo-row">
    <div class="demo-col">
      <h3>📋 Código a copiar</h3>
      <div class="code-block">
        <button class="copy-btn" onclick="copyCode(this,'snippet1')">Copiar</button>
        <pre id="snippet1"><span class="k">&lt;script</span> <span class="a">src</span>=<span class="s">"https://rendata.es/widget.js"</span> <span class="a">data-ciudad</span>=<span class="s">"madrid"</span><span class="k">&gt;&lt;/script&gt;</span></pre>
      </div>
    </div>
    <div class="demo-col">
      <h3>👁️ Lo que verán tus visitantes</h3>
      <div class="live-demo">
        <script src="/widget.js" data-ciudad="madrid"></script>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2>Características</h2>
  <div class="feat-grid">
    <div class="feat">
      <div class="feat-icon">⚡</div>
      <h3>Ligero y rápido</h3>
      <p>Menos de 5KB minificado. Carga asíncrona, no bloquea tu página.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">🔌</div>
      <h3>Sin dependencias</h3>
      <p>Vanilla JavaScript. Funciona en cualquier web — WordPress, Webflow, custom.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">📊</div>
      <h3>Datos siempre frescos</h3>
      <p>Se actualiza cada vez que publicamos nuevos datos trimestrales. Sin intervención por tu parte.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">🎨</div>
      <h3>Diseño limpio</h3>
      <p>Estilo neutro que encaja con cualquier marca. Sin tracking ni cookies de terceros.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">🆓</div>
      <h3>100% gratis</h3>
      <p>Uso libre comercial y personal. Solo te pedimos no eliminar el enlace a Ren Data.</p>
    </div>
    <div class="feat">
      <div class="feat-icon">📱</div>
      <h3>Responsive</h3>
      <p>Se adapta al ancho disponible. Móvil, tablet y desktop sin cambios.</p>
    </div>
  </div>
</section>

<section class="section">
  <h2>Más ejemplos en vivo</h2>
  <p>Cada widget de abajo se carga con su slug correspondiente. Cambia el <code style="background:#f1f5f9;padding:.15rem .4rem;border-radius:4px">data-ciudad</code> para apuntar a la ciudad que quieras.</p>

  <div class="examples-grid">
    <div class="example-cell">
      <div class="label">data-ciudad="bilbao"</div>
      <script src="/widget.js" data-ciudad="bilbao"></script>
    </div>
    <div class="example-cell">
      <div class="label">data-ciudad="zaragoza"</div>
      <script src="/widget.js" data-ciudad="zaragoza"></script>
    </div>
    <div class="example-cell">
      <div class="label">data-ciudad="valencia"</div>
      <script src="/widget.js" data-ciudad="valencia"></script>
    </div>
    <div class="example-cell">
      <div class="label">data-ciudad="sevilla"</div>
      <script src="/widget.js" data-ciudad="sevilla"></script>
    </div>
    <div class="example-cell">
      <div class="label">data-ciudad="cuenca"</div>
      <script src="/widget.js" data-ciudad="cuenca"></script>
    </div>
    <div class="example-cell">
      <div class="label">data-ciudad="palma"</div>
      <script src="/widget.js" data-ciudad="palma"></script>
    </div>
  </div>
</section>

<section class="section">
  <h2>Método alternativo: div con clase</h2>
  <p>Si prefieres tener el control del lugar exacto donde aparece el widget, usa este método:</p>

  <div class="demo-row">
    <div class="demo-col">
      <h3>📋 Código</h3>
      <div class="code-block">
        <button class="copy-btn" onclick="copyCode(this,'snippet2')">Copiar</button>
<pre id="snippet2"><span class="c">&lt;!-- En el lugar donde quieres el widget --&gt;</span>
<span class="k">&lt;div</span> <span class="a">class</span>=<span class="s">"rendata-widget"</span> <span class="a">data-ciudad</span>=<span class="s">"barcelona"</span><span class="k">&gt;&lt;/div&gt;</span>

<span class="c">&lt;!-- Al final del &lt;body&gt; --&gt;</span>
<span class="k">&lt;script</span> <span class="a">src</span>=<span class="s">"https://rendata.es/widget.js"</span><span class="k">&gt;&lt;/script&gt;</span></pre>
      </div>
    </div>
    <div class="demo-col">
      <h3>👁️ Resultado</h3>
      <div class="live-demo">
        <div class="rendata-widget" data-ciudad="barcelona"></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2>Preguntas frecuentes</h2>
  <div class="faq-list">
    <details class="faq">
      <summary>¿Qué pasa si la ciudad no existe en Ren Data?</summary>
      <div class="faq-body">El widget mostrará un mensaje claro indicando que no hay datos para esa ciudad, con un enlace para que el visitante explore las ciudades disponibles. Para ver todas las ciudades, visita <a href="/" target="_blank">la home</a>.</div>
    </details>
    <details class="faq">
      <summary>¿Cómo encuentro el slug de mi ciudad?</summary>
      <div class="faq-body">El slug es la última parte de la URL de la ficha. Por ejemplo, <code>rendata.es/rentabilidad-zaragoza.html</code> → slug es <code>zaragoza</code>. Para "Las Palmas de Gran Canaria" → <code>las-palmas-gc</code>. Para "San Sebastián" → <code>san-sebastian</code>.</div>
    </details>
    <details class="faq">
      <summary>¿Puedo personalizar el diseño?</summary>
      <div class="faq-body">El widget aplica estilos con prefijo <code>.rdw-*</code> y <code>.rendata-widget</code>. Puedes sobrescribirlos con tu propio CSS (con mayor especificidad o <code>!important</code>). Las clases principales: <code>.rendata-widget</code>, <code>.rdw-city</code>, <code>.rdw-kpi</code>, <code>.rdw-cta</code>.</div>
    </details>
    <details class="faq">
      <summary>¿Funciona con WordPress, Webflow, Squarespace?</summary>
      <div class="faq-body">Sí. Cualquier plataforma que permita insertar HTML/JavaScript admite el widget. En WordPress, usa el bloque "HTML personalizado". En Webflow, el bloque "Embed". En Squarespace, el bloque "Code".</div>
    </details>
    <details class="faq">
      <summary>¿Cuánto pesa?</summary>
      <div class="faq-body">El JavaScript es ~5KB. Los datos (widget-data.json) ~70KB y se cargan una sola vez aunque tengas varios widgets en la página (cacheado en memoria).</div>
    </details>
    <details class="faq">
      <summary>¿Hay límites de uso?</summary>
      <div class="faq-body">No. Uso libre. Solo te pedimos que no elimines el enlace a Ren Data del widget — es lo que nos permite mantener los datos gratis.</div>
    </details>
    <details class="faq">
      <summary>¿Cómo aviso si encuentro un error?</summary>
      <div class="faq-body">Escríbenos por el <a href="/contacto.html">formulario de contacto</a>. Te respondemos en menos de 48 horas en días laborables.</div>
    </details>
  </div>
</section>

<div class="section">
  <div class="cta-block">
    <h2>¿Listo para añadirlo?</h2>
    <p>Copia la línea de código, pégala en tu web y listo. En 5 minutos tienes datos de rentabilidad real en tu sitio.</p>
    <a href="#snippet1" class="cta-btn" onclick="window.scrollTo({top:0,behavior:'smooth'});return false">↑ Volver al código</a>
  </div>
</div>

<footer>
  <p>© 2026 <a href="/">Ren Data</a> · Widget gratuito · <a href="/metodologia.html">Ver metodología</a> · <a href="/contacto.html">Contacto</a></p>
</footer>

<script>
function copyCode(btn, id){
  var el = document.getElementById(id);
  var text = el.innerText || el.textContent;
  navigator.clipboard.writeText(text).then(function(){
    var orig = btn.textContent;
    btn.textContent = "✓ Copiado";
    btn.classList.add("copied");
    setTimeout(function(){ btn.textContent = orig; btn.classList.remove("copied"); }, 1800);
  });
}
</script>

</body>
</html>
'''

(BETA / "widget-demo.html").write_text(DEMO_HTML, encoding="utf-8")
print(f"widget-demo.html written")
