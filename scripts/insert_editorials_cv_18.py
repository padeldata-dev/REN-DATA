"""Genera e inserta editoriales para 18 ciudades de la C. Valenciana sin editorial."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

CITIES = {
    "algemesi": {
        "name": "Algemesí",
        "roi": "6,2%", "precio": "1.400€", "alquiler": "724€/mes", "dias": "24",
        "alts": [("rentabilidad-alzira.html", "Alzira"), ("rentabilidad-sueca.html", "Sueca")],
        "paragraphs": [
            "<p>Algemesí es una ciudad media de la Ribera Alta valenciana, conocida por su Festa de la Mare de Déu de la Salut — Patrimonio Cultural Inmaterial de la Humanidad UNESCO — y un tejido económico equilibrado entre agricultura citrícola, agroindustria y manufacturas (textil, metal, alimentación). La conexión por Cercanías C-1 a 35 minutos de Valencia capital la hace funcional como ciudad media autónoma. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>724€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores de polígonos industriales, agroindustria y servicios comarcales, junto con jóvenes profesionales que prefieren huir del precio valenciano. Los <strong>24 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, Carrasca y Raval Nou</strong>. ITP Comunitat Valenciana: <strong>10%</strong> (alto, encarece la operación). Tesis: piso de 2-3 dormitorios para alquiler residencial estable, con yield decente y entrada moderada para una ciudad bien conectada con Valencia por cercanías.</p>",
            ["Ribera Alta", "UNESCO inmaterial", "Cercanías C-1", "Yield estable"],
        ],
    },
    "benicarlo": {
        "name": "Benicarló",
        "roi": "6,0%", "precio": "1.700€", "alquiler": "850€/mes", "dias": "23",
        "alts": [("rentabilidad-vinaros.html", "Vinaròs"), ("rentabilidad-peniscola.html", "Peñíscola")],
        "paragraphs": [
            "<p>Benicarló es una ciudad media costera del norte de Castellón, con la <strong>Alcachofa de Benicarló</strong> (DOP) como referencia agroalimentaria, un puerto pesquero activo y un tejido industrial diverso (mueble, plástico). La conexión por AP-7 y la cercanía a Peñíscola y Vinaròs la integran en un eje turístico-residencial. Precio medio: <strong>1.700€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>; alquiler medio <strong>850€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores agrícolas e industriales con un componente turístico estacional creciente. Los <strong>23 días</strong> de absorción confirman demanda activa. Zonas: <strong>Centro, Avenida Magallanes (paseo) y entorno del puerto</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial todo el año, con opción de combinar VUT estacional en zona paseo. Combinación interesante de yield medio + apreciación apoyada en eje turístico Peñíscola-Vinaròs.</p>",
            ["Costa de Castellón", "Alcachofa DOP", "Puerto pesquero", "Mixto residencial/VUT"],
        ],
    },
    "burriana": {
        "name": "Burriana",
        "roi": "6,0%", "precio": "1.500€", "alquiler": "750€/mes", "dias": "24",
        "alts": [("rentabilidad-vila-real.html", "Vila-real"), ("rentabilidad-castellon-de-la-plana.html", "Castellón")],
        "paragraphs": [
            "<p>Burriana es una ciudad media de la Plana Baixa castellonense, cuna histórica del comercio de la naranja valenciana (sus muelles fueron pioneros en exportación citrícola) y con un perfil económico que combina agricultura, industria cerámica (parte del clúster azulejero) y costa propia (Burriana Playa). Precio medio: <strong>1.500€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>; alquiler medio <strong>750€/mes</strong>.</p>",
            "<p>La demanda de alquiler procede de trabajadores del sector cerámico, agricultura y servicios comarcales. Los <strong>24 días</strong> de absorción reflejan un mercado fluido. Zonas: <strong>Centro histórico, Sant Pau y Burriana Playa</strong> (esta última con potencial VUT estacional). ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo cerámico, con la opción de Burriana Playa para perfil turístico-segunda residencia.</p>",
            ["Plana Baixa", "Naranja histórica", "Cerámica", "Burriana Playa"],
        ],
    },
    "cullera": {
        "name": "Cullera",
        "roi": "5,8%", "precio": "2.100€", "alquiler": "1.015€/mes", "dias": "21",
        "alts": [("rentabilidad-sueca.html", "Sueca"), ("rentabilidad-gandia.html", "Gandía")],
        "paragraphs": [
            "<p>Cullera es uno de los destinos turísticos clásicos de la costa valenciana, con la silueta de su castillo, el faro y 15 km de playas (San Antonio, Los Olivos, El Racó). Combina turismo nacional consolidado, residentes europeos y un sector pesquero tradicional en la desembocadura del Júcar. Precio medio: <strong>2.100€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>1.015€/mes</strong>.</p>",
            "<p>La demanda de alquiler es muy estacional: residencial todo el año en el casco urbano y temporada alta turística entre junio y septiembre en zona playa. Los <strong>21 días</strong> de absorción confirman demanda fuerte. Zonas: <strong>San Antonio (alquiler turístico), Faro y casco urbano</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis ganadora: VUT registrada en San Antonio para combinar yield turístico estival con alquiler residencial de octubre a junio. Plaza con marca turística consolidada.</p>",
            ["Costa Valencia sur", "Turismo familiar", "VUT estacional", "Yield mixto"],
        ],
    },
    "guardamar-del-segura": {
        "name": "Guardamar del Segura",
        "roi": "6,2%", "precio": "1.900€", "alquiler": "981€/mes", "dias": "20",
        "alts": [("rentabilidad-torrevieja.html", "Torrevieja"), ("rentabilidad-pilar-de-la-horadada.html", "Pilar de la Horadada")],
        "paragraphs": [
            "<p>Guardamar del Segura es un municipio costero de la Vega Baja alicantina, con 11 km de playas vírgenes protegidas por el Parque Natural de las Dunas y un perfil dual: pueblo pesquero tradicional y residencial-turístico con fuerte presencia europea (británicos, escandinavos, franceses). Precio medio: <strong>1.900€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>981€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residente extranjero permanente (jubilado o teletrabajador), turismo familiar nacional y temporada estival. Los <strong>20 días</strong> de absorción reflejan mercado muy líquido. Zonas: <strong>Centro urbano, Eras de la Sal y zona Babilonia</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso o estudio bien orientado para alquiler residencial a comunidad europea (rotación baja, contratos largos) o VUT registrada en zona playa, según perfil de inversor.</p>",
            ["Vega Baja", "Dunas protegidas", "Comunidad europea", "Larga duración"],
        ],
    },
    "javea": {
        "name": "Jávea",
        "roi": "5,2%", "precio": "3.200€", "alquiler": "1.385€/mes", "dias": "17",
        "alts": [("rentabilidad-denia.html", "Dénia"), ("rentabilidad-moraira.html", "Moraira")],
        "paragraphs": [
            "<p>Jávea (Xàbia) es uno de los destinos residenciales premium de la Marina Alta alicantina, con tres núcleos diferenciados (Pueblo, Puerto, Arenal), el icónico Cabo de San Antonio y una de las mayores comunidades de europeos del norte residentes en España (británicos, alemanes, holandeses, franceses). Precio medio: <strong>3.200€/m²</strong> — el más alto del grupo — y <strong>rentabilidad bruta del 5,2%</strong>, típica de plaza turística-residencial premium.</p>",
            "<p>El alquiler medio (<strong>1.385€/mes</strong>) y los <strong>17 días</strong> de absorción confirman un mercado muy líquido y tensionado. La demanda combina residencial permanente extranjero y VUT premium. Zonas: <strong>Arenal (turismo), Puerto (mixto) y Pueblo (residencial)</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: VUT registrada en Arenal o piso premium en Pueblo para alquiler residencial a comunidad europea — apreciación apoyada en demanda inelástica internacional + yield turístico.</p>",
            ["Marina Alta", "Comunidad europea premium", "VUT alto rendimiento", "Mercado tensionado"],
        ],
    },
    "lliria": {
        "name": "Llíria",
        "roi": "6,0%", "precio": "1.500€", "alquiler": "750€/mes", "dias": "24",
        "alts": [("rentabilidad-betera.html", "Bétera"), ("rentabilidad-paterna.html", "Paterna")],
        "paragraphs": [
            "<p>Llíria es una ciudad media del Camp de Túria valenciano, con identidad cultural muy fuerte: declarada <strong>Ciudad Creativa de la Música por la UNESCO</strong> (única en España), conserva además un patrimonio arqueológico romano-iberíco excepcional (Santuari del Plá de l'Arc, Mausoleo). Conexión por línea 1 de Metrovalencia (TRAM) y CV-35. Precio medio: <strong>1.500€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>.</p>",
            "<p>La demanda combina residentes locales, profesionales del cinturón metropolitano de Valencia (Paterna, Riba-roja) y familias jóvenes que aprovechan la conexión por TRAM. Alquiler medio: <strong>750€/mes</strong>; <strong>24 días</strong> de absorción. Zonas: <strong>Centro, Sant Vicent y entorno TRAM</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso de 2-3 dormitorios cerca de la estación TRAM para alquiler residencial estable, capturando demanda metropolitana en una ciudad con identidad propia y servicios completos.</p>",
            ["Camp de Túria", "UNESCO música", "TRAM línea 1", "Cinturón Valencia"],
        ],
    },
    "mislata": {
        "name": "Mislata",
        "roi": "5,7%", "precio": "2.100€", "alquiler": "998€/mes", "dias": "20",
        "alts": [("rentabilidad-valencia.html", "Valencia"), ("rentabilidad-quart-de-poblet.html", "Quart de Poblet")],
        "paragraphs": [
            "<p>Mislata es uno de los municipios con mayor densidad de población de toda España, conurbado con Valencia capital al oeste de la Avenida del Cid y prácticamente integrado en el continuo urbano valenciano. Conexión por Metrovalencia líneas 3, 5 y 9 (Mislata, Nou d'Octubre, Faitanar). El precio medio (<strong>2.100€/m²</strong>) está claramente por debajo de Valencia capital pero cerca, y la <strong>rentabilidad bruta del 5,7%</strong> es razonable para un mercado tensionado.</p>",
            "<p>El inquilino tipo es estudiante, joven profesional o familia que trabaja en Valencia capital pero busca alquiler más asequible. Alquiler medio: <strong>998€/mes</strong>; <strong>20 días</strong> de absorción reflejan mercado muy líquido. Zonas: <strong>Casa Grande, La Florida y entorno Metro</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso de 2 dormitorios próximo a Metro para alquiler residencial estable, capturando spillover de la presión inmobiliaria valenciana con yield superior a la capital.</p>",
            ["Conurbado Valencia", "Metro 3-5-9", "Densidad alta", "Spillover capital"],
        ],
    },
    "nules": {
        "name": "Nules",
        "roi": "6,2%", "precio": "1.400€", "alquiler": "724€/mes", "dias": "24",
        "alts": [("rentabilidad-burriana.html", "Burriana"), ("rentabilidad-vila-real.html", "Vila-real")],
        "paragraphs": [
            "<p>Nules es un municipio de la Plana Baixa castellonense con un perfil agroindustrial sólido: capital citrícola histórica (sede de cooperativas y exportadoras importantes) y con costa propia (Mareny de Nules). Conexión por AP-7 y Cercanías C-6 a 25 minutos de Castellón. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>724€/mes</strong>.</p>",
            "<p>La demanda de alquiler procede de trabajadores agrícolas (con picos por campañas citrícolas), industria de envasado y servicios comarcales. Los <strong>24 días</strong> de absorción reflejan mercado tranquilo pero con demanda estructural. Zonas: <strong>Centro, Sant Bertomeu y Mareny de Nules (perfil residencial-turístico)</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso urbano para alquiler estable, con opción de adquirir vivienda en Mareny para perfil turismo de proximidad estival.</p>",
            ["Plana Baixa", "Citrícola histórica", "Mareny de Nules", "Yield medio"],
        ],
    },
    "ontinyent": {
        "name": "Ontinyent",
        "roi": "6,5%", "precio": "1.050€", "alquiler": "540€/mes", "dias": "22",
        "alts": [("rentabilidad-xativa.html", "Xàtiva"), ("rentabilidad-alcoy.html", "Alcoy")],
        "paragraphs": [
            "<p>Ontinyent es la capital de La Vall d'Albaida valenciana, con un tejido industrial textil histórico (mantas, tejidos, prendas de hogar) que sigue siendo motor económico junto con la industria del papel y servicios comarcales. La ciudad combina identidad propia muy marcada con buena conexión por la N-340. El precio medio (<strong>1.050€/m²</strong>) es uno de los más bajos del grupo y entrega una <strong>rentabilidad bruta del 6,5%</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores textiles, sector papel, comercio y servicios. Alquiler medio: <strong>540€/mes</strong>; <strong>22 días</strong> de absorción muestran mercado fluido para una ciudad interior. Zonas: <strong>Centro histórico, Sant Rafel y barrio Vila</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: tickets bajos con yield alto, ideal para inversor que busca cash-flow estable apoyado en empleo industrial diversificado, con menos dependencia turística que las plazas costeras.</p>",
            ["Vall d'Albaida", "Textil histórico", "Industria papel", "Ticket bajo"],
        ],
    },
    "peniscola": {
        "name": "Peñíscola",
        "roi": "5,8%", "precio": "2.200€", "alquiler": "1.063€/mes", "dias": "21",
        "alts": [("rentabilidad-benicarlo.html", "Benicarló"), ("rentabilidad-vinaros.html", "Vinaròs")],
        "paragraphs": [
            "<p>Peñíscola es una de las plazas turísticas con mayor proyección internacional del norte castellonense, con su castillo del Papa Luna sobre el peñón (escenario de Juego de Tronos), 14 km de playa y un casco antiguo amurallado. La marca turística es muy potente y la demanda nacional + internacional sostenida. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>1.063€/mes</strong>.</p>",
            "<p>La demanda de alquiler tiene dos perfiles: residencial todo el año en zonas urbanas (centro, Levante) y VUT estacional intensivo en zonas próximas a la playa Norte y casco antiguo. Los <strong>21 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Casco Antiguo (regulado), Levante y zona Las Doncellas</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: VUT registrada con licencia para capturar tarifas premium de junio a septiembre, complementada con alquiler residencial en temporada baja.</p>",
            ["Costa Castellón norte", "Castillo Papa Luna", "VUT premium", "Marca internacional"],
        ],
    },
    "pilar-de-la-horadada": {
        "name": "Pilar de la Horadada",
        "roi": "6,5%", "precio": "1.800€", "alquiler": "975€/mes", "dias": "20",
        "alts": [("rentabilidad-torrevieja.html", "Torrevieja"), ("rentabilidad-orihuela.html", "Orihuela")],
        "paragraphs": [
            "<p>Pilar de la Horadada es el municipio más meridional de la Comunidad Valenciana, en la Vega Baja alicantina, con perfil dual: pueblo agrícola interior (cultivos hortícolas) y zona costera consolidada (Mil Palmeras, Torre de la Horadada) muy demandada por residentes europeos y turismo familiar. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para plaza costera.</p>",
            "<p>El inquilino tipo combina residente extranjero permanente (británicos, escandinavos), turismo familiar nacional y trabajadores agrícolas. Alquiler medio: <strong>975€/mes</strong>; <strong>20 días</strong> de absorción reflejan mercado muy líquido. Zonas: <strong>Mil Palmeras (residencial-turística), Torre de la Horadada y casco urbano</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso o adosado en zona costera para alquiler residencial a comunidad europea o VUT estacional, con yield alto apoyado en demanda estructural internacional.</p>",
            ["Vega Baja sur", "Costa Mil Palmeras", "Comunidad europea", "Yield alto costero"],
        ],
    },
    "requena": {
        "name": "Requena",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "595€/mes", "dias": "26",
        "alts": [("rentabilidad-utiel.html", "Utiel"), ("rentabilidad-valencia.html", "Valencia")],
        "paragraphs": [
            "<p>Requena es la cabecera de la comarca interior de la Plana de Utiel-Requena, con denominación de origen vinícola propia (DO Utiel-Requena, una de las más extensas de España, con la variedad Bobal como referencia) y un tejido económico basado en viticultura, agroindustria y servicios. Conexión por AVE Madrid-Valencia (parada Requena-Utiel) y A-3. Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>.</p>",
            "<p>La demanda de alquiler es local: trabajadores del sector vinícola, bodegas, agroindustria y servicios. Alquiler medio: <strong>595€/mes</strong>; <strong>26 días</strong> de absorción reflejan ritmo pausado típico de mercado interior. Zonas: <strong>Casco histórico (La Villa), Las Peñas y centro</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: ticket bajo con yield alto, ideal para inversor rentista que busque cash-flow apoyado en una economía agraria estable y la marca DO Utiel-Requena.</p>",
            ["Plana Utiel-Requena", "DO vino", "AVE", "Yield alto rentista"],
        ],
    },
    "sueca": {
        "name": "Sueca",
        "roi": "6,5%", "precio": "1.400€", "alquiler": "758€/mes", "dias": "24",
        "alts": [("rentabilidad-cullera.html", "Cullera"), ("rentabilidad-algemesi.html", "Algemesí")],
        "paragraphs": [
            "<p>Sueca es la capital de La Ribera Baixa valenciana, en el corazón de la zona arrocera del Parque Natural de la Albufera. Es además referencia gastronómica internacional como cuna del concurso mundial de paella valenciana. Combina arroz, pesca lacustre, agroindustria y un núcleo costero (El Perelló, Mareny de Barraquetes) integrado en el municipio. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>758€/mes</strong>.</p>",
            "<p>La demanda combina trabajadores agrícolas (campañas arroceras), agroindustria, residentes locales y turismo de proximidad. Los <strong>24 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, Estación y zona costera (Perelló-Mareny)</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable + opción de inversión en Perelló para perfil turismo-segunda residencia. Yield decente con motor económico arrocero estructural.</p>",
            ["Ribera Baixa", "Albufera arrocera", "El Perelló", "Yield alto"],
        ],
    },
    "tavernes-de-la-valldigna": {
        "name": "Tavernes de la Valldigna",
        "roi": "6,0%", "precio": "1.600€", "alquiler": "800€/mes", "dias": "23",
        "alts": [("rentabilidad-cullera.html", "Cullera"), ("rentabilidad-gandia.html", "Gandía")],
        "paragraphs": [
            "<p>Tavernes de la Valldigna es la cabecera de la histórica Vall de Aigua Blanca (La Valldigna), entre la Sierra de Corbera y el Mediterráneo, con núcleo urbano interior y zona costera propia (Tavernes Playa) integrada en el municipio. La economía combina cítricos (mandarina y naranja), comercio comarcal y un componente turístico estival. Precio medio: <strong>1.600€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>.</p>",
            "<p>La demanda combina residentes locales, trabajadores agrícolas y un componente residencial-turístico en zona playa. Alquiler medio: <strong>800€/mes</strong>; <strong>23 días</strong> de absorción muestran mercado activo. Zonas: <strong>Centro urbano, El Calvari y Tavernes Playa</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial estable o adquisición en Tavernes Playa para alquiler estacional. Plaza con buena combinación coste/yield en eje turístico Cullera-Gandía.</p>",
            ["La Valldigna", "Mandarina/naranja", "Tavernes Playa", "Eje turístico"],
        ],
    },
    "villena": {
        "name": "Villena",
        "roi": "6,4%", "precio": "750€", "alquiler": "400€/mes", "dias": "22",
        "alts": [("rentabilidad-elda.html", "Elda"), ("rentabilidad-yecla.html", "Yecla")],
        "paragraphs": [
            "<p>Villena es la capital comarcal del Alto Vinalopó alicantino, con un tejido industrial histórico centrado en el calzado (parte del clúster de Elda-Elche), bodegas (DO Alicante) y un patrimonio arqueológico excepcional (Tesoro de Villena, segundo conjunto áureo más importante de Europa). El precio medio (<strong>750€/m²</strong>) es <strong>el más bajo del grupo analizado</strong> y ofrece tickets de entrada extraordinariamente accesibles, con <strong>rentabilidad bruta del 6,4%</strong>.</p>",
            "<p>La demanda procede de trabajadores industriales del calzado, sector vinícola y servicios comarcales. Alquiler medio: <strong>400€/mes</strong>; <strong>22 días</strong> de absorción muestran mercado fluido. Zonas: <strong>Centro, La Solana y entorno Castillo de la Atalaya</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: vivienda completa por menos de 60.000€ es factible con yield decente — plaza idónea para inversor que diversifica cartera con tickets muy bajos en el interior alicantino.</p>",
            ["Alto Vinalopó", "Calzado", "DO Alicante", "Ticket muy bajo"],
        ],
    },
    "vinaros": {
        "name": "Vinaròs",
        "roi": "6,2%", "precio": "1.700€", "alquiler": "878€/mes", "dias": "23",
        "alts": [("rentabilidad-benicarlo.html", "Benicarló"), ("rentabilidad-peniscola.html", "Peñíscola")],
        "paragraphs": [
            "<p>Vinaròs es la ciudad más septentrional de la costa castellonense, frontera con el Delta del Ebro tarraconense, conocida por el <strong>Langostino de Vinaròs</strong> (referencia gastronómica nacional), un puerto pesquero activo y un casco urbano histórico cuidado. Conexión por AP-7. Precio medio: <strong>1.700€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>878€/mes</strong>.</p>",
            "<p>La demanda combina residentes permanentes, trabajadores del sector pesquero y agroalimentario, y turismo gastronómico-residencial. Los <strong>23 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centro, Paseo Marítimo Colón y entorno Puerto</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso urbano para alquiler residencial todo el año + opción VUT estacional en zona paseo marítimo. Plaza con marca gastronómica consolidada que apoya la apreciación a medio plazo.</p>",
            ["Costa Castellón norte", "Langostino DOP", "Frontera Tarragona", "Mixto"],
        ],
    },
    "xativa": {
        "name": "Xàtiva",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "550€/mes", "dias": "22",
        "alts": [("rentabilidad-ontinyent.html", "Ontinyent"), ("rentabilidad-alzira.html", "Alzira")],
        "paragraphs": [
            "<p>Xàtiva es una de las ciudades históricas más singulares de la Comunidad Valenciana, capital de La Costera, cuna de los papas Borgia (Calixto III y Alejandro VI) y con un patrimonio cultural excepcional (Castillo, Colegiata, Hospital Real). Conexión por AVE (estación Xàtiva en línea Madrid-Valencia) y N-340. Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>550€/mes</strong>.</p>",
            "<p>La demanda de alquiler combina residentes locales, estudiantes (sede de la UPV-EHU y UV en Xàtiva), trabajadores agrícolas y servicios comarcales. Los <strong>22 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro histórico (regulado), Sant Joan y entorno estación</strong>. ITP Comunitat Valenciana: <strong>10%</strong>. Tesis: piso pequeño próximo al casco para alquiler estudiantil/residencial, con opción VUT cultural en zona protegida. Conexión AVE añade valor a 5-7 años.</p>",
            ["La Costera", "Papas Borgia", "AVE", "Universitario"],
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
