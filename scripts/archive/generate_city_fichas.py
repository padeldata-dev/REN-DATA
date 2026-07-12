#!/usr/bin/env python3
"""Genera 7 fichas de ciudades a partir de archivos twin (rentabilidad-*.html).

Idempotente: si la salida ya existe, se sobreescribe.
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"

# ---------------------------------------------------------------------------
# Datos por ciudad
# ---------------------------------------------------------------------------
CITIES = [
    dict(
        slug="santa-coloma-de-gramenet",
        name="Santa Coloma de Gramenet",
        ccaa="Cataluña",
        ccaa_slug="cataluna",
        prov="Barcelona",
        pop=123981,
        twin="l-hospitalet-de-llobregat",
        precio=2700, alq=1200, roi=5.3, vp=5.6, va=8.0, dias=21,
        itp_pct=10, itp_label="Cataluña",
        region="norte",
        tags=["Suburbio Barcelona", "Demanda inquilino joven", "Yields > Barcelona", "Riesgo zonas tensionadas"],
        editorial=[
            "Santa Coloma de Gramenet es uno de los municipios más densos del área metropolitana de Barcelona — apenas 4 km² para casi 124.000 habitantes — y desempeña un papel clave en la cadena residencial barcelonesa: absorbe a inquilinos jóvenes, parejas sin hijos y familias trabajadoras desplazadas del núcleo central por los precios de Barcelona ciudad. A <strong>2.700€/m²</strong> — la mitad de lo que cuesta Eixample o Gràcia — y con un yield bruto del <strong>5,3%</strong>, ofrece rentabilidades algo superiores a las de Barcelona capital con un perfil de inquilino estructuralmente sólido por la conectividad con la L1 y L9N.",
            "El inquilino tipo aquí es joven, profesional precario, autónomo o estudiante de últimos cursos que ya no puede pagar Barcelona pero quiere mantener acceso directo en metro. La demanda de alquiler es muy alta y los pisos se cubren con rapidez: <strong>21 días</strong> de tiempo medio de venta. Las zonas con mejor relación precio/demanda son <strong>Singuerlín, Llatí y Centre</strong>, próximas a estaciones de metro y bien conectadas con la red de cercanías Rodalies. La estrategia óptima es piso de 2 dormitorios para parejas y profesionales jóvenes en alquiler de larga duración.",
            "El principal riesgo es regulatorio: <strong>Cataluña aplica el índice de zonas tensionadas</strong> con tope al precio del alquiler, y Santa Coloma está en la lista activa desde 2024. Verificar siempre si el inmueble cae dentro de la zona declarada antes de comprar. ITP Cataluña: <strong>10%</strong> (uno de los más altos de España). La revalorización es moderada por la madurez del mercado, pero la demanda estructural y el yield superior a Barcelona compensan."
        ],
        alt_cities=[("Badalona","badalona"),("L'Hospitalet de Llobregat","l-hospitalet-de-llobregat")],
        perspectiva="Santa Coloma es el clásico extrarradio metropolitano denso: yield superior a Barcelona capital, demanda sólida del eje L1/L9 y precios todavía 50% por debajo del núcleo central. La tesis es piso compacto de 60-75 m² cerca de metro para alquiler joven o profesional. El gran caveat es la regulación catalana de zonas tensionadas — antes de comprar hay que verificar el tope vigente para esa dirección concreta.",
        nearest=[("Badalona","badalona","2.600€"),("Cornellà de Llobregat","cornella-de-llobregat","2.800€"),("L'Hospitalet de Llobregat","l-hospitalet-de-llobregat","3.400€"),("Mataró","mataro","2.200€")],
    ),
    dict(
        slug="melilla",
        name="Melilla",
        ccaa="Melilla",
        ccaa_slug="andalucia",  # placeholder slug for ccaa link
        prov="Melilla",
        pop=86780,
        twin="cadiz",
        precio=1300, alq=700, roi=6.5, vp=4.0, va=5.0, dias=32,
        itp_pct=0.5, itp_label="Melilla (IPSI)",
        region="andalucia",
        tags=["Ciudad autónoma", "Régimen IPSI", "Demanda institucional", "Sin zonas tensionadas"],
        editorial=[
            "Melilla es una de las dos ciudades autónomas españolas y uno de los mercados inmobiliarios más singulares del país. La economía depende fuertemente del sector público — funcionarios estatales, militares, Guardia Civil, sanitarios y docentes destinados temporalmente — y eso configura una demanda de alquiler institucional muy estable pero limitada en volumen. A <strong>1.300€/m²</strong> y con un yield bruto del <strong>6,5%</strong>, Melilla está claramente por encima de la media nacional en rentabilidad, aunque con un mercado de muy poca profundidad.",
            "El inquilino tipo es funcionario en traslado de 2-4 años, militar destinado o personal sanitario en plaza temporal. Los contratos suelen ser cortos pero con altísima solvencia, lo que reduce el riesgo de impagos a casi cero. Las zonas más demandadas son <strong>Centro, Real y Polígono</strong>, próximas a las plazas administrativas y a los servicios. El alquiler medio se sitúa en <strong>700€/mes</strong> para un piso estándar, con <strong>32 días</strong> de tiempo medio en mercado en el lado de compraventa — más lento que la península por la menor liquidez.",
            "La gran ventaja fiscal es el <strong>régimen IPSI</strong>: en lugar de ITP autonómico (7-10% en el resto de España), las transmisiones tributan al <strong>0,5%</strong> aproximadamente, lo que reduce drásticamente los gastos de compra. Además se aplica una <strong>bonificación del 60% en IRPF</strong> a residentes y no hay zonas tensionadas declaradas. Los principales riesgos son geopolíticos (frontera con Marruecos) y de liquidez de salida: vender un piso en Melilla puede llevar varios meses por el reducido pool de compradores."
        ],
        alt_cities=[("Ceuta","ceuta"),("Málaga","malaga")],
        perspectiva="Melilla ofrece la combinación inusual de yield 6,5% bruto con gastos de compra mínimos por el régimen IPSI — la rentabilidad neta puede acercarse al 5,5%, muy por encima de plazas peninsulares similares. El inquilino institucional (funcionario, militar) elimina prácticamente el riesgo de impago. Los caveats son liquidez (mercado pequeño) y el componente geopolítico. Tesis: piso bien ubicado en Centro o Real para alquiler de larga duración a personal del Estado.",
        nearest=[("Ceuta","ceuta","1.500€"),("Málaga","malaga","2.800€"),("Almería","almeria","1.380€")],
    ),
    dict(
        slug="valdemoro",
        name="Valdemoro",
        ccaa="C. de Madrid",
        ccaa_slug="madrid",
        prov="Madrid",
        pop=85972,
        twin="arganda-del-rey",
        precio=2100, alq=950, roi=5.4, vp=6.5, va=10.0, dias=19,
        itp_pct=6, itp_label="C. de Madrid",
        region="centro",
        tags=["Polo logístico A-4", "Corredor sur", "Cercanías C-3", "Crecimiento demográfico"],
        editorial=[
            "Valdemoro es uno de los principales polos logísticos del sur de Madrid, vertebrado por la <strong>A-4</strong> y la línea <strong>Cercanías C-3</strong>. La instalación de grandes operadores logísticos — almacén central de Carrefour, plataforma de Amazon, polígonos de El Caño y La Postura — ha generado en la última década un fuerte tirón de empleo cualificado y semicualificado, que se ha traducido en una demanda residencial sostenida. A <strong>2.100€/m²</strong> y con un yield del <strong>5,4%</strong>, Valdemoro ofrece una rentabilidad razonable para una ciudad con muy buena conectividad a Madrid central (35 minutos en cercanías).",
            "El inquilino tipo es profesional de logística, técnico de almacén, parejas jóvenes que trabajan en Madrid pero buscan precio más asequible y familias del segmento medio que valoran tener vivienda nueva en proyectos como El Restón. El alquiler medio se sitúa en <strong>950€/mes</strong> y los <strong>19 días</strong> de tiempo medio de venta indican un mercado muy activo. Las mejores zonas para inversión son <strong>El Restón, Centro y La Postura</strong> — esta última con presencia de promoción residencial nueva muy demandada.",
            "ITP Comunidad de Madrid: <strong>6%</strong>, uno de los más bajos de España. No hay zonas tensionadas declaradas en Valdemoro y la regulación es la estatal genérica. Los riesgos principales son sensibilidad cíclica a la actividad logística (si Amazon o Carrefour redimensionan, hay impacto local) y la competencia creciente con municipios próximos como Pinto o Ciempozuelos que también se posicionan como receptores del crecimiento sur."
        ],
        alt_cities=[("Pinto","pinto"),("Aranjuez","aranjuez")],
        perspectiva="Valdemoro funciona como polo logístico del eje A-4, una de las áreas con más empleo industrial-terciario creado en la última década en Madrid. La tesis es piso de 2-3 dormitorios cerca de Cercanías o el centro para alquiler a profesionales del polo logístico y parejas jóvenes que trabajan en Madrid capital. Yield 5,4% combinado con ITP Madrid del 6% (uno de los más bajos del país) deja un perfil neto muy competitivo.",
        nearest=[("Pinto","pinto","2.100€"),("Aranjuez","aranjuez","1.800€"),("Parla","parla","1.750€"),("Arganda del Rey","arganda-del-rey","2.000€")],
    ),
    dict(
        slug="ceuta",
        name="Ceuta",
        ccaa="Ceuta",
        ccaa_slug="andalucia",
        prov="Ceuta",
        pop=83595,
        twin="cadiz",
        precio=1500, alq=780, roi=6.2, vp=4.5, va=6.0, dias=30,
        itp_pct=0.5, itp_label="Ceuta (IPSI)",
        region="andalucia",
        tags=["Ciudad autónoma", "Régimen IPSI", "Plaza estratégica", "Frontera con Marruecos"],
        editorial=[
            "Ceuta comparte con Melilla el estatus de ciudad autónoma y un régimen fiscal singular, pero su dinámica económica es algo distinta: más peso del turismo, mayor flujo fronterizo con Marruecos (Tarajal) y presencia militar significativa por su valor geoestratégico en el Estrecho. A <strong>1.500€/m²</strong> y con una rentabilidad bruta del <strong>6,2%</strong>, Ceuta combina precio accesible con yield notable, situándose en la franja alta del ranking nacional de rentabilidad.",
            "La demanda de alquiler procede fundamentalmente de funcionarios estatales, militares, Guardia Civil y personal sanitario destinados a plazas de 2-4 años, complementada por trabajadores ligados a la actividad portuaria y a los servicios fronterizos. Las zonas más demandadas son <strong>Centro, Almadraba y Recinto Sur</strong>, con buena conexión al núcleo administrativo y a los servicios. El alquiler medio se sitúa en <strong>780€/mes</strong> y el mercado tiene una rotación más lenta que en península: <strong>30 días</strong> de tiempo medio de venta.",
            "El régimen fiscal es el principal atractivo: <strong>IPSI del 0,5%</strong> aproximadamente en lugar del ITP autonómico (7-10% en el resto del país), además de una <strong>bonificación del 60% en IRPF</strong> para residentes. Esto reduce los gastos de compra a aproximadamente un 4,5% del precio frente al 11-13% de la mayoría de CCAA. Los riesgos son geopolíticos — la presión migratoria en la frontera y las tensiones diplomáticas periódicas con Marruecos — y de liquidez de salida por el reducido tamaño del mercado."
        ],
        alt_cities=[("Melilla","melilla"),("Algeciras","algeciras")],
        perspectiva="Ceuta combina yield 6,2% bruto con un régimen IPSI que reduce los gastos de compra al 4,5% del precio — la rentabilidad neta resultante es de las más altas del país. El inquilino institucional (funcionarios, militares) aporta solvencia y estabilidad de cobro. La tesis es piso bien situado en Centro o Recinto Sur para alquiler a personal estatal en destinos rotatorios. Los caveats son geopolíticos y de liquidez de salida — no es un mercado para horizontes cortos.",
        nearest=[("Melilla","melilla","1.300€"),("Algeciras","algeciras","1.450€"),("Cádiz","cadiz","2.200€")],
    ),
    dict(
        slug="sant-vicent-del-raspeig",
        name="Sant Vicent del Raspeig",
        ccaa="C. Valenciana",
        ccaa_slug="comunitat-valenciana",
        prov="Alicante",
        pop=60247,
        twin="burjassot",
        precio=1800, alq=870, roi=5.8, vp=7.0, va=10.5, dias=22,
        itp_pct=10, itp_label="C. Valenciana",
        region="levante",
        tags=["Universidad de Alicante", "Demanda estudiantil", "Alquiler por habitación", "Rotación alta"],
        editorial=[
            "Sant Vicent del Raspeig es el municipio universitario por excelencia del área metropolitana de Alicante: alberga el <strong>campus principal de la Universidad de Alicante</strong>, con más de 25.000 estudiantes, sobre una población residente de apenas 60.000 habitantes. Esa densidad universitaria configura un mercado de alquiler muy específico, dominado por el modelo de alquiler por habitaciones y con una rotación anual altísima ligada al calendario académico. A <strong>1.800€/m²</strong> — significativamente más barato que Alicante capital — y con un yield bruto del <strong>5,8%</strong>, ofrece la combinación más atractiva del área metropolitana alicantina para la estrategia estudiantil.",
            "El inquilino tipo es estudiante universitario en grado o máster, complementado por profesorado universitario, personal de servicios y profesionales del polígono industrial Canastell. La demanda es estacional pero predecible: pico fuerte de julio a septiembre, contratos típicos de 9-10 meses y la posibilidad de operar a coste por habitación que multiplica el yield del piso compartido. Las mejores zonas son <strong>Universidad, Centre i Santa Isabel</strong>, todas dentro de un radio de 1 km del campus. El alquiler medio para piso completo se sitúa en <strong>870€/mes</strong> y <strong>22 días</strong> de absorción.",
            "ITP Comunidad Valenciana: <strong>10%</strong>, uno de los más altos del país. Verificar si la ubicación cae en zona tensionada declarada (la Comunitat ha avanzado en la implementación del índice). El principal riesgo es la dependencia del calendario universitario: meses de bajada estival si no se gestiona bien y rotación de inquilinos que puede aumentar costes de mantenimiento. Compensa con yield estructuralmente alto si se opera con la estrategia adecuada."
        ],
        alt_cities=[("Alicante","alicante"),("Elche","elche")],
        perspectiva="Sant Vicent del Raspeig vive y respira del campus de la Universidad de Alicante. La tesis ganadora es piso de 3-4 habitaciones a menos de 1 km de campus para alquiler por habitación a estudiantes — el yield efectivo de esa estrategia supera con holgura el 7-8% bruto frente al 5,8% del alquiler convencional. Requiere gestión activa y aceptar la estacionalidad veraniega, pero la previsibilidad del calendario académico convierte la rotación en algo medible y planificable.",
        nearest=[("Alicante","alicante","2.300€"),("Elche","elche","1.500€"),("Mutxamel","mutxamel","1.700€")],
    ),
    dict(
        slug="colmenar-viejo",
        name="Colmenar Viejo",
        ccaa="C. de Madrid",
        ccaa_slug="madrid",
        prov="Madrid",
        pop=58730,
        twin="tres-cantos",
        precio=2400, alq=1050, roi=5.2, vp=6.0, va=9.5, dias=19,
        itp_pct=6, itp_label="C. de Madrid",
        region="centro",
        tags=["Norte Madrid", "Sierra de Guadarrama", "Cercanías C-4", "Familias clase media-alta"],
        editorial=[
            "Colmenar Viejo es uno de los grandes suburbios del norte de Madrid, ubicado en la falda sur de la <strong>Sierra de Guadarrama</strong> y conectado con la capital por la <strong>A-1, M-607 y Cercanías C-4</strong>. La ciudad se ha posicionado en la última década como destino preferente de familias de clase media-alta que buscan huir del precio y la densidad del núcleo central manteniendo conectividad razonable (35-45 minutos a Plaza de Castilla). A <strong>2.400€/m²</strong> y con un yield bruto del <strong>5,2%</strong>, Colmenar Viejo es un mercado equilibrado: yield discreto pero compensado por una revalorización sostenida.",
            "El inquilino tipo es familia joven con hijos, profesional sénior con teletrabajo parcial, y trabajador del polo terciario norte de Madrid (Alcobendas-San Sebastián de los Reyes-Tres Cantos). Las preferencias residenciales se orientan a chalet adosado, dúplex y piso amplio (3-4 dormitorios) con preferencia por barrios como <strong>Centro, La Estación y Adelfillas</strong>, con buena dotación de colegios e infraestructura deportiva. El alquiler medio para piso estándar se sitúa en <strong>1.050€/mes</strong> y los <strong>19 días</strong> de tiempo medio de venta confirman un mercado activo.",
            "ITP Comunidad de Madrid: <strong>6%</strong>, de los más bajos. Sin zonas tensionadas declaradas. La principal ventaja para el inversor es la estabilidad: inquilinos de larga duración (típicamente 3-5 años), tasas de impago bajas y revalorización constante apoyada por la presión residencial del norte de Madrid. El riesgo principal es la dependencia del coche para muchos desplazamientos diarios y la sensibilidad a tipos de interés (perfil de familia hipotecada)."
        ],
        alt_cities=[("Tres Cantos","tres-cantos"),("Alcobendas","alcobendas")],
        perspectiva="Colmenar Viejo es la opción 'familiar' clásica del norte de Madrid: huida del centro buscando calidad de vida en la falda de la Sierra de Guadarrama, manteniendo conectividad por A-1 y Cercanías C-4. La tesis es piso amplio o dúplex de 3-4 dormitorios para alquiler familiar de larga duración. Yield discreto (5,2%) pero compensado por estabilidad, baja vacancia y una revalorización apoyada por la presión demográfica del eje norte madrileño.",
        nearest=[("Tres Cantos","tres-cantos","3.200€"),("Alcobendas","alcobendas","3.500€"),("San Sebastián de los Reyes","san-sebastian-de-los-reyes","3.200€"),("Collado Villalba","collado-villalba","2.200€")],
    ),
    dict(
        slug="vila-real",
        name="Vila-real",
        ccaa="C. Valenciana",
        ccaa_slug="comunitat-valenciana",
        prov="Castellón",
        pop=53623,
        twin="burriana",
        precio=1200, alq=600, roi=6.0, vp=5.5, va=7.5, dias=25,
        itp_pct=10, itp_label="C. Valenciana",
        region="levante",
        tags=["Capital cerámica mundial", "Empleo industrial", "Villarreal CF", "Yield estable"],
        editorial=[
            "Vila-real es, junto con Castellón y los municipios del área de l'Alcalatén, el corazón mundial de la <strong>industria cerámica</strong>: más del 80% de la producción española de azulejo, gres porcelánico y pavimento cerámico se concentra en este cinturón industrial. La ciudad alberga sedes de gigantes como Porcelanosa, Pamesa y Keraben, y un tejido denso de empresas auxiliares (atomizadoras, esmaltes, maquinaria). Esa especialización industrial sostiene una demanda residencial muy estable basada en empleo cualificado y semicualificado del sector. A <strong>1.200€/m²</strong> y con un yield bruto del <strong>6,0%</strong>, Vila-real ofrece la rentabilidad más sólida del área metropolitana castellonense.",
            "El inquilino tipo es trabajador del polígono industrial, técnico cualificado del sector cerámico, parejas jóvenes locales y profesionales ligados a la industria auxiliar. La <strong>proyección internacional del Villarreal CF</strong> aporta además un componente menor pero recurrente de inquilinos foráneos vinculados al fútbol profesional. Las mejores zonas son <strong>Centre, Madrigal i Pius XII</strong>, con buena dotación de servicios y conexión por carretera y ferrocarril a Castellón. Alquiler medio: <strong>600€/mes</strong>; tiempo medio de venta: <strong>25 días</strong>.",
            "ITP Comunidad Valenciana: <strong>10%</strong> — el principal coste fiscal a considerar. No hay zonas tensionadas declaradas específicamente en Vila-real, aunque la Comunitat avanza en la implementación del índice. El principal riesgo es la concentración sectorial: si el ciclo cerámico se deteriora (caída exportación, encarecimiento energético), el impacto residencial es inmediato. Compensa con precio muy bajo, yield sólido y una demanda estructural ligada a un sector con liderazgo mundial."
        ],
        alt_cities=[("Castellón","castellon"),("Burriana","burriana")],
        perspectiva="Vila-real es una jugada industrial pura: la ciudad vive de la cerámica y la cerámica de la ciudad. Mientras el sector mantenga competitividad global (Porcelanosa, Pamesa, Keraben), la demanda residencial está garantizada. La tesis es piso de 2-3 dormitorios en zona centro o Madrigal para alquiler a profesionales del sector. Precio de entrada muy bajo (1.200€/m²) más yield sostenido del 6% genera un perfil de rentabilidad neta muy competitivo, con la cautela del riesgo sectorial.",
        nearest=[("Castellón","castellon","1.500€"),("Burriana","burriana","1.300€"),("Onda","onda","1.100€")],
    ),
]


# ---------------------------------------------------------------------------
# Datos exactos de cada twin (extraidos del HTML real)
# ---------------------------------------------------------------------------
TWINS = {
    "l-hospitalet-de-llobregat": dict(
        name="L'Hospitalet de Llobregat", name_url="l-hospitalet-de-llobregat",
        ccaa="Cataluña", ccaa_slug="cataluna",
        precio=3400, alq=1500, roi=5.3, vp=8.0, va=7.2, dias=20,
        itp_pct=10, itp_label="Cataluña",
    ),
    "burjassot": dict(
        name="Burjassot", name_url="burjassot",
        ccaa="C. Valenciana", ccaa_slug="comunitat-valenciana",
        precio=2100, alq=960, roi=5.5, vp=10.0, va=9.0, dias=21,
        itp_pct=10, itp_label="C. Valenciana",
    ),
    "burriana": dict(
        name="Burriana", name_url="burriana",
        ccaa="C. Valenciana", ccaa_slug="comunitat-valenciana",
        precio=1500, alq=1400, roi=6.0, vp=8.0, va=9.9, dias=24,
        itp_pct=10, itp_label="C. Valenciana",
    ),
    "arganda-del-rey": dict(
        name="Arganda del Rey", name_url="arganda-del-rey",
        ccaa="C. de Madrid", ccaa_slug="madrid",
        precio=2000, alq=900, roi=5.4, vp=11.0, va=9.9, dias=20,
        itp_pct=6, itp_label="C. de Madrid",
    ),
    "tres-cantos": dict(
        name="Tres Cantos", name_url="tres-cantos",
        ccaa="C. de Madrid", ccaa_slug="madrid",
        precio=3200, alq=1380, roi=6.5, vp=11.0, va=9.9, dias=22,
        itp_pct=6, itp_label="C. de Madrid",
    ),
    "cadiz": dict(
        name="Cádiz", name_url="cadiz",
        ccaa="Andalucía", ccaa_slug="andalucia",
        # cadiz has dual ROI references: 5.5 banner-ish, 4.7 effective
        precio=2200, alq=1000, roi=4.7, vp=9.0, va=8.1, dias=23,
        itp_pct=7, itp_label="Andalucía",
        extra_rois=[5.5],  # additional ROI numbers that appear in cadiz
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    s = f"{n:,}".replace(",", ".")
    return s


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def fmt_pct_en(n):
    return f"{n:.1f}"


def replace_int(html, tw, nv):
    """Reemplaza un valor entero (precio/alquiler) en formatos europeo y plano."""
    if tw == nv:
        return html
    eu_old = fmt_eu(tw)
    eu_new = fmt_eu(nv)
    # Patrones de mayor especificidad primero
    patterns = [
        (eu_old + "€", eu_new + "€"),       # 2.100€
        (eu_old + " €", eu_new + " €"),     # 2.100 € (evo-chart)
        (str(tw) + "€", str(nv) + "€"),     # 2100€
        (str(tw) + " €", str(nv) + " €"),   # 2100 €
        # En contexto de JS de zonas: precio:2100,
        (f"precio:{tw},", f"precio:{nv},"),
        (f"alquiler:{tw},", f"alquiler:{nv},"),
    ]
    for old, new in patterns:
        html = html.replace(old, new)
    return html


def replace_pct(html, tw, nv):
    """Reemplaza un porcentaje (ROI/vp/va) en formato europeo y americano."""
    if abs(tw - nv) < 1e-9:
        return html
    patterns = [
        (fmt_pct(tw) + "%", fmt_pct(nv) + "%"),
        (fmt_pct_en(tw) + "%", fmt_pct_en(nv) + "%"),
    ]
    for old, new in patterns:
        html = html.replace(old, new)
    return html


def replace_city_name(html, twin_name, new_name):
    """Reemplaza el nombre de la ciudad en sus variantes."""
    if twin_name == new_name:
        return html
    html = html.replace(twin_name, new_name)
    if twin_name == "Cádiz":
        html = html.replace("C&#225;diz", new_name)
        html = html.replace("Cadiz", new_name)
    if twin_name == "L'Hospitalet de Llobregat":
        html = html.replace("L&#39;Hospitalet de Llobregat", new_name)
    return html


def build_editorial_html(city):
    stats = (
        f'<div class="ed-stat"><div class="ed-stat-val">{fmt_pct(city["roi"])}%</div><div class="ed-stat-lbl">rentabilidad bruta</div></div>'
        f'<div class="ed-stat"><div class="ed-stat-val">{fmt_eu(city["precio"])}€</div><div class="ed-stat-lbl">precio medio m²</div></div>'
        f'<div class="ed-stat"><div class="ed-stat-val">+{fmt_pct(city["vp"])}%</div><div class="ed-stat-lbl">subida precio anual</div></div>'
        f'<div class="ed-stat"><div class="ed-stat-val">{city["dias"]}</div><div class="ed-stat-lbl">días media venta</div></div>'
    )
    paragraphs = "\n      ".join(f"<p>{p}</p>" for p in city["editorial"])
    tags = "".join(f'<span class="ed-tag">{t}</span>' for t in city["tags"])
    alts = " · ".join(
        f'<a href="/rentabilidad-{slug}.html" style="color:var(--blue);text-decoration:none;font-weight:600">{name}</a>'
        for name, slug in city["alt_cities"]
    )
    return f"""<div class="ed-body">
      <div class="ed-highlight">
        {stats}
      </div>
      {paragraphs}
      <p>{tags}</p>
      <p style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border);font-size:.85rem"><strong>Ciudades alternativas:</strong> {alts}</p>
    </div>"""


def replace_ed_body(html, city):
    """Sustituye el bloque <div class="ed-body">...</div> (hasta el </div> que
    lo cierra) con el nuevo contenido."""
    start_marker = '<div class="ed-body">'
    si = html.find(start_marker)
    if si == -1:
        return html

    # Avanza balanceando divs anidados desde el inicio del ed-body
    pos = si
    depth = 0
    while pos < len(html):
        next_open = html.find("<div", pos)
        next_close = html.find("</div>", pos)
        if next_close == -1:
            return html
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                end = pos  # justo despues del </div> que cierra ed-body
                break
    else:
        return html

    new_body = build_editorial_html(city)
    return html[:si] + new_body + html[end:]


def replace_perspectiva(html, city):
    new_p = f'<div class="tend-perspectiva">💡 <strong>Perspectiva Ren Data:</strong> {city["perspectiva"]}</div>'
    return re.sub(
        r'<div class="tend-perspectiva">.*?</div>',
        new_p,
        html,
        count=1,
        flags=re.DOTALL,
    )


def replace_sim_section(html, city):
    """Reemplaza el bloque <div class="sim-grid">...</div> con div-balancing."""
    nearest = city["nearest"]
    if not nearest:
        return html
    start_marker = '<div class="sim-grid">'
    si = html.find(start_marker)
    if si == -1:
        return html
    pos = si
    depth = 0
    end = -1
    while pos < len(html):
        next_open = html.find("<div", pos)
        next_close = html.find("</div>", pos)
        if next_close == -1:
            return html
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                end = pos
                break
    if end == -1:
        return html
    cards = []
    for name, slug, price in nearest[:4]:
        cards.append(
            f'      <a href="/rentabilidad-{slug}.html" class="sim-card">\n'
            f'        <div class="sim-name">{name}</div>\n'
            f'        <div class="sim-cc">{city["ccaa"]}</div>\n'
            f'        <div class="sim-roi">Precio {price}/m²</div>\n'
            f'        <div class="sim-price">Cercano</div>\n'
            f'      </a>'
        )
    new_grid = '<div class="sim-grid">\n' + "\n".join(cards) + "\n    </div>"
    return html[:si] + new_grid + html[end:]


def replace_banner_img(html, slug):
    return re.sub(
        r'(<img class="banner-img" src=")img/[^"]+\.webp(")',
        rf'\1img/{slug}.webp\2',
        html,
        count=1,
    )


def update_alt_text(html, twin_name, new_name):
    if twin_name == new_name:
        return html
    return html.replace(f"Foto de {twin_name}", f"Foto de {new_name}")


def apply_ipsi_overrides(html, city):
    """Sustituciones IPSI para Ceuta/Melilla."""
    # En meta description / og: 'ITP 7% en Andalucia' -> 'IPSI 0,5% en {city}'
    html = re.sub(
        r'ITP 7% en Andalucía',
        f'IPSI 0,5% en {city["name"]}',
        html,
    )
    subs = [
        ("ITP al comprar en Andalucía", f"IPSI al comprar en {city['name']}"),
        ('<span class="itp-chip itp-chip-med">Andalucía 7%</span>',
         f'<span class="itp-chip itp-chip-low">{city["name"]} 0,5%</span>'),
        ("ITP Andalucía: 7%", f"IPSI {city['name']}: 0,5%"),
        ("ITP Andalucía 7%", f"IPSI {city['name']} 0,5%"),
        ("ITP en Andalucía 7%", f"IPSI en {city['name']} 0,5%"),
        ("ITP del 7%", "IPSI del 0,5%"),
        ("ITP 7%", "IPSI 0,5%"),
        ("ITP: 7%", "IPSI: 0,5%"),
        ("7% ITP", "0,5% IPSI"),
        # The twin (cadiz) was replaced city name -> twin's references "ITP Andalucia" stayed
        # but also "ITP {city['name']}" appearances exist where city_name replaced "Andalucia".
        # We handle those too:
        (f"ITP {city['name']}: 7%", f"IPSI {city['name']}: 0,5%"),
        (f"ITP {city['name']} 7%", f"IPSI {city['name']} 0,5%"),
        (f"ITP en {city['name']} 7%", f"IPSI en {city['name']} 0,5%"),
        (f"ITP ({city['name']}): 7%", f"IPSI ({city['name']}): 0,5%"),
        ("ITP Andalucía", f"IPSI {city['name']}"),
        (f"ITP {city['name']}", f"IPSI {city['name']}"),
    ]
    for old, new in subs:
        html = html.replace(old, new)

    # itp-badge itp-high -> itp-low + label
    html = re.sub(
        r'<span class="itp-badge itp-high">[^<]+</span>',
        '<span class="itp-badge itp-low">Mínimo</span>',
        html,
    )

    # itp-val: el valor numerico de la card (era '7' del twin cadiz)
    html = re.sub(
        r'<div class="itp-val">\d+(?:\.\d+)?<span class="itp-pct">%</span></div>',
        '<div class="itp-val">0,5<span class="itp-pct">%</span></div>',
        html,
        count=1,
    )

    # "Para un piso de 171.600 pagaras 12.012 de ITP" -> recalculo IPSI 0.5%
    precio_piso = city["precio"] * 78
    ipsi_amount = int(round(precio_piso * 0.005))
    html = re.sub(
        r'<div class="itp-desc">Para un piso de [\d\.]+€ pagarás <strong>[\d\.]+€ de (?:ITP|IPSI)</strong></div>',
        f'<div class="itp-desc">Para un piso de {fmt_eu(precio_piso)}€ pagarás <strong>{fmt_eu(ipsi_amount)}€ de IPSI</strong></div>',
        html,
    )

    # Gastos compra (~12%) o (~9%) o (~11%) -> (~4,5%)
    html = re.sub(
        r'Gastos compra \(~\d+(?:,\d+)?%\)',
        'Gastos compra (~4,5%)',
        html,
    )
    # En el JS calc hipoteca: precio*0.12 -> precio*0.045
    html = re.sub(
        r'precio\*0\.(?:09|11|12)',
        'precio*0.045',
        html,
    )

    # gr-item ITP/IPSI label (la sustitucion textual anterior ya pudo cambiar
    # 'ITP Andalucia' -> 'IPSI Melilla' dejando '7%' intacto)
    html = re.sub(
        r'<div class="gr-item"><div class="gr-label">(?:ITP|IPSI) [^<]+</div><div class="gr-val">\d+%</div></div>',
        f'<div class="gr-item"><div class="gr-label">IPSI {city["name"]}</div><div class="gr-val">0,5%</div></div>',
        html,
        count=1,
    )
    # Total gastos est. (recalculado para 4.5%)
    nuevo_total = int(round(precio_piso * 0.045))
    html = re.sub(
        r'(<div class="gr-item"><div class="gr-label">Total gastos est\.</div><div class="gr-val">)[\d\.]+€(</div></div>)',
        rf'\g<1>{fmt_eu(nuevo_total)}€\g<2>',
        html,
        count=1,
    )

    # coll-trigger-sub: "Proceso legal · ITP Andalucia 7% · Gastos totales est. X"
    html = re.sub(
        r'<span class="coll-trigger-sub">Proceso legal · (?:ITP|IPSI) [^·]+ · Gastos totales est\. [\d\.]+€</span>',
        f'<span class="coll-trigger-sub">Proceso legal · IPSI {city["name"]} 0,5% · Gastos totales est. {fmt_eu(nuevo_total)}€</span>',
        html,
        count=1,
    )

    # Paso 1: "Reserva XXX€ para gastos de compra"
    html = re.sub(
        r'(Reserva )[\d\.]+€( para gastos de compra)',
        rf'\g<1>{fmt_eu(nuevo_total)}€\g<2>',
        html,
        count=1,
    )

    # Paso 6: ITP Andalucia 7% del precio = 12.012 -> IPSI Ceuta 0,5% del precio = X
    ipsi_paso6 = int(round(precio_piso * 0.005))
    html = re.sub(
        r'<span>(?:ITP|IPSI) \([^\)]+\): \d+% del precio = [\d\.]+€</span>',
        f'<span>IPSI ({city["name"]}): 0,5% del precio = {fmt_eu(ipsi_paso6)}€</span>',
        html,
        count=1,
    )

    # reg-card: regulacion fiscal especial
    reg_special = f'''<div class="reg-card" style="border-color:#05966920">
  <div class="reg-header" style="background:#ecfdf5;border-bottom:1px solid #05966922">
    <div><div class="reg-badge" style="background:#059669;color:#fff">BAJO</div><div class="reg-title">Régimen fiscal singular</div></div>
    <div class="reg-icon">✅</div>
  </div>
  <p class="reg-desc">{city["name"]} es ciudad autónoma con régimen fiscal IPSI (no ITP), sin zonas tensionadas declaradas y bonificación del 60% en IRPF para residentes.</p>
  <div class="reg-list">
    <div class="reg-item">✅ IPSI 0,5% en transmisiones (vs ITP 7-10% peninsular)</div><div class="reg-item">✅ Bonificación del 60% IRPF para residentes</div><div class="reg-item">✅ Sin zonas tensionadas declaradas</div><div class="reg-item">ℹ️ Régimen económico-fiscal de ciudad autónoma</div>
  </div>
</div>'''
    html = re.sub(
        r'<div class="reg-card" style="border-color:#05966920">.*?</div>\s*</div>',
        reg_special,
        html,
        count=1,
        flags=re.DOTALL,
    )

    # Aviso legal estimaciones
    html = re.sub(
        r'⚠️ Estimaciones basadas en precio medio de [^.]+\. (?:ITP|IPSI) [^.]+\.',
        f'⚠️ Estimaciones basadas en precio medio de {city["name"]}. IPSI {city["name"]}: 0,5% (no ITP).',
        html,
    )

    # FAQ impuestos
    ipsi_faq = (
        f'Al comprar una vivienda en {city["name"]} pagarás <strong>IPSI</strong> '
        f'(Impuesto sobre la Producción, los Servicios y la Importación) en lugar '
        f'de ITP. El tipo aplicable a transmisiones inmobiliarias es '
        f'aproximadamente <strong>0,5%</strong> del precio, mucho menor que el ITP '
        f'autonómico peninsular (7-10%). A esto se suman notaría y registro (~1%). '
        f'Los gastos totales de compra rondan el <strong>4,5%</strong>. Además, '
        f'{city["name"]} aplica una <strong>bonificación del 60% en IRPF</strong> '
        f'a residentes, lo que mejora aún más la rentabilidad neta.'
    )
    html = re.sub(
        r'(<div class="faq-a" id="fa-body-7">)[^<]+(</div>)',
        rf'\1{ipsi_faq}\2',
        html,
    )

    # Breadcrumb JSON-LD: position 2 name Andalucia -> nombre ciudad autonoma
    html = re.sub(
        r'(\{"@type":"ListItem","position":2,"name":")Andalucía(","item":"https://rendata\.es/ccaa-andalucia\.html"\})',
        rf'\1{city["name"]}\2',
        html,
    )
    # Breadcrumb visible
    html = re.sub(
        r'(<a href="ccaa-andalucia\.html">)Andalucía(</a>)',
        rf'\g<1>{city["name"]}\g<2>',
        html,
    )

    return html


def generate(city):
    twin_key = city["twin"]
    twin = TWINS[twin_key]
    src = BETA / f"rentabilidad-{twin['name_url']}.html"
    html = src.read_text(encoding="utf-8")

    is_autonoma = city["ccaa"] in ("Ceuta", "Melilla")

    # 1) Numeros: floats antes que ints (porcentajes son patrones mas largos)
    html = replace_pct(html, twin["roi"], city["roi"])
    # ROIs extra que aparecen en el twin (ej. cadiz tiene 5.5 y 4.7)
    for extra_roi in twin.get("extra_rois", []):
        html = replace_pct(html, extra_roi, city["roi"])
    html = replace_pct(html, twin["vp"], city["vp"])
    html = replace_pct(html, twin["va"], city["va"])
    html = replace_int(html, twin["precio"], city["precio"])
    html = replace_int(html, twin["alq"], city["alq"])

    # 2) Dias
    if twin["dias"] != city["dias"]:
        html = html.replace(f"{twin['dias']} días", f"{city['dias']} días")
        # En sticky-bar: <span class="sb-val">21</span>
        html = re.sub(
            rf'(<span class="sb-val">){twin["dias"]}(</span>)',
            rf'\g<1>{city["dias"]}\g<2>',
            html,
        )
        # En icard <div class="ival">21</div>
        html = re.sub(
            rf'(<div class="ival">){twin["dias"]}(</div>)',
            rf'\g<1>{city["dias"]}\g<2>',
            html,
        )

    # 3) ITP (si no es ciudad autonoma)
    if not is_autonoma and twin["itp_pct"] != city["itp_pct"]:
        # Reemplaza el numero seguido de % SOLO en contexto ITP
        # Por seguridad: usamos varias formas concretas
        html = re.sub(
            rf'(<div class="itp-val">){twin["itp_pct"]}(<span class="itp-pct">%</span></div>)',
            rf'\g<1>{city["itp_pct"]}\g<2>',
            html,
        )
        html = html.replace(f"{twin['itp_pct']}% del precio",
                            f"{city['itp_pct']}% del precio")
        html = html.replace(f"ITP {twin['ccaa']}: {twin['itp_pct']}%",
                            f"ITP {city['ccaa']}: {city['itp_pct']}%")
        html = html.replace(f"ITP {twin['ccaa']} {twin['itp_pct']}%",
                            f"ITP {city['ccaa']} {city['itp_pct']}%")
        html = html.replace(f"ITP en {twin['ccaa']}: {twin['itp_pct']}%",
                            f"ITP en {city['ccaa']}: {city['itp_pct']}%")
        # Comparativa de ITP en chips: substituye el del twin solo si difiere
        if city["ccaa"] != twin["ccaa"]:
            html = html.replace(f">{twin['ccaa']} {twin['itp_pct']}%<",
                                f">{city['ccaa']} {city['itp_pct']}%<")

    # 4) Nombre de ciudad
    html = replace_city_name(html, twin["name"], city["name"])

    # 5) CCAA visible (texto)
    if not is_autonoma:
        # Sustituye CCAA y enlaces ccaa-*.html
        if twin["ccaa"] != city["ccaa"]:
            html = html.replace(twin["ccaa"], city["ccaa"])
        if twin["ccaa_slug"] != city["ccaa_slug"]:
            html = re.sub(
                rf'ccaa-{re.escape(twin["ccaa_slug"])}\.html',
                f'ccaa-{city["ccaa_slug"]}.html',
                html,
            )
    else:
        # Para Ceuta/Melilla: sustituye texto Andalucia -> nombre ciudad autonoma
        # pero conserva enlaces a ccaa-andalucia.html (no creamos pagina CCAA).
        # Substitucion solo de texto "Andalucia" no precedido por ccaa-
        # Hacemos sustitucion de texto visible explicitamente despues
        # via apply_ipsi_overrides (breadcrumb visible y JSON-LD)
        # Tambien substituye otras menciones visibles de Andalucia que no sean URL
        # Cuidado: en el <head> y nav-flag references a Andalucia debemos preservar.
        # Estrategia: sustituye Andalucia solo dentro de bloques especificos:
        # spatialCoverage, Mercado inmobiliario X 2026 description...
        html = re.sub(
            r'(spatialCoverage":"[^"]+, )Andalucía(, España")',
            rf'\1{city["name"]}\2',
            html,
        )
        html = re.sub(
            r'(en [^,]+, )Andalucía(\.")',
            rf'\1{city["name"]}\2',
            html,
        )
        # itp-card label
        html = html.replace(
            "ITP al comprar en Andalucía",
            f"IPSI al comprar en {city['name']}",
        )

    # 6) Slug del twin -> slug nuevo en URLs
    html = re.sub(
        rf'rentabilidad-{re.escape(twin["name_url"])}\.html',
        f'rentabilidad-{city["slug"]}.html',
        html,
    )

    # 7) Banner img + alt
    html = replace_banner_img(html, city["slug"])
    html = update_alt_text(html, twin["name"], city["name"])

    # 8) Editorial body
    html = replace_ed_body(html, city)

    # 9) Perspectiva
    html = replace_perspectiva(html, city)

    # 10) Sim-grid
    html = replace_sim_section(html, city)

    # 11) IPSI overrides para Ceuta/Melilla
    if is_autonoma:
        html = apply_ipsi_overrides(html, city)

    # 12) Banner sub
    html = re.sub(
        r'(<div class="banner-sub">)[^<]+(</div>)',
        rf'\1{city["ccaa"]} · Análisis de inversión inmobiliaria · Mayo 2026\2',
        html,
        count=1,
    )

    # 12b) Limpiar el array zones=[...] de JS si contenia datos del twin
    html = re.sub(
        r'const zones=\[\s*\{.*?\}\s*\];',
        'const zones=[];',
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 13) Recalcular numeros derivados: precio*78 (piso tipico)
    precio_piso = city["precio"] * 78
    # precio * 100 (FAQ "Un piso de 100 m² costaría aproximadamente XXX")
    precio_100 = city["precio"] * 100
    twin_100 = twin["precio"] * 100
    if twin_100 != precio_100:
        # Solo dentro del texto "costaría aproximadamente X€" para evitar colisiones
        html = re.sub(
            rf'(piso de 100 m² costaría aproximadamente ){fmt_eu(twin_100)}€',
            rf'\g<1>{fmt_eu(precio_100)}€',
            html,
        )
    # 'Precio est: 171.600€' / 'precio est: <NEW>€'
    html = re.sub(
        r'(<div class="dato-sub" style="margin-top:.15rem">Precio est: )[\d\.]+€(</div>)',
        rf'\g<1>{fmt_eu(precio_piso)}€\g<2>',
        html,
        count=1,
    )
    # 'Para un inmueble de XXX€ necesitarias una entrada de YY€'
    entrada = int(round(precio_piso * 0.20))
    html = re.sub(
        r'Para un inmueble de [\d\.]+€ necesitarías una entrada de <strong>[\d\.]+€</strong>',
        f'Para un inmueble de {fmt_eu(precio_piso)}€ necesitarías una entrada de <strong>{fmt_eu(entrada)}€</strong>',
        html,
        count=1,
    )
    # 'Para un piso medio de 78 m2 en X necesitaras aproximadamente <strong>YY</strong>'
    # Total gastos: precio_piso * 1.11 (o 1.045 si IPSI), pero ya se actualizo en IPSI overrides
    if not is_autonoma:
        total_inversion = int(round(precio_piso * 1.11))
        html = re.sub(
            r'(Para un piso medio de 78 m² en )[^ ]+( necesitarás aproximadamente <strong>)[\d\.]+€(</strong>)',
            rf'\g<1>{city["name"]}\g<2>{fmt_eu(total_inversion)}€\g<3>',
            html,
            count=1,
        )

    return html


def main():
    results = []
    for city in CITIES:
        try:
            html = generate(city)
            out_path = BETA / f"rentabilidad-{city['slug']}.html"
            out_path.write_text(html, encoding="utf-8")
            lines = html.count("\n") + 1
            results.append(f"[ok] {city['slug']}: {lines} líneas")
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append(f"[ERROR] {city['slug']}: {e}")
    print("\n".join(results))


if __name__ == "__main__":
    main()
