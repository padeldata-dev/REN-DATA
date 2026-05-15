"""Genera e inserta editoriales para las 69 ciudades restantes (13 CCAA)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

CITIES = {
    # ===== CANARIAS (12) - ITP 6,5% =====
    "adeje": {
        "name": "Adeje",
        "roi": "5,3%", "precio": "3.200€", "alquiler": "1.400€/mes", "dias": "22",
        "alts": [("rentabilidad-arona.html", "Arona"), ("rentabilidad-granadilla-de-abona.html", "Granadilla de Abona")],
        "paragraphs": [
            "<p>Adeje es uno de los grandes motores turísticos del sur de Tenerife, con la marca <strong>Costa Adeje</strong> consolidada como destino premium del archipiélago: hoteles de 5 estrellas, complejos all-inclusive, golf y la playa de Fañabé como referencia. La economía gira en torno al turismo internacional británico, alemán y peninsular. Precio medio: <strong>3.200€/m²</strong>; <strong>rentabilidad bruta 5,3%</strong>; alquiler medio <strong>1.400€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector hotelero (residencial estable), residentes europeos de larga duración y demanda VUT con tarifas elevadas. Los <strong>22 días</strong> de absorción reflejan mercado tensionado. Zonas: <strong>Costa Adeje (premium turística), Fañabé y Adeje pueblo</strong>. ITP Canarias: <strong>6,5%</strong> (más bajo que la mayoría de CCAA peninsulares). Tesis: VUT registrada en Costa Adeje para tarifas premium o residencial estable a personal hotelero, con apreciación apoyada en marca turística líder en el archipiélago.</p>",
            ["Tenerife sur", "Costa Adeje premium", "Turismo internacional", "VUT premium"],
        ],
    },
    "aguimes": {
        "name": "Agüimes",
        "roi": "5,8%", "precio": "1.900€", "alquiler": "918€/mes", "dias": "22",
        "alts": [("rentabilidad-telde.html", "Telde"), ("rentabilidad-santa-lucia-de-tirajana.html", "Santa Lucía de Tirajana")],
        "paragraphs": [
            "<p>Agüimes es un municipio del sureste de Gran Canaria con un perfil singular: combina un casco antiguo histórico bien conservado con la <strong>Zona Industrial de Arinaga</strong> — uno de los polos económicos más importantes del archipiélago, con presencia de empresas energéticas, petroquímicas, ZEC (Zona Especial Canaria) y la futura plataforma offshore eólica. Cuenta además con playa propia (Arinaga, Vargas para windsurf). Precio medio: <strong>1.900€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del polígono industrial, profesionales con beneficios ZEC y un componente turístico-windsurf en zona costera. Alquiler medio: <strong>918€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Casco antiguo, Cruce de Arinaga y entorno industrial</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso urbano para alquiler residencial a personal industrial — demanda estructural apoyada en empleo industrial-energético + ventajas fiscales ZEC.</p>",
            ["Gran Canaria sureste", "Zona industrial Arinaga", "ZEC", "Windsurf Vargas"],
        ],
    },
    "granadilla-de-abona": {
        "name": "Granadilla de Abona",
        "roi": "6,5%", "precio": "2.200€", "alquiler": "1.060€/mes", "dias": "22",
        "alts": [("rentabilidad-adeje.html", "Adeje"), ("rentabilidad-arona.html", "Arona")],
        "paragraphs": [
            "<p>Granadilla de Abona es un municipio del sur de Tenerife con perfil dual: zona costera turística (<strong>El Médano</strong>, capital del windsurf y kitesurf con campeonatos mundiales) y zona industrial-portuaria con el Polígono Industrial de Granadilla y el aeropuerto Tenerife Sur en su término. Conexión por TF-1 a 15 km de Costa Adeje. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para Tenerife.</p>",
            "<p>El inquilino tipo combina trabajadores aeroportuarios, personal industrial, comunidad surfera-windsurf internacional y residencial local. Alquiler medio: <strong>1.060€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>El Médano (premium surf), San Isidro (residencial) y casco urbano</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso en El Médano para VUT segmentado a comunidad windsurf internacional (alta rotación + tarifas premium) o residencial estable a personal aeroportuario en San Isidro.</p>",
            ["Tenerife sur", "El Médano windsurf", "Aeropuerto TFS", "Yield alto"],
        ],
    },
    "guimar": {
        "name": "Güímar",
        "roi": "5,6%", "precio": "1.800€", "alquiler": "840€/mes", "dias": "23",
        "alts": [("rentabilidad-candelaria.html", "Candelaria"), ("rentabilidad-granadilla-de-abona.html", "Granadilla de Abona")],
        "paragraphs": [
            "<p>Güímar es una ciudad media del sureste de Tenerife, conocida por las <strong>Pirámides de Güímar</strong> (parque etnográfico que estudió Thor Heyerdahl) y por una economía basada en agricultura (plátano, hortícolas), pesca artesanal y servicios comarcales. La conexión por TF-1 la sitúa a 25 minutos de Santa Cruz. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>840€/mes</strong>.</p>",
            "<p>El inquilino tipo es residente local: trabajadores agrícolas, profesionales sanitarios del Hospital del Sur y familias jóvenes. Los <strong>23 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, Puertito de Güímar y El Escobonal</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso urbano para alquiler residencial estable o vivienda en Puertito de Güímar para combinar residencial costero con ocasional VUT. Plaza con entrada moderada para Tenerife y demanda local sostenida.</p>",
            ["Tenerife sureste", "Pirámides", "Agricultura plátano", "Entrada moderada"],
        ],
    },
    "la-oliva": {
        "name": "La Oliva",
        "roi": "5,8%", "precio": "2.400€", "alquiler": "1.155€/mes", "dias": "19",
        "alts": [("rentabilidad-puerto-del-rosario.html", "Puerto del Rosario"), ("rentabilidad-pajara.html", "Pájara")],
        "paragraphs": [
            "<p>La Oliva es el municipio más septentrional de Fuerteventura, con <strong>Corralejo</strong> como referencia turística internacional (puerto de conexión con Lanzarote, Parque Natural de las Dunas de Corralejo, surf y windsurf de nivel mundial). Combina turismo masivo con residentes europeos consolidados. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>1.155€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, comunidad europea (británicos, italianos, alemanes), surferos internacionales y temporada VUT prácticamente continua. Los <strong>19 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Corralejo Centro, Pueblo Pescador y El Cotillo</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso o estudio en Corralejo para VUT estacional intensivo (ocupación alta todo el año por estacionalidad invertida del archipiélago) o residencial a personal hotelero.</p>",
            ["Fuerteventura norte", "Corralejo", "Surf mundial", "VUT intensivo"],
        ],
    },
    "la-orotava": {
        "name": "La Orotava",
        "roi": "6,5%", "precio": "2.000€", "alquiler": "920€/mes", "dias": "22",
        "alts": [("rentabilidad-puerto-de-la-cruz.html", "Puerto de la Cruz"), ("rentabilidad-los-realejos.html", "Los Realejos")],
        "paragraphs": [
            "<p>La Orotava es el corazón histórico del Valle de la Orotava, en el norte de Tenerife, con un casco antiguo declarado <strong>Conjunto Histórico-Artístico</strong> (alfombras del Corpus, casas señoriales, balcones canarios) y referencia patrimonial del archipiélago. La economía combina turismo cultural, agricultura (plátano, vid) y servicios comarcales. Precio medio: <strong>2.000€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para Tenerife norte.</p>",
            "<p>El inquilino tipo combina familias locales, trabajadores agrícolas, comerciantes del casco histórico y un componente turístico cultural. Alquiler medio: <strong>920€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Casco histórico (regulado), La Perdoma y San Antonio</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso urbano para alquiler residencial estable o vivienda con encanto en casco histórico para VUT cultural — apreciación apoyada en marca patrimonial consolidada.</p>",
            ["Tenerife norte", "Conjunto histórico", "Patrimonio canario", "Mixto residencial/VUT"],
        ],
    },
    "los-llanos-de-aridane": {
        "name": "Los Llanos de Aridane",
        "roi": "5,6%", "precio": "1.700€", "alquiler": "793€/mes", "dias": "24",
        "alts": [("rentabilidad-santa-cruz-de-la-palma.html", "Santa Cruz de La Palma"), ("rentabilidad-tazacorte.html", "Tazacorte")],
        "paragraphs": [
            "<p>Los Llanos de Aridane es la segunda ciudad de La Palma y capital comarcal del Valle de Aridane, con un tejido económico apoyado en la agricultura del plátano (referencia productiva del archipiélago), comercio comarcal y un mercado inmobiliario muy condicionado por la <strong>erupción del volcán Cumbre Vieja (2021)</strong>, que arrasó zonas significativas del municipio. Precio medio: <strong>1.700€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>793€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores agrícolas, comerciantes y un componente creciente de familias afectadas por la erupción que mantienen demanda inelástica. Los <strong>24 días</strong> de absorción reflejan mercado pausado pero con dinámica especial post-volcán. Zonas: <strong>Centro, El Paso (vecino) y Argual</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: vivienda urbana fuera de zonas afectadas para alquiler residencial estable, con potencial de apreciación a medio plazo por escasez relativa de oferta tras la erupción.</p>",
            ["La Palma", "Valle de Aridane", "Plátano", "Post-volcán"],
        ],
    },
    "san-bartolome-de-tirajana": {
        "name": "San Bartolomé de Tirajana",
        "roi": "5,4%", "precio": "2.400€", "alquiler": "1.080€/mes", "dias": "22",
        "alts": [("rentabilidad-santa-lucia-de-tirajana.html", "Santa Lucía de Tirajana"), ("rentabilidad-mogan.html", "Mogán")],
        "paragraphs": [
            "<p>San Bartolomé de Tirajana es el municipio turístico por excelencia del sur de Gran Canaria, que aglutina las marcas internacionales de <strong>Maspalomas, Playa del Inglés, San Agustín y las Dunas de Maspalomas</strong> (Reserva Natural). Es el destino más visitado del archipiélago, con presencia masiva de turismo británico, alemán y nórdico. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,4%</strong>; alquiler medio <strong>1.080€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, residentes europeos consolidados y demanda VUT continua. Los <strong>22 días</strong> de absorción confirman demanda firme. Zonas: <strong>Playa del Inglés (turística), Maspalomas y San Fernando (residencial)</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: apartamento en Playa del Inglés para VUT con ocupación estructural (estacionalidad invertida) o residencial a personal hotelero en San Fernando — segmento turístico maduro con marca consolidada.</p>",
            ["Gran Canaria sur", "Maspalomas", "Playa del Inglés", "VUT continuo"],
        ],
    },
    "santa-cruz-de-la-palma": {
        "name": "Santa Cruz de La Palma",
        "roi": "5,8%", "precio": "1.800€", "alquiler": "870€/mes", "dias": "22",
        "alts": [("rentabilidad-los-llanos-de-aridane.html", "Los Llanos de Aridane"), ("rentabilidad-brena-alta.html", "Breña Alta")],
        "paragraphs": [
            "<p>Santa Cruz de La Palma es la capital de La Palma — Reserva de la Biosfera y Reserva Starlight (cielos protegidos del IAC, Roque de los Muchachos) — con un casco histórico singular (balcones, calles empedradas) y un puerto activo que es el principal acceso marítimo a la isla. La economía combina administración, comercio, turismo y un sector astronómico-científico vinculado al observatorio. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>.</p>",
            "<p>El inquilino tipo combina funcionarios, profesionales del puerto, científicos del IAC y residentes locales. Alquiler medio: <strong>870€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Casco histórico (regulado), Mirca y entorno puerto</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en demanda institucional + componente científico, con potencial VUT cultural-astronómico en zonas próximas al casco. Plaza con identidad propia y demanda estructural.</p>",
            ["La Palma capital", "Reserva Starlight", "Puerto", "Demanda científica"],
        ],
    },
    "santa-lucia-de-tirajana": {
        "name": "Santa Lucía de Tirajana",
        "roi": "5,7%", "precio": "2.000€", "alquiler": "950€/mes", "dias": "22",
        "alts": [("rentabilidad-aguimes.html", "Agüimes"), ("rentabilidad-san-bartolome-de-tirajana.html", "San Bartolomé de Tirajana")],
        "paragraphs": [
            "<p>Santa Lucía de Tirajana es uno de los municipios con mayor crecimiento poblacional de Gran Canaria, con <strong>Vecindario</strong> como núcleo urbano principal (capital comercial del sur de la isla). Combina perfil residencial creciente (familias jóvenes), comercio dinámico y proximidad a las zonas turísticas del sur (Maspalomas a 15 minutos). Precio medio: <strong>2.000€/m²</strong>; <strong>rentabilidad bruta 5,7%</strong>; alquiler medio <strong>950€/mes</strong>.</p>",
            "<p>El inquilino tipo combina familias jóvenes, trabajadores del comercio y servicios, y personal hotelero del sur que prefiere vivir en zona residencial. Los <strong>22 días</strong> de absorción confirman demanda fuerte. Zonas: <strong>Vecindario, Sardina del Sur y Doctoral</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: piso de 2-3 dormitorios en Vecindario para alquiler familiar estable con yield decente — combinación interesante de comercio dinámico + spillover demográfico de la zona turística.</p>",
            ["Gran Canaria sureste", "Vecindario", "Crecimiento poblacional", "Comercio comarcal"],
        ],
    },
    "teguise": {
        "name": "Teguise",
        "roi": "5,5%", "precio": "2.600€", "alquiler": "1.190€/mes", "dias": "20",
        "alts": [("rentabilidad-arrecife.html", "Arrecife"), ("rentabilidad-yaiza.html", "Yaiza")],
        "paragraphs": [
            "<p>Teguise es la antigua capital de Lanzarote (hasta 1852) y un municipio singular con dos realidades: el <strong>casco histórico de La Villa de Teguise</strong> — Conjunto Histórico-Artístico, con el famoso mercadillo dominical — y la zona costera de <strong>Costa Teguise</strong> (turismo internacional, golf, playa Las Cucharas para windsurf). Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.190€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, residentes europeos (británicos especialmente) y demanda VUT continua. Los <strong>20 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Costa Teguise (turística), La Villa (cultural-residencial) y Tahíche</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: apartamento en Costa Teguise para VUT con ocupación estable (clima e isla muy demandada) o vivienda con encanto en La Villa para alquiler cultural-VUT diferenciado.</p>",
            ["Lanzarote", "Costa Teguise", "Antigua capital", "Mercadillo dominical"],
        ],
    },
    "yaiza": {
        "name": "Yaiza",
        "roi": "5,7%", "precio": "2.800€", "alquiler": "1.330€/mes", "dias": "19",
        "alts": [("rentabilidad-teguise.html", "Teguise"), ("rentabilidad-tias.html", "Tías")],
        "paragraphs": [
            "<p>Yaiza es el municipio más meridional de Lanzarote, hogar del <strong>Parque Nacional de Timanfaya</strong> (paisajes volcánicos únicos) y de las marcas turísticas <strong>Playa Blanca y Marina Rubicón</strong> (turismo de calidad, conexión por ferry con Fuerteventura). Combina turismo internacional premium, residentes europeos y un sector vitivinícola singular (La Geria, viñedos en ceniza volcánica). Precio medio: <strong>2.800€/m²</strong>; <strong>rentabilidad bruta 5,7%</strong>; alquiler medio <strong>1.330€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, residentes europeos jubilados o teletrabajadores y demanda VUT premium continua. Los <strong>19 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Playa Blanca (premium turística), Marina Rubicón y Yaiza pueblo</strong>. ITP Canarias: <strong>6,5%</strong>. Tesis: apartamento en Playa Blanca para VUT con tarifas premium (ocupación estructural por estacionalidad invertida) o residencial a comunidad europea consolidada.</p>",
            ["Lanzarote sur", "Playa Blanca", "Timanfaya", "VUT premium"],
        ],
    },

    # ===== MURCIA (10) - ITP 8% =====
    "alcantarilla": {
        "name": "Alcantarilla",
        "roi": "6,3%", "precio": "1.100€", "alquiler": "580€/mes", "dias": "22",
        "alts": [("rentabilidad-murcia.html", "Murcia"), ("rentabilidad-molina-de-segura.html", "Molina de Segura")],
        "paragraphs": [
            "<p>Alcantarilla es un municipio del área metropolitana inmediata de Murcia, prácticamente conurbado con la capital (a 7 km del centro), con un perfil residencial y comercial consolidado. Su tejido económico combina industria histórica (alimentación, construcción), comercio y un componente residencial estructural alimentado por el spillover de Murcia. Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,3%</strong>; alquiler medio <strong>580€/mes</strong>.</p>",
            "<p>El inquilino tipo combina familias jóvenes que trabajan en Murcia capital pero buscan alquiler más asequible, trabajadores industriales y profesionales. Los <strong>22 días</strong> de absorción confirman demanda estable. Zonas: <strong>Centro, Cayitas y entorno Hospital</strong>. ITP Murcia: <strong>8%</strong>. Tesis: piso de 2-3 dormitorios para alquiler familiar estable, capturando spillover metropolitano de Murcia con tickets de entrada muy bajos y yield superior a la capital.</p>",
            ["Área metropolitana Murcia", "Conurbado capital", "Spillover", "Yield alto"],
        ],
    },
    "cieza": {
        "name": "Cieza",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "520€/mes", "dias": "22",
        "alts": [("rentabilidad-jumilla.html", "Jumilla"), ("rentabilidad-mula.html", "Mula")],
        "paragraphs": [
            "<p>Cieza es la capital comarcal de la Vega Alta del Segura murciana, conocida internacionalmente por la <strong>floración de los frutales</strong> (melocotón, nectarina) — espectáculo natural que atrae miles de visitantes en marzo — y por una economía agraria sólida basada en frutales de hueso (referencia productiva nacional). Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>520€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores agrícolas (con picos por campañas frutícolas), agroindustria (envasado, congelados) y servicios comarcales. Los <strong>22 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, La Aurora y entorno estación</strong>. ITP Murcia: <strong>8%</strong>. Tesis: ticket muy bajo con yield decente, ideal para inversor rentista que busca cash-flow apoyado en empleo agroindustrial estable y demanda local sostenida. Vivienda completa por menos de 70.000€ es factible.</p>",
            ["Vega Alta del Segura", "Frutales de hueso", "Floración turística", "Cash-flow"],
        ],
    },
    "jumilla": {
        "name": "Jumilla",
        "roi": "6,8%", "precio": "1.000€", "alquiler": "567€/mes", "dias": "27",
        "alts": [("rentabilidad-yecla.html", "Yecla"), ("rentabilidad-cieza.html", "Cieza")],
        "paragraphs": [
            "<p>Jumilla es la capital del Altiplano murciano y referencia vitivinícola con la <strong>DO Jumilla</strong> (Monastrell como variedad insignia, vinos de gran reconocimiento internacional). La economía combina viticultura, agroindustria del aceite, ganadería caprina y un patrimonio histórico potente (Castillo, Iglesia de Santiago). Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong> — de las más altas de la región.</p>",
            "<p>El inquilino tipo es local: trabajadores del sector vinícola, bodegas (Casa Castillo, Juan Gil), agroindustria y servicios. Alquiler medio: <strong>567€/mes</strong>; <strong>27 días</strong> de absorción reflejan ritmo pausado del altiplano. Zonas: <strong>Centro, San Juan y barrio del Castillo</strong>. ITP Murcia: <strong>8%</strong>. Tesis: tickets muy bajos con yield alto, ideal para inversor rentista que busca cash-flow estable apoyado en una economía vitivinícola con marca DO consolidada.</p>",
            ["Altiplano Murcia", "DO Jumilla", "Monastrell", "Yield alto rentista"],
        ],
    },
    "la-union": {
        "name": "La Unión",
        "roi": "7,2%", "precio": "900€", "alquiler": "540€/mes", "dias": "27",
        "alts": [("rentabilidad-cartagena.html", "Cartagena"), ("rentabilidad-fuente-alamo-de-murcia.html", "Fuente Álamo")],
        "paragraphs": [
            "<p>La Unión es un municipio de la comarca de Cartagena con un patrimonio histórico-industrial único: cuna de la <strong>minería del plomo y la plata de la Sierra Minera de Cartagena-La Unión</strong> y sede del <strong>Cante de las Minas</strong> (el festival flamenco más prestigioso del mundo, patrimonio cultural). Tras el cierre de las minas, la ciudad afronta reconversión apoyada en turismo cultural y residencial. Precio medio: <strong>900€/m²</strong> — el más bajo del grupo — y <strong>rentabilidad bruta del 7,2%</strong>, top del grupo.</p>",
            "<p>El inquilino tipo es residente local con poder adquisitivo modesto, trabajadores del entorno industrial cartagenero y un creciente componente de jóvenes que aprovechan el bajo coste. Alquiler medio: <strong>540€/mes</strong>; <strong>27 días</strong> de absorción. Zonas: <strong>Centro, Roche y Portmán (vecino)</strong>. ITP Murcia: <strong>8%</strong>. Tesis: tickets extremadamente bajos con el yield más alto del grupo, plaza para rentista que asume menor liquidez por máximo cash-flow porcentual.</p>",
            ["Sierra Minera", "Cante de las Minas", "Yield máximo", "Reconversión"],
        ],
    },
    "los-alcazares": {
        "name": "Los Alcázares",
        "roi": "6,4%", "precio": "1.700€", "alquiler": "906€/mes", "dias": "22",
        "alts": [("rentabilidad-san-pedro-del-pinatar.html", "San Pedro del Pinatar"), ("rentabilidad-san-javier.html", "San Javier")],
        "paragraphs": [
            "<p>Los Alcázares es uno de los municipios consolidados de la ribera del <strong>Mar Menor</strong> murciano, con un perfil histórico ligado a la presencia militar (la <strong>Academia General del Aire</strong> está en el vecino San Javier) y un turismo familiar de proximidad regional. La crisis ecológica del Mar Menor ha frenado parcialmente el mercado pero hay signos de recuperación. Precio medio: <strong>1.700€/m²</strong>; <strong>rentabilidad bruta 6,4%</strong>; alquiler medio <strong>906€/mes</strong>.</p>",
            "<p>El inquilino tipo combina personal militar, residentes locales y residentes europeos del entorno (especialmente británicos). Los <strong>22 días</strong> de absorción reflejan mercado tensionado. Zonas: <strong>Centro, Las Palmeras y Roda Golf</strong>. ITP Murcia: <strong>8%</strong>. Tesis: piso para alquiler residencial estable a comunidad europea + alquiler de temporada militar, con yield superior al de San Pedro o San Javier vecinos y exposición controlada a la dinámica del Mar Menor.</p>",
            ["Mar Menor", "Cercano AGA", "Comunidad europea", "Yield medio costero"],
        ],
    },
    "molina-de-segura": {
        "name": "Molina de Segura",
        "roi": "5,8%", "precio": "1.400€", "alquiler": "680€/mes", "dias": "22",
        "alts": [("rentabilidad-murcia.html", "Murcia"), ("rentabilidad-alcantarilla.html", "Alcantarilla")],
        "paragraphs": [
            "<p>Molina de Segura es la tercera ciudad por población de la Región de Murcia, integrada en el área metropolitana norte de la capital. Su tejido económico está apoyado en agroindustria potente (Hero, ElPozo cercano), polígonos industriales activos y servicios comarcales. Conexión por A-30 a 10 minutos del centro de Murcia. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>680€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores agroindustriales, profesionales del comercio y familias jóvenes que trabajan en Murcia. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centro, La Quinta y entorno polígono</strong>. ITP Murcia: <strong>8%</strong>. Tesis: piso de 2-3 dormitorios para alquiler familiar estable apoyado en empleo agroindustrial diversificado. Plaza con motor económico propio más allá del spillover metropolitano.</p>",
            ["Área metropolitana Murcia norte", "Agroindustria Hero", "Polígono industrial", "Familiar"],
        ],
    },
    "san-javier": {
        "name": "San Javier",
        "roi": "5,5%", "precio": "1.800€", "alquiler": "820€/mes", "dias": "22",
        "alts": [("rentabilidad-los-alcazares.html", "Los Alcázares"), ("rentabilidad-san-pedro-del-pinatar.html", "San Pedro del Pinatar")],
        "paragraphs": [
            "<p>San Javier es uno de los municipios costeros del Mar Menor murciano, con un perfil singular: alberga la <strong>Academia General del Aire (AGA)</strong> — única en España, donde se forman los oficiales del Ejército del Aire — y el aeropuerto Región de Murcia (Corvera funciona como principal pero AGA mantiene actividad). Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>820€/mes</strong>.</p>",
            "<p>El inquilino tipo es muy específico: oficiales y suboficiales en formación o destinados (con rotación previsible y contratos demandantes), familias militares y residentes locales. Los <strong>22 días</strong> de absorción confirman demanda estructural. Zonas: <strong>Centro, Santiago de la Ribera y entorno AGA</strong>. ITP Murcia: <strong>8%</strong>. Tesis: piso amueblado próximo a AGA para alquiler temporal a personal militar (rotación cada curso académico, demanda inelástica), nicho con yield estable.</p>",
            ["Mar Menor", "Academia General del Aire", "Alquiler militar", "Demanda estructural"],
        ],
    },
    "san-pedro-del-pinatar": {
        "name": "San Pedro del Pinatar",
        "roi": "6,2%", "precio": "1.800€", "alquiler": "930€/mes", "dias": "22",
        "alts": [("rentabilidad-los-alcazares.html", "Los Alcázares"), ("rentabilidad-pilar-de-la-horadada.html", "Pilar de la Horadada")],
        "paragraphs": [
            "<p>San Pedro del Pinatar es el municipio más septentrional del litoral murciano, con un perfil singular: <strong>Salinas y Arenales de San Pedro</strong> (Parque Regional, baños de lodo terapéuticos), puerto pesquero activo (<strong>Lonja del Mar Menor</strong>) y Lo Pagán como zona residencial-turística. La cercanía a la Comunidad Valenciana (Pilar de la Horadada) le da un componente fronterizo. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>930€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector pesquero, residentes europeos (sobre todo británicos), turismo de salud (lodos) y residencial permanente. Los <strong>22 días</strong> de absorción confirman demanda estable. Zonas: <strong>Lo Pagán (residencial-turística), Centro y Las Esperanzas</strong>. ITP Murcia: <strong>8%</strong>. Tesis: piso en Lo Pagán para alquiler residencial a comunidad europea o VUT estacional. Buena combinación coste/yield.</p>",
            ["Mar Menor norte", "Lo Pagán", "Salinas terapéuticas", "Comunidad europea"],
        ],
    },
    "totana": {
        "name": "Totana",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "560€/mes", "dias": "22",
        "alts": [("rentabilidad-lorca.html", "Lorca"), ("rentabilidad-alhama-de-murcia.html", "Alhama de Murcia")],
        "paragraphs": [
            "<p>Totana es una ciudad media del valle del Guadalentín murciano, conocida por la <strong>alfarería tradicional</strong> (referencia artesanal nacional, con conjunto industrial protegido) y por la cercanía al <strong>Parque Regional de Sierra Espuña</strong> (turismo de naturaleza). La economía combina alfarería, agroindustria (envasado, agricultura intensiva) y comercio comarcal. Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>560€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores agrícolas e industriales, artesanos del barro y familias locales. Los <strong>22 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, La Vega y entorno polígono</strong>. ITP Murcia: <strong>8%</strong>. Tesis: ticket bajo con yield decente apoyado en empleo agroindustrial diversificado. Plaza con identidad propia (alfarería, Sierra Espuña) para inversor que busca diversificación geográfica con cash-flow estable.</p>",
            ["Valle del Guadalentín", "Alfarería tradicional", "Sierra Espuña", "Cash-flow"],
        ],
    },
    "yecla": {
        "name": "Yecla",
        "roi": "6,5%", "precio": "950€", "alquiler": "500€/mes", "dias": "22",
        "alts": [("rentabilidad-jumilla.html", "Jumilla"), ("rentabilidad-villena.html", "Villena")],
        "paragraphs": [
            "<p>Yecla es la <strong>capital española del mueble</strong> (concentra una de las mayores agrupaciones empresariales del sector mueble nacional, con feria internacional propia) y referencia vitivinícola con la <strong>DO Yecla</strong> (Monastrell como variedad principal). El tejido empresarial es excepcional para una ciudad de su tamaño. Precio medio: <strong>950€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>500€/mes</strong>.</p>",
            "<p>El inquilino tipo es trabajador industrial del mueble, sector vinícola, agroindustria y servicios. Los <strong>22 días</strong> de absorción confirman demanda estructural apoyada en empleo industrial estable. Zonas: <strong>Centro, San Cristóbal y entorno polígono</strong>. ITP Murcia: <strong>8%</strong>. Tesis: ticket muy bajo (vivienda completa por menos de 65.000€) con yield decente apoyado en empleo industrial diversificado. Plaza con motor económico real más allá de la marca vinícola.</p>",
            ["Altiplano Murcia", "Capital del mueble", "DO Yecla", "Empleo industrial"],
        ],
    },

    # ===== BALEARES (9) - ITP escala 8-13% =====
    "alcudia": {
        "name": "Alcúdia",
        "roi": "5,1%", "precio": "3.800€", "alquiler": "1.615€/mes", "dias": "17",
        "alts": [("rentabilidad-pollenca.html", "Pollença"), ("rentabilidad-can-picafort.html", "Can Picafort")],
        "paragraphs": [
            "<p>Alcúdia es uno de los municipios turísticos consolidados del norte de Mallorca, con la <strong>Bahía de Alcúdia</strong> (10 km de playa, una de las más extensas de las islas), el casco antiguo amurallado romano-medieval y el Puerto de Alcúdia como nodo portuario y turístico. Precio medio: <strong>3.800€/m²</strong>; <strong>rentabilidad bruta 5,1%</strong>; alquiler medio <strong>1.615€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, residentes europeos (alemanes, británicos) y demanda VUT estacional intensiva. Los <strong>17 días</strong> de absorción confirman mercado muy líquido y tensionado. Zonas: <strong>Casco antiguo, Puerto de Alcúdia y Aucanada</strong>. ITP Baleares: <strong>8%</strong> (escala 8-13% según valor). Tesis: VUT registrada en Puerto Alcúdia para tarifas premium estivales (yield combinado muy superior) o vivienda con encanto en casco antiguo para alquiler residencial diferenciado a comunidad europea.</p>",
            ["Mallorca norte", "Bahía Alcúdia", "Casco amurallado", "VUT premium"],
        ],
    },
    "andratx": {
        "name": "Andratx",
        "roi": "4,5%", "precio": "5.000€", "alquiler": "1.875€/mes", "dias": "15",
        "alts": [("rentabilidad-calvia.html", "Calvià"), ("rentabilidad-soller.html", "Sóller")],
        "paragraphs": [
            "<p>Andratx es uno de los municipios premium absolutos del suroeste de Mallorca, con el <strong>Puerto de Andratx</strong> como referencia náutica internacional (yates de lujo, restaurantes de alta cocina) y zonas como Camp de Mar, Sant Elm y Mola que concentran segunda residencia europea ultra-premium. Precio medio: <strong>5.000€/m²</strong> — el más alto del grupo — y <strong>rentabilidad bruta del 4,5%</strong>, baja como corresponde a residencial ultra-premium.</p>",
            "<p>El inquilino tipo es ultra-alto: ejecutivos internacionales, alta dirección europea, deportistas y celebridades. Alquiler medio: <strong>1.875€/mes</strong>; <strong>15 días</strong> de absorción — los más rápidos del grupo, mercado extremadamente líquido. Zonas: <strong>Port d'Andratx, Camp de Mar y Mola</strong>. ITP Baleares: <strong>8-13%</strong> (tramos altos para inmuebles >1M€). Tesis: vivienda de lujo para alquiler patrimonialista, foco absoluto en preservación de capital y revalorización a 5-10 años. Yield secundario.</p>",
            ["Mallorca SW premium", "Port d'Andratx", "Yates", "Ultra-premium"],
        ],
    },
    "calvia": {
        "name": "Calvià",
        "roi": "4,7%", "precio": "4.800€", "alquiler": "1.880€/mes", "dias": "22",
        "alts": [("rentabilidad-andratx.html", "Andratx"), ("rentabilidad-marratxi.html", "Marratxí")],
        "paragraphs": [
            "<p>Calvià es uno de los municipios turísticos por antonomasia de Mallorca, con marcas internacionales en su término: <strong>Magaluf, Palmanova, Santa Ponça, Portals Nous, Bendinat y Costa d'en Blanes</strong>. El perfil económico está totalmente apoyado en turismo internacional (británico mayoritariamente) y residencia premium europea. Precio medio: <strong>4.800€/m²</strong>; <strong>rentabilidad bruta 4,7%</strong>; alquiler medio <strong>1.880€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, residentes europeos premium y demanda VUT muy intensa estacional. Los <strong>22 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Magaluf (turística masiva), Santa Ponça (residencial-turística) y Portals Nous (premium náutico)</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: segmentar por zona — VUT en Magaluf para tarifas estivales alto volumen o residencial premium en Santa Ponça/Portals para apreciación a comunidad europea.</p>",
            ["Mallorca SW", "Magaluf", "Santa Ponça", "Turismo masivo + premium"],
        ],
    },
    "ciutadella-de-menorca": {
        "name": "Ciutadella de Menorca",
        "roi": "5,2%", "precio": "3.600€", "alquiler": "1.560€/mes", "dias": "18",
        "alts": [("rentabilidad-mao.html", "Maó"), ("rentabilidad-alaior.html", "Alaior")],
        "paragraphs": [
            "<p>Ciutadella de Menorca es la antigua capital de la isla, con un casco histórico medieval excepcional, las celebradas Festas de Sant Joan (UNESCO inmaterial Patrimonio Cultural) y un entorno natural protegido (Reserva de la Biosfera). La economía combina turismo de calidad, comercio comarcal y un componente residencial premium europeo. Precio medio: <strong>3.600€/m²</strong>; <strong>rentabilidad bruta 5,2%</strong>; alquiler medio <strong>1.560€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros, residentes europeos (italianos, británicos, alemanes) y demanda VUT estacional intensiva. Los <strong>18 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Casco histórico (regulado), Cala en Forcat y Son Xoriguer</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: VUT registrada en zonas próximas al casco para tarifas premium o vivienda con encanto en casco histórico para residencial a comunidad europea consolidada — Menorca tiene marca internacional creciente.</p>",
            ["Menorca", "Casco medieval", "Sant Joan UNESCO", "VUT premium"],
        ],
    },
    "felanitx": {
        "name": "Felanitx",
        "roi": "5,5%", "precio": "2.800€", "alquiler": "1.283€/mes", "dias": "19",
        "alts": [("rentabilidad-manacor.html", "Manacor"), ("rentabilidad-llucmajor.html", "Llucmajor")],
        "paragraphs": [
            "<p>Felanitx es un municipio del este de Mallorca con un perfil singular: combina pueblo interior agrícola tradicional (vino DO Pla i Llevant, almendro) con la zona costera de <strong>Portocolom</strong> (puerto pesquero pintoresco) y la cala de <strong>Cala d'Or</strong> (parcialmente en su término), referente turístico de calidad. Precio medio: <strong>2.800€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.283€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes locales agrícolas, comunidad europea (sobre todo alemana) en zonas costeras y demanda VUT estacional. Los <strong>19 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Portocolom (residencial-costero), Cala d'Or y Felanitx pueblo</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: vivienda en Portocolom para alquiler residencial a comunidad alemana o VUT estacional, capturando combinación de marca premium (Cala d'Or) + pueblo auténtico.</p>",
            ["Mallorca este", "Portocolom", "Cala d'Or", "Comunidad alemana"],
        ],
    },
    "llucmajor": {
        "name": "Llucmajor",
        "roi": "6,5%", "precio": "3.600€", "alquiler": "1.560€/mes", "dias": "22",
        "alts": [("rentabilidad-palma.html", "Palma"), ("rentabilidad-marratxi.html", "Marratxí")],
        "paragraphs": [
            "<p>Llucmajor es uno de los municipios de mayor extensión territorial de Mallorca, con un perfil dual: pueblo interior tradicional (calzado, agricultura) y la pujante zona costera de <strong>S'Arenal</strong> (turismo masivo de proximidad a Palma) más urbanizaciones residenciales como Cala Pi y Bahía Azul. Precio medio: <strong>3.600€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para Baleares.</p>",
            "<p>El inquilino tipo combina trabajadores del sector turístico, residentes europeos en urbanizaciones costeras y un componente residencial creciente apoyado en spillover de Palma. Alquiler medio: <strong>1.560€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>S'Arenal (turística), Llucmajor pueblo y Cala Pi</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: VUT registrada en S'Arenal para tarifas estivales o residencial estable en pueblo. Plaza con buena combinación yield/marca turística.</p>",
            ["Mallorca sur", "S'Arenal", "Cala Pi", "Yield alto Baleares"],
        ],
    },
    "marratxi": {
        "name": "Marratxí",
        "roi": "6,5%", "precio": "3.200€", "alquiler": "1.490€/mes", "dias": "22",
        "alts": [("rentabilidad-palma.html", "Palma"), ("rentabilidad-bunyola.html", "Bunyola")],
        "paragraphs": [
            "<p>Marratxí es uno de los municipios estrella del área metropolitana de Palma, conurbado con la capital y con un perfil residencial-comercial premium consolidado. La conexión por Metro de Palma (estaciones Pont d'Inca, Marratxí, Es Caülls) y la presencia del centro comercial Festival Park lo convierten en plaza muy demandada. Precio medio: <strong>3.200€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación premium con yield notable.</p>",
            "<p>El inquilino tipo es familia profesional que trabaja en Palma y prefiere vivienda más amplia con jardín o piscina comunitaria. Alquiler medio: <strong>1.490€/mes</strong>; <strong>22 días</strong> de absorción confirman demanda firme. Zonas: <strong>Pont d'Inca, Sa Cabaneta y Es Garrovers</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: piso o adosado de 3 dormitorios próximo al Metro para alquiler familiar largo plazo, capturando spillover residencial de Palma con yield alto para Baleares premium.</p>",
            ["Área metropolitana Palma", "Metro Palma", "Festival Park", "Familiar premium"],
        ],
    },
    "pollenca": {
        "name": "Pollença",
        "roi": "4,9%", "precio": "4.200€", "alquiler": "1.715€/mes", "dias": "16",
        "alts": [("rentabilidad-alcudia.html", "Alcúdia"), ("rentabilidad-soller.html", "Sóller")],
        "paragraphs": [
            "<p>Pollença es uno de los municipios premium del norte de Mallorca, con tres núcleos diferenciados: pueblo interior con casco histórico cuidado (Calvario), <strong>Port de Pollença</strong> (residencial-turístico premium con marca británica histórica) y Cala Sant Vicenç. La Sierra de Tramuntana (Patrimonio Mundial UNESCO) configura el entorno. Precio medio: <strong>4.200€/m²</strong>; <strong>rentabilidad bruta 4,9%</strong>; alquiler medio <strong>1.715€/mes</strong>.</p>",
            "<p>El inquilino tipo es residente europeo premium (británicos sobre todo, también alemanes, escandinavos), familias internacionales y demanda VUT premium. Los <strong>16 días</strong> de absorción confirman mercado muy líquido y tensionado. Zonas: <strong>Port de Pollença (premium), Cala Sant Vicenç y Pollença pueblo</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: vivienda en Port de Pollença para alquiler patrimonialista a comunidad británica + VUT premium estival — marca consolidada y demanda inelástica.</p>",
            ["Mallorca norte", "Tramuntana UNESCO", "Port de Pollença", "Marca británica"],
        ],
    },
    "soller": {
        "name": "Sóller",
        "roi": "4,8%", "precio": "4.500€", "alquiler": "1.800€/mes", "dias": "16",
        "alts": [("rentabilidad-pollenca.html", "Pollença"), ("rentabilidad-deia.html", "Deià")],
        "paragraphs": [
            "<p>Sóller es una de las plazas más singulares de Mallorca, en pleno corazón de la <strong>Serra de Tramuntana (Patrimonio Mundial UNESCO)</strong>, con un casco modernista único, el Puerto de Sóller y conexión por el icónico tren de madera Palma-Sóller. La economía combina turismo cultural-natural premium, agricultura tradicional (naranja, olivo) y residentes europeos. Precio medio: <strong>4.500€/m²</strong>; <strong>rentabilidad bruta 4,8%</strong>; alquiler medio <strong>1.800€/mes</strong>.</p>",
            "<p>El inquilino tipo es residente europeo cultural-premium (alemanes, británicos, holandeses), comunidad artística y demanda VUT cultural-natural. Los <strong>16 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Sóller pueblo, Port de Sóller y Biniaraix</strong>. ITP Baleares: <strong>8-13%</strong>. Tesis: vivienda con encanto en Sóller pueblo o Puerto para alquiler residencial cultural-premium o VUT diferenciado de turismo masivo. Marca Tramuntana UNESCO sostiene la apreciación.</p>",
            ["Serra Tramuntana UNESCO", "Tren histórico", "Modernista", "VUT cultural"],
        ],
    },

    # ===== PAÍS VASCO (9) - ITP 4% (de los más bajos!) =====
    "basauri": {
        "name": "Basauri",
        "roi": "5,3%", "precio": "2.200€", "alquiler": "980€/mes", "dias": "22",
        "alts": [("rentabilidad-bilbao.html", "Bilbao"), ("rentabilidad-galdakao.html", "Galdakao")],
        "paragraphs": [
            "<p>Basauri es uno de los municipios consolidados del área metropolitana de Bilbao, integrado en la conurbación del Gran Bilbao, con un perfil industrial histórico (Sefanitro, Cromados Salgui) en transformación hacia residencial-servicios. Conexión por Metro Bilbao Línea 2 (estaciones Basauri, Etxebarri) y Cercanías. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,3%</strong>; alquiler medio <strong>980€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores industriales en transición, jóvenes profesionales que trabajan en Bilbao pero buscan alquiler más asequible y familias jóvenes. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centro, San Miguel y entorno Metro</strong>. ITP País Vasco: <strong>4%</strong> (de los más bajos de España, ventaja competitiva). Tesis: piso de 2 dormitorios próximo al Metro para alquiler residencial a jóvenes profesionales, capturando spillover bilbaíno con yield aceptable y ventaja fiscal por ITP bajo.</p>",
            ["Gran Bilbao", "Metro L2", "Industrial en transición", "ITP 4%"],
        ],
    },
    "bermeo": {
        "name": "Bermeo",
        "roi": "5,5%", "precio": "2.600€", "alquiler": "1.190€/mes", "dias": "22",
        "alts": [("rentabilidad-mundaka.html", "Mundaka"), ("rentabilidad-gernika-lumo.html", "Gernika-Lumo")],
        "paragraphs": [
            "<p>Bermeo es uno de los puertos pesqueros más importantes del Cantábrico, con tradición ballenera histórica y referencia gastronómica del bonito y la anchoa. La <strong>Reserva de la Biosfera de Urdaibai</strong> y la cercanía a Mundaka (icónica ola surfera mundial) configuran un entorno natural protegido excepcional. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>1.190€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector pesquero y conservero, residentes locales y un nicho de surferos internacionales atraídos por Mundaka. Los <strong>22 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centro, Puerto Viejo y entorno paseo</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: piso urbano para alquiler residencial estable a personal pesquero/conservero o vivienda con encanto en Puerto Viejo para VUT cultural-gastronómico. ITP bajo aporta ventaja fiscal sobre Cantabria/Galicia vecinas.</p>",
            ["Costa Vizcaya", "Puerto pesquero", "Urdaibai UNESCO", "Mundaka surf"],
        ],
    },
    "durango": {
        "name": "Durango",
        "roi": "6,5%", "precio": "2.400€", "alquiler": "1.080€/mes", "dias": "22",
        "alts": [("rentabilidad-eibar.html", "Eibar"), ("rentabilidad-bilbao.html", "Bilbao")],
        "paragraphs": [
            "<p>Durango es la capital de la Merindad de Durango (Vizcaya interior), un nodo industrial histórico (máquina-herramienta, automoción, sede de Astra) integrado en el eje industrial Bilbao-San Sebastián. Conexión por A-8 y Cercanías. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable para País Vasco.</p>",
            "<p>El inquilino tipo es trabajador industrial cualificado (máquina-herramienta, automoción), profesionales del comercio y familias jóvenes. Alquiler medio: <strong>1.080€/mes</strong>; <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centro, Tabira y Landako</strong>. ITP País Vasco: <strong>4%</strong> (ventaja fiscal significativa). Tesis: piso de 2-3 dormitorios para alquiler familiar estable apoyado en empleo industrial estructural. Combinación interesante de yield superior a Bilbao + ITP bajo.</p>",
            ["Vizcaya interior", "Máquina-herramienta", "Eje industrial", "Yield alto vasco"],
        ],
    },
    "eibar": {
        "name": "Eibar",
        "roi": "5,5%", "precio": "1.800€", "alquiler": "820€/mes", "dias": "22",
        "alts": [("rentabilidad-durango.html", "Durango"), ("rentabilidad-mondragon.html", "Mondragón")],
        "paragraphs": [
            "<p>Eibar es una de las ciudades industriales históricas más singulares de España, cuna de la <strong>industria armera nacional</strong> en los siglos XIX-XX, hoy reconvertida en industria de máquina-herramienta, automoción y sede de marcas como CAF (componentes ferroviarios). El Eibar SD da nombre internacional al municipio. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,5%</strong>; alquiler medio <strong>820€/mes</strong>.</p>",
            "<p>El inquilino tipo es trabajador industrial cualificado, profesionales y familias locales. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centro, Urki y Amaña</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo industrial diversificado. Plaza con tickets más accesibles que Durango o Mondragón vecinas y mantenimiento del ITP bajo vasco como ventaja fiscal estructural.</p>",
            ["Guipúzcoa", "Industria armera histórica", "Máquina-herramienta", "Tickets accesibles"],
        ],
    },
    "gernika-lumo": {
        "name": "Gernika-Lumo",
        "roi": "5,4%", "precio": "2.400€", "alquiler": "1.080€/mes", "dias": "22",
        "alts": [("rentabilidad-bermeo.html", "Bermeo"), ("rentabilidad-durango.html", "Durango")],
        "paragraphs": [
            "<p>Gernika-Lumo es una de las ciudades más simbólicas del País Vasco: sede de la <strong>Casa de Juntas</strong> (origen del Estatuto Vasco, Árbol de Gernika), escenario del bombardeo de 1937 inmortalizado por Picasso, y referencia cultural-histórica de primer nivel. Cabecera comarcal de Busturialdea-Urdaibai (Reserva de la Biosfera). Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,4%</strong>; alquiler medio <strong>1.080€/mes</strong>.</p>",
            "<p>El inquilino tipo combina funcionarios, profesionales del comercio comarcal, trabajadores agroalimentarios y residentes locales. Los <strong>22 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, Iparralde y entorno Casa de Juntas</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: piso urbano para alquiler residencial estable, con potencial complementario de turismo cultural-político (visitas Casa de Juntas, museo de la paz). Plaza con identidad cultural única.</p>",
            ["Vizcaya", "Casa de Juntas", "Urdaibai UNESCO", "Cabecera comarcal"],
        ],
    },
    "hondarribia": {
        "name": "Hondarribia",
        "roi": "5,2%", "precio": "3.400€", "alquiler": "1.473€/mes", "dias": "20",
        "alts": [("rentabilidad-irun.html", "Irún"), ("rentabilidad-zarautz.html", "Zarautz")],
        "paragraphs": [
            "<p>Hondarribia es una de las plazas más premium de Guipúzcoa: villa amurallada medieval junto a la frontera francesa (Bahía de Txingudi), con casco histórico cuidado, marina (Puerto), playa y referencia gastronómica internacional (varios restaurantes Michelin). La cercanía a Hendaya y el aeropuerto de San Sebastián configuran una plaza singular. Precio medio: <strong>3.400€/m²</strong>; <strong>rentabilidad bruta 5,2%</strong>; alquiler medio <strong>1.473€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes premium locales (industriales, profesionales liberales), residentes franceses y demanda VUT gastronómico-cultural. Los <strong>20 días</strong> de absorción confirman mercado muy líquido. Zonas: <strong>Casco histórico (regulado), Marina y entorno playa</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: vivienda con encanto en casco histórico para VUT cultural-gastronómico premium o residencial a comunidad francesa. Marca consolidada + ITP bajo = ventaja competitiva.</p>",
            ["Guipúzcoa frontera", "Casco amurallado", "Gastronomía Michelin", "Comunidad francesa"],
        ],
    },
    "mondragon": {
        "name": "Mondragón",
        "roi": "5,6%", "precio": "2.200€", "alquiler": "1.023€/mes", "dias": "22",
        "alts": [("rentabilidad-eibar.html", "Eibar"), ("rentabilidad-arrasate.html", "Arrasate")],
        "paragraphs": [
            "<p>Mondragón (Arrasate) es la cuna y sede de <strong>Mondragón Corporación Cooperativa (MCC)</strong> — el mayor grupo cooperativo del mundo, con empresas como Fagor, Eroski, Laboral Kutxa y la Universidad de Mondragón. La economía está completamente apoyada en este modelo industrial-cooperativo singular. Precio medio: <strong>2.200€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>1.023€/mes</strong>.</p>",
            "<p>El inquilino tipo es trabajador-cooperativista de MCC (estabilidad laboral muy alta), estudiante de Mondragón Unibertsitatea y profesionales del valle del Deba. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centro, San Andrés y entorno universidad</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: piso de 2 dormitorios para alquiler residencial a cooperativistas con estabilidad laboral excepcional o estudiantes universitarios — demanda muy inelástica apoyada en modelo MCC.</p>",
            ["Alto Deba Guipúzcoa", "MCC cooperativa", "Universidad Mondragón", "Demanda inelástica"],
        ],
    },
    "tolosa": {
        "name": "Tolosa",
        "roi": "5,4%", "precio": "2.400€", "alquiler": "1.080€/mes", "dias": "22",
        "alts": [("rentabilidad-irun.html", "Irún"), ("rentabilidad-mondragon.html", "Mondragón")],
        "paragraphs": [
            "<p>Tolosa es una ciudad media de Guipúzcoa, capital histórica de la provincia hasta 1854, con un patrimonio histórico cuidado (casco antiguo, mercado del sábado), tradición chocolatera (referencia regional) y tejido industrial diversificado (papel, automoción). Conexión por A-15 a 25 minutos de San Sebastián. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 5,4%</strong>; alquiler medio <strong>1.080€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores industriales, comerciantes y profesionales que trabajan en San Sebastián pero prefieren vivir en Tolosa por coste/calidad de vida. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Centro histórico, Amarotz y Aldaba</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo industrial + spillover donostiarra. ITP bajo + entrada moderada para Guipúzcoa configuran ventaja competitiva.</p>",
            ["Guipúzcoa", "Antigua capital", "Industria papel", "Spillover Donostia"],
        ],
    },
    "zarautz": {
        "name": "Zarautz",
        "roi": "6,5%", "precio": "4.200€", "alquiler": "1.820€/mes", "dias": "22",
        "alts": [("rentabilidad-getaria.html", "Getaria"), ("rentabilidad-donostia.html", "Donostia")],
        "paragraphs": [
            "<p>Zarautz es uno de los destinos costeros premium de Guipúzcoa, con la <strong>playa de Zarautz</strong> (la más extensa del País Vasco) como referencia surfera y residencial. La cercanía a San Sebastián (20 km), a Getaria (Balenciaga, txakoli) y a la Costa Vasca-Geoparque configuran un entorno premium. Precio medio: <strong>4.200€/m²</strong> — alto, marca premium — y <strong>rentabilidad bruta del 6,5%</strong> (combinación inusual de premium + yield alto).</p>",
            "<p>El inquilino tipo es residente vasco con poder adquisitivo (profesionales liberales, alta dirección donostiarra), surferos internacionales y demanda VUT estival. Alquiler medio: <strong>1.820€/mes</strong>; <strong>22 días</strong> de absorción confirman demanda fuerte. Zonas: <strong>Centro, Salberdin y entorno playa</strong>. ITP País Vasco: <strong>4%</strong>. Tesis: piso próximo a la playa para alquiler residencial premium a comunidad donostiarra + VUT segmentado a surferos. ITP bajo aporta ventaja fiscal significativa frente a Costa Brava o Mediterráneo premium.</p>",
            ["Guipúzcoa costa", "Surf", "Premium playa", "Yield alto premium"],
        ],
    },

    # ===== CASTILLA-LA MANCHA (6) - ITP 9% =====
    "alcazar-de-san-juan": {
        "name": "Alcázar de San Juan",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "595€/mes", "dias": "26",
        "alts": [("rentabilidad-tomelloso.html", "Tomelloso"), ("rentabilidad-ciudad-real.html", "Ciudad Real")],
        "paragraphs": [
            "<p>Alcázar de San Juan es uno de los principales nodos ferroviarios de España (intersección de líneas Madrid-Andalucía, Madrid-Levante y Mediterráneo), capital comarcal de la Mancha, con economía apoyada en agroindustria del vino (DO La Mancha), molinos de viento y la base militar de Helicópteros del Ejército de Tierra (BHELMA). Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>595€/mes</strong>.</p>",
            "<p>El inquilino tipo combina personal ferroviario (RENFE, ADIF), trabajadores agroindustriales, militares y familias locales. Los <strong>26 días</strong> de absorción reflejan ritmo pausado del interior manchego. Zonas: <strong>Centro, San Juan y entorno estación</strong>. ITP Castilla-La Mancha: <strong>9%</strong> (alto, encarece operación). Tesis: piso urbano para alquiler residencial estable apoyado en empleo institucional ferroviario y militar (sectores con baja sensibilidad cíclica), con yield decente y ticket bajo.</p>",
            ["La Mancha", "Nodo ferroviario", "Agroindustria vino", "BHELMA"],
        ],
    },
    "almansa": {
        "name": "Almansa",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "542€/mes", "dias": "27",
        "alts": [("rentabilidad-villena.html", "Villena"), ("rentabilidad-yecla.html", "Yecla")],
        "paragraphs": [
            "<p>Almansa es una ciudad media del este de Albacete, con un Castillo medieval icónico, escenario de la decisiva <strong>Batalla de Almansa (1707)</strong> en la Guerra de Sucesión, y un tejido económico apoyado en industria del calzado (cluster Almansa-Villena-Elda) y la agroindustria. Conexión por AVE Madrid-Levante y A-31. Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>542€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores del calzado, agroindustria y servicios. Los <strong>27 días</strong> de absorción reflejan ritmo pausado típico de mercado interior. Zonas: <strong>Centro, San Roque y entorno Castillo</strong>. ITP Castilla-La Mancha: <strong>9%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo industrial del calzado, con tickets bajos (vivienda completa <70.000€) y yield decente. Plaza para inversor rentista que diversifica fuera del eje turístico-mediterráneo.</p>",
            ["Albacete este", "Calzado", "Castillo histórico", "AVE"],
        ],
    },
    "hellin": {
        "name": "Hellín",
        "roi": "6,8%", "precio": "900€", "alquiler": "510€/mes", "dias": "28",
        "alts": [("rentabilidad-albacete.html", "Albacete"), ("rentabilidad-jumilla.html", "Jumilla")],
        "paragraphs": [
            "<p>Hellín es una ciudad media del sur de Albacete, conocida por la <strong>Tamborada de Hellín</strong> (Patrimonio Cultural Inmaterial de la Humanidad UNESCO, junto con Tobarra y otras) y por una economía agrícola potente (cereal, vid, hortícolas) y tradicional alfarería. Cabecera comarcal de Sierra del Segura. Precio medio: <strong>900€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>; alquiler medio <strong>510€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores agrícolas, agroindustria, servicios comarcales y un componente sanitario del Hospital de Hellín. Los <strong>28 días</strong> de absorción reflejan ritmo muy pausado del interior. Zonas: <strong>Centro, Constitución y entorno hospital</strong>. ITP Castilla-La Mancha: <strong>9%</strong>. Tesis: ticket muy bajo (vivienda completa <60.000€) con yield alto, plaza para inversor rentista que asume menor liquidez por máximo cash-flow porcentual.</p>",
            ["Albacete sur", "Tamborada UNESCO", "Cabecera comarcal", "Yield alto rentista"],
        ],
    },
    "puertollano": {
        "name": "Puertollano",
        "roi": "6,4%", "precio": "750€", "alquiler": "400€/mes", "dias": "22",
        "alts": [("rentabilidad-ciudad-real.html", "Ciudad Real"), ("rentabilidad-valdepenas.html", "Valdepeñas")],
        "paragraphs": [
            "<p>Puertollano es la segunda ciudad de Ciudad Real, con un perfil industrial-energético singular: sede de la <strong>Refinería Repsol</strong> (una de las mayores de España), de Encasur (química) y polo de generación renovable (energía solar fotovoltaica). Tras el cierre minero, ha consolidado su perfil energético. Precio medio: <strong>750€/m²</strong> — el más bajo del grupo — y <strong>rentabilidad bruta del 6,4%</strong>.</p>",
            "<p>El inquilino tipo es trabajador industrial-energético cualificado (Repsol, Iberdrola, química), técnicos en rotación y familias locales. Alquiler medio: <strong>400€/mes</strong>; <strong>22 días</strong> de absorción confirman demanda estructural. Zonas: <strong>Centro, El Carmen y entorno polígono</strong>. ITP Castilla-La Mancha: <strong>9%</strong>. Tesis: tickets extremadamente bajos (vivienda completa <50.000€) con demanda inelástica apoyada en empleo industrial-energético estructural. Plaza para inversor que busca diversificación geográfica con yield estable.</p>",
            ["Ciudad Real sur", "Refinería Repsol", "Polo energético", "Ticket muy bajo"],
        ],
    },
    "tomelloso": {
        "name": "Tomelloso",
        "roi": "6,5%", "precio": "1.100€", "alquiler": "595€/mes", "dias": "26",
        "alts": [("rentabilidad-alcazar-de-san-juan.html", "Alcázar de San Juan"), ("rentabilidad-valdepenas.html", "Valdepeñas")],
        "paragraphs": [
            "<p>Tomelloso es la <strong>capital mundial del vino</strong> por volumen de producción (la mayor concentración bodeguera de España), con DO La Mancha y un tejido económico apoyado en agroindustria vinícola, alcoholes y queso manchego. Cuna del escritor Francisco García Pavón (Plinio). Precio medio: <strong>1.100€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>595€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector vinícola (campañas estacionales), agroindustria (alcoholes, quesos) y servicios comarcales. Los <strong>26 días</strong> de absorción reflejan ritmo pausado típico del interior manchego. Zonas: <strong>Centro, Pueblo Nuevo y entorno polígono</strong>. ITP Castilla-La Mancha: <strong>9%</strong>. Tesis: ticket bajo con yield alto apoyado en empleo agroindustrial estructural. Plaza con marca vitivinícola consolidada para inversor rentista.</p>",
            ["La Mancha", "Capital mundial del vino", "DO La Mancha", "Yield alto"],
        ],
    },
    "valdepenas": {
        "name": "Valdepeñas",
        "roi": "6,8%", "precio": "1.000€", "alquiler": "567€/mes", "dias": "27",
        "alts": [("rentabilidad-tomelloso.html", "Tomelloso"), ("rentabilidad-ciudad-real.html", "Ciudad Real")],
        "paragraphs": [
            "<p>Valdepeñas es la capital de la <strong>DO Valdepeñas</strong> (vinos de larga tradición histórica desde el siglo XVI, con los típicos de mesa) y una ciudad media del sur de Ciudad Real con economía vinícola, agroindustrial (frigoríficos, conservas) y comercial. Conexión por A-4 y AVE (estación Villa de Valdepeñas). Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>; alquiler medio <strong>567€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores vinícolas, bodegas (Bodegas Real, Félix Solís), agroindustria y servicios comarcales. Los <strong>27 días</strong> de absorción reflejan ritmo pausado del interior. Zonas: <strong>Centro, Cervantes y Las Águilas</strong>. ITP Castilla-La Mancha: <strong>9%</strong>. Tesis: ticket bajo con yield alto, ideal para inversor rentista que busca cash-flow apoyado en empleo agroindustrial vinícola con marca DO consolidada.</p>",
            ["DO Valdepeñas", "Vino histórico", "AVE", "Yield alto rentista"],
        ],
    },

    # ===== GALICIA (5) - ITP 9% =====
    "cangas-do-morrazo": {
        "name": "Cangas do Morrazo",
        "roi": "5,9%", "precio": "1.800€", "alquiler": "886€/mes", "dias": "24",
        "alts": [("rentabilidad-vigo.html", "Vigo"), ("rentabilidad-pontevedra.html", "Pontevedra")],
        "paragraphs": [
            "<p>Cangas do Morrazo es uno de los municipios más singulares de la Ría de Vigo, en la Península do Morrazo, conectado con Vigo por catamarán (15 minutos) y con un perfil dual: pesquero tradicional y residencial-turístico creciente apoyado en el spillover de Vigo. Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,9%</strong>; alquiler medio <strong>886€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores pesqueros y conserveros, profesionales que trabajan en Vigo (vía catamarán o A-9), familias locales y un componente turístico estival creciente. Los <strong>24 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, Aldán y entorno catamarán</strong>. ITP Galicia: <strong>9%</strong>. Tesis: piso urbano para alquiler residencial estable a profesionales que conectan con Vigo + opción VUT estacional en zonas próximas a calas. Combinación interesante de yield/conexión metropolitana.</p>",
            ["Ría de Vigo", "Catamarán", "Pesquero", "Spillover Vigo"],
        ],
    },
    "carballo": {
        "name": "Carballo",
        "roi": "6,2%", "precio": "1.200€", "alquiler": "620€/mes", "dias": "26",
        "alts": [("rentabilidad-a-coruna.html", "A Coruña"), ("rentabilidad-cee.html", "Cee")],
        "paragraphs": [
            "<p>Carballo es la capital de la comarca de Bergantiños (A Coruña), con un perfil económico apoyado en agroindustria (cárnico, lácteo), comercio comarcal y proximidad al complejo industrial de Sabón (refinería, eólica). La conexión por AG-55 a 30 minutos de A Coruña la integra en un eje funcional. Precio medio: <strong>1.200€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>620€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores agroindustriales, profesionales del comercio comarcal, sector industrial Sabón y familias locales. Los <strong>26 días</strong> de absorción reflejan ritmo pausado del interior gallego. Zonas: <strong>Centro, Sofán y entorno polígono</strong>. ITP Galicia: <strong>9%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo agroindustrial diversificado, con tickets bajos para Galicia y yield decente. Plaza para inversor rentista comarcal.</p>",
            ["Bergantiños", "Cabecera comarcal", "Agroindustria", "Sabón industrial"],
        ],
    },
    "naron": {
        "name": "Narón",
        "roi": "6,2%", "precio": "1.200€", "alquiler": "620€/mes", "dias": "22",
        "alts": [("rentabilidad-ferrol.html", "Ferrol"), ("rentabilidad-fene.html", "Fene")],
        "paragraphs": [
            "<p>Narón es un municipio de Ferrolterra conurbado con Ferrol, con un perfil residencial-comercial creciente apoyado en el spillover de Ferrol y en su propio dinamismo (Centro Comercial Odeón, polígonos industriales). La conexión por AP-9 lo integra en el eje atlántico A Coruña-Ferrol. Precio medio: <strong>1.200€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>620€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del astillero Navantia (Ferrol vecino), industria auxiliar, comerciantes y familias jóvenes. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Xubia, A Solaina y entorno Centro Comercial</strong>. ITP Galicia: <strong>9%</strong>. Tesis: piso de 2-3 dormitorios para alquiler familiar estable, capturando spillover ferrolano con yield superior a Ferrol y tickets accesibles. Plaza con dinámica residencial creciente.</p>",
            ["Ferrolterra", "Conurbado Ferrol", "Navantia", "Familiar"],
        ],
    },
    "sanxenxo": {
        "name": "Sanxenxo",
        "roi": "5,4%", "precio": "2.600€", "alquiler": "1.170€/mes", "dias": "22",
        "alts": [("rentabilidad-o-grove.html", "O Grove"), ("rentabilidad-portonovo.html", "Portonovo")],
        "paragraphs": [
            "<p>Sanxenxo es la capital turística de las <strong>Rías Baixas</strong> pontevedresas, con marcas internacionales como <strong>Playa de Silgar, Portonovo, La Lanzada</strong> y un perfil veraniego premium. Sede de muchos eventos VIP, regatas y el círculo social madrileño-gallego. Precio medio: <strong>2.600€/m²</strong>; <strong>rentabilidad bruta 5,4%</strong>; alquiler medio <strong>1.170€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hoteleros y de servicios turísticos, residentes premium gallegos-madrileños con segunda residencia y demanda VUT estival muy intensa. Los <strong>22 días</strong> de absorción reflejan demanda fuerte. Zonas: <strong>Centro, Portonovo y A Lanzada</strong>. ITP Galicia: <strong>9%</strong>. Tesis: piso o estudio próximo a Silgar/Portonovo para VUT estival premium (yield combinado muy superior) o residencial a personal hotelero. Marca consolidada que sostiene la apreciación.</p>",
            ["Rías Baixas", "Capital turística Galicia", "Premium veraniego", "VUT premium"],
        ],
    },
    "vilagarcia-de-arousa": {
        "name": "Vilagarcía de Arousa",
        "roi": "5,8%", "precio": "1.800€", "alquiler": "870€/mes", "dias": "24",
        "alts": [("rentabilidad-cambados.html", "Cambados"), ("rentabilidad-pontevedra.html", "Pontevedra")],
        "paragraphs": [
            "<p>Vilagarcía de Arousa es la cabecera comarcal del Salnés, en la Ría de Arousa pontevedresa, con un puerto industrial-comercial activo, una flota pesquera importante (mejillón, almeja) y un componente turístico de proximidad apoyado en las Rías Baixas. Conexión por AP-9 y AVE (Vilagarcía). Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>870€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores portuarios, sector marisquero (mejilloneros), profesionales del comercio comarcal y un componente residencial-turístico estival. Los <strong>24 días</strong> de absorción reflejan mercado fluido. Zonas: <strong>Centro, Carril y A Illa de Arousa (vecino)</strong>. ITP Galicia: <strong>9%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo portuario-pesquero + opción VUT estival. Plaza con buena combinación coste/yield en Rías Baixas.</p>",
            ["Ría de Arousa", "Cabecera comarcal", "Mejillón/almeja", "AVE"],
        ],
    },

    # ===== ASTURIAS (5) - ITP 8% =====
    "castrillon": {
        "name": "Castrillón",
        "roi": "6,5%", "precio": "1.300€", "alquiler": "640€/mes", "dias": "22",
        "alts": [("rentabilidad-aviles.html", "Avilés"), ("rentabilidad-corvera-de-asturias.html", "Corvera")],
        "paragraphs": [
            "<p>Castrillón es un municipio del centro asturiano, conurbado con Avilés, con un perfil dual: zona costera residencial premium (<strong>Salinas</strong>, una de las playas urbanas más demandadas de Asturias, surf y residencial de alta gama) y núcleo administrativo-comercial (Piedras Blancas) apoyado en industria avilesina. Precio medio: <strong>1.300€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable.</p>",
            "<p>El inquilino tipo combina trabajadores industriales (Arcelor Avilés, química), profesionales que trabajan en Avilés-Oviedo, familias residenciales y un componente turístico estival en Salinas. Alquiler medio: <strong>640€/mes</strong>; <strong>22 días</strong> de absorción. Zonas: <strong>Salinas (premium costero), Piedras Blancas y Naveces</strong>. ITP Asturias: <strong>8%</strong>. Tesis: piso en Salinas para alquiler residencial premium o VUT estival, capturando combinación premium costero + yield alto. Plaza con marca residencial consolidada.</p>",
            ["Centro Asturias", "Salinas", "Conurbado Avilés", "Premium costero"],
        ],
    },
    "llanes": {
        "name": "Llanes",
        "roi": "5,6%", "precio": "2.000€", "alquiler": "933€/mes", "dias": "25",
        "alts": [("rentabilidad-ribadesella.html", "Ribadesella"), ("rentabilidad-cangas-de-onis.html", "Cangas de Onís")],
        "paragraphs": [
            "<p>Llanes es uno de los destinos turísticos más consolidados del oriente asturiano, con un casco histórico marinero protegido, las famosas <strong>Cubos de la Memoria</strong> de Agustín Ibarrola en el puerto y playas como Sablón, Toró, Cué y Andrín. La cercanía a los Picos de Europa y la marca turística consolidada sostienen la demanda. Precio medio: <strong>2.000€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>933€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes locales (sector turístico, hostelería), comunidad madrileña con segunda residencia y demanda VUT estival muy intensa. Los <strong>25 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Casco histórico (regulado), Sablón y Cué</strong>. ITP Asturias: <strong>8%</strong>. Tesis: vivienda con encanto en casco histórico para VUT cultural-natural estival o residencial a personal hostelero. Marca consolidada de turismo asturiano premium.</p>",
            ["Asturias oriental", "Cubos de la Memoria", "Playas históricas", "VUT premium"],
        ],
    },
    "luarca": {
        "name": "Luarca",
        "roi": "5,8%", "precio": "1.800€", "alquiler": "870€/mes", "dias": "25",
        "alts": [("rentabilidad-aviles.html", "Avilés"), ("rentabilidad-cudillero.html", "Cudillero")],
        "paragraphs": [
            "<p>Luarca es la capital del concejo de Valdés, conocida como la <strong>Villa Blanca de la Costa Verde</strong>, con uno de los puertos pesqueros más pintorescos de Asturias, casas de indianos cuidadas y un casco histórico que combina pesca, turismo y tradición ballenera (Severo Ochoa nació aquí). Precio medio: <strong>1.800€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>870€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores pesqueros y conserveros, residentes locales, jubilados y un componente turístico estival. Los <strong>25 días</strong> de absorción reflejan mercado pausado típico del occidente asturiano. Zonas: <strong>Centro, Puerto y entorno paseo</strong>. ITP Asturias: <strong>8%</strong>. Tesis: vivienda con encanto en zona puerto para alquiler residencial estable o VUT cultural-gastronómico. Plaza con identidad propia y marca turística diferenciada del eje oriental masivo.</p>",
            ["Asturias occidental", "Villa Blanca", "Puerto pesquero", "Casas de indianos"],
        ],
    },
    "ribadesella": {
        "name": "Ribadesella",
        "roi": "5,8%", "precio": "2.000€", "alquiler": "966€/mes", "dias": "24",
        "alts": [("rentabilidad-llanes.html", "Llanes"), ("rentabilidad-cangas-de-onis.html", "Cangas de Onís")],
        "paragraphs": [
            "<p>Ribadesella es una de las plazas más turísticas del oriente asturiano, en la desembocadura del río Sella (sede del internacional <strong>Descenso Internacional del Sella</strong>) con la <strong>Cueva de Tito Bustillo</strong> (Patrimonio Mundial UNESCO, arte rupestre) y la playa de Santa Marina como referencias. Precio medio: <strong>2.000€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>966€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hosteleros, residentes locales, comunidad madrileña con segunda residencia y demanda VUT estival intensiva. Los <strong>24 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centro, Santa Marina y entorno puerto</strong>. ITP Asturias: <strong>8%</strong>. Tesis: vivienda en Santa Marina o casco para VUT estival con tarifas premium (Sella + Picos de Europa) o residencial a personal hostelero. Marca turística consolidada con triple eje (mar, río, montaña).</p>",
            ["Asturias oriental", "Sella", "Tito Bustillo UNESCO", "VUT triple eje"],
        ],
    },
    "siero": {
        "name": "Siero",
        "roi": "5,8%", "precio": "1.400€", "alquiler": "680€/mes", "dias": "22",
        "alts": [("rentabilidad-oviedo.html", "Oviedo"), ("rentabilidad-langreo.html", "Langreo")],
        "paragraphs": [
            "<p>Siero es uno de los municipios estrella del área central de Asturias, con <strong>Pola de Siero</strong> como capital y referencia comercial-residencial del centro de la región. Conurbado funcionalmente con Oviedo (15 km), alberga importantes polígonos industriales (Granda, Bobes), el Hipódromo y el centro comercial Parque Principado. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>680€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores industriales y comerciales, profesionales que trabajan en Oviedo y familias jóvenes. Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Pola de Siero, Lugones y entorno polígono</strong>. ITP Asturias: <strong>8%</strong>. Tesis: piso de 2-3 dormitorios en Pola o Lugones para alquiler familiar estable, capturando spillover ovetense con yield superior a Oviedo y entrada accesible. Plaza con dinámica metropolitana propia.</p>",
            ["Centro Asturias", "Pola de Siero", "Conurbado Oviedo", "Polígonos industriales"],
        ],
    },

    # ===== ARAGÓN (3) - ITP 8% =====
    "alcaniz": {
        "name": "Alcañiz",
        "roi": "6,8%", "precio": "1.000€", "alquiler": "567€/mes", "dias": "27",
        "alts": [("rentabilidad-teruel.html", "Teruel"), ("rentabilidad-zaragoza.html", "Zaragoza")],
        "paragraphs": [
            "<p>Alcañiz es la capital del Bajo Aragón turolense, una ciudad media histórica (Castillo Calatravo, casco antiguo monumental) con un perfil económico singular: combina agricultura del olivar, agroindustria y el complejo internacional de <strong>MotorLand Aragón</strong> (sede de la MotoGP, WSBK y Fórmula Renault), polo automovilístico mundial. Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>; alquiler medio <strong>567€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores agrícolas, agroindustria, sector servicios y un componente turístico-deportivo vinculado a MotorLand. Los <strong>27 días</strong> de absorción reflejan ritmo pausado interior. Zonas: <strong>Centro, Plaza de España y entorno Castillo</strong>. ITP Aragón: <strong>8%</strong>. Tesis: ticket bajo con yield alto + nicho VUT puntual en eventos MotorLand (tarifas premium concentradas en pocos fines de semana). Plaza para inversor rentista con upside turístico-deportivo.</p>",
            ["Bajo Aragón", "MotorLand", "Olivar", "Yield alto rentista"],
        ],
    },
    "barbastro": {
        "name": "Barbastro",
        "roi": "6,5%", "precio": "1.200€", "alquiler": "650€/mes", "dias": "26",
        "alts": [("rentabilidad-huesca.html", "Huesca"), ("rentabilidad-monzon.html", "Monzón")],
        "paragraphs": [
            "<p>Barbastro es la capital del Somontano oscense, referencia de la <strong>DO Somontano</strong> (vinos de calidad reconocidos internacionalmente) y un patrimonio histórico-religioso potente (Catedral, Conjunto de San Julián). La cercanía al Pirineo (Pirineos Aragoneses, Aínsa-Sobrarbe) y la conexión por A-22 configuran una plaza con identidad. Precio medio: <strong>1.200€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>650€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores agroindustriales (vino, hortícolas), profesionales sanitarios del Hospital de Barbastro, comerciantes y familias locales. Los <strong>26 días</strong> de absorción reflejan ritmo pausado típico del interior. Zonas: <strong>Centro, Santo Cristo y entorno Catedral</strong>. ITP Aragón: <strong>8%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo agroindustrial vinícola + sanitario. Yield decente con marca DO Somontano consolidada.</p>",
            ["Somontano", "DO Somontano vino", "Cabecera comarcal", "Yield rentista"],
        ],
    },
    "calatayud": {
        "name": "Calatayud",
        "roi": "7,0%", "precio": "900€", "alquiler": "525€/mes", "dias": "27",
        "alts": [("rentabilidad-zaragoza.html", "Zaragoza"), ("rentabilidad-tarazona.html", "Tarazona")],
        "paragraphs": [
            "<p>Calatayud es la capital de la Comunidad de Calatayud (Zaragoza), una ciudad media con un patrimonio histórico-religioso excepcional (Colegiata de Santa María, antigua Bilbilis romana) y conexión por <strong>AVE Madrid-Barcelona</strong> (estación AVE Calatayud) y A-2. La economía combina agricultura, agroindustria y servicios comarcales. Precio medio: <strong>900€/m²</strong>; <strong>rentabilidad bruta 7,0%</strong> — top del grupo.</p>",
            "<p>El inquilino tipo es local: trabajadores agroindustriales, sector servicios, profesionales sanitarios del Hospital Ernest Lluch y un componente vinculado a la conexión AVE (profesionales que viajan a Madrid/Zaragoza). Alquiler medio: <strong>525€/mes</strong>; <strong>27 días</strong> de absorción. Zonas: <strong>Centro, Bilbilis y entorno estación</strong>. ITP Aragón: <strong>8%</strong>. Tesis: ticket muy bajo (vivienda completa <55.000€) con yield top, plaza para rentista que aprovecha conexión AVE como factor de revalorización potencial.</p>",
            ["Comunidad Calatayud", "AVE", "Bilbilis", "Yield top rentista"],
        ],
    },

    # ===== EXTREMADURA (3) - ITP 8% =====
    "almendralejo": {
        "name": "Almendralejo",
        "roi": "6,5%", "precio": "900€", "alquiler": "470€/mes", "dias": "22",
        "alts": [("rentabilidad-merida.html", "Mérida"), ("rentabilidad-zafra.html", "Zafra")],
        "paragraphs": [
            "<p>Almendralejo es la capital de la <strong>Tierra de Barros</strong> (Badajoz), referencia vitivinícola con la <strong>DO Ribera del Guadiana</strong> (mayor zona productora de Extremadura, vinos blancos y tintos) y un tejido económico apoyado en agroindustria del vino, aceite, cárnico y agricultura. Precio medio: <strong>900€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>470€/mes</strong>.</p>",
            "<p>El inquilino tipo es local: trabajadores agrícolas, bodegas, agroindustria y servicios. Los <strong>22 días</strong> de absorción reflejan demanda estructural sólida para una ciudad media interior. Zonas: <strong>Centro, San Francisco y entorno polígono</strong>. ITP Extremadura: <strong>8%</strong>. Tesis: ticket extremadamente bajo (vivienda completa <50.000€) con yield decente apoyado en empleo agroindustrial estructural. Plaza ideal para inversor rentista que diversifica geográficamente con cash-flow alto y baja entrada.</p>",
            ["Tierra de Barros", "DO Ribera del Guadiana", "Agroindustria vinícola", "Ticket muy bajo"],
        ],
    },
    "navalmoral-de-la-mata": {
        "name": "Navalmoral de la Mata",
        "roi": "6,5%", "precio": "1.000€", "alquiler": "542€/mes", "dias": "27",
        "alts": [("rentabilidad-plasencia.html", "Plasencia"), ("rentabilidad-talavera-de-la-reina.html", "Talavera de la Reina")],
        "paragraphs": [
            "<p>Navalmoral de la Mata es la cabecera comarcal del Campo Arañuelo cacereño, un nodo logístico-comercial entre Madrid y Extremadura (A-5), con un perfil económico singular: la cercanía a la <strong>Central Nuclear de Almaraz</strong> (a 18 km, una de las mayores de España) genera empleo cualificado estructural. Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong>; alquiler medio <strong>542€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores de la Central Nuclear (técnicos, ingenieros con contratos largos), comerciantes y familias locales. Los <strong>27 días</strong> de absorción reflejan ritmo pausado del interior. Zonas: <strong>Centro, Las Eras y entorno A-5</strong>. ITP Extremadura: <strong>8%</strong>. Tesis: piso de 2 dormitorios para alquiler a personal nuclear (rotación previsible, ingresos estables) — nicho de demanda muy específico con baja sensibilidad cíclica. Cuidado: depende del calendario de cierre nuclear post-2027.</p>",
            ["Campo Arañuelo", "Central Nuclear Almaraz", "A-5", "Empleo nuclear"],
        ],
    },
    "zafra": {
        "name": "Zafra",
        "roi": "6,8%", "precio": "1.000€", "alquiler": "567€/mes", "dias": "27",
        "alts": [("rentabilidad-almendralejo.html", "Almendralejo"), ("rentabilidad-merida.html", "Mérida")],
        "paragraphs": [
            "<p>Zafra — la <strong>Sevilla la Chica</strong> — es una ciudad histórica del sur de Badajoz, capital de la comarca Zafra-Río Bodión, con un patrimonio renacentista excepcional (Alcázar de los Duques de Feria, Plazas Grande y Chica) y la <strong>Feria Internacional Ganadera de San Miguel</strong> (referencia ganadera española). Conexión por A-66. Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>; alquiler medio <strong>567€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores ganaderos-agrícolas (cerdo ibérico, ovino), comerciantes (importante mercado mayorista comarcal) y un nicho de turismo cultural. Los <strong>27 días</strong> de absorción reflejan ritmo pausado del interior. Zonas: <strong>Casco histórico (regulado), Centro y entorno Plaza Grande</strong>. ITP Extremadura: <strong>8%</strong>. Tesis: ticket bajo con yield alto + opción VUT cultural en casco histórico. Plaza con marca patrimonial consolidada.</p>",
            ["Sevilla la Chica", "Ganadería ibérico", "Patrimonio renacentista", "Yield alto"],
        ],
    },

    # ===== CANTABRIA (3) - ITP 9-10% =====
    "castro-urdiales": {
        "name": "Castro-Urdiales",
        "roi": "6,5%", "precio": "2.400€", "alquiler": "1.060€/mes", "dias": "22",
        "alts": [("rentabilidad-laredo.html", "Laredo"), ("rentabilidad-bilbao.html", "Bilbao")],
        "paragraphs": [
            "<p>Castro-Urdiales es el municipio más oriental de Cantabria, prácticamente conurbado funcionalmente con el Gran Bilbao por la A-8 (35 minutos a Bilbao centro). Combina pueblo pesquero histórico (puerto, casco antiguo cuidado), playas urbanas y un componente residencial muy fuerte de profesionales bilbaínos que prefieren vivir en Cantabria. Precio medio: <strong>2.400€/m²</strong>; <strong>rentabilidad bruta 6,5%</strong> — combinación notable.</p>",
            "<p>El inquilino tipo es profesional bilbaíno o industrial vasco que trabaja en Bilbao y vive en Castro por calidad de vida + componente residencial cántabro. Alquiler medio: <strong>1.060€/mes</strong>; <strong>22 días</strong> de absorción confirman demanda fuerte. Zonas: <strong>Centro, Brazomar y Sámano</strong>. ITP Cantabria: <strong>10%</strong> (alto, encarece operación). Tesis: piso para alquiler residencial estable a profesional bilbaíno (rotación baja, contratos largos) — demanda inelástica apoyada en spillover bilbaíno + marca costera cántabra.</p>",
            ["Cantabria oriental", "Spillover Bilbao", "A-8 Bilbao 35 min", "Yield alto costero"],
        ],
    },
    "laredo": {
        "name": "Laredo",
        "roi": "5,8%", "precio": "1.900€", "alquiler": "918€/mes", "dias": "23",
        "alts": [("rentabilidad-castro-urdiales.html", "Castro-Urdiales"), ("rentabilidad-santona.html", "Santoña")],
        "paragraphs": [
            "<p>Laredo es uno de los destinos costeros consolidados del oriente cántabro, con la <strong>Playa de la Salvé</strong> (5 km, una de las más largas del Cantábrico) y la histórica Puebla Vieja medieval (Conjunto Histórico-Artístico). El componente turístico es estival muy intenso (multiplica su población en julio-agosto). Precio medio: <strong>1.900€/m²</strong>; <strong>rentabilidad bruta 5,8%</strong>; alquiler medio <strong>918€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores hosteleros, residentes locales, comunidad madrileña con segunda residencia y demanda VUT estival intensa. Los <strong>23 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centro, Puebla Vieja y entorno Salvé</strong>. ITP Cantabria: <strong>10%</strong>. Tesis: piso próximo a Salvé para VUT estival (yield combinado superior) o residencial estable. Marca turística cántabra consolidada con diferenciación clara respecto a Castro-Urdiales (más residencial bilbaíno).</p>",
            ["Cantabria oriental", "Salvé histórica", "Puebla Vieja", "VUT estival"],
        ],
    },
    "suances": {
        "name": "Suances",
        "roi": "5,6%", "precio": "2.000€", "alquiler": "933€/mes", "dias": "24",
        "alts": [("rentabilidad-santander.html", "Santander"), ("rentabilidad-santillana-del-mar.html", "Santillana del Mar")],
        "paragraphs": [
            "<p>Suances es un municipio costero del centro de Cantabria, con un perfil residencial-turístico apoyado en sus playas (La Concha, Los Locos para surf) y la cercanía a Santander (25 km) y Santillana del Mar (10 km). Combina turismo familiar con un componente residencial creciente. Precio medio: <strong>2.000€/m²</strong>; <strong>rentabilidad bruta 5,6%</strong>; alquiler medio <strong>933€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes locales, profesionales que trabajan en Santander, surferos y demanda VUT estival familiar. Los <strong>24 días</strong> de absorción reflejan mercado activo. Zonas: <strong>Centro, La Concha y Hinojedo</strong>. ITP Cantabria: <strong>10%</strong>. Tesis: piso próximo a La Concha para alquiler residencial estable a profesional santanderino o VUT estival familiar. Plaza con buena combinación coste/yield + cercanía a la marca turística cántabra (Santillana, Comillas).</p>",
            ["Centro Cantabria", "Cerca de Santander", "Playas surf", "Mixto residencial/VUT"],
        ],
    },

    # ===== CASTILLA Y LEÓN (2) - ITP 8% =====
    "ciudad-rodrigo": {
        "name": "Ciudad Rodrigo",
        "roi": "6,8%", "precio": "1.000€", "alquiler": "567€/mes", "dias": "28",
        "alts": [("rentabilidad-salamanca.html", "Salamanca"), ("rentabilidad-bejar.html", "Béjar")],
        "paragraphs": [
            "<p>Ciudad Rodrigo es una ciudad histórica del oeste salmantino, plaza fuerte fronteriza con Portugal con una <strong>muralla medieval intacta</strong> (3 km de perímetro), Catedral románico-gótica y un casco antiguo declarado Conjunto Histórico-Artístico. La economía combina turismo cultural, comercio fronterizo (Portugal a 30 km) y agricultura comarcal. Precio medio: <strong>1.000€/m²</strong>; <strong>rentabilidad bruta 6,8%</strong>; alquiler medio <strong>567€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes locales, militares de la Brigada Galicia VII (acuartelamiento en la ciudad), comerciantes y un nicho de turismo cultural. Los <strong>28 días</strong> de absorción reflejan ritmo pausado del interior fronterizo. Zonas: <strong>Casco amurallado (regulado), Sancti Spíritu y entorno Catedral</strong>. ITP Castilla y León: <strong>8%</strong>. Tesis: vivienda con encanto en casco amurallado para VUT cultural + alquiler residencial militar. Plaza con marca patrimonial consolidada.</p>",
            ["Oeste salmantino", "Frontera Portugal", "Muralla medieval", "Brigada militar"],
        ],
    },
    "segovia": {
        "name": "Segovia",
        "roi": "5,7%", "precio": "1.600€", "alquiler": "760€/mes", "dias": "22",
        "alts": [("rentabilidad-avila.html", "Ávila"), ("rentabilidad-valladolid.html", "Valladolid")],
        "paragraphs": [
            "<p>Segovia es una de las grandes capitales históricas españolas, con tres iconos Patrimonio de la Humanidad UNESCO: el <strong>Acueducto romano, el Alcázar y la Catedral gótica</strong>. Combina turismo cultural masivo (excursionistas desde Madrid en el día), gastronomía premium (cochinillo) y conexión por <strong>AVE en 27 minutos a Madrid Chamartín</strong>, factor estructural para residencial. Precio medio: <strong>1.600€/m²</strong>; <strong>rentabilidad bruta 5,7%</strong>; alquiler medio <strong>760€/mes</strong>.</p>",
            "<p>El inquilino tipo combina funcionarios, profesionales que aprovechan AVE para trabajar en Madrid (commuters), estudiantes (campus IE University, sede UVa) y demanda turística (VUT regulada en zona patrimonio). Los <strong>22 días</strong> de absorción reflejan demanda estable. Zonas: <strong>Casco histórico (regulado), Nueva Segovia y entorno AVE</strong>. ITP Castilla y León: <strong>8%</strong>. Tesis: piso urbano cerca del AVE para alquiler a commuters Madrid + opción VUT cultural — combinación de marca UNESCO + conectividad ferroviaria.</p>",
            ["Capital UNESCO", "AVE 27 min Madrid", "Patrimonio masivo", "Commuters"],
        ],
    },

    # ===== NAVARRA (1) - ITP 6% =====
    "estella-lizarra": {
        "name": "Estella-Lizarra",
        "roi": "6,0%", "precio": "1.400€", "alquiler": "700€/mes", "dias": "25",
        "alts": [("rentabilidad-pamplona.html", "Pamplona"), ("rentabilidad-tudela.html", "Tudela")],
        "paragraphs": [
            "<p>Estella-Lizarra es una ciudad histórica del sur de Navarra, parada clave del <strong>Camino de Santiago Francés</strong>, con un patrimonio románico-medieval excepcional (Iglesia del Santo Sepulcro, Palacio Real) y una economía combinando agroindustria, comercio comarcal y un componente turístico vinculado al Camino. Precio medio: <strong>1.400€/m²</strong>; <strong>rentabilidad bruta 6,0%</strong>; alquiler medio <strong>700€/mes</strong>.</p>",
            "<p>El inquilino tipo combina residentes locales, trabajadores agroindustriales y un nicho de servicios al peregrino. Los <strong>25 días</strong> de absorción reflejan ritmo pausado del interior. Zonas: <strong>Casco histórico, San Pedro y entorno Camino</strong>. ITP Navarra: <strong>6%</strong> (más bajo que CCAA limítrofes — ventaja fiscal). Tesis: piso urbano para alquiler residencial estable + nicho VUT/albergue para peregrinos del Camino. Plaza con marca patrimonial-jacobea consolidada y ventaja fiscal por foralidad.</p>",
            ["Sur Navarra", "Camino de Santiago", "Patrimonio románico", "ITP foral 6%"],
        ],
    },

    # ===== LA RIOJA (1) - ITP 7% =====
    "haro": {
        "name": "Haro",
        "roi": "6,2%", "precio": "1.300€", "alquiler": "671€/mes", "dias": "25",
        "alts": [("rentabilidad-logrono.html", "Logroño"), ("rentabilidad-laguardia.html", "Laguardia")],
        "paragraphs": [
            "<p>Haro es la <strong>capital del vino de Rioja</strong> por excelencia: el Barrio de la Estación concentra una densidad de bodegas centenarias única en el mundo (López de Heredia Tondonia, CVNE, Muga, La Rioja Alta, Bodegas Bilbaínas, Roda). La economía está completamente apoyada en el sector vitivinícola y un creciente turismo enológico premium. Precio medio: <strong>1.300€/m²</strong>; <strong>rentabilidad bruta 6,2%</strong>; alquiler medio <strong>671€/mes</strong>.</p>",
            "<p>El inquilino tipo combina trabajadores del sector vinícola (bodegueros, técnicos, comerciales), profesionales del turismo enológico y residentes locales. Los <strong>25 días</strong> de absorción reflejan ritmo pausado típico del interior. Zonas: <strong>Centro, Barrio de la Estación y entorno bodegas históricas</strong>. ITP La Rioja: <strong>7%</strong>. Tesis: piso urbano para alquiler residencial estable apoyado en empleo vinícola estructural + opción VUT enoturístico premium. Marca DOC Rioja sostiene la apreciación a medio plazo.</p>",
            ["Rioja Alta", "Capital vino DOC Rioja", "Barrio de la Estación", "Enoturismo premium"],
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

print(f"OK insertadas: {len(inserted)} de {len(CITIES)}")
for s in inserted: print(f"  + {s}")
if errors:
    print("\nERRORES:")
    for e in errors: print(f"  ! {e}")
