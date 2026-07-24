# Ren Data — [rendata.es](https://rendata.es)

Sitio estático de análisis de rentabilidad inmobiliaria por ciudad en España
(597 ciudades). El sitio vive en `rendata_beta/` y se despliega en Cloudflare
Workers (assets estáticos). El dataset se actualiza con el pipeline (`pipeline/`).

## Estructura

| Ruta | Qué es |
|------|--------|
| `rendata_beta/` | El sitio (HTML/CSS/JS/fuentes). Es lo único que se despliega. |
| `pipeline/` | Pipeline trimestral de datos (INE, MIVAU, observatorios). Ver `pipeline/README.md`. |
| `scripts/` | Utilidades de build y QA. |
| `drafts/` | Borradores editoriales **no publicados** (fuera del deploy y del sitemap). |
| `frozen_files.json` | Ficheros **congelados** con su SHA256 (ver más abajo). |
| `PENDIENTES_DESCONGELACION.md` | Cambios propuestos sobre ficheros congelados, pendientes de aplicar. |

## Guardián de calidad — `scripts/qa_check.py`

Verificación local en una sola pasada. **Ejecútalo SIEMPRE antes de cada deploy.**

```bash
python scripts/qa_check.py
```

Comprueba, sobre todo `rendata_beta/` (incluidos `academia/` y `en/`):

1. **Enlaces internos rotos** — 0 tolerados.
2. **sitemap.xml** — todas sus URLs resuelven a una página existente.
3. **Slugs únicos** en el `DATA[]` de `index.html`.
4. **canonical / og:url** presentes, absolutos y en el dominio `rendata.es`.
5. **JSON-LD** parseable en todas las páginas.
6. **Ficheros congelados** — SHA256 vs `frozen_files.json`; si un hash cambia, **FALLA**.

Sale con código `0` si todo pasa y `1` si algún check crítico falla (apto para CI
o para bloquear un deploy).

## Ficheros congelados

`frozen_files.json` lista ficheros que **no deben cambiar** (p. ej. durante una
campaña de prensa): `ranking.html`, el artículo de la provincia de Málaga y las
28 fichas de municipios malagueños. Si necesitas cambiar uno, anótalo en
`PENDIENTES_DESCONGELACION.md` en lugar de editarlo. `qa_check.py` falla si el
contenido de cualquiera de ellos cambia.

Para **descongelar** y fijar una nueva línea base tras aplicar cambios aprobados,
regenera los hashes (recalcula el SHA256 de cada fichero de la lista y
sobrescribe `frozen_files.json`).

## Deploy

```bash
python scripts/qa_check.py          # 1. debe pasar en verde
git add -A && git commit -m "..."   # 2. commit (git status de congelados = 0)
git push origin main                # 3. push
npx wrangler@4.87.0 deploy          # 4. deploy a Cloudflare
```

Recuerda: los `/css/*` y `/js/*` se cachean 30 días. Al cambiar un CSS/JS,
actualiza el sufijo `?v=YYYYMMDD` de sus `<link>`/`<script>` para que el cambio
llegue a visitantes recurrentes.
