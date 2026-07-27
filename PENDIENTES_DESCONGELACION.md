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

## 3. Campo `pob` de `DATA[]` / `RANK[]` — plan listo, bloqueado por la congelación

**Diagnóstico cerrado y script escrito y validado el 2026-07-27:
`scripts/sync_poblacion.py`.** No se ha aplicado nada porque escribir exige tocar
`ranking.html`, que está congelado. `DATA[]` y `RANK[]` se actualizan **a la vez o
ninguno**: desincronizarlos sería peor que el estado actual.

### 3.1 Qué pasa

`pob` nunca se pobló con padrón: lleva **marcadores redondeados a millar en 176
municipios** (59 de ellos un `30000` genérico). Además `DATA[]` solo tiene el campo en
**448 de 597**, mientras que `RANK[]` lo tiene en los 597.

**Pero las fichas tampoco son fiables del todo**, así que un volcado "desde la ficha"
habría corrompido datos:

- **34 fichas comparten su población con otra ficha.** El valor `50.021` aparece en
  **7 municipios**: Adeje, Cangas do Morrazo, Luarca, Mairena del Aljarafe, Mislata,
  Rincón de la Victoria y Utrera.
- Valores absurdos: **Granada 2.287** hab., **Torrent 182**, **Mieres 369**,
  **Calahorra 680** (su propio texto dice "25.000 habitantes").
- A veces es al revés: **Castellón** muestra 172.000 redondeado y `RANK` trae 180.379,
  que es el fino.

### 3.2 El plan (ya calculado)

| | |
|---|--:|
| Sincronizables con seguridad | **299** (290 desde la ficha + 9 rellenando `DATA` desde `RANK`) |
| En cuarentena, revisión manual | **26** |
| Cobertura de `pob` en `DATA[]` | 448 → **586** |

Salvaguardas que aplica el script antes de fiarse de una ficha: (1) su valor no está
repetido en otra ficha, (2) si `RANK` no es un marcador redondo, la ficha debe estar
entre 0,5x y 2x, (3) la ficha no puede ser redonda a millar cuando `RANK` trae un valor
más fino. Lo que no pasa el filtro queda en cuarentena, no se escribe.

**Los 26 en cuarentena:** 19 por valor duplicado (incluye Adeje, Luarca, Mislata,
Rincón de la Victoria, Utrera, Mairena, Cangas), 4 por ficha implausible frente a un
`RANK` fino (Granada, Torrent, Mieres, Calahorra), 2 por ficha redondeada con `RANK`
más fino (Castellón, Orense) y 1 implausible (Arroyomolinos, ficha 816).

### 3.3 Efecto en el filtro ">50.000 hab." de `ranking.html`

`passes()` usa `c.pob>=50000`. Tras la corrección: **122 → 153 municipios (+31 entran,
0 salen)**. Entran, entre otros, Alcobendas (123.342 reales, hoy figura con 30.000),
Torrejón de Ardoz (143.526), El Ejido (91.440), Chiclana (90.864) y Coslada (80.512).

### 3.4 Cómo aplicarlo

1. Sacar `ranking.html` de `frozen_files.json`.
2. `python scripts/sync_poblacion.py` (informe) y luego `--apply`. El script se niega a
   escribir mientras detecte la congelación.
3. `python scripts/qa_check.py` — el check **[11]** ya está puesto y exige
   `pob` de `DATA[]` == `pob` de `RANK[]` (invariante duro, con test negativo hecho).
   La deuda con las fichas sale como WARN.
4. Resolver los 26 de cuarentena a mano contra INE.

**Nada de esto afecta a rentabilidad, precio, alquiler ni al orden del ranking**, que se
calcula solo con el ROI.
