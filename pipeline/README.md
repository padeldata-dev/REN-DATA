# REN DATA Pipeline

Pipeline de actualización trimestral del dataset de las 329 ciudades de
[rendata.es](https://rendata.es) usando **únicamente fuentes oficiales y
abiertas** (INE, MIVAU, Notariado, Observatorios CCAA).

> **No usa scraping** de Idealista/Fotocasa — sus TOS lo prohíben
> explícitamente y tienen Cloudflare. Para alquileres se cubre lo que
> publican los observatorios públicos; el resto se estima por ratio
> histórico.

## Estructura

```
pipeline/
├── __init__.py
├── __main__.py          # CLI: python -m pipeline {fetch|apply|run|audit}
├── config.py            # Paths, doctrine ROI, user-agent
├── cities.py            # Carga master CSV
├── aggregator.py        # Combina fuentes → CSV final
├── updater.py           # Aplica CSV → DATA[] + 329 fichas HTML
├── data/
│   └── cities_master.csv  # Fuente de verdad: 329 slugs + valores actuales
└── sources/
    ├── ine.py           # ✅ Población — pobmun.zip — automático
    ├── mivau.py         # ⚠️ Precio €/m² — descarga manual
    ├── notariado.py     # ⚠️ Validación cruzada — descarga manual
    └── observatorios/
        ├── madrid.py    # ⚠️ Madrid CCAA — descarga manual
        ├── cataluna.py  # ⚠️ Cataluña — descarga manual
        └── andalucia.py # ⚠️ Andalucía — descarga manual

data/
├── raw/                  # Cache descargas (pobmun.zip, *.xlsx, *.csv)
├── snapshots/            # Histórico CSV trimestral
└── processed/            # Output: cities_YYYYQN.csv
```

## Comandos

```bash
# Solo fetch (no toca rendata_beta/)
python -m pipeline fetch --quarter 2026Q2

# Solo apply (asume que el CSV ya está generado)
python -m pipeline apply --quarter 2026Q2

# Todo en uno
python -m pipeline run --quarter 2026Q2

# Auditar cobertura sin escribir nada
python -m pipeline audit
```

## Cobertura por fuente

| Fuente | Acceso | Cobertura | Datos |
|---|---|--:|---|
| INE pobmun.zip | ✅ Auto | **329/329 (100%)** | Población |
| MIVAU Excel | ⚠️ Manual | ~250/329 (~75%) si descargado | Precio €/m² compra |
| Notariado | ⚠️ Manual | ~80 capitales/provincias | Validación cruzada |
| Madrid Obs. | ⚠️ Manual | ~19 municipios CAM | Precio + alquiler |
| Cataluña Obs. | ⚠️ Manual | ~27 municipios CAT | Alquiler |
| Andalucía Obs. | ⚠️ Manual | ~30 municipios AND | Precio + alquiler |
| **Días mercado** | ❌ | 0% | Marcado "Estimado" en HTML — no actualizable sin scraping |

Sin descargas manuales, el pipeline solo refresca **población**. Los demás campos quedan con valor histórico.

## Workflow trimestral

1. **Cuando se publican los datos del trimestre** (~15-30 días después del cierre):
   - Visita los portales y descarga los ficheros (ver instrucciones en cada `python -m pipeline.sources.{nombre}`)
   - Guárdalos en `data/raw/` con nombres esperados (`mivau_2026Q2.xlsx`, `madrid_vivienda_2026.csv`, etc.)
2. **Ejecuta**: `python -m pipeline run --quarter 2026Q2`
3. **Revisa** el CSV `data/processed/cities_2026Q2.csv` — verifica fuentes (`fuente_precio`, `fuente_alquiler`)
4. **Despliega**: `git commit && git push && npx wrangler deploy` (los cambios ya están en `rendata_beta/`)

## URLs de descarga manual

| Source | URL portal | Archivo destino |
|---|---|---|
| MIVAU | https://www.mivau.gob.es/vivienda/datos-y-estadisticas | `data/raw/mivau_2026QN.xlsx` |
| Notariado | https://www.notariado.org/portal/centro-de-informacion-estadistica-notarial | `data/raw/notariado_2026QN.xlsx` |
| Madrid CAM | https://datos.comunidad.madrid/dataset?theme=Vivienda | `data/raw/madrid_vivienda_2026.csv` |
| Cataluña | https://analisi.transparenciacatalunya.cat/ | `data/raw/cataluna_lloguer_2026.csv` |
| Andalucía | https://www.juntadeandalucia.es/institutodeestadisticaycartografia | `data/raw/andalucia_vivienda_2026.csv` |

## Política de merge (precio compra)

```
1. MIVAU (oficial)
2. Observatorio CCAA correspondiente
3. Valor histórico (sin cambio)
```

## Política de merge (alquiler)

```
1. Observatorio CCAA correspondiente
2. Estimado: precio_nuevo × (alquiler_actual / precio_actual_historico) × 0.85
3. Valor histórico
```

## Doctrina ROI

`ROI = (alquiler × 12) / (precio_m² × 100m²) × 100`

100m² es la superficie de cálculo unificada en mayo 2026 (próxima a la
media INE 2021 de vivienda española).

## Riesgo legal

Cero. Todas las fuentes son **open data** oficiales con licencia compatible
con uso educativo/comercial siempre que se cite atribución (ya en footer del
sitio: "Fuente: Idealista Q1 2026 · Ministerio de Vivienda").

Si se quisiera mejorar cobertura de alquileres (especialmente municipios
pequeños), las opciones son:
- Acuerdo comercial con Idealista (API B2B, ~€500/mes)
- Convenio con think tanks o universidades que publiquen datasets propios

## Roadmap

- [ ] Catastro SOAP API (superficie media construida por municipio)
- [ ] Banco de España (indicadores macroeconómicos contextuales)
- [ ] Integrar más observatorios CCAA (País Vasco, Galicia, C. Valenciana)
- [ ] Auto-detección del trimestre más reciente publicado en cada portal
- [ ] Test suite con fixtures
