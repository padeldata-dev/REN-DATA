// Parchea todas las HTML existentes:
//  1) Añade "Vivir en…" al nav móvil y desktop (después de Análisis)
//  2) Añade "Vivir en…" al footer (después de Ranking completo)
//  3) En cada rentabilidad-{slug}.html con un vivir-en-{slug}.html correspondiente,
//     inyecta un CTA enlazando a la guía.
const fs = require('fs');
const path = require('path');
const ROOT = path.join(__dirname,'..','rendata_beta');
const list = require('../data/vivir-list.json');
const vivirSet = new Set(list.map(c=>c.slug));

const files = fs.readdirSync(ROOT).filter(f=>f.endsWith('.html'));
let patchedNav=0, patchedFooter=0, patchedCta=0, errors=[];

for(const f of files){
  if(f.startsWith('vivir-en-')) continue; // ya generadas con el nav nuevo
  const full = path.join(ROOT,f);
  let html = fs.readFileSync(full,'utf8');
  let changed = false;

  // 1) Mobile nav (incluye emoji)
  if(html.includes('>📈 Análisis</a>') && !html.includes('>🏡 Vivir en…</a>')){
    html = html.replace(
      /(<a href="\/analisis\.html">📈 Análisis<\/a>)/,
      '$1\n      <a href="/vivir-en-espana.html">🏡 Vivir en…</a>'
    );
    changed = true; patchedNav++;
  }
  // 2) Desktop nav (sin emoji) — sólo si todavía no se ha añadido
  // Patrón frecuente: <a href="/analisis.html">Análisis</a> seguido de otra <a o un <div
  if(!html.includes('>Vivir en…</a>') && /<a href="\/analisis\.html">Análisis<\/a>/.test(html)){
    html = html.replace(
      /(<a href="\/analisis\.html">Análisis<\/a>)(?!\s*\n\s*<a href="\/vivir-en-espana\.html")/,
      '$1\n    <a href="/vivir-en-espana.html">Vivir en…</a>'
    );
    changed = true;
  }

  // 3) Footer: añade "Vivir en…" tras "Ranking completo"
  if(!html.includes('<a href="vivir-en-espana.html">Vivir en…</a>') && html.includes('<a href="ranking.html">Ranking completo</a>')){
    html = html.replace(
      /(<a href="ranking\.html">Ranking completo<\/a>\s*\n\s*<a href="analisis\.html">Análisis<\/a>)/,
      '$1\n      <a href="vivir-en-espana.html">Vivir en…</a>'
    );
    // fallback si el orden está al revés u otro pequeño desvío
    if(!html.includes('<a href="vivir-en-espana.html">Vivir en…</a>')){
      html = html.replace(
        /(<a href="ranking\.html">Ranking completo<\/a>)/,
        '$1\n      <a href="vivir-en-espana.html">Vivir en…</a>'
      );
    }
    changed = true; patchedFooter++;
  }

  // 4) CTA en fichas rentabilidad
  const m = /^rentabilidad-(.+)\.html$/.exec(f);
  if(m){
    const slug = m[1];
    if(vivirSet.has(slug) && !html.includes(`href="vivir-en-${slug}.html"`)){
      // Insertar tarjeta justo después del breadcrumb principal (.bc), antes de la sección zonas / sticky-bar
      const cta = `
<aside class="vivir-cta-card" style="max-width:1200px;margin:1rem auto 0;padding:0 1.5rem">
  <a href="vivir-en-${slug}.html" style="display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:1.1rem 1.35rem;border-radius:12px;text-decoration:none;gap:1rem;flex-wrap:wrap;box-shadow:0 4px 16px rgba(14,42,107,.15)">
    <div>
      <div style="font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#93c5fd;margin-bottom:.25rem">Guía residencial</div>
      <div style="font-size:1.02rem;font-weight:700;letter-spacing:-.02em">🏡 ¿Te planteas vivir aquí? Lee la guía completa</div>
      <div style="font-size:.83rem;color:rgba(255,255,255,.82);margin-top:.25rem">Barrios reales, transporte, empleo, sanidad, educación y pros/contras</div>
    </div>
    <div style="background:rgba(255,255,255,.18);padding:.55rem 1.05rem;border-radius:8px;font-size:.85rem;font-weight:700;white-space:nowrap">Ver guía →</div>
  </a>
</aside>
`;
      // Intentar insertar después de cierre de </header> (o tras div.bc / nav.bc)
      let inserted = false;
      const reBcDiv = /(<div class="bc">[\s\S]*?<\/div>)/;
      const reBcNav = /(<nav class="bc"[\s\S]*?<\/nav>)/;
      if(reBcDiv.test(html)){
        html = html.replace(reBcDiv, '$1\n'+cta);
        inserted = true;
      } else if(reBcNav.test(html)){
        html = html.replace(reBcNav, '$1\n'+cta);
        inserted = true;
      } else {
        html = html.replace('</header>','</header>\n'+cta);
        inserted = true;
      }
      if(inserted){ patchedCta++; changed = true; }
    }
  }

  if(changed){
    fs.writeFileSync(full, html, 'utf8');
  }
}

console.log('nav patched:', patchedNav);
console.log('footer patched:', patchedFooter);
console.log('rentabilidad CTAs:', patchedCta);
if(errors.length){ console.log('ERRORS:', errors); }
