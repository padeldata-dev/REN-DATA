# Pendientes de aplicar al levantar la congelación

**Congelación activa desde:** 2026-07-27 (campaña de prensa Málaga, 3 emails enviados).
**Ficheros congelados:** los 9 de `frozen_files.json`.

Todo lo de aquí es una corrección **legítima y verificada** que NO se aplicó porque
tocaría una página que los periodistas tienen delante. Al levantar la congelación:
aplicar, correr `python scripts/qa_check.py`, y borrar la entrada.

---

## 1. `rentabilidad-velez-malaga.html` — ed-stat "subida precio anual"

| | |
|---|---|
| **Muestra** | `+10%` |
| **DATA[] dice** | `vp: 7.0` → debería ser `+7,0%` |
| **Detectado** | 2026-07-27, al ejecutar `scripts/fix_edstat_dias_vp.py` |
| **Cómo aplicarlo** | Basta con volver a ejecutar `python scripts/fix_edstat_dias_vp.py` una vez la ficha salga de `frozen_files.json`. El script ya la detecta y la reporta como bloqueada. |
| **Riesgo de dejarlo** | Bajo. Es el bloque editorial destacado; ningún email de prensa cita la revalorización de Vélez-Málaga (solo su ROI 6,0%, que sí es correcto). |

`qa_check[8]` lo saca como **WARN**, no como error, precisamente para que no bloquee
los deploys mientras dure la congelación.

---

## 2. Tabla "Gastos reales" — 8 de las 9 congeladas están afectadas

El saneamiento de la tabla de gastos (ver informe del 2026-07-27) está **parado a la
espera de aprobación de la fórmula**. Cuando se apruebe, estas congeladas entran en el
mismo lote:

| Ficha | Ingresos que muestra | `alq`×12 real | Estado |
|---|---|---|---|
| `rentabilidad-mollina` | 6.000€ | 5.760€ | plantilla sin personalizar |
| `rentabilidad-villanueva-del-trabuco` | 6.000€ | 5.400€ | plantilla sin personalizar |
| `rentabilidad-alameda` | 6.000€ | 5.520€ | plantilla sin personalizar |
| `rentabilidad-archidona` | 6.000€ | 6.240€ | plantilla sin personalizar |
| `rentabilidad-campillos` | 6.720€ | 6.000€ | trimestre anterior (implica 560€/mes; hoy `alq`=500€) |
| `rentabilidad-benahavis` | 14.160€ | 16.800€ | trimestre anterior (implica 1.180€/mes; hoy `alq`=1.400€) |
| `rentabilidad-velez-malaga` | 9.600€ | 9.600€ | **correcta, no requiere acción** |

`mercado-inmobiliario-provincia-malaga-2026` y `ranking.html` no tienen tabla de gastos
(verificado). Así que de las 9 congeladas, **6 entrarán en el lote** y 3 no.

**Ninguno de los 3 emails cita la tabla de gastos**, así que la congelación no protege
un dato erróneo que se haya comunicado: protege una página cuyo titular sí es correcto.
