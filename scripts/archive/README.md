# Archive

Scripts de un solo uso ya ejecutados: auditorías puntuales de bloques SEO,
generación/integración de lotes concretos de fichas (41/100/110 ciudades),
descargas de fotos, migraciones de fuentes/superficie/nav ya aplicadas,
inserciones de contenido editorial por lote, etc. Se conservan como
referencia histórica de qué se hizo y cómo, no para volver a ejecutarse.

**Nota:** varios de estos scripts calculan `ROOT` como
`Path(__file__).resolve().parent.parent`, asumiendo que viven en
`scripts/` (un nivel bajo la raíz del repo). Al estar ahora en
`scripts/archive/` (dos niveles bajo la raíz), esa ruta ya no apunta a
la raíz del proyecto. Si necesitas reejecutar alguno, ajusta `ROOT` o
cópialo temporalmente a `scripts/`.

## Qué sigue vigente en `scripts/` (no archivado)

- `check_internal_links.py` — valida sitemap.xml contra los ficheros reales.
- `regenerate_sitemap.py` — regenera sitemap.xml completo desde el estado actual de `rendata_beta/`.
- `differentiate_clones.py` — detecta y diferencia ciudades con precio+alquiler+ROI clonados.
- `compute_hero_stats.py` — recalcula agregados de DATA[] para contrastar con el hero/trust-bar.
- `generate_widget.py` — regenera `widget.js` / `widget-data.json` / `widget-demo.html`.
- `update_nav.py` — migración masiva de navegación (bloque `<nav>` canónico, inyecta nav.css/nav-dropdown.js).
