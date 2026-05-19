"""
FASE 3 BLOQUE 2 — Genera 8 articulos nuevos orientados a compradores.

Usa el template visual de top10.css / ciudades-baratas-comprar-piso-espana-2026.html
para mantener consistencia con el resto del corpus editorial.
"""

from pathlib import Path

ROOT       = Path(__file__).resolve().parents[1]
FICHAS_DIR = ROOT / "rendata_beta"

ADSENSE = ('<script async src="https://pagead2.googlesyndication.com/pagead/js/'
           'adsbygoogle.js?client=ca-pub-6236025065305645"\n     '
           'crossorigin="anonymous"></script>')

NAV_HEADER = '''<header>
  <a href="/" class="logo">
    <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
    <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
  </a>
  <nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="mob-nav-links">
      <a href="/">🏠 Ciudades</a>
      <a href="/ranking.html">📊 Ranking</a>
      <a href="/analisis.html">📈 Análisis</a>
      <a href="/comparador.html">⚖️ Comparar</a>
      <a href="/metodologia.html">📊 Metodología</a>
      <a href="/glosario.html">📖 Glosario</a>
      <a href="/guia-inversor.html">🎯 Guía inversor</a>
      <a href="/sobre.html">ℹ️ Sobre</a>
    </div>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/comparador.html">Comparador</a>
    <a href="/metodologia.html">Metodología</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/guia-inversor.html">Guía</a>
    <a href="/sobre.html">Sobre</a>
  </nav>
</header>'''

FOOTER = '''<footer>
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
</footer>'''

CSS_EXTRA = '''<style>
.bc{max-width:880px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}
.bc a{color:var(--muted);text-decoration:none;font-weight:500;transition:color .15s}
.bc a:hover{color:var(--blue);text-decoration:underline}
.bc-sep{color:#cbd5e1}
.bc-cur{color:var(--text);font-weight:600}
.tabla-comparativa{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem;background:var(--white,#fff);border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.tabla-comparativa thead{background:#f1f5f9}
.tabla-comparativa th{padding:.7rem .85rem;text-align:left;font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;color:var(--text2,#475569);font-weight:700;border-bottom:1px solid var(--border,#e2e8f0)}
.tabla-comparativa td{padding:.65rem .85rem;border-bottom:1px solid var(--border,#e2e8f0);color:var(--text2,#475569)}
.tabla-comparativa td strong{color:var(--text,#0e1828)}
.tabla-comparativa tr:hover td{background:#f8fafc}
.tabla-comparativa .num{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.kpi-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.85rem;margin:1.25rem 0}
.kpi-card{background:var(--white,#fff);border:1px solid var(--border,#e2e8f0);border-radius:12px;padding:1rem 1.1rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.kpi-val{font-size:1.6rem;font-weight:800;letter-spacing:-.03em;color:var(--blue,#1a56db);line-height:1;margin-bottom:.3rem}
.kpi-lbl{font-size:.74rem;color:var(--muted,#64748b);font-weight:600;line-height:1.35}
.callout{background:#eff6ff;border-left:3px solid var(--blue,#1a56db);border-radius:8px;padding:.95rem 1.15rem;margin:1.2rem 0;font-size:.88rem;line-height:1.65}
.callout strong{color:#1a56db}
.callout.warn{background:#fffbeb;border-color:#d97706}
.callout.warn strong{color:#92400e}
.callout.ok{background:#ecfdf5;border-color:var(--green,#059669)}
.callout.ok strong{color:#065f46}
</style>'''


def article_head(title: str, desc: str, slug: str,
                 published: str = "2026-05-19",
                 article_json: dict | None = None) -> str:
    canonical = f"https://rendata.es/{slug}.html"
    json_ld = (article_json or {})
    keywords = json_ld.get("keywords", [])
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
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "datePublished": "{published}",
  "dateModified": "{published}",
  "author": {{"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"}},
  "publisher": {{
    "@type": "Organization",
    "name": "Ren Data",
    "url": "https://rendata.es/",
    "logo": {{"@type": "ImageObject", "url": "https://rendata.es/favicon.svg"}}
  }},
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "{canonical}"}},
  "inLanguage": "es-ES",
  "keywords": {keywords}
}}</script>
<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
{CSS_EXTRA}
<link rel="stylesheet" href="/css/nav.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){{dataLayer.push(arguments);}}gtag('js', new Date());gtag('config', 'G-0M57323B51');</script>
{ADSENSE}
</head>
<body>
'''


def article_hero(eyebrow: str, h1: str, lead: str, published_h: str) -> str:
    return f'''<section class="art-hero">
  <div class="art-hero-inner">
    <div class="art-eyebrow"><span class="live-dot"></span>{eyebrow}</div>
    <h1>{h1}</h1>
    <div class="art-meta">
      <span>📅 {published_h}</span>
      <span>📊 Fuente: INE · Ministerio de Vivienda · Banco de España</span>
      <span>🔄 Actualizado mensualmente</span>
    </div>
    <p class="art-lead">{lead}</p>
  </div>
</section>'''


def breadcrumb(curr: str) -> str:
    return f'''<nav class="bc" aria-label="Breadcrumb">
  <a href="/">Inicio</a>
  <span class="bc-sep">›</span>
  <a href="analisis.html">Análisis</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">{curr}</span>
</nav>'''


def wrap(head: str, hero: str, bc: str, body: str) -> str:
    return f'''{head}
{NAV_HEADER}

{bc}

{hero}

<article class="art">
{body}
</article>

{FOOTER}

</body>
</html>
'''


# ===================== ARTÍCULOS =========================================

# --- 1. comprar-piso-primera-vez-espana-2026.html ----------------------------
ART1_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#preparar">1. Preparación previa: ahorro y financiación</a></li>
      <li><a href="#zona">2. Elección de zona y tipo de inmueble</a></li>
      <li><a href="#dd">3. Due diligence del inmueble</a></li>
      <li><a href="#arras">4. Reserva y contrato de arras</a></li>
      <li><a href="#hipoteca">5. Hipoteca: comparar y aprobar</a></li>
      <li><a href="#notaria">6. Firma ante notario y registro</a></li>
      <li><a href="#postcompra">7. Después de la firma</a></li>
      <li><a href="#errores">Errores típicos del comprador novato</a></li>
    </ul>
  </div>

  <h2 id="preparar">1. Preparación previa: ahorro y financiación</h2>
  <p>Antes de visitar la primera casa, necesitas <strong>ahorro líquido equivalente al 28-30% del precio</strong> del inmueble: 20% de entrada que el banco no te financiará + 8-10% de gastos de compra (ITP/IVA, notaría, registro, gestoría). Para una vivienda de 200.000€, esto son 56-60.000€.</p>
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-val">20%</div><div class="kpi-lbl">Entrada mínima<br>(banco financia 80%)</div></div>
    <div class="kpi-card"><div class="kpi-val">8-10%</div><div class="kpi-lbl">Gastos de compra<br>(ITP + notaría + registro)</div></div>
    <div class="kpi-card"><div class="kpi-val">35%</div><div class="kpi-lbl">Esfuerzo máximo<br>(% renta a hipoteca)</div></div>
    <div class="kpi-card"><div class="kpi-val">25-30</div><div class="kpi-lbl">Años hipoteca<br>(estándar)</div></div>
  </div>
  <div class="callout"><strong>Aval ICO al rescate:</strong> si eres menor de 35 años o familia con menores, el <a href="aval-ico-primera-vivienda-2026.html">Aval ICO del 20%</a> te permite comprar con solo los gastos en mano (no necesitas la entrada). Programa vigente hasta 2027.</div>

  <h2 id="zona">2. Elección de zona y tipo de inmueble</h2>
  <p>Tres preguntas clave antes de comprar tu primera vivienda:</p>
  <ul>
    <li><strong>¿Cuánto tiempo voy a vivir aquí?</strong> Si la respuesta es &lt;5 años, los gastos de compra (~8%) tardan más en amortizarse que el coste de alquilar. Si son &gt;7 años, comprar suele ser más eficiente.</li>
    <li><strong>¿Voy a tener hijos en este horizonte?</strong> Si sí, prioriza colegios, parques y conexión transporte sobre m² adicionales en zona prime.</li>
    <li><strong>¿Necesito flexibilidad geográfica?</strong> Si tu empleo puede mudarte a otra ciudad en 3-5 años, alquilar es más prudente.</li>
  </ul>
  <p>Para comparar zonas concretas usa el <a href="comparador.html">comparador de ciudades</a> de Ren Data o consulta nuestra <a href="ciudades-baratas-comprar-piso-espana-2026.html">lista de ciudades más baratas para comprar</a>.</p>

  <h2 id="dd">3. Due diligence del inmueble</h2>
  <p>Antes de firmar arras, verifica siempre:</p>
  <ul>
    <li><strong>Nota simple registral</strong> (~9€): confirma titularidad, cargas, hipotecas y embargos.</li>
    <li><strong>Certificado de eficiencia energética</strong>: obligatorio para vender. Letra E o peor implica facturas elevadas.</li>
    <li><strong>ITE (Inspección Técnica del Edificio)</strong> si el inmueble tiene &gt;30 años en la mayoría de municipios.</li>
    <li><strong>Cuotas de comunidad y derramas pendientes</strong>: pídelos por escrito al presidente o administrador.</li>
    <li><strong>Cédula de habitabilidad</strong> y licencia de primera ocupación.</li>
  </ul>

  <h2 id="arras">4. Reserva y contrato de arras</h2>
  <p>Las arras son la señal que asegura la operación mientras tramitas hipoteca. <strong>Cuantía típica: 5-10% del precio</strong>.</p>
  <ul>
    <li><strong>Arras penitenciales</strong> (las más comunes): si el comprador se echa atrás pierde las arras; si es el vendedor, devuelve el doble. Regulado en el art. 1454 del Código Civil.</li>
    <li><strong>Arras confirmatorias</strong>: refuerzan el compromiso sin establecer indemnización específica.</li>
  </ul>
  <p>Pacta un <strong>plazo razonable para la firma</strong> (6-8 semanas para tramitar hipoteca, 3-4 si compras al contado). Si el banco no aprueba la hipoteca por causas ajenas a ti, la cláusula de condición suspensiva te permite recuperar las arras.</p>

  <h2 id="hipoteca">5. Hipoteca: comparar y aprobar</h2>
  <p>Pide oferta a al menos <strong>3 bancos</strong>. Compara <strong>TAE</strong> (no solo tipo nominal): incluye comisiones, productos vinculados y diferencial sobre Euríbor en variables.</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Tipo</th><th>Ventajas</th><th>Cuándo elegirla</th></tr></thead>
    <tbody>
      <tr><td><strong>Fija</strong></td><td>Cuota constante toda la vida del préstamo. Sin sorpresas si suben los tipos.</td><td>Horizonte largo &gt;15 años. Aversión al riesgo.</td></tr>
      <tr><td><strong>Variable</strong></td><td>Cuota inicial más baja. Aprovecha bajadas de tipo.</td><td>Horizonte corto &lt;10 años o expectativa de amortización anticipada.</td></tr>
      <tr><td><strong>Mixta</strong></td><td>Fijo 3-5 años + variable después. Equilibrio.</td><td>Quieres certidumbre los primeros años pero esperas bajadas de Euríbor a futuro.</td></tr>
    </tbody>
  </table>
  <p>Para una comparativa actualizada con datos del Banco de España, ver <a href="hipoteca-fija-vs-variable-2026.html">Hipoteca fija vs variable en 2026</a>.</p>

  <h2 id="notaria">6. Firma ante notario y registro</h2>
  <p>El día de la firma, en la notaría, se otorga la escritura pública y el banco entrega el dinero al vendedor (o cancela la hipoteca anterior si la había). Tú firmas la nueva hipoteca y recibes las llaves.</p>
  <p>Después se liquidan los impuestos (ITP o IVA+AJD) y se inscribe en el Registro de la Propiedad. La gestoría suele encargarse de estos trámites (~400-700€).</p>

  <h2 id="postcompra">7. Después de la firma</h2>
  <ul>
    <li>Cambia los suministros (luz, agua, gas) a tu nombre — primer mes.</li>
    <li>Comunica el cambio al Ayuntamiento (IBI) y a la comunidad de propietarios.</li>
    <li>Contrata un seguro de hogar (obligatorio para la hipoteca).</li>
    <li>Guarda copia digital de todas las escrituras y facturas de la compra.</li>
  </ul>

  <h2 id="errores">Errores típicos del comprador novato</h2>
  <ul>
    <li><strong>Calcular solo el precio de venta y olvidar los gastos.</strong> El 8-10% adicional sorprende a muchos.</li>
    <li><strong>Visitar solo de día.</strong> El ruido, tráfico y luz cambian radicalmente por la tarde-noche.</li>
    <li><strong>Pedir hipoteca a un único banco.</strong> Las diferencias entre TAE pueden suponer miles de euros a 25 años.</li>
    <li><strong>No reservar dinero para reformas.</strong> Sumar 5-10% del precio en presupuesto adicional es prudente.</li>
    <li><strong>Comprar emocionalmente en mercado caliente.</strong> Si los pisos se venden en &lt;20 días, presión para decidir en una visita única — peligroso.</li>
  </ul>

  <div class="callout ok"><strong>Calcula tu caso:</strong> usa la <a href="comparador.html">calculadora de Ren Data</a> o entra en la ficha de tu ciudad objetivo (ej. <a href="rentabilidad-madrid.html">Madrid</a>, <a href="rentabilidad-valencia.html">Valencia</a>, <a href="rentabilidad-sevilla.html">Sevilla</a>) para ver años de sueldo, esfuerzo mensual y price-to-rent local.</div>
'''

# --- 2. aval-ico-primera-vivienda-2026.html ----------------------------------
ART2_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#que-es">1. Qué es el Aval ICO 20%</a></li>
      <li><a href="#requisitos">2. Requisitos completos</a></li>
      <li><a href="#limites">3. Límites de precio por zona</a></li>
      <li><a href="#bancos">4. Bancos adheridos</a></li>
      <li><a href="#pasos">5. Pasos para solicitarlo</a></li>
      <li><a href="#ciudades">6. Ciudades donde aprovecha más</a></li>
      <li><a href="#faq">FAQ</a></li>
    </ul>
  </div>

  <h2 id="que-es">1. Qué es el Aval ICO 20% primera vivienda</h2>
  <p>Es un <strong>aval del Instituto de Crédito Oficial</strong> que cubre el 20% del valor de tasación de la vivienda — el 20% que tradicionalmente el comprador tenía que aportar de entrada. En la práctica permite financiar hasta el 100% de la vivienda, dejándote solo con los gastos de compra (8-10%) a aportar.</p>
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-val">20%</div><div class="kpi-lbl">Aval estándar<br>(o 25% con menores)</div></div>
    <div class="kpi-card"><div class="kpi-val">35</div><div class="kpi-lbl">Edad máxima<br>(sin hijos a cargo)</div></div>
    <div class="kpi-card"><div class="kpi-val">4,5x</div><div class="kpi-lbl">IPREM máximo<br>(unidad familiar)</div></div>
    <div class="kpi-card"><div class="kpi-val">2027</div><div class="kpi-lbl">Vigente hasta<br>(Plan Estatal 2022-2025 + prórroga)</div></div>
  </div>

  <h2 id="requisitos">2. Requisitos completos</h2>
  <ul>
    <li><strong>Edad</strong>: menor de 35 años a la solicitud, <strong>o</strong> familia con menores a cargo (sin límite de edad si hay menores).</li>
    <li><strong>Residencia fiscal en España</strong> los últimos 2 años.</li>
    <li><strong>Primera vivienda en propiedad</strong> en España. No haber sido propietario completo de otra antes.</li>
    <li><strong>Vivienda habitual</strong>: residencia efectiva mínimo 4 años (si vendes antes, debes devolver el beneficio del aval).</li>
    <li><strong>Ingresos máximos</strong>: 4,5 veces el IPREM (Indicador Público de Renta de Efectos Múltiples) anual. En 2026 esto equivale a ~37.800€ individual / ~50.400€ unidad familiar.</li>
    <li><strong>Patrimonio</strong>: no superar 100.000€ de patrimonio neto (excluyendo la propia vivienda a comprar).</li>
    <li><strong>No tener morosidad</strong> en ASNEF/RAI ni con la AEAT/Seguridad Social.</li>
  </ul>

  <h2 id="limites">3. Límites de precio máximo por zona</h2>
  <p>El precio máximo de la vivienda elegible varía por <strong>zona ICO</strong>:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Zona</th><th>Ejemplos de municipios</th><th>Precio máx. vivienda</th></tr></thead>
    <tbody>
      <tr><td>Zona A</td><td>Madrid capital, Barcelona, Bilbao, San Sebastián, Palma</td><td class="num">250.000€</td></tr>
      <tr><td>Zona B</td><td>Capitales de provincia, áreas metropolitanas grandes</td><td class="num">225.000€</td></tr>
      <tr><td>Zona C</td><td>Resto de municipios &gt;5.000 hab.</td><td class="num">200.000€</td></tr>
      <tr><td>Zona D</td><td>Municipios pequeños y rurales</td><td class="num">175.000€</td></tr>
    </tbody>
  </table>
  <div class="callout warn"><strong>Atención:</strong> los límites se actualizan periódicamente. Verifica el importe vigente en la página oficial del Ministerio de Vivienda y del ICO antes de solicitar. Para Madrid y Barcelona, hay propuestas de elevar el techo a 300.000€ en 2026.</div>

  <h2 id="bancos">4. Bancos adheridos al Aval ICO</h2>
  <p>El convenio ICO-Banca incluye a la mayoría de entidades españolas. Los más activos en aprobaciones:</p>
  <ul>
    <li>CaixaBank · Santander · BBVA · Banco Sabadell · Bankinter · Unicaja</li>
    <li>Abanca · ING · Kutxabank · Ibercaja · Cajamar · Laboral Kutxa</li>
    <li>EVO Banco · Openbank · Triodos Bank (con condiciones)</li>
  </ul>
  <p>El aval es complementario a la hipoteca — primero te aprueban la hipoteca y luego se solicita el aval ICO, que se anexa al préstamo.</p>

  <h2 id="pasos">5. Pasos para solicitarlo</h2>
  <ol style="margin-left:1.5rem">
    <li>Comprueba que cumples los <strong>requisitos personales</strong> (edad, renta, patrimonio).</li>
    <li>Identifica una <strong>vivienda dentro del límite</strong> de precio de su zona ICO.</li>
    <li>Acude al <strong>banco adherido</strong> de tu preferencia y solicita una hipoteca <strong>indicando que quieres incluir el aval ICO</strong>.</li>
    <li>El banco te pide documentación (declaración renta, vida laboral, certificado deudas) y tramita la hipoteca + el aval simultáneamente.</li>
    <li>Si se aprueba, firmas <strong>simultáneamente</strong> en la notaría: escritura + hipoteca + cláusula de aval ICO.</li>
    <li>El aval queda <strong>congelado durante 4 años</strong>. Si vendes antes de ese plazo, devuelves el beneficio.</li>
  </ol>

  <h2 id="ciudades">6. Ciudades donde el Aval ICO marca más diferencia</h2>
  <p>El Aval ICO es más útil donde el precio del piso está cerca del límite de su zona (te permite saltar la barrera de la entrada) y donde el ticket es manejable para el banco. Para inversores en alquiler, el aval no aplica — es solo para vivienda habitual primera.</p>
  <p>Ciudades donde el límite de 200-250.000€ encaja con el precio típico:</p>
  <ul>
    <li><strong>Zona A (250k):</strong> <a href="rentabilidad-madrid.html">Madrid</a> (solo periferia), <a href="rentabilidad-barcelona.html">Barcelona</a> (solo periferia), <a href="rentabilidad-bilbao.html">Bilbao</a> (parcial).</li>
    <li><strong>Zona B (225k):</strong> <a href="rentabilidad-valencia.html">Valencia</a>, <a href="rentabilidad-sevilla.html">Sevilla</a>, <a href="rentabilidad-malaga.html">Málaga</a>, <a href="rentabilidad-zaragoza.html">Zaragoza</a>, <a href="rentabilidad-alicante.html">Alicante</a>.</li>
    <li><strong>Zona C (200k):</strong> <a href="rentabilidad-murcia.html">Murcia</a>, <a href="rentabilidad-valladolid.html">Valladolid</a>, <a href="rentabilidad-vigo.html">Vigo</a>, <a href="rentabilidad-cordoba.html">Córdoba</a>, <a href="rentabilidad-granada.html">Granada</a>.</li>
    <li><strong>Zona D (175k):</strong> mayoría de capitales de provincia pequeñas y municipios rurales.</li>
  </ul>

  <h2 id="faq">Preguntas frecuentes</h2>
  <h3>¿Puedo combinar Aval ICO con la ayuda autonómica de mi CCAA?</h3>
  <p>Sí, son compatibles. El Aval ICO cubre el 20% de la entrada; la ayuda autonómica (ej. Plan Mi Primera Vivienda Madrid) puede sumar otro 15-20% adicional o cubrir gastos.</p>
  <h3>¿Tengo que devolver el aval si vendo el piso?</h3>
  <p>Solo si vendes en los primeros 4 años. Pasado ese plazo, el aval se libera y no hay devolución.</p>
  <h3>¿Funciona para vivienda nueva u obra?</h3>
  <p>Sí, pero la vivienda debe estar terminada en el momento de la firma. Si compras sobre plano, el aval se aplica al cierre, no en las entregas a cuenta.</p>
'''

# --- 3. hipoteca-fija-vs-variable-2026.html ----------------------------------
ART3_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#contexto">1. Contexto 2026: dónde están los tipos</a></li>
      <li><a href="#fija">2. Hipoteca fija — pros, contras, tipos actuales</a></li>
      <li><a href="#variable">3. Hipoteca variable — riesgos del Euríbor</a></li>
      <li><a href="#mixta">4. Hipoteca mixta — el equilibrio</a></li>
      <li><a href="#comparativa">5. Comparativa numérica</a></li>
      <li><a href="#cuando">6. Cuándo elegir cada una</a></li>
    </ul>
  </div>

  <h2 id="contexto">1. Contexto 2026: dónde están los tipos de interés</h2>
  <p>Tras el ciclo de subidas del BCE 2022-2024 y el inicio de bajadas en 2025, los tipos de referencia se han estabilizado en niveles moderados. A mediados de 2026, los rangos típicos en hipotecas a particulares son:</p>
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-val">~3,0%</div><div class="kpi-lbl">Hipoteca fija<br>(TAE media a 25-30 años)</div></div>
    <div class="kpi-card"><div class="kpi-val">~2,3%</div><div class="kpi-lbl">Euríbor 12m<br>(referencia variable)</div></div>
    <div class="kpi-card"><div class="kpi-val">~2,7%</div><div class="kpi-lbl">Hipoteca variable<br>(Euríbor + 0,4-0,7)</div></div>
    <div class="kpi-card"><div class="kpi-val">~3,2%</div><div class="kpi-lbl">BCE tipo depósito<br>(referencia política)</div></div>
  </div>
  <div class="callout"><strong>Fuente:</strong> Banco de España — Estadísticas de tipos de interés efectivos en operaciones nuevas a particulares. Valores indicativos; cada operación se negocia individualmente.</div>

  <h2 id="fija">2. Hipoteca fija</h2>
  <p>El tipo de interés se mantiene <strong>constante toda la vida del préstamo</strong>. La cuota mensual no cambia salvo por amortización anticipada.</p>
  <p><strong>Ventajas:</strong> certidumbre absoluta sobre cuánto pagarás cada mes durante 25-30 años. Protección frente a subidas del Euríbor. Más sencilla de presupuestar.</p>
  <p><strong>Desventajas:</strong> en 2026 el tipo fijo está ~0,7-1 punto por encima del variable. Si los tipos bajan más, no te beneficias. Penalizaciones por amortización anticipada suelen ser mayores (hasta 2% el primer año).</p>

  <h2 id="variable">3. Hipoteca variable</h2>
  <p>Tipo de interés = <strong>Euríbor + diferencial</strong> (típicamente 0,4-0,9 puntos). Se revisa cada 6-12 meses según el contrato.</p>
  <p><strong>Ventajas:</strong> cuota inicial más baja. Aprovecha automáticamente cualquier bajada del Euríbor. Comisiones de amortización menores (0,15-0,25%).</p>
  <p><strong>Desventajas:</strong> sometida al ciclo monetario. En 2022-2024 vimos cómo el Euríbor pasó de -0,5% a +4%, doblando la cuota de muchos titulares. Riesgo no asegurable.</p>

  <h2 id="mixta">4. Hipoteca mixta</h2>
  <p>Combina ambos: <strong>tipo fijo los primeros 3-10 años</strong>, luego pasa a variable (Euríbor + diferencial). Es la opción de crecimiento más rápido en 2025-2026 entre los nuevos préstamos.</p>
  <p><strong>Ventajas:</strong> certidumbre los primeros años (cuando el saldo pendiente es máximo), pero te beneficias de futuras bajadas del Euríbor a partir del año 5-10.</p>
  <p><strong>Desventajas:</strong> el tipo fijo inicial suele ser ligeramente más alto que el fijo puro. Y si el Euríbor sube cuando llega la fase variable, pagas más.</p>

  <h2 id="comparativa">5. Comparativa numérica — vivienda de 200.000€</h2>
  <p>Hipoteca de 160.000€ (80% LTV) a 25 años (300 meses). Cuotas mensuales aproximadas según tipo de interés:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Modalidad</th><th>Tipo inicial</th><th>Cuota mensual</th><th>Coste total 25 años</th><th>Intereses</th></tr></thead>
    <tbody>
      <tr><td><strong>Fija 3,0%</strong></td><td class="num">3,00%</td><td class="num">759€</td><td class="num">227.700€</td><td class="num">67.700€</td></tr>
      <tr><td><strong>Mixta 5+20</strong></td><td class="num">2,75% / 2,80% est.</td><td class="num">~735€</td><td class="num">~220.500€</td><td class="num">~60.500€</td></tr>
      <tr><td><strong>Variable</strong></td><td class="num">2,70% inicial</td><td class="num">733€ inicial</td><td class="num">depende del Euríbor</td><td class="num">variable</td></tr>
    </tbody>
  </table>
  <div class="callout warn"><strong>Cuidado con los escenarios:</strong> la cuota inicial de variable es atractiva, pero si el Euríbor sube 1 punto, la cuota sube ~80€/mes. Si sube 3 puntos (como en 2022-2023), sube ~260€/mes.</div>

  <h2 id="cuando">6. Cuándo elegir cada una</h2>
  <p><strong>Elige fija si:</strong> aversión alta al riesgo, presupuesto familiar ajustado (esfuerzo &gt;30% de la renta), plazo largo &gt;20 años, expectativa de subidas del Euríbor.</p>
  <p><strong>Elige variable si:</strong> tienes capacidad de ahorro para absorber subidas, plazo corto &lt;15 años, esperas amortización anticipada importante, expectativa de tipos a la baja sostenida.</p>
  <p><strong>Elige mixta si:</strong> quieres certidumbre en la fase inicial (cuando el capital es máximo y los intereses pesan más) pero prevés flexibilidad después.</p>

  <div class="callout ok"><strong>Calcula tu caso:</strong> usa la <a href="comparador.html">calculadora de hipoteca</a> en cualquier ficha de ciudad (ej. <a href="rentabilidad-madrid.html">Madrid</a> o <a href="rentabilidad-valencia.html">Valencia</a>) para ver cuota mensual, intereses totales y tabla de amortización por año.</div>
'''

# --- 4. gastos-comprar-piso-por-comunidad-2026.html --------------------------
ART4_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#segunda-mano">Vivienda de segunda mano (ITP)</a></li>
      <li><a href="#nueva">Vivienda nueva (IVA + AJD)</a></li>
      <li><a href="#otros">Notaría · Registro · Gestoría · Tasación</a></li>
      <li><a href="#total">Tabla total por CCAA</a></li>
      <li><a href="#bonificaciones">Bonificaciones autonómicas</a></li>
    </ul>
  </div>

  <h2 id="segunda-mano">ITP — Impuesto de Transmisiones Patrimoniales (vivienda de segunda mano)</h2>
  <p>Lo paga el comprador a la Hacienda autonómica. Varía del 4% (País Vasco vivienda habitual) al 11% (Cataluña tramos altos). Es el gasto más relevante en la compra y la principal causa de que el coste varíe tanto entre CCAA.</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Comunidad Autónoma</th><th>ITP general</th><th>Bonificaciones</th></tr></thead>
    <tbody>
      <tr><td>País Vasco</td><td class="num">4%</td><td>Para vivienda habitual; régimen foral</td></tr>
      <tr><td>Navarra</td><td class="num">6%</td><td>Régimen foral</td></tr>
      <tr><td>C. de Madrid</td><td class="num">6%</td><td>Bonificaciones para familias numerosas</td></tr>
      <tr><td>Canarias</td><td class="num">6,5%</td><td>Plus bonificaciones jóvenes &lt;35</td></tr>
      <tr><td>La Rioja</td><td class="num">7%</td><td>Bonificación zona rural</td></tr>
      <tr><td>Andalucía</td><td class="num">7%</td><td>3,5% para jóvenes &lt;35 en vivienda &lt;130k</td></tr>
      <tr><td>Aragón</td><td class="num">8%</td><td>5% jóvenes y familia numerosa</td></tr>
      <tr><td>Asturias</td><td class="num">8%</td><td>4% jóvenes y discapacidad</td></tr>
      <tr><td>Castilla y León</td><td class="num">8%</td><td>4% jóvenes &lt;36 zonas rurales</td></tr>
      <tr><td>Islas Baleares</td><td class="num">8-11,5%</td><td>Escalonado por valor (más alto en lujo)</td></tr>
      <tr><td>R. de Murcia</td><td class="num">8%</td><td>3% jóvenes y familia numerosa</td></tr>
      <tr><td>Castilla-La Mancha</td><td class="num">9%</td><td>6% vivienda habitual jóvenes</td></tr>
      <tr><td>Cantabria</td><td class="num">9%</td><td>5% jóvenes y discapacidad zona rural</td></tr>
      <tr><td>Galicia</td><td class="num">9%</td><td>8% vivienda habitual jóvenes &lt;36</td></tr>
      <tr><td>Extremadura</td><td class="num">8-11%</td><td>Escalonado · bonificación jóvenes y discapacitados</td></tr>
      <tr><td>Cataluña</td><td class="num">10-11%</td><td>10% &lt;1M€, 11% &gt;1M€. 5% jóvenes &lt;32</td></tr>
      <tr><td>C. Valenciana</td><td class="num">10%</td><td>8% jóvenes y familia numerosa</td></tr>
    </tbody>
  </table>

  <h2 id="nueva">IVA + AJD — Vivienda nueva</h2>
  <p>La vivienda nueva no paga ITP. Paga <strong>IVA al 10% en toda España</strong> (4% en VPO de régimen especial) + <strong>Actos Jurídicos Documentados</strong> (AJD) que sí varía por CCAA:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>CCAA</th><th>AJD general</th><th>Bonificación jóvenes/VH</th></tr></thead>
    <tbody>
      <tr><td>C. de Madrid</td><td class="num">0,75%</td><td>0,4% familia numerosa</td></tr>
      <tr><td>La Rioja</td><td class="num">1%</td><td>0,5% rural</td></tr>
      <tr><td>Navarra</td><td class="num">0,5%</td><td>Régimen foral</td></tr>
      <tr><td>País Vasco</td><td class="num">0,5%</td><td>Régimen foral</td></tr>
      <tr><td>Andalucía</td><td class="num">1,2%</td><td>0,3% familia numerosa</td></tr>
      <tr><td>Asturias</td><td class="num">1,2%</td><td>0,3% jóvenes &lt;35</td></tr>
      <tr><td>Canarias</td><td class="num">0,75%</td><td>0,4% jóvenes</td></tr>
      <tr><td>Resto CCAA</td><td class="num">1,5%</td><td>Variable (0,1-0,75% con bonificaciones)</td></tr>
    </tbody>
  </table>

  <h2 id="otros">Notaría · Registro · Gestoría · Tasación</h2>
  <p>Costes adicionales relativamente uniformes en toda España. Varían ligeramente según el precio del inmueble:</p>
  <ul>
    <li><strong>Notaría</strong>: 0,3-0,5% del precio (tarifa regulada). Para piso de 200.000€: ~600-1.000€.</li>
    <li><strong>Registro de la Propiedad</strong>: 0,2-0,3% del precio. Para 200.000€: ~400-600€.</li>
    <li><strong>Gestoría</strong> (opcional, recomendable): 300-600€ fijos.</li>
    <li><strong>Tasación bancaria</strong> para hipoteca: 250-400€.</li>
    <li><strong>Nota simple registral</strong>: 9€ (paga el comprador antes de las arras).</li>
  </ul>

  <h2 id="total">Tabla total — vivienda 2ª mano de 200.000€</h2>
  <table class="tabla-comparativa">
    <thead><tr><th>CCAA</th><th>ITP</th><th>Otros gastos</th><th>Total estimado</th><th>% sobre precio</th></tr></thead>
    <tbody>
      <tr><td>País Vasco (4%)</td><td class="num">8.000€</td><td class="num">~2.300€</td><td class="num"><strong>10.300€</strong></td><td class="num">5,2%</td></tr>
      <tr><td>Madrid / Navarra (6%)</td><td class="num">12.000€</td><td class="num">~2.300€</td><td class="num"><strong>14.300€</strong></td><td class="num">7,2%</td></tr>
      <tr><td>Andalucía / La Rioja (7%)</td><td class="num">14.000€</td><td class="num">~2.300€</td><td class="num"><strong>16.300€</strong></td><td class="num">8,2%</td></tr>
      <tr><td>Aragón / Asturias / CyL / Murcia (8%)</td><td class="num">16.000€</td><td class="num">~2.300€</td><td class="num"><strong>18.300€</strong></td><td class="num">9,2%</td></tr>
      <tr><td>Cantabria / CLM / Galicia (9%)</td><td class="num">18.000€</td><td class="num">~2.300€</td><td class="num"><strong>20.300€</strong></td><td class="num">10,2%</td></tr>
      <tr><td>Cataluña / C. Valenciana (10%)</td><td class="num">20.000€</td><td class="num">~2.300€</td><td class="num"><strong>22.300€</strong></td><td class="num">11,2%</td></tr>
    </tbody>
  </table>
  <div class="callout"><strong>Diferencia clave:</strong> comprar la misma vivienda en Madrid (6% ITP) cuesta <strong>12.000€ menos</strong> en impuestos que en Cataluña o C. Valenciana (10%). Una variable a tener muy presente al comparar ciudades fronterizas.</div>

  <h2 id="bonificaciones">Bonificaciones autonómicas: cuándo aplican</h2>
  <p>La mayoría de CCAA reducen el ITP/AJD para perfiles específicos:</p>
  <ul>
    <li><strong>Menores de 35 años</strong> (algunos límites a 32, 36, 40): aplican reducciones de 1-4 puntos en ITP.</li>
    <li><strong>Familia numerosa</strong>: típicamente reducción similar a jóvenes.</li>
    <li><strong>Discapacidad ≥33%</strong>: bonificación adicional, a veces acumulable con joven.</li>
    <li><strong>Vivienda en municipios pequeños</strong> (despoblación): muchas CCAA premian la compra en zonas rurales.</li>
    <li><strong>Vivienda protegida (VPO)</strong>: tipos reducidos casi siempre.</li>
  </ul>
  <p>Para datos por ciudad concreta, consulta la sección "Ayudas para comprar en {CCAA}" en cada ficha (<a href="rentabilidad-madrid.html">ej. Madrid</a>, <a href="rentabilidad-valencia.html">Valencia</a>, <a href="rentabilidad-sevilla.html">Sevilla</a>).</p>
'''

# --- 5. cuanto-ahorrar-comprar-piso-espana-2026.html -------------------------
ART5_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#regla">La regla del 28-30%</a></li>
      <li><a href="#desglose">Desglose del ahorro necesario</a></li>
      <li><a href="#ciudades">Ahorro por ciudad (top 20)</a></li>
      <li><a href="#aval">Reducción con Aval ICO</a></li>
      <li><a href="#plazo">Cuánto tiempo tardarás en ahorrarlo</a></li>
    </ul>
  </div>

  <h2 id="regla">La regla del 28-30% del precio</h2>
  <p>Para comprar una vivienda en España necesitas, salvo Aval ICO, <strong>tener ahorrado el 28-30% del precio</strong>: el 20% de entrada (el banco financia el 80%) más el 8-10% de gastos de compra (ITP/IVA, notaría, registro, gestoría, tasación).</p>
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-val">20%</div><div class="kpi-lbl">Entrada<br>(LTV 80%)</div></div>
    <div class="kpi-card"><div class="kpi-val">~8%</div><div class="kpi-lbl">Gastos<br>(ITP+notaría+registro)</div></div>
    <div class="kpi-card"><div class="kpi-val">~28%</div><div class="kpi-lbl">Ahorro total<br>necesario</div></div>
    <div class="kpi-card"><div class="kpi-val">~3-5%</div><div class="kpi-lbl">Reserva<br>obras+imprevistos</div></div>
  </div>

  <h2 id="desglose">Desglose del ahorro necesario</h2>
  <p>Tomemos como ejemplo una vivienda de 200.000€:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Concepto</th><th>%</th><th>Importe sobre 200.000€</th></tr></thead>
    <tbody>
      <tr><td>Entrada al banco (LTV 80%)</td><td class="num">20,0%</td><td class="num"><strong>40.000€</strong></td></tr>
      <tr><td>ITP (medio nacional, 8%)</td><td class="num">8,0%</td><td class="num">16.000€</td></tr>
      <tr><td>Notaría</td><td class="num">0,4%</td><td class="num">800€</td></tr>
      <tr><td>Registro de la propiedad</td><td class="num">0,3%</td><td class="num">600€</td></tr>
      <tr><td>Gestoría</td><td class="num">0,2%</td><td class="num">~400€</td></tr>
      <tr><td>Tasación bancaria</td><td class="num">0,15%</td><td class="num">~300€</td></tr>
      <tr><td><strong>TOTAL ahorro mínimo</strong></td><td class="num"><strong>29,1%</strong></td><td class="num"><strong>~58.100€</strong></td></tr>
      <tr><td>+ Reserva imprevistos (recomendado)</td><td class="num">5%</td><td class="num">10.000€</td></tr>
      <tr><td><strong>AHORRO IDEAL CON COLCHÓN</strong></td><td class="num"><strong>34%</strong></td><td class="num"><strong>~68.000€</strong></td></tr>
    </tbody>
  </table>

  <h2 id="ciudades">Ahorro necesario por ciudad — top 20 más buscadas</h2>
  <p>Estimaciones para piso típico (~80m²) en cada ciudad usando ITP local. Datos Q2 2026 de Ren Data:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Ciudad</th><th>Precio piso típico</th><th>Entrada 20%</th><th>Gastos ~8%</th><th>Ahorro total</th></tr></thead>
    <tbody>
      <tr><td>Madrid</td><td class="num">476.800€</td><td class="num">95.360€</td><td class="num">38.144€</td><td class="num"><strong>133.504€</strong></td></tr>
      <tr><td>Barcelona</td><td class="num">392.000€</td><td class="num">78.400€</td><td class="num">39.200€</td><td class="num"><strong>117.600€</strong></td></tr>
      <tr><td>San Sebastián</td><td class="num">416.000€</td><td class="num">83.200€</td><td class="num">16.640€</td><td class="num"><strong>99.840€</strong></td></tr>
      <tr><td>Bilbao</td><td class="num">252.000€</td><td class="num">50.400€</td><td class="num">10.080€</td><td class="num"><strong>60.480€</strong></td></tr>
      <tr><td>Palma</td><td class="num">336.000€</td><td class="num">67.200€</td><td class="num">26.880€</td><td class="num"><strong>94.080€</strong></td></tr>
      <tr><td>Málaga</td><td class="num">254.400€</td><td class="num">50.880€</td><td class="num">17.808€</td><td class="num"><strong>68.688€</strong></td></tr>
      <tr><td>Valencia</td><td class="num">216.000€</td><td class="num">43.200€</td><td class="num">21.600€</td><td class="num"><strong>64.800€</strong></td></tr>
      <tr><td>Sevilla</td><td class="num">196.000€</td><td class="num">39.200€</td><td class="num">13.720€</td><td class="num"><strong>52.920€</strong></td></tr>
      <tr><td>Alicante</td><td class="num">180.000€</td><td class="num">36.000€</td><td class="num">18.000€</td><td class="num"><strong>54.000€</strong></td></tr>
      <tr><td>Zaragoza</td><td class="num">156.000€</td><td class="num">31.200€</td><td class="num">12.480€</td><td class="num"><strong>43.680€</strong></td></tr>
      <tr><td>Granada</td><td class="num">158.400€</td><td class="num">31.680€</td><td class="num">11.088€</td><td class="num"><strong>42.768€</strong></td></tr>
      <tr><td>Vitoria</td><td class="num">216.000€</td><td class="num">43.200€</td><td class="num">8.640€</td><td class="num"><strong>51.840€</strong></td></tr>
      <tr><td>Pamplona</td><td class="num">236.000€</td><td class="num">47.200€</td><td class="num">14.160€</td><td class="num"><strong>61.360€</strong></td></tr>
      <tr><td>Murcia</td><td class="num">140.000€</td><td class="num">28.000€</td><td class="num">11.200€</td><td class="num"><strong>39.200€</strong></td></tr>
      <tr><td>Valladolid</td><td class="num">128.000€</td><td class="num">25.600€</td><td class="num">10.240€</td><td class="num"><strong>35.840€</strong></td></tr>
      <tr><td>Lleida</td><td class="num">104.000€</td><td class="num">20.800€</td><td class="num">10.400€</td><td class="num"><strong>31.200€</strong></td></tr>
      <tr><td>Teruel</td><td class="num">65.600€</td><td class="num">13.120€</td><td class="num">5.248€</td><td class="num"><strong>18.368€</strong></td></tr>
      <tr><td>Soria</td><td class="num">67.200€</td><td class="num">13.440€</td><td class="num">5.376€</td><td class="num"><strong>18.816€</strong></td></tr>
      <tr><td>Villena</td><td class="num">58.400€</td><td class="num">11.680€</td><td class="num">5.840€</td><td class="num"><strong>17.520€</strong></td></tr>
      <tr><td>Mieres</td><td class="num">60.000€</td><td class="num">12.000€</td><td class="num">4.800€</td><td class="num"><strong>16.800€</strong></td></tr>
    </tbody>
  </table>
  <div class="callout"><strong>De 17.000€ a 133.000€:</strong> el ahorro necesario varía 8x según ciudad. Comprar en Villena, Mieres o Soria requiere ~18.000€; en Madrid o Barcelona, &gt;115.000€. Para cifras por tu ciudad concreta, ve a la <a href="/">página principal</a> y abre su ficha.</div>

  <h2 id="aval">Aval ICO 20%: reduce el ahorro necesario al 8%</h2>
  <p>Con el <a href="aval-ico-primera-vivienda-2026.html">Aval ICO</a> (vigente hasta 2027), si eres menor de 35 o tienes hijos a cargo, no necesitas el 20% de entrada — solo los gastos (~8%). Eso significa:</p>
  <ul>
    <li>Madrid: de 133.504€ → <strong>~38.144€</strong> con aval.</li>
    <li>Valencia: de 64.800€ → <strong>~21.600€</strong> con aval.</li>
    <li>Sevilla: de 52.920€ → <strong>~13.720€</strong> con aval.</li>
    <li>Teruel: de 18.368€ → <strong>~5.248€</strong> con aval.</li>
  </ul>

  <h2 id="plazo">Cuánto tiempo tardarás en ahorrarlo</h2>
  <p>Con un salario neto medio español de ~22.000€ y un ahorro mensual razonable de 300-500€/mes (15-25% del neto), los plazos típicos:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>Ahorro mensual</th><th>20.000€ (Mieres)</th><th>50.000€ (Sevilla)</th><th>100.000€ (Bilbao)</th><th>130.000€ (Madrid)</th></tr></thead>
    <tbody>
      <tr><td>300€/mes</td><td class="num">5,5 años</td><td class="num">14 años</td><td class="num">28 años</td><td class="num">36 años</td></tr>
      <tr><td>500€/mes</td><td class="num">3,3 años</td><td class="num">8,3 años</td><td class="num">17 años</td><td class="num">21 años</td></tr>
      <tr><td>800€/mes</td><td class="num">2,1 años</td><td class="num">5,2 años</td><td class="num">10,4 años</td><td class="num">13,5 años</td></tr>
      <tr><td>1.200€/mes</td><td class="num">1,4 años</td><td class="num">3,5 años</td><td class="num">7 años</td><td class="num">9 años</td></tr>
    </tbody>
  </table>
'''

# --- 6. barrios-baratos-madrid-barcelona-2026.html ---------------------------
ART6_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#madrid">Madrid — 5 barrios accesibles</a></li>
      <li><a href="#barcelona">Barcelona — 5 barrios accesibles</a></li>
      <li><a href="#periferia">Periferia metropolitana con tickets bajos</a></li>
      <li><a href="#perfil">Qué tipo de comprador encaja</a></li>
    </ul>
  </div>

  <h2 id="madrid">Madrid — 5 barrios accesibles para comprador</h2>
  <p>Madrid capital tiene un precio medio de 5.960€/m² (Q1 2026), pero la dispersión por distrito es enorme. Estas son las zonas más accesibles para primera vivienda, con tickets dentro del límite Aval ICO (≤250.000€) para un piso de 70m²:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>#</th><th>Distrito / Barrio</th><th>Precio m²</th><th>Piso 70m²</th><th>Perfil</th></tr></thead>
    <tbody>
      <tr><td>1</td><td><strong>Vallecas (Puente y Villa)</strong></td><td class="num">2.900€</td><td class="num">203.000€</td><td>Residencial popular, en transformación</td></tr>
      <tr><td>2</td><td><strong>Carabanchel</strong></td><td class="num">3.300€</td><td class="num">231.000€</td><td>Familiar, conexión metro y bus</td></tr>
      <tr><td>3</td><td><strong>Usera</strong></td><td class="num">3.500€</td><td class="num">245.000€</td><td>Multicultural, joven, en alza</td></tr>
      <tr><td>4</td><td><strong>Villaverde</strong></td><td class="num">2.700€</td><td class="num">189.000€</td><td>Periférico sur, mercado consolidado</td></tr>
      <tr><td>5</td><td><strong>San Blas-Canillejas</strong></td><td class="num">3.400€</td><td class="num">238.000€</td><td>Este, conexión Metropolitano y aeropuerto</td></tr>
    </tbody>
  </table>
  <p>Los cinco distritos están dentro del límite Aval ICO Zona A (250k). Vallecas y Usera son los más dinámicos en revalorización de la última década (+45% acumulado).</p>

  <h2 id="barcelona">Barcelona — 5 barrios accesibles para comprador</h2>
  <p>Barcelona capital tiene precio medio de 4.900€/m². Como en Madrid, los barrios periféricos ofrecen tickets entrada accesibles, aunque algunos de los más baratos quedan ya fuera del límite Aval ICO Zona A si el inmueble supera los 65-70m²:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>#</th><th>Distrito / Barrio</th><th>Precio m²</th><th>Piso 60m²</th><th>Perfil</th></tr></thead>
    <tbody>
      <tr><td>1</td><td><strong>Nou Barris</strong></td><td class="num">2.600€</td><td class="num">156.000€</td><td>Norte, residencial popular, metro L1/L4</td></tr>
      <tr><td>2</td><td><strong>Sant Andreu</strong></td><td class="num">3.000€</td><td class="num">180.000€</td><td>Familiar, identidad de barrio, AVE</td></tr>
      <tr><td>3</td><td><strong>Horta-Guinardó</strong></td><td class="num">3.200€</td><td class="num">192.000€</td><td>Verde, residencial, parque Güell</td></tr>
      <tr><td>4</td><td><strong>Sant Martí (norte)</strong></td><td class="num">3.500€</td><td class="num">210.000€</td><td>El Clot, La Verneda, en transformación</td></tr>
      <tr><td>5</td><td><strong>Sants (zona periférica)</strong></td><td class="num">3.700€</td><td class="num">222.000€</td><td>Hostafrancs, La Bordeta, conexión estación</td></tr>
    </tbody>
  </table>

  <h2 id="periferia">Periferia metropolitana con tickets bajos</h2>
  <p>Si el barrio capital encarece la operación, las primeras coronas metropolitanas ofrecen pisos competitivos con buena conexión:</p>
  <ul>
    <li><strong>Madrid metropolitano (sur):</strong> <a href="rentabilidad-fuenlabrada.html">Fuenlabrada</a> (1.900€/m²), <a href="rentabilidad-getafe.html">Getafe</a> (2.400€/m²), <a href="rentabilidad-leganes.html">Leganés</a> (2.200€/m²), <a href="rentabilidad-mostoles.html">Móstoles</a> (2.100€/m²).</li>
    <li><strong>Barcelona metropolitano:</strong> <a href="rentabilidad-l-hospitalet-de-llobregat.html">L'Hospitalet</a> (3.400€/m²), <a href="rentabilidad-badalona.html">Badalona</a> (2.600€/m²), <a href="rentabilidad-cornell-de-llobregat.html">Cornellà</a> (2.800€/m²), <a href="rentabilidad-sabadell.html">Sabadell</a> (1.800€/m²) y <a href="rentabilidad-terrassa.html">Terrassa</a> (1.750€/m²).</li>
  </ul>

  <h2 id="perfil">Qué tipo de comprador encaja en cada zona</h2>
  <p><strong>Vallecas, Usera, Nou Barris</strong>: comprador joven o familia con ingresos medios que prioriza precio sobre ubicación prime. Conexión metro/cercanías buena pero distancia al centro 20-30 min.</p>
  <p><strong>Carabanchel, Horta-Guinardó, Sant Andreu</strong>: comprador familiar de clase media que busca identidad de barrio, parques, colegios. Mercado más consolidado.</p>
  <p><strong>Periferia metropolitana</strong> (Fuenlabrada, L'Hospitalet, Sabadell): comprador que prioriza espacio (3 hab, terraza, garaje) sobre proximidad a centro. Trayecto laboral diario en cercanías o coche.</p>

  <div class="callout"><strong>Para comparar dos barrios o ciudades concretas</strong> usa el <a href="comparador.html">comparador de Ren Data</a> con sus métricas de comprador (años de sueldo, esfuerzo mensual, price-to-rent).</div>
'''

# --- 7. cuando-es-buen-momento-comprar-piso-2026.html ------------------------
ART7_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#indicadores">Los 6 indicadores clave</a></li>
      <li><a href="#mercado">Estado del mercado 2026</a></li>
      <li><a href="#personal">El factor personal pesa más</a></li>
      <li><a href="#regla">La regla de los 5-7 años</a></li>
      <li><a href="#ahora">Conclusión: ¿comprar ahora?</a></li>
    </ul>
  </div>

  <h2 id="indicadores">Los 6 indicadores clave del mercado</h2>
  <ol style="margin-left:1.5rem">
    <li><strong>Subida anual del precio del m²</strong>: si supera la inflación + 3 puntos, el mercado está caliente.</li>
    <li><strong>Días de venta media</strong>: &lt;20 días = mercado del vendedor, &gt;45 días = mercado del comprador.</li>
    <li><strong>Variación de la oferta disponible</strong>: caídas continuadas señalan escasez sostenida.</li>
    <li><strong>Esfuerzo financiero medio</strong>: % de la renta neta dedicado a la cuota. &gt;40% = burbuja, &lt;30% = sostenible.</li>
    <li><strong>Ratio precio/salario</strong>: años de sueldo bruto para comprar piso. Histórico España: ~7,5; &gt;10 = tensión.</li>
    <li><strong>Tipos de interés (Euríbor + diferencial)</strong>: tipos bajos abaratan financiación; tipos altos enfrían el mercado.</li>
  </ol>

  <h2 id="mercado">Estado del mercado español Q2 2026</h2>
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-val">+6,6%</div><div class="kpi-lbl">Subida media m²<br>(anual nacional)</div></div>
    <div class="kpi-card"><div class="kpi-val">~24</div><div class="kpi-lbl">Días medios<br>de venta nacional</div></div>
    <div class="kpi-card"><div class="kpi-val">~37%</div><div class="kpi-lbl">Esfuerzo medio<br>(% renta familiar)</div></div>
    <div class="kpi-card"><div class="kpi-val">~7,5</div><div class="kpi-lbl">Años de salario<br>para comprar 100m²</div></div>
  </div>
  <p>El mercado español muestra señales mixtas:</p>
  <ul>
    <li><strong>Caliente en grandes capitales y costas</strong>: Madrid, Barcelona, Bilbao, Málaga, Palma, Valencia tienen subidas &gt;7-12% anuales, esfuerzo &gt;40% y &lt;20 días de venta.</li>
    <li><strong>Equilibrado o frío en interior y norte</strong>: muchas capitales medias (Salamanca, León, Valladolid, Oviedo) tienen subidas moderadas (3-5%), esfuerzo razonable y stock saneado.</li>
    <li><strong>Aceleración en municipios &lt;20.000 hab.</strong> tras la pandemia: ahorro acumulado + teletrabajo elevan demanda en interior.</li>
  </ul>

  <h2 id="personal">El factor personal pesa más que el ciclo</h2>
  <p>Aunque los indicadores macro importen, para tu caso concreto pesan más:</p>
  <ul>
    <li><strong>Horizonte de permanencia</strong>: si vas a vivir en la casa &gt;7 años, el ciclo importa poco.</li>
    <li><strong>Estabilidad laboral y familiar</strong>: una hipoteca es un compromiso a 25-30 años — no se cancela fácilmente.</li>
    <li><strong>Tu ahorro disponible</strong>: si tienes el 30% del precio + colchón, esperar no es necesariamente mejor.</li>
    <li><strong>El coste de oportunidad de alquilar</strong>: si pagas 1.000€ alquiler cuando comprar te costaría 900€ de cuota, esperas 5 años "perdiendo" 60.000€ acumulados.</li>
  </ul>

  <h2 id="regla">La regla práctica de los 5-7 años</h2>
  <p>Si tu horizonte de permanencia en la vivienda es <strong>menor a 5 años</strong>, los gastos de compra (~8% del precio) no se amortizan y comprar es financieramente subóptimo frente a alquilar. Si es <strong>mayor a 7 años</strong>, comprar suele ganar incluso en mercados caros. Entre 5 y 7 años, depende del esfuerzo financiero y del coste alternativo del alquiler local.</p>

  <h2 id="ahora">Conclusión: ¿es buen momento para comprar?</h2>
  <p>No hay una respuesta nacional única. Depende de la ciudad concreta y de tu perfil. Para un análisis específico de tu ciudad objetivo, abre su ficha en Ren Data y revisa la sección "¿Puedo permitirme comprar en X?" — cruza años de sueldo, esfuerzo mensual y price-to-rent local para darte un veredicto contextual.</p>
  <p>Ejemplos: <a href="rentabilidad-madrid.html">Madrid</a> · <a href="rentabilidad-barcelona.html">Barcelona</a> · <a href="rentabilidad-valencia.html">Valencia</a> · <a href="rentabilidad-sevilla.html">Sevilla</a> · <a href="rentabilidad-zaragoza.html">Zaragoza</a> · <a href="rentabilidad-malaga.html">Málaga</a> · <a href="rentabilidad-bilbao.html">Bilbao</a> · <a href="rentabilidad-vigo.html">Vigo</a>.</p>
'''

# --- 8. comprar-piso-joven-espana-2026.html ----------------------------------
ART8_BODY = '''
  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#contexto">El reto del joven comprador 2026</a></li>
      <li><a href="#aval">Aval ICO 20% (estatal)</a></li>
      <li><a href="#ccaa">Ayudas autonómicas joven por CCAA</a></li>
      <li><a href="#hipoteca">Hipoteca joven: cómo conseguirla</a></li>
      <li><a href="#estrategias">Estrategias de comprador joven</a></li>
      <li><a href="#donde">Dónde comprar siendo joven con presupuesto ajustado</a></li>
    </ul>
  </div>

  <h2 id="contexto">El reto del joven comprador en 2026</h2>
  <p>Comprar primera vivienda como menor de 35 en España requiere cumplir tres condiciones simultáneamente: <strong>ingresos estables suficientes</strong> para hipoteca, <strong>ahorro acumulado</strong> para entrada y gastos, y <strong>edad &lt;35</strong> para aprovechar las ayudas. Datos del INE 2024: la edad media de emancipación en España es 30,3 años, y solo el 21% de los menores de 30 tiene vivienda en propiedad.</p>

  <h2 id="aval">Aval ICO 20% — la ayuda más potente</h2>
  <p>Programa estatal vigente hasta 2027 que <strong>permite financiar el 100% de la vivienda</strong> sin aportar entrada — solo necesitas los gastos (~8%).</p>
  <ul>
    <li><strong>Edad</strong>: &lt;35 años (o sin límite si tienes hijos a cargo).</li>
    <li><strong>Renta máxima</strong>: 4,5x IPREM anual (~37.800€ individual / ~50.400€ unidad familiar).</li>
    <li><strong>Patrimonio máximo</strong>: 100.000€ (excluyendo la vivienda a comprar).</li>
    <li><strong>Vivienda</strong>: primera, habitual, hasta 250.000€ (Zona A: grandes ciudades) o menos en zonas B-D.</li>
  </ul>
  <p>Análisis completo en <a href="aval-ico-primera-vivienda-2026.html">Aval ICO 20% primera vivienda 2026</a>.</p>

  <h2 id="ccaa">Ayudas autonómicas para jóvenes por CCAA</h2>
  <p>La mayoría de comunidades tienen programas propios para menores de 35-36, frecuentemente acumulables con el Aval ICO:</p>
  <table class="tabla-comparativa">
    <thead><tr><th>CCAA</th><th>Programa principal</th><th>Beneficio típico</th></tr></thead>
    <tbody>
      <tr><td>Madrid</td><td>Mi Primera Vivienda</td><td>Aval autonómico hasta 15% adicional al ICO. Total hasta 35%.</td></tr>
      <tr><td>Cataluña</td><td>Bonificación AJD jóvenes &lt;32</td><td>AJD reducido al 0,5% en vivienda nueva.</td></tr>
      <tr><td>País Vasco</td><td>Deducción IRPF 18%</td><td>Hasta 1.530€/año en cuota IRPF compra vivienda habitual.</td></tr>
      <tr><td>Navarra</td><td>Deducción foral 15%</td><td>Hasta 1.200€/año en IRPF foral por compra.</td></tr>
      <tr><td>Galicia</td><td>Ayuda compra rural &lt;36</td><td>Hasta 10.800€ a la compra en municipios &lt;10.000 hab.</td></tr>
      <tr><td>Castilla y León</td><td>Deducción IRPF 15%</td><td>Hasta 9.000€ acumulados en jóvenes &lt;36 zonas rurales.</td></tr>
      <tr><td>Castilla-La Mancha</td><td>Subvención &lt;36</td><td>Hasta 10.800€ directos para primera vivienda en municipios pequeños.</td></tr>
      <tr><td>Andalucía</td><td>Reducción ITP jóvenes &lt;35</td><td>ITP del 3,5% (vs 7% general) en vivienda &lt;130.000€.</td></tr>
      <tr><td>Murcia</td><td>Deducción IRPF 5%</td><td>Hasta 300€/año por primera vivienda.</td></tr>
      <tr><td>Otras CCAA</td><td>Variable</td><td>Consulta con tu CCAA — bono alquiler joven estatal vigente en todas.</td></tr>
    </tbody>
  </table>
  <p>Para datos por tu CCAA concreta, abre la ficha de tu ciudad y consulta el bloque "Ayudas para comprar en {CCAA}".</p>

  <h2 id="hipoteca">Hipoteca joven: cómo conseguirla</h2>
  <p>Aunque no existe una "hipoteca joven" como producto estándar, los bancos competen por captar clientes jóvenes con condiciones específicas:</p>
  <ul>
    <li><strong>Plazos más largos</strong>: hasta 35-40 años (vs 25-30 estándar).</li>
    <li><strong>LTV alto + Aval ICO</strong>: financiación 100% combinando con el aval estatal.</li>
    <li><strong>Diferenciales mejores</strong> en variable (Euríbor + 0,4-0,6 si tienes nómina domiciliada).</li>
    <li><strong>Carencias iniciales</strong> opcionales (solo pagas intereses los primeros 1-2 años, útil si esperas mejora salarial).</li>
  </ul>
  <p>Bancos más activos en hipoteca joven 2026: CaixaBank, Santander, BBVA, Sabadell, EVO Banco, Openbank, ING.</p>

  <h2 id="estrategias">Estrategias del comprador joven en 2026</h2>
  <ol style="margin-left:1.5rem">
    <li><strong>Compra colaborativa</strong>: hermanos, pareja sin contrato matrimonial o amigos firmando en proindiviso. Suma rentas y multiplica capacidad.</li>
    <li><strong>Compra de obra nueva en plano</strong>: pagas entregas a cuenta durante la construcción (24 meses típicos), te da tiempo a ahorrar.</li>
    <li><strong>Comprar en municipio pequeño con teletrabajo</strong>: tickets bajos (60-90k€), ayudas extra a despoblación, y trabajo remoto compensa la distancia.</li>
    <li><strong>Comprar la casa familiar a tus padres</strong>: si tienen una vivienda libre, comprársela con tasación de mercado evita la búsqueda y aprovechas vínculos familiares para condiciones.</li>
    <li><strong>VPO (Vivienda de Protección Oficial)</strong>: lista de espera larga pero precios &lt;50% del mercado libre y ITP reducido.</li>
  </ol>

  <h2 id="donde">Dónde comprar siendo joven con presupuesto ajustado</h2>
  <p>Las 10 ciudades más asequibles para joven comprador (precio piso 70m² &lt;100.000€):</p>
  <ul>
    <li><a href="rentabilidad-villena.html">Villena</a> (51k€), <a href="rentabilidad-puertollano.html">Puertollano</a> (53k€), <a href="rentabilidad-mieres.html">Mieres</a> (53k€)</li>
    <li><a href="rentabilidad-linares.html">Linares</a> (55k€), <a href="rentabilidad-ferrol.html">Ferrol</a> (56k€), <a href="rentabilidad-langreo.html">Langreo</a> (57k€)</li>
    <li><a href="rentabilidad-teruel.html">Teruel</a> (57k€), <a href="rentabilidad-soria.html">Soria</a> (59k€), <a href="rentabilidad-ecija.html">Écija</a> (60k€)</li>
    <li><a href="rentabilidad-jaen.html">Jaén</a> (69k€), <a href="rentabilidad-zamora.html">Zamora</a> (67k€), <a href="rentabilidad-ourense.html">Ourense</a> (76k€)</li>
  </ul>
  <p>Para una lista completa ordenada por precio, ver <a href="ciudades-baratas-comprar-piso-espana-2026.html">Las 10 ciudades más baratas para comprar piso</a>.</p>

  <div class="callout ok"><strong>Calcula cuánto necesitas:</strong> usa el <a href="cuanto-ahorrar-comprar-piso-espana-2026.html">artículo de ahorro necesario</a> y la calculadora de hipoteca de cualquier ficha de ciudad.</div>
'''


# ===================== Definicion de articulos ==========================

ARTICLES = [
    {
        "slug": "comprar-piso-primera-vez-espana-2026",
        "title": "Comprar piso por primera vez en España 2026 — Guía paso a paso",
        "desc": "Guía completa para comprar tu primera vivienda en España: ahorro necesario, hipoteca, arras, notaría, gastos y errores típicos. Datos Q2 2026.",
        "eyebrow": "Guía completa · Datos Q2 2026",
        "h1": "Comprar piso por <span class=\"ac\">primera vez</span> en España (2026)",
        "lead": "Si nunca has comprado vivienda, esta guía cubre el proceso completo: cuánto ahorrar antes de empezar, cómo elegir zona, due diligence del inmueble, contrato de arras, comparación de hipotecas, firma ante notario y errores típicos de comprador novato. Pensada para España, datos Q2 2026.",
        "body": ART1_BODY,
        "breadcrumb": "Comprar piso por primera vez 2026",
        "keywords": ["comprar piso primera vez", "primera vivienda España", "guía comprador 2026", "proceso de compra vivienda"],
    },
    {
        "slug": "aval-ico-primera-vivienda-2026",
        "title": "Aval ICO 20% primera vivienda 2026 — Requisitos y bancos",
        "desc": "Cómo funciona el Aval ICO del 20% para primera vivienda en 2026: requisitos, límites de precio por zona, bancos adheridos y pasos para solicitarlo.",
        "eyebrow": "Análisis · Plan Estatal de Vivienda · Q2 2026",
        "h1": "<span class=\"ac\">Aval ICO 20%</span> para primera vivienda en 2026",
        "lead": "El Aval ICO del 20% permite comprar primera vivienda sin aportar entrada propia, financiando hasta el 100% del precio. Programa estatal vigente hasta 2027. Esta guía explica requisitos completos, límites de precio por zona, lista de bancos adheridos, pasos para solicitarlo y ciudades donde encaja mejor.",
        "body": ART2_BODY,
        "breadcrumb": "Aval ICO 20% primera vivienda",
        "keywords": ["aval ICO 20%", "primera vivienda 2026", "ayudas compra joven", "100% financiación"],
    },
    {
        "slug": "hipoteca-fija-vs-variable-2026",
        "title": "Hipoteca fija vs variable 2026 — Cuál elegir y cuándo",
        "desc": "Comparativa actualizada de hipoteca fija, variable y mixta en 2026 con datos del Banco de España. Cuándo elegir cada modalidad según tu perfil y plazo.",
        "eyebrow": "Análisis · Banco de España · Q2 2026",
        "h1": "Hipoteca <span class=\"ac\">fija vs variable</span> en 2026",
        "lead": "Tras el ciclo de subidas del BCE 2022-2024 y el inicio de bajadas en 2025, las hipotecas en 2026 ofrecen un escenario intermedio. Tipo fijo ~3,0%, variable Euríbor+0,5 ~2,7%, mixta entre ambos. Esta comparativa con datos del Banco de España analiza las tres modalidades, simula la cuota mensual y el coste total para una vivienda de 200.000€, y orienta cuándo elegir cada una.",
        "body": ART3_BODY,
        "breadcrumb": "Hipoteca fija vs variable 2026",
        "keywords": ["hipoteca fija", "hipoteca variable", "hipoteca mixta", "Euríbor 2026", "Banco de España hipoteca"],
    },
    {
        "slug": "gastos-comprar-piso-por-comunidad-2026",
        "title": "Gastos comprar piso por comunidad autónoma 2026 — Tabla completa",
        "desc": "Tabla completa de gastos para comprar piso por CCAA en 2026: ITP, IVA, AJD, notaría, registro y bonificaciones autonómicas para jóvenes y familias.",
        "eyebrow": "Análisis · Ministerio de Hacienda · Q2 2026",
        "h1": "Gastos de comprar piso <span class=\"ac\">por CCAA</span> (2026)",
        "lead": "Comprar una vivienda en España genera gastos del 8-12% sobre el precio según la comunidad autónoma. El ITP/IVA es el factor decisivo: del 4% en País Vasco al 10-11% en Cataluña. Tabla completa con bonificaciones para jóvenes, familias numerosas y discapacidad. Datos actualizados Q2 2026.",
        "body": ART4_BODY,
        "breadcrumb": "Gastos comprar piso por CCAA 2026",
        "keywords": ["ITP por comunidad", "AJD vivienda nueva", "gastos comprar piso", "notaría registro"],
    },
    {
        "slug": "cuanto-ahorrar-comprar-piso-espana-2026",
        "title": "Cuánto ahorrar para comprar piso en España 2026 — Por ciudad",
        "desc": "Cálculo de ahorro necesario para comprar piso en 20 ciudades de España. Entrada 20% + gastos 8%. De 17.000€ en Villena a 133.000€ en Madrid.",
        "eyebrow": "Calculadora · Datos Q2 2026",
        "h1": "Cuánto <span class=\"ac\">ahorrar</span> para comprar piso (España 2026)",
        "lead": "El ahorro necesario para comprar primera vivienda en España depende mucho de la ciudad: desde 17.000€ en Villena hasta 133.000€ en Madrid. Esta calculadora muestra el desglose entrada+gastos para 20 ciudades, ajuste con el Aval ICO 20% y plazos típicos de ahorro según renta. Datos Q2 2026.",
        "body": ART5_BODY,
        "breadcrumb": "Cuánto ahorrar comprar piso 2026",
        "keywords": ["ahorro comprar piso", "entrada hipoteca 20%", "gastos compra vivienda", "calculadora ahorro"],
    },
    {
        "slug": "barrios-baratos-madrid-barcelona-2026",
        "title": "Barrios baratos en Madrid y Barcelona 2026 — Para comprador",
        "desc": "Los 5 barrios más accesibles para comprar piso en Madrid y Barcelona en 2026. Vallecas, Usera, Nou Barris, Sant Andreu y más. Datos Q2 2026.",
        "eyebrow": "Análisis por distrito · Q2 2026",
        "h1": "Barrios <span class=\"ac\">accesibles</span> en Madrid y Barcelona",
        "lead": "Las dos ciudades más caras de España tienen también la mayor dispersión por barrio. En Madrid: Vallecas, Usera, Carabanchel, Villaverde y San Blas con tickets dentro del límite Aval ICO. En Barcelona: Nou Barris, Sant Andreu, Horta-Guinardó, Sant Martí y Sants periférico. Datos Q2 2026 con perfil de comprador para cada zona.",
        "body": ART6_BODY,
        "breadcrumb": "Barrios baratos Madrid Barcelona 2026",
        "keywords": ["barrios baratos Madrid", "barrios baratos Barcelona", "Vallecas Nou Barris", "comprar piso periferia"],
    },
    {
        "slug": "cuando-es-buen-momento-comprar-piso-2026",
        "title": "¿Cuándo es buen momento para comprar piso? 2026 análisis",
        "desc": "Análisis de los 6 indicadores que determinan si es buen momento para comprar piso en 2026: subidas, días en mercado, esfuerzo, ratio precio/salario y tipos.",
        "eyebrow": "Análisis del ciclo · Q2 2026",
        "h1": "¿Cuándo es <span class=\"ac\">buen momento</span> para comprar piso? (2026)",
        "lead": "No hay un \"buen momento\" universal para comprar piso. Depende del ciclo macro (tipos, oferta, demanda), del mercado local (subidas anuales, días en mercado, esfuerzo) y, sobre todo, de tu situación personal (horizonte, estabilidad, ahorro). Esta guía analiza los 6 indicadores clave con datos Q2 2026 y propone una regla práctica de decisión.",
        "body": ART7_BODY,
        "breadcrumb": "Cuándo comprar piso 2026",
        "keywords": ["buen momento comprar piso", "ciclo inmobiliario 2026", "esfuerzo financiero", "ratio precio salario"],
    },
    {
        "slug": "comprar-piso-joven-espana-2026",
        "title": "Comprar piso siendo joven en España 2026 — Ayudas reales",
        "desc": "Guía para comprar primera vivienda siendo menor de 35 años en España 2026. Aval ICO, ayudas autonómicas por CCAA, hipoteca joven y estrategias.",
        "eyebrow": "Guía joven · Q2 2026",
        "h1": "Comprar piso siendo <span class=\"ac\">joven</span> en España (2026)",
        "lead": "Con la edad media de emancipación en 30,3 años y solo el 21% de menores de 30 con vivienda en propiedad, comprar primera vivienda siendo joven es un reto. Pero hay herramientas: Aval ICO 20% estatal (vigente hasta 2027), deducciones autonómicas IRPF, hipoteca joven y estrategias específicas. Esta guía las cubre todas, con condiciones reales por CCAA.",
        "body": ART8_BODY,
        "breadcrumb": "Comprar piso joven 2026",
        "keywords": ["comprar piso joven", "primera vivienda menor 35", "aval ICO joven", "hipoteca joven España"],
    },
]


# ===================== MAIN ==============================================

def main() -> int:
    count = 0
    for art in ARTICLES:
        head = article_head(art["title"], art["desc"], art["slug"],
                            article_json={"keywords": art["keywords"]})
        hero = article_hero(art["eyebrow"], art["h1"], art["lead"],
                            "Publicado el 19 de mayo de 2026")
        bc = breadcrumb(art["breadcrumb"])
        html = wrap(head, hero, bc, art["body"])
        out = FICHAS_DIR / f'{art["slug"]}.html'
        out.write_text(html, encoding="utf-8")
        size_kb = out.stat().st_size // 1024
        print(f'Created: {art["slug"]}.html  ({size_kb} KB)')
        count += 1
    print(f'TOTAL: {count}/{len(ARTICLES)} articulos generados')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
