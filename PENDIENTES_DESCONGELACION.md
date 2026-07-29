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

---

## 4. `rentabilidad-velez-malaga.html` — cifras en prosa editorial

Detectado 2026-07-27 al ejecutar `scripts/fix_prosa_vp_va.py`. Es la única congelada
que necesita el fix de prosa (las otras 6 ya estaban bien en estas frases).

| Bloque | Qué muestra | Debería |
|---|---|---|
| info-box "Mercado en expansión" | subida de precio con el valor de `va` | `vp` = **+7,0%**, y la comparación redactada según los datos |
| "En los últimos 12 meses el precio ha subido un X%" (×2: cuerpo y JSON-LD) | valor cruzado | `vp` = **+7,0%** |
| "revalorización anual del inmueble (+X%)" | valor cruzado | `vp` = **+7,0%** |

**Cómo aplicarlo:** sacar la ficha de `frozen_files.json` y volver a ejecutar
`python scripts/fix_prosa_vp_va.py`. El script ya la detecta y la reporta como
bloqueada. `qa_check[12]` la saca como WARN mientras dure la congelación.

Esta ficha acumula ya tres pendientes (ed-stat `vp`, tabla de gastos y prosa): al
descongelar, ejecutar los tres fixers en orden y revisarla entera.

---

## 5. Sincronización de precio y alquiler — 7 congeladas pendientes

El 2026-07-29 se ligaron a `DATA[]` **19 huecos** de precio/alquiler que hasta ahora
nadie vigilaba (hero, barra sticky, gráfico de evolución, "Pulso del mercado", FAQ
JSON-LD y prosa editorial). Se aplicó a **590 fichas** con `scripts/fix_ficha_sync.py`;
estas 7 quedaron fuera **solo por estar congeladas**.

| Ficha | Huecos a corregir |
|---|---|
| `rentabilidad-alameda` | FAQ (ROI ×2, alquiler 1 y 3 hab., piso 100 m², `va`), prosa (días, ROI), pulso (días) |
| `rentabilidad-archidona` | evo precio, hero alquiler, FAQ (ROI ×2, alquiler y derivados, piso, `va`), prosa (alquiler, ROI, `vp`), badge ITP |
| `rentabilidad-benahavis` | FAQ (ROI, alquiler 1 y 3 hab., piso, `va`), prosa (alquiler, precio), badge ITP |
| `rentabilidad-campillos` | serie histórica, FAQ (ROI, derivados, piso, `va`), prosa (precio), badge ITP |
| `rentabilidad-mollina` | FAQ (ROI ×2, derivados, piso, `va`), prosa (días, ROI), pulso (días) |
| `rentabilidad-velez-malaga` | hero (precio y alquiler), evo badge, FAQ (`vp` ×2, `va` ×2), prosa (precio, `vp`, `va`), badge ITP |
| `rentabilidad-villanueva-del-trabuco` | evo precio + serie, hero alquiler, FAQ (ROI ×2, alquiler y derivados, piso, `va`), prosa (alquiler, días, ROI, `vp`), pulso (días), badge ITP |

**Cómo aplicarlo:** sacarlas de `frozen_files.json` y volver a ejecutar
`python scripts/fix_ficha_sync.py`. El script ya las detecta y las lista como
saltadas. `qa_check[13]` y `[14]` las sacan como **WARN** mientras dure la congelación.

**Riesgo de dejarlo:** medio-bajo. El ROI, el precio y el alquiler del **titular** de las
7 son correctos (los vigilan `[8]` y `[9]`); lo desincronizado son huecos secundarios.
La excepción a mirar con cuidado es `rentabilidad-velez-malaga`, cuyo **hero** sirve un
precio y un alquiler distintos de `DATA[]` — y el hero es lo primero que ve un
periodista. Es la cuarta deuda acumulada de esa ficha.

---

## 6. Tres municipios DUPLICADOS en `DATA[]` y `RANK[]` — plan aprobado, bloqueado

Detectado el 2026-07-29. **El dataset dice 597 municipios pero solo hay 594 distintos.**
Tres municipios aparecen dos veces, con dos slugs, dos fichas vivas y **cifras
contradictorias**:

| Municipio (INE) | Entrada A | Entrada B | Población común |
|---|---|---|--:|
| Ourense · 32054 | `ourense` — #21, **6,8%**, 1.080 €/m², 610 €/mes | `orense` — #256, **5,8%**, 1.150 €/m², 555 €/mes | 105.769 |
| Castelló de la Plana · 12040 | `castellon` — #197, **6,0%**, 1.500 €/m², 750 €/mes | `castellon-de-la-plana` — #231, **5,9%**, 1.400 €/m², 690 €/mes | 180.379 |
| Calp · 03047 | `calpe` — #550, **5,1%**, 2.800 €/m², 1.200 €/mes | `calp` — #356, **5,6%**, 2.310 €/m², 1.080 €/mes | 27.616 |

El duplicado viene de origen: `pipeline/data/cities_master.csv` ya trae las dos filas de
cada par. `qa_check[3]` solo exigía slugs únicos, no municipios únicos.

### 6.1 Qué dice la fuente oficial

Verificado contra INE y BOE:

- **Ourense** es la denominación del INE (código 32054); *Orense* es la forma castellana,
  no la oficial.
- **Castelló de la Plana** es la denominación exclusiva desde el
  [Decreto 40/2019 del Consell](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-5721)
  (INE 12040). Ni *Castellón* ni *Castellón de la Plana* son ya la forma oficial.
- **Calp** es la denominación exclusiva desde el
  [Decreto 125/2009 del Consell](https://www.boe.es/diario_boe/txt.php?id=BOE-A-2009-15957)
  (INE 03047); en 2022 el ayuntamiento inició el expediente para recuperar la forma
  bilingüe *Calp/Calpe*.

> **Lo que la fuente oficial NO resuelve: cuál de los dos precios es el bueno.** El INE no
> publica precio ni alquiler, y en `data/processed/cities_2026Q3.csv` **las dos filas de
> cada par salen marcadas `estimado_ratio` / `historico`**: ninguna está medida. Elegir una
> u otra es elegir entre dos estimaciones igual de respaldadas. Por eso el plan es
> quedarse con la del slug que se conserva y **volver a medir los tres municipios contra
> MIVAU en el próximo trimestre** en vez de fingir que una de las dos es la correcta.

### 6.2 Cuál se queda y cuál se retira

Evidencia de enlazado interno medida sobre las 844 páginas:

| Slug | Enlaces internos | Páginas que enlazan | ¿Página `barrios-`? | ¿En `_redirects`? |
|---|--:|--:|:--:|:--:|
| `ourense` | **24** | 16 | sí | no |
| `orense` | 15 | 11 | no | no |
| `castellon` | **26** | 22 | no | no |
| `castellon-de-la-plana` | 18 | 12 | sí | sí |
| `calpe` | **10** | 7 | no | no |
| `calp` | 9 | 8 | no | no |

**Propuesta:**

1. **Ourense** — se queda `ourense` (nombre oficial *y* más enlazado). Se retira `orense`
   con **301 → `/rentabilidad-ourense`**. Decisión limpia: los dos criterios coinciden.
2. **Castellón** — se queda **`castellon`** (26 enlaces frente a 18) con el **nombre
   mostrado corregido a "Castelló de la Plana"**, y 301 desde `castellon-de-la-plana`.
   *Aquí los dos criterios NO coinciden* (el slug oficial sería el otro, que además tiene
   la página `barrios-`): se prioriza el URL con más enlaces entrantes y mejor encaje con
   la demanda de búsqueda, y se arregla el nombre visible. **Confirmar antes de ejecutar.**
3. **Calp/Calpe** — se queda **`calpe`** (10 enlaces frente a 9, y es la forma dominante en
   búsqueda) con el nombre mostrado **"Calp"**, y 301 desde `calp`. Margen estrecho:
   también es defendible al revés. **Confirmar antes de ejecutar.**

Ninguna de las tres se borra: las 6 tienen enlaces internos, así que las tres retiradas
van con **301**, no con `rm`. Sus enlaces internos hay que repuntarlos igualmente, o
`qa_check[1]` se cae al borrar el fichero.

### 6.3 Por qué está bloqueado

| Lo que exige | Choca con |
|---|---|
| Quitar 3 entradas de `RANK[]` | `ranking.html` está **congelado**, y es la URL que los 3 emails de prensa invitan a abrir |
| Recalcular los puestos `r:` de los 597 | Ídem: todo `RANK[]` se renumera |
| Bajar el contador **597 → 594** | Aparece **1.009 veces en 821 ficheros**, incluidos **los 9 congelados** |
| Ídem | Hay un artículo publicado cuya **URL** lleva la cifra: `/actualidad-597-mercados-vivienda-2026` |
| Ídem | El dato macro del dossier nacional pasa a ser **"593 de 594 rinden más que Madrid"**, y el "596 de 597" ya está en la bandeja de entrada de los periodistas |

### 6.4 Cómo aplicarlo (al levantar la congelación)

1. Confirmar las dos decisiones marcadas arriba (Castellón y Calp/Calpe).
2. Quitar las 3 entradas retiradas de `DATA[]` (`index.html`) y de `RANK[]`
   (`ranking.html`), y renumerar `r:` en `RANK[]`.
3. Repuntar los enlaces internos de las 3 retiradas hacia el slug que se queda.
4. Añadir los 3 `301` a `rendata_beta/_redirects` y quitar las 3 URLs de `sitemap.xml`.
5. Corregir el nombre mostrado a la forma oficial en las fichas que se quedan.
6. Sustituir **597 → 594** en los 821 ficheros; decidir aparte qué hacer con la URL
   `/actualidad-597-mercados-vivienda-2026` (301 a una nueva o dejarla y corregir solo el
   cuerpo).
7. Rehacer también `pipeline/data/cities_master.csv`, que es de donde nace el duplicado,
   o volverá a aparecer en la siguiente pasada del pipeline.
8. Añadir a `qa_check` un check de **municipio único** (hoy `[3]` solo mira slugs):
   mismo `cc` + misma `pob` exacta y no redondeada ⇒ error.
9. Actualizar `dossier_top_nacional.md` ("596 de 597") y `dossier_nuevos_angulos.md`
   (que ya avisa del duplicado y no propone Ourense por este motivo).

### 6.5 Falso positivo descartado

**Berga y Canovelles** (Cataluña) comparten el valor `17.473` de población siendo
municipios distintos. **No es un duplicado**: es un error del campo `pob`, que entra en la
deuda del punto 3 de este documento, no en esta.
