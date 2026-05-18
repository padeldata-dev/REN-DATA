/*!
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
