"""Genera e inserta editoriales para las 22 ciudades andaluzas restantes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

CITIES = {
    "mairena-del-alcor": {
        "name": "Mairena del Alcor",
        "roi": "6,2%", "precio": "1.600€", "alquiler": "827€/mes", "dias": "23",
        "alts": [("rentabilidad-alcala-de-guadaira.html", "Alcalá de Guadaíra"), ("rentabilidad-carmona.html", "Carmona")],
        "paragraphs": [
            "<p>Mairena del Alcor pertenece a la comarca de Los Alcores sevillana, un eje residencial entre Sevilla capital y Carmona que ha experimentado un crecimiento sostenido en la última década. La ciudad combina identidad local fuerte (la Feria de Abril mairenera, el Castillo de Luna) con un tejido económico de servicios y agricultura. El precio medio es de <strong>1.600€/m²</strong> y la <strong>rentabilidad bruta del 6,2%</strong> ofrece un equilibrio razonable entre yield y entrada moderada.</p>",
            "<p>El inquilino tipo es una familia joven que trabaja en Sevilla pero busca vivienda más amplia y asequible a 25 km de la capital. El alquiler medio (<strong>827€/mes</strong>) y los <strong>23 días</strong> de absorción confirman demanda fluida. Zonas con tracción: <strong>El Patriarca, El Calvario y entorno del Castillo</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso de 3 dormitorios o adosado para alquiler familiar, aprovechando la migración Sevilla→corona metropolitana.</p>",
            ["Los Alcores", "Área metropolitana Sevilla", "Familias jóvenes", "Adosados"],
        ],
    },
    "mairena-del-aljarafe": {
        "name": "Mairena del Aljarafe",
        "roi": "5,9%", "precio": "1.800€", "alquiler": "884€/mes", "dias": "21",
        "alts": [("rentabilidad-bormujos.html", "Bormujos"), ("rentabilidad-tomares.html", "Tomares")],
        "paragraphs": [
            "<p>Mairena del Aljarafe es uno de los municipios más poblados del cinturón metropolitano de Sevilla, integrado en el eje Bormujos-Tomares-Castilleja, con un perfil claramente residencial de clase media. La cercanía a Sevilla por la SE-30 y el Metro Línea 1 — con cabecera en Ciudad Expo — han disparado la demanda. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,9%</strong>.</p>",
            "<p>El alquiler medio (<strong>884€/mes</strong>) y los <strong>21 días</strong> de absorción reflejan un mercado tensionado, de los más rápidos del Aljarafe. La demanda procede de familias jóvenes y profesionales del sector servicios sevillano. Zonas: <strong>Ciudad Aljarafe, Lepanto y entorno del Metro</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: pisos de 2-3 dormitorios bien conectados al Metro, donde la combinación de yield estable y revalorización por demanda creciente es óptima.</p>",
            ["Aljarafe", "Metro Sevilla", "Residencial premium", "Mercado tensionado"],
        ],
    },
    "marchena": {
        "name": "Marchena",
        "roi": "6,8%", "precio": "900€", "alquiler": "510€/mes", "dias": "27",
        "alts": [("rentabilidad-osuna.html", "Osuna"), ("rentabilidad-ecija.html", "Écija")],
        "paragraphs": [
            "<p>Marchena es una ciudad media de la campiña sevillana con un patrimonio histórico notable (las murallas almohades, la iglesia de San Juan Bautista) y una economía agraria centrada en el olivar y el cereal. El precio medio (<strong>900€/m²</strong>) la sitúa entre los mercados más baratos de la provincia, con una <strong>rentabilidad bruta del 6,8%</strong> claramente superior a la media nacional. Alquiler medio: <strong>510€/mes</strong>.</p>",
            "<p>El inquilino habitual es local: trabajadores del olivar, agroindustria y servicios comarcales. Los <strong>27 días</strong> de absorción reflejan el ritmo pausado típico de plaza interior, pero con demanda estructural sostenida por una economía agraria estable. Zonas: <strong>casco histórico, La Soledad y el ensanche</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: comprar muy barato (vivienda completa por menos de 65.000€ es factible) con yield alto, asumiendo menor revalorización pero cash-flow muy estable.</p>",
            ["Campiña sevillana", "Olivar", "Yield alto", "Cash-flow"],
        ],
    },
    "martos": {
        "name": "Martos",
        "roi": "6,8%", "precio": "900€", "alquiler": "510€/mes", "dias": "28",
        "alts": [("rentabilidad-jaen.html", "Jaén"), ("rentabilidad-alcala-la-real.html", "Alcalá la Real")],
        "paragraphs": [
            "<p>Martos es la capital mundial del aceite de oliva por volumen de producción (más de 5 millones de olivos en su término municipal) y la segunda ciudad de Jaén, con un tejido industrial vinculado al sector (almazaras, envasado, maquinaria agrícola) y la planta de Valeo. El precio medio (<strong>900€/m²</strong>) es de los más bajos de Andalucía y entrega una <strong>rentabilidad bruta del 6,8%</strong>.</p>",
            "<p>La demanda de alquiler procede de trabajadores industriales (Valeo emplea a más de 1.000 personas) y del sector oleícola. El alquiler medio (<strong>510€/mes</strong>) y los <strong>28 días</strong> de absorción muestran un mercado pausado pero con demanda apoyada en empleo industrial estable. Zonas: <strong>centro, Polígono y La Veleta</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: vivienda funcional para alquiler residencial con yield superior, en una plaza con motor industrial real más allá del olivar.</p>",
            ["Sierra Sur de Jaén", "Capital del aceite", "Industrial Valeo", "Yield alto"],
        ],
    },
    "mojacar": {
        "name": "Mojácar",
        "roi": "5,6%", "precio": "2.800€", "alquiler": "1.307€/mes", "dias": "19",
        "alts": [("rentabilidad-vera.html", "Vera"), ("rentabilidad-roquetas-de-mar.html", "Roquetas de Mar")],
        "paragraphs": [
            "<p>Mojácar es uno de los iconos turísticos del Levante almeriense, con su pueblo blanco encaramado en la sierra y 17 km de playas vírgenes en Mojácar Playa. La fuerte presencia de comunidad británica, irlandesa y nórdica desde los años 60 ha consolidado un mercado residencial-turístico premium. Precio medio: <strong>2.800€/m²</strong> — el más alto del grupo — y <strong>rentabilidad bruta del 5,6%</strong>, típica de plaza turística madura.</p>",
            "<p>El alquiler medio supera los <strong>1.307€/mes</strong> en residencial y los <strong>19 días</strong> de absorción confirman un mercado muy líquido. La explotación VUT en Mojácar Playa ofrece yields combinados muy superiores. Zonas: <strong>Mojácar Pueblo (turismo cultural), Mojácar Playa norte y Marina de la Torre</strong>. ITP Andalucía: <strong>7%</strong>. Tesis ganadora: VUT registrada en zona playa para combinar yield estacional alto con apreciación a medio plazo, apoyada en demanda extranjera estructural.</p>",
            ["Levante almeriense", "Turismo premium", "Comunidad extranjera", "VUT alto rendimiento"],
        ],
    },
    "montilla": {
        "name": "Montilla",
        "roi": "6,8%", "precio": "1.000€", "alquiler": "567€/mes", "dias": "27",
        "alts": [("rentabilidad-lucena.html", "Lucena"), ("rentabilidad-cordoba.html", "Córdoba")],
        "paragraphs": [
            "<p>Montilla es la capital del vino Montilla-Moriles, una de las denominaciones de origen más antiguas de España, con bodegas centenarias (Alvear, Pérez Barquero) y un patrimonio agroindustrial vinculado al vino y al aceite. La ciudad combina identidad cultural fuerte con economía estable. El precio medio (<strong>1.000€/m²</strong>) es muy contenido y entrega una <strong>rentabilidad bruta del 6,8%</strong>, de las más altas de la región.</p>",
            "<p>El inquilino tipo es local: trabajadores del sector vinícola, agroindustria y servicios comarcales (Montilla es cabecera de la Campiña Sur cordobesa). El alquiler medio (<strong>567€/mes</strong>) y los <strong>27 días</strong> de absorción muestran un mercado sólido aunque pausado. Zonas: <strong>centro histórico, Llano de Palacio y barrio de la Cruz</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: ticket muy bajo con yield alto, ideal para construir cartera diversificada en interior andaluz con cash-flow estable.</p>",
            ["Campiña Sur de Córdoba", "Vino Montilla-Moriles", "Cabecera comarcal", "Yield alto"],
        ],
    },
    "moron-de-la-frontera": {
        "name": "Morón de la Frontera",
        "roi": "6,8%", "precio": "1.100€", "alquiler": "623€/mes", "dias": "27",
        "alts": [("rentabilidad-utrera.html", "Utrera"), ("rentabilidad-marchena.html", "Marchena")],
        "paragraphs": [
            "<p>Morón de la Frontera es una ciudad media de la Sierra Sur sevillana, con un perfil económico singular: combina agricultura olivarera tradicional con la presencia de la <strong>Base Aérea de Morón</strong> (operada conjuntamente por el Ejército del Aire español y la USAF), que sostiene un volumen importante de empleo militar y civil. Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>.</p>",
            "<p>La demanda de alquiler tiene un componente único: personal militar estadounidense rotatorio, que busca residencias amuebladas con contratos cortos y precios premium. A esto se suma la demanda local de trabajadores agrícolas y servicios. Alquiler medio: <strong>623€/mes</strong>; <strong>27 días</strong> de absorción. Zonas: <strong>centro, La Atalaya y entorno de la Base</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: vivienda amueblada para alquiler temporal a personal de la Base, con yields significativamente superiores a la media del residencial estándar.</p>",
            ["Sierra Sur sevillana", "Base Aérea Morón", "Alquiler temporal premium", "Yield alto"],
        ],
    },
    "osuna": {
        "name": "Osuna",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "595€/mes", "dias": "27",
        "alts": [("rentabilidad-ecija.html", "Écija"), ("rentabilidad-marchena.html", "Marchena")],
        "paragraphs": [
            "<p>Osuna es una ciudad histórica ducal de la campiña sevillana, conocida por su Colegiata renacentista, su Universidad (sede de la US y la UNED) y por haber acogido rodajes de Juego de Tronos en su plaza de toros. El tejido económico combina servicios universitarios, agroindustria olivarera y un creciente turismo cultural. Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>595€/mes</strong>.</p>",
            "<p>La demanda de alquiler es estable: estudiantes universitarios, profesores destinados, trabajadores agrícolas y un nicho de profesionales sanitarios del Hospital de la Merced. Los <strong>27 días</strong> de absorción reflejan el ritmo pausado de plaza pequeña pero con motor universitario. Zonas: <strong>centro histórico (regulado), San Pedro y entorno universitario</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso pequeño para alquiler estudiantil de septiembre a junio, complementado con VUT puntual de fines de semana culturales.</p>",
            ["Campiña sevillana", "Universitaria", "Patrimonio ducal", "Mixto residencial/VUT"],
        ],
    },
    "palma-del-rio": {
        "name": "Palma del Río",
        "roi": "6,8%", "precio": "900€", "alquiler": "510€/mes", "dias": "27",
        "alts": [("rentabilidad-ecija.html", "Écija"), ("rentabilidad-cordoba.html", "Córdoba")],
        "paragraphs": [
            "<p>Palma del Río se encuentra en la confluencia del Genil y el Guadalquivir, en el oeste de Córdoba, y es la capital española del cultivo de la naranja, además de tener un tejido agroindustrial diversificado (cítricos, hortícolas, conservas). La ciudad fue además base de los Vascos del Califato y conserva un patrimonio histórico relevante. Precio medio: <strong>900€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>.</p>",
            "<p>La demanda de alquiler procede de trabajadores agrícolas (con picos estacionales por la campaña de la naranja), agroindustria y servicios comarcales. Alquiler medio: <strong>510€/mes</strong>; <strong>27 días</strong> de absorción. Zonas: <strong>centro, Las Mercedes y la Veracruz</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: tickets muy bajos con yields altos, en una ciudad con economía agraria diversificada y cierta protección frente a fluctuaciones de un solo cultivo. Atractivo para inversor rentista.</p>",
            ["Vega del Guadalquivir", "Capital de la naranja", "Agroindustria", "Yield alto"],
        ],
    },
    "priego-de-cordoba": {
        "name": "Priego de Córdoba",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "542€/mes", "dias": "27",
        "alts": [("rentabilidad-cabra.html", "Cabra"), ("rentabilidad-lucena.html", "Lucena")],
        "paragraphs": [
            "<p>Priego de Córdoba es una de las joyas barrocas de Andalucía, con conjuntos como la Fuente del Rey y el Barrio de la Villa, y la cuna del aceite con DOP Priego (uno de los aceites más premiados del mundo). La ciudad combina patrimonio cultural con olivar de altísima calidad y un sector textil tradicional. Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>.</p>",
            "<p>La demanda de alquiler proviene de trabajadores del olivar, almazaras, sector textil y servicios. El turismo cultural — sostenido y de calidad — abre la puerta a explotación VUT en el centro histórico, especialmente en los famosos balcones del Adarve. Alquiler medio: <strong>542€/mes</strong>; <strong>27 días</strong> de absorción. Zonas: <strong>casco histórico, El Llano y entorno del centro</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: vivienda con potencial VUT en zona barroca + residencial estable, dual interesante.</p>",
            ["Subbética cordobesa", "Barroco", "DOP Priego", "Mixto residencial/VUT"],
        ],
    },
    "rincon-de-la-victoria": {
        "name": "Rincón de la Victoria",
        "roi": "5,6%", "precio": "2.000€", "alquiler": "933€/mes", "dias": "22",
        "alts": [("rentabilidad-malaga.html", "Málaga"), ("rentabilidad-velez-malaga.html", "Vélez-Málaga")],
        "paragraphs": [
            "<p>Rincón de la Victoria es un municipio costero del área metropolitana oriental de Málaga, conurbado con la capital y con uno de los crecimientos demográficos más altos de la provincia. Combina playa urbana, residencial de clase media y conexión directa con Málaga por la N-340 y la línea de cercanías. Precio medio: <strong>2.000€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>, típica de plaza costera-residencial premium.</p>",
            "<p>El inquilino tipo es residencial permanente: familias y profesionales que trabajan en Málaga capital y valoran la combinación de playa + ciudad. El alquiler medio (<strong>933€/mes</strong>) y los <strong>22 días</strong> de absorción confirman demanda estructural fuerte. Zonas: <strong>Torre de Benagalbón, La Cala del Moral y centro</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso de 2-3 dormitorios para alquiler residencial estable, con apreciación apoyada en presión demográfica metropolitana.</p>",
            ["Costa del Sol oriental", "Área metropolitana Málaga", "Residencial premium", "Cercanías"],
        ],
    },
    "roquetas-de-mar": {
        "name": "Roquetas de Mar",
        "roi": "6,4%", "precio": "1.600€", "alquiler": "853€/mes", "dias": "22",
        "alts": [("rentabilidad-el-ejido.html", "El Ejido"), ("rentabilidad-adra.html", "Adra")],
        "paragraphs": [
            "<p>Roquetas de Mar es el segundo municipio más poblado de la provincia de Almería y un nodo turístico-residencial que combina turismo internacional (Aguadulce, Urbanización), agricultura intensiva bajo plástico y un sector servicios robusto. El crecimiento poblacional sostenido — entre los más altos de España en las últimas décadas — apoya la demanda. Precio medio: <strong>1.600€/m²</strong>; <strong>rentabilidad bruta 6,4%</strong>.</p>",
            "<p>La demanda de alquiler es muy diversa: trabajadores agrícolas, residentes europeos jubilados, turismo familiar y profesionales del sector servicios. El alquiler medio (<strong>853€/mes</strong>) y los <strong>22 días</strong> de absorción muestran mercado tensionado. Zonas: <strong>Aguadulce, El Parador y Urbanización Roquetas</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: pisos para alquiler residencial todo el año en El Parador o VUT estacional en Aguadulce, según perfil de inversor.</p>",
            ["Poniente almeriense", "Turismo + agricultura", "Crecimiento sostenido", "Mixto"],
        ],
    },
    "rota": {
        "name": "Rota",
        "roi": "5,8%", "precio": "1.800€", "alquiler": "870€/mes", "dias": "22",
        "alts": [("rentabilidad-el-puerto-de-santa-maria.html", "El Puerto de Santa María"), ("rentabilidad-chipiona.html", "Chipiona")],
        "paragraphs": [
            "<p>Rota es una plaza costera muy singular de la Costa de la Luz gaditana: combina playas urbanas (La Costilla, El Rompidillo) con la <strong>Base Naval de Rota</strong>, operada conjuntamente por la Armada española y la US Navy. El componente militar internacional sostiene una demanda de alquiler atípica y muy estable. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>870€/mes</strong>.</p>",
            "<p>La demanda combina turismo familiar nacional, residencial permanente y un nicho premium de personal militar estadounidense que busca vivienda amueblada con contratos de 2-3 años y precios por encima de mercado. Los <strong>22 días</strong> de absorción confirman demanda fuerte. Zonas: <strong>Costa Ballena, El Rompidillo y centro</strong>. ITP Andalucía: <strong>7%</strong>. Tesis ganadora: vivienda amueblada en zonas próximas a la base, segmentada al inquilino militar internacional con yields premium.</p>",
            ["Costa de la Luz", "Base Naval Rota", "Alquiler militar premium", "Demanda estable"],
        ],
    },
    "san-fernando-cadiz": {
        "name": "San Fernando",
        "roi": "5,8%", "precio": "1.500€", "alquiler": "720€/mes", "dias": "22",
        "alts": [("rentabilidad-cadiz.html", "Cádiz"), ("rentabilidad-chiclana-de-la-frontera.html", "Chiclana")],
        "paragraphs": [
            "<p>San Fernando — la histórica Isla de León — ocupa una posición central en la Bahía de Cádiz, con el Arsenal de la Carraca y la Escuela Naval Militar como motores económicos clave. La conurbación con Cádiz, Chiclana y Puerto Real configura una de las áreas urbanas más densas de Andalucía. Precio medio: <strong>1.500€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>720€/mes</strong>.</p>",
            "<p>La demanda de alquiler es estructural y diversa: personal de la Armada, funcionarios, estudiantes del campus de la UCA y trabajadores del astillero. Los <strong>22 días</strong> de absorción confirman un mercado dinámico. Zonas: <strong>centro, La Casería y entorno del Arsenal</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso urbano para alquiler residencial estable, apoyado en una demanda institucional (militar y administrativa) prácticamente inelástica al ciclo económico.</p>",
            ["Bahía de Cádiz", "Armada española", "Demanda institucional", "Histórica"],
        ],
    },
    "sanlucar-de-barrameda": {
        "name": "Sanlúcar de Barrameda",
        "roi": "6,2%", "precio": "1.400€", "alquiler": "724€/mes", "dias": "24",
        "alts": [("rentabilidad-chipiona.html", "Chipiona"), ("rentabilidad-rota.html", "Rota")],
        "paragraphs": [
            "<p>Sanlúcar de Barrameda es la Capital Española de la Gastronomía 2022 y uno de los destinos turístico-culturales con más proyección de la Costa de la Luz. Combina manzanilla, langostinos, las carreras de caballos en la playa y la puerta de entrada al Parque Nacional de Doñana. El reconocimiento gastronómico ha impulsado los precios sin saturar todavía el mercado. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>.</p>",
            "<p>La demanda combina residencial permanente, turismo gastronómico premium y un creciente interés de segunda residencia. Alquiler medio: <strong>724€/mes</strong>; <strong>24 días</strong> de absorción. Zonas: <strong>Bajo de Guía (referencia gastronómica), Barrio Alto y centro</strong>. ITP Andalucía: <strong>7%</strong>. Tesis muy interesante: VUT registrada en Bajo de Guía o cerca del centro para capturar el boom gastronómico, combinada con apreciación a 5 años por marca turística consolidada.</p>",
            ["Costa de la Luz", "Capital gastronómica", "Doñana", "VUT premium"],
        ],
    },
    "tarifa": {
        "name": "Tarifa",
        "roi": "5,4%", "precio": "2.600€", "alquiler": "1.170€/mes", "dias": "20",
        "alts": [("rentabilidad-conil-de-la-frontera.html", "Conil"), ("rentabilidad-algeciras.html", "Algeciras")],
        "paragraphs": [
            "<p>Tarifa es la capital mundial del kitesurf y windsurf, con vientos de Levante y Poniente legendarios y playas como Valdevaqueros, Bolonia o Los Lances. El perfil turístico es muy específico: deportes acuáticos, surferos europeos, ecoturismo y una comunidad cosmopolita estable. Es además el punto más al sur de la Europa continental. Precio medio: <strong>2.600€/m²</strong> — el segundo más alto del grupo — y <strong>rentabilidad bruta del 5,4%</strong>, contenida por la entrada cara.</p>",
            "<p>El alquiler medio supera los <strong>1.170€/mes</strong> y los <strong>20 días</strong> de absorción confirman un mercado muy líquido. La explotación VUT alcanza yields combinados muy superiores en temporada alta (mayo-octubre). Zonas: <strong>Casco Antiguo (regulado), Atunara y zona Valdevaqueros</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: VUT registrada con licencia, segmentada a comunidad surfera internacional, con tarifas premium y ocupación elevada 6 meses al año.</p>",
            ["Costa de la Luz", "Kitesurf mundial", "VUT premium", "Mercado líquido"],
        ],
    },
    "tomares": {
        "name": "Tomares",
        "roi": "5,4%", "precio": "2.200€", "alquiler": "990€/mes", "dias": "21",
        "alts": [("rentabilidad-bormujos.html", "Bormujos"), ("rentabilidad-mairena-del-aljarafe.html", "Mairena del Aljarafe")],
        "paragraphs": [
            "<p>Tomares es uno de los municipios con mayor renta per cápita de Andalucía y la plaza residencial premium del Aljarafe sevillano, junto con Bormujos. Su perfil de clase media-alta, los chalets adosados y unifamiliares y la cercanía a Sevilla por la SE-30 configuran un mercado caro pero muy estable. Precio medio: <strong>2.200€/m²</strong> — top del Aljarafe — y <strong>rentabilidad bruta del 5,4%</strong>, baja como corresponde a residencial premium.</p>",
            "<p>La demanda se concentra en familias profesionales que trabajan en Sevilla y buscan calidad de vida con espacio. El alquiler medio (<strong>990€/mes</strong>) y los <strong>21 días</strong> de absorción reflejan un mercado tensionado. Zonas: <strong>El Tomillar, Aljamar y Santa Eufemia</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso amplio de 3-4 dormitorios o adosado para alquiler familiar de larga duración, con foco en revalorización a 5-7 años más que en yield bruto.</p>",
            ["Aljarafe premium", "Residencial alto poder", "Adosados", "Apreciación"],
        ],
    },
    "torrox": {
        "name": "Torrox",
        "roi": "5,8%", "precio": "2.200€", "alquiler": "1.063€/mes", "dias": "22",
        "alts": [("rentabilidad-nerja.html", "Nerja"), ("rentabilidad-velez-malaga.html", "Vélez-Málaga")],
        "paragraphs": [
            "<p>Torrox es un municipio de la Axarquía malagueña con una identidad dual: pueblo blanco interior de origen nazarí y una zona costera (Torrox Costa) consolidada como destino turístico para comunidad alemana. De hecho, presume del eslogan “mejor clima de Europa” según un estudio de la Universidad de Düsseldorf. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>.</p>",
            "<p>El inquilino tipo es residente alemán o centroeuropeo (jubilado o teletrabajador) que busca clima y comunidad. El alquiler medio (<strong>1.063€/mes</strong>) y los <strong>22 días</strong> de absorción muestran demanda fuerte. Zonas: <strong>Torrox Costa (alquiler residencial alemán), Torrox Pueblo y El Morche</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso o estudio bien orientado en Torrox Costa para alquiler residencial estable a comunidad alemana, con tipo de cliente fidelizado y rotación baja.</p>",
            ["Costa del Sol oriental", "Axarquía", "Comunidad alemana", "Larga duración"],
        ],
    },
    "ubeda": {
        "name": "Úbeda",
        "roi": "6,5%", "precio": "1.200€", "alquiler": "580€/mes", "dias": "22",
        "alts": [("rentabilidad-baeza.html", "Baeza"), ("rentabilidad-jaen.html", "Jaén")],
        "paragraphs": [
            "<p>Úbeda es Patrimonio de la Humanidad por la UNESCO desde 2003 (junto con Baeza), una ciudad joya del Renacimiento español con la Plaza Vázquez de Molina y las obras de Andrés de Vandelvira como referencia. La economía combina turismo cultural, olivar y un tejido industrial moderado (cerámica artesanal, agroalimentaria). Precio medio: <strong>1.200€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>.</p>",
            "<p>La demanda de alquiler es estable: trabajadores agrícolas, profesionales sanitarios del Hospital San Juan de la Cruz, docentes y un nicho de demanda turística (VUT en casco histórico, regulado). Alquiler medio: <strong>580€/mes</strong>; <strong>22 días</strong> de absorción — fluido para una plaza del interior. Zonas: <strong>casco histórico (regulado), San Isidoro y el ensanche</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: vivienda con cierto encanto en casco para combinar VUT cultural + alquiler residencial.</p>",
            ["UNESCO", "Renacimiento", "Olivar", "Mixto residencial/VUT"],
        ],
    },
    "utrera": {
        "name": "Utrera",
        "roi": "6,4%", "precio": "1.300€", "alquiler": "694€/mes", "dias": "25",
        "alts": [("rentabilidad-alcala-de-guadaira.html", "Alcalá de Guadaíra"), ("rentabilidad-lebrija.html", "Lebrija")],
        "paragraphs": [
            "<p>Utrera es una ciudad media del sur de la provincia de Sevilla, con una posición estratégica en el eje Sevilla-Cádiz, conexión por AVE y un tejido económico equilibrado: agricultura, industria agroalimentaria, polígonos y servicios. La cercanía a Sevilla (35 km) la convierte en alternativa real para familias que buscan vivienda asequible. Precio medio: <strong>1.300€/m²</strong>; <strong>rentabilidad bruta 6,4%</strong>.</p>",
            "<p>La demanda de alquiler procede de trabajadores industriales, agrícolas y un componente creciente de profesionales sevillanos que aprovechan la conexión por cercanías. Alquiler medio: <strong>694€/mes</strong>; <strong>25 días</strong> de absorción. Zonas: <strong>centro, Vistalegre y el ensanche norte</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso de 2-3 dormitorios para alquiler familiar con yield superior a Sevilla y exposición indirecta a la presión demográfica metropolitana sevillana.</p>",
            ["Bajo Guadalquivir", "Eje Sevilla-Cádiz", "AVE + cercanías", "Familiar"],
        ],
    },
    "velez-blanco": {
        "name": "Vélez-Blanco",
        "roi": "7,0%", "precio": "800€", "alquiler": "467€/mes", "dias": "28",
        "alts": [("rentabilidad-huercal-overa.html", "Huércal-Overa"), ("rentabilidad-vera.html", "Vera")],
        "paragraphs": [
            "<p>Vélez-Blanco es una de las plazas más singulares de Almería: un municipio del altiplano norte coronado por el Castillo de los Fajardo (siglo XVI), con el Parque Natural Sierra María-Los Vélez como escenario y un patrimonio prehistórico (Cueva de los Letreros, arte rupestre). El precio medio (<strong>800€/m²</strong>) es el más bajo del grupo y entrega la <strong>rentabilidad bruta más alta: 7,0%</strong>.</p>",
            "<p>La demanda de alquiler es muy reducida en términos absolutos pero estable: trabajadores agrícolas, ganaderos, funcionarios y un nicho creciente de turismo rural y ecoturismo. Alquiler medio: <strong>467€/mes</strong>; <strong>28 días</strong> de absorción reflejan un mercado pequeño y poco líquido. Zonas: <strong>casco histórico, La Almudina y entorno del Castillo</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: comprar muy barato (vivienda completa por menos de 50.000€ es factible) para uso turístico rural o cash-flow modesto pero alto en porcentaje.</p>",
            ["Altiplano almeriense", "Patrimonio rupestre", "Turismo rural", "Yield máximo"],
        ],
    },
    "vera": {
        "name": "Vera",
        "roi": "6,2%", "precio": "1.800€", "alquiler": "930€/mes", "dias": "22",
        "alts": [("rentabilidad-mojacar.html", "Mojácar"), ("rentabilidad-huercal-overa.html", "Huércal-Overa")],
        "paragraphs": [
            "<p>Vera es uno de los municipios con mayor crecimiento del Levante almeriense, con un perfil dual: casco histórico interior (la antigua Vera) y la pujante zona costera de Vera Playa, conocida por sus urbanizaciones turísticas y por contar con uno de los mayores núcleos naturistas de Europa. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>930€/mes</strong>.</p>",
            "<p>La demanda combina residencial permanente, turismo internacional (alemanes, británicos, franceses) y nicho naturista en Vera Playa. Los <strong>22 días</strong> de absorción reflejan un mercado tensionado. Zonas: <strong>Vera Playa (residencial-turística), Vera centro y Las Marinas</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso en Vera Playa para VUT estacional o alquiler residencial a comunidad europea, capturando tanto yield turístico como apreciación por crecimiento poblacional sostenido del Levante.</p>",
            ["Levante almeriense", "Vera Playa", "Turismo europeo", "Crecimiento sostenido"],
        ],
    },
}

EDITORIAL_TEMPLATE = """  <!-- EDITORIAL {SLUG_UP} -->
  <div class="section ed-section">
    <div class="sec-hdr">
      <div class="sec-eye">Análisis del mercado</div>
      <h2>Qué debes saber antes de invertir en {NAME} en 2026</h2>
    </div>
    <div class="ed-body">
      <div class="ed-highlight">
        <div class="ed-stat"><div class="ed-stat-val">{ROI}</div><div class="ed-stat-lbl">rentabilidad bruta</div></div>
        <div class="ed-stat"><div class="ed-stat-val">{PRECIO}</div><div class="ed-stat-lbl">precio medio m²</div></div>
        <div class="ed-stat"><div class="ed-stat-val">{ALQUILER}</div><div class="ed-stat-lbl">alquiler medio</div></div>
        <div class="ed-stat"><div class="ed-stat-val">{DIAS}</div><div class="ed-stat-lbl">días media venta</div></div>
      </div>
      {PARAGRAPHS}
      <p>{TAGS}</p>
      <p style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border);font-size:.85rem"><strong>Ciudades alternativas:</strong> {ALTS}</p>
    </div>
  </div>

"""

def render_tags(tags):
    return "".join(f'<span class="ed-tag">{t}</span>' for t in tags)

def render_alts(alts):
    return " · ".join(
        f'<a href="/{href}" style="color:var(--blue);text-decoration:none;font-weight:600">{name}</a>'
        for href, name in alts
    )

inserted, errors = [], []
for slug, c in CITIES.items():
    fp = ROOT / f"rentabilidad-{slug}.html"
    if not fp.exists():
        errors.append(f"{slug}: archivo no existe"); continue
    html = fp.read_text(encoding="utf-8")
    if "<!-- EDITORIAL" in html:
        errors.append(f"{slug}: ya tiene EDITORIAL, salto"); continue
    if "  <!-- TIPOS DE VIVIENDA -->" not in html:
        errors.append(f"{slug}: no encuentro ancla TIPOS DE VIVIENDA"); continue

    paragraphs = "\n      ".join(c["paragraphs"][:-1])
    tags = render_tags(c["paragraphs"][-1])
    block = EDITORIAL_TEMPLATE.format(
        SLUG_UP=slug.upper().replace("-", " "),
        NAME=c["name"],
        ROI=c["roi"], PRECIO=c["precio"], ALQUILER=c["alquiler"], DIAS=c["dias"],
        PARAGRAPHS=paragraphs, TAGS=tags, ALTS=render_alts(c["alts"]),
    )
    new_html = html.replace("  <!-- TIPOS DE VIVIENDA -->", block + "  <!-- TIPOS DE VIVIENDA -->", 1)
    fp.write_text(new_html, encoding="utf-8")
    inserted.append(slug)

print(f"OK insertadas: {len(inserted)}")
for s in inserted: print(f"  + {s}")
if errors:
    print("\nERRORES:")
    for e in errors: print(f"  ! {e}")
