"""Genera e inserta editoriales para 25 ciudades andaluzas en sus rentabilidad-*.html"""
import re, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

# (slug, nombre_display, roi, precio, alquiler, dias, [alt1_slug,alt1_nombre], [alt2_slug,alt2_nombre], [tag1, tag2, tag3])
CITIES = {
    "adra": {
        "name": "Adra",
        "roi": "6,4%", "precio": "1.300€", "alquiler": "693€/mes", "dias": "24",
        "alts": [("rentabilidad-el-ejido.html", "El Ejido"), ("rentabilidad-roquetas-de-mar.html", "Roquetas de Mar")],
        "tags": ["Costa de Almería", "Pesquero", "Invernaderos"],
        "title_extra": "Adra",
        "paragraphs": [
            "<p>Adra es la ciudad más antigua de Almería y un nodo costero del poniente almeriense que combina pesca artesanal, agricultura intensiva bajo plástico y un turismo de proximidad todavía poco saturado. Con un precio medio de <strong>1.300€/m²</strong> y una <strong>rentabilidad bruta del 6,4%</strong>, ofrece un punto de entrada accesible muy por debajo del coste medio andaluz. El alquiler ronda los <strong>693€/mes</strong> y el tiempo medio en mercado de <strong>24 días</strong> apunta a una demanda activa, sostenida por el empleo agrícola y portuario.</p>",
            "<p>El inquilino tipo es un trabajador de la cadena hortofrutícola o del sector servicios local, frecuentemente con contratos estables de temporada larga. Las zonas más sólidas para invertir son <strong>Puerta del Mar, La Curva y Puente del Río</strong>, donde la combinación de stock con cierta antigüedad y proximidad al casco abre margen de revalorización. ITP Andalucía: <strong>7%</strong>. Para inversores que priorizan cash-flow sobre revalorización rápida, Adra ofrece tickets bajos y yields consistentes.</p>",
            ["Costa de Almería", "Pesquero", "Invernaderos", "Sin VUT tensionada"],
        ],
    },
    "alcala-la-real": {
        "name": "Alcalá la Real",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "542€/mes", "dias": "27",
        "alts": [("rentabilidad-jaen.html", "Jaén"), ("rentabilidad-martos.html", "Martos")],
        "title_extra": "Alcalá la Real",
        "paragraphs": [
            "<p>Alcalá la Real es una ciudad media del sur de Jaén con una identidad histórica fuerte — la Fortaleza de la Mota domina el horizonte — y una economía apoyada en el olivar, la industria agroalimentaria y los servicios comarcales. Con un precio de <strong>1.000€/m²</strong>, está entre los mercados más baratos de Andalucía y entrega un <strong>ROI bruto del 6,5%</strong>, ligeramente por encima de la media nacional. El alquiler medio se sitúa en <strong>542€/mes</strong>.</p>",
            "<p>La demanda de alquiler proviene de trabajadores del olivar, profesores destinados a la zona y familias jóvenes que buscan vivienda accesible cerca de los servicios. Los <strong>27 días</strong> medios de venta reflejan un mercado pausado pero líquido. Zonas recomendadas: <strong>el ensanche, Llanillo y entorno del centro histórico</strong>. ITP Andalucía: <strong>7%</strong>. Para inversores con horizonte a 7-10 años, ofrece entradas baratas y rentabilidad estable, sin la volatilidad de la costa.</p>",
            ["Sierra Sur de Jaén", "Olivar", "Patrimonio histórico", "Mercado pausado"],
        ],
    },
    "alhaurin-de-la-torre": {
        "name": "Alhaurín de la Torre",
        "roi": "5,8%", "precio": "2.100€", "alquiler": "1.015€/mes", "dias": "22",
        "alts": [("rentabilidad-malaga.html", "Málaga"), ("rentabilidad-alhaurin-el-grande.html", "Alhaurín el Grande")],
        "title_extra": "Alhaurín de la Torre",
        "paragraphs": [
            "<p>Alhaurín de la Torre es uno de los municipios de mayor crecimiento del área metropolitana de Málaga, con un perfil residencial de clase media-alta empujado por la cercanía al aeropuerto, al PTA (Parque Tecnológico de Andalucía) y a la propia capital. El precio medio asciende a <strong>2.100€/m²</strong> — claramente por encima de la media andaluza — y la <strong>rentabilidad bruta del 5,8%</strong> queda por debajo del 6,5% nacional, pero compensada por una revalorización notable.</p>",
            "<p>El inquilino típico es un profesional cualificado vinculado al PTA o a Málaga capital, frecuentemente con familia, que busca chalet o vivienda amplia con zonas comunes. El <strong>alquiler medio (1.015€/mes)</strong> y los <strong>22 días</strong> de absorción confirman una demanda fuerte. Zonas a vigilar: <strong>El Romeral, Pinos de Alhaurín y Santa Clara</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: jugar la apreciación residencial a 5-7 años más que el yield puro.</p>",
            ["Área metropolitana Málaga", "PTA", "Residencial", "Apreciación"],
        ],
    },
    "alhaurin-el-grande": {
        "name": "Alhaurín el Grande",
        "roi": "6,2%", "precio": "1.700€", "alquiler": "876€/mes", "dias": "24",
        "alts": [("rentabilidad-coin.html", "Coín"), ("rentabilidad-alhaurin-de-la-torre.html", "Alhaurín de la Torre")],
        "title_extra": "Alhaurín el Grande",
        "paragraphs": [
            "<p>Alhaurín el Grande es el corazón del Valle del Guadalhorce, un municipio interior de la comarca malagueña con fuerte presencia de comunidad británica y centroeuropea. A diferencia de su vecino Alhaurín de la Torre — más urbano y caro —, aquí el precio medio se queda en <strong>1.700€/m²</strong> y la <strong>rentabilidad bruta llega al 6,2%</strong>, un equilibrio razonable entre coste de entrada y yield. El alquiler medio es de <strong>876€/mes</strong>.</p>",
            "<p>El perfil de demanda mezcla inquilino local con jubilados extranjeros y teletrabajadores que buscan vida tranquila a 30 minutos de la costa. <strong>24 días</strong> de absorción media indican un mercado fluido. Zonas: <strong>El Calvario, Villafranco del Guadalhorce y entorno del casco</strong>. ITP Andalucía: <strong>7%</strong>. Es una plaza idónea para inversor patrimonialista que combine alquiler residencial con eventual venta a comprador extranjero.</p>",
            ["Valle del Guadalhorce", "Demanda extranjera", "Interior Costa del Sol", "Patrimonialista"],
        ],
    },
    "almunecar": {
        "name": "Almuñécar",
        "roi": "5,5%", "precio": "2.400€", "alquiler": "1.100€/mes", "dias": "22",
        "alts": [("rentabilidad-motril.html", "Motril"), ("rentabilidad-nerja.html", "Nerja")],
        "title_extra": "Almuñécar",
        "paragraphs": [
            "<p>Almuñécar es la capital de la Costa Tropical granadina, con microclima subtropical, 19 km de costa y una mezcla de turismo nacional, comunidad expatriada (especialmente británica y nórdica) y residentes permanentes. El precio medio sube a <strong>2.400€/m²</strong> — el más alto del grupo analizado — y la <strong>rentabilidad bruta del 5,5%</strong> queda por debajo de la media, lo habitual en plazas turísticas consolidadas.</p>",
            "<p>El alquiler medio (<strong>1.100€/mes</strong>) y los <strong>22 días</strong> de absorción reflejan una demanda firme, sostenida por el turismo y por residentes europeos jubilados. Las zonas más rentables están en <strong>La Herradura, Velilla y el casco antiguo</strong>. La fiscalidad turística es clave: con licencia VUT operativa, el yield combinado supera al residencial puro. ITP Andalucía: <strong>7%</strong>. Tesis ideal: comprar a 5-7 años con uso mixto residencial/temporada.</p>",
            ["Costa Tropical", "Turismo", "Expatriados", "VUT viable"],
        ],
    },
    "andujar": {
        "name": "Andújar",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "520€/mes", "dias": "22",
        "alts": [("rentabilidad-jaen.html", "Jaén"), ("rentabilidad-linares.html", "Linares")],
        "title_extra": "Andújar",
        "paragraphs": [
            "<p>Andújar es una ciudad media del norte de Jaén con un tejido económico equilibrado: olivar, industria del aceite, fabricación de plásticos y servicios comarcales. El precio medio de <strong>1.000€/m²</strong> la sitúa entre las plazas más baratas de la región, con una <strong>rentabilidad bruta del 6,5%</strong> que iguala la media nacional. El alquiler medio se queda en <strong>520€/mes</strong>, lo que la hace atractiva para tickets pequeños.</p>",
            "<p>La demanda de alquiler combina trabajadores del polígono industrial, funcionarios y familias jóvenes. La romería de la Virgen de la Cabeza genera además picos puntuales de ocupación turística. <strong>22 días</strong> de absorción muestran un mercado relativamente líquido para una ciudad pequeña. Zonas: <strong>el centro, Polígono y Puerta de Madrid</strong>. ITP Andalucía: <strong>7%</strong>. Buena plaza para inversores que buscan diversificación geográfica con yield decente y entrada baja.</p>",
            ["Norte de Jaén", "Olivar", "Industrial", "Ticket bajo"],
        ],
    },
    "armilla": {
        "name": "Armilla",
        "roi": "5,9%", "precio": "1.800€", "alquiler": "884€/mes", "dias": "22",
        "alts": [("rentabilidad-granada.html", "Granada"), ("rentabilidad-maracena.html", "Maracena")],
        "title_extra": "Armilla",
        "paragraphs": [
            "<p>Armilla es uno de los municipios estrella del cinturón metropolitano de Granada, conurbado con la capital y polo de servicios (PTS, Centro Comercial Nevada, base aérea). El precio medio se sitúa en <strong>1.800€/m²</strong> — bastante por encima de la media provincial — y entrega una <strong>rentabilidad bruta del 5,9%</strong>. El alquiler medio (<strong>884€/mes</strong>) se sostiene en demanda universitaria desbordada desde Granada y profesionales del PTS.</p>",
            "<p>El perfil de inquilino es muy mixto: estudiantes de la UGR que no encuentran piso en Granada, sanitarios del PTS, parejas jóvenes y familias con hijos pequeños. Los <strong>22 días</strong> de absorción reflejan un mercado tensionado. Zonas: <strong>Santa Ana, Centro y el entorno del Nevada</strong>. ITP Andalucía: <strong>7%</strong>. Es una plaza para invertir en pisos de 2-3 dormitorios con buena conectividad al metro de Granada.</p>",
            ["Área metropolitana Granada", "PTS", "Universitario", "Conectado por metro"],
        ],
    },
    "baeza": {
        "name": "Baeza",
        "roi": "6,2%", "precio": "1.100€", "alquiler": "567€/mes", "dias": "27",
        "alts": [("rentabilidad-ubeda.html", "Úbeda"), ("rentabilidad-jaen.html", "Jaén")],
        "title_extra": "Baeza",
        "paragraphs": [
            "<p>Baeza es Patrimonio de la Humanidad por la UNESCO desde 2003, una joya renacentista del centro de Jaén que combina turismo cultural, sede universitaria (UNIA) y economía olivarera. El precio medio (<strong>1.100€/m²</strong>) refleja la condición de ciudad pequeña pero con prestigio patrimonial; la <strong>rentabilidad bruta del 6,2%</strong> es competitiva. Alquiler medio: <strong>567€/mes</strong>.</p>",
            "<p>La demanda de alquiler es estable: estudiantes universitarios, docentes y trabajadores agrícolas. El turismo cultural — sostenido y de calidad — abre la puerta a explotación VUT en el casco antiguo, aunque con limitaciones por la protección patrimonial. Los <strong>27 días</strong> de absorción reflejan un ritmo pausado típico de plaza pequeña. Zonas: <strong>casco histórico (regulado), entorno UNIA y arrabales</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: comprar bien por debajo del precio medio aprovechando ineficiencias del mercado local.</p>",
            ["UNESCO", "Universitaria UNIA", "Turismo cultural", "Olivar"],
        ],
    },
    "baza": {
        "name": "Baza",
        "roi": "7,0%", "precio": "900€", "alquiler": "525€/mes", "dias": "28",
        "alts": [("rentabilidad-guadix.html", "Guadix"), ("rentabilidad-granada.html", "Granada")],
        "title_extra": "Baza",
        "paragraphs": [
            "<p>Baza es la cabecera comarcal del altiplano granadino, un mercado interior con una de las <strong>rentabilidades brutas más altas de Andalucía: 7,0%</strong>. El precio medio (<strong>900€/m²</strong>) es de los más bajos de la región y permite tickets de inversión muy contenidos. El alquiler medio se sitúa en <strong>525€/mes</strong>, suficiente para sostener el yield.</p>",
            "<p>La demanda de alquiler proviene de trabajadores agrícolas, ganaderos, personal sanitario del Hospital de Baza y funcionarios. El mercado es pequeño y los <strong>28 días</strong> de absorción exigen paciencia, pero la baja oferta limita la competencia entre arrendadores. Zonas: <strong>centro histórico, ensanche y entorno de la Plaza Mayor</strong>. ITP Andalucía: <strong>7%</strong>. Plaza recomendada para inversores que buscan máximo yield y aceptan menor liquidez en favor de cash-flow estable.</p>",
            ["Altiplano de Granada", "Yield alto", "Ticket muy bajo", "Mercado pequeño"],
        ],
    },
    "bormujos": {
        "name": "Bormujos",
        "roi": "5,8%", "precio": "2.000€", "alquiler": "965€/mes", "dias": "21",
        "alts": [("rentabilidad-tomares.html", "Tomares"), ("rentabilidad-mairena-del-aljarafe.html", "Mairena del Aljarafe")],
        "title_extra": "Bormujos",
        "paragraphs": [
            "<p>Bormujos pertenece al Aljarafe sevillano, una de las áreas residenciales más demandadas del entorno metropolitano de Sevilla, con perfil de clase media-alta y crecimiento poblacional sostenido. El precio medio (<strong>2.000€/m²</strong>) refleja esa demanda, y la <strong>rentabilidad bruta del 5,8%</strong> es típica de zonas residenciales premium. El alquiler medio supera los <strong>965€/mes</strong>.</p>",
            "<p>El inquilino tipo es una familia joven de profesionales que trabajan en Sevilla capital pero buscan vivienda más amplia con jardín o piscina comunitaria. Los <strong>21 días</strong> de absorción confirman un mercado tensionado, de los más rápidos de la zona. Zonas: <strong>La Motilla, Cavaleri y entorno del Hospital San Juan de Dios</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso de 3 dormitorios para alquiler familiar largo plazo o adosado para revalorización a 5 años.</p>",
            ["Aljarafe", "Residencial premium", "Familias jóvenes", "Mercado tensionado"],
        ],
    },
    "carmona": {
        "name": "Carmona",
        "roi": "6,0%", "precio": "1.400€", "alquiler": "700€/mes", "dias": "25",
        "alts": [("rentabilidad-ecija.html", "Écija"), ("rentabilidad-marchena.html", "Marchena")],
        "title_extra": "Carmona",
        "paragraphs": [
            "<p>Carmona es una de las ciudades históricas más singulares de la campiña sevillana, con un casco amurallado de origen romano-musulmán y fuerte componente turístico de calidad. La cercanía a Sevilla (35 km) y al aeropuerto la convierte en un mercado dual: residencia secundaria y vivienda permanente para quienes huyen del precio sevillano. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>.</p>",
            "<p>La demanda de alquiler combina familias locales, trabajadores agrícolas y sanitarios del Hospital de la Merced. La actividad VUT en el casco histórico es relevante pero con regulación creciente. El <strong>alquiler medio (700€/mes)</strong> y los <strong>25 días</strong> de absorción muestran un mercado saneado. Zonas: <strong>casco histórico (regulado), San Pedro y nuevas promociones del ensanche</strong>. ITP Andalucía: <strong>7%</strong>. Atractivo para inversor que combine residencial con explotación turística limitada.</p>",
            ["Campiña sevillana", "Turismo cultural", "Histórico", "VUT regulada"],
        ],
    },
    "chiclana-de-la-frontera": {
        "name": "Chiclana de la Frontera",
        "roi": "5,5%", "precio": "2.000€", "alquiler": "920€/mes", "dias": "22",
        "alts": [("rentabilidad-conil-de-la-frontera.html", "Conil"), ("rentabilidad-san-fernando-cadiz.html", "San Fernando")],
        "title_extra": "Chiclana de la Frontera",
        "paragraphs": [
            "<p>Chiclana es uno de los grandes núcleos de la Bahía de Cádiz, con la Playa de la Barrosa como motor turístico y Sancti Petri como zona hotelera consolidada. El crecimiento poblacional ha sido fuerte en la última década, lo que ha empujado el precio medio a <strong>2.000€/m²</strong>. La <strong>rentabilidad bruta (5,5%)</strong> queda por debajo de la media andaluza, lo habitual en plazas costeras maduras.</p>",
            "<p>La demanda de alquiler es muy estacional: residencial todo el año en el núcleo urbano y temporada alta turística entre junio y septiembre en la zona costera. El <strong>alquiler medio (920€/mes)</strong> y los <strong>22 días</strong> de absorción reflejan demanda sostenida. Zonas: <strong>Novo Sancti Petri, La Barrosa y casco urbano</strong>. ITP Andalucía: <strong>7%</strong>. Tesis ganadora: VUT con licencia en zona Barrosa para combinar yield turístico y revalorización.</p>",
            ["Bahía de Cádiz", "Costa de la Luz", "Turismo de playa", "VUT estacional"],
        ],
    },
    "chipiona": {
        "name": "Chipiona",
        "roi": "6,0%", "precio": "1.600€", "alquiler": "800€/mes", "dias": "23",
        "alts": [("rentabilidad-rota.html", "Rota"), ("rentabilidad-sanlucar-de-barrameda.html", "Sanlúcar de Barrameda")],
        "title_extra": "Chipiona",
        "paragraphs": [
            "<p>Chipiona es un clásico del veraneo familiar de la Costa de la Luz gaditana, con el faro más alto de España y una identidad cultural fuerte (Rocío Jurado, manzanilla, moscatel). El mercado se mueve a <strong>1.600€/m²</strong> con una <strong>rentabilidad bruta del 6,0%</strong>, equilibrio razonable entre plaza turística y precio accesible respecto a Conil o El Puerto.</p>",
            "<p>El alquiler medio (<strong>800€/mes</strong>) y los <strong>23 días</strong> de absorción muestran un mercado activo. La estacionalidad es marcada: residencia permanente en otoño-invierno, alquiler turístico-vacacional en verano. Las zonas más rentables están <strong>cerca del paseo marítimo, Regla y el centro</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: combinar alquiler residencial de octubre a junio con VUT en julio-agosto para maximizar yield combinado.</p>",
            ["Costa de la Luz", "Turismo familiar", "Manzanilla", "Yield mixto VUT/residencial"],
        ],
    },
    "coin": {
        "name": "Coín",
        "roi": "6,0%", "precio": "1.600€", "alquiler": "800€/mes", "dias": "25",
        "alts": [("rentabilidad-alhaurin-el-grande.html", "Alhaurín el Grande"), ("rentabilidad-marbella.html", "Marbella")],
        "title_extra": "Coín",
        "paragraphs": [
            "<p>Coín es el centro comarcal del Valle del Guadalhorce, en el interior de Málaga, con una mezcla creciente entre población local y comunidad extranjera (británica, alemana, escandinava) atraída por la calidad de vida y el clima. El precio medio se sitúa en <strong>1.600€/m²</strong> y la <strong>rentabilidad bruta es del 6,0%</strong>. El alquiler medio (<strong>800€/mes</strong>) está apoyado por demanda permanente de jubilados extranjeros con poder adquisitivo.</p>",
            "<p>El inquilino habitual es residencial de larga duración: familias locales, profesionales que trabajan en Málaga capital o Marbella y expatriados europeos. Los <strong>25 días</strong> de absorción reflejan un mercado fluido. Zonas: <strong>Los Llanos, El Charcón y entorno del centro</strong>. ITP Andalucía: <strong>7%</strong>. Plaza idónea para inversor patrimonialista con horizonte 5-10 años, enfocado en chalets pareados o pisos amplios.</p>",
            ["Valle del Guadalhorce", "Comunidad extranjera", "Interior Málaga", "Larga duración"],
        ],
    },
    "conil-de-la-frontera": {
        "name": "Conil de la Frontera",
        "roi": "5,6%", "precio": "2.200€", "alquiler": "1.023€/mes", "dias": "22",
        "alts": [("rentabilidad-chiclana-de-la-frontera.html", "Chiclana"), ("rentabilidad-vejer-de-la-frontera.html", "Vejer")],
        "title_extra": "Conil de la Frontera",
        "paragraphs": [
            "<p>Conil es uno de los destinos más demandados de la Costa de la Luz, con playas como El Palmar (referencia surfera), Cala del Aceite o Fuente del Gallo. El crecimiento turístico ha empujado el precio medio a <strong>2.200€/m²</strong>, alto para un municipio interior pero coherente con la marca turística. La <strong>rentabilidad bruta del 5,6%</strong> es típica de plaza costera consolidada con entrada cara.</p>",
            "<p>El alquiler medio supera los <strong>1.023€/mes</strong> en residencial, pero el verdadero atractivo está en el VUT estacional: ocupación elevada de junio a septiembre con tarifas premium. Los <strong>22 días</strong> de absorción confirman una demanda fuerte. Zonas: <strong>El Palmar, Roche y casco</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: comprar para explotación VUT registrada combinando alquiler de temporada con apreciación a medio plazo.</p>",
            ["Costa de la Luz", "Surf", "VUT premium", "Apreciación turística"],
        ],
    },
    "ecija": {
        "name": "Écija",
        "roi": "6,5%", "precio": "850€", "alquiler": "460€/mes", "dias": "22",
        "alts": [("rentabilidad-carmona.html", "Carmona"), ("rentabilidad-marchena.html", "Marchena")],
        "title_extra": "Écija",
        "paragraphs": [
            "<p>Écija, conocida como “la sartén de Andalucía” por sus altas temperaturas estivales, es una ciudad media de la campiña sevillana con un patrimonio barroco extraordinario (11 torres) y una economía basada en agricultura, agroindustria y servicios. Es uno de los mercados <strong>más baratos de la región: 850€/m²</strong>, con una <strong>rentabilidad bruta del 6,5%</strong> y alquiler medio de <strong>460€/mes</strong>.</p>",
            "<p>La demanda de alquiler es local: familias jóvenes, trabajadores agrícolas y de la guarnición militar (Acuartelamiento de Écija). Los <strong>22 días</strong> de absorción muestran un mercado más fluido de lo esperable para una ciudad de su tamaño. Zonas: <strong>centro histórico, El Picadero y el ensanche</strong>. ITP Andalucía: <strong>7%</strong>. Es una plaza muy interesante para inversor que busca tickets de entrada bajísimos (vivienda completa por menos de 60.000€ es factible) con yields sólidos.</p>",
            ["Campiña sevillana", "Patrimonio barroco", "Ticket muy bajo", "Cash-flow"],
        ],
    },
    "el-ejido": {
        "name": "El Ejido",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "570€/mes", "dias": "22",
        "alts": [("rentabilidad-roquetas-de-mar.html", "Roquetas de Mar"), ("rentabilidad-adra.html", "Adra")],
        "title_extra": "El Ejido",
        "paragraphs": [
            "<p>El Ejido es la capital mundial de la agricultura intensiva bajo plástico, un municipio almeriense con un dinamismo económico inusual para su tamaño y un PIB per cápita de los más altos de la provincia. El precio medio (<strong>1.100€/m²</strong>) sigue siendo bajo respecto al peso económico real de la ciudad, lo que se traduce en una <strong>rentabilidad bruta del 6,5%</strong>. Alquiler medio: <strong>570€/mes</strong>.</p>",
            "<p>La demanda de alquiler es enorme y muy específica: trabajadores del sector hortofrutícola — muchos extranjeros con contratos estables — empresarios agrícolas y servicios auxiliares. Los <strong>22 días</strong> de absorción reflejan un mercado tensionado. Zonas: <strong>centro, Almerimar (residencial-turístico) y Las Norias</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: vivienda funcional para alquiler residencial estable, con la opción de Almerimar para perfil turístico-segunda residencia.</p>",
            ["Poniente almeriense", "Invernaderos", "Demanda estructural", "Almerimar"],
        ],
    },
    "el-puerto-de-santa-maria": {
        "name": "El Puerto de Santa María",
        "roi": "5,7%", "precio": "1.800€", "alquiler": "860€/mes", "dias": "22",
        "alts": [("rentabilidad-cadiz.html", "Cádiz"), ("rentabilidad-rota.html", "Rota")],
        "title_extra": "El Puerto de Santa María",
        "paragraphs": [
            "<p>El Puerto de Santa María es una de las cuatro ciudades de la Bahía de Cádiz, con una posición estratégica entre Cádiz capital, Jerez y Rota. Aúna patrimonio histórico (bodegas, casco antiguo), playas urbanas (Valdelagrana, La Puntilla) y conectividad por catamarán con Cádiz. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,7%</strong>. Alquiler medio: <strong>860€/mes</strong>.</p>",
            "<p>La demanda mezcla residencial permanente, estudiantes que se desplazan a Cádiz capital, trabajadores de la base de Rota y turismo. Los <strong>22 días</strong> de absorción reflejan un mercado dinámico. Zonas con tracción: <strong>Valdelagrana, casco histórico (con potencial VUT) y Vistahermosa</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso urbano para alquiler residencial + posible explotación VUT en casco histórico previa licencia. Buena revalorización por dinamismo metropolitano de la Bahía.</p>",
            ["Bahía de Cádiz", "Patrimonio", "Conectividad", "Mixto residencial/VUT"],
        ],
    },
    "guadix": {
        "name": "Guadix",
        "roi": "6,8%", "precio": "900€", "alquiler": "510€/mes", "dias": "27",
        "alts": [("rentabilidad-baza.html", "Baza"), ("rentabilidad-granada.html", "Granada")],
        "title_extra": "Guadix",
        "paragraphs": [
            "<p>Guadix es una de las ciudades más singulares de Andalucía: cuenta con el barrio de cuevas habitadas más grande de Europa y un casco histórico con catedral renacentista y alcazaba árabe. Es la cabecera comarcal del altiplano granadino, con una economía basada en agricultura, servicios y un creciente turismo cultural. El precio medio (<strong>900€/m²</strong>) la sitúa entre las plazas más baratas y entrega un <strong>ROI bruto del 6,8%</strong> — claramente por encima de la media nacional.</p>",
            "<p>El inquilino tipo es local: familias, funcionarios y trabajadores agrícolas. Las cuevas, además, son un nicho de inversión turística específico (alojamiento experiencial). El alquiler medio (<strong>510€/mes</strong>) y los <strong>27 días</strong> de absorción reflejan un mercado pausado pero sólido. Zonas: <strong>casco histórico, Barriada de las Cuevas y ensanche</strong>. ITP Andalucía: <strong>7%</strong>. Tesis dual: residencial de alto yield + cueva turística para experiencia VUT.</p>",
            ["Altiplano de Granada", "Cuevas habitadas", "Patrimonio", "Yield alto"],
        ],
    },
    "huercal-overa": {
        "name": "Huércal-Overa",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "542€/mes", "dias": "27",
        "alts": [("rentabilidad-vera.html", "Vera"), ("rentabilidad-mojacar.html", "Mojácar")],
        "title_extra": "Huércal-Overa",
        "paragraphs": [
            "<p>Huércal-Overa es la cabecera comarcal del Levante almeriense, un nodo de servicios (Hospital La Inmaculada, juzgados, comercio) que abastece a una amplia zona rural y turística. La ciudad atrae demanda residencial estable de personal sanitario y administrativo, y opera además como base logística para los municipios costeros próximos (Vera, Mojácar, Garrucha). El precio medio es de <strong>1.000€/m²</strong> con una <strong>rentabilidad bruta del 6,5%</strong>.</p>",
            "<p>El alquiler medio (<strong>542€/mes</strong>) y los <strong>27 días</strong> de absorción muestran un mercado tranquilo pero con demanda estructural. Zonas: <strong>centro urbano, El Saliente y entorno hospitalario</strong>. ITP Andalucía: <strong>7%</strong>. Es una plaza interesante para inversor que busca rentabilidad estable apoyada en empleo público (sanidad, justicia), con menor volatilidad que las plazas turísticas costeras del Levante. Buen complemento de cartera con activos en Vera o Mojácar.</p>",
            ["Levante almeriense", "Hospital comarcal", "Demanda estructural", "Cabecera comarcal"],
        ],
    },
    "isla-cristina": {
        "name": "Isla Cristina",
        "roi": "6,4%", "precio": "1.400€", "alquiler": "746€/mes", "dias": "24",
        "alts": [("rentabilidad-ayamonte.html", "Ayamonte"), ("rentabilidad-huelva.html", "Huelva")],
        "title_extra": "Isla Cristina",
        "paragraphs": [
            "<p>Isla Cristina es uno de los puertos pesqueros más importantes de Andalucía y un destino turístico emergente de la Costa de la Luz onubense. Combina pesca industrial, conserveras y un turismo de playa todavía más asequible que Cádiz. El precio medio (<strong>1.400€/m²</strong>) ofrece un punto de entrada interesante para una plaza costera y la <strong>rentabilidad bruta del 6,4%</strong> es notable para una zona de playa.</p>",
            "<p>La demanda mezcla residencial permanente (trabajadores del puerto y conserveras), turismo familiar nacional y un creciente interés extranjero (sobre todo portugués por la cercanía con el Algarve). Alquiler medio: <strong>746€/mes</strong>. <strong>24 días</strong> de absorción. Zonas: <strong>Playa Central, Punta del Caimán y casco</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: VUT estacional + alquiler residencial de invierno, con yield combinado superior a otras plazas de la Costa de la Luz.</p>",
            ["Costa de la Luz onubense", "Puerto pesquero", "Frontera Algarve", "VUT viable"],
        ],
    },
    "la-linea-de-la-concepcion": {
        "name": "La Línea de la Concepción",
        "roi": "6,0%", "precio": "1.200€", "alquiler": "600€/mes", "dias": "22",
        "alts": [("rentabilidad-algeciras.html", "Algeciras"), ("rentabilidad-san-roque.html", "San Roque")],
        "title_extra": "La Línea de la Concepción",
        "paragraphs": [
            "<p>La Línea es la ciudad fronteriza con Gibraltar, una plaza atípica con dinámica económica muy condicionada por el Peñón: miles de trabajadores transfronterizos cruzan a diario. El precio medio (<strong>1.200€/m²</strong>) es bajo respecto a su localización privilegiada y entrega una <strong>rentabilidad bruta del 6,0%</strong>. El alquiler medio (<strong>600€/mes</strong>) está sostenido por demanda muy estable.</p>",
            "<p>El inquilino tipo es trabajador con empleo en Gibraltar (que cobra en libras y vive en La Línea por coste), funcionarios y familias locales. Los <strong>22 días</strong> de absorción confirman demanda estructural. Zonas: <strong>centro, La Atunara, La Velada</strong>. ITP Andalucía: <strong>7%</strong>. Plaza con tesis muy específica: yield apoyado en empleo transfronterizo y volatilidad asociada a fluctuaciones de la libra y la relación UE-Reino Unido. Para inversor que entienda esa exposición.</p>",
            ["Frontera Gibraltar", "Trabajadores transfronterizos", "Yield estructural", "Exposición libra"],
        ],
    },
    "la-rinconada": {
        "name": "La Rinconada",
        "roi": "6,5%", "precio": "1.300€", "alquiler": "670€/mes", "dias": "22",
        "alts": [("rentabilidad-sevilla.html", "Sevilla"), ("rentabilidad-alcala-de-guadaira.html", "Alcalá de Guadaíra")],
        "title_extra": "La Rinconada",
        "paragraphs": [
            "<p>La Rinconada es un municipio del área metropolitana norte de Sevilla, conurbado con la capital y bien conectado por C1 de cercanías. Combina población residencial, polígonos industriales (PISA, La Carrasca) y un crecimiento sostenido apoyado en familias jóvenes que salen de Sevilla buscando vivienda más asequible. Precio medio: <strong>1.300€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>.</p>",
            "<p>El alquiler medio (<strong>670€/mes</strong>) es accesible y los <strong>22 días</strong> de absorción confirman un mercado fluido. La demanda procede de familias jóvenes, trabajadores de polígonos sevillanos y profesionales que valoran la conexión por cercanías. Zonas: <strong>San José de la Rinconada, La Estación y Pago de Enmedio</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: piso de 2-3 dormitorios para alquiler familiar con yield superior al de Sevilla capital y demanda más estable.</p>",
            ["Área metropolitana Sevilla", "Cercanías C1", "Familias jóvenes", "Yield superior a Sevilla"],
        ],
    },
    "lebrija": {
        "name": "Lebrija",
        "roi": "7,0%", "precio": "1.000€", "alquiler": "583€/mes", "dias": "28",
        "alts": [("rentabilidad-utrera.html", "Utrera"), ("rentabilidad-sanlucar-de-barrameda.html", "Sanlúcar de Barrameda")],
        "title_extra": "Lebrija",
        "paragraphs": [
            "<p>Lebrija es una ciudad media del Bajo Guadalquivir sevillano, con una economía agraria potente (algodón, viñedo, hortícolas) y conexión por AVE Sevilla-Cádiz. La <strong>rentabilidad bruta del 7,0%</strong> es de las más altas de Andalucía y refleja el equilibrio entre precios bajos (<strong>1.000€/m²</strong>) y alquileres razonables (<strong>583€/mes</strong>). Es una plaza pensada para cash-flow.</p>",
            "<p>La demanda de alquiler procede de familias locales, trabajadores agrícolas y empleados del sector industrial vinculado al campo. Los <strong>28 días</strong> de absorción exigen paciencia, lo habitual en mercados de tamaño medio del interior andaluz. Zonas: <strong>centro histórico, El Cuartillo y El Carmen</strong>. ITP Andalucía: <strong>7%</strong>. Tesis: comprar barato con yield alto, asumiendo menor liquidez y revalorización moderada. Ideal para inversor con vocación rentista a 8-10 años.</p>",
            ["Bajo Guadalquivir", "Agricultura", "AVE", "Rentista cash-flow"],
        ],
    },
    "lucena": {
        "name": "Lucena",
        "roi": "6,4%", "precio": "900€", "alquiler": "480€/mes", "dias": "22",
        "alts": [("rentabilidad-cabra.html", "Cabra"), ("rentabilidad-cordoba.html", "Córdoba")],
        "title_extra": "Lucena",
        "paragraphs": [
            "<p>Lucena es la segunda ciudad de la provincia de Córdoba y la capital española de la industria del mueble, con un tejido empresarial diverso (frío industrial, agroalimentaria, servicios). El precio medio (<strong>900€/m²</strong>) es muy bajo para una ciudad con su nivel económico, lo que entrega una <strong>rentabilidad bruta del 6,4%</strong>. Alquiler medio: <strong>480€/mes</strong>.</p>",
            "<p>La demanda de alquiler procede de trabajadores industriales, profesionales del sector mueble y familias jóvenes. La actividad económica genera demanda estructural y los <strong>22 días</strong> de absorción son notables para una ciudad de su tamaño en el interior. Zonas: <strong>centro histórico, Las Erillas y entorno polígono</strong>. ITP Andalucía: <strong>7%</strong>. Plaza muy interesante para inversor que busca tickets de entrada por debajo de 70.000€ con yield sólido respaldado por empleo industrial estable.</p>",
            ["Subbética cordobesa", "Industria del mueble", "Empleo industrial", "Ticket bajo"],
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

inserted = []
errors = []

for slug, c in CITIES.items():
    fp = ROOT / f"rentabilidad-{slug}.html"
    if not fp.exists():
        errors.append(f"{slug}: archivo no existe")
        continue
    html = fp.read_text(encoding="utf-8")
    if "<!-- EDITORIAL" in html:
        errors.append(f"{slug}: ya tiene EDITORIAL, salto")
        continue
    if "  <!-- TIPOS DE VIVIENDA -->" not in html:
        errors.append(f"{slug}: no encuentro ancla TIPOS DE VIVIENDA")
        continue

    # parágrafos: c["paragraphs"][:-1] son strings <p>...</p>; c["paragraphs"][-1] es lista de tags
    paragraphs = "\n      ".join(c["paragraphs"][:-1])
    tags = render_tags(c["paragraphs"][-1])
    block = EDITORIAL_TEMPLATE.format(
        SLUG_UP=slug.upper().replace("-", " "),
        NAME=c["name"],
        ROI=c["roi"],
        PRECIO=c["precio"],
        ALQUILER=c["alquiler"],
        DIAS=c["dias"],
        PARAGRAPHS=paragraphs,
        TAGS=tags,
        ALTS=render_alts(c["alts"]),
    )

    new_html = html.replace("  <!-- TIPOS DE VIVIENDA -->", block + "  <!-- TIPOS DE VIVIENDA -->", 1)
    fp.write_text(new_html, encoding="utf-8")
    inserted.append(slug)

print(f"OK insertadas: {len(inserted)}")
for s in inserted:
    print(f"  + {s}")
if errors:
    print("\nERRORES:")
    for e in errors:
        print(f"  ! {e}")
