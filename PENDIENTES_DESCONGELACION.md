# Pendientes de descongelación (campaña de prensa Málaga)

Cambios **propuestos** sobre ficheros CONGELADOS que NO se han aplicado por estar
en el set congelado (`frozen_files.json`). Aplicar cuando se descongele cada uno.

Ficheros congelados: `ranking.html`, `mercado-inmobiliario-provincia-malaga-2026.html`
y las 28 fichas `rentabilidad-<municipio-de-Málaga>.html`.

---

<!-- Los bloques de esta tarea añaden entradas debajo. Formato:
## <fichero>
- [bloque N] descripción del cambio propuesto y motivo
-->

## Los 30 ficheros congelados (ranking.html, artículo Málaga y 28 fichas)
- [bloque 1] Añadir en el footer el enlace "Sala de prensa" → /prensa.html
  (se aplicó a las 762 páginas NO congeladas; falta en estas 30).
- [bloque 4] Versionar sus `<link>`/`<script>` propios con `?v=20260724`
  (se aplicó a las 762 NO congeladas; estas 30 siguen enlazando /css/*.css y
  /js/*.js sin query, por lo que un cambio futuro de esos CSS/JS tardará hasta
  30 días en llegar a visitantes recurrentes). Aplicar al descongelar.
- [bloque 4] Revisión SEO opcional: las 28 fichas y el artículo comparten el
  patrón de `<title>` keyword-rich >60 caracteres y algunas `meta description`
  >160. No es un error (indexan completo), pero si se decide recortar títulos
  para mejorar el CTR en SERP, hacerlo al descongelar y de forma homogénea.

## enlazado interno / SEO — sin pendientes de contenido
- [bloque 3] Ninguna página congelada quedó huérfana ni con módulo de
  "ciudades relacionadas" débil (<3 enlaces). Nada que corregir.
- [bloque 4] JSON-LD válido, H1 único y `alt` presente también en las
  congeladas. Nada que corregir.
