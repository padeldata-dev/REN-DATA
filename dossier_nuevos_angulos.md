# Nuevos ángulos de prensa — exploración del DATA[] completo (597 municipios)

> **Uso interno.** No se publica ni se despliega.
> Cifras verificadas el **2026-07-29** contra `DATA[]` de `index.html`, `RANK[]` de `ranking.html`
> y las **fichas descargadas en vivo de rendata.es** (producción == repo, comprobado por SHA256).
> ROI = rentabilidad bruta estimada (alquiler anual / precio, superficie 100 m²).
> Media nacional real de los 597: **5,79% → 5,8%**.
> Zonas descartadas como protagonistas: provincia de Málaga completa, Cuenca, Zamora, La Unión,
> Ciudad Real, Teruel, Jaén, Ávila, Soria, Lugo y Cáceres.

---

## Resumen: 4 historias, ordenadas por fuerza del titular

| # | Protagonista | Titular en una línea | Ficha |
|---|---|---|:--:|
| 1 | **Alicante** | La ciudad donde más ha subido la vivienda de España (+13,0%) | ✅ limpia |
| 2 | **Badajoz · Albacete · Almería** | Las tres ciudades grandes más rentables de España | ✅ limpias |
| 3 | **Lleida** | La gran ciudad donde más sube el alquiler (+16,1%) | ✅ limpia |
| 4 | **Palencia** | Capital de 6,8% con el piso a 102.000 € | ✅ limpia |

Una quinta historia (**Ourense**, contraste interior-costa gallego) está **bloqueada por un bug de
datos**: ver §6.

---

## 1. Alicante — la ciudad donde más ha subido la vivienda de España

**Ángulo:** el precio corre por delante del alquiler y se come la rentabilidad. Alicante es el
municipio donde más ha subido el precio de toda la serie, y a la vez está en el **puesto 454 de 597**
por rentabilidad. Titular doble: récord de subida + advertencia al comprador.

**Datos (verificados en ficha viva):**

- **+13,0% de subida del precio en un año — el dato más alto de los 597 municipios, sin empate.**
  Los siguientes van a +12,0%: Valencia, Madrid, Jávea y Mojácar.
- El alquiler sube **+9,0%**: el precio corre **4,0 puntos** por delante. Es la **segunda tijera
  precio-alquiler más ancha de España**, solo por detrás de Málaga capital (+4,6 puntos).
- **ROI 5,3% — puesto #454 de 597**, por debajo de la media nacional (5,8%). Un piso de 100 m²
  cuesta **225.000 €** y se paga con **18,9 años** de alquiler íntegro.
- m² a **2.250 €**, alquiler medio **990 €/mes**, **19 días** de venta media, 338.577 habitantes.
- Contraste directo: Valencia 2.700 €/m² (+12,0%) y Madrid 5.960 €/m² (+12,0%) — Alicante sube más
  que las dos.

**Matiz que conviene tener preparado** (el mismo de Benahavís y Madrid en los dossiers anteriores):
que la rentabilidad del alquiler caiga no significa que sea mal negocio; significa que es mal negocio
**de renta**, porque el precio se está revalorizando más rápido. Es negocio de patrimonio, no de flujo.

**Municipio de prensa:** Alicante ciudad / provincia de Alicante.

---

## 2. Badajoz, Albacete y Almería — las tres ciudades grandes más rentables de España

**Ángulo:** el dossier del top nacional dice que la rentabilidad está en las capitales pequeñas del
interior. Estas tres lo completan por el otro lado: **son las únicas ciudades de más de 150.000
habitantes que superan el 6,5%**. Responde a la pregunta obvia de cualquier periodista — *"vale, ¿y
en una ciudad de verdad?"*. Sirve como envío nacional y como tres envíos locales.

De los **45 municipios de más de 150.000 habitantes** del dataset, el podio de rentabilidad es:

| | Municipio | Nac./597 | Población | ROI | m² | Alquiler | Piso 100 m² | Años de alquiler |
|--|---|--:|--:|--:|--:|--:|--:|--:|
| 🥇 | **Badajoz** | #15 | 150.209 | **6,9%** | 920 € | 530 €/mes | **92.000 €** | 14,5 |
| 🥈 | **Albacete** | #20 | 175.400 | **6,8%** | 1.200 € | 680 €/mes | 120.000 € | 14,7 |
| 🥉 | **Almería** | #43 | 205.468 | **6,6%** | 1.380 € | 760 €/mes | 138.000 € | 15,1 |

- Las tres están **por encima de la media nacional (5,8%)** y las tres son capitales de provincia,
  en tres comunidades distintas (Extremadura, Castilla-La Mancha, Andalucía).
- **Contraste:** Madrid, con 3,5% (#597 de 597), el m² a 5.960 € y **28,4 años** de alquiler para
  pagar el mismo piso. Badajoz lo hace en **14,5 años** — prácticamente la mitad (1,96 veces menos).
- Dato extra para Albacete y Almería: son también de las que más sube el alquiler —
  **Albacete +13,6%** y **Almería +14,0%** (puestos 4º y 3º entre las ciudades de más de 100.000 hab).
- Dato extra para Almería: es **la 2ª capital andaluza más rentable**, solo por detrás de Jaén (7,1%),
  y muy por delante de Sevilla (5,3%), Granada (5,5%) o Málaga (5,1%).

> ⚠️ **No enlazar la 4ª de la lista.** La siguiente sería Sabadell (6,4%), pero su ficha tiene el
> bloque de cabecera descuadrado (ver §7). Si hace falta un cuarto nombre, la cifra es correcta en
> `DATA[]`/ranking; lo que no conviene es mandar a un periodista a esa página.

**Municipios de prensa:** Badajoz · Albacete · Almería (tres envíos independientes + uno nacional).

---

## 3. Lleida — la gran ciudad donde más sube el alquiler de España

**Ángulo:** el reverso exacto de Alicante. Aquí el alquiler sube más del doble que el precio, así que
la rentabilidad va **al alza**. Y es la historia de la capital catalana barata que nadie mira.

**Datos (verificados en ficha viva):**

- **Alquiler +16,1% en un año: la cifra más alta de los 66 municipios de más de 100.000 habitantes**,
  con distancia. Le siguen Huelva (+14,4%), Almería (+14,0%) y Albacete (+13,6%).
- El precio sube **+7,5%**: el alquiler corre **8,6 puntos** por delante. Es la **segunda tijera
  alquiler-precio más ancha de España** de los 597.
- **ROI 6,0% (#199 de 597)**, m² a **1.300 €**, alquiler **650 €/mes**, 22 días de venta,
  146.266 habitantes. Piso de 100 m²: **130.000 €**, 16,7 años de alquiler.
- **Es la capital catalana más barata, con diferencia:** Barcelona 4.900 €/m², Girona 2.300 €,
  Tarragona 1.780 €, **Lleida 1.300 €**. El m² de Barcelona cuesta **3,8 veces** el de Lleida.
- Empata en ROI con Tarragona (6,0%) y la adelanta en el ranking (#199 vs #201): decir *"la capital
  catalana más rentable"* es correcto según el ranking publicado, pero si un periodista aprieta, la
  respuesta honesta es *"empata con Tarragona y encabeza por desempate"*.

> ⚠️ **Precaución al citar Ávila.** En términos absolutos el récord nacional de subida del alquiler es
> de Ávila (+20,0%), que está reservada para la tanda del top nacional. Por eso el titular de Lleida
> debe acotarse a **"ciudades de más de 100.000 habitantes"** — así es exacto y no choca con el otro envío.
>
> ⚠️ **No enlazar la ficha de Barcelona** para el contraste (tiene el bloque de cabecera descuadrado, §7).
> El 4,6% y los 4.900 €/m² son correctos en `DATA[]`; usar el ranking como enlace.

**Municipio de prensa:** Lleida / comarca del Segrià (Ponent).

---

## 4. Palencia — la capital pequeña donde el alquiler corre al doble que el precio

**Ángulo:** el de "primer comprador" que pedías. Capital de provincia con servicios, 77.000
habitantes, y un piso de 100 m² por **102.000 €** rindiendo un **6,8%**. Es el perfil exacto de quien
da el salto a comprar por primera vez.

**Datos (verificados en ficha viva):**

- **ROI 6,8% — puesto #23 de 597**, un punto entero por encima de la media nacional.
- m² a **1.020 €**: la **2ª capital de provincia más barata** de todas las que no están ya en el
  dossier del top nacional (solo Badajoz, 920 €, es más barata).
- Piso de 100 m²: **102.000 €**. Se paga con **14,7 años** de alquiler íntegro, frente a los 28,4 de Madrid.
- Alquiler **580 €/mes**, subiendo un **+13,2%** anual frente a un **+7,5%** del precio: **5,7 puntos**
  de tijera, la **3ª más ancha de España** (tras Ávila y Lleida).
- 28 días de venta media, 77.466 habitantes.

**Segundo nombre para el mismo pitch, si quieres doblar el envío:** **Huesca** — #49 de 597, ROI 6,6%,
m² 1.350 €, alquiler 740 €/mes, 55.454 hab, piso de 100 m² por 135.000 €, 15,2 años. Ficha también
limpia. Aragón queda cubierto sin tocar Teruel.

**Municipio de prensa:** Palencia (y Huesca como segundo).

---

## 5. Comprobación de bugs — las 4 familias conocidas

`python scripts/qa_check.py` pasa en verde: **[9] badge "Media España" y [12] prosa editorial (yield,
12 meses, revalorización, cruce vp/va) están OK en las 596 fichas no congeladas**. La única desviación
es `rentabilidad-velez-malaga.html`, que está congelada y ya anotada.

Verificación adicional, ficha por ficha y **contra producción en vivo**, de las 6 candidatas:

| Ficha | yield≠ROI | badge Media España | cruce vp/va | 12 meses | hero | ITP | serie | Congelada |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Alicante | ✅ | ✅ 5,8% | ✅ | ✅ 13,0% | ✅ | ✅ | ✅ | no |
| Badajoz | ✅ | ✅ 5,8% | ✅ | ✅ 8,0% | ✅ | ✅ | ✅ | no |
| Albacete | ✅ | ✅ 5,8% | ✅ | ✅ 8,5% | ✅ | ✅ | ✅ | no |
| Almería | ✅ | ✅ 5,8% | ✅ | ✅ 9,5% | ✅ | ✅ | ✅ | no |
| Lleida | ✅ | ✅ 5,8% | ✅ | ✅ 7,5% | ✅ | ✅ | ✅ | no |
| Palencia | ✅ | ✅ 5,8% | ✅ | ✅ 13,2% | ✅ | ✅ | ✅ | no |

Ninguna de las 6 está en `frozen_files.json`. Producción == repo (SHA256 sobre contenido normalizado a LF).

---

## 6. Historia bloqueada — Ourense y el contraste interior-costa gallego

El ángulo es bueno y es exactamente el "Ronda / Axarquía fuera de Andalucía" que buscabas:

- **Ourense (interior): ROI 6,8% (#21 de 597), m² 1.080 €, 105.769 hab.**
- **A Coruña (costa): ROI 5,0% (#557 de 597), m² 2.100 €.**
- **536 puestos de diferencia** y casi el doble de precio por metro, dentro de la misma comunidad.
  Vigo 5,8% / 1.850 €, Pontevedra 5,4% / 1.700 €.

**Está bloqueado.** `DATA[]` contiene el municipio **dos veces**, con cifras contradictorias y las dos
fichas vivas y publicadas:

| Slug | Nombre | Puesto | ROI | m² | Alquiler | Población |
|---|---|--:|--:|--:|--:|--:|
| `ourense` | Ourense | **#21** | **6,8%** | 1.080 € | 610 €/mes | 105.769 |
| `orense` | Orense | **#256** | **5,8%** | 1.150 € | 555 €/mes | 105.769 |

Misma población exacta, misma comunidad: es el mismo municipio duplicado. Un periodista que busque
"Ourense" en el buscador del sitio encuentra las dos y la historia se cae sola. **Hay que fusionarlas
antes de proponer esta plaza.**

---

## 7. Hallazgos de calidad de datos (fuera de las 4 familias conocidas)

Al barrer las 597 fichas para validar candidatas aparecieron cuatro problemas sistémicos que
`qa_check.py` no cubre hoy. Ninguno afecta a las 4 historias propuestas — todas se eligieron entre las
que pasan limpias — pero acotan mucho a qué páginas se puede mandar a un periodista.

1. **Bloque de cabecera (hero) descuadrado con `DATA[]` — 484 de 597 fichas.**
   El check [8] vigila el ROI en 7 sitios, los días y el `vp` del `ed-stat`, pero **no** el precio, el
   alquiler ni los porcentajes del hero. Desglose: 380 fichas con el alquiler mal, 283 con el `va`,
   263 con el precio, 165 con el `vp`.
   *Ejemplo:* Villena muestra en cabecera 750 €/m² ↑11,0% y 400 €/mes ↑15,0%, cuando `DATA[]` dice
   730 €, +9,4%, 389 € y +7,6%. En la misma página, el bloque editorial sí da los valores correctos.

2. **Serie histórica que contradice su propia etiqueta — 74 fichas** bajan de precio en el gráfico
   mientras muestran una flecha ↑, y en **263** el último punto de la serie no coincide con el precio
   de `DATA[]`.
   *Ejemplo:* Sestao dibuja 2.820 € (2024) → 1.900 € (2026) con la etiqueta "↑ 4,5% último año".
   Es el riesgo más citable de todos: es lo que un periodista captura de pantalla.

3. **`meta description` con el alquiler desincronizado — 216 de 597 fichas.**
   El ROI y el precio de la meta sí cuadran en las 597; solo falla el alquiler. Es lo que sale en
   Google, no en la página. *Ejemplo:* Langreo anuncia 440 €/mes y su `DATA[]` dice 452 € (440 es,
   justamente, el de Ferrol).

4. **Tarjeta de ITP incoherente con su propio tipo — 163 fichas.** Arrastran un texto de plantilla
   ("piso de 68.880 €, 5.510 € de ITP") que no corresponde ni al precio del municipio ni al tipo de su
   comunidad. En Villena la tarjeta rotula 10% y el importe sale al 8%.

5. **Tres municipios duplicados** — el dataset dice 597 y en realidad son **594 distintos**:

   | Duplicado | Puesto / ROI | Puesto / ROI | Población común |
   |---|---|---|--:|
   | Ourense / Orense | #21 · 6,8% | #256 · 5,8% | 105.769 |
   | Castellón / Castellón de la Plana | #197 · 6,0% | #231 · 5,9% | 180.379 |
   | Calpe / Calp | #550 · 5,1% | #356 · 5,6% | 27.616 |

   Afecta al dato macro del dossier nacional ("596 de 597 rinden más que Madrid") y a cualquier
   titular sobre **Castellón**, que hoy aparece dos veces con dos rentabilidades distintas.
   *(Nota aparte: Berga y Canovelles comparten el valor 17.473 de población siendo municipios
   distintos — ahí el error está en el campo `pob`, no hay duplicado.)*

**Fichas sin ninguna contradicción visible: 63 de 597.** Es, hoy por hoy, el universo del que conviene
sacar candidatas de prensa.

---

*Fuente: `DATA[]` y `RANK[]` de Ren Data (597 registros, Q1 2026), verificados contra
https://rendata.es el 2026-07-29. Precio y alquiler: Ministerio de Vivienda / observatorios
autonómicos; población: INE Padrón. Rentabilidad bruta estimada sobre 100 m².*
