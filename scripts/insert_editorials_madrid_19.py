"""Genera e inserta editoriales para 19 ciudades de Madrid sin editorial."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

CITIES = {
    "alcobendas": {
        "name": "Alcobendas",
        "roi": "5,4%", "precio": "3.200€", "alquiler": "1.450€/mes", "dias": "22",
        "alts": [("rentabilidad-san-sebastian-de-los-reyes.html", "San Sebastián de los Reyes"), ("rentabilidad-tres-cantos.html", "Tres Cantos")],
        "paragraphs": [
            "<p>Alcobendas es uno de los grandes polos económicos del corredor norte de Madrid, sede de la matriz española de multinacionales (Endesa, Cepsa, Indra, BMW Ibérica) y referencia de oficinas corporativas (Distrito C, Arroyo de la Vega). El precio medio (<strong>3.200€/m²</strong>) es alto, claramente por encima de la media de Madrid metropolitana, y la <strong>rentabilidad bruta del 5,4%</strong> queda en línea con plazas premium. Alquiler medio: <strong>1.450€/mes</strong>.</p>",
            "<p>El inquilino tipo es ejecutivo o profesional cualificado de las multinacionales del Distrito C, frecuentemente expatriado o nacional con relocación corporativa. Esto sostiene un mercado de alquiler residencial premium con contratos de 2-3 años y precios elevados. Los <strong>22 días</strong> de absorción confirman demanda firme. Zonas: <strong>La Moraleja (chalets premium), Arroyo de la Vega y Valdelasfuentes</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 3 dormitorios cerca del Distrito C para alquiler corporativo, con apreciación apoyada en demanda inelástica de oficinas.</p>",
            ["Corredor norte Madrid", "Distrito C", "Alquiler corporativo", "La Moraleja"],
        ],
    },
    "aranjuez": {
        "name": "Aranjuez",
        "roi": "5,8%", "precio": "2.000€", "alquiler": "966€/mes", "dias": "21",
        "alts": [("rentabilidad-pinto.html", "Pinto"), ("rentabilidad-toledo.html", "Toledo")],
        "paragraphs": [
            "<p>Aranjuez es un caso atípico en la Comunidad de Madrid: una ciudad real con Patrimonio Mundial UNESCO (Palacio Real, Jardines, Casa del Labrador), 50 km al sur de Madrid capital y enclave histórico-cultural único. Combina turismo cultural creciente con población local, y conexión por Cercanías C-3. Precio medio: <strong>2.000€/m²</strong> — muy por debajo de la media de Madrid CCAA — con <strong>rentabilidad bruta del 5,8%</strong>.</p>",
            "<p>La demanda combina familias locales, profesionales que prefieren huir del precio madrileño y un nicho de turismo cultural que abre la puerta a explotación VUT controlada. Alquiler medio: <strong>966€/mes</strong>; <strong>21 días</strong> de absorción reflejan mercado activo. Zonas: <strong>centro histórico (regulado), Las Aves y Foso</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso urbano para alquiler residencial estable, con un precio de entrada accesible y exposición indirecta a la presión madrileña sin pagar prima metropolitana.</p>",
            ["Sur de Madrid", "UNESCO", "Cercanías C-3", "Ticket bajo para Madrid"],
        ],
    },
    "arroyomolinos": {
        "name": "Arroyomolinos",
        "roi": "5,6%", "precio": "2.400€", "alquiler": "1.120€/mes", "dias": "19",
        "alts": [("rentabilidad-mostoles.html", "Móstoles"), ("rentabilidad-pinto.html", "Pinto")],
        "paragraphs": [
            "<p>Arroyomolinos es uno de los municipios de mayor crecimiento poblacional de la Comunidad de Madrid en las últimas dos décadas, impulsado por desarrollos residenciales nuevos y por el centro comercial Xanadú como referencia comercial y de ocio del suroeste. La conexión por la M-407 y M-50 lo integra plenamente en la corona metropolitana sur. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>.</p>",
            "<p>El perfil de inquilino es muy claro: familias jóvenes con hijos pequeños que trabajan en el sur de Madrid o en la propia ciudad capital y buscan vivienda nueva, espaciosa y asequible respecto al núcleo urbano. Los <strong>19 días</strong> de absorción son de los más rápidos de Madrid CCAA. Zonas: <strong>El Caracol, Casco Antiguo y nuevas urbanizaciones del entorno Xanadú</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso o adosado de 3 dormitorios para alquiler familiar largo plazo, con yield estable y demanda creciente.</p>",
            ["Suroeste Madrid", "Xanadú", "Crecimiento poblacional", "Familias jóvenes"],
        ],
    },
    "boadilla-del-monte": {
        "name": "Boadilla del Monte",
        "roi": "4,8%", "precio": "3.200€", "alquiler": "1.280€/mes", "dias": "18",
        "alts": [("rentabilidad-pozuelo-de-alarcon.html", "Pozuelo de Alarcón"), ("rentabilidad-las-rozas.html", "Las Rozas")],
        "paragraphs": [
            "<p>Boadilla del Monte es uno de los municipios residenciales premium del oeste madrileño, con perfil de clase alta-media alta, urbanizaciones de chalets, varios campos de golf (Las Lomas, Olivar de la Hinojosa) y la sede corporativa de Banco Santander (Ciudad Grupo Santander). El precio medio (<strong>3.200€/m²</strong>) refleja la calidad del entorno y la <strong>rentabilidad bruta del 4,8%</strong> es típica de plaza residencial alta gama.</p>",
            "<p>La demanda procede de familias profesionales con alto poder adquisitivo, frecuentemente vinculadas a Santander o a empresas del oeste de Madrid. Alquiler medio: <strong>1.280€/mes</strong>; <strong>18 días</strong> de absorción — entre los más rápidos de la CCAA, mercado muy tensionado. Zonas: <strong>Casco urbano, Valdecabañas y Bonanza</strong>. ITP Madrid: <strong>6%</strong>. Tesis: chalet o piso amplio para alquiler familiar premium, jugando apreciación a 5-7 años más que yield puro. Bajo riesgo, baja rentabilidad bruta, alta liquidez.</p>",
            ["Oeste Madrid premium", "Santander HQ", "Golf", "Apreciación"],
        ],
    },
    "collado-villalba": {
        "name": "Collado Villalba",
        "roi": "6,5%", "precio": "2.400€", "alquiler": "1.000€/mes", "dias": "22",
        "alts": [("rentabilidad-galapagar.html", "Galapagar"), ("rentabilidad-torrelodones.html", "Torrelodones")],
        "paragraphs": [
            "<p>Collado Villalba es la cabecera de la Sierra de Guadarrama y una de las ciudades dormitorio mejor conectadas con Madrid (Cercanías C-3, C-8, C-9 y A-6). Combina población residencial estable, comercio comarcal y un volumen importante de jóvenes profesionales que escogen vivir en la sierra y trabajar en la capital. El precio medio (<strong>2.400€/m²</strong>) y el <strong>ROI bruto del 6,5%</strong> ofrecen una de las mejores combinaciones de yield/precio de Madrid CCAA.</p>",
            "<p>El inquilino tipo es muy diverso: jóvenes, familias, parejas que trabajan en Madrid pero priorizan calidad de vida (sierra, aire limpio, naturaleza). Alquiler medio: <strong>1.000€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>casco urbano, La Estación y Pueblo</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 2-3 dormitorios cerca de la estación de cercanías para alquiler residencial estable, capturando yield superior a Las Rozas o Majadahonda con menos prima por marca.</p>",
            ["Sierra Guadarrama", "Cercanías", "Yield superior", "Ciudad dormitorio"],
        ],
    },
    "coslada": {
        "name": "Coslada",
        "roi": "5,5%", "precio": "2.600€", "alquiler": "1.200€/mes", "dias": "22",
        "alts": [("rentabilidad-san-fernando-de-henares.html", "San Fernando de Henares"), ("rentabilidad-torrejon-de-ardoz.html", "Torrejón de Ardoz")],
        "paragraphs": [
            "<p>Coslada es un nodo logístico estratégico del Corredor del Henares, con el Centro de Transportes (CTC) y Mercamadrid II generando un volumen muy alto de empleo. La cercanía a Barajas (5 km) la convierte en residencia natural para personal aeroportuario, y la conexión por Metro Línea 7 y Cercanías C-7 la integra plenamente en Madrid. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.200€/mes</strong>.</p>",
            "<p>El inquilino tipo es trabajador del sector logístico, personal de Iberia y AENA (Barajas) y profesionales que valoran la conexión al aeropuerto y a Madrid centro. Los <strong>22 días</strong> de absorción confirman demanda estable. Zonas: <strong>Ciudad 70, El Cañaveral y entorno Metro</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso bien conectado a Metro/Cercanías para alquiler residencial estable apoyado en empleo logístico-aeroportuario, sector con crecimiento estructural y baja sensibilidad al ciclo.</p>",
            ["Corredor del Henares", "Logístico", "Barajas", "Metro 7"],
        ],
    },
    "galapagar": {
        "name": "Galapagar",
        "roi": "5,4%", "precio": "2.600€", "alquiler": "1.170€/mes", "dias": "19",
        "alts": [("rentabilidad-collado-villalba.html", "Collado Villalba"), ("rentabilidad-torrelodones.html", "Torrelodones")],
        "paragraphs": [
            "<p>Galapagar es un municipio residencial de la sierra noroeste de Madrid, con perfil de chalets adosados y unifamiliares, mucha presencia de familias con hijos y figuras públicas (Felipe VI residió aquí antes de la jefatura del Estado). La cercanía a Madrid por la A-6 y Cercanías C-8 se combina con un entorno natural privilegiado. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,4%</strong>; alquiler medio <strong>1.170€/mes</strong>.</p>",
            "<p>La demanda procede de familias con poder adquisitivo medio-alto que trabajan en Madrid y buscan calidad de vida residencial con espacio. Los <strong>19 días</strong> de absorción reflejan mercado muy líquido, de los más rápidos de la sierra. Zonas: <strong>La Navata, Casco Urbano y Mataespesa</strong>. ITP Madrid: <strong>6%</strong>. Tesis: chalet o adosado para alquiler familiar de larga duración, con yield estable y revalorización apoyada en demanda residencial sierra noroeste.</p>",
            ["Sierra noroeste Madrid", "Residencial familiar", "Mercado líquido", "Adosados"],
        ],
    },
    "las-rozas": {
        "name": "Las Rozas",
        "roi": "5,1%", "precio": "3.800€", "alquiler": "1.620€/mes", "dias": "22",
        "alts": [("rentabilidad-majadahonda.html", "Majadahonda"), ("rentabilidad-pozuelo-de-alarcon.html", "Pozuelo de Alarcón")],
        "paragraphs": [
            "<p>Las Rozas de Madrid es uno de los municipios estrella del corredor noroeste, con las sedes corporativas de Microsoft, Real Madrid (Ciudad Real Madrid en Valdebebas, junto al término), Bankinter y un volumen muy alto de empresas tecnológicas. El perfil residencial es premium, con urbanizaciones de chalets y pisos modernos. El precio medio (<strong>3.800€/m²</strong>) está entre los más altos de la CCAA y la <strong>rentabilidad bruta del 5,1%</strong> es la habitual en plaza alta gama.</p>",
            "<p>El inquilino tipo es ejecutivo o profesional cualificado vinculado a las multinacionales del corredor A-6 o de Madrid. Alquiler medio: <strong>1.620€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Monte Rozas, Las Matas y Európolis</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso amplio o chalet pareado para alquiler corporativo de 2-3 años, jugando combinación de yield estable y apreciación apoyada en demanda inelástica de tecnológicas.</p>",
            ["Noroeste Madrid", "Microsoft HQ", "Corporativo", "Alta gama"],
        ],
    },
    "majadahonda": {
        "name": "Majadahonda",
        "roi": "5,2%", "precio": "3.600€", "alquiler": "1.560€/mes", "dias": "22",
        "alts": [("rentabilidad-las-rozas.html", "Las Rozas"), ("rentabilidad-pozuelo-de-alarcon.html", "Pozuelo de Alarcón")],
        "paragraphs": [
            "<p>Majadahonda es uno de los municipios premium del oeste de Madrid, con el Hospital Universitario Puerta de Hierro (referencia nacional) como motor sanitario y un perfil residencial de clase media-alta consolidado. La conexión por A-6, Cercanías C-7 y M-50 la integra plenamente en Madrid. Precio medio: <strong>3.600€/m²</strong>; <strong>rentabilidad bruta 5,2%</strong>; alquiler medio <strong>1.560€/mes</strong>.</p>",
            "<p>La demanda combina personal sanitario del Puerta de Hierro (médicos, residentes MIR), familias profesionales y un creciente componente de jóvenes profesionales que trabajan en Madrid. Los <strong>22 días</strong> de absorción confirman mercado tensionado. Zonas: <strong>Centro, Monte del Pilar y entorno Hospital</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 2-3 dormitorios próximo al Hospital para alquiler a personal sanitario (residentes MIR rotan cada año), nicho con demanda inelástica y rotación previsible.</p>",
            ["Oeste Madrid", "Hospital Puerta de Hierro", "Alquiler sanitario", "Residencial premium"],
        ],
    },
    "paracuellos-de-jarama": {
        "name": "Paracuellos de Jarama",
        "roi": "5,5%", "precio": "2.600€", "alquiler": "1.190€/mes", "dias": "18",
        "alts": [("rentabilidad-coslada.html", "Coslada"), ("rentabilidad-san-fernando-de-henares.html", "San Fernando de Henares")],
        "paragraphs": [
            "<p>Paracuellos de Jarama es un municipio residencial al este de Madrid, junto al aeropuerto de Barajas (Terminal 4), con un crecimiento poblacional notable en la última década gracias a desarrollos urbanísticos como Belvis y Miramadrid. La cercanía al aeropuerto y la conexión por A-2 y M-50 lo integran plenamente en la corona metropolitana este. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>.</p>",
            "<p>El inquilino tipo es personal aeroportuario de Barajas (pilotos, tripulaciones, controladores), familias jóvenes y profesionales del corredor del Henares. Alquiler medio: <strong>1.190€/mes</strong>; <strong>18 días</strong> de absorción — entre los más rápidos de la CCAA. Zonas: <strong>Belvis del Jarama, Miramadrid y casco urbano</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso o chalet adosado para alquiler residencial estable apoyado en empleo aeroportuario, con liquidez muy alta y yield superior a la media del corredor.</p>",
            ["Este Madrid", "Junto a Barajas", "Personal aeroportuario", "Alta liquidez"],
        ],
    },
    "pinto": {
        "name": "Pinto",
        "roi": "6,5%", "precio": "2.200€", "alquiler": "1.010€/mes", "dias": "22",
        "alts": [("rentabilidad-getafe.html", "Getafe"), ("rentabilidad-aranjuez.html", "Aranjuez")],
        "paragraphs": [
            "<p>Pinto es una ciudad media del sur de Madrid, integrada en la corona metropolitana sur, con un tejido económico equilibrado: polígonos industriales (Las Arenas, Las Ánimas), comercio y residencial. La conexión por Cercanías C-3 y A-4 la sitúa a 25 minutos de Madrid centro. El precio medio (<strong>2.200€/m²</strong>) y el <strong>ROI bruto del 6,5%</strong> la convierten en una de las mejores combinaciones yield/precio del sur madrileño.</p>",
            "<p>La demanda procede de familias jóvenes, trabajadores de los polígonos industriales y profesionales del sur de Madrid. Alquiler medio: <strong>1.010€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>El Egido, Casco Antiguo y Las Cristinas</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 2-3 dormitorios para alquiler familiar estable, con yield muy superior al de Getafe o Leganés y demanda apoyada en presión demográfica del sur metropolitano.</p>",
            ["Sur Madrid", "Cercanías C-3", "Yield alto para Madrid", "Polígonos industriales"],
        ],
    },
    "pozuelo-de-alarcon": {
        "name": "Pozuelo de Alarcón",
        "roi": "4,9%", "precio": "4.200€", "alquiler": "1.720€/mes", "dias": "22",
        "alts": [("rentabilidad-las-rozas.html", "Las Rozas"), ("rentabilidad-majadahonda.html", "Majadahonda")],
        "paragraphs": [
            "<p>Pozuelo de Alarcón es el municipio con mayor renta per cápita de España según los registros del INE, plaza residencial premium absoluta del oeste de Madrid, con urbanizaciones como Monte Alina, La Finca o Húmera concentrando el segmento más alto del mercado madrileño. El precio medio (<strong>4.200€/m²</strong>) es de los más altos de la CCAA y la <strong>rentabilidad bruta del 4,9%</strong> es la habitual en residencial ultra-premium.</p>",
            "<p>El inquilino es ejecutivo, alta dirección, deportista de élite o profesional liberal, con alquileres por encima de mercado y exigencias muy específicas (seguridad, servicios, calidad). Alquiler medio: <strong>1.720€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>La Finca, Monte Alina, Húmera y Casco Urbano</strong>. ITP Madrid: <strong>6%</strong>. Tesis: chalet o piso de lujo para alquiler patrimonialista, con foco absoluto en revalorización a 5-7 años y conservación de capital. Yield secundario.</p>",
            ["Oeste Madrid ultra-premium", "Mayor renta per cápita España", "Alta dirección", "Conservación de capital"],
        ],
    },
    "rivas-vaciamadrid": {
        "name": "Rivas-Vaciamadrid",
        "roi": "6,5%", "precio": "2.800€", "alquiler": "1.260€/mes", "dias": "22",
        "alts": [("rentabilidad-arganda-del-rey.html", "Arganda del Rey"), ("rentabilidad-coslada.html", "Coslada")],
        "paragraphs": [
            "<p>Rivas-Vaciamadrid es uno de los municipios más jóvenes y de crecimiento más rápido de la Comunidad de Madrid, con un perfil demográfico singular: la edad media más baja de la CCAA, alto número de familias jóvenes, identidad ecologista y participación cívica intensa. Conexión por Metro Línea 9 y A-3. Precio medio: <strong>2.800€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación excepcional para el sureste madrileño.</p>",
            "<p>El inquilino tipo es familia joven con hijos pequeños o pareja milenial, frecuentemente con perfil profesional y valores progresistas. Alquiler medio: <strong>1.260€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Rivas Centro, Rivas Pueblo, Cristo de Rivas y Pablo Iglesias</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 3 dormitorios para alquiler familiar largo plazo, capturando una de las mejores combinaciones yield/apreciación del sureste con demografía estructuralmente fuerte.</p>",
            ["Sureste Madrid", "Metro Línea 9", "Familias jóvenes", "Demografía favorable"],
        ],
    },
    "san-fernando-de-henares": {
        "name": "San Fernando de Henares",
        "roi": "5,6%", "precio": "2.200€", "alquiler": "1.025€/mes", "dias": "19",
        "alts": [("rentabilidad-coslada.html", "Coslada"), ("rentabilidad-torrejon-de-ardoz.html", "Torrejón de Ardoz")],
        "paragraphs": [
            "<p>San Fernando de Henares es un municipio del Corredor del Henares, conurbado con Coslada y bien conectado por Metro Línea 7 y Cercanías C-2/C-7. Su tejido económico combina logística, industria moderada y un componente residencial creciente. El precio medio (<strong>2.200€/m²</strong>) es uno de los más asequibles del corredor próximo a Madrid, con <strong>rentabilidad bruta del 5,6%</strong>. Alquiler medio: <strong>1.025€/mes</strong>.</p>",
            "<p>La demanda procede de trabajadores logísticos, personal de Iberia/AENA, jóvenes profesionales y familias que buscan vivienda asequible bien conectada con Madrid. Los <strong>19 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>El Quiñón, Casco Urbano y entorno Metro</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 2 dormitorios próximo a Metro Línea 7 para alquiler residencial a jóvenes profesionales, con entrada moderada para Madrid CCAA y yield decente.</p>",
            ["Corredor del Henares", "Metro Línea 7", "Logístico", "Entrada moderada"],
        ],
    },
    "san-lorenzo-de-el-escorial": {
        "name": "San Lorenzo de El Escorial",
        "roi": "5,2%", "precio": "2.800€", "alquiler": "1.213€/mes", "dias": "20",
        "alts": [("rentabilidad-collado-villalba.html", "Collado Villalba"), ("rentabilidad-galapagar.html", "Galapagar")],
        "paragraphs": [
            "<p>San Lorenzo de El Escorial alberga el Real Sitio del Monasterio de El Escorial — Patrimonio Mundial UNESCO desde 1984 — y es uno de los municipios serranos más singulares de Madrid. Combina turismo cultural sostenido, residencial de clase media-alta y la sede de los cursos de verano de la Universidad Complutense. Precio medio: <strong>2.800€/m²</strong>; <strong>rentabilidad bruta 5,2%</strong>; alquiler medio <strong>1.213€/mes</strong>.</p>",
            "<p>La demanda combina familias residentes permanentes, profesionales que trabajan en Madrid y un nicho de turismo cultural que abre la puerta a explotación VUT (con regulación creciente por el peso patrimonial). Los <strong>20 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Casco Histórico (regulado), Las Zorreras y Los Arroyos</strong>. ITP Madrid: <strong>6%</strong>. Tesis: vivienda con encanto en zona protegida para combinar VUT cultural con residencial estable, dual interesante en plaza con marca turística sólida.</p>",
            ["Sierra Madrid", "UNESCO", "Turismo cultural", "Mixto residencial/VUT"],
        ],
    },
    "san-sebastian-de-los-reyes": {
        "name": "San Sebastián de los Reyes",
        "roi": "5,4%", "precio": "2.900€", "alquiler": "1.310€/mes", "dias": "22",
        "alts": [("rentabilidad-alcobendas.html", "Alcobendas"), ("rentabilidad-tres-cantos.html", "Tres Cantos")],
        "paragraphs": [
            "<p>San Sebastián de los Reyes — Sanse — está conurbado con Alcobendas formando uno de los grandes polos del corredor norte de Madrid. Combina perfil residencial, comercio (Plaza Norte 2, Megapark) y un volumen importante de oficinas y empresas. Conexión por Cercanías C-4 y A-1. Precio medio: <strong>2.900€/m²</strong>; <strong>rentabilidad bruta 5,4%</strong>; alquiler medio <strong>1.310€/mes</strong>.</p>",
            "<p>El inquilino tipo es familia joven o profesional cualificado vinculado a las empresas del corredor norte (incluido el Distrito C de Alcobendas), con preferencia por vivienda más amplia que en Madrid capital. Los <strong>22 días</strong> de absorción confirman demanda firme. Zonas: <strong>Tempranales, Dehesa Vieja y casco</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 3 dormitorios cerca de Cercanías para alquiler familiar largo plazo, jugando combinación de yield decente y apreciación apoyada en demanda corporativa del eje Alcobendas-Sanse.</p>",
            ["Corredor norte Madrid", "Conurbado Alcobendas", "Plaza Norte 2", "Familiar"],
        ],
    },
    "torrejon-de-ardoz": {
        "name": "Torrejón de Ardoz",
        "roi": "6,5%", "precio": "2.600€", "alquiler": "1.210€/mes", "dias": "22",
        "alts": [("rentabilidad-coslada.html", "Coslada"), ("rentabilidad-alcala-de-henares.html", "Alcalá de Henares")],
        "paragraphs": [
            "<p>Torrejón de Ardoz es la cuarta ciudad por población de la Comunidad de Madrid y uno de los polos industriales-logísticos del Corredor del Henares, con la Base Aérea de Torrejón (Cuartel General del Mando Aéreo de Combate) como motor económico institucional clave. Conexión por Cercanías C-2/C-7 y A-2. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación excepcional para Madrid CCAA.</p>",
            "<p>La demanda combina trabajadores industriales, personal militar de la Base, logística y familias jóvenes. Alquiler medio: <strong>1.210€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Soto del Henares, Veredillas y centro</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 2-3 dormitorios para alquiler residencial estable, con yield superior al de Coslada o San Fernando y demanda multifuente (industrial, militar, familiar) que reduce riesgo de concentración.</p>",
            ["Corredor del Henares", "Base Aérea Torrejón", "Yield alto Madrid", "Demanda diversificada"],
        ],
    },
    "torrelodones": {
        "name": "Torrelodones",
        "roi": "5,1%", "precio": "3.000€", "alquiler": "1.275€/mes", "dias": "19",
        "alts": [("rentabilidad-las-rozas.html", "Las Rozas"), ("rentabilidad-galapagar.html", "Galapagar")],
        "paragraphs": [
            "<p>Torrelodones es uno de los municipios premium de la sierra noroeste madrileña, con perfil de chalets unifamiliares, gran calidad medioambiental (parque regional del Manzanares) y excelente conexión con Madrid por A-6 y Cercanías C-8. La renta per cápita está entre las más altas de la CCAA. Precio medio: <strong>3.000€/m²</strong>; <strong>rentabilidad bruta 5,1%</strong>; alquiler medio <strong>1.275€/mes</strong>.</p>",
            "<p>El inquilino tipo es familia profesional con alto poder adquisitivo que prioriza calidad de vida sierra + conectividad a Madrid. Los <strong>19 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Pueblo, Colonia y Bomberos</strong>. ITP Madrid: <strong>6%</strong>. Tesis: chalet o piso amplio para alquiler familiar de larga duración, con perfil patrimonialista enfocado en preservación de capital y revalorización moderada por escasez relativa de oferta nueva.</p>",
            ["Sierra noroeste Madrid", "Premium", "Mercado líquido", "Patrimonialista"],
        ],
    },
    "tres-cantos": {
        "name": "Tres Cantos",
        "roi": "6,5%", "precio": "3.200€", "alquiler": "1.380€/mes", "dias": "22",
        "alts": [("rentabilidad-alcobendas.html", "Alcobendas"), ("rentabilidad-colmenar-viejo.html", "Colmenar Viejo")],
        "paragraphs": [
            "<p>Tres Cantos es la única ciudad planificada ex-novo de la Comunidad de Madrid (años 70-80), un municipio joven con un perfil tecnológico singular: parque empresarial con sede de Hewlett Packard, GMV, Roche Farma y diversas tecnológicas e I+D. Conexión por Cercanías C-4 y A-1. Precio medio: <strong>3.200€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación inusual de plaza premium + yield alto.</p>",
            "<p>El inquilino tipo es ingeniero, profesional tecnológico o investigador vinculado al parque empresarial, con preferencia por vivienda amplia, urbanismo ordenado (anchas avenidas, abundantes zonas verdes) y servicios de calidad. Alquiler medio: <strong>1.380€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Sector Pintores, Sector Literatos y entorno PCM</strong>. ITP Madrid: <strong>6%</strong>. Tesis: piso de 2-3 dormitorios cerca de Cercanías para alquiler corporativo a profesionales tech, yield notable + demanda inelástica del polo I+D.</p>",
            ["Norte Madrid", "Tecnológico I+D", "Ciudad planificada", "Yield alto premium"],
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
