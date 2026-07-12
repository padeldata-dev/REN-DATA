"""Genera e inserta editoriales para 27 ciudades de Cataluña sin editorial."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

CITIES = {
    "banyoles": {
        "name": "Banyoles",
        "roi": "5,6%", "precio": "2.200€", "alquiler": "1.023€/mes", "dias": "22",
        "alts": [("rentabilidad-girona.html", "Girona"), ("rentabilidad-olot.html", "Olot")],
        "paragraphs": [
            "<p>Banyoles es la capital del Pla de l'Estany gerundense, conocida internacionalmente por su lago natural — sede de las pruebas olímpicas de remo en Barcelona 92 — y por un casco antiguo medieval bien conservado. Combina turismo deportivo y de naturaleza, agroindustria, sector cárnico y servicios comarcales. Conexión por A-26 a 18 km de Girona. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>1.023€/mes</strong>.</p>",
            "<p>El inquilino tipo combina familias locales, profesionales que trabajan en Girona y un nicho de deportistas (remo, triatlón) y turismo activo. Los <strong>22 días</strong> de absorción reflejan mercado equilibrado. Zonas: <strong>Centre Històric, La Farga y entorno del lago</strong>. ITP Catalunya: <strong>10%</strong> (encarece la operación). Tesis: piso urbano para alquiler residencial estable, con potencial complementario de VUT puntual ligado a eventos deportivos. Plaza con marca consolidada y demanda diversificada.</p>",
            ["Pla de l'Estany", "Lago natural", "Olímpico remo", "Cerca de Girona"],
        ],
    },
    "calafell": {
        "name": "Calafell",
        "roi": "5,7%", "precio": "2.200€", "alquiler": "1.045€/mes", "dias": "21",
        "alts": [("rentabilidad-cunit.html", "Cunit"), ("rentabilidad-vilanova-i-la-geltru.html", "Vilanova i la Geltrú")],
        "paragraphs": [
            "<p>Calafell es uno de los municipios costeros consolidados de la Costa Daurada tarraconense, con tres núcleos diferenciados (Pueblo, Playa, Segur) y un perfil turístico-residencial maduro. La cercanía a Barcelona (50 minutos por R2 sur) y a Tarragona, junto con la AP-7, sostienen una demanda dual: segunda residencia y residencial permanente creciente. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,7%</strong>.</p>",
            "<p>El alquiler medio (<strong>1.045€/mes</strong>) y los <strong>21 días</strong> de absorción confirman demanda firme. La estacionalidad VUT es marcada en julio-agosto. Zonas: <strong>Calafell Platja (turística), Segur de Calafell y casco urbano</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso en Segur o Platja para combinar alquiler residencial todo el año con VUT de temporada. Plaza con buen equilibrio entre yield medio y apreciación apoyada en presión turística sostenida.</p>",
            ["Costa Daurada", "R2 cercanías", "Turismo familiar", "VUT estacional"],
        ],
    },
    "calella": {
        "name": "Calella",
        "roi": "5,7%", "precio": "2.200€", "alquiler": "1.045€/mes", "dias": "21",
        "alts": [("rentabilidad-pineda-de-mar.html", "Pineda de Mar"), ("rentabilidad-malgrat-de-mar.html", "Malgrat de Mar")],
        "paragraphs": [
            "<p>Calella es uno de los nodos turísticos clásicos del Maresme barcelonés, con un perfil muy enfocado al turismo familiar internacional (especialmente alemán, británico y centroeuropeo) y una concentración hotelera de las más altas de Cataluña. Conexión por R1 a Barcelona (80 minutos) y N-II/AP-7. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,7%</strong>; alquiler medio <strong>1.045€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector hotelero (residencial estable), familias locales y un componente turístico estacional para VUT. Los <strong>21 días</strong> de absorción confirman mercado activo. Zonas: <strong>Centro, paseo marítimo y entorno R1</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable a personal hotelero (rotación previsible) o VUT estival. Plaza con dinámica turística estructural pero mercado maduro y precios contenidos.</p>",
            ["Maresme", "Turismo internacional", "R1 Cercanías", "Hostelería"],
        ],
    },
    "castello-d-empuries": {
        "name": "Castelló d'Empúries",
        "roi": "5,8%", "precio": "2.400€", "alquiler": "1.160€/mes", "dias": "20",
        "alts": [("rentabilidad-roses.html", "Roses"), ("rentabilidad-l-escala.html", "L'Escala")],
        "paragraphs": [
            "<p>Castelló d'Empúries es un municipio del Alt Empordà gerundense con dos realidades muy diferenciadas: el casco histórico medieval (capital del antiguo Comtat d'Empúries, con la Basílica de Santa María) y <strong>Empuriabrava</strong> — la mayor marina residencial de Europa, con más de 30 km de canales navegables y aeródromo propio. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>1.160€/mes</strong>.</p>",
            "<p>El inquilino tipo es muy específico de Empuriabrava: residentes europeos (alemanes, holandeses, franceses, suizos) que buscan vivienda con amarre privado o turismo náutico, paracaidismo y golf. Los <strong>20 días</strong> de absorción reflejan mercado muy líquido. Zonas: <strong>Empuriabrava (canales), Casco Histórico y Sant Mori</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: vivienda con amarre en Empuriabrava para alquiler residencial a comunidad europea + VUT náutico estival. Nicho premium muy específico.</p>",
            ["Alt Empordà", "Empuriabrava", "Marina europea", "Demanda náutica"],
        ],
    },
    "cerdanyola-del-valles": {
        "name": "Cerdanyola del Vallès",
        "roi": "6,5%", "precio": "2.800€", "alquiler": "1.220€/mes", "dias": "22",
        "alts": [("rentabilidad-sant-cugat-del-valles.html", "Sant Cugat del Vallès"), ("rentabilidad-rubi.html", "Rubí")],
        "paragraphs": [
            "<p>Cerdanyola del Vallès es uno de los municipios más singulares del Vallès Occidental: alberga el campus principal de la <strong>Universitat Autònoma de Barcelona (UAB)</strong> — una de las mayores universidades de España — y el <strong>Sincrotrón ALBA</strong>, infraestructura científica de primer nivel europeo. La demanda universitaria y científica es estructural. Precio medio: <strong>2.800€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para el área metropolitana de Barcelona.</p>",
            "<p>El inquilino tipo es estudiante de la UAB, profesor o investigador (con contratos rotatorios), personal del Sincrotrón y profesionales que trabajan en Barcelona o Sabadell. Alquiler medio: <strong>1.220€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Centre, Bellaterra (campus UAB) y entorno FGC</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso compartido o estudio próximo al campus UAB para alquiler estudiantil rotatorio (yield superior a residencial), demanda inelástica universitaria.</p>",
            ["Vallès Occidental", "UAB", "Sincrotrón ALBA", "Alquiler estudiantil"],
        ],
    },
    "el-prat-de-llobregat": {
        "name": "El Prat de Llobregat",
        "roi": "6,5%", "precio": "2.500€", "alquiler": "1.120€/mes", "dias": "22",
        "alts": [("rentabilidad-viladecans.html", "Viladecans"), ("rentabilidad-sant-boi-de-llobregat.html", "Sant Boi de Llobregat")],
        "paragraphs": [
            "<p>El Prat de Llobregat es la sede del Aeropuerto Josep Tarradellas Barcelona-El Prat — uno de los mayores hubs aéreos de Europa — y un nodo logístico-industrial estratégico del Baix Llobregat. La conexión por Metro Línea 9 sud, Cercanías R2 y proximidad al puerto de Barcelona refuerzan su perfil. Precio medio: <strong>2.500€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>1.120€/mes</strong>.</p>",
            "<p>El inquilino tipo es personal aeroportuario (AENA, compañías aéreas, handling), trabajadores logísticos y familias jóvenes que valoran la conexión aérea internacional. Los <strong>22 días</strong> de absorción reflejan demanda estructural firme. Zonas: <strong>Centre, Sant Cosme y entorno Metro L9</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo a Metro/aeropuerto para alquiler residencial estable apoyado en empleo aeroportuario, sector con crecimiento estructural y baja sensibilidad cíclica.</p>",
            ["Baix Llobregat", "Aeropuerto BCN", "Metro L9", "Demanda aeroportuaria"],
        ],
    },
    "esplugues-de-llobregat": {
        "name": "Esplugues de Llobregat",
        "roi": "6,5%", "precio": "3.000€", "alquiler": "1.280€/mes", "dias": "22",
        "alts": [("rentabilidad-sant-just-desvern.html", "Sant Just Desvern"), ("rentabilidad-cornella-de-llobregat.html", "Cornellà de Llobregat")],
        "paragraphs": [
            "<p>Esplugues de Llobregat es un municipio del Baix Llobregat conurbado con Barcelona por el oeste, sede del <strong>Hospital Sant Joan de Déu</strong> (referencia pediátrica europea) y de la sede corporativa de Areas. Combina perfil residencial de clase media-alta con un componente sanitario importante. Precio medio: <strong>3.000€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación muy buena para una plaza tan próxima a Barcelona.</p>",
            "<p>El inquilino tipo es personal sanitario del Sant Joan de Déu (médicos, residentes MIR, enfermería), profesionales corporativos y familias que prefieren huir del precio barcelonés. Alquiler medio: <strong>1.280€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Centre, Can Vidalet y Finestrelles (junto al Hospital)</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2 dormitorios próximo al Hospital para alquiler a personal sanitario rotatorio (residentes MIR), nicho con demanda inelástica.</p>",
            ["Baix Llobregat", "Hospital Sant Joan de Déu", "Conurbado Barcelona", "Sanitario MIR"],
        ],
    },
    "gava": {
        "name": "Gavà",
        "roi": "6,5%", "precio": "3.200€", "alquiler": "1.400€/mes", "dias": "22",
        "alts": [("rentabilidad-castelldefels.html", "Castelldefels"), ("rentabilidad-viladecans.html", "Viladecans")],
        "paragraphs": [
            "<p>Gavà es un municipio costero del Baix Llobregat barcelonés, con un perfil dual: núcleo urbano interior bien conectado con Barcelona (R2 sur, Metro L9) y la zona costera de <strong>Gavà Mar</strong>, con urbanizaciones residenciales premium junto al Parque Natural del Garraf. Precio medio: <strong>3.200€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación premium con yield notable.</p>",
            "<p>El inquilino tipo combina familias profesionales que trabajan en Barcelona y buscan calidad de vida costera, junto con profesionales del Hospital de Viladecans y del entorno aeroportuario. Alquiler medio: <strong>1.400€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Gavà Mar (premium), Centre y Pla de Queralt</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso o adosado en Gavà Mar para alquiler residencial premium familiar, capturando combinación de calidad de vida costera + conexión Barcelona.</p>",
            ["Baix Llobregat", "Gavà Mar", "R2 sur", "Premium costero"],
        ],
    },
    "granollers": {
        "name": "Granollers",
        "roi": "5,6%", "precio": "2.200€", "alquiler": "1.020€/mes", "dias": "22",
        "alts": [("rentabilidad-mollet-del-valles.html", "Mollet del Vallès"), ("rentabilidad-sabadell.html", "Sabadell")],
        "paragraphs": [
            "<p>Granollers es la capital del Vallès Oriental, con uno de los tejidos industriales más diversificados de Cataluña (industria cárnica, química, automóvil, logística) y referencia comarcal en servicios. Conexión por R2 norte y AP-7 a 30 minutos de Barcelona. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>1.020€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores industriales, profesionales del comercio y servicios, y un componente creciente de jóvenes que buscan alternativa a Sabadell o Barcelona. Los <strong>22 días</strong> de absorción reflejan mercado estable. Zonas: <strong>Centre, Sant Miquel y Hostal d'en Quart</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios cerca del centro para alquiler residencial estable, apoyado en empleo industrial diversificado y demanda comarcal sostenida. Plaza media con buena liquidez.</p>",
            ["Vallès Oriental", "Industrial diversificado", "R2 norte", "Capital comarcal"],
        ],
    },
    "igualada": {
        "name": "Igualada",
        "roi": "6,0%", "precio": "1.800€", "alquiler": "900€/mes", "dias": "23",
        "alts": [("rentabilidad-vilafranca-del-penedes.html", "Vilafranca del Penedès"), ("rentabilidad-manresa.html", "Manresa")],
        "paragraphs": [
            "<p>Igualada es la capital de la Anoia barcelonesa, con un patrimonio industrial muy singular: cuna histórica del curtido de pieles en España (Barri del Rec, conjunto industrial protegido) y referencia textil-tecnológica. La conexión por A-2 y FGC (Línia Llobregat-Anoia) la sitúa a 65 km de Barcelona. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>; alquiler medio <strong>900€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores industriales (piel, textil, química), profesionales sanitarios del Hospital d'Igualada y servicios comarcales. Los <strong>23 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centre, Sant Crist y entorno FGC</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable, con yield decente y entrada moderada. Plaza con identidad propia y motor económico industrial diferenciado del eje litoral barcelonés.</p>",
            ["Anoia", "Curtidos históricos", "FGC", "Capital comarcal"],
        ],
    },
    "l-escala": {
        "name": "L'Escala",
        "roi": "5,5%", "precio": "2.600€", "alquiler": "1.190€/mes", "dias": "20",
        "alts": [("rentabilidad-castello-d-empuries.html", "Castelló d'Empúries"), ("rentabilidad-roses.html", "Roses")],
        "paragraphs": [
            "<p>L'Escala es uno de los destinos más característicos del Alt Empordà gerundense, con un patrimonio singular: las ruinas grecorromanas de <strong>Empúries</strong> (yacimiento clave de la historia mediterránea) y la <strong>Anchoa de L'Escala</strong> como producto gastronómico de referencia. Combina turismo cultural-gastronómico con un sector pesquero tradicional. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.190€/mes</strong>.</p>",
            "<p>El inquilino combina residentes locales, comunidad europea (especialmente francesa por proximidad) y turismo gastronómico-cultural. Los <strong>20 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Centre, Riells y Riells de Dalt</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso o adosado para alquiler residencial a comunidad europea (rotación baja) o VUT estacional con marca patrimonial-gastronómica diferenciada del turismo costero genérico.</p>",
            ["Alt Empordà", "Empúries arqueológica", "Anchoa", "Comunidad francesa"],
        ],
    },
    "mollet-del-valles": {
        "name": "Mollet del Vallès",
        "roi": "5,6%", "precio": "2.100€", "alquiler": "980€/mes", "dias": "22",
        "alts": [("rentabilidad-granollers.html", "Granollers"), ("rentabilidad-sabadell.html", "Sabadell")],
        "paragraphs": [
            "<p>Mollet del Vallès es un nodo del Vallès Oriental con buena conexión por R2/R3/R8 y AP-7, conurbado con el corredor Sabadell-Granollers. Su tejido económico combina industria, logística y un componente residencial creciente apoyado en familias jóvenes que aprovechan la conectividad ferroviaria con Barcelona (25 minutos por R2). Precio medio: <strong>2.100€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>980€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores industriales, jóvenes profesionales del corredor Vallès y familias que buscan alternativa al precio barcelonés. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centre, Plana Lledó y entorno R2</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo a la estación para alquiler residencial a familias jóvenes, capturando demanda metropolitana norte con entrada más asequible que Sabadell o Granollers.</p>",
            ["Vallès Oriental", "R2/R3/R8", "Corredor Vallès", "Familias jóvenes"],
        ],
    },
    "olot": {
        "name": "Olot",
        "roi": "6,0%", "precio": "1.700€", "alquiler": "850€/mes", "dias": "23",
        "alts": [("rentabilidad-banyoles.html", "Banyoles"), ("rentabilidad-girona.html", "Girona")],
        "paragraphs": [
            "<p>Olot es la capital de La Garrotxa gerundense, ubicada en la zona volcánica de la Garrotxa (Parque Natural con más de 40 conos volcánicos), con un tejido económico singular: industria cárnica de primer nivel (matadero, embutidos, derivados — destacando empresas como Noel Alimentaria), turismo de naturaleza y artesanía. Conexión por A-26 a 55 minutos de Girona. Precio medio: <strong>1.700€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>; alquiler medio <strong>850€/mes</strong>.</p>",
            "<p>El inquilino tipo es trabajador del sector cárnico, agroindustria, comercio comarcal y profesionales sanitarios del Hospital d'Olot. Los <strong>23 días</strong> de absorción muestran mercado fluido para una ciudad pequeña-media. Zonas: <strong>Centre, Sant Roc y Mas Bernat</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo industrial cárnico, con yield decente y entrada moderada para Cataluña interior.</p>",
            ["Garrotxa", "Volcanes", "Industria cárnica", "Yield interior"],
        ],
    },
    "palafrugell": {
        "name": "Palafrugell",
        "roi": "5,5%", "precio": "2.800€", "alquiler": "1.283€/mes", "dias": "21",
        "alts": [("rentabilidad-palamos.html", "Palamós"), ("rentabilidad-begur.html", "Begur")],
        "paragraphs": [
            "<p>Palafrugell es uno de los destinos premium de la Costa Brava gerundense, con tres calas singulares (<strong>Calella de Palafrugell, Llafranc, Tamariu</strong>) que figuran entre las más cotizadas del Mediterráneo español. Combina turismo de calidad, residentes europeos del norte (alemanes, británicos, franceses) y un casco urbano interior con identidad propia. Precio medio: <strong>2.800€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.283€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes europeos permanentes, segunda residencia premium nacional y demanda de VUT en julio-agosto con tarifas elevadas. Los <strong>21 días</strong> de absorción confirman demanda firme. Zonas: <strong>Calella de Palafrugell (premium turística), Llafranc y casco urbano</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: vivienda en cala para VUT estacional premium o alquiler residencial a comunidad europea — apreciación apoyada en marca Costa Brava consolidada.</p>",
            ["Costa Brava premium", "Tres calas icónicas", "Comunidad europea", "VUT premium"],
        ],
    },
    "palamos": {
        "name": "Palamós",
        "roi": "5,6%", "precio": "2.600€", "alquiler": "1.213€/mes", "dias": "21",
        "alts": [("rentabilidad-palafrugell.html", "Palafrugell"), ("rentabilidad-sant-feliu-de-guixols.html", "Sant Feliu de Guíxols")],
        "paragraphs": [
            "<p>Palamós es uno de los puertos pesqueros más importantes de la Costa Brava gerundense, conocido internacionalmente por la <strong>Gamba de Palamós</strong> (marca registrada de excelencia gastronómica) y por una lonja activa con valor añadido turístico (Espai del Peix, Museu de la Pesca). Combina pesca, turismo y un sector residencial estable. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>1.213€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes locales (sector pesquero, hostelería), comunidad europea y turismo gastronómico-residencial. Los <strong>21 días</strong> de absorción confirman demanda fuerte. Zonas: <strong>La Catifa, paseo marítimo y entorno del Puerto</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso urbano cerca del paseo marítimo para alquiler residencial estable a hostelería + opción VUT estacional. Plaza con marca gastronómica consolidada que sostiene la apreciación.</p>",
            ["Costa Brava", "Gamba de Palamós", "Puerto pesquero", "Marca gastronómica"],
        ],
    },
    "pineda-de-mar": {
        "name": "Pineda de Mar",
        "roi": "5,8%", "precio": "2.000€", "alquiler": "966€/mes", "dias": "21",
        "alts": [("rentabilidad-calella.html", "Calella"), ("rentabilidad-malgrat-de-mar.html", "Malgrat de Mar")],
        "paragraphs": [
            "<p>Pineda de Mar forma parte del eje turístico del Maresme barcelonés (junto a Calella y Malgrat), con un perfil orientado al turismo familiar internacional (centroeuropeo, sobre todo) y residencial permanente. Conexión por R1 a Barcelona (90 minutos). El precio medio (<strong>2.000€/m²</strong>) es de los más asequibles del Maresme costero, con <strong>rentabilidad bruta del 5,8%</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector hotelero (alquiler residencial estable), familias locales y un componente turístico estacional. Alquiler medio: <strong>966€/mes</strong>; <strong>21 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centre, Poblenou y entorno R1</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso urbano de entrada moderada para alquiler residencial estable a personal hotelero o familias, con potencial complementario VUT en verano. Mejor relación coste/yield que Calella vecina.</p>",
            ["Maresme", "R1 Cercanías", "Turismo familiar", "Entrada accesible"],
        ],
    },
    "premia-de-mar": {
        "name": "Premià de Mar",
        "roi": "5,6%", "precio": "2.600€", "alquiler": "1.213€/mes", "dias": "20",
        "alts": [("rentabilidad-vilassar-de-mar.html", "Vilassar de Mar"), ("rentabilidad-el-masnou.html", "El Masnou")],
        "paragraphs": [
            "<p>Premià de Mar es uno de los municipios del Bajo Maresme barcelonés, conurbado con Vilassar y El Masnou, con un perfil residencial y comercial muy consolidado y excelente conexión por R1 a Barcelona (35 minutos). El componente costero + cercanía a Barcelona configuran un mercado tensionado. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>1.213€/mes</strong>.</p>",
            "<p>El inquilino tipo es familia profesional o joven profesional que trabaja en Barcelona y prioriza la combinación de playa + buena conectividad. Los <strong>20 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Centre, Cotet y entorno R1</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo a la estación R1 para alquiler residencial estable, capturando demanda metropolitana norte con apreciación apoyada en marca Maresme consolidada.</p>",
            ["Bajo Maresme", "R1 35 min Barcelona", "Residencial costero", "Mercado líquido"],
        ],
    },
    "puigcerda": {
        "name": "Puigcerdà",
        "roi": "5,2%", "precio": "3.000€", "alquiler": "1.300€/mes", "dias": "20",
        "alts": [("rentabilidad-la-seu-d-urgell.html", "La Seu d'Urgell"), ("rentabilidad-andorra-la-vella.html", "Andorra la Vella")],
        "paragraphs": [
            "<p>Puigcerdà es la capital de la Cerdanya gerundense, en plena frontera con Francia y Andorra, una plaza singular que combina turismo de montaña (esquí en Masella, La Molina, Font-Romeu), residentes franceses y catalanes con segunda residencia, y comercio fronterizo. Precio medio: <strong>3.000€/m²</strong> — alto para el interior catalán — y <strong>rentabilidad bruta del 5,2%</strong>, típica de plaza turística premium.</p>",
            "<p>El inquilino combina residentes locales (servicios sanitarios del Hospital de Puigcerdà-Cerdanya, comercio), trabajadores fronterizos (Francia/Andorra) y un nicho de segunda residencia que genera VUT estacional invernal. Alquiler medio: <strong>1.300€/mes</strong>; <strong>20 días</strong> de absorción reflejan mercado muy líquido. Zonas: <strong>Centre, Estavar y Pi</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso o estudio para VUT estacional invierno-verano + alquiler residencial estable. Plaza con marca de montaña consolidada.</p>",
            ["Cerdanya", "Frontera Francia/Andorra", "Esquí", "VUT montaña"],
        ],
    },
    "rubi": {
        "name": "Rubí",
        "roi": "5,5%", "precio": "2.400€", "alquiler": "1.100€/mes", "dias": "22",
        "alts": [("rentabilidad-sant-cugat-del-valles.html", "Sant Cugat del Vallès"), ("rentabilidad-terrassa.html", "Terrassa")],
        "paragraphs": [
            "<p>Rubí es uno de los municipios industriales del Vallès Occidental, integrado en el eje Terrassa-Sabadell-Barcelona, con un tejido económico diversificado (química, automóvil, logística) y una población con perfil residencial joven creciente. Conexión por FGC Línia Vallès y AP-7. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.100€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores industriales, jóvenes profesionales del Vallès y familias jóvenes que aprovechan la conexión FGC con Barcelona (45 minutos). Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centre, Can Fatjó y entorno FGC</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo a la estación FGC para alquiler residencial a jóvenes profesionales, con yield superior al de Sant Cugat y entrada más asequible. Buena combinación coste/conectividad.</p>",
            ["Vallès Occidental", "FGC", "Industrial diversificado", "Familiar"],
        ],
    },
    "sant-boi-de-llobregat": {
        "name": "Sant Boi de Llobregat",
        "roi": "5,3%", "precio": "2.700€", "alquiler": "1.200€/mes", "dias": "22",
        "alts": [("rentabilidad-viladecans.html", "Viladecans"), ("rentabilidad-sant-feliu-de-llobregat.html", "Sant Feliu de Llobregat")],
        "paragraphs": [
            "<p>Sant Boi de Llobregat es uno de los municipios consolidados del Baix Llobregat barcelonés, con perfil dual: industria histórica (San Boi del Llobregat fue cuna del Avión Pegaso de Hispano-Suiza) y residencial creciente. Conexión por Metro Línea 8 (FGC), Cercanías R1 y AP-2. Precio medio: <strong>2.700€/m²</strong>; <strong>rentabilidad bruta 5,3%</strong>; alquiler medio <strong>1.200€/mes</strong>.</p>",
            "<p>El inquilino tipo combina familias profesionales que trabajan en Barcelona, personal sanitario del Parc Sanitari Sant Joan de Déu (segundo hospital tras Esplugues) y trabajadores industriales. Los <strong>22 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centre, Marianao y Casablanca</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo a Metro/FGC para alquiler residencial estable apoyado en demanda sanitaria + corona metropolitana sur.</p>",
            ["Baix Llobregat", "Parc Sanitari", "Metro L8/FGC", "Mixto industrial/residencial"],
        ],
    },
    "sant-cugat-del-valles": {
        "name": "Sant Cugat del Vallès",
        "roi": "4,8%", "precio": "4.500€", "alquiler": "1.800€/mes", "dias": "22",
        "alts": [("rentabilidad-cerdanyola-del-valles.html", "Cerdanyola del Vallès"), ("rentabilidad-rubi.html", "Rubí")],
        "paragraphs": [
            "<p>Sant Cugat del Vallès es uno de los municipios con mayor renta per cápita de Cataluña y referencia residencial premium del Vallès Occidental, sede de empresas tecnológicas (HP, Roche, Sharp), del CAR (Centro de Alto Rendimiento) y con presencia importante de directivos de Barcelona que prefieren vivir en zona residencial con mejor calidad de vida. Conexión por FGC. Precio medio: <strong>4.500€/m²</strong> — el más alto del grupo — y <strong>rentabilidad bruta del 4,8%</strong>, típica de residencial premium.</p>",
            "<p>El inquilino tipo es ejecutivo, alta dirección o profesional cualificado vinculado a tecnológicas, sanitarias o multinacionales. Alquiler medio: <strong>1.800€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Centre, Mira-sol y La Floresta</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso amplio o adosado para alquiler corporativo de 2-3 años, con foco en revalorización a 5-7 años más que yield puro. Conservación de capital en plaza ultra-premium.</p>",
            ["Vallès Occidental", "Mayor renta Catalunya", "Tecnológicas HQ", "Premium"],
        ],
    },
    "sant-feliu-de-llobregat": {
        "name": "Sant Feliu de Llobregat",
        "roi": "6,5%", "precio": "2.600€", "alquiler": "1.160€/mes", "dias": "22",
        "alts": [("rentabilidad-sant-boi-de-llobregat.html", "Sant Boi de Llobregat"), ("rentabilidad-esplugues-de-llobregat.html", "Esplugues de Llobregat")],
        "paragraphs": [
            "<p>Sant Feliu de Llobregat es la capital del Baix Llobregat (sede del consell comarcal) y un nodo administrativo, sanitario y residencial del entorno metropolitano de Barcelona. Conexión por R4 Cercanías a Sants en 20 minutos, FGC y A-2. Combina perfil residencial estable con servicios comarcales. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para una plaza tan próxima a Barcelona.</p>",
            "<p>El inquilino tipo combina familias profesionales que trabajan en Barcelona, funcionarios del consell comarcal y trabajadores sanitarios. Alquiler medio: <strong>1.160€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Centre, Falguera y Mas Lluí</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo a la estación R4 para alquiler residencial estable, capturando una de las mejores combinaciones yield/proximidad a Barcelona del Baix Llobregat.</p>",
            ["Baix Llobregat", "Capital comarcal", "R4 20 min Barcelona", "Yield alto metropolitano"],
        ],
    },
    "tortosa": {
        "name": "Tortosa",
        "roi": "6,5%", "precio": "1.300€", "alquiler": "703€/mes", "dias": "25",
        "alts": [("rentabilidad-amposta.html", "Amposta"), ("rentabilidad-vinaros.html", "Vinaròs")],
        "paragraphs": [
            "<p>Tortosa es la capital histórica de las Terres de l'Ebre tarraconenses, una ciudad media a orillas del Ebro con un patrimonio extraordinario (Catedral, Castell de la Suda, Reales Colegios) y un tejido económico basado en agricultura (arroz del Delta), agroindustria, sector papelero y servicios comarcales. Conexión por AP-7 y AVE (Camp de Tarragona a 35 minutos). Precio medio: <strong>1.300€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>703€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores agroindustriales, profesionales sanitarios del Hospital Verge de la Cinta y servicios comarcales. Los <strong>25 días</strong> de absorción reflejan ritmo pausado del interior. Zonas: <strong>Centre, Remolins y Sant Llàtzer</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable, con tickets bajos para Cataluña y yield alto. Plaza para inversor rentista que diversifica fuera del eje litoral barcelonés.</p>",
            ["Terres de l'Ebre", "Capital comarcal", "Patrimonio histórico", "Yield alto rentista"],
        ],
    },
    "tossa-de-mar": {
        "name": "Tossa de Mar",
        "roi": "5,2%", "precio": "3.200€", "alquiler": "1.387€/mes", "dias": "19",
        "alts": [("rentabilidad-lloret-de-mar.html", "Lloret de Mar"), ("rentabilidad-sant-feliu-de-guixols.html", "Sant Feliu de Guíxols")],
        "paragraphs": [
            "<p>Tossa de Mar es uno de los iconos de la Costa Brava gerundense, con la <strong>Vila Vella</strong> (única población medieval fortificada que se conserva en la costa catalana) y un casco antiguo que sirvió como escenario de cine en los años 50 (Ava Gardner). Combina turismo de calidad, residentes europeos del norte y un casco peatonal cuidado. Precio medio: <strong>3.200€/m²</strong> — alto, marca premium — y <strong>rentabilidad bruta del 5,2%</strong>.</p>",
            "<p>El inquilino tipo combina residentes europeos permanentes (alemanes, británicos, franceses), turismo de calidad y demanda VUT estacional con tarifas premium. Alquiler medio: <strong>1.387€/mes</strong>; <strong>19 días</strong> de absorción — entre los más rápidos del grupo. Zonas: <strong>Vila Vella (regulada), Sa Bauma y Centre</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: VUT registrada en zonas próximas a Vila Vella + alquiler residencial a comunidad europea — apreciación apoyada en marca histórica única.</p>",
            ["Costa Brava", "Vila Vella medieval", "VUT premium", "Marca cinematográfica"],
        ],
    },
    "vila-seca": {
        "name": "Vila-seca",
        "roi": "5,6%", "precio": "2.400€", "alquiler": "1.120€/mes", "dias": "21",
        "alts": [("rentabilidad-salou.html", "Salou"), ("rentabilidad-cambrils.html", "Cambrils")],
        "paragraphs": [
            "<p>Vila-seca es un municipio singular del Tarragonès, con un perfil económico inusual: incluye en su término <strong>PortAventura World</strong> (uno de los mayores resorts turísticos de Europa) y una buena parte del polo petroquímico de Tarragona, además de la zona costera de La Pineda. Esta combinación industria + turismo + residencial sostiene una demanda muy diversificada. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>1.120€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores petroquímicos (Repsol, Dow, Covestro), personal de PortAventura, residentes de La Pineda y familias locales. Los <strong>21 días</strong> de absorción confirman demanda firme. Zonas: <strong>Centre, La Pineda y entorno PortAventura</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso o estudio en La Pineda para VUT estacional (alta demanda PortAventura) o residencial estable a personal petroquímico. Demanda multifuente que reduce riesgo.</p>",
            ["Tarragonès", "PortAventura", "Petroquímico", "Demanda diversificada"],
        ],
    },
    "viladecans": {
        "name": "Viladecans",
        "roi": "5,3%", "precio": "2.600€", "alquiler": "1.150€/mes", "dias": "22",
        "alts": [("rentabilidad-gava.html", "Gavà"), ("rentabilidad-sant-boi-de-llobregat.html", "Sant Boi de Llobregat")],
        "paragraphs": [
            "<p>Viladecans es uno de los municipios consolidados del Baix Llobregat barcelonés, con un perfil residencial-industrial diversificado, sede del <strong>Hospital de Viladecans</strong> y bien conectado por Metro Línea 9 sud, R2 sur y A-2. Cercanía al aeropuerto y a la zona costera (Gavà Mar, parque Garraf). Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,3%</strong>; alquiler medio <strong>1.150€/mes</strong>.</p>",
            "<p>El inquilino tipo combina familias profesionales que trabajan en Barcelona, personal sanitario del Hospital de Viladecans, trabajadores aeroportuarios y un componente industrial. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centre, Montserratina y entorno Hospital</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios próximo al Hospital o Metro L9 para alquiler residencial estable apoyado en demanda sanitaria + corona metropolitana sur.</p>",
            ["Baix Llobregat", "Metro L9 sud", "Hospital de Viladecans", "Cerca aeropuerto"],
        ],
    },
    "vilanova-i-la-geltru": {
        "name": "Vilanova i la Geltrú",
        "roi": "6,5%", "precio": "2.400€", "alquiler": "1.120€/mes", "dias": "22",
        "alts": [("rentabilidad-sitges.html", "Sitges"), ("rentabilidad-calafell.html", "Calafell")],
        "paragraphs": [
            "<p>Vilanova i la Geltrú es la capital del Garraf barcelonés, una ciudad media costera con identidad fuerte (sede del Carnaval más singular de Cataluña), un puerto pesquero activo y la <strong>EPSEVG-UPC</strong> (Escola Politècnica Superior d'Enginyeria). Conexión por R2 sur a Barcelona en 50 minutos. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para una plaza costera-universitaria.</p>",
            "<p>El inquilino tipo combina estudiantes de ingeniería de la UPC, profesionales que trabajan en Barcelona y un componente residencial costero estable. Los <strong>22 días</strong> de absorción reflejan demanda fuerte. Zonas: <strong>Centre, Mar y entorno UPC</strong>. ITP Catalunya: <strong>10%</strong>. Tesis: piso pequeño próximo a estación R2 o UPC para alquiler estudiantil/joven profesional con yield muy superior a Sitges vecina, capturando demanda metropolitana sur con marca propia.</p>",
            ["Garraf", "EPSEVG-UPC", "R2 50 min Barcelona", "Yield alto costero"],
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
