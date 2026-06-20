# Informe de Auditoría y Corrección SEO — rendata.es

**Fecha:** 2026-06-20
**Ámbito:** `rendata_beta/` (sitio estático servido por Cloudflare Workers Assets)
**Páginas totales:** 769 HTML (768 indexables + `404.html`)

---

## Resumen ejecutivo

Se ha auditado y corregido la configuración SEO completa del sitio. Los problemas
más relevantes detectados y resueltos han sido:

1. **Canonicals apuntando a URLs con `.html`** (768 páginas) — apuntaban a una URL
   que Cloudflare redirige (307) a la versión limpia, perdiendo señal de canonicalización.
2. **Canonical a dominio externo erróneo** en `glosario.html` (`invertirzona.es`).
3. **Falta de redirección** `https://www.rendata.es → https://rendata.es`.
4. **Sitemap con URLs `.html`** (no canónicas, redirigidas).
5. **`og:url`/`twitter:url` desalineados** con el canonical (747 páginas).

Todo ello queda corregido y desplegable. A continuación el detalle por bloque.

---

## BLOQUE 1 — HTTP/HTTPS y WWW

**Estado previo:** `_redirects` solo cubría `http://rendata.es/*` y `http://www.rendata.es/*`.
Faltaba forzar `https://www.rendata.es → https://rendata.es`.

**Redirecciones implementadas (301):**

| Origen | Destino |
|---|---|
| `http://rendata.es/*` | `https://rendata.es/:splat` |
| `http://www.rendata.es/*` | `https://rendata.es/:splat` |
| `https://www.rendata.es/*` | `https://rendata.es/:splat` *(añadida)* |

Resultado: un único origen canónico `https://rendata.es` (sin `www`, siempre `https`).

---

## BLOQUE 2 — Eliminar duplicidad `.html`

- **Verificado:** no existían reglas que redirigieran `/ciudad` → `/ciudad.html`.
  Cloudflare Workers Assets ya realiza automáticamente `307 /ciudad.html → /ciudad`.
- Los rewrites `200` internos (`/rentabilidad/*` y `/ccaa/*`) se conservan: sirven
  contenido sin redirigir y **no** crean bucle con el `html_handling` de Cloudflare.
  No están enlazados desde ninguna página (no generan contenido duplicado indexable).
- **Añadidas 50 redirecciones 301 explícitas** `.html → URL limpia` para las páginas
  más importantes, convirtiendo el 307 automático (temporal) en 301 (permanente),
  preferible para SEO:
  - 40 ciudades: Madrid, Barcelona, Valencia, Málaga, Sevilla, Zaragoza, Bilbao,
    Alicante, Granada, Murcia, Valladolid, Córdoba, Palma, Vigo, Gijón, A Coruña,
    Santander, San Sebastián, Pamplona, Burgos, Las Palmas GC, Santa Cruz de Tenerife,
    Oviedo, Salamanca, León, Cádiz, Huelva, Jaén, Almería, Logroño, Vitoria, Badajoz,
    Castellón, Tarragona, Lleida, Girona, Toledo, Albacete, Marbella, Móstoles.
  - 10 páginas clave: ranking, analisis, comparador, calculadora-hipoteca,
    simulador-comprar-vs-alquilar, top10-ciudades-rentables-2026,
    informe-rentabilidad-espana-q2-2026, guia-inversor, barrios, metodologia.

---

## BLOQUE 3 — Canonicals

**Auditoría completa de las 769 páginas:**

| Comprobación | Resultado |
|---|---|
| Páginas con exactamente 1 `<link rel="canonical">` | 769 / 769 ✅ |
| Canonicals apuntando a URL sin `.html` | 769 / 769 ✅ |
| Canonicals a dominio `rendata.es` | 769 / 769 ✅ |
| Canonicals a dominio externo | 0 ✅ |

**Correcciones aplicadas:**
- 768 canonicals reescritos de `https://rendata.es/x.html` → `https://rendata.es/x`.
- `glosario.html`: eliminado canonical duplicado y erróneo a `https://invertirzona.es/glosario`;
  conservado el correcto `https://rendata.es/glosario`.
- `index.html` mantiene su canonical raíz `https://rendata.es/`.
- **Adicional:** 747 etiquetas `og:url`/`twitter:url` alineadas con el canonical (sin `.html`).

Cubre todas las familias de páginas: rentabilidad (ciudades), CCAA (`ccaa-*`),
mercado inmobiliario, barrios, vivir-en, herramientas, artículos y páginas generales.

---

## BLOQUE 4 — sitemap.xml

Regenerado desde el canonical de cada página.

| Comprobación | Resultado |
|---|---|
| URLs totales | 768 |
| URLs con `.html` | 0 ✅ |
| URLs no `https://` | 0 ✅ |
| Duplicados | 0 ✅ |
| URLs sin archivo real | 0 ✅ (validado 1:1 contra `rendata_beta/`) |
| `404.html` (noindex) | excluido ✅ |

- `lastmod` original preservado por página.
- `changefreq`/`priority` asignados por tipo (home 1.0, ranking/análisis 0.9,
  ciudades 0.8, CCAA/mercado 0.7, barrios/vivir-en 0.6, legales 0.4).

---

## BLOQUE 5 — Títulos y meta descriptions (20 ciudades)

Reescritos `<title>`, `<meta name="description">`, `og:title`, `og:description`
(y `twitter:*` si existían) en:

Madrid, Barcelona, Valencia, Málaga, Sevilla, Zaragoza, Bilbao, Alicante, Granada,
Murcia, Valladolid, Córdoba, Palma, Vigo, Gijón, A Coruña, Santander, San Sebastián,
Pamplona, Burgos.

- **Título:** `Invertir en {Ciudad} 2026: precio m², alquiler y rentabilidad`
- **Meta:** `Consulta el precio medio por m², alquiler, rentabilidad y evolución del
  mercado inmobiliario en {Ciudad}. Datos actualizados y comparativas.`

---

## BLOQUE 6 — Enlaces internos

Añadida una banda visible **"Ciudades destacadas"** con enlaces (URL limpia) a
Madrid, Barcelona, Valencia, Málaga y Sevilla, justo bajo el hero, en:

- `index.html`
- `ranking.html`
- Las 17 páginas CCAA (`ccaa-*.html`)

Refuerza el enlazado interno hacia las páginas de ciudad de mayor valor.

---

## BLOQUE 7 — Oportunidades SEO detectadas

### Prioridad ALTA
- **Migrar enlaces internos a URL limpia.** Los enlaces internos del sitio aún usan
  `.html` (p. ej. `index.html` tiene ~410 enlaces a `*.html`). Funcionan vía
  redirección, pero cada salto 301/307 diluye señal y añade latencia. Recomendado
  reescribir todos los `href="*.html"` internos a su versión limpia.
- **Datos estructurados (Schema.org).** Añadir `BreadcrumbList` y, en páginas de
  ciudad, `Dataset`/`FAQPage` para enriquecer resultados (rich snippets).

### Prioridad MEDIA
- **`widget-demo.html` indexable.** Página de demostración sin valor de búsqueda;
  conviene `noindex` o excluirla del sitemap (actualmente incluida).
- **Unificar formato de títulos en el resto de ciudades** (>500 páginas) con el
  patrón aplicado a las 20 principales, para coherencia y CTR.
- **Revisar longitud de meta descriptions** en artículos largos (>160 caracteres
  se truncan en SERP).

### Prioridad BAJA
- **`lastmod` del sitemap:** automatizar su actualización en el pipeline de build
  para reflejar cambios reales.
- **Imágenes:** verificar `alt` descriptivos y `width/height` para CLS.
- **Hreflang:** no aplica (sitio monolingüe es-ES), pero declarar `lang="es"`
  de forma consistente.

---

## Validación final

| Métrica | Valor |
|---|---|
| Canonicals correctos | 769 / 769 |
| Canonicals con `.html` | 0 |
| Canonicals a dominio externo | 0 |
| URLs en sitemap | 768 (0 con `.html`, 0 duplicados, 0 inexistentes) |
| Redirecciones de dominio (301) | 3 (http→https, www→no-www) |
| Redirecciones 301 `.html`→limpia | 50 |
| Páginas con título/meta optimizado | 20 |
| Páginas con banda de enlaces internos | 19 |

Estado: **listo para deploy.**
