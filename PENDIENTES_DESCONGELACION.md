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

---

## 3. Campo `pob` de `DATA[]` / `RANK[]` — estimaciones redondeadas, no datos

**Resuelto el origen el 2026-07-27.** No es un caso aislado de La Unión: el campo `pob`
lleva **marcadores redondeados a millar en 175 de los 448 municipios** que lo tienen, y
en muchos es un **30.000 genérico**. Las fichas, en cambio, llevan el dato real de padrón.
Difieren en **176 fichas**.

### 3.1 La Unión — dato confirmado

| | |
|---|---|
| **Cifra correcta** | **21.380 habitantes** — INE 2025, municipio completo (código INE 30041, comarca del Campo de Cartagena). Serie coherente: 20.560 (Censo 2021) → 21.153 (1-ene-2024) → 21.380 (2025). |
| **Ya correcto en** | `rentabilidad-la-union.html` (bloque Demografía) — **no requiere acción** |
| **A corregir** | `rendata_beta/ranking.html` → `RANK[]`, entrada `sl:"la-union"`: **`pob:18000` → `pob:21380`** |
| **A corregir** | `rendata_beta/index.html` → `DATA[]`, entrada `sl:"la-union"`: **`pob:18000` → `pob:21380`** |
| **Por qué no se aplica hoy** | `ranking.html` está congelado. Tocar solo `index.html` dejaría `DATA[]` y `RANK[]` desincronizados, que es peor que la incoherencia actual. **Se aplican los dos a la vez o ninguno.** |
| **Urgencia** | Media. La Unión es #3 nacional y va en el envío de prensa top nacional, pero el dossier ya indica usar 21.380 y `pob` **no interviene** en el cálculo del puesto (solo el ROI). |

### 3.2 El problema de fondo — el filtro ">50.000 hab." del ranking está mal

`ranking.html` usa `c.pob>=50000` para el filtro de municipios grandes. Con los
marcadores redondeados, **37 municipios quedan fuera del filtro pese a superar los
50.000 habitantes**. Los peores casos:

| Municipio | Población real (ficha) | `pob` en DATA/RANK |
|---|--:|--:|
| Alcobendas | 123.342 | 30.000 |
| El Ejido | 91.440 | 30.000 |
| Chiclana de la Frontera | 90.864 | 30.000 |
| El Puerto de Santa María | 89.983 | 30.000 |
| Coslada | 80.512 | 30.000 |
| Collado Villalba | 67.274 | 30.000 |
| El Prat de Llobregat | 66.338 | 30.000 |
| Granadilla de Abona | 58.752 | 30.000 |
| Cerdanyola del Vallès | 58.528 | 30.000 |
| Calvià | 53.793 | 30.000 |

Ninguno entra falsamente (0 falsos positivos): el sesgo es solo por defecto.

**Cómo aplicarlo al descongelar:** repoblar `pob` en `DATA[]` y `RANK[]` desde el dato
de padrón que ya tienen las fichas (que es el bueno), no desde los marcadores. Añadir
después un check a `qa_check.py` que exija `pob` de `DATA[]` == habitantes de la ficha,
igual que se hizo con ROI, días y vp.

**Esto NO afecta a ninguna cifra de rentabilidad, precio, alquiler ni al orden del
ranking**, que se calcula solo con el ROI.
