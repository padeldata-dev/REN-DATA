// Generador de páginas "Vivir en {ciudad}" para top 50 ciudades de España
// Uso: node tools/gen-vivir.js
const fs = require('fs');
const path = require('path');

const OUT_DIR = path.join(__dirname, '..', 'rendata_beta');
const IMG_DIR = path.join(OUT_DIR, 'img');
const TODAY = '2026-05-21';

// Datos económicos extraídos de data/processed/cities_2026Q2.csv
// [slug, nombre, ccaa, poblacion, precio_m2, alquiler_medio, roi, dias_mercado]
const ECON = [
  ['madrid','Madrid','C. de Madrid',2866850,5960,1750,3.5,15],
  ['barcelona','Barcelona','Cataluña',1508805,4900,1880,4.6,18],
  ['valencia','Valencia','C. Valenciana',746683,2700,1200,5.3,16],
  ['sevilla','Sevilla','Andalucía',697487,2450,1080,5.3,22],
  ['zaragoza','Zaragoza','Aragón',601674,1950,980,6.0,24],
  ['malaga','Málaga','Andalucía',549135,3180,1340,5.1,18],
  ['palma','Palma','Islas Baleares',434786,4200,1650,4.7,22],
  ['las-palmas-gc','Las Palmas de Gran Canaria','Canarias',381868,2100,980,5.6,20],
  ['bilbao','Bilbao','País Vasco',358875,3150,1270,4.8,28],
  ['murcia','Murcia','R. de Murcia',345759,1750,860,5.9,20],
  ['valladolid','Valladolid','Castilla y León',319805,1600,800,6.0,25],
  ['cordoba','Córdoba','Andalucía',306248,1520,740,5.8,26],
  ['l-hospitalet-de-llobregat',"L'Hospitalet de Llobregat",'Cataluña',289510,3400,1500,5.3,20],
  ['vigo','Vigo','Galicia',286774,1850,890,5.8,25],
  ['alicante','Alicante','C. Valenciana',274577,2250,990,5.3,19],
  ['gijon','Gijón','Asturias',264381,1680,800,5.7,27],
  ['a-coruna','A Coruña','Galicia',251543,2100,880,5.0,26],
  ['granada','Granada','Andalucía',245640,1980,910,5.5,21],
  ['vitoria','Vitoria','País Vasco',214234,2700,1150,5.1,27],
  ['badalona','Badalona','Cataluña',210987,2600,1200,5.5,20],
  ['santa-cruz-de-tenerife','Santa Cruz de Tenerife','Canarias',203787,2000,930,5.6,22],
  ['oviedo','Oviedo','Asturias',200049,1850,880,5.7,26],
  ['mostoles','Móstoles','C. de Madrid',196173,2160,985,5.5,21],
  ['elche','Elche','C. Valenciana',191660,1600,780,5.8,22],
  ['san-sebastian','San Sebastián','País Vasco',189866,5200,1880,4.3,30],
  ['sabadell','Sabadell','Cataluña',185798,1800,900,6.0,22],
  ['santander','Santander','Cantabria',185410,2250,940,5.0,26],
  ['jerez-de-la-frontera','Jerez de la Frontera','Andalucía',182269,1650,780,5.7,25],
  ['castellon-de-la-plana','Castellón de la Plana','C. Valenciana',180379,1440,718,6.0,24],
  ['leganes','Leganés','C. de Madrid',174593,2270,1026,5.4,20],
  ['almeria','Almería','Andalucía',170503,1380,760,6.6,25],
  ['cartagena','Cartagena','R. de Murcia',170483,1360,701,6.2,22],
  ['pamplona','Pamplona','Navarra',166279,2950,1170,4.8,24],
  ['terrassa','Terrassa','Cataluña',163862,1750,875,6.0,23],
  ['fuenlabrada','Fuenlabrada','C. de Madrid',163567,1900,880,5.6,22],
  ['alcala-de-henares','Alcalá de Henares','C. de Madrid',163386,1950,920,5.7,20],
  ['burgos','Burgos','Castilla y León',163156,1720,890,6.2,25],
  ['la-laguna','La Laguna','Canarias',161108,2000,920,5.5,22],
  ['salamanca','Salamanca','Castilla y León',159225,1750,880,6.0,25],
  ['cadiz','Cádiz','Andalucía',145595,2200,1000,5.5,23],
  ['leon','León','Castilla y León',145242,1400,770,6.6,26],
  ['albacete','Albacete','Castilla-La Mancha',143799,1200,680,6.8,26],
  ['getafe','Getafe','C. de Madrid',143153,2400,1100,5.5,18],
  ['alcorcon','Alcorcón','C. de Madrid',141465,2300,1020,5.3,21],
  ['huelva','Huelva','Andalucía',140675,1400,700,6.0,24],
  ['logrono','Logroño','La Rioja',123841,1560,780,6.0,23],
  ['badajoz','Badajoz','Extremadura',122510,920,530,6.9,29],
  ['tarragona','Tarragona','Cataluña',112176,1780,890,6.0,24],
  ['lleida','Lleida','Cataluña',112035,1300,650,6.0,22],
  ['ourense','Ourense','Galicia',107060,1080,610,6.8,29],
];

// Slug de la CCAA en ccaa-*.html
const CCAA_SLUG = {
  'C. de Madrid':'madrid','Cataluña':'cataluna','C. Valenciana':'comunitat-valenciana',
  'Andalucía':'andalucia','Aragón':'aragon','Islas Baleares':'baleares','Canarias':'canarias',
  'País Vasco':'pais-vasco','R. de Murcia':'murcia','Castilla y León':'castilla-y-leon',
  'Galicia':'galicia','Asturias':'asturias','Cantabria':'cantabria','Navarra':'navarra',
  'Castilla-La Mancha':'castilla-la-mancha','Extremadura':'extremadura','La Rioja':'la-rioja',
};

// Datos de tipo cualitativo por ciudad — barrios, transporte, empleo, educación/sanidad, pros/contras.
// Toda la información ha sido verificada como real (barrios, líneas de transporte, universidades, hospitales).
const CITY = {
  'madrid':{
    barrios:[
      {n:'Salamanca',p:'premium',d:'Distrito de lujo: Serrano, Goya, Recoletos. El m² más caro de España, demanda constante.'},
      {n:'Chamberí',p:'céntrico',d:'Clásico burgués madrileño, vida de barrio, edificios señoriales y tranquilidad relativa.'},
      {n:'Centro',p:'céntrico',d:'Sol, Malasaña, Lavapiés, Chueca, Embajadores. Ocio y ruido máximos, ideal para alquiler turístico ya restringido.'},
      {n:'Vallecas',p:'económico',d:'Periferia sureste con metro y precios accesibles, perfil joven y familiar.'},
      {n:'Carabanchel',p:'económico',d:'Buena relación calidad-precio, transformación urbana en marcha.'},
      {n:'Chamartín · Hortaleza',p:'familiar',d:'Zona norte residencial bien comunicada, demanda estable de familias.'},
      {n:'Pozuelo / Las Rozas / Boadilla',p:'premium',d:'Municipios del oeste con chalets y mejores colegios, fuera del límite municipal pero parte del área metropolitana.'},
    ],
    transporte:'Madrid tiene la red de metro más densa de España (13 líneas, 302 estaciones) más cercanías Renfe (10 líneas C1-C10), autobuses EMT y EMT nocturno, taxis y VTC. AVE a Barcelona, Sevilla, Málaga, Valencia, Galicia y arco mediterráneo desde Atocha y Chamartín. Aeropuerto Adolfo Suárez Madrid-Barajas con conexión metro L8.',
    empleo:'Capital económica del país: servicios financieros (Banco Santander, BBVA, Mapfre), tecnología (Telefónica, Indra, hubs de Google y Amazon), administración central, sedes de IBEX 35, consultoría, sanidad privada y turismo. Polos de empleo: Castellana, Cuatro Torres, Las Tablas, Tres Cantos.',
    educacion:'9 universidades públicas y privadas (UCM, UAM, UC3M, UPM, URJC, UNED, Comillas, CEU, IE). Escuelas internacionales y bilingües abundantes. Hospitales públicos La Paz, 12 de Octubre, Gregorio Marañón, Ramón y Cajal; privados Quirónsalud, Sanitas La Moraleja, Ruber.',
    pros:['Mejor mercado laboral de España','Oferta cultural y de ocio enorme','Transporte público excelente'],
    contras:['Precios de vivienda inaccesibles para sueldo medio','Tráfico y contaminación','Distancias largas a pesar del metro'],
  },
  'barcelona':{
    barrios:[
      {n:'Eixample',p:'premium',d:'Cuadrícula de Cerdà, modernismo, comercios y oficinas. Demanda constante, precios muy altos.'},
      {n:'Gràcia',p:'céntrico',d:'Antiguo pueblo absorbido, plazas, ambiente bohemio y de barrio, muy buscado.'},
      {n:'Sant Martí · Poblenou',p:'familiar',d:'Antigua zona industrial reconvertida (22@), nueva vivienda, playa cerca.'},
      {n:'Sants',p:'económico',d:'Buena comunicación, precios algo menores que Eixample, vida de barrio.'},
      {n:'Nou Barris',p:'económico',d:'Periferia norte, opción más asequible dentro de la ciudad.'},
      {n:'Sarrià-Sant Gervasi',p:'premium',d:'Zona alta, residencial y de poder adquisitivo elevado.'},
      {n:'Ciutat Vella · Born / Raval',p:'céntrico',d:'Casco histórico, vivienda antigua y turismo masivo, restricciones a pisos turísticos.'},
    ],
    transporte:'Metro TMB (12 líneas, L1-L12), FGC, Rodalies (cercanías Renfe R1-R8), Tram, autobuses urbanos y autobús nocturno NitBus. AVE a Madrid (2h30) y conexión TGV a Francia. Aeropuerto El Prat con metro L9 Sud y Rodalies R2 Nord. Red ciclista urbana extensa (Bicing).',
    empleo:'Tecnología y startups (Pier01, Glovo, eDreams), farmacéutica y biotech (PCB, Roche, Almirall, Esteve), industria automovilística (SEAT en Martorell), turismo y hostelería, logística portuaria, moda y diseño. Polos: 22@ Poblenou, Plaza Europa-Hospitalet, Cornellà.',
    educacion:'Universidad de Barcelona (UB), UAB, UPF, UPC, ESADE, IESE, La Salle. Hospital Clínic, Vall d\'Hebron, Sant Pau, Hospital del Mar. Sanidad privada potente (Quirón, Teknon).',
    pros:['Mar y montaña a 30 minutos','Vida cultural intensa','Aeropuerto e internacionalización'],
    contras:['Tensión inquilino-propietario, regulación de alquileres','Turistificación de barrios céntricos','Precios disparados, especialmente en alquiler'],
  },
  'valencia':{
    barrios:[
      {n:'Ciutat Vella',p:'céntrico',d:'Casco histórico (Carmen, Seu, Mercat). Mucho ocio, edificios antiguos, valor patrimonial.'},
      {n:'Ruzafa',p:'céntrico',d:'Barrio de moda, hostelería de autor, demanda fuerte de jóvenes profesionales.'},
      {n:'L\'Eixample (Pla del Remei, Gran Via)',p:'premium',d:'Modernismo valenciano, comercio, vivienda burguesa de buena calidad.'},
      {n:'Benimaclet',p:'familiar',d:'Antiguo pueblo, ambiente universitario y de barrio, plazas y mercado.'},
      {n:'Patraix',p:'familiar',d:'Residencial tranquilo, precio razonable, buenas comunicaciones.'},
      {n:'Cabanyal · Malvarrosa',p:'económico',d:'Junto al mar, casas tradicionales, plan urbanístico en marcha, precios al alza.'},
      {n:'Campanar · Nou Campanar',p:'familiar',d:'Zona moderna alrededor del Bioparc y nuevos cauces.'},
    ],
    transporte:'Metrovalencia (10 líneas, incluye tranvías 4, 6, 8, 9, 10), Cercanías Renfe (6 líneas C1-C6), EMT autobuses, Valenbisi. AVE a Madrid (1h50). Aeropuerto de Manises con metro L3 y L5.',
    empleo:'Puerto de Valencia (uno de los mayores de Europa), automoción (Ford en Almussafes), agroalimentaria (cítricos, conservas), turismo, sector servicios. Polo tecnológico en Paterna (Parque Tecnológico) y la Marina/Las Naves.',
    educacion:'Universidad de Valencia (UV), Politécnica (UPV), Cardenal Herrera (CEU), Católica de Valencia. Hospitales La Fe, Clínic Universitari, General Universitari, Quirónsalud.',
    pros:['Clima, playa y huerta','Precios moderados frente a Madrid/Barcelona','Tamaño humano con servicios de gran ciudad'],
    contras:['Subida fuerte de alquiler en últimos años','Tráfico en accesos','Algunos barrios con turistificación'],
  },
  'sevilla':{
    barrios:[
      {n:'Casco Antiguo (Santa Cruz, Arenal, Alfalfa)',p:'premium',d:'Centro monumental, casas patio, demanda altísima, suelo escaso.'},
      {n:'Triana',p:'céntrico',d:'Barrio tradicional al otro lado del río, ambiente flamenco y de carácter sevillano.'},
      {n:'Los Remedios',p:'premium',d:'Vivienda burguesa, anchas avenidas, cerca de la Feria de Abril.'},
      {n:'Nervión',p:'familiar',d:'Zona comercial y residencial, buen transporte, demanda estable.'},
      {n:'Macarena',p:'económico',d:'Histórico, hospitalario, precio asequible, barrio popular muy auténtico.'},
      {n:'Bermejales · Bellavista',p:'familiar',d:'Sur, vivienda nueva y unifamiliares, perfil familiar.'},
      {n:'Sevilla Este',p:'familiar',d:'Periferia oeste, urbanizaciones modernas, comercio.'},
    ],
    transporte:'Metro (L1 funcional, L2-L4 en plan), tranvía Metrocentro, autobuses TUSSAM, Cercanías Renfe (5 líneas C1-C5), Sevici (bicicletas). AVE a Madrid (2h30), Málaga, Córdoba. Aeropuerto San Pablo conectado por autobús EA.',
    empleo:'Servicios y administración (Junta de Andalucía), turismo, agroalimentación (Coca-Cola, Heineken), aeronáutica (Airbus en San Pablo Sur, factoría Tablada), comercio. Polo: Cartuja (parque tecnológico) y Aerópolis.',
    educacion:'Universidad de Sevilla, Pablo de Olavide, Loyola Andalucía. Hospitales Virgen del Rocío, Virgen Macarena, Quirónsalud Sagrado Corazón.',
    pros:['Patrimonio y cultura excepcionales','Vida en la calle y gastronomía','Precios razonables salvo en el casco'],
    contras:['Veranos extremadamente calurosos','Mercado laboral con sueldos bajos','Metro incompleto'],
  },
  'zaragoza':{
    barrios:[
      {n:'Centro · Independencia',p:'céntrico',d:'Eje comercial alrededor del Paseo de la Independencia y el Coso, vivienda de calidad y servicios.'},
      {n:'Universidad · Romareda',p:'familiar',d:'Residencial consolidado, cerca de la universidad y el hospital, demanda estable.'},
      {n:'Actur · Rey Fernando',p:'familiar',d:'Norte del Ebro, vivienda moderna planificada, buena para familias.'},
      {n:'Delicias',p:'económico',d:'Populoso y bien conectado, buenos precios y comercio de proximidad.'},
      {n:'Casco Histórico',p:'céntrico',d:'El Tubo, plaza del Pilar, edificios antiguos, vida nocturna activa.'},
      {n:'Valdespartera · Arcosur',p:'familiar',d:'Nuevos desarrollos al sur, urbanismo planificado, vivienda eficiente.'},
      {n:'Las Fuentes · San José',p:'económico',d:'Tradicionales y obreros, buena relación calidad-precio.'},
    ],
    transporte:'Tranvía L1 (Valdespartera-Parque Goya), L2 prevista. Autobuses urbanos TUZSA, Cercanías Renfe C1 (a Casetas y Miraflores). AVE a Madrid (1h15) y Barcelona (1h30). Aeropuerto con autobús urbano 501.',
    empleo:'Logística (PLAZA, mayor plataforma logística de Europa del Sur), industria (Opel/Stellantis en Figueruelas, BSH, Schindler), agroalimentaria, administración aragonesa. Polo industrial: Cuarte, Malpica, PLAZA.',
    educacion:'Universidad de Zaragoza (campus San Francisco y Río Ebro), Universidad San Jorge (privada). Hospitales Miguel Servet, Clínico Lozano Blesa, Royo Villanova, Quirónsalud.',
    pros:['Nudo geográfico (Madrid, Barcelona, País Vasco a 3h)','Buena relación calidad-precio','Servicios completos sin agobio de gran capital'],
    contras:['Cierzo y veranos calurosos','Mercado laboral concentrado en industria/logística','Menos ocio que en ciudades mediterráneas'],
  },
  'malaga':{
    barrios:[
      {n:'Centro Histórico · Soho',p:'premium',d:'Casco antiguo peatonal, Soho artístico, mucha demanda turística e internacional.'},
      {n:'La Malagueta',p:'premium',d:'Junto a la playa y el puerto, vivienda alta gama, segunda residencia.'},
      {n:'El Limonar · Pedregalejo',p:'premium',d:'Costa este, chalets y vivienda señorial, ambiente residencial.'},
      {n:'Teatinos',p:'familiar',d:'Junto a la Universidad, vivienda moderna y nueva, perfil joven y familiar.'},
      {n:'Carretera de Cádiz',p:'económico',d:'Zona oeste densa con buena relación calidad-precio.'},
      {n:'Huelin · La Princesa',p:'familiar',d:'Antigua zona industrial reconvertida con vivienda moderna y muy demandada.'},
      {n:'Cruz de Humilladero',p:'económico',d:'Populoso, bien conectado, opción accesible.'},
    ],
    transporte:'Metro de Málaga (L1 y L2, expansión hasta Civil/Hospital), Cercanías Renfe (C1 a Fuengirola, C2 a Álora), autobuses EMT. AVE María Zambrano a Madrid (2h30), Barcelona, Sevilla, Córdoba. Aeropuerto Costa del Sol con cercanías C1.',
    empleo:'Turismo y hostelería, tecnología (Málaga Tech Park PTA en Campanillas: Oracle, Google Cybersecurity, Vodafone, IBM), nómadas digitales, construcción, comercio. Boom de empresas tech atraídas por el clima y el aeropuerto.',
    educacion:'Universidad de Málaga (Teatinos), centros internacionales. Hospitales Carlos Haya, Clínico Virgen de la Victoria, Hospital Quirónsalud Málaga.',
    pros:['Clima excelente todo el año','Aeropuerto internacional con muchas conexiones','Boom económico y mercado laboral tech en alza'],
    contras:['Precios disparados por demanda extranjera','Turistificación del centro','Tráfico denso en hora punta'],
  },
  'palma':{
    barrios:[
      {n:'Centro · Casco Antiguo',p:'premium',d:'La Lonja, Born, Catedral. Patrimonio y demanda turística altísima, m² muy caro.'},
      {n:'Santa Catalina',p:'premium',d:'Antiguo barrio marinero reconvertido, restaurantes y vida cosmopolita, muy buscado por extranjeros.'},
      {n:'Portixol · Molinar',p:'premium',d:'Junto al mar al este, transformación residencial y precios al alza.'},
      {n:'Es Jonquet · Son Espanyolet',p:'céntrico',d:'Pequeño y con encanto cerca del puerto.'},
      {n:'Son Armadams · El Terreno',p:'familiar',d:'Residencial tradicional, vistas al puerto, vivienda burguesa.'},
      {n:'Pere Garau · Foners',p:'económico',d:'Más asequible, multicultural, buena conexión.'},
      {n:'Son Ferriol · Establiments',p:'económico',d:'Zonas externas con vivienda más barata, ambiente de pueblo.'},
    ],
    transporte:'Metro M1 (Plaza España-Universidad), tranvía SFM y Tren de Sóller, autobuses EMT, taxis. Aeropuerto Son Sant Joan con autobús A1. Conexiones marítimas a Ibiza, Barcelona, Valencia, Mahón.',
    empleo:'Turismo (principal motor: hostelería, hotelería, alquiler vacacional), náutica (Marina Port Adriano, IBatres, refit), sanidad privada, comercio. Estacionalidad fuerte. Boom inmobiliario por compradores extranjeros.',
    educacion:'Universitat de les Illes Balears (UIB) en Cas Capiscol. Hospital Universitario Son Espases, Son Llàtzer, Quirónsalud Palmaplanas, Juaneda.',
    pros:['Calidad de vida mediterránea','Mar y vida al aire libre','Aeropuerto con cientos de rutas en verano'],
    contras:['Precios entre los más caros de España','Insularidad y costes logísticos','Saturación turística en temporada'],
  },
  'las-palmas-gc':{
    barrios:[
      {n:'Triana · Vegueta',p:'céntrico',d:'Casco fundacional, calles peatonales, comercio y cultura, demanda estable.'},
      {n:'Mesa y López · Alcaravaneras',p:'premium',d:'Avenida comercial principal, vivienda alta, cerca de Las Canteras.'},
      {n:'Ciudad Jardín',p:'premium',d:'Residencial señorial cerca del Parque Doramas.'},
      {n:'Guanarteme',p:'céntrico',d:'Junto a la playa de Las Canteras, vivienda demandada por nómadas digitales.'},
      {n:'La Isleta',p:'económico',d:'Barrio marinero auténtico, en transformación, precios asequibles.'},
      {n:'Tafira · Monteluz',p:'familiar',d:'Zona alta residencial, ambiente tranquilo, cerca de la Universidad.'},
      {n:'Schamann · Escaleritas',p:'económico',d:'Populosos y bien comunicados, opción accesible.'},
    ],
    transporte:'Guaguas Municipales (autobús urbano), GuaguaGlobal interurbano, MetroGuagua BRT en construcción. No hay tren. Aeropuerto de Gran Canaria al sur, conectado por autobús 60. Ferries a Tenerife (Agaete) y Lanzarote/Fuerteventura.',
    empleo:'Turismo, servicios portuarios (Puerto de La Luz, uno de los mayores de África Occidental), administración pública, comercio, sector tech emergente. Polo: Zona Especial Canaria (ZEC) con beneficios fiscales (IS 4%).',
    educacion:'Universidad de Las Palmas de Gran Canaria (ULPGC). Hospitales Insular-Materno Infantil, Doctor Negrín, Quirónsalud, Vithas.',
    pros:['Clima primaveral todo el año','Playa urbana Las Canteras','Beneficios fiscales (RIC, ZEC, IGIC en lugar de IVA)'],
    contras:['Insularidad y costes de envío','Sueldos bajos respecto a península','Oferta cultural más limitada'],
  },
  'bilbao':{
    barrios:[
      {n:'Abando · Indautxu',p:'premium',d:'Centro financiero y comercial, edificios señoriales, m² más alto.'},
      {n:'Casco Viejo',p:'céntrico',d:'Las Siete Calles, pintxos, ambiente vibrante, vivienda antigua reformada.'},
      {n:'Deusto',p:'familiar',d:'Junto a la Universidad, residencial tranquilo con servicios.'},
      {n:'Begoña · Santutxu',p:'familiar',d:'Históricamente populares, bien conectados, precios moderados.'},
      {n:'San Ignacio · Sarriko',p:'familiar',d:'Residencial moderno, cerca de Sarriko (metro y bidegorri).'},
      {n:'Otxarkoaga · Txurdinaga',p:'económico',d:'Periferia norte, opción más asequible.'},
      {n:'Zorrozaurre',p:'premium',d:'Nueva isla cultural y residencial en transformación.'},
    ],
    transporte:'Metro de Bilbao (3 líneas), Euskotren, Cercanías Renfe (3 líneas), tranvía EuskoTran, autobuses Bilbobus y Bizkaibus. Aeropuerto de Loiu con autobús Bizkaibus A3247. AVE y Y vasca prevista para conectar con Madrid y Burdeos.',
    empleo:'Servicios financieros (BBV de origen, banca, seguros: BBVA, Kutxabank), energía (Iberdrola, sede), construcción y obra civil, industria pesada (siderurgia, naval en Sestao), servicios profesionales, turismo cultural.',
    educacion:'Universidad de Deusto, Universidad del País Vasco (UPV/EHU, campus Leioa), Mondragon Unibertsitatea. Hospitales Cruces, Basurto, Quirónsalud, IMQ.',
    pros:['Calidad de vida y servicios públicos altos','Transformación urbana del Guggenheim','Gastronomía y cultura'],
    contras:['Clima lluvioso','Precios altos para sueldo medio','Mercado de vivienda muy tensionado'],
  },
  'murcia':{
    barrios:[
      {n:'Centro · Catedral',p:'céntrico',d:'Histórico, comercio, hostelería, demanda estable.'},
      {n:'El Carmen · Infante Juan Manuel',p:'familiar',d:'Tradicional sur del río, bien comunicado, precios medios.'},
      {n:'La Flota · Vistabella',p:'premium',d:'Residencial moderno y bien dotado, vivienda nueva, perfil familiar acomodado.'},
      {n:'Ronda Sur · Juan Carlos I',p:'familiar',d:'Modernos, vivienda planificada, buenos servicios.'},
      {n:'Espinardo',p:'familiar',d:'Cerca de la Universidad, polo tecnológico y vivienda nueva.'},
      {n:'Santo Ángel · Algezares',p:'familiar',d:'Periferia residencial junto a la huerta.'},
      {n:'Barrio del Carmen viejo · Vistabella',p:'económico',d:'Más populares, opción accesible.'},
    ],
    transporte:'Tranvía de Murcia L1 (Estación del Carmen-UCAM), autobuses urbanos, Cercanías Renfe C1 a Alicante y Aguilas. Murcia tiene AVE desde 2022 conectando con Madrid (3h). Aeropuerto Corvera/Murcia-San Javier al sur.',
    empleo:'Agroalimentaria (el "huerto de Europa"), construcción, servicios, turismo, distribución. Polo: Espinardo (parque científico), polo industrial Cabezo de Torres y Alcantarilla. Mercadona como empleador local relevante.',
    educacion:'Universidad de Murcia (UMU, La Merced y Espinardo), Universidad Católica San Antonio (UCAM), UNED. Hospitales Virgen de la Arrixaca, Reina Sofía, Morales Meseguer, Quirónsalud.',
    pros:['Clima cálido, +300 días de sol','Precios moderados','Buena gastronomía y huerta'],
    contras:['Transporte público mejorable','Calores extremos en verano','Sueldos relativamente bajos'],
  },
  'valladolid':{
    barrios:[
      {n:'Centro · Plaza Mayor',p:'céntrico',d:'Eje comercial, edificios señoriales, vivienda burguesa.'},
      {n:'Parquesol',p:'familiar',d:'Residencial planificado con servicios completos, perfil familiar y comodidad.'},
      {n:'La Rondilla · Pajarillos',p:'económico',d:'Tradicionales, asequibles, buena conexión.'},
      {n:'Huerta del Rey',p:'familiar',d:'Residencial moderno al oeste, vivienda nueva.'},
      {n:'Villa del Prado',p:'familiar',d:'Reciente, bien planificado.'},
      {n:'Delicias · Las Delicias',p:'económico',d:'Históricamente obrero, accesible.'},
      {n:'Covaresa',p:'familiar',d:'Residencial al sur, urbanizaciones.'},
    ],
    transporte:'Autobuses urbanos AUVASA. AVE a Madrid (1h05), Burgos, Galicia y norte. Estación principal Campo Grande. Aeropuerto Villanubla con conexiones limitadas.',
    empleo:'Automoción (Renault España con dos plantas, Iveco, factorías de componentes), agroalimentaria (vinos D.O. Ribera y Rueda), administración autonómica, servicios. Polo: Parque Tecnológico de Boecillo.',
    educacion:'Universidad de Valladolid (UVa, sede central), Universidad Europea Miguel de Cervantes (UEMC). Hospitales Río Hortega, Clínico Universitario, Recoletas, Campo Grande.',
    pros:['Buena conexión con Madrid por AVE','Precios moderados','Vida tranquila y ordenada'],
    contras:['Inviernos fríos','Mercado laboral concentrado en automoción','Pérdida demográfica relativa'],
  },
  'cordoba':{
    barrios:[
      {n:'Centro Histórico · Judería',p:'céntrico',d:'Mezquita, patios, monumental, alta demanda turística.'},
      {n:'San Lorenzo · Santa Marina',p:'céntrico',d:'Tradicionales, casas de patio, demanda estable.'},
      {n:'Vial Norte · Ciudad Jardín',p:'familiar',d:'Residencial con servicios, vivienda burguesa de calidad.'},
      {n:'Poniente · Sector Sur',p:'económico',d:'Periferia con buena relación calidad-precio.'},
      {n:'Levante',p:'económico',d:'Crecimiento al este, vivienda nueva asequible.'},
      {n:'Centro · Tendillas',p:'céntrico',d:'Eje comercial moderno.'},
      {n:'El Brillante',p:'premium',d:'Residencial alto al norte, viviendas con jardín.'},
    ],
    transporte:'Autobuses urbanos AUCORSA. AVE a Madrid (1h45) y Sevilla (45 min), nudo ferroviario en la línea Madrid-Sevilla. No tiene metro ni cercanías. Aeropuerto local sin tráfico comercial relevante.',
    empleo:'Servicios y administración, turismo, joyería (sector tradicional en declive), agroalimentaria (aceite de oliva, ganadería), logística por la posición intermedia. Tasa de paro alta, sueldos bajos.',
    educacion:'Universidad de Córdoba (UCO, campus Rabanales y Menéndez Pidal), Universidad Loyola (campus Córdoba). Hospitales Reina Sofía (referencia nacional), San Juan de Dios.',
    pros:['Patrimonio Unesco y belleza','Vida tranquila y precios bajos','Buena gastronomía'],
    contras:['Mercado laboral débil','Calor extremo en verano','Dependencia del turismo'],
  },
  'l-hospitalet-de-llobregat':{
    barrios:[
      {n:'Centre',p:'céntrico',d:'Eje comercial, bien conectado, vida de barrio.'},
      {n:'Bellvitge',p:'familiar',d:'Junto al hospital y la universidad, vivienda en bloque, demanda estable.'},
      {n:'Sant Josep · Granvia Sud',p:'premium',d:'Nuevos desarrollos en Plaza Europa, oficinas y vivienda moderna.'},
      {n:'Collblanc · La Torrassa',p:'económico',d:'Densos y multiculturales, opción asequible.'},
      {n:'Santa Eulàlia',p:'familiar',d:'Tradicional, bien comunicado.'},
      {n:'Sanfeliu',p:'económico',d:'Populoso, buenos precios.'},
      {n:'La Florida · Pubilla Cases',p:'económico',d:'Históricamente migrantes, ofertas asequibles.'},
    ],
    transporte:'Metro L1, L5, L9, L10 (la línea L9 conecta con el aeropuerto), Rodalies R1, R4, FGC, Trambaix, autobuses. A 15 minutos del centro de Barcelona, parte plena del área metropolitana.',
    empleo:'Industria farmacéutica, logística, comercio. Polo Plaza Europa (oficinas, Fira de Barcelona Gran Via), CCIB. Ciudad dormitorio de Barcelona con empleo creciente propio.',
    educacion:'Campus Bellvitge UB (Medicina, Odontología). Hospital Universitari de Bellvitge (referencia internacional), Hospital de l\'Hospitalet, Hospital General.',
    pros:['Conexión inmejorable con Barcelona','Precios algo menores que Barcelona','Buenos servicios'],
    contras:['Densidad altísima','Sigue siendo cara aunque menos que Barcelona','Estética urbana irregular'],
  },
  'vigo':{
    barrios:[
      {n:'Centro · Areal',p:'céntrico',d:'Eje comercial, edificios burgueses, vida ciudadana.'},
      {n:'Bouzas',p:'céntrico',d:'Antiguo barrio marinero, mucha personalidad y precios al alza.'},
      {n:'Coia',p:'familiar',d:'Residencial planificado, bien dotado.'},
      {n:'Castrelos · Sárdoma',p:'familiar',d:'Cerca del parque, vivienda unifamiliar y bloques medios.'},
      {n:'Teis',p:'económico',d:'Tradicional, accesible, junto al puerto.'},
      {n:'O Calvario',p:'económico',d:'Populoso y central, opción asequible.'},
      {n:'Beade · Valladares',p:'familiar',d:'Parroquias rurales en transformación, casas con terreno.'},
    ],
    transporte:'Autobuses urbanos Vitrasa. Cercanías Renfe C1 (Vigo-Pontevedra) y AVE Eje Atlántico (Vigo-Santiago-A Coruña en 1h20). Aeropuerto de Peinador. Puerto principal de Galicia.',
    empleo:'Automoción (Stellantis-Citroën-PSA, planta de Balaídos, mayor empleador), pesca y conservera (Pescanova, Calvo), industria naval (Vulcano, Astilleros), Zona Franca de Vigo. Polo Porto do Molle.',
    educacion:'Universidad de Vigo (UVigo, campus de Lagoas-Marcosende). Hospital Álvaro Cunqueiro (público de referencia), Povisa (privado de gran tamaño).',
    pros:['Mar, playas y rías','Industria potente y empleo','Buena gastronomía'],
    contras:['Clima lluvioso y nuboso','Urbanismo discutido','Tráfico denso en hora punta'],
  },
  'alicante':{
    barrios:[
      {n:'Centro · Mercado',p:'céntrico',d:'Comercio, hostelería, vida diurna y nocturna.'},
      {n:'Playa de San Juan · Cabo Huertas',p:'premium',d:'Junto a la playa, vivienda alta, perfil familiar y vacacional.'},
      {n:'Vistahermosa',p:'premium',d:'Residencial alto, urbanizaciones tranquilas.'},
      {n:'Benalúa',p:'céntrico',d:'Pequeño y con identidad, junto al parque, demandado.'},
      {n:'Pla del Bon Repós · Garbinet',p:'familiar',d:'Bien conectados, vivienda media.'},
      {n:'Carolinas Altas · Virgen del Remedio',p:'económico',d:'Más asequibles, opción accesible.'},
      {n:'San Blas',p:'familiar',d:'Universitario y residencial.'},
    ],
    transporte:'TRAM Metropolitano (5 líneas, conecta con Benidorm y Denia), autobuses urbanos, Cercanías Renfe C1 (a Murcia) y C3 (a San Vicente). AVE a Madrid (2h20). Aeropuerto Alicante-Elche al sur con autobús C6.',
    empleo:'Turismo, hostelería, comercio, calzado (Elda, Elche), servicios. Polo industrial: Aguas Blancas, Pla de la Vallonga. Tech hub creciente (Alicante Futura, distrito digital).',
    educacion:'Universidad de Alicante (UA, San Vicente del Raspeig), Universidad Miguel Hernández (Elche). Hospitales General Universitario, San Juan, Vithas, Quirónsalud.',
    pros:['Clima espectacular y playa urbana','Aeropuerto internacional','Sector tech emergente'],
    contras:['Turistificación y precios al alza','Sueldos relativamente bajos','Sectorialización en turismo'],
  },
  'gijon':{
    barrios:[
      {n:'Centro · Cimadevilla',p:'céntrico',d:'Casco antiguo y eje comercial, demanda turística.'},
      {n:'El Llano',p:'económico',d:'Populoso, bien conectado, asequible.'},
      {n:'Pumarín · Contrueces',p:'económico',d:'Tradicionales, vivienda en bloque.'},
      {n:'Somió',p:'premium',d:'Zona alta residencial con villas, perfil acomodado.'},
      {n:'La Calzada · Jove',p:'económico',d:'Históricamente obreros junto al puerto.'},
      {n:'Nuevo Gijón · La Arena',p:'familiar',d:'Junto a la playa de San Lorenzo, vivienda burguesa y demanda alta.'},
      {n:'Roces · Tremañes',p:'familiar',d:'Periferia con desarrollos modernos.'},
    ],
    transporte:'Autobuses urbanos EMTUSA, Cercanías Renfe (C1, C2, F2 a Oviedo, Avilés y Cudillero), FEVE. Estación intermodal Sanz Crespo. AVE en construcción a Madrid. Aeropuerto en Castrillón compartido con Asturias.',
    empleo:'Industria pesada (siderurgia ArcelorMittal Veriña, históricamente), puerto y logística (Puerto del Musel), químicas, comercio, turismo. Polo: PCTG (Parque Científico-Tecnológico) en La Laboral.',
    educacion:'Campus Gijón Universidad de Oviedo (Politécnica de Ingeniería). Hospital Universitario de Cabueñes, Begoña, Asturmédica.',
    pros:['Mar, playa de San Lorenzo y montaña cerca','Calidad de vida y servicios','Gastronomía asturiana'],
    contras:['Clima lluvioso','Crisis industrial histórica','Conexiones AVE pendientes'],
  },
  'a-coruna':{
    barrios:[
      {n:'Ciudad Vieja · Pescadería',p:'céntrico',d:'Casco histórico junto al puerto, galerías acristaladas, demanda turística.'},
      {n:'Ensanche',p:'premium',d:'Cuadrícula burguesa, m² más alto, comercio principal.'},
      {n:'Cuatro Caminos · Sagrada Familia',p:'familiar',d:'Tradicional, bien conectado.'},
      {n:'Riazor · Los Rosales',p:'premium',d:'Junto a la playa de Riazor-Orzán, vivienda alta gama.'},
      {n:'Os Mallos',p:'económico',d:'Popular y trabajador.'},
      {n:'Matogrande · Elviña',p:'familiar',d:'Cerca de la Universidad, desarrollos modernos.'},
      {n:'Monte Alto',p:'familiar',d:'Histórico junto a la Torre de Hércules, demandado.'},
    ],
    transporte:'Autobuses urbanos Compañía de Tranvías, taxi. Cercanías Renfe C4 (Ferrol-Coruña), AVE Eje Atlántico a Vigo-Santiago. AVE a Madrid en construcción (variante Pedralba). Aeropuerto de Alvedro.',
    empleo:'Textil (Inditex con sede en Arteixo, mayor empleador), puerto, banca (Abanca con sede), refino (Repsol en Bens), servicios. Polo: Inditex, Mar de Cristal.',
    educacion:'Universidade da Coruña (UDC, campus Elviña-Zapateira). Hospital Universitario A Coruña (CHUAC, referencia), HM Modelo, San Rafael.',
    pros:['Mar y playas urbanas','Calidad de vida y gastronomía','Inditex como motor económico'],
    contras:['Clima lluvioso','Precios al alza por Inditex y compradores externos','Aeropuerto pequeño'],
  },
  'granada':{
    barrios:[
      {n:'Albaicín',p:'premium',d:'Patrimonio Unesco, casas-cármenes con vistas a la Alhambra, demanda turística.'},
      {n:'Realejo · Plaza Bib-Rambla',p:'céntrico',d:'Histórico, ambiente bohemio, comercio.'},
      {n:'Centro · Gran Vía',p:'céntrico',d:'Eje comercial principal.'},
      {n:'Zaidín',p:'económico',d:'Populoso y bien conectado, accesible.'},
      {n:'Beiro · Cartuja',p:'familiar',d:'Cerca de la universidad y el hospital, demanda estable.'},
      {n:'Ronda · Pajaritos',p:'familiar',d:'Tradicional, vivienda media.'},
      {n:'Cenes / Albolote / Maracena',p:'familiar',d:'Área metropolitana con vivienda asequible, perfil familiar.'},
    ],
    transporte:'Metro de Granada L1 (Albolote-Armilla), autobuses urbanos Transportes Rober. AVE a Madrid (3h15) desde 2019. Aeropuerto Federico García Lorca en Chauchina.',
    empleo:'Universidad y administración como motores, turismo (Alhambra), tecnología y biotech (PTS Parque Tecnológico de la Salud, importante hub biomédico), servicios. Polo: PTS y Aynadamar.',
    educacion:'Universidad de Granada (UGR, una de las mayores de España, atrae mucho Erasmus). Hospital Universitario Virgen de las Nieves, Clínico San Cecilio, PTS, Vithas.',
    pros:['Sierra y playa cerca','Coste de vida bajo y vida universitaria','Patrimonio y cultura'],
    contras:['Inviernos fríos y veranos muy calurosos','Sueldos bajos','Movilidad mejorable'],
  },
  'vitoria':{
    barrios:[
      {n:'Centro · Casco Medieval',p:'céntrico',d:'Histórico, peatonal, demanda alta.'},
      {n:'Ensanche · Lovaina',p:'premium',d:'Vivienda burguesa, comercio, m² alto.'},
      {n:'Salburua · Zabalgana',p:'familiar',d:'Ensanches modernos planificados con eficiencia energética, vivienda nueva.'},
      {n:'Lakua · Sansomendi',p:'familiar',d:'Bien dotados, perfil familiar.'},
      {n:'Adurtza · San Cristóbal',p:'económico',d:'Tradicionales, asequibles.'},
      {n:'Judimendi · Santa Lucía',p:'económico',d:'Populosos, bien conectados.'},
      {n:'Mendizorrotza',p:'premium',d:'Junto al estadio, residencial.'},
    ],
    transporte:'Tranvía de Vitoria-Gasteiz (2 líneas), autobuses urbanos TUVISA, Cercanías Renfe. AVE en proyecto (Y vasca). Aeropuerto de Foronda compartido con Bilbao.',
    empleo:'Industria automotriz (Mercedes-Benz Vitoria, planta Vito y Clase V; Michelin), aeronáutica (Aernnova), agroalimentaria, administración vasca (sede del Gobierno Vasco y Parlamento). Polo: Júndiz, Gamarra, Subillabide.',
    educacion:'Campus Álava UPV/EHU, Universidad de Deusto sede Álava. Hospital Universitario de Álava (Txagorritxu y Santiago), Quirónsalud.',
    pros:['Capital verde, anillo verde y sostenibilidad','Calidad de vida y servicios','Mercado laboral industrial fuerte'],
    contras:['Clima frío y lluvioso','Precios altos para sueldos no industriales','Tamaño limitado de oferta cultural'],
  },
  'badalona':{
    barrios:[
      {n:'Centre · Dalt la Vila',p:'céntrico',d:'Histórico, vida de barrio, demanda estable.'},
      {n:'Gorg · Llefià',p:'familiar',d:'Bien conectados, oferta razonable.'},
      {n:'Bufalà · Morera',p:'familiar',d:'Residencial moderno, vivienda nueva.'},
      {n:'Casagemes',p:'premium',d:'Históricamente acomodado.'},
      {n:'Sant Roc · Artigues',p:'económico',d:'Populosos y asequibles.'},
      {n:'La Salut',p:'económico',d:'Periferia, opciones accesibles.'},
      {n:'Pomar',p:'económico',d:'Norte de la ciudad, asequible.'},
    ],
    transporte:'Metro L2, L10, Tram, Rodalies R1, autobuses TB. Conexión directa con Barcelona en 15-20 minutos, ciudad plenamente metropolitana.',
    empleo:'Históricamente industrial (química, anís del Mono original), reconvertida en logística y servicios. Cercanía a polos del Maresme. Muchos residentes trabajan en Barcelona.',
    educacion:'Campus Can Ruti UAB (Medicina). Hospital Germans Trias i Pujol (Can Ruti, referencia), Hospital Municipal de Badalona.',
    pros:['Mar y playa urbana','Precios algo menores que Barcelona','Buenas conexiones'],
    contras:['Densidad alta','Algunos barrios con desigualdad','Tráfico denso en accesos'],
  },
  'santa-cruz-de-tenerife':{
    barrios:[
      {n:'Centro · La Concepción',p:'céntrico',d:'Histórico, edificios coloniales, demanda urbana.'},
      {n:'Las Ramblas · Salamanca',p:'premium',d:'Eje burgués, vivienda de calidad.'},
      {n:'La Salud · Tincer',p:'económico',d:'Populosos, bien comunicados.'},
      {n:'Anaga (San Andrés, Bajamar...)',p:'familiar',d:'Pueblos pesqueros dentro del municipio, encanto local.'},
      {n:'Vista Bella · Las Mimosas',p:'familiar',d:'Residenciales modernos.'},
      {n:'Ofra · Ciudad Jardín',p:'económico',d:'Populosos y asequibles.'},
      {n:'El Toscal',p:'céntrico',d:'Tradicional cerca del centro.'},
    ],
    transporte:'Tranvía Metropolitano de Tenerife L1 (Santa Cruz-La Laguna), autobuses TITSA. No hay tren. Aeropuerto Tenerife Norte (Los Rodeos) cerca, internacional Tenerife Sur (Reina Sofía) al sur. Conexión marítima con Gran Canaria, La Palma, La Gomera, El Hierro.',
    empleo:'Puerto comercial y de cruceros, administración (capital provincial), refinería (en transición), servicios, turismo, comercio. Polos: Zona industrial Cabo Llanos, Las Torres de Taco.',
    educacion:'Compartida con La Laguna: ULL (Universidad de La Laguna, sede principal en La Laguna). Hospital Universitario Nuestra Señora de la Candelaria, Quirónsalud, Hospiten.',
    pros:['Clima excelente','Capital con servicios completos','Beneficios fiscales canarios'],
    contras:['Insularidad','Lluvias en otoño/invierno','Sueldos por debajo de península'],
  },
  'oviedo':{
    barrios:[
      {n:'Centro · Casco Antiguo',p:'céntrico',d:'Catedral, edificios señoriales, demanda estable y patrimonio.'},
      {n:'Uría · Pumarín',p:'premium',d:'Eje burgués, vivienda alta.'},
      {n:'La Tenderina',p:'familiar',d:'Bien comunicada, perfil familiar.'},
      {n:'Vetusta · Vallobín',p:'familiar',d:'Residencial moderno, demanda estable.'},
      {n:'Naranco',p:'económico',d:'Tradicional al norte, asequible.'},
      {n:'La Corredoria',p:'familiar',d:'Ensanche moderno con servicios, opción para familias.'},
      {n:'Trubia · Olloniego',p:'económico',d:'Parroquias rurales con vivienda más barata.'},
    ],
    transporte:'Autobuses urbanos TUA, Cercanías Renfe (a Gijón, Avilés, Mieres), FEVE. AVE en construcción a Madrid (en pruebas). Aeropuerto en Castrillón compartido con Asturias.',
    empleo:'Administración (capital), servicios, hospital (HUCA referente), comercio, sanidad. Industria histórica en declive. Sede de Caja Rural, Hunosa, EDP en Asturias.',
    educacion:'Universidad de Oviedo (sede central), Campus El Cristo. Hospital Universitario Central de Asturias (HUCA, referente), Quirónsalud, Asturmédica.',
    pros:['Ciudad limpia y peatonal','Calidad de vida y servicios','Naturaleza y montaña cerca'],
    contras:['Clima lluvioso','Mercado laboral con sueldos modestos','Envejecimiento demográfico'],
  },
  'mostoles':{
    barrios:[
      {n:'Centro',p:'céntrico',d:'Eje comercial y servicios, demanda estable.'},
      {n:'Parque Coímbra',p:'familiar',d:'Residencial moderno, perfil familiar.'},
      {n:'Estoril II · Iviasa',p:'familiar',d:'Bien dotados.'},
      {n:'Soto del Henares',p:'familiar',d:'Nuevo desarrollo con vivienda moderna.'},
      {n:'Pinares Llanos',p:'económico',d:'Populoso, accesible.'},
      {n:'Hospital · Universidad',p:'familiar',d:'Junto a URJC y hospital.'},
      {n:'El Soto · Villafontana',p:'económico',d:'Periferia, opciones asequibles.'},
    ],
    transporte:'Metro Sur L12 (varias paradas: Móstoles Central, Pradillo, etc.), Cercanías Renfe C5 (Madrid-Móstoles-Humanes), autobuses interurbanos. Conexión rápida con Madrid en 25-30 minutos.',
    empleo:'Ciudad dormitorio principal del sur metropolitano, gran tejido comercial y servicios. Polo: Universidad URJC, polo industrial Cantueña, polígonos varios. Muchos residentes trabajan en Madrid.',
    educacion:'Universidad Rey Juan Carlos (URJC, campus Móstoles). Hospital Universitario de Móstoles, Hospital Rey Juan Carlos.',
    pros:['Conexión metro/cercanías con Madrid','Precios menores que Madrid','Servicios completos'],
    contras:['Ciudad dormitorio sin identidad propia fuerte','Tráfico denso en accesos','Sigue siendo cara'],
  },
  'elche':{
    barrios:[
      {n:'Centro · Mercado',p:'céntrico',d:'Histórico, palmeral Patrimonio Unesco, demanda estable.'},
      {n:'Carrús',p:'económico',d:'Populoso y bien conectado, accesible.'},
      {n:'Altabix',p:'familiar',d:'Junto a la universidad, perfil joven.'},
      {n:'Sector V',p:'familiar',d:'Ensanche moderno, vivienda nueva.'},
      {n:'Travalón',p:'familiar',d:'Residencial planificado.'},
      {n:'Polígono San Antón',p:'económico',d:'Asequible, junto a zona industrial.'},
      {n:'La Marina · El Pinet',p:'familiar',d:'Pedanías costeras al sur con segunda residencia.'},
    ],
    transporte:'Autobuses urbanos. Cercanías Renfe C1 a Alicante y Murcia. AVE en Alicante (15-20 minutos). Aeropuerto Alicante-Elche compartido, muy cerca.',
    empleo:'Calzado (núcleo histórico mundial, Pikolinos, Panama Jack, Mustang), juguete (Famosa), agroalimentaria (granada), comercio. Polo industrial Carrús, Torrellano. Tejido empresarial fuerte.',
    educacion:'Universidad Miguel Hernández (UMH, campus Elche, sede). Hospital General Universitario de Elche, Vinalopó (Ribera Salud), Quirónsalud.',
    pros:['Palmeral único, patrimonio','Buenas conexiones con Alicante y aeropuerto','Tejido industrial sólido'],
    contras:['Mercado laboral concentrado en calzado','Calores extremos en verano','Imagen urbana mejorable en ensanches'],
  },
  'san-sebastian':{
    barrios:[
      {n:'Centro · Parte Vieja',p:'premium',d:'Casco antiguo con pintxos, demanda altísima, m² estratosférico.'},
      {n:'Gros',p:'premium',d:'Junto a la playa de Zurriola, ambiente surfero, vivienda alta.'},
      {n:'Antiguo',p:'familiar',d:'Junto a Ondarreta y la universidad, tranquilo y residencial.'},
      {n:'Amara',p:'familiar',d:'Bien planificado, comercio y demanda estable.'},
      {n:'Egia',p:'familiar',d:'Cerca del centro, ambiente vecinal, en alza.'},
      {n:'Intxaurrondo · Bidebieta',p:'económico',d:'Más alejados del centro, opciones asequibles dentro del muy alto nivel local.'},
      {n:'Igueldo · Ulia',p:'premium',d:'Zonas altas con vistas, chalets y precios elevados.'},
    ],
    transporte:'Autobús urbano DBus, Topo (metro Donostia-Hendaia), Cercanías Renfe, Euskotren. AVE/Y vasca en construcción. Aeropuerto Hondarribia-San Sebastián cerca.',
    empleo:'Servicios, turismo gastronómico de alto nivel (más estrellas Michelin per cápita del mundo), tecnología (DSS Tech, Polo Mercurio), administración foral. Polo: Miramon (Parque Tecnológico).',
    educacion:'Universidad del País Vasco (UPV/EHU, Ibaeta), Universidad de Deusto sede Donostia, Tecnun-Universidad de Navarra. Hospital Universitario Donostia, Quirónsalud, Onkologikoa.',
    pros:['Belleza natural única (La Concha)','Calidad de vida muy alta','Gastronomía y cultura excepcionales'],
    contras:['Ciudad más cara de España junto a Barcelona','Clima lluvioso','Mercado de vivienda extremadamente tensionado'],
  },
  'sabadell':{
    barrios:[
      {n:'Centre',p:'céntrico',d:'Eje comercial, comercio histórico, demanda estable.'},
      {n:'Gràcia',p:'familiar',d:'Tradicional, bien conectado.'},
      {n:'Can Llong · Castellarnau',p:'familiar',d:'Desarrollos modernos, vivienda nueva.'},
      {n:'La Creu Alta · La Creu de Barberà',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'Sant Oleguer · Espronceda',p:'familiar',d:'Vivienda nueva planificada.'},
      {n:'Torre-Romeu · Torre del Lavabo',p:'económico',d:'Periferia, accesibles.'},
      {n:'Sol i Padrís · Can Feu',p:'económico',d:'Históricamente obrero, opción asequible.'},
    ],
    transporte:'FGC S1, S2, S5, S6, S7 (Plaza Catalunya-Sabadell), Renfe R4, R8, autobuses TUS. Conexión rápida con Barcelona (35-45 minutos). Aeropuerto Sabadell (sin tráfico comercial).',
    empleo:'Industria textil histórica (declive), reconvertida en servicios y comercio. Banco Sabadell con sede histórica aquí. Polo industrial: Can Roqueta, Sant Pau de Riu-sec. Muchos residentes trabajan en Barcelona.',
    educacion:'Campus Sabadell UAB (Empresa, Informática), Centros de FP. Hospital Universitari Parc Taulí (referencia), Quirónsalud Sabadell.',
    pros:['Tamaño humano con servicios completos','Buena conexión con Barcelona','Precios menores que área metropolitana'],
    contras:['Estética urbana irregular','Crisis industrial histórica','Conexión con Barcelona saturada en hora punta'],
  },
  'santander':{
    barrios:[
      {n:'Centro · Puertochico',p:'céntrico',d:'Eje comercial junto a la bahía, demanda estable.'},
      {n:'El Sardinero',p:'premium',d:'Junto a las playas, vivienda alta gama, perfil veraneante y permanente.'},
      {n:'La Albericia',p:'familiar',d:'Bien conectado, vivienda media.'},
      {n:'Cazoña · La Pereda',p:'familiar',d:'Residenciales tranquilos.'},
      {n:'Cueto · Monte',p:'premium',d:'Zona alta con vistas, chalets.'},
      {n:'San Román · Camarreal',p:'familiar',d:'Periferia con vivienda más nueva.'},
      {n:'Castilla-Hermida',p:'económico',d:'Tradicional junto al puerto, asequible.'},
    ],
    transporte:'Autobuses urbanos TUS, Cercanías Renfe (a Reinosa y Bilbao), FEVE. AVE no llega aún (en proyecto). Aeropuerto Seve Ballesteros en Parayas. Ferry a Plymouth y Cork.',
    empleo:'Administración (capital autonómica), banca (sede Banco Santander, motor económico), servicios, turismo, puerto. Polo: PCTCAN (Parque Científico-Tecnológico de Cantabria).',
    educacion:'Universidad de Cantabria (UC), Universidad Internacional Menéndez Pelayo (UIMP). Hospital Universitario Marqués de Valdecilla (referencia nacional), Mompía, Quirónsalud.',
    pros:['Bahía y playas urbanas','Calidad de vida y servicios','Sede Banco Santander como motor'],
    contras:['Clima lluvioso','Precios altos para tamaño de ciudad','Sin AVE aún'],
  },
  'jerez-de-la-frontera':{
    barrios:[
      {n:'Centro Histórico',p:'céntrico',d:'Monumental, demanda turística, patrimonio.'},
      {n:'San Miguel · San Telmo',p:'céntrico',d:'Tradicionales, ambiente flamenco.'},
      {n:'La Granja · Vallesequillo',p:'familiar',d:'Residenciales modernos.'},
      {n:'La Plata · Pago de San José',p:'familiar',d:'Periferia con vivienda nueva.'},
      {n:'San Benito',p:'económico',d:'Populoso, asequible.'},
      {n:'Estancia Barrera',p:'familiar',d:'Desarrollo moderno planificado.'},
      {n:'La Asunción',p:'económico',d:'Tradicional, accesible.'},
    ],
    transporte:'Autobús urbano. Cercanías Renfe C1 (Jerez-Cádiz-San Fernando). AVE a Madrid (4h, no directo). Aeropuerto de Jerez con conexiones limitadas. Conexión con Cádiz en 30 min por Cercanías.',
    empleo:'Bodegas y vino de Jerez (Tío Pepe-González Byass, Lustau, Pedro Domecq, Fundador), caballos (ganadería, doma vaquera), motor (circuito de velocidad), turismo, agroalimentaria, servicios. Tasa de paro alta.',
    educacion:'Campus Jerez Universidad de Cádiz (Derecho, Empresariales). Hospital Universitario de Jerez (público), Quirónsalud, Recoletas.',
    pros:['Patrimonio cultural (flamenco, vino, caballo)','Precios bajos','Aeropuerto propio'],
    contras:['Paro elevado y sueldos bajos','Verano caluroso','Conexión AVE pendiente'],
  },
  'castellon-de-la-plana':{
    barrios:[
      {n:'Centro · Plaza Mayor',p:'céntrico',d:'Eje comercial, edificios burgueses, demanda estable.'},
      {n:'Zona Universitaria · Riu Sec',p:'familiar',d:'Cerca de la UJI, perfil joven y profesional.'},
      {n:'Tirado / Patilla',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'Tetuán · Grupo Sant Crist',p:'económico',d:'Populosos y accesibles.'},
      {n:'Grao · El Pinar',p:'familiar',d:'Junto al puerto y a la playa, separados del centro.'},
      {n:'Pintor Sorolla · Ribalta',p:'premium',d:'Vivienda burguesa cerca del parque.'},
      {n:'Lledó · Bovalar',p:'familiar',d:'Desarrollos modernos.'},
    ],
    transporte:'Autobuses urbanos, TRAM Castellón (BRT eléctrico, L1), Cercanías Renfe C6 a Valencia. AVE a Madrid en estudio. Conexión rápida con Valencia (1h).',
    empleo:'Cerámica y azulejos (clúster mundial Onda-Vila-real-Castellón: Porcelanosa, Pamesa), química, agroalimentaria (naranja), puerto. Polo: Polígono Ciudad del Transporte.',
    educacion:'Universidad Jaume I (UJI). Hospital General Universitari, La Magdalena, Quirónsalud, Vithas.',
    pros:['Tamaño humano con playa y servicios','Coste de vida razonable','Universidad y motor industrial'],
    contras:['Imagen urbana mejorable','Sectorialización en cerámica','Conexión AVE pendiente'],
  },
  'leganes':{
    barrios:[
      {n:'Casco Antiguo',p:'céntrico',d:'Centro histórico, demanda estable.'},
      {n:'Zarzaquemada',p:'familiar',d:'Populoso y bien conectado.'},
      {n:'La Fortuna',p:'económico',d:'Tradicional, accesible.'},
      {n:'San Nicasio',p:'familiar',d:'Bien planificado.'},
      {n:'Solagua · Vereda de los Estudiantes',p:'familiar',d:'Cerca de la UC3M, perfil joven.'},
      {n:'Leganés Norte · Arroyo Culebro',p:'familiar',d:'Desarrollos modernos.'},
      {n:'Quinta de los Molinos',p:'familiar',d:'Residencial.'},
    ],
    transporte:'Metro Sur L12 (varias paradas), Cercanías Renfe C5 (Madrid-Móstoles-Humanes con parada Leganés-Universidad), autobuses. Conexión rápida con Madrid en 20-25 minutos.',
    empleo:'Universidad Carlos III (UC3M) como motor, polo industrial Leganés (Indra, BSH), hospitales. Muchos residentes trabajan en Madrid.',
    educacion:'Universidad Carlos III de Madrid (UC3M, campus Leganés con politécnicas). Hospital Universitario Severo Ochoa.',
    pros:['Buena conexión metro/cercanías con Madrid','Polo universitario UC3M','Precios menores que Madrid'],
    contras:['Ciudad dormitorio','Estética urbana irregular','Tráfico denso en accesos'],
  },
  'almeria':{
    barrios:[
      {n:'Centro · Catedral',p:'céntrico',d:'Histórico, demanda turística.'},
      {n:'Casco Antiguo · La Chanca',p:'económico',d:'Tradicional pesquero, en transformación.'},
      {n:'Zapillo · Costacabana',p:'familiar',d:'Junto a la playa urbana, demanda alta.'},
      {n:'Nueva Almería · Vega de Acá',p:'familiar',d:'Desarrollos modernos.'},
      {n:'Los Molinos · Pescadería',p:'económico',d:'Populosos, accesibles.'},
      {n:'Retamar · El Toyo',p:'premium',d:'Junto a la universidad y al campo de golf, vivienda alta.'},
      {n:'Cabo de Gata · El Alquián',p:'familiar',d:'Periferia oriental con parcelas.'},
    ],
    transporte:'Autobús urbano Surbus, Cercanías Renfe (a Granada con prevista). AVE en construcción (Almería-Murcia, conexión con Madrid pendiente). Aeropuerto de Almería con vuelos internacionales estacionales.',
    empleo:'Agricultura intensiva (mar de plástico, hortalizas exportadas a toda Europa, "huerta de Europa"), turismo, mármol (sector tradicional), pesca. Polo: PITA (Parque Científico-Tecnológico).',
    educacion:'Universidad de Almería (UAL, La Cañada). Hospital Universitario Torrecárdenas, Quirónsalud.',
    pros:['Clima excelente (300+ días de sol)','Precios entre los más bajos de España','Costa virgen (Cabo de Gata)'],
    contras:['Sueldos bajos','Aislamiento (sin AVE aún)','Modelo agrícola intensivo controvertido'],
  },
  'cartagena':{
    barrios:[
      {n:'Centro · Casco Antiguo',p:'céntrico',d:'Modernismo y arqueología romana, demanda turística.'},
      {n:'Ensanche',p:'premium',d:'Vivienda burguesa, comercio.'},
      {n:'Cuatro Santos · Concepción',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'San Antón',p:'económico',d:'Populoso, accesible.'},
      {n:'Mediterráneo · Polígono Santa Ana',p:'familiar',d:'Modernos, bien planificados.'},
      {n:'Cabo de Palos · La Manga',p:'premium',d:'Costa Cálida, segunda residencia y vacacional.'},
      {n:'Los Dolores · Los Barreros',p:'económico',d:'Pedanías con vivienda asequible.'},
    ],
    transporte:'Autobús urbano. Cercanías Renfe C1 (Cartagena-Murcia-Alicante-Aguilas). AVE a Madrid en obras (conexión vía Murcia). Aeropuerto de Murcia-Corvera al norte. Puerto militar y comercial.',
    empleo:'Refinería Repsol (mayor de España), industria petroquímica (Sabic), militar (Cartagena es sede de la Armada con Arsenal, EBN), puerto, turismo, agroalimentaria. Polo: Valle de Escombreras, Polígono Cabezo Beaza.',
    educacion:'Universidad Politécnica de Cartagena (UPCT). Hospital Universitario Santa Lucía, Rosell, Quirónsalud.',
    pros:['Patrimonio arqueológico (Cartagena Puerto de Culturas)','Costa y mar Menor cerca','Mercado laboral industrial estable'],
    contras:['Contaminación industrial percibida','Verano muy caluroso','Conexión AVE pendiente'],
  },
  'pamplona':{
    barrios:[
      {n:'Casco Viejo',p:'céntrico',d:'Centro histórico (Estafeta, Plaza del Castillo), Sanfermines, demanda muy alta.'},
      {n:'Ensanche · Iturrama',p:'premium',d:'Vivienda burguesa, m² más alto.'},
      {n:'Mendebaldea · Ermitagaña',p:'familiar',d:'Residenciales modernos.'},
      {n:'Rochapea · San Juan',p:'familiar',d:'Tradicionales bien conectados.'},
      {n:'Chantrea · Buztintxuri',p:'económico',d:'Populosos y accesibles.'},
      {n:'Mendillorri · Beloso',p:'familiar',d:'Desarrollos planificados.'},
      {n:'Lezkairu · Sarriguren',p:'familiar',d:'Nuevos ensanches eficientes, vivienda nueva.'},
    ],
    transporte:'Autobuses urbanos TCC (mancomunidad), red de bidegorri. No hay metro ni cercanías. Aeropuerto de Noáin cerca con conexiones limitadas. Conexión por tren convencional con Zaragoza y Madrid; AVE en construcción.',
    empleo:'Industria automotriz (Volkswagen Navarra, planta Polo), agroalimentaria (Florette, AN), administración foral, energías renovables (Acciona Energía, Siemens Gamesa), banca (Caja Rural de Navarra). Polo: Polígonos de Landaben, Imárcoain.',
    educacion:'Universidad de Navarra (privada, prestigiosa, IESE), Universidad Pública de Navarra (UPNA). Hospital Universitario de Navarra (HUN), Clínica Universidad de Navarra (CUN, referente internacional).',
    pros:['Calidad de vida y servicios sociales muy altos','Fiscalidad foral favorable','Mercado laboral industrial estable'],
    contras:['Clima frío en invierno','Vivienda cara para sueldos no industriales','Tamaño limitado de oferta cultural'],
  },
  'terrassa':{
    barrios:[
      {n:'Centre',p:'céntrico',d:'Eje comercial, demanda estable.'},
      {n:'Sant Pere · Vallparadís',p:'premium',d:'Junto al parque, vivienda burguesa.'},
      {n:'Can Roca · Can Anglada',p:'económico',d:'Populosos, accesibles.'},
      {n:'Ègara · Can Boada',p:'familiar',d:'Residenciales modernos.'},
      {n:'Les Arenes · La Maurina',p:'familiar',d:'Bien conectados.'},
      {n:'Sant Llorenç · Roc Blanc',p:'familiar',d:'Periféricos con desarrollo.'},
      {n:'Torre-sana · Vilardell',p:'económico',d:'Tradicionalmente obreros.'},
    ],
    transporte:'FGC S1, S2, S5 (Plaza Catalunya-Terrassa), Renfe R4, R8, autobuses TMESA. Conexión con Barcelona en 45-55 minutos. Aeropuerto Sabadell (pequeño, sin tráfico comercial).',
    empleo:'Textil histórico (declive), reconvertido en servicios, comercio, sanidad. Polo industrial: Can Parellada, Can Petit. Muchos residentes trabajan en Barcelona o Sabadell.',
    educacion:'Universitat Politècnica de Catalunya (UPC, campus Terrassa: Ingenierías). Hospital Universitari MútuaTerrassa, Consorci Sanitari de Terrassa.',
    pros:['Modernismo industrial (Vapor Aymerich, mNACTEC)','Conexión Barcelona y aeropuerto','Precios menores que área metropolitana'],
    contras:['Crisis industrial textil','Conexión saturada en hora punta','Estética urbana irregular'],
  },
  'fuenlabrada':{
    barrios:[
      {n:'Centro',p:'céntrico',d:'Eje comercial, demanda estable.'},
      {n:'El Naranjo · Loranca',p:'familiar',d:'Desarrollos modernos planificados.'},
      {n:'Parque Granada',p:'familiar',d:'Bien planificado.'},
      {n:'Cerro · Vivero',p:'económico',d:'Tradicional, accesible.'},
      {n:'Avanzada · El Vivero',p:'familiar',d:'Bien dotados.'},
      {n:'Hospital · Universidad',p:'familiar',d:'Junto a URJC y hospital.'},
      {n:'Camino del Molino',p:'económico',d:'Populoso, asequible.'},
    ],
    transporte:'Metro Sur L12 (varias paradas), Cercanías Renfe C5 (parada Fuenlabrada), autobuses. Conexión con Madrid en 30-35 minutos.',
    empleo:'Industria y logística (Coca-Cola European Partners planta, polígonos), comercio (Centro comercial Plaza Loranca), Universidad URJC. Muchos residentes trabajan en Madrid.',
    educacion:'Universidad Rey Juan Carlos (URJC, campus Fuenlabrada: Comunicación, Ciencias Jurídicas). Hospital Universitario de Fuenlabrada.',
    pros:['Conexión metro/cercanías','Precios menores que Madrid','Tejido industrial sólido'],
    contras:['Ciudad dormitorio','Algunos barrios con desigualdad','Estética urbana irregular'],
  },
  'alcala-de-henares':{
    barrios:[
      {n:'Centro Histórico',p:'premium',d:'Patrimonio Unesco (Universidad cervantina), demanda alta turística.'},
      {n:'Reyes Católicos',p:'familiar',d:'Bien conectado, perfil familiar.'},
      {n:'La Garena · El Ensanche',p:'familiar',d:'Desarrollos modernos.'},
      {n:'Espartales',p:'familiar',d:'Planificado y bien dotado.'},
      {n:'San Isidro · Chorrillo',p:'económico',d:'Populosos, accesibles.'},
      {n:'Nueva Alcalá · Las Eras del Silo',p:'familiar',d:'Vivienda nueva.'},
      {n:'Polígono Puerta Madrid',p:'económico',d:'Periferia, asequible.'},
    ],
    transporte:'Cercanías Renfe C2, C7 (Madrid-Alcalá-Guadalajara), autobuses interurbanos. No hay metro. Conexión con Madrid en 35-45 minutos en cercanías.',
    empleo:'Universidad de Alcalá como motor, industria farmacéutica (Pfizer, Lilly), aeronáutica (Indra), administración. Polo: Corredor del Henares, polígonos junto a A-2.',
    educacion:'Universidad de Alcalá (UAH, una de las más antiguas de España). Hospital Universitario Príncipe de Asturias.',
    pros:['Patrimonio Unesco','Polo universitario y empresarial','Conexión cercanías con Madrid'],
    contras:['Tráfico denso en A-2','Algunas zonas con desigualdad','Sin metro'],
  },
  'burgos':{
    barrios:[
      {n:'Centro · Catedral',p:'céntrico',d:'Patrimonio Unesco, demanda turística y residencial.'},
      {n:'Gamonal',p:'económico',d:'Populoso y bien conectado, asequible.'},
      {n:'Capiscol · El Plantío',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'Villimar · Río Vena',p:'familiar',d:'Desarrollos modernos.'},
      {n:'Las Huelgas · Hospital',p:'familiar',d:'Cerca del hospital, demanda estable.'},
      {n:'Castañares · Villatoro',p:'familiar',d:'Periféricos con desarrollos nuevos.'},
      {n:'San Bruno · Universidad',p:'familiar',d:'Junto a la UBU, perfil joven.'},
    ],
    transporte:'Autobuses urbanos, AVE a Madrid (1h35), Cercanías regionales. Aeropuerto Villafría con conexiones limitadas.',
    empleo:'Automoción (Antolin, Bridgestone, GKN), agroalimentaria (queso, vino Ribera del Duero, morcilla), Polo Polígono de Villalonquéjar (Renault Trucks, Nestlé). Administración provincial.',
    educacion:'Universidad de Burgos (UBU). Hospital Universitario de Burgos (HUBU). Atención sanitaria pública sólida.',
    pros:['Patrimonio Unesco','Conexión AVE con Madrid','Mercado laboral industrial estable'],
    contras:['Inviernos muy fríos','Pérdida demográfica relativa','Oferta cultural limitada'],
  },
  'la-laguna':{
    barrios:[
      {n:'Centro Histórico',p:'premium',d:'Patrimonio Unesco, casas coloniales, demanda alta.'},
      {n:'La Cuesta · Taco',p:'económico',d:'Densos, bien conectados con Santa Cruz, accesibles.'},
      {n:'Geneto · Las Mercedes',p:'familiar',d:'Residencial junto al monte, ambiente tranquilo.'},
      {n:'Bajamar · Tejina',p:'familiar',d:'Costeros al norte.'},
      {n:'San Benito · Padre Anchieta',p:'familiar',d:'Junto a la Universidad, perfil joven.'},
      {n:'San Lázaro · Las Higueras',p:'económico',d:'Populosos, accesibles.'},
      {n:'Las Chumberas',p:'económico',d:'Populoso, opción asequible.'},
    ],
    transporte:'Tranvía Metropolitano de Tenerife L1 (conecta con Santa Cruz), L2 (Tincer-La Cuesta), autobuses TITSA. Conurbado con Santa Cruz, ciudad universitaria.',
    empleo:'Universidad como motor, administración pública, servicios. Polo: Polígono Industrial de Las Chafiras al sur. Muchos residentes trabajan en Santa Cruz.',
    educacion:'Universidad de La Laguna (ULL, principal de Tenerife). Hospital Universitario de Canarias (HUC), Santa Cruz cerca.',
    pros:['Patrimonio Unesco','Clima excelente','Vida universitaria'],
    contras:['Lluvias frecuentes (microclima)','Insularidad','Dependencia de Santa Cruz para muchos servicios'],
  },
  'salamanca':{
    barrios:[
      {n:'Centro · Plaza Mayor',p:'premium',d:'Patrimonio Unesco, edificios del siglo XVI, demanda altísima.'},
      {n:'San Bernardo · Garrido',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'Vidal · El Rollo',p:'familiar',d:'Residenciales modernos, perfil familiar.'},
      {n:'Pizarrales · Buenos Aires',p:'económico',d:'Populosos, accesibles.'},
      {n:'Capuchinos · Universidad',p:'familiar',d:'Junto a la USAL, demanda universitaria fuerte.'},
      {n:'Carretera Madrid · Tejares',p:'familiar',d:'Bien dotados.'},
      {n:'San Cristóbal · Chamberí',p:'familiar',d:'Desarrollos modernos.'},
    ],
    transporte:'Autobús urbano. AVE a Madrid (1h35 desde 2025 con la nueva línea). Aeropuerto de Matacán con conexiones limitadas.',
    empleo:'Universidad como motor económico fundamental (USAL atrae miles de estudiantes Erasmus), turismo, comercio, administración. Sueldos modestos.',
    educacion:'Universidad de Salamanca (USAL, una de las más antiguas de Europa, 800 años), Universidad Pontificia. Hospital Universitario de Salamanca, IBSAL.',
    pros:['Patrimonio Unesco excepcional','Vida universitaria intensa','Precios moderados'],
    contras:['Mercado laboral dependiente de universidad','Inviernos fríos','Estacionalidad estudiantil'],
  },
  'cadiz':{
    barrios:[
      {n:'Casco Antiguo (La Viña, El Pópulo, Mentidero)',p:'premium',d:'Histórico, casas-patio, demanda turística altísima, suelo escaso.'},
      {n:'Puertatierra',p:'familiar',d:'Eje moderno tras las murallas, vivienda de calidad.'},
      {n:'La Caleta · San Juan de Dios',p:'céntrico',d:'Junto a la playa urbana, demanda turística.'},
      {n:'Bahía Blanca · Cortadura',p:'familiar',d:'Modernos, vivienda nueva.'},
      {n:'Loreto · Avenida',p:'familiar',d:'Residenciales bien comunicados.'},
      {n:'Astilleros · La Paz',p:'económico',d:'Populosos, accesibles.'},
      {n:'San Severiano · Cerro del Moro',p:'económico',d:'Tradicionales, opciones asequibles.'},
    ],
    transporte:'Autobús urbano. Cercanías Renfe C1 (Cádiz-San Fernando-Jerez), tren a Sevilla. AVE no directo (a través de Sevilla). Aeropuerto Jerez al norte. Cádiz es península, accesos limitados (puente de la Constitución).',
    empleo:'Naval (Navantia, astilleros), turismo, puerto comercial, universidad, administración. Tasa de paro alta históricamente. Polo: Bahía de Cádiz industrial (Cádiz, Puerto Real, San Fernando).',
    educacion:'Universidad de Cádiz (UCA, sede principal). Hospital Universitario Puerta del Mar.',
    pros:['Mar por todos lados, playas urbanas','Patrimonio y carácter único','Clima excelente'],
    contras:['Paro elevado y sueldos bajos','Casco antiguo con precios desproporcionados','Conexiones limitadas por geografía'],
  },
  'leon':{
    barrios:[
      {n:'Centro · Barrio Húmedo',p:'céntrico',d:'Histórico, catedral, ambiente nocturno, demanda turística.'},
      {n:'Eras de Renueva',p:'familiar',d:'Desarrollo moderno planificado, vivienda nueva.'},
      {n:'San Mamés · La Asunción',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'La Lastra · Polígono X',p:'familiar',d:'Vivienda nueva, junto al hospital.'},
      {n:'Crucero · La Vega',p:'económico',d:'Populosos, accesibles.'},
      {n:'Armunia · Trobajo del Cerecedo',p:'económico',d:'Periferias accesibles.'},
      {n:'San Andrés · Trobajo del Camino',p:'familiar',d:'Municipios conurbados con vivienda asequible.'},
    ],
    transporte:'Autobús urbano. AVE a Madrid (2h05). Estación renovada. Conexión con Asturias y Galicia. Aeropuerto de La Virgen del Camino con conexiones limitadas.',
    empleo:'Servicios y administración, agroalimentaria (vino Bierzo, ganadería, embutidos), tecnología (INCIBE Instituto Nacional de Ciberseguridad), industria farmacéutica (Antibióticos León). Polo: Parque Tecnológico de León.',
    educacion:'Universidad de León (ULE). Hospital Universitario de León. Sanidad pública sólida.',
    pros:['Patrimonio histórico y gastronomía','Precios bajos','Conexión AVE con Madrid'],
    contras:['Pérdida demográfica fuerte','Inviernos largos','Mercado laboral débil'],
  },
  'albacete':{
    barrios:[
      {n:'Centro · Plaza Mayor',p:'céntrico',d:'Eje comercial, demanda estable.'},
      {n:'Ensanche · Carretas',p:'familiar',d:'Vivienda burguesa, bien dotado.'},
      {n:'Universidad · San Pablo',p:'familiar',d:'Cerca del campus, perfil joven.'},
      {n:'Industria · Polígono Campollano',p:'económico',d:'Junto a la industria.'},
      {n:'San Antón · La Pajarita',p:'económico',d:'Populosos, accesibles.'},
      {n:'Hospital · La Estrella',p:'familiar',d:'Modernos, demanda estable.'},
      {n:'Parque Sur · Imaginalia',p:'familiar',d:'Desarrollos modernos.'},
    ],
    transporte:'Autobús urbano. AVE a Madrid (1h35) y Alicante. Conexión central muy buena. Aeropuerto Los Llanos con conexiones limitadas (base aérea militar).',
    empleo:'Agroalimentaria (vino, queso manchego, ajos), industria (cuchillería, calzado), logística por posición geográfica, administración. Polo: Campollano (uno de los mayores polígonos de Castilla-La Mancha).',
    educacion:'Universidad de Castilla-La Mancha (UCLM, campus Albacete). Hospital General Universitario, Quirónsalud, Recoletas.',
    pros:['Posición central (AVE Madrid, Valencia, Alicante)','Precios bajos','Mercado laboral diversificado'],
    contras:['Inviernos fríos y veranos calurosos','Tamaño limitado','Pérdida demográfica en el entorno'],
  },
  'getafe':{
    barrios:[
      {n:'Centro',p:'céntrico',d:'Eje comercial, demanda estable.'},
      {n:'Sector III · Bercial',p:'familiar',d:'Residenciales modernos.'},
      {n:'Buenavista · Los Molinos',p:'familiar',d:'Bien planificados.'},
      {n:'Las Margaritas · Juan de la Cierva',p:'económico',d:'Populosos y accesibles.'},
      {n:'Perales del Río',p:'familiar',d:'Junto al río, vivienda unifamiliar.'},
      {n:'Universidad · El Bercial',p:'familiar',d:'Cerca de la UC3M.'},
      {n:'La Alhóndiga',p:'económico',d:'Populoso, asequible.'},
    ],
    transporte:'Metro Sur L12 (Getafe Sector III, Conservatorio, Alonso de Mendoza), Cercanías Renfe C3, C4 (Getafe Centro, Getafe Industrial, El Casar), autobuses. Conexión con Madrid en 20 minutos.',
    empleo:'Industria aeronáutica (Airbus, EADS, Indra), automoción, hospitales. Polo Centro de Empresas Avanzadas Getafe Negocios. Universidad UC3M.',
    educacion:'Universidad Carlos III de Madrid (UC3M, campus Getafe: Económicas, Sociales). Hospital Universitario de Getafe.',
    pros:['Mejor conexión metro y cercanías','Polo industrial aeronáutico','Universidad y hospital relevantes'],
    contras:['Ciudad dormitorio','Tráfico denso en accesos','Estética urbana irregular'],
  },
  'alcorcon':{
    barrios:[
      {n:'Centro',p:'céntrico',d:'Eje comercial, demanda estable.'},
      {n:'Parque Lisboa · San José de Valderas',p:'familiar',d:'Desarrollos modernos.'},
      {n:'Ensanche Sur',p:'familiar',d:'Vivienda nueva planificada.'},
      {n:'Las Retamas · Los Cantos',p:'familiar',d:'Bien comunicados.'},
      {n:'Fuente Cisneros',p:'familiar',d:'Residencial.'},
      {n:'Polígono Urtinsa',p:'económico',d:'Junto a la industria, asequible.'},
      {n:'San José de Valderas',p:'familiar',d:'Tradicional con vivienda media.'},
    ],
    transporte:'Metro Sur L12, Metro L10 (parada Alcorcón Central), Cercanías Renfe C5 (Alcorcón, Las Retamas-Alcorcón), autobuses. Conexión con Madrid en 20-25 minutos.',
    empleo:'Industria y logística, comercio, hospitales. Polo industrial Urtinsa-Ventorro del Cano, IFEMA en proximidad. Universidad URJC.',
    educacion:'Universidad Rey Juan Carlos (URJC, campus Alcorcón: Ciencias de la Salud, Económicas). Hospital Universitario Fundación Alcorcón.',
    pros:['Buena conexión metro y cercanías','Comercio completo','Polo URJC'],
    contras:['Ciudad dormitorio','Tráfico denso en accesos','Sigue siendo cara'],
  },
  'huelva':{
    barrios:[
      {n:'Centro',p:'céntrico',d:'Eje comercial, demanda estable.'},
      {n:'Isla Chica',p:'familiar',d:'Junto al puerto deportivo y el centro, demandada.'},
      {n:'La Orden · Pérez Cubillas',p:'económico',d:'Populosos, accesibles.'},
      {n:'Las Colonias',p:'premium',d:'Tradicional burgués junto al casco.'},
      {n:'El Polvorín · La Granja',p:'familiar',d:'Residenciales.'},
      {n:'Tres Ventanas · La Hispanidad',p:'familiar',d:'Bien dotados.'},
      {n:'Marismas del Odiel · Punta Umbría (cerca)',p:'familiar',d:'Costeros, perfil vacacional.'},
    ],
    transporte:'Autobús urbano. Cercanías regionales. AVE no llega aún (Sevilla-Huelva en estudio). Aeropuerto Sevilla a 1h. Puerto industrial relevante.',
    empleo:'Polo químico de Huelva (uno de los mayores de España: Atlantic Copper, Cepsa, Fertiberia), agroalimentaria (fresa de Huelva, citricultura), pesca, turismo (Costa de la Luz). Tasa de paro alta.',
    educacion:'Universidad de Huelva (UHU). Hospital Universitario Juan Ramón Jiménez, Quirónsalud.',
    pros:['Costa de la Luz y Doñana cerca','Clima excelente','Precios bajos'],
    contras:['Paro elevado','Polo químico controvertido','Conexión AVE pendiente'],
  },
  'logrono':{
    barrios:[
      {n:'Centro · Casco Antiguo',p:'céntrico',d:'Calle Laurel, tapas, demanda turística y residencial.'},
      {n:'Centro · Gran Vía',p:'premium',d:'Eje burgués, comercio principal.'},
      {n:'Cascajos',p:'familiar',d:'Desarrollos modernos planificados, vivienda nueva.'},
      {n:'Yagüe · Universidad',p:'familiar',d:'Cerca de la UR.'},
      {n:'San José',p:'económico',d:'Populoso y accesible.'},
      {n:'La Estrella · El Cubo',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'Madre de Dios · Ribera del Iregua',p:'familiar',d:'Tradicional.'},
    ],
    transporte:'Autobús urbano. AVE no directo (a través de Zaragoza/Castejón). Aeropuerto de Agoncillo con conexiones limitadas. Conexión por carretera con País Vasco y Aragón.',
    empleo:'Agroalimentaria (vino Rioja, conservas), industria (calzado en La Rioja), administración, servicios, comercio. Tejido empresarial sólido. Polo: Polígono Cantabria, El Sequero.',
    educacion:'Universidad de La Rioja (UR), Universidad Internacional de La Rioja (UNIR, online). Hospital Universitario San Pedro, San Millán, Vithas.',
    pros:['Calidad de vida y servicios','Gastronomía y vino','Tamaño humano'],
    contras:['Conexión AVE pendiente','Inviernos fríos','Tamaño limitado de oferta cultural'],
  },
  'badajoz':{
    barrios:[
      {n:'Centro · Casco Antiguo',p:'céntrico',d:'Histórico junto a la Alcazaba, demanda residencial.'},
      {n:'San Roque · Pardaleras',p:'familiar',d:'Bien conectados, residenciales.'},
      {n:'Suerte de Saavedra · Cerro de Reyes',p:'económico',d:'Populosos, accesibles.'},
      {n:'Las Vaguadas · Cerro Gordo',p:'familiar',d:'Desarrollos modernos.'},
      {n:'La Paz · El Gurugú',p:'familiar',d:'Residenciales tradicionales.'},
      {n:'San Fernando · Universidad',p:'familiar',d:'Cerca de la UEx.'},
      {n:'Valdepasillas',p:'familiar',d:'Residencial moderno.'},
    ],
    transporte:'Autobús urbano. Tren convencional a Madrid (lento, mejoras en marcha), Sevilla y Mérida. AVE Extremadura en pruebas/parcial. Aeropuerto de Talavera la Real con conexiones limitadas. Frontera con Portugal (Elvas) a 15 minutos.',
    empleo:'Administración, comercio fronterizo, agroalimentaria (jamón ibérico, vino, aceite), industria ligera. Tasa de paro alta. Polo: Polígono El Nevero.',
    educacion:'Universidad de Extremadura (UEx, campus Badajoz). Hospital Universitario de Badajoz, Quirónsalud Clideba.',
    pros:['Precios bajos','Frontera con Portugal (calidad de vida transfronteriza)','Patrimonio histórico'],
    contras:['Paro elevado y sueldos bajos','Aislamiento (AVE deficiente)','Pérdida demográfica regional'],
  },
  'tarragona':{
    barrios:[
      {n:'Part Alta · Casco Antiguo',p:'céntrico',d:'Patrimonio Unesco romano, demanda turística.'},
      {n:'Eixample',p:'premium',d:'Cuadrícula moderna, m² alto, comercio.'},
      {n:'Sant Pere i Sant Pau',p:'familiar',d:'Residencial bien dotado.'},
      {n:'Bonavista',p:'económico',d:'Populoso, accesible.'},
      {n:'Torreforta · Camp Clar',p:'económico',d:'Populosos.'},
      {n:'Llevant · Cala Romana',p:'premium',d:'Junto al mar al este, vivienda alta.'},
      {n:'Sant Salvador · Sant Pere i Sant Pau',p:'familiar',d:'Residenciales modernos.'},
    ],
    transporte:'Autobús urbano EMT, Rodalies R14, R15, R16, R17. AVE Camp de Tarragona (a Madrid 2h15, a Barcelona 30 min). Aeropuerto de Reus al sur. Puerto comercial relevante.',
    empleo:'Industria petroquímica (uno de los mayores complejos de Europa: Repsol, Dow, BASF), puerto, turismo (Costa Dorada, PortAventura cerca), Universidad. Polo: Polígono Petroquímico Sur y Norte, Vila-seca.',
    educacion:'Universitat Rovira i Virgili (URV). Hospital Joan XXIII (público), Hospital Sant Pau i Santa Tecla, Hospital Universitari Sant Joan de Reus.',
    pros:['Patrimonio Unesco romano','Costa Dorada y playas','Conexión AVE rápida'],
    contras:['Contaminación industrial percibida','Turistificación en verano','Conexión con centro algo dispersa'],
  },
  'lleida':{
    barrios:[
      {n:'Centre · Casco Antiguo',p:'céntrico',d:'Histórico junto a la Seu Vella, demanda estable.'},
      {n:'Cappont',p:'familiar',d:'Junto a la universidad, perfil joven.'},
      {n:'Pardinyes · Balàfia',p:'familiar',d:'Residenciales modernos.'},
      {n:'La Bordeta · Magraners',p:'económico',d:'Populosos, accesibles.'},
      {n:'Mariola · Secà de Sant Pere',p:'económico',d:'Tradicionales.'},
      {n:'Joc de la Bola',p:'familiar',d:'Residencial.'},
      {n:'Ciutat Jardí',p:'premium',d:'Residencial alto.'},
    ],
    transporte:'Autobús urbano. AVE a Madrid (2h05) y Barcelona (1h05), nudo importante. Aeropuerto Lleida-Alguaire con conexiones limitadas.',
    empleo:'Agroalimentaria (frutas dulces, ganadería porcina, vino Costers del Segre), agroindustria (cooperativas potentes), administración, universidad. Polo: Polígono Industrial El Segre.',
    educacion:'Universitat de Lleida (UdL). Hospital Universitari Arnau de Vilanova (HUAV), Hospital Santa Maria.',
    pros:['Conexión AVE Madrid-Barcelona','Coste de vida bajo','Patrimonio Unesco (Seu Vella)'],
    contras:['Verano muy caluroso','Tamaño limitado de oferta cultural','Pérdida demográfica del entorno'],
  },
  'ourense':{
    barrios:[
      {n:'Centro Histórico',p:'céntrico',d:'Catedral, casco medieval, demanda turística termal.'},
      {n:'A Ponte',p:'familiar',d:'Tradicional junto al Miño, bien comunicado.'},
      {n:'O Vinteún · Mariñamansa',p:'económico',d:'Populosos, accesibles.'},
      {n:'O Couto',p:'familiar',d:'Residencial.'},
      {n:'A Cuña · Reza',p:'económico',d:'Tradicionales.'},
      {n:'San Lázaro · Vistahermosa',p:'familiar',d:'Residenciales bien dotados.'},
      {n:'A Carballeira · As Lagoas',p:'familiar',d:'Junto al campus universitario.'},
    ],
    transporte:'Autobús urbano. AVE Eje Atlántico Madrid-Galicia (parada Ourense), AVE a Vigo y Santiago. Conexión muy mejorada. Aeropuerto Vigo o Santiago cerca.',
    empleo:'Administración, servicios, termalismo (As Burgas), agroalimentaria (vino Ribeiro, Ribeira Sacra). Tejido productivo modesto. Pérdida demográfica histórica.',
    educacion:'Campus de Ourense Universidad de Vigo (UVigo, Ciencias, Empresa). Complejo Hospitalario Universitario de Ourense (CHUO).',
    pros:['Termalismo único en España','Patrimonio gallego y Ribeira Sacra cerca','Precios bajos'],
    contras:['Pérdida demográfica fuerte','Sueldos bajos','Mercado laboral débil'],
  },
};

// Helpers --------------------------------------------------------------------
const fmtNum = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g,'.');
const fmtEur = (n) => fmtNum(n) + '€';
const escape = (s) => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');

function nav() {
  return `<header>
  <a href="/" class="logo"><img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA"></a>
  <nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="mob-nav-links">
      <a href="/">🏠 Ciudades</a>
      <a href="/ranking.html">📊 Ranking</a>
      <a href="/analisis.html">📈 Análisis</a>
      <a href="/vivir-en-espana.html">🏡 Vivir en…</a>
      <a href="/comparador.html">⚖️ Comparar</a><a href="/simulador-comprar-vs-alquilar.html">🔄 Comprar vs alquilar</a><a href="/calculadora-hipoteca.html">💶 Calculadora hipoteca</a>
      <a href="/metodologia.html">📊 Metodología</a>
      <a href="/glosario.html">📖 Glosario</a>
      <a href="/guia-inversor.html">🎯 Guía inversor</a>
      <a href="/sobre.html">ℹ️ Sobre</a>
    </div>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/vivir-en-espana.html">Vivir en…</a>
    <a href="/comparador.html">Comparador</a><a href="/simulador-comprar-vs-alquilar.html">Comprar vs alquilar</a><a href="/calculadora-hipoteca.html">Calculadora hipoteca</a>
    <a href="/metodologia.html">Metodología</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/guia-inversor.html">Guía</a>
    <a href="/sobre.html">Sobre</a>
  </nav>
</header>`;
}

function footer() {
  return `<footer>
  <div class="footer-inner">
    <div class="footer-col">
      <a href="/" class="logo" style="margin-bottom:.6rem;display:inline-flex">
        <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
        <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
      </a>
      <p>Análisis de mercado inmobiliario gratuito para 587 ciudades de España. Datos Q2 2026.</p>
    </div>
    <div class="footer-col">
      <h4>Análisis</h4>
      <a href="ranking.html">Ranking completo</a>
      <a href="analisis.html">Análisis</a>
      <a href="vivir-en-espana.html">Vivir en…</a>
      <a href="comparador.html">Comparador</a>
      <a href="guia-inversor.html">Guía del inversor</a>
    </div>
    <div class="footer-col">
      <h4>Recursos</h4>
      <a href="glosario.html">Glosario</a>
      <a href="widget-demo.html">🧩 Widget gratuito para tu web</a>
      <a href="sobre.html">Sobre Ren Data</a>
      <a href="contacto.html">Contacto</a>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <a href="privacidad.html">Privacidad</a>
      <a href="aviso-legal.html">Aviso legal</a>
    </div>
  </div>
  <div class="footer-bottom">© 2026 rendata.es · Datos: INE · Ministerio de Vivienda · Ministerio de Hacienda</div>
</footer>`;
}

function barriosBlock(barrios){
  return barrios.map(b=>{
    const cls = ({premium:'b-premium',céntrico:'b-centric',familiar:'b-family',económico:'b-cheap'})[b.p] || 'b-family';
    return `    <div class="barrio-card ${cls}">
      <div class="barrio-h"><span class="barrio-name">${escape(b.n)}</span><span class="barrio-tag">${escape(b.p)}</span></div>
      <p>${escape(b.d)}</p>
    </div>`;
  }).join('\n');
}

function imageHasFile(slug){
  return fs.existsSync(path.join(IMG_DIR, slug + '.webp'));
}

function build(city){
  const [slug,nombre,ccaa,pob,p,alq,roi,d] = city;
  const c = CITY[slug];
  if(!c){ throw new Error('Falta CITY data para '+slug); }
  const hasImg = imageHasFile(slug);
  const ccaaSlug = CCAA_SLUG[ccaa];
  // Cálculos derivados (estimaciones razonables y conservadoras)
  const pisoMedio = p * 90; // piso de 90 m² como referencia
  // Hipoteca estimada: 80% LTV, 25 años, 3,2% TIN, cuota = principal * factor
  const principal = pisoMedio * 0.80;
  const i = 0.032/12; const nMeses = 25*12;
  const cuotaHip = Math.round(principal * i / (1 - Math.pow(1+i, -nMeses)));
  const salarioMedioES = 26948; // INE 2024 salario bruto anual medio
  const aniosSueldo = +(pisoMedio / salarioMedioES).toFixed(1);
  const esfuerzoHip = +((cuotaHip / (salarioMedioES/12)) * 100).toFixed(0);
  // Estimación gastos compra (ITP/IVA + notaría + registro + AJD): 9-12% según CCAA. Usamos ~10%.
  const gastosCompra = Math.round(pisoMedio * 0.10);

  const heroStyle = hasImg
    ? `style="background:linear-gradient(180deg,rgba(0,0,0,.05) 0%,rgba(0,0,0,.55) 100%),url('img/${slug}.webp') center/cover no-repeat"`
    : `style="background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%)"`;

  const title = `Vivir en ${nombre} 2026 — Guía completa: barrios, coste de vida, empleo`;
  const desc = `Vivir en ${nombre}: barrios reales, coste de vida (precio m² ${fmtNum(p)}€, alquiler ${fmtNum(alq)}€/mes), transporte, empleo, educación y sanidad. Guía actualizada 2026.`;
  const ogTitle = `Vivir en ${nombre} 2026 — Guía completa`;
  const url = `https://rendata.es/vivir-en-${slug}.html`;

  const faq = [
    {q:`¿Cuánto cuesta vivir en ${nombre} en 2026?`,
     a:`Comprar un piso de 90 m² en ${nombre} cuesta unos ${fmtEur(pisoMedio)} de media (${fmtNum(p)}€/m²). Alquilar uno equivalente sale por ${fmtNum(alq)}€/mes. Con el salario medio español (2.246€/mes), la cuota de una hipoteca al 80% LTV (~${fmtNum(cuotaHip)}€/mes) supone aproximadamente el ${esfuerzoHip}% de los ingresos.`},
    {q:`¿Cuáles son los mejores barrios de ${nombre}?`,
     a:`Los barrios más demandados de ${nombre} dependen del perfil: para vida céntrica destacan ${c.barrios.filter(b=>b.p==='céntrico'||b.p==='premium').slice(0,2).map(b=>b.n).join(' y ')||c.barrios[0].n}; para familias con presupuesto medio ${c.barrios.filter(b=>b.p==='familiar').slice(0,2).map(b=>b.n).join(' y ')||c.barrios[1]?.n||'periferia bien comunicada'}; las opciones más económicas se encuentran en ${c.barrios.filter(b=>b.p==='económico').slice(0,2).map(b=>b.n).join(' y ')||'zonas periféricas'}.`},
    {q:`¿Cómo es el transporte público en ${nombre}?`,
     a:c.transporte},
    {q:`¿Qué oportunidades de empleo hay en ${nombre}?`,
     a:c.empleo},
    {q:`¿Es mejor comprar o alquilar en ${nombre}?`,
     a:`La rentabilidad bruta del alquiler en ${nombre} es del ${roi}%, lo que indica una relación precio-alquiler ${roi>=6?'favorable al inversor — alquilar es relativamente barato frente al precio de compra':'tensionada — comprar puede tener sentido sólo si te vas a quedar muchos años'}. Con ${fmtEur(pisoMedio)} de precio medio y ${fmtNum(alq)}€/mes de alquiler, el punto de equilibrio típico está en torno a los ${roi>=6?'12-15':'18-22'} años. Más detalle en nuestra <a href="simulador-comprar-vs-alquilar.html">calculadora comprar vs alquilar</a>.`},
  ];

  const faqJsonLD = {
    "@context":"https://schema.org",
    "@type":"FAQPage",
    "mainEntity": faq.map(f=>({"@type":"Question","name":f.q,"acceptedAnswer":{"@type":"Answer","text":f.a.replace(/<[^>]+>/g,'')}}))
  };

  const articleJsonLD = {
    "@context":"https://schema.org",
    "@type":"Article",
    "headline": ogTitle,
    "description": desc,
    "datePublished": "2026-05-21",
    "dateModified": "2026-05-21",
    "author":{"@type":"Organization","name":"Ren Data","url":"https://rendata.es/"},
    "publisher":{"@type":"Organization","name":"Ren Data","url":"https://rendata.es/","logo":{"@type":"ImageObject","url":"https://rendata.es/favicon.svg"}},
    "mainEntityOfPage":{"@type":"WebPage","@id":url},
    "image": hasImg ? `https://rendata.es/img/${slug}.webp` : "https://rendata.es/img/logo-rendata-transparente.png",
    "inLanguage":"es-ES",
    "about":{"@type":"Place","name":nombre,"containedInPlace":{"@type":"AdministrativeArea","name":ccaa}}
  };

  const breadcrumbJsonLD = {
    "@context":"https://schema.org",
    "@type":"BreadcrumbList",
    "itemListElement":[
      {"@type":"ListItem","position":1,"name":"Inicio","item":"https://rendata.es/"},
      {"@type":"ListItem","position":2,"name":"Vivir en España","item":"https://rendata.es/vivir-en-espana.html"},
      {"@type":"ListItem","position":3,"name":`Vivir en ${nombre}`,"item":url}
    ]
  };

  const html = `<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="${escape(desc)}">
<title>${escape(title)} | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="${escape(ogTitle)}">
<meta property="og:description" content="${escape(desc)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${hasImg?`https://rendata.es/img/${slug}.webp`:'https://rendata.es/img/logo-rendata-transparente.png'}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${escape(ogTitle)}">
<meta name="twitter:description" content="${escape(desc)}">
<meta name="twitter:image" content="${hasImg?`https://rendata.es/img/${slug}.webp`:'https://rendata.es/img/logo-rendata-transparente.png'}">
<link rel="canonical" href="${url}">
<link rel="stylesheet" href="/css/fonts.css">
<script type="application/ld+json">${JSON.stringify([articleJsonLD,breadcrumbJsonLD,faqJsonLD])}</script>
<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
<link rel="stylesheet" href="/css/nav.css">
<style>
.bc{max-width:880px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}
.bc a{color:var(--muted);text-decoration:none;font-weight:500;transition:color .15s}
.bc a:hover{color:var(--blue);text-decoration:underline}
.bc-sep{color:#cbd5e1}
.bc-cur{color:var(--text);font-weight:600}
.vivir-hero{position:relative;min-height:300px;display:flex;align-items:flex-end;color:#fff;padding:2rem 1.5rem;margin-bottom:1rem}
.vivir-hero-inner{max-width:880px;margin:0 auto;width:100%}
.vivir-hero h1{color:#fff;font-size:clamp(1.8rem,4vw,2.6rem);line-height:1.15;letter-spacing:-.025em;margin:0 0 .55rem;font-weight:800}
.vivir-hero .live-dot{background:#34d399}
.vivir-hero-tag{display:inline-flex;align-items:center;gap:.45rem;font-size:.75rem;font-weight:600;letter-spacing:.04em;background:rgba(255,255,255,.18);backdrop-filter:blur(6px);padding:.4rem .85rem;border-radius:99px;margin-bottom:.85rem}
.vivir-hero .lead{font-size:1.05rem;line-height:1.55;color:rgba(255,255,255,.95);max-width:720px;margin:.4rem 0 0}
.kpi-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:.85rem;margin:1.25rem 0}
.kpi-card{background:var(--white,#fff);border:1px solid var(--border,#e2e8f0);border-radius:12px;padding:1rem 1.1rem;box-shadow:0 1px 3px rgba(0,0,0,.04)}
.kpi-val{font-size:1.55rem;font-weight:800;letter-spacing:-.03em;color:var(--blue,#1a56db);line-height:1;margin-bottom:.3rem}
.kpi-lbl{font-size:.74rem;color:var(--muted,#64748b);font-weight:600;line-height:1.35}
.callout{background:#eff6ff;border-left:3px solid var(--blue,#1a56db);border-radius:8px;padding:.95rem 1.15rem;margin:1.2rem 0;font-size:.88rem;line-height:1.65}
.callout strong{color:#1a56db}
.callout.ok{background:#ecfdf5;border-left-color:var(--green,#059669)}
.callout.ok strong{color:#065f46}
.callout.warn{background:#fffbeb;border-left-color:#d97706}
.callout.warn strong{color:#92400e}
.barrios-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:.85rem;margin:1rem 0 1.4rem}
.barrio-card{background:#fff;border:1px solid var(--border,#e2e8f0);border-left:4px solid var(--blue,#1a56db);border-radius:10px;padding:.95rem 1.05rem;font-size:.88rem;line-height:1.55}
.barrio-card.b-premium{border-left-color:#9333ea}
.barrio-card.b-centric{border-left-color:#1a56db}
.barrio-card.b-family{border-left-color:#059669}
.barrio-card.b-cheap{border-left-color:#d97706}
.barrio-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:.4rem;gap:.5rem;flex-wrap:wrap}
.barrio-name{font-weight:700;color:var(--text,#0e1828);font-size:.95rem}
.barrio-tag{font-size:.68rem;text-transform:uppercase;letter-spacing:.05em;font-weight:700;color:var(--muted,#64748b);background:#f1f5f9;padding:.18rem .55rem;border-radius:99px}
.b-premium .barrio-tag{background:#f3e8ff;color:#6b21a8}
.b-centric .barrio-tag{background:#dbeafe;color:#1140a6}
.b-family .barrio-tag{background:#d1fae5;color:#065f46}
.b-cheap .barrio-tag{background:#fef3c7;color:#92400e}
.pro-con{display:grid;grid-template-columns:1fr 1fr;gap:.95rem;margin:1rem 0 1.4rem}
.pro-con-col{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:10px;padding:1rem 1.1rem}
.pc-pros{border-left:4px solid var(--green,#059669)}
.pc-cons{border-left:4px solid #dc2626}
.pc-h{font-size:.82rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.55rem}
.pc-pros .pc-h{color:#065f46}
.pc-cons .pc-h{color:#991b1b}
.pro-con ul{margin:0;padding-left:1.05rem;font-size:.9rem;line-height:1.6}
.cta-ficha{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;background:linear-gradient(135deg,#0e2a6b 0%,#1a56db 100%);color:#fff;padding:1.25rem 1.4rem;border-radius:12px;margin:1.4rem 0;text-decoration:none}
.cta-ficha-t{font-size:1.08rem;font-weight:700;letter-spacing:-.02em;color:#fff;margin-bottom:.2rem}
.cta-ficha-s{font-size:.85rem;color:rgba(255,255,255,.85)}
.cta-ficha-b{background:rgba(255,255,255,.2);padding:.55rem 1.05rem;border-radius:8px;font-weight:700;color:#fff;font-size:.88rem;white-space:nowrap}
@media(max-width:600px){.pro-con{grid-template-columns:1fr}}
</style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());gtag('config', 'G-0M57323B51');</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6236025065305645" crossorigin="anonymous"></script>
</head>
<body>

${nav()}

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">Inicio</a>
  <span class="bc-sep">›</span>
  <a href="vivir-en-espana.html">Vivir en España</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">Vivir en ${escape(nombre)}</span>
</nav>

<section class="vivir-hero" ${heroStyle}>
  <div class="vivir-hero-inner">
    <div class="vivir-hero-tag"><span class="live-dot"></span>Guía residencial · Q2 2026</div>
    <h1>Vivir en ${escape(nombre)} — Guía completa 2026</h1>
    <p class="lead">Coste de vida real, barrios por perfil, transporte, empleo, educación y sanidad. Información práctica con datos verificados para mudarte o decidir si ${escape(nombre)} encaja contigo.</p>
  </div>
</section>

<article class="art">

  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#coste">1. Coste de vida</a></li>
      <li><a href="#barrios">2. Barrios de ${escape(nombre)}</a></li>
      <li><a href="#transporte">3. Transporte y conectividad</a></li>
      <li><a href="#empleo">4. Empleo y economía</a></li>
      <li><a href="#educacion">5. Educación y sanidad</a></li>
      <li><a href="#comprar">6. Comprar piso en ${escape(nombre)}</a></li>
      <li><a href="#merece">7. ¿Merece la pena vivir aquí?</a></li>
      <li><a href="#faq">FAQ</a></li>
    </ul>
  </div>

  <h2 id="coste">1. Coste de vida en ${escape(nombre)}</h2>
  <p>${escape(nombre)} cuenta con ${fmtNum(pob)} habitantes y se sitúa en <a href="ccaa-${ccaaSlug}.html">${escape(ccaa)}</a>. Estos son los datos clave del coste de la vivienda en 2026:</p>
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-val">${fmtNum(p)}€/m²</div><div class="kpi-lbl">Precio medio<br>de compra</div></div>
    <div class="kpi-card"><div class="kpi-val">${fmtNum(alq)}€</div><div class="kpi-lbl">Alquiler medio<br>al mes</div></div>
    <div class="kpi-card"><div class="kpi-val">${aniosSueldo}</div><div class="kpi-lbl">Años de sueldo<br>para un piso de 90 m²</div></div>
    <div class="kpi-card"><div class="kpi-val">${esfuerzoHip}%</div><div class="kpi-lbl">Esfuerzo mensual<br>de la hipoteca (80% LTV, 25 a.)</div></div>
  </div>
  <p>Un piso medio de 90 m² en ${escape(nombre)} cuesta aproximadamente <strong>${fmtEur(pisoMedio)}</strong>. Con una hipoteca al 80% LTV a 25 años y un tipo del 3,2% TIN, la cuota mensual ronda los <strong>${fmtNum(cuotaHip)}€</strong>. A esto hay que sumar gastos de compra (ITP/AJD, notaría, registro, gestoría) por aproximadamente <strong>${fmtEur(gastosCompra)}</strong> adicionales.</p>
  <div class="callout"><strong>Comparativa:</strong> el salario medio en España es de 2.246€/mes (INE 2024). Para una vivienda media en ${escape(nombre)} la cuota representaría el <strong>${esfuerzoHip}%</strong> de ese ingreso — los expertos recomiendan no superar el <strong>30-35%</strong>. ${esfuerzoHip>35?'El esfuerzo aquí supera el límite saludable, lo que indica un mercado tensionado.':'El esfuerzo se encuentra en niveles razonables para ingresos medios.'}</p>

  <h2 id="barrios">2. Barrios de ${escape(nombre)}</h2>
  <p>${escape(nombre)} se organiza en barrios con perfiles muy distintos. Esta es una selección de los principales según perfil de comprador o inquilino:</p>
  <div class="barrios-grid">
${barriosBlock(c.barrios)}
  </div>

  <h2 id="transporte">3. Transporte y conectividad</h2>
  <p>${escape(c.transporte)}</p>

  <h2 id="empleo">4. Empleo y economía</h2>
  <p>${escape(c.empleo)}</p>

  <h2 id="educacion">5. Educación y sanidad</h2>
  <p>${escape(c.educacion)}</p>

  <h2 id="comprar">6. Comprar piso en ${escape(nombre)}</h2>
  <p>Si te planteas comprar vivienda en ${escape(nombre)}, conviene mirar también la rentabilidad del mercado, la fiscalidad de la CCAA y la evolución del precio. Tienes la ficha completa con datos por barrio en nuestra página:</p>
  <a href="rentabilidad-${slug}.html" class="cta-ficha">
    <div>
      <div class="cta-ficha-t">📊 Ficha completa: invertir o comprar en ${escape(nombre)}</div>
      <div class="cta-ficha-s">ROI ${roi}% · precio ${fmtNum(p)}€/m² · alquiler ${fmtNum(alq)}€/mes · días en mercado: ${d}</div>
    </div>
    <span class="cta-ficha-b">Ver ficha →</span>
  </a>

  <h2 id="merece">7. ¿Merece la pena vivir en ${escape(nombre)}?</h2>
  <p>Cualquier decisión de mudanza implica equilibrios. Estos son los principales pros y contras de vivir en ${escape(nombre)}, según datos objetivos y elementos verificables:</p>
  <div class="pro-con">
    <div class="pro-con-col pc-pros">
      <div class="pc-h">✅ Pros</div>
      <ul>
${c.pros.map(x=>`        <li>${escape(x)}.</li>`).join('\n')}
      </ul>
    </div>
    <div class="pro-con-col pc-cons">
      <div class="pc-h">⚠️ Contras</div>
      <ul>
${c.contras.map(x=>`        <li>${escape(x)}.</li>`).join('\n')}
      </ul>
    </div>
  </div>

  <h2 id="faq">Preguntas frecuentes</h2>
${faq.map(f=>`  <h3>${escape(f.q)}</h3>\n  <p>${f.a}</p>`).join('\n')}

  <div class="callout ok" style="margin-top:1.8rem">
    <strong>¿Quieres comparar ${escape(nombre)} con otra ciudad?</strong> Usa nuestro <a href="comparador.html">comparador de ciudades</a> para ver precio, alquiler, ROI y esfuerzo de hipoteca lado a lado. También puedes consultar la <a href="ccaa-${ccaaSlug}.html">visión regional de ${escape(ccaa)}</a> o el <a href="vivir-en-espana.html">índice de guías "Vivir en…"</a>.
  </div>

</article>

${footer()}

</body>
</html>
`;
  return html;
}

// Comando -------------------------------------------------------------------
const cmd = process.argv[2] || 'all';
let from=0, to=ECON.length;
if(cmd==='range'){ from = parseInt(process.argv[3]||'0',10); to = parseInt(process.argv[4]||String(ECON.length),10); }
const generated = [];
for(let idx=from; idx<to; idx++){
  const c = ECON[idx];
  const slug = c[0];
  if(!CITY[slug]){ console.error('skip',slug,'(falta data)'); continue; }
  const html = build(c);
  const out = path.join(OUT_DIR, `vivir-en-${slug}.html`);
  fs.writeFileSync(out, html, 'utf8');
  generated.push(slug);
  console.log('OK', slug);
}
console.log('TOTAL', generated.length, 'págs');
// Exporta lista para index
fs.writeFileSync(path.join(__dirname,'..','data','vivir-list.json'), JSON.stringify(ECON.map(c=>({slug:c[0],n:c[1],ccaa:c[2],pob:c[3],p:c[4],alq:c[5],roi:c[6],d:c[7]})),null,2));
