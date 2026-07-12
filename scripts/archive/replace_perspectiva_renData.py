"""
Reemplaza el div .tend-perspectiva en los 329 HTML con 12 variantes nuevas
segmentadas por arquetipo de ciudad. Clasificación con listas curadas + heurísticas.
"""
import re, glob, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "rendata_beta"

# ============ 12 PLANTILLAS (placeholder {C} = nombre ciudad) ============

PLANTILLAS = {
    "costera_turistica":
        "{C} es una plaza costera con marca turística consolidada: la combinación de demanda nacional, residentes europeos y oferta limitada por suelo costero protegido sostiene tanto el alquiler estacional como la apreciación. La estrategia ganadora pasa por VUT registrada con licencia para capturar tarifas premium estivales y residencial en temporada baja, con horizonte de revalorización a 5-7 años.",

    "capital_provincial":
        "Como capital de provincia, {C} concentra demanda institucional (administración, universidad, sanidad), demografía estable y un mercado de alquiler estructural inelástico al ciclo. Para inversores que priorizan estabilidad sobre yield máximo, ofrece un equilibrio difícil de replicar: tickets razonables, demanda inelástica y revalorización moderada pero sostenida.",

    "suburbio_metropolitano":
        "{C} se beneficia del spillover residencial de su área metropolitana: familias y profesionales que prefieren huir del precio del núcleo central pero mantener conectividad. La tesis es clara — piso de 2-3 dormitorios bien conectado por cercanías o metro para alquiler familiar largo plazo, con apreciación apoyada en presión demográfica metropolitana.",

    "ciudad_industrial":
        "{C} mantiene un tejido industrial estructural que sostiene la demanda de alquiler residencial con baja sensibilidad cíclica. Para el inversor con perfil rentista, la combinación de empleo estable, tickets accesibles y rotación previsible de inquilinos configura una plaza de cash-flow consistente, con menor exposición a shocks turísticos o financieros.",

    "ciudad_universitaria":
        "{C} cuenta con una población universitaria estructural que renueva la demanda cada curso académico, generando una rotación previsible y rentabilidades superiores al residencial estándar mediante alquiler por habitaciones o contratos cortos. La tesis óptima pasa por pisos de 3-4 dormitorios próximos al campus, segmentados al alquiler estudiantil con yield premium.",

    "rural_despoblacion":
        "{C} se sitúa en una zona con menor presión demográfica donde los tickets de entrada son extremadamente bajos pero la liquidez puede exigir paciencia. Plaza recomendada para inversor rentista con horizonte largo (8-10 años), enfocado en cash-flow porcentual alto sobre demanda local estable, sin esperar revalorización significativa.",

    "isla":
        "El mercado insular de {C} opera con dinámica propia: oferta de suelo limitada por el carácter geográfico, demanda turística internacional con estacionalidad invertida y una comunidad europea residente estructural. La clave inversora está en la regulación de la VUT — donde existe licencia, los yields combinados superan ampliamente al residencial puro, con apreciación apoyada en la escasez de oferta nueva.",

    "historica_patrimonio":
        "{C} conserva un patrimonio histórico que actúa como activo turístico-cultural diferenciador, abriendo nichos específicos (VUT cultural, alquiler a investigadores y profesionales del patrimonio). El casco histórico suele estar regulado, lo que limita la oferta y protege la apreciación. Tesis dual: vivienda con encanto en zona protegida + residencial estable en barrios contiguos.",

    "polo_logistico":
        "{C} actúa como nodo logístico con empleo estructural en transporte, almacenaje y distribución — sectores con crecimiento estructural y baja sensibilidad al ciclo económico. La demanda de alquiler residencial es inelástica y diversificada (operarios, técnicos, transportistas), lo que reduce el riesgo de concentración. Tesis: piso funcional próximo a polígonos para alquiler residencial estable.",

    "ciudad_dormitorio":
        "{C} funciona como ciudad-dormitorio del núcleo metropolitano cercano: la mayoría de sus residentes trabajan fuera y vuelven a dormir y vivir. Esto configura un mercado de alquiler de renovación predecible y demanda inelástica. La conexión por cercanías o autovía es el factor crítico — pisos próximos a la estación capturan el yield más estable.",

    "zona_tensionada":
        "{C} es un mercado tensionado donde la demanda supera estructuralmente a la oferta y los días medios de venta son los más bajos del entorno. La rentabilidad bruta queda por debajo de la media nacional pero la apreciación a 5-7 años compensa: inversor con horizonte patrimonialista que prioriza preservación de capital y revalorización sobre yield puro encuentra aquí su plaza natural.",

    "media_equilibrada":
        "{C} ofrece un perfil equilibrado para invertir: precio medio razonable, rentabilidad bruta en línea con la media nacional y demanda local estable apoyada en una economía diversificada. Es una plaza idónea para construir cartera diversificada sin asumir extremos de yield ni de coste de entrada — el inversor obtiene cash-flow predecible y revalorización moderada con baja volatilidad.",
}

# ============ LISTAS CURADAS POR ARQUETIPO ============

# Histórica / patrimonio (UNESCO o patrimonio destacado, prevalece sobre capital)
HISTORICA = {
    "toledo","segovia","cuenca","salamanca","caceres","tarragona","merida","avila",
    "baeza","ubeda","aranjuez","san-lorenzo-de-el-escorial","carmona","zafra",
    "ciudad-rodrigo","trujillo","plasencia","coria","sigüenza","siguenza",
    "alcala-de-henares","santiago-de-compostela","santillana-del-mar",
    "ronda","priego-de-cordoba","alcala-la-real","osuna","ecija","la-orotava",
    "tossa-de-mar","palma","gernika-lumo","besalu","banyoles","olot","seu-d-urgell",
    "leon","burgos","lugo","ourense","palencia","zamora","soria","teruel",
    "mondonedo","pedraza","penaranda-de-bracamonte","guadalupe","cudillero",
    "frigiliana","mojacar","luarca","sanlucar-de-barrameda","jerez-de-la-frontera",
    "ciutadella-de-menorca","peniscola","baeza","xativa","estella-lizarra",
    "tortosa","guadix","santa-cruz-de-la-palma",
}

# Capitales provinciales (50)
CAPITALES = {
    "a-coruna","albacete","alicante","almeria","avila","badajoz","barcelona","bilbao",
    "burgos","caceres","cadiz","castellon-de-la-plana","ciudad-real","cordoba","cuenca",
    "girona","granada","guadalajara","huelva","huesca","jaen","las-palmas-de-gran-canaria",
    "leon","lleida","logrono","lugo","madrid","malaga","melilla","merida","murcia",
    "ourense","oviedo","palencia","palma","pamplona","pontevedra","salamanca",
    "san-sebastian-donostia","santa-cruz-de-tenerife","santander","segovia","sevilla",
    "soria","tarragona","teruel","toledo","valencia","valladolid","vitoria-gasteiz",
    "zamora","zaragoza",
}

# Islas (Canarias + Baleares no capital — capitales gana antes)
CCAA_INSULARES = {"canarias", "baleares"}

# Suburbios metropolitanos (Madrid, Barcelona, Bilbao, Sevilla, Valencia)
SUBURBIO_METRO = {
    # Madrid
    "alcobendas","san-sebastian-de-los-reyes","tres-cantos","alcorcon","fuenlabrada",
    "leganes","getafe","mostoles","parla","alcala-de-henares","torrejon-de-ardoz",
    "coslada","san-fernando-de-henares","majadahonda","las-rozas","pozuelo-de-alarcon",
    "boadilla-del-monte","villaviciosa-de-odon","arroyomolinos","valdemoro",
    "rivas-vaciamadrid","paracuellos-de-jarama",
    # Barcelona
    "el-prat-de-llobregat","esplugues-de-llobregat","cornella-de-llobregat","gava",
    "sant-boi-de-llobregat","sant-feliu-de-llobregat","viladecans","sant-cugat-del-valles",
    "cerdanyola-del-valles","mollet-del-valles","sant-just-desvern","badalona",
    "santa-coloma-de-gramenet","l-hospitalet-de-llobregat","castelldefels","premia-de-mar",
    "el-masnou","rubi","mairena-del-aljarafe","mairena-del-alcor",
    # Sevilla / Valencia / Bilbao / Otros
    "tomares","bormujos","alcala-de-guadaira","camas","la-rinconada","dos-hermanas",
    "torrent","paterna","mislata","aldaia","quart-de-poblet","manises","burjassot",
    "barakaldo","getxo","portugalete","leioa","sestao","santurtzi","basauri","galdakao",
    "armilla","maracena",
}

# Costera turística (marca turística clara)
COSTERA = {
    "marbella","torremolinos","fuengirola","benalmadena","mijas","estepona","manilva",
    "nerja","torrox","frigiliana","velez-malaga","rincon-de-la-victoria","sotogrande",
    "salobrena","almuñecar","almunecar","la-herradura","motril",
    "javea","denia","calpe","altea","benidorm","villajoyosa","el-campello","santa-pola",
    "guardamar-del-segura","torrevieja","orihuela","pilar-de-la-horadada",
    "cullera","gandia","oliva","tavernes-de-la-valldigna","peniscola","vinaros",
    "benicarlo","benicassim",
    "salou","cambrils","calafell","sitges","l-escala","palafrugell","palamos","tossa-de-mar",
    "lloret-de-mar","blanes","calella","pineda-de-mar","malgrat-de-mar","s-agaro",
    "vilanova-i-la-geltru","cunit","castello-d-empuries","roses",
    "tarifa","conil-de-la-frontera","chiclana-de-la-frontera","el-puerto-de-santa-maria",
    "rota","chipiona","sanlucar-de-barrameda","barbate","los-canos-de-meca",
    "ayamonte","isla-cristina","punta-umbria","matalascanas",
    "sanxenxo","baiona","cangas-do-morrazo","vilagarcia-de-arousa","o-grove",
    "llanes","ribadesella","cudillero","luarca",
    "laredo","castro-urdiales","san-vicente-de-la-barquera","comillas","suances",
    "zarautz","getaria","hondarribia","mundaka","bermeo","zumaia","deba","orio",
    "mojacar","vera","carboneras","aguilas",
    "salinas","castrillon",
}

# Polo logístico
POLO_LOGISTICO = {
    "algeciras","cartagena","valencia",  # puertos
    "el-prat-de-llobregat","coslada","san-fernando-de-henares","alcala-de-guadaira",
    "miranda-de-ebro","irun","jundiz","torrejon-de-ardoz",
    "vila-seca","ferrol","naron","fene",
    "antequera","puente-genil",
    "barbastro","zaragoza-actur",
}

# Universitaria (no capital ya cubierta o donde la universidad domina)
UNIVERSITARIA = {
    "cerdanyola-del-valles",  # UAB
    "mondragon",  # MGEP
    "pollensa-pollenca","lleida","baeza",  # UNIA
    "osuna","puerto-real",  # campus UCA
}

# Industrial (industria histórica/dominante)
INDUSTRIAL = {
    "eibar","mondragon","durango","tolosa","bermeo","barakaldo","sestao","portugalete",
    "santurtzi","basauri","galdakao","ortuella","abanto-zierbena","muskiz",
    "linares","baena","lucena","puente-genil","martos","villacarrillo","ubrique",
    "yecla","jumilla","cieza","yeste","totana","molina-de-segura","fuente-alamo-de-murcia",
    "puertollano","talavera-de-la-reina","villarrobledo","tomelloso","valdepenas",
    "almansa","villena","elda","petrer","sax","ibi","alcoy","ontinyent","cocentaina",
    "ferrol","naron","aviles","mieres","langreo","la-felguera","san-martin-del-rey-aurelio",
    "miranda-de-ebro","aranda-de-duero","villalpando",
    "vitoria-gasteiz","alava-norte",
    "siero","vila-real","bayona","calzada-de-calatrava",
    "navalmoral-de-la-mata","azuaga",
    "almendralejo","calatayud",
    "alcantarilla","alcala-la-real",
    "andujar","jaen-norte",
    "burriana","nules","onda","la-vall-d-uixo","castello-de-la-plana",
}

# Dormitorio (función residencial-conexión)
DORMITORIO = {
    "collado-villalba","galapagar","torrelodones","colmenar-viejo","alpedrete",
    "guadarrama","cercedilla","bustarviejo","pinto","valdemoro","ciempozuelos",
    "humanes-de-madrid","mocejon","esquivias",
    "mollet-del-valles","granollers","caldes-de-montbui","la-llagosta","montcada-i-reixac",
    "santa-perpetua-de-mogoda","rubi","sant-vicenc-dels-horts","cornella-de-llobregat",
    "pinto","arroyomolinos",
    "berriozar","villava","burlada","ansoain","barañain",
    "cabanillas-del-campo","azuqueca-de-henares","alovera","yunquera-de-henares",
    "torreblanca","mocejon","yeles","numancia-de-la-sagra",
    "el-vendrell","roda-de-bera",
}

# ============ CLASIFICADOR ============

def clasificar(slug, ccaa, datos):
    """Devuelve la clave de plantilla más adecuada (orden de prioridad)."""
    precio = datos.get("precio") or 0
    roi = datos.get("roi") or 0
    dias = datos.get("dias") or 99

    # 1) Histórica/patrimonio (gana sobre capital cuando aplique)
    if slug in HISTORICA:
        return "historica_patrimonio"
    # 2) Isla (Canarias + Baleares no capital)
    if ccaa in CCAA_INSULARES and slug not in CAPITALES:
        return "isla"
    # 3) Capital provincial
    if slug in CAPITALES:
        return "capital_provincial"
    # 4) Suburbio metropolitano
    if slug in SUBURBIO_METRO:
        return "suburbio_metropolitano"
    # 5) Costera turística
    if slug in COSTERA:
        return "costera_turistica"
    # 6) Polo logístico
    if slug in POLO_LOGISTICO:
        return "polo_logistico"
    # 7) Universitaria
    if slug in UNIVERSITARIA:
        return "ciudad_universitaria"
    # 8) Industrial
    if slug in INDUSTRIAL:
        return "ciudad_industrial"
    # 9) Dormitorio
    if slug in DORMITORIO:
        return "ciudad_dormitorio"
    # 10) Zona tensionada (precio alto + días bajos)
    if precio >= 2800 and dias <= 21:
        return "zona_tensionada"
    # 11) Rural / despoblación (precio muy bajo + ROI alto + días largos)
    if precio <= 1200 and roi >= 6.5 and dias >= 25:
        return "rural_despoblacion"
    # 12) Default: ciudad media equilibrada
    return "media_equilibrada"


# ============ EJECUCIÓN ============

def main():
    data_path = Path(__file__).resolve().parent / "_cities_data.json"
    cities = json.loads(data_path.read_text(encoding="utf-8"))

    pat_div = re.compile(
        r'(<div class="tend-perspectiva">💡 <strong>Perspectiva Ren Data:</strong>\s*)(.+?)(</div>)'
    )

    asignaciones = {k: [] for k in PLANTILLAS}
    cambios = 0
    errors = []

    for slug, datos in sorted(cities.items()):
        fp = ROOT / f"rentabilidad-{slug}.html"
        html = fp.read_text(encoding="utf-8")
        m = pat_div.search(html)
        if not m:
            errors.append(f"{slug}: sin div tend-perspectiva")
            continue

        # Extraer nombre de ciudad del texto actual
        old_txt = m.group(2)
        # Patrones para extraer el nombre
        m_name = (
            re.match(r'Las perspectivas a corto y medio plazo para (.+?) son', old_txt) or
            re.match(r'El mercado de (.+?) ofrece', old_txt) or
            re.match(r'En (.+?), el inversor', old_txt) or
            re.match(r'(.+?) destaca como', old_txt)
        )
        if not m_name:
            errors.append(f"{slug}: nombre no extraído de '{old_txt[:60]}'")
            continue
        nombre = m_name.group(1).strip()

        clave = clasificar(slug, datos.get("ccaa"), datos)
        asignaciones[clave].append(slug)
        nuevo_txt = PLANTILLAS[clave].replace("{C}", nombre)
        nuevo_div = m.group(1) + nuevo_txt + m.group(3)
        new_html = html[:m.start()] + nuevo_div + html[m.end():]
        fp.write_text(new_html, encoding="utf-8")
        cambios += 1

    print(f"\nReemplazos: {cambios} / {len(cities)}\n")
    print("Distribucion por arquetipo:")
    print("-" * 50)
    for k in sorted(asignaciones, key=lambda x: -len(asignaciones[x])):
        print(f"  {k:30}  {len(asignaciones[k]):>4}")
    if errors:
        print(f"\nErrores ({len(errors)}):")
        for e in errors[:20]: print(f"   {e}")

if __name__ == "__main__":
    main()
