#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera rendata_beta/academia.html (índice) y rendata_beta/academia/que-es-{slug}.html (30 mini-guías)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
SCRATCH = Path(r"C:\Users\Usuario\AppData\Local\Temp\claude\C--Users-Usuario-REN-DATA\209ab947-f175-4d83-8ecb-870b342fced2\scratchpad")

HEADER = (SCRATCH / "header.html").read_text(encoding="utf-8")
FOOTER = (SCRATCH / "footer.html").read_text(encoding="utf-8")

CATS = [
    ("conceptos-basicos", "📐", "Conceptos básicos"),
    ("fiscalidad", "🧾", "Fiscalidad"),
    ("hipotecas", "🏦", "Hipotecas"),
    ("inversion", "📈", "Inversión"),
    ("proceso-compra", "🔑", "Proceso de compra"),
]

# slug, name, cat, definicion, ejemplo, [errores], cta_href, cta_text
TERMS = [
    ("roi-inmobiliario", "ROI inmobiliario", "conceptos-basicos",
     "Return on Investment. Medida de la ganancia total de una inversión en relación con su coste, incluyendo tanto ingresos por alquiler como revalorización del activo.",
     "Un piso comprado por 100.000€ que genera 5.000€/año en alquiler y se revaloriza un 5% tiene un ROI total del 10% anual.",
     ["Calcular el ROI solo con el alquiler, sin incluir la revalorización (o depreciación) del inmueble.",
      "No descontar los gastos de compra (ITP, notaría, gestoría) al calcular el capital realmente invertido.",
      "Confundir ROI con rentabilidad anual: el ROI puede calcularse acumulado a varios años, no solo anual."],
     "/ranking.html", "Consulta el ROI real de 587 ciudades en el ranking Ren Data"),

    ("rentabilidad-bruta", "Rentabilidad bruta", "conceptos-basicos",
     "Porcentaje que representa los ingresos anuales por alquiler sobre el precio de compra del inmueble, sin descontar gastos.",
     "Si compras un piso por 150.000€ y lo alquilas por 750€/mes, tus ingresos anuales son 9.000€. La rentabilidad bruta es 9.000/150.000 × 100 = 6%.",
     ["Usarla como única referencia para decidir una compra, sin mirar la rentabilidad neta (que descuenta gastos reales).",
      "No actualizar el cálculo si el alquiler de mercado cambia tras la compra.",
      "Comparar rentabilidades brutas entre ciudades con estructuras de gastos e impuestos muy distintas."],
     "/ranking.html", "Compara la rentabilidad bruta y neta de cada ciudad en el ranking"),

    ("rentabilidad-neta", "Rentabilidad neta", "conceptos-basicos",
     "Rentabilidad real después de descontar todos los gastos: IBI, comunidad, seguro, mantenimiento, vacancia y gestoría.",
     "Sobre una rentabilidad bruta del 6%, los gastos típicos reducen entre 1,5 y 2 puntos, dejando una rentabilidad neta de entre 4% y 4,5%.",
     ["Olvidar incluir la vacancia media (meses sin inquilino) en el cálculo de gastos.",
      "No actualizar los gastos de comunidad o seguro al comparar con años anteriores.",
      "Confundir rentabilidad neta con cash flow: la rentabilidad neta no descuenta la cuota de la hipoteca, el cash flow sí."],
     "/ranking.html", "Consulta la rentabilidad neta estimada por ciudad"),

    ("precio-por-metro-cuadrado", "Precio por metro cuadrado", "conceptos-basicos",
     "Precio de venta o alquiler de un inmueble dividido entre su superficie en metros cuadrados. Es el indicador más usado para comparar inmuebles.",
     "Un piso de 80 m² vendido por 200.000€ tiene un precio de 2.500€/m². Si el precio medio de la zona es 2.200€/m², se está pagando un 14% por encima de la media.",
     ["Compararlo entre viviendas con calidades, antigüedad o alturas muy distintas sin ajustar por esas diferencias.",
      "No verificar si la superficie es construida o útil: la diferencia puede ser del 10-15% y distorsiona la comparación.",
      "Usar solo el precio medio de la ciudad sin mirar el barrio, donde el precio por m² puede variar mucho."],
     "/ranking.html", "Consulta el precio medio por m² de cada ciudad española"),

    ("valor-catastral", "Valor catastral", "conceptos-basicos",
     "Valor administrativo asignado por el Catastro a cada inmueble. Sirve de base para calcular el IBI y otros impuestos. Suele ser inferior al precio de mercado.",
     "Un piso con valor catastral de 80.000€ puede tener un precio de mercado de 200.000€. El IBI se calcula aplicando un tipo sobre el valor catastral.",
     ["Pensar que el valor catastral y el valor de mercado son iguales: el catastral suele ser inferior y desactualizado.",
      "Olvidar que el valor catastral también se usa para calcular el ITP mínimo o la plusvalía municipal, no solo el IBI.",
      "No comprobar si ha habido una revisión catastral reciente en el municipio, que puede haber subido el valor de forma notable."],
     "/calculadora-hipoteca.html", "Simula tu hipoteca con la calculadora Ren Data"),

    ("itp-impuesto-transmisiones-patrimoniales", "ITP (Impuesto de Transmisiones Patrimoniales)", "fiscalidad",
     "Impuesto que grava la compraventa de vivienda de segunda mano. Lo paga el comprador. Varía entre el 6% y el 10% según la comunidad autónoma.",
     "En Andalucía el ITP es el 7%. Si compras por 200.000€, pagas 14.000€ de ITP. En Cataluña sería el 10%, es decir, 20.000€.",
     ["Olvidar presupuestar el ITP al calcular el coste total de la compra: se paga aparte del precio y la hipoteca no siempre lo cubre.",
      "Pensar que el porcentaje es igual en toda España: varía entre el 6% y el 10% según la comunidad autónoma.",
      "Confundirlo con el IVA: el ITP solo aplica a vivienda de segunda mano; la vivienda nueva paga IVA."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Consulta el ITP exacto de tu comunidad autónoma"),

    ("iva-vivienda-nueva", "IVA en vivienda nueva", "fiscalidad",
     "Las viviendas nuevas tributan por IVA (10% general, 4% para vivienda protegida) en lugar de ITP. Además lleva AJD.",
     "Un piso nuevo de 250.000€ lleva 25.000€ de IVA al 10% más el AJD (entre 0,5% y 1,5% según CCAA).",
     ["Olvidar sumar el AJD al presupuesto, que se paga además del IVA en vivienda nueva.",
      "Pensar que el tipo reducido del 4% aplica a cualquier vivienda: solo aplica a vivienda protegida (VPO) en las condiciones que fija cada CCAA.",
      "No verificar si la promotora incluye el IVA en el precio anunciado o si se añade aparte."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Calcula todos los gastos de comprar vivienda nueva"),

    ("ajd-actos-juridicos-documentados", "AJD (Actos Jurídicos Documentados)", "fiscalidad",
     "Impuesto sobre la escritura pública de compraventa e hipoteca. En vivienda nueva lo paga el comprador, en hipotecas lo paga el banco desde 2018.",
     "El AJD varía entre el 0,5% y el 1,5% según la comunidad. En una hipoteca de 160.000€, el banco paga entre 800€ y 2.400€.",
     ["Pensar que el comprador paga siempre el AJD de la hipoteca: desde 2018 lo paga el banco por ley.",
      "No comprobar el tipo exacto de la CCAA (varía entre 0,5% y 1,5%), que afecta directamente al presupuesto de la escritura de compraventa.",
      "Confundir el AJD de la escritura de compraventa (que sí paga el comprador) con el de la hipoteca (que paga el banco)."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Consulta el AJD por comunidad autónoma"),

    ("plusvalia-municipal", "Plusvalía municipal", "fiscalidad",
     "Impuesto municipal sobre el incremento del valor del suelo urbano al transmitir un inmueble. Lo paga el vendedor.",
     "Si vendiste un piso en Madrid comprado hace 10 años, el ayuntamiento calcula el incremento del valor del suelo y cobra un porcentaje de ese incremento.",
     ["Pensar que la paga el comprador: la paga siempre el vendedor.",
      "No comprobar si ha habido pérdida en la venta: desde la sentencia del Tribunal Constitucional de 2021, si no hay incremento de valor real, no se debe pagar este impuesto.",
      "Confundirla con la ganancia patrimonial del IRPF: son impuestos distintos y compatibles entre sí."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Revisa los gastos asociados a vender vivienda"),

    ("ibi-impuesto-bienes-inmuebles", "IBI (Impuesto sobre Bienes Inmuebles)", "fiscalidad",
     "Impuesto municipal anual que paga el propietario de un inmueble. Se calcula aplicando un tipo (entre 0,4% y 1,1%) sobre el valor catastral.",
     "Un piso con valor catastral de 90.000€ en un municipio con tipo del 0,5% tiene un IBI de 450€/año (37,5€/mes).",
     ["No comprobar el valor catastral actualizado antes de comprar: puede haber subido tras una revisión catastral reciente.",
      "Olvidar que en el año de la compra, el pago del IBI se suele prorratear entre comprador y vendedor según lo acordado.",
      "Pensar que el tipo es igual en todos los municipios: cada ayuntamiento fija el suyo dentro del rango legal (0,4%-1,1%)."],
     "/ranking.html", "El IBI ya está incluido en el cálculo de rentabilidad neta del ranking"),

    ("irpf-alquiler", "IRPF alquiler", "fiscalidad",
     "Los ingresos por alquiler tributan en el IRPF como rendimientos del capital inmobiliario. Hay una reducción del 60% si es vivienda habitual del inquilino.",
     "Si cobras 10.000€/año de alquiler residencial y tienes 3.000€ de gastos deducibles, el rendimiento neto es 7.000€. Con la reducción del 60%, solo tributas por 2.800€.",
     ["Olvidar aplicar la reducción del 60% si el inquilino lo usa como vivienda habitual, pagando más impuestos de los necesarios.",
      "No declarar gastos deducibles reales (IBI, comunidad, seguros, intereses de hipoteca), reduciendo el rendimiento neto a declarar.",
      "Confundir el alquiler de vivienda habitual (con reducción) con el alquiler turístico o de temporada (sin esa reducción)."],
     "/simulador-comprar-vs-alquilar.html", "Simula el impacto fiscal de alquilar vs comprar"),

    ("irav", "IRAV (Índice de Referencia de Arrendamientos de Vivienda)", "fiscalidad",
     "El IRAV es el índice que desde 2025 sustituye al IPC para actualizar anualmente las rentas de los contratos de alquiler de vivienda en España. Lo publica el INE cada mes, con el objetivo de evitar subidas de alquiler superiores a la evolución real de salarios y mercado.",
     "El IRAV de referencia para actualizaciones en julio de 2026 (dato INE de mayo de 2026) es del 2,48%. Un alquiler de 900€/mes se actualizaría a 900 × 1,0248 = 922€/mes (+22€), en lugar de aplicar el IPC general, que suele ser más alto.",
     ["Confundir el IRAV con el IPC general: algunos propietarios siguen aplicando el IPC por desconocimiento, algo no ajustado a la normativa vigente para los contratos afectados.",
      "Pensar que el IRAV es un valor fijo: cambia cada mes, hay que consultar el dato del INE correspondiente a la fecha exacta de revisión del contrato.",
      "Aplicar el IRAV a contratos firmados antes de la entrada en vigor de la Ley de Vivienda sin revisar si tienen una cláusula de actualización distinta pactada."],
     "/actualidad-ley-vivienda-2026.html", "Lee el análisis completo de la Ley de Vivienda 2026"),

    ("euribor", "Euríbor", "hipotecas",
     "Euro Interbank Offered Rate. Tipo de interés al que los bancos europeos se prestan dinero entre sí. Referencia principal de las hipotecas variables en España.",
     "Si tienes una hipoteca variable a Euríbor + 1% y el Euríbor está al 3,2%, tu tipo de interés total es del 4,2%.",
     ["Pensar que la hipoteca se actualiza con el valor del euríbor del día: los bancos suelen usar la media mensual del mes anterior a la revisión.",
      "No comprobar el diferencial (el % que se suma al euríbor), que puede variar mucho entre bancos aunque el euríbor sea el mismo.",
      "Asumir que el euríbor solo sube: ha tenido periodos negativos (2016-2022) y de fuerte subida (2022-2023)."],
     "/actualidad-euribor-julio-2026.html", "Consulta la evolución actual del euríbor"),

    ("hipoteca-fija", "Hipoteca fija", "hipotecas",
     "Hipoteca con tipo de interés constante durante toda la vida del préstamo. La cuota mensual no varía.",
     "Una hipoteca fija al 3,2% a 25 años de 160.000€ tiene una cuota de ~775€/mes que nunca cambia.",
     ["Pensar que la fija siempre es más cara que la variable: depende del diferencial de la variable y del momento del ciclo del euríbor.",
      "No comparar la TAE entre ofertas fijas, que pueden incluir comisiones distintas por vinculación de productos.",
      "Olvidar que cancelar anticipadamente una hipoteca fija puede tener una comisión distinta a la de una variable."],
     "/hipoteca-fija-vs-variable-2026.html", "Compara hipoteca fija vs variable con datos reales"),

    ("hipoteca-variable", "Hipoteca variable", "hipotecas",
     "Hipoteca cuyo tipo de interés se revisa periódicamente (normalmente anual) según el euríbor más un diferencial.",
     "Una hipoteca Euríbor + 0,8% en 2021 con Euríbor negativo podía estar al 0,5%. En 2024 con Euríbor al 3,5%, el tipo subía al 4,3%.",
     ["No simular cómo afectaría una subida fuerte del euríbor a la cuota mensual antes de firmar.",
      "Pensar que la revisión siempre es anual: algunos bancos revisan semestralmente.",
      "Olvidar el diferencial al comparar ofertas, fijándose solo en si el euríbor está \"bajo\" en ese momento."],
     "/hipoteca-fija-vs-variable-2026.html", "Compara hipoteca fija vs variable con datos reales"),

    ("ltv-loan-to-value", "LTV (Loan to Value)", "hipotecas",
     "Porcentaje que representa el importe del préstamo sobre el valor de tasación. Los bancos suelen financiar hasta el 80% (LTV 80%).",
     "Si compras un piso tasado en 200.000€ y el banco te da el 80%, el préstamo es de 160.000€ (LTV=80%). Necesitas aportar los 40.000€ restantes más gastos.",
     ["Pensar que el banco financia siempre el 80%: puede ser menor según el perfil de riesgo o mayor con avales (ICO, familiares).",
      "Calcular el LTV sobre el precio de compra en vez de sobre la tasación: el banco usa el menor de los dos valores.",
      "No presupuestar que, aunque el LTV sea del 80%, aún hay que cubrir los gastos de compra (8-10% adicional)."],
     "/calculadora-hipoteca.html", "Calcula tu cuota según el LTV con la calculadora Ren Data"),

    ("tin-vs-tae", "TIN vs TAE", "hipotecas",
     "El TIN (Tipo de Interés Nominal) es el tipo de interés puro de la hipoteca, sin incluir comisiones ni gastos. La TAE (Tasa Anual Equivalente) incluye además comisiones, gastos y la periodicidad de las cuotas, reflejando el coste real total del préstamo. La TAE siempre es igual o mayor que el TIN.",
     "Una hipoteca con TIN del 3,0% y una comisión de apertura del 0,5% más gastos de estudio puede tener una TAE del 3,25%. Al comparar dos ofertas, la que tiene el TIN más bajo no siempre es la más barata: hay que comparar siempre la TAE.",
     ["Comparar hipotecas solo por el TIN, ignorando la TAE, donde suelen aparecer las comisiones reales.",
      "No tener en cuenta que la TAE de una hipoteca variable es una estimación (parte del euríbor actual), no un dato fijo para toda la vida del préstamo.",
      "Olvidar que los seguros vinculados obligatorios (vida, hogar) no siempre están incluidos en el cálculo de la TAE publicitada."],
     "/calculadora-hipoteca.html", "Compara TIN y TAE con la calculadora de hipoteca"),

    ("aval-ico", "Aval ICO vivienda", "hipotecas",
     "El Aval ICO Vivienda es una garantía pública del Instituto de Crédito Oficial que cubre hasta el 20% (25% con menores a cargo) del valor de tasación de una vivienda, permitiendo financiar hasta el 100% del precio sin aportar la entrada tradicional. Dirigido a menores de 35 años o familias con menores a cargo, con límites de ingresos y patrimonio.",
     "Un piso de 200.000€ normalmente requiere un 20% de entrada (40.000€) más gastos. Con el Aval ICO, el banco puede financiar el 100% del precio (200.000€), dejando al comprador solo los gastos de compra (8-10%, unos 16.000-20.000€) a cubrir con ahorros.",
     ["Pensar que el aval cubre también los gastos de compra (ITP/IVA, notaría, registro): solo cubre el porcentaje de financiación de la vivienda, no los gastos asociados.",
      "No comprobar el límite de precio máximo por zona ICO antes de buscar piso (varía entre 175.000€ y 250.000€ según el municipio).",
      "Superar sin saberlo el límite de patrimonio neto o de ingresos (4,5 veces el IPREM), lo que descarta la solicitud."],
     "/aval-ico-primera-vivienda-2026.html", "Guía completa del Aval ICO: requisitos, bancos y zonas"),

    ("cap-rate", "Cap Rate", "inversion",
     "Capitalización Rate. Ratio entre el Beneficio Operativo Neto (NOI) y el valor de mercado del inmueble. Muy usado en inversión profesional.",
     "Un edificio con NOI de 60.000€/año y valor de 1.000.000€ tiene un cap rate del 6%.",
     ["Confundirlo con el ROI o la rentabilidad bruta: el cap rate usa el NOI (ingresos menos gastos operativos), no solo el alquiler bruto.",
      "Aplicarlo sin ajustar por vacancia o gastos reales, sobreestimando la rentabilidad del activo.",
      "Comparar cap rates de mercados distintos sin tener en cuenta el riesgo y la liquidez de cada zona."],
     "/ranking.html", "Consulta ingresos y gastos estimados por ciudad en el ranking"),

    ("yield", "Yield", "inversion",
     "Término anglosajón equivalente a rentabilidad. El yield bruto es el porcentaje de ingresos por alquiler sobre el precio de compra.",
     "Un inmueble con yield del 7% genera 7€ de alquiler anual por cada 100€ de precio de compra.",
     ["Confundir yield bruto con yield neto (después de gastos): son cifras muy diferentes y ambas se usan indistintamente en muchos anuncios.",
      "No tener en cuenta la vacancia o los meses sin inquilino al calcular el yield esperado.",
      "Comparar el yield de vivienda con el de otros activos (bonos, SOCIMIs) sin ajustar por riesgo y liquidez."],
     "/ranking.html", "Compara el yield bruto y neto de 587 ciudades"),

    ("cash-flow", "Cash flow", "inversion",
     "Flujo de caja neto mensual o anual que genera un inmueble, después de pagar la hipoteca y todos los gastos.",
     "Un piso con alquiler de 900€/mes, hipoteca de 550€ y gastos de 100€ genera un cash flow positivo de 250€/mes.",
     ["Olvidar incluir gastos no mensuales (IBI anual, seguros, mantenimiento) al calcular el cash flow mensual real.",
      "No provisionar para periodos de vacancia (piso vacío) o impagos, que reducen el cash flow medio anual.",
      "Confundir cash flow positivo con rentabilidad: un piso puede tener cash flow positivo y aun así rentabilidad baja si el apalancamiento es muy alto."],
     "/simulador-comprar-vs-alquilar.html", "Simula tu cash flow con la calculadora Ren Data"),

    ("apalancamiento-inmobiliario", "Apalancamiento inmobiliario", "inversion",
     "Uso de deuda (hipoteca) para comprar un activo mayor del que se podría adquirir con capital propio, amplificando el retorno sobre el capital invertido.",
     "Con 50.000€ propios puedes comprar un piso de 200.000€ (apalancamiento 4:1). Si el piso sube un 5%, ganas 10.000€ sobre 50.000€ = 20% de retorno sobre tu capital, no el 5%.",
     ["Pensar que más apalancamiento siempre es mejor: amplifica tanto las ganancias como las pérdidas si el precio cae.",
      "No tener en cuenta que un cash flow negativo con apalancamiento alto puede forzar una venta en mal momento.",
      "Olvidar que el apalancamiento también aumenta el riesgo si sube el tipo de interés en hipotecas variables."],
     "/guia-inversor.html", "Lee la guía del inversor Ren Data"),

    ("socimi", "SOCIMI", "inversion",
     "Sociedad Cotizada de Inversión en el Mercado Inmobiliario. Equivalente español a los REITs anglosajones. Permite invertir en inmobiliario a través de bolsa.",
     "Merlin Properties o Colonial son SOCIMIs cotizadas en el IBEX. Permiten invertir en inmobiliario desde 1€ de forma líquida, recibiendo dividendos del 80% de sus beneficios.",
     ["Pensar que invertir en una SOCIMI es lo mismo que ser propietario directo de un inmueble: se compra liquidez y diversificación, no control sobre activos concretos.",
      "No comprobar la política de dividendos: aunque reparten al menos el 80% del beneficio, la cotización puede fluctuar como cualquier acción.",
      "Confundir SOCIMI con fondos de inversión inmobiliaria tradicionales: la SOCIMI cotiza en bolsa y tiene liquidez diaria, el fondo no siempre."],
     "/guia-inversor.html", "Lee la guía del inversor Ren Data"),

    ("zona-tensionada-alquiler", "Zona tensionada de alquiler", "inversion",
     "Área declarada oficialmente con mercado residencial tensionado. Permite limitar las subidas de alquiler y aplicar regulación de precios.",
     "Cataluña fue la primera CCAA en declarar zonas tensionadas. En estas zonas, los grandes propietarios tienen limitaciones adicionales para subir el precio del alquiler.",
     ["Pensar que la declaración aplica igual en toda España: cada comunidad autónoma decide si se acoge y qué zonas concretas declara.",
      "No comprobar si el propietario es \"gran tenedor\" (varias viviendas), ya que las limitaciones son más estrictas en ese caso.",
      "Asumir que el alquiler no puede subir nada: existen límites, no una congelación total, y varían según el contrato previo."],
     "/actualidad-ley-vivienda-2026.html", "Lee el análisis completo de la Ley de Vivienda 2026"),

    ("arras", "Arras", "proceso-compra",
     "El contrato de arras es un acuerdo previo a la escritura de compraventa en el que comprador y vendedor se comprometen a formalizar la operación, entregando el comprador una señal (habitualmente el 10% del precio) como garantía. Si el comprador se echa atrás, pierde la señal; si es el vendedor quien incumple, debe devolver el doble (arras penitenciales, las más habituales).",
     "En la compra de un piso de 150.000€, es habitual firmar arras por 15.000€ (10%). Si el comprador decide no seguir adelante, pierde esos 15.000€. Si el vendedor se retracta, debe devolver 30.000€ (el doble de la señal).",
     ["Firmar arras sin cláusula de \"sujeto a financiación\", perdiendo la señal si el banco deniega la hipoteca.",
      "Confundir arras penitenciales (las habituales, permiten desistir perdiendo o devolviendo el doble de la señal) con arras confirmatorias o penales, que tienen consecuencias legales distintas.",
      "No fijar un plazo claro para la firma de escritura, lo que genera disputas sobre incumplimiento."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Revisa todos los gastos del proceso de compra"),

    ("nota-simple-registral", "Nota simple registral", "proceso-compra",
     "Documento del Registro de la Propiedad que informa sobre el titular, cargas, hipotecas y limitaciones de un inmueble. Cuesta 9,02€.",
     "La nota simple te dice si el vendedor es realmente el propietario, si hay hipotecas pendientes, embargos, servidumbres u otras cargas que afectan al inmueble.",
     ["Pensar que la nota simple certifica que no hay ningún problema: solo refleja lo que consta inscrito en el Registro, no situaciones no registradas.",
      "No pedirla justo antes de firmar: puede haber cambios (nuevas cargas) entre la primera consulta y la firma.",
      "Confundirla con la escritura pública: la nota simple es solo informativa, no un documento con validez notarial."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Revisa todos los gastos del proceso de compra"),

    ("cedula-de-habitabilidad", "Cédula de habitabilidad", "proceso-compra",
     "Documento que acredita que una vivienda cumple las condiciones mínimas de habitabilidad según la normativa autonómica. Obligatoria en Cataluña, Baleares y otras CCAA.",
     "En Cataluña no puedes vender ni alquilar una vivienda sin cédula de habitabilidad vigente. Su obtención requiere inspección y tiene un coste de entre 80€ y 200€.",
     ["Pensar que es obligatoria en toda España: solo lo es en algunas CCAA (Cataluña, Baleares y otras), no en Madrid, por ejemplo.",
      "Olvidar renovarla si ha caducado (suele tener vigencia de 15 años) antes de vender o alquilar.",
      "Confundirla con la licencia de primera ocupación, que es un documento distinto para vivienda de nueva construcción."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Consulta los trámites según tu comunidad autónoma"),

    ("nuda-propiedad", "Nuda propiedad", "proceso-compra",
     "La nuda propiedad es la titularidad de un inmueble sin el derecho de uso y disfrute (usufructo), que pertenece a otra persona, normalmente durante su vida (usufructo vitalicio). El nudo propietario recupera la plena propiedad al extinguirse el usufructo, habitualmente al fallecimiento del usufructuario.",
     "Una persona de 75 años vende la nuda propiedad de su vivienda valorada en 200.000€ reservándose el usufructo vitalicio. Según las tablas de valoración fiscal (que restan un 1% del valor por cada año por encima de 19, con un mínimo del 10%), el comprador de la nuda propiedad paga solo una parte del precio de mercado, sin poder usar la vivienda hasta la extinción del usufructo.",
     ["Pensar que comprar la nuda propiedad da derecho a vivir en la vivienda o alquilarla: mientras exista usufructo, ese derecho es solo del usufructuario.",
      "No calcular bien el valor fiscal del usufructo (depende de la edad del usufructuario según las tablas de la Agencia Tributaria), lo que afecta directamente al ITP a pagar.",
      "Olvidar que el nudo propietario suele asumir gastos estructurales e IBI, aunque no pueda usar la vivienda mientras dure el usufructo."],
     "/guia-inversor.html", "Lee la guía del inversor Ren Data"),

    ("precio-de-tasacion", "Precio de tasación", "proceso-compra",
     "Valor oficial de un inmueble determinado por un tasador homologado por el Banco de España. Los bancos lo usan para calcular la hipoteca.",
     "Si la tasación es de 200.000€ y el banco financia el 80%, prestará un máximo de 160.000€, independientemente del precio de compra.",
     ["Pensar que el banco financia sobre el precio de compra: siempre financia sobre el menor de los dos valores (compra o tasación).",
      "No comparar tasaciones de distintas entidades: pueden variar significativamente entre tasadoras.",
      "Olvidar que la tasación tiene un coste (habitualmente entre 250€ y 600€) que corre a cargo del comprador."],
     "/calculadora-hipoteca.html", "Simula tu hipoteca según el valor de tasación"),

    ("licencia-primera-ocupacion", "Licencia de primera ocupación", "proceso-compra",
     "Autorización municipal que certifica que un edificio nuevo cumple la normativa y puede habitarse. Imprescindible para registrar el suministro de servicios.",
     "Sin licencia de primera ocupación no puedes darte de alta en agua, luz y gas. Es el documento que confirma la legalidad de una vivienda nueva.",
     ["Pensar que se puede ocupar la vivienda nueva sin ella: sin esta licencia no se pueden dar de alta los suministros.",
      "Confundirla con la cédula de habitabilidad, que es un documento autonómico distinto (y solo obligatorio en algunas CCAA).",
      "No comprobar con el promotor si está tramitada antes de firmar la compraventa de obra nueva."],
     "/gastos-comprar-piso-por-comunidad-2026.html", "Consulta los trámites de compra de vivienda nueva"),
]

CAT_LOOKUP = {c[0]: c for c in CATS}


def defined_term_ld(name, definition):
    esc = lambda s: s.replace('"', '\\"')
    return (
        '<script type="application/ld+json">{'
        f'"@context":"https://schema.org","@type":"DefinedTerm",'
        f'"name":"{esc(name)}","description":"{esc(definition)}",'
        f'"inDefinedTermSet":"https://rendata.es/academia"'
        '}</script>'
    )


def faq_ld(name, definition, example):
    esc = lambda s: s.replace('"', '\\"')
    return (
        '<script type="application/ld+json">{'
        '"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{'
        f'"@type":"Question","name":"¿Qué es {esc(name)}?",'
        '"acceptedAnswer":{"@type":"Answer","text":"' + esc(definition) + '"}'
        '},{'
        f'"@type":"Question","name":"¿Puedes poner un ejemplo de {esc(name)}?",'
        '"acceptedAnswer":{"@type":"Answer","text":"' + esc(example) + '"}'
        '}]}</script>'
    )


def build_term_page(slug, name, cat_key, definition, example, errores, cta_href, cta_text):
    cat_key2, icon, cat_label = CAT_LOOKUP[cat_key]
    others = [t for t in TERMS if t[2] == cat_key and t[0] != slug][:4]
    related_html = "".join(
        f'<a href="/academia/que-es-{o[0]}.html">{o[1]}</a>' for o in others
    )
    errores_html = "".join(f"<li>{e}</li>" for e in errores)
    title = f"¿Qué es {name}? Definición y ejemplo | Academia Ren Data"
    desc = definition if len(definition) <= 155 else definition[:152].rsplit(" ", 1)[0] + "…"
    canonical = f"https://rendata.es/academia/que-es-{slug}"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="¿Qué es {name}?">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="https://rendata.es/img/logo-rendata-transparente.png"><meta property="og:image:width" content="512"><meta property="og:image:height" content="512">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="¿Qué es {name}?">
<meta name="twitter:description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/academia.css">
<link rel="stylesheet" href="/css/nav.css">
<script src="/js/nav-dropdown.js" defer></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-0M57323B51");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6236025065305645" crossorigin="anonymous"></script>
{defined_term_ld(name, definition)}
{faq_ld(name, definition, example)}
</head>
<body>

<header>
  <a href="/" class="logo"><img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA"></a>
  {HEADER}
</header>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">Inicio</a>
  <span class="bc-sep">›</span>
  <a href="/academia.html">Academia</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">{name}</span>
</nav>

<article class="aca-art">
  <span class="aca-art-eyebrow">{icon} {cat_label}</span>
  <h1>¿Qué es {name}?</h1>

  <div class="aca-def-box">
    <strong>Definición:</strong> {definition}
  </div>

  <h2>📌 Ejemplo práctico</h2>
  <div class="aca-example">
    <span class="aca-example-label">Con números reales</span>
    <p style="margin:0">{example}</p>
  </div>

  <h2>⚠️ Errores comunes</h2>
  <div class="aca-errors">
    <span class="aca-errors-label">Lo que mucha gente hace mal</span>
    <ul>{errores_html}</ul>
  </div>

  <div class="aca-cta">
    <span class="aca-cta-ico">🛠️</span>
    <span><a href="{cta_href}">{cta_text} →</a></span>
  </div>

  <div class="aca-related">
    <div class="aca-related-title">Más términos de {cat_label.lower()}</div>
    <div class="aca-related-links">{related_html}
      <a href="/academia.html">Ver todos ↗</a>
    </div>
  </div>
</article>

<footer>
{FOOTER}
</footer>

</body>
</html>
"""
    return html


def build_index():
    total = len(TERMS)
    cat_sections = []
    for cat_key, icon, label in CATS:
        terms_in_cat = [t for t in TERMS if t[2] == cat_key]
        cards = "".join(
            f'<a href="/academia/que-es-{t[0]}.html" class="aca-card">'
            f'<div class="aca-card-q">Qué es</div>'
            f'<div class="aca-card-t">{t[1]}</div>'
            f'<div class="aca-card-d">{t[3]}</div>'
            f'</a>'
            for t in terms_in_cat
        )
        cat_sections.append(f"""
  <div class="aca-cat">
    <div class="aca-cat-head">
      <span class="aca-cat-ico">{icon}</span>
      <h2>{label}</h2>
      <span class="aca-cat-count">{len(terms_in_cat)} guías</span>
    </div>
    <div class="aca-grid">{cards}</div>
  </div>""")

    item_list = ",".join(
        f'{{"@type":"ListItem","position":{i+1},"name":"{t[1]}","url":"https://rendata.es/academia/que-es-{t[0]}"}}'
        for i, t in enumerate(TERMS)
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Academia Ren Data: {total} guías educativas sobre fiscalidad, hipotecas, inversión y proceso de compra de vivienda en España. Definiciones claras con ejemplos reales y errores comunes.">
<title>Academia Ren Data — Guías de Inversión Inmobiliaria | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="Academia Ren Data — {total} guías de inversión inmobiliaria">
<meta property="og:description" content="Conceptos básicos, fiscalidad, hipotecas, inversión y proceso de compra explicados con ejemplos reales.">
<meta property="og:url" content="https://rendata.es/academia"><meta property="og:image" content="https://rendata.es/img/logo-rendata-transparente.png"><meta property="og:image:width" content="512"><meta property="og:image:height" content="512">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Academia Ren Data">
<meta name="twitter:description" content="{total} guías de inversión inmobiliaria explicadas con ejemplos reales.">
<link rel="canonical" href="https://rendata.es/academia">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/academia.css">
<link rel="stylesheet" href="/css/nav.css">
<script src="/js/nav-dropdown.js" defer></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-0M57323B51");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6236025065305645" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Academia Ren Data","description":"Guías educativas sobre inversión inmobiliaria en España","url":"https://rendata.es/academia","hasPart":[{item_list}]}}</script>
</head>
<body>

<header>
  <a href="/" class="logo"><img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA"></a>
  {HEADER}
</header>

<section class="aca-hero">
  <div class="aca-hero-inner">
    <div class="aca-eyebrow">🎓 Academia Ren Data</div>
    <h1>Aprende a invertir en vivienda, término a término</h1>
    <p>{total} guías cortas sobre fiscalidad, hipotecas, inversión y proceso de compra. Cada una con definición clara, ejemplo con números reales y los errores más comunes que cometen los compradores.</p>
    <div class="aca-stats">
      <div class="aca-stat"><div class="aca-stat-val">{total}</div><div class="aca-stat-lbl">Guías educativas</div></div>
      <div class="aca-stat"><div class="aca-stat-val">5</div><div class="aca-stat-lbl">Categorías</div></div>
      <div class="aca-stat"><div class="aca-stat-val">587</div><div class="aca-stat-lbl">Ciudades con datos reales</div></div>
    </div>
  </div>
</section>

<div class="aca-wrap">
  <p style="font-size:.9rem;color:var(--muted);margin:-1rem 0 2rem">¿Buscas un término concreto? Prueba también el <a href="/glosario.html">glosario rápido</a> con más de 50 definiciones cortas.</p>
{"".join(cat_sections)}
</div>

<footer>
{FOOTER}
</footer>

</body>
</html>
"""
    return html


def main():
    academia_dir = BETA / "academia"
    academia_dir.mkdir(exist_ok=True)

    (BETA / "academia.html").write_text(build_index(), encoding="utf-8")
    print("Wrote academia.html")

    for slug, name, cat_key, definition, example, errores, cta_href, cta_text in TERMS:
        page = build_term_page(slug, name, cat_key, definition, example, errores, cta_href, cta_text)
        out = academia_dir / f"que-es-{slug}.html"
        out.write_text(page, encoding="utf-8")
    print(f"Wrote {len(TERMS)} mini-guides in academia/")


if __name__ == "__main__":
    main()
