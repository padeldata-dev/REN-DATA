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

## 2. Tabla "Gastos reales" — 7 congeladas pendientes (fórmula YA aprobada y aplicada al resto)

El saneamiento se aplicó el 2026-07-27 a **590 fichas** con `scripts/fix_gastos_reales.py`.
Estas 7 quedaron fuera **solo por estar congeladas**. Para aplicarlas: sacarlas de
`frozen_files.json` y volver a ejecutar el script — ya las detecta y las reporta como
bloqueadas.

Fórmula aplicada: `ingresos = alq×12`, cada gasto = su % actual × ingresos nuevos,
`neto_€ = ingresos − Σgastos`, `neto_% = neto_€ / (precio_m² × 100)`. Las del grupo A
reciben además la línea "Estimación con parámetros medios…" bajo la tabla.

| Ficha | Grupo | Ingresos que muestra | `alq`×12 correcto | Qué le falta |
|---|---|---|---|---|
| `rentabilidad-mollina` | A | 6.000€ | 5.760€ | base + neto + nota de estimación |
| `rentabilidad-villanueva-del-trabuco` | A | 6.000€ | 5.400€ | base + neto + nota de estimación |
| `rentabilidad-alameda` | A | 6.000€ | 5.520€ | base + neto + nota de estimación |
| `rentabilidad-archidona` | A | 6.000€ | 6.240€ | base + neto + nota de estimación |
| `rentabilidad-campillos` | B | 6.720€ | 6.000€ | base (implica 560€/mes; hoy `alq`=500€) + neto |
| `rentabilidad-benahavis` | B | 14.160€ | 16.800€ | base (implica 1.180€/mes; hoy `alq`=1.400€) + neto |
| `rentabilidad-velez-malaga` | C | 9.600€ | 9.600€ | solo el neto (la base ya es correcta) |

`mercado-inmobiliario-provincia-malaga-2026` y `ranking.html` no tienen tabla de gastos
(verificado): de las 9 congeladas entran **7** en el lote.

`qa_check[10]` las reporta como **WARN**, no como error, para no bloquear deploys
mientras dure la campaña.

**Ninguno de los 3 emails cita la tabla de gastos.** La congelación no está protegiendo
un dato erróneo comunicado a prensa: protege una página cuyo titular (ROI, precio,
alquiler, puesto nacional) sí es correcto y está verificado.

