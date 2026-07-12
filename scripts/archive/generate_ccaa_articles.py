#!/usr/bin/env python3
"""Generates 16 missing CCAA analysis articles in rendata_beta/.

Reads DATA[] from index.html, groups by CCAA, computes aggregates, and
produces mercado-inmobiliario-{ccaa-slug}-2026.html using the same
template structure as the existing País Vasco article.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
INDEX = BETA / "index.html"

# CCAA metadata: name, slug, ITP%, fiscal profile, key sectors, marca/perception
CCAA_INFO = {
    "Andalucía": {
        "slug": "andalucia",
        "itp": 7,
        "drivers": "agroalimentaria intensiva, turismo costero (Costa del Sol, Costa de la Luz), industria aeronáutica (Sevilla), servicios y construcción",
        "marca": "comunidad más grande de España por superficie y segunda por población. Marca turística global (Sevilla, Granada, Costa del Sol, Marbella)",
        "fiscal_notes": "ITP del 7% (favorable frente a la media nacional). Reducción del 60% por arrendamiento de vivienda habitual (IRPF estatal). Sin Impuesto sobre el Patrimonio efectivo en 2026 (bonificación del 100%). Junta de Andalucía aplica bonificaciones al ITP para menores de 35 años y vivienda habitual.",
        "regulacion": "Andalucía NO ha declarado zonas tensionadas bajo la Ley Estatal de Vivienda 2023 — marco regulatorio estable. Sin tope autonómico al alquiler. Alquiler turístico (VFT) regulado por decreto 28/2016: registro obligatorio en el RTA, licencia por vivienda.",
        "intro": "Andalucía es <strong>el mercado inmobiliario más diverso de España</strong>: combina capitales históricas con yield moderado (Sevilla, Granada, Málaga), municipios costeros premium (Marbella, Estepona), capitales comarcales agrícolas de alto yield (Lebrija, Arahal, Bailén, Almonte) y zonas turísticas masivas (Costa del Sol, Costa de la Luz).",
        "perfiles": ["Inversor de cash-flow alto con foco interior agrícola", "Inversor turístico-vacacional Costa del Sol", "Inversor patrimonial Málaga/Sevilla"],
    },
    "Cataluña": {
        "slug": "cataluna",
        "itp": 10,
        "drivers": "industria automotriz (SEAT, Volkswagen), química (Tarragona), farmacéutica, sedes corporativas en BCN, turismo masivo, viticultura Penedès, agroalimentaria Delta Ebro",
        "marca": "segunda economía de España. Barcelona como marca global, Costa Brava, modernismo, gastronomía",
        "fiscal_notes": "ITP del 10% (uno de los más altos de España, junto a Galicia, CV, Aragón). Sin reducciones generales de ITP. IRPF estatal aplica reducción del 60% por alquiler de vivienda habitual. Tributación del patrimonio bajo IGS estatal.",
        "regulacion": "Cataluña aplica desde 2024 el <strong>índice de zonas tensionadas</strong> bajo la Ley Estatal de Vivienda 2023. Verifica si la vivienda cae en zona declarada antes de comprar — afecta al precio de alquiler máximo y exenciones fiscales. La Generalitat regula el alquiler turístico (HUT) con moratorias en Barcelona y otras zonas masificadas.",
        "intro": "Cataluña es el <strong>mercado más complejo regulatoriamente de España</strong>. Tiene Barcelona como marca premium global, una corona metropolitana densa (Baix Llobregat, Vallès), tejido industrial sólido y litoral turístico fuerte. Pero el marco de zonas tensionadas y la regulación de VUT obligan al inversor a hacer due diligence específica antes de cada operación.",
        "perfiles": ["Inversor patrimonial Barcelona corona", "Inversor de yield medio Vallès/Penedès industrial", "Inversor costa Maresme/Costa Brava"],
    },
    "C. Valenciana": {
        "slug": "comunitat-valenciana",
        "itp": 10,
        "drivers": "agricultura cítrica, turismo Costa Blanca, industria cerámica (Castellón), calzado (Elda/Elche/Petrer), juguete (Ibi), residencial extranjero Alicante",
        "marca": "tercer mercado por volumen tras Madrid y Cataluña. Marca turística (Benidorm, Alicante, Valencia)",
        "fiscal_notes": "ITP del 10% (alineado con Cataluña). La Generalitat Valenciana ha reducido el Impuesto de Sucesiones para residentes (importante para herederos). Reducción del 60% en IRPF por alquiler vivienda habitual.",
        "regulacion": "La Comunitat avanza en la implementación del índice de zonas tensionadas — partial declaration en algunos municipios. Alquiler turístico regulado con licencia obligatoria por vivienda (registro autonómico). Verifica antes de comprar para uso turístico.",
        "intro": "La Comunitat Valenciana ofrece <strong>el mayor abanico precio/yield de España</strong>: desde Benidorm (ROI 5,3% pero 2.500€/m²) hasta La Vall d'Uixó o Crevillent (ROI 6,1% con tickets de 1.100€/m²). Mercados muy distintos: costa Alicante extranjera, L'Horta de Valencia metropolitana, interior agroindustrial Castellón, comarcas calzado/cerámica del Vinalopó.",
        "perfiles": ["Inversor vacacional Costa Blanca", "Inversor industrial Vinalopó/Plana Baixa", "Inversor L'Horta metropolitana Valencia"],
    },
    "C. de Madrid": {
        "slug": "madrid",
        "itp": 6,
        "drivers": "servicios y finanzas (capital), sede de grandes corporaciones, logística (Corredor Henares, A-4 sur), industria farmacéutica, ferroviaria, residencial premium suroeste",
        "marca": "capital política, económica y financiera de España. Mercado más caro tras País Vasco y Baleares en CCAA grandes",
        "fiscal_notes": "ITP del 6% (uno de los más bajos de España, solo superado por canarias). La CAM aplica bonificación del 100% al Impuesto sobre el Patrimonio (de hecho, no se paga). IRPF reducción del 60% por alquiler. <strong>Fiscalidad agregada muy favorable</strong> al inversor.",
        "regulacion": "Madrid NO ha declarado zonas tensionadas bajo la Ley Estatal de Vivienda 2023 — la Comunidad rechaza la aplicación. Marco regulatorio máximo de estabilidad para el inversor. Sin tope autonómico de alquiler. Alquiler turístico bajo regulación municipal.",
        "intro": "Madrid es <strong>el mercado más codiciado de España para el inversor</strong>: ITP bajo, sin Patrimonio efectivo, sin zonas tensionadas, demanda inquebrantable. El precio en Madrid capital supera los 5.000€/m² en barrios centrales y se modera en suburbios sur (Móstoles, Parla, Getafe) y suburbios premium oeste (Pozuelo, Boadilla, Las Rozas, Villaviciosa de Odón).",
        "perfiles": ["Inversor patrimonial Madrid capital", "Inversor de yield medio suburbio sur", "Inversor premium suroeste"],
    },
    "Galicia": {
        "slug": "galicia",
        "itp": 10,
        "drivers": "pesquero y conservero (capital nacional), naval, automotriz (Stellantis Vigo), Inditex (sede Arteixo), agroalimentaria, turismo cultural y costero",
        "marca": "comunidad de cuatro provincias con marca propia. A Coruña/Vigo como polos económicos. Santiago Patrimonio Mundial",
        "fiscal_notes": "ITP del 10%. Galicia tiene bonificaciones autonómicas para vivienda habitual de menores de 36 años en zonas rurales (reducción a 5%). Reducción del 60% IRPF por alquiler.",
        "regulacion": "Galicia NO ha declarado zonas tensionadas bajo la Ley Estatal de Vivienda 2023. Marco regulatorio estable. La Xunta regula el alquiler turístico (REAT) con registro obligatorio.",
        "intro": "Galicia ofrece <strong>uno de los mejores binomios precio/yield de España</strong> en municipios costeros y comarcales. Vigo (motor económico con Stellantis y polígonos), A Coruña (Inditex, servicios), Santiago (universidad y administración) son tres mercados distintos. Las rías + los municipios pesqueros (Ribeira, Cangas, Marín) y residenciales metropolitanos (Oleiros, Culleredo, Cambre, Sada) ofrecen oportunidades sólidas.",
        "perfiles": ["Inversor residencial premium A Coruña metropolitana", "Inversor industrial-pesquero Vigo", "Inversor comarcal de yield alto"],
    },
    "Castilla y León": {
        "slug": "castilla-y-leon",
        "itp": 8,
        "drivers": "agricultura cereal y oleaginosas (mayor productor nacional), industria automotriz (Iveco, Renault, Nissan), agroindustria, ruta de los vinos (Ribera Duero, Toro, Rueda), turismo histórico (Salamanca, Ávila, Segovia, Burgos)",
        "marca": "comunidad más extensa de España. 9 provincias con realidades muy diversas. Despoblación rural compensada por capitales con universidad y ruta del vino",
        "fiscal_notes": "ITP del 8%. Castilla y León tiene bonificaciones por adquisición de vivienda habitual en municipios <2.000 habitantes. Reducción del 60% IRPF.",
        "regulacion": "Castilla y León NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "Castilla y León combina <strong>capitales históricas con yield muy atractivo</strong> (Zamora 7,5%, Palencia 6,8%, Ávila 6,5%) y un mercado rural en despoblación. Las capitales con universidad (Valladolid, Salamanca, Burgos, León) tienen demanda residencial estable, las capitales menores ofrecen yield muy alto a tickets bajos.",
        "perfiles": ["Inversor cash-flow máximo Zamora/Palencia/Ávila", "Inversor universitario Salamanca/Valladolid/Burgos", "Inversor patrimonial Burgos/Valladolid"],
    },
    "Castilla-La Mancha": {
        "slug": "castilla-la-mancha",
        "itp": 9,
        "drivers": "agroalimentaria (vino DO La Mancha, Valdepeñas), industria del calzado y cerámica, polos logísticos corredor A-4 (Seseña, Illescas, Ocaña), aeropuerto Ciudad Real, dormitorio Madrid sur",
        "marca": "comunidad más despoblada de España con grandes contrastes: dormitorios Madrid sur con yield alto, capitales históricas (Toledo, Cuenca), mercados agroalimentarios rurales",
        "fiscal_notes": "ITP del 9%. Castilla-La Mancha mantiene Impuesto sobre Sucesiones con bonificaciones por parentesco. Reducción del 60% IRPF.",
        "regulacion": "Castilla-La Mancha NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "Castilla-La Mancha es <strong>la comunidad de los polos logísticos del corredor A-4 (Seseña, Illescas, Ocaña, Tarancón)</strong> con yield 6,1-6,2% y tickets bajos (1.500-1.700€/m²), de las capitales con yield alto (Cuenca 7,5%, Ciudad Real 7,2%, Talavera, Toledo) y de la Mancha vinícola.",
        "perfiles": ["Inversor logístico Corredor A-4", "Inversor yield alto capitales", "Inversor agroindustrial Mancha"],
    },
    "Canarias": {
        "slug": "canarias",
        "itp": 6.5,
        "drivers": "turismo masivo (capital mundial de hotelería de sol y playa), agricultura (plátano, tomate), servicios, residencial extranjero",
        "marca": "REF (Régimen Económico Fiscal) canario. Insularidad. Clima permanente. Mercado turístico estacional de altísima demanda",
        "fiscal_notes": "ITP del 6,5% (uno de los más bajos de España gracias al REF). El IGIC sustituye al IVA al 7% (vs 21% peninsular). Sin Impuesto sobre el Patrimonio efectivo. Reducción del 60% IRPF.",
        "regulacion": "Canarias regula el alquiler vacacional con licencia obligatoria por vivienda. La saturación turística en Tenerife sur y Gran Canaria sur ha llevado a moratorias parciales. Verifica antes de comprar.",
        "intro": "Canarias combina <strong>el mejor régimen fiscal de España (IGIC 7%, ITP 6,5%, REF) con un mercado turístico estructuralmente fuerte</strong>. Los municipios de las dos islas grandes (Las Palmas GC y Tenerife) muestran realidades distintas: capitales con demanda residencial premium (Las Palmas, Santa Cruz, La Laguna), municipios turísticos (Adeje, San Bartolomé de Tirajana, Puerto del Carmen) y municipios cumbres residenciales (La Laguna, Santa Brígida).",
        "perfiles": ["Inversor turístico Costa Adeje/Gran Canaria sur", "Inversor residencial Las Palmas/Tenerife metropolitana", "Inversor patrimonial Tenerife norte"],
    },
    "Islas Baleares": {
        "slug": "baleares",
        "itp": 11,
        "drivers": "turismo premium (mercado alemán y británico), residencial extranjero alta gama, servicios náuticos",
        "marca": "primer mercado más caro de España por m². Marca global Ibiza, Mallorca, Menorca. Insularidad limita oferta",
        "fiscal_notes": "ITP en escala progresiva: 8% hasta 400k€, 9% 400k-600k€, 10% 600k-1M, 11% 1M+. El más alto de España en tramo alto. Reducción del 60% IRPF.",
        "regulacion": "Baleares regula estrictamente el alquiler vacacional: licencias limitadas, moratoria en Palma para nuevos VTV, zonas restringidas en Ibiza. La compra para uso turístico requiere due diligence severa.",
        "intro": "Baleares es <strong>el mercado más caro y más regulado de España</strong>: ITP máximo del 11%, licencias VTV limitadas, restricciones a la compra por extranjeros no UE. El yield medio del 4,5-4,7% es bajo, pero la marca, la revalorización y la demanda alemana/británica/escandinava sostienen los precios.",
        "perfiles": ["Inversor patrimonial premium con horizonte 10 años+", "Inversor vacacional con licencia VTV existente", "Inversor residencial Palma/Inca"],
    },
    "Aragón": {
        "slug": "aragon",
        "itp": 10,
        "drivers": "agroalimentaria, automotriz (Stellantis Zaragoza), logística (Plataforma PLAZA Zaragoza), agricultura cereal Cinco Villas, fruta dulce Bajo Cinca",
        "marca": "Zaragoza como polo logístico medio Madrid-Barcelona. Pirineo aragonés (turismo). Tres provincias dispares: Zaragoza dominante, Huesca natural, Teruel despoblada",
        "fiscal_notes": "ITP del 10%. Aragón mantiene bonificaciones al ITP para vivienda habitual de jóvenes y familias numerosas. Reducción del 60% IRPF.",
        "regulacion": "Aragón NO ha declarado zonas tensionadas. Marco regulatorio estable. Alquiler turístico regulado con registro autonómico.",
        "intro": "Aragón ofrece <strong>uno de los ROI medios más altos de España (6,7%)</strong> gracias a sus capitales menores (Teruel, Calatayud) con tickets bajos. Zaragoza concentra el peso económico (logística PLAZA, automotriz, servicios) con yield 5,8-6%. Huesca y Barbastro ofrecen yield moderado en mercado residencial estable. Teruel es la plaza con mejor binomio ticket/yield del país (1.000€/m², ROI 7,2%).",
        "perfiles": ["Inversor cash-flow máximo Teruel/Calatayud", "Inversor logístico Zaragoza PLAZA", "Inversor patrimonial Zaragoza capital"],
    },
    "R. de Murcia": {
        "slug": "murcia",
        "itp": 8,
        "drivers": "agricultura intensiva (capital agroalimentaria nacional), polo químico Cartagena, turismo Mar Menor y golf, residencial extranjero",
        "marca": "comunidad uniprovincial. Mercado agroalimentario clave (Vega del Segura). Turismo golf Mar Menor",
        "fiscal_notes": "ITP del 8% (alineado con Andalucía). Murcia mantiene bonificaciones para jóvenes y familias numerosas. Reducción del 60% IRPF.",
        "regulacion": "Murcia NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "Murcia combina <strong>yield muy alto en mercados agroindustriales</strong> (Lorca, Cieza, Caravaca, La Unión con 6,3-7,2% ROI) con mercados costeros turísticos (Águilas, Los Alcázares, San Pedro del Pinatar) y la capital con yield medio. La Unión es la plaza con mayor ROI de Murcia (7,2%).",
        "perfiles": ["Inversor cash-flow máximo La Unión/Lorca/Cieza", "Inversor turístico-golf Mar Menor", "Inversor agroindustrial Vega Segura"],
    },
    "Asturias": {
        "slug": "asturias",
        "itp": 10,
        "drivers": "industria siderúrgica (ArcelorMittal), agroalimentaria (Danone, Capsa), turismo costero, naval, minería en reconversión",
        "marca": "comunidad uniprovincial. Mercado en transición post-minera. Costa cantábrica. Marca gastronómica fuerte (sidra)",
        "fiscal_notes": "ITP del 10%. Asturias mantiene bonificaciones a vivienda habitual en concejos rurales. Reducción del 60% IRPF.",
        "regulacion": "Asturias NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "Asturias presenta <strong>un mercado en transición</strong>: tres polos urbanos (Oviedo, Gijón, Avilés) con yield 5,7-6%, los concejos costeros (Llanes, Ribadesella) con yield estable y mercado vacacional, los concejos mineros en reconversión (Mieres, Langreo, San Martín del Rey Aurelio) con yield muy alto (6,3-6,4%) y demanda más débil.",
        "perfiles": ["Inversor patrimonial Oviedo/Gijón", "Inversor turístico costa cantábrica", "Inversor yield máximo cuencas mineras"],
    },
    "Cantabria": {
        "slug": "cantabria",
        "itp": 10,
        "drivers": "industria (Santander), servicios financieros, turismo costero, ganadería lechera, naval",
        "marca": "comunidad uniprovincial. Santander como capital regional. Costa cantábrica con marca premium (Comillas, Castro Urdiales)",
        "fiscal_notes": "ITP del 10%. Cantabria mantiene bonificaciones a vivienda habitual de menores de 36 años. Reducción del 60% IRPF.",
        "regulacion": "Cantabria NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "Cantabria es un <strong>mercado pequeño pero estable</strong> centrado en el área metropolitana de Santander (Santander, Camargo, El Astillero, Piélagos) y los municipios costeros del oriente (Castro Urdiales, Laredo, Suances). Yield medio del 5,5-6% en capitales y suburbios, con tickets moderados.",
        "perfiles": ["Inversor patrimonial Santander", "Inversor costero oriental (Castro/Laredo)", "Inversor suburbio metropolitano"],
    },
    "Navarra": {
        "slug": "navarra",
        "itp": 6,
        "drivers": "industria automotriz (Volkswagen Pamplona), agroalimentaria, energía renovable, viticultura DO Navarra",
        "marca": "régimen foral propio (Convenio Económico). Marca cultural (San Fermín). Industria potente con peso del automóvil",
        "fiscal_notes": "Navarra tiene <strong>Hacienda Foral propia</strong>: ITP del 6% (igual a Madrid), IRPF con tipos propios (marginal máximo 49%), Impuesto sobre Patrimonio vigente. Reducción del 60% por alquiler de vivienda habitual con limitaciones específicas forales.",
        "regulacion": "Navarra NO ha declarado zonas tensionadas. Marco regulatorio foral estable.",
        "intro": "Navarra es un <strong>mercado pequeño y caro</strong>. Pamplona y su corona metropolitana (Barañáin, Burlada, Zizur Mayor, Valle de Egüés) concentran la mayor parte del mercado, con yield 5,4-5,5% y tickets premium (2.200-2.400€/m²). Tudela y Estella son las plazas de yield más alto (6%+) con tickets bajos.",
        "perfiles": ["Inversor patrimonial Pamplona", "Inversor de yield Tudela/Estella", "Inversor residencial corona Pamplona"],
    },
    "Extremadura": {
        "slug": "extremadura",
        "itp": 8,
        "drivers": "agroalimentaria, tomate y aceituna, jamón ibérico Dehesa, energía solar, ganadería extensiva",
        "marca": "comunidad menos densa de España. Despoblación rural acusada. Mercado pequeño con dos capitales (Badajoz, Cáceres) y ciudades comarcales",
        "fiscal_notes": "ITP del 8%. Extremadura mantiene bonificaciones al ITP para vivienda habitual de jóvenes. Reducción del 60% IRPF.",
        "regulacion": "Extremadura NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "Extremadura es <strong>el mercado más pequeño de España por volumen</strong> con dos capitales (Badajoz, Cáceres), Mérida (administrativa), Plasencia, Don Benito y Villanueva de la Serena. Yield muy alto (6,2-6,4%) y tickets muy bajos (900-1.100€/m²). Mercado de inversor local o de presupuesto limitado.",
        "perfiles": ["Inversor cash-flow máximo con presupuesto limitado", "Inversor patrimonial Badajoz/Cáceres", "Inversor local extremeño"],
    },
    "La Rioja": {
        "slug": "la-rioja",
        "itp": 7,
        "drivers": "viticultura DOC Rioja, industria del calzado (Arnedo), agroalimentaria, conservas",
        "marca": "comunidad uniprovincial. Marca DOC Rioja global. Mercado pequeño concentrado en Logroño + Calahorra + Arnedo",
        "fiscal_notes": "ITP del 7% (alineado con Andalucía). La Rioja mantiene bonificaciones específicas para vivienda habitual de jóvenes. Reducción del 60% IRPF.",
        "regulacion": "La Rioja NO ha declarado zonas tensionadas. Marco regulatorio estable.",
        "intro": "La Rioja es <strong>uno de los mercados más pequeños de España</strong>. Logroño concentra la actividad, con Calahorra, Haro y Arnedo como mercados comarcales. Yield medio 5,7-6,2% con tickets razonables.",
        "perfiles": ["Inversor local riojano", "Inversor patrimonial Logroño", "Inversor comarcal de yield (Calahorra/Arnedo)"],
    },
    "Melilla": {
        "slug": None,
        "itp": 6,
        "drivers": "comercio fronterizo, militar, servicios",
        "marca": "ciudad autónoma",
        "fiscal_notes": "ITP del 6%. IPSI (Impuesto sobre Producción, Servicios e Importación) sustituye al IVA. Régimen fiscal específico.",
        "regulacion": "Sin zonas tensionadas.",
        "intro": "Melilla es una ciudad autónoma con mercado pequeño y específico.",
        "perfiles": ["Inversor local melillense"],
    },
    "Ceuta": {
        "slug": None,
        "itp": 6,
        "drivers": "comercio fronterizo, militar, servicios",
        "marca": "ciudad autónoma",
        "fiscal_notes": "ITP del 6%. IPSI sustituye al IVA. Régimen fiscal específico.",
        "regulacion": "Sin zonas tensionadas.",
        "intro": "Ceuta es una ciudad autónoma con mercado pequeño y específico.",
        "perfiles": ["Inversor local ceutí"],
    },
}


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def parse_data():
    html = INDEX.read_text(encoding="utf-8")
    pat = re.compile(
        r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
        r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
        r'd:(\d+),sl:"([^"]+)"'
    )
    rows = []
    for m in pat.finditer(html):
        rows.append({
            "n": m.group(1), "cc": m.group(2), "reg": m.group(3),
            "roi": float(m.group(4)), "p": int(m.group(5)), "alq": int(m.group(6)),
            "vp": float(m.group(7)), "va": float(m.group(8)),
            "d": int(m.group(9)), "sl": m.group(10),
        })
    return rows


def build_nav_html():
    """Reusable header navigation."""
    return '''<header>
  <a href="/" class="logo">
    <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
    <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
  </a>
  <nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <a href="/comparador.html">Comparador</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/guia-inversor.html">Guía</a>
    <a href="/sobre.html">Sobre</a>
  </nav>
</header>'''


def build_footer_html(total_cities):
    return f'''<footer>
  <div class="footer-inner">
    <div class="footer-col">
      <a href="/" class="logo" style="margin-bottom:.6rem;display:inline-flex">
        <svg width="22" height="22" viewBox="0 0 34 34" fill="none"><path d="M17 2.5C12.3 2.5 8.5 6.3 8.5 11c0 3.2 1.7 6.7 3.8 9.8C14 23.4 15.7 25.8 17 27.5c1.3-1.7 3-4.1 4.7-6.7 2.1-3.1 3.8-6.6 3.8-9.8 0-4.7-3.8-8.5-8.5-8.5z" fill="#1a56db"/><polyline points="12,13 14.2,10.5 16.4,12.3 19.2,8.8 22,10.2" stroke="white" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
        <div class="logo-wm"><span style="color:var(--text);font-weight:800;letter-spacing:-.03em">Ren</span><span style="color:var(--blue);font-weight:800;letter-spacing:-.03em"> Data</span></div>
      </a>
      <p>Análisis de rentabilidad inmobiliaria gratuito para {total_cities} ciudades de España. Datos Q1 2026.</p>
    </div>
    <div class="footer-col">
      <h4>Análisis</h4>
      <a href="ranking.html">Ranking completo</a>
      <a href="analisis.html">Análisis</a>
      <a href="comparador.html">Comparador</a>
      <a href="guia-inversor.html">Guía del inversor</a>
    </div>
    <div class="footer-col">
      <h4>Recursos</h4>
      <a href="glosario.html">Glosario</a>
      <a href="sobre.html">Sobre Ren Data</a>
      <a href="contacto.html">Contacto</a>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <a href="privacidad.html">Privacidad</a>
      <a href="aviso-legal.html">Aviso legal</a>
    </div>
  </div>
  <div class="footer-bottom">© 2026 rendata.es · Fuente: Idealista Q1 2026 · Ministerio de Vivienda</div>
</footer>'''


def build_article(ccaa_name, info, cities, total_cities):
    """Compose one CCAA article from data + info."""
    ccaa_slug = info["slug"]
    # Stats
    cities_s = sorted(cities, key=lambda x: -x["roi"])
    n = len(cities_s)
    avg_roi = sum(c["roi"] for c in cities_s) / n
    avg_p = sum(c["p"] for c in cities_s) / n
    avg_alq = sum(c["alq"] for c in cities_s) / n
    avg_vp = sum(c["vp"] for c in cities_s) / n
    avg_d = sum(c["d"] for c in cities_s) / n
    top5 = cities_s[:5]

    title = f"Mercado inmobiliario en {ccaa_name} 2026 — Análisis completo"
    desc = (
        f"Análisis completo del mercado inmobiliario en {ccaa_name} 2026: "
        f"{n} ciudades del DATA Ren Data, precio medio {fmt_eu(avg_p)}€/m², "
        f"ROI medio {fmt_pct(avg_roi)}%, fiscalidad ITP {info['itp']}%, "
        f"perfil del inversor y ranking completo."
    )

    # JSON-LD Article
    article_json = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "datePublished": "2026-05-18",
        "dateModified": "2026-05-18",
        "author": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"},
        "publisher": {
            "@type": "Organization",
            "name": "Ren Data", "url": "https://rendata.es/",
            "logo": {"@type": "ImageObject", "url": "https://rendata.es/favicon.svg"}
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://rendata.es/mercado-inmobiliario-{ccaa_slug}-2026.html"
        },
        "inLanguage": "es-ES",
        "about": [{"@type": "Place", "name": ccaa_name}] + [{"@type": "Place", "name": c["n"]} for c in top5[:3]] + [{"@type": "Thing", "name": "Inversión inmobiliaria"}],
        "keywords": [f"mercado inmobiliario {ccaa_name}", f"invertir {ccaa_name}", f"ROI {ccaa_name}", f"precio vivienda {ccaa_name}", "rentabilidad alquiler"]
    }

    breadcrumb_json = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://rendata.es/"},
            {"@type": "ListItem", "position": 2, "name": "Análisis", "item": "https://rendata.es/analisis.html"},
            {"@type": "ListItem", "position": 3, "name": f"Mercado inmobiliario en {ccaa_name} 2026", "item": f"https://rendata.es/mercado-inmobiliario-{ccaa_slug}-2026.html"}
        ]
    }

    # Top 5 detailed analysis
    top5_html = ""
    for i, c in enumerate(top5, 1):
        top5_html += (
            f'  <h3>{c["n"]}<span class="h3-ccaa">— {fmt_pct(c["roi"])}% ROI · {c["cc"]}</span></h3>\n'
            f'  <div class="art-kpi">\n'
            f'    <div class="art-kpi-item"><div class="art-kpi-v"><span class="blue">{fmt_pct(c["roi"])}%</span></div><div class="art-kpi-l">ROI bruto</div></div>\n'
            f'    <div class="art-kpi-item"><div class="art-kpi-v">{fmt_eu(c["p"])}€</div><div class="art-kpi-l">precio m²</div></div>\n'
            f'    <div class="art-kpi-item"><div class="art-kpi-v">{fmt_eu(c["alq"])}€/mes</div><div class="art-kpi-l">alquiler</div></div>\n'
            f'    <div class="art-kpi-item"><div class="art-kpi-v">{c["d"]} días</div><div class="art-kpi-l">venta</div></div>\n'
            f'  </div>\n'
            f'  <p>{c["n"]} ofrece un ROI bruto del <strong>{fmt_pct(c["roi"])}%</strong> con un precio medio de <strong>{fmt_eu(c["p"])}€/m²</strong> y alquileres en torno a <strong>{fmt_eu(c["alq"])}€/mes</strong> para vivienda estándar de 100m². La subida de precio anual ({fmt_pct(c["vp"])}%) y el tiempo medio de venta ({c["d"]} días) reflejan un mercado con liquidez razonable y momento favorable para el inversor. <a href="rentabilidad-{c["sl"]}.html">Ver ficha completa →</a></p>\n\n'
        )

    # Full ranking table
    rows_html = ""
    for i, c in enumerate(cities_s, 1):
        rank_class = "gold" if i == 1 else "silver" if i == 2 else "bronze" if i == 3 else ""
        vp_sign = "+" if c["vp"] > 0 else ""
        rows_html += (
            f'        <tr><td class="cmp-rank {rank_class}">{i}</td>'
            f'<td><a href="rentabilidad-{c["sl"]}.html" class="cmp-city">{c["n"]}</a><span class="cmp-cc">{c["cc"]}</span></td>'
            f'<td><span class="cmp-roi">{fmt_pct(c["roi"])}%</span></td>'
            f'<td class="cmp-num">{fmt_eu(c["p"])}€</td>'
            f'<td class="cmp-num">{fmt_eu(c["alq"])}€/mes</td>'
            f'<td class="cmp-num">{vp_sign}{fmt_pct(c["vp"])}%</td>'
            f'<td><a href="rentabilidad-{c["sl"]}.html">Ver →</a></td></tr>\n'
        )

    perfiles_html = ""
    for i, p in enumerate(info["perfiles"], 1):
        perfiles_html += f'  <p><strong>{i}. {p}.</strong></p>\n'

    head = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title} | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://rendata.es/mercado-inmobiliario-{ccaa_slug}-2026.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="Análisis profundo de {ccaa_name}: {n} ciudades, ROI medio {fmt_pct(avg_roi)}%, precio medio {fmt_eu(avg_p)}€/m².">
<link rel="canonical" href="https://rendata.es/mercado-inmobiliario-{ccaa_slug}-2026.html">
<link rel="stylesheet" href="/css/fonts.css">

<script type="application/ld+json">{json.dumps(article_json, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_json, ensure_ascii=False)}</script>

<script src="/js/nav-dropdown.js" defer></script>
<link rel="stylesheet" href="/css/top10.css">
<style>
.bc{{max-width:880px;margin:0 auto;padding:.9rem 2rem 0;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:.4rem}}
.bc a{{color:var(--muted);text-decoration:none;font-weight:500}}
.bc a:hover{{color:var(--blue);text-decoration:underline}}
.bc-sep{{color:#cbd5e1}}
.bc-cur{{color:var(--text);font-weight:600}}
.pro-con{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin:1.5rem 0 2rem}}
.pc-col{{padding:1.25rem 1.4rem;border-radius:var(--r);background:var(--white);border:1px solid var(--border);box-shadow:var(--sh)}}
.pc-col.pro{{border-left:4px solid var(--green)}}
.pc-col.con{{border-left:4px solid #dc2626}}
.pc-col h3{{font-size:1.05rem;font-weight:800;color:var(--text);margin:0 0 .8rem;border:none;padding:0;display:block;letter-spacing:-.02em}}
.pc-col.pro h3{{color:var(--green)}}
.pc-col.con h3{{color:#dc2626}}
.pc-col ul{{list-style:none;padding:0;margin:0}}
.pc-col li{{font-size:.88rem;padding:.45rem 0;color:var(--text2);line-height:1.55;border-bottom:1px solid var(--border)}}
.pc-col li:last-child{{border-bottom:none}}
.pc-col li:before{{margin-right:.4rem;font-weight:700}}
.pc-col.pro li:before{{content:"✓";color:var(--green)}}
.pc-col.con li:before{{content:"⚠";color:#dc2626}}
.tax-box{{background:#fef3c7;border:1px solid #fcd34d;border-radius:var(--r);padding:1.4rem 1.6rem;margin:1.5rem 0;font-size:.92rem;color:#78350f;line-height:1.7}}
.tax-box h3{{font-size:1.05rem;font-weight:800;color:#78350f;margin:0 0 .6rem;border:none;padding:0;display:block;letter-spacing:-.02em}}
@media(max-width:740px){{.pro-con{{grid-template-columns:1fr}}}}
</style>
<link rel="stylesheet" href="/css/nav.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-0M57323B51');</script>
</head>
<body>
'''

    body = f'''{build_nav_html()}

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">Inicio</a>
  <span class="bc-sep">›</span>
  <a href="analisis.html">Análisis</a>
  <span class="bc-sep">›</span>
  <span class="bc-cur">Mercado inmobiliario en {ccaa_name} 2026</span>
</nav>

<section class="art-hero">
  <div class="art-hero-inner">
    <div class="art-eyebrow"><span class="live-dot"></span>Análisis · Datos Q1 2026</div>
    <h1>Mercado inmobiliario en <span class="ac">{ccaa_name}</span> — Análisis completo 2026</h1>
    <div class="art-meta">
      <span>📅 Publicado el 18 de mayo de 2026</span>
      <span>📊 Fuente: Idealista, Ministerio de Vivienda</span>
      <span>🔄 Actualizado mensualmente</span>
    </div>
    <p class="art-lead">{info["intro"]} Análisis completo con datos reales Q1 2026 de las <strong>{n} ciudades</strong> del DATA Ren Data en {ccaa_name}.</p>
  </div>
</section>

<article class="art">

  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#cifras">Las cifras del mercado en {ccaa_name}</a></li>
      <li><a href="#top5">Top 5 ciudades por rentabilidad</a></li>
      <li><a href="#tabla">Ranking completo de las {n} ciudades</a></li>
      <li><a href="#fiscalidad">Fiscalidad específica</a></li>
      <li><a href="#regulacion">Regulación específica</a></li>
      <li><a href="#inversor">Perfil del inversor ideal</a></li>
      <li><a href="#conclusion">Conclusión</a></li>
    </ul>
  </div>

  <h2 id="cifras">Las cifras del mercado en {ccaa_name}</h2>

  <div class="art-kpi">
    <div class="art-kpi-item"><div class="art-kpi-v"><span class="blue">{fmt_pct(avg_roi)}%</span></div><div class="art-kpi-l">ROI medio</div></div>
    <div class="art-kpi-item"><div class="art-kpi-v">{fmt_eu(avg_p)}€</div><div class="art-kpi-l">precio m² medio</div></div>
    <div class="art-kpi-item"><div class="art-kpi-v">{fmt_eu(avg_alq)}€/mes</div><div class="art-kpi-l">alquiler medio</div></div>
    <div class="art-kpi-item"><div class="art-kpi-v">{avg_d:.0f} días</div><div class="art-kpi-l">venta media</div></div>
  </div>

  <p>{ccaa_name} cuenta con <strong>{n} ciudades analizadas</strong> en el DATA Ren Data. Los motores económicos principales son <strong>{info["drivers"]}</strong>. {info["marca"]}. La subida media de precios en los últimos 12 meses ha sido del <strong>+{fmt_pct(avg_vp)}%</strong>.</p>

  <h2 id="top5">Top 5 ciudades por rentabilidad en {ccaa_name}</h2>

{top5_html}

  <h2 id="tabla">Ranking completo de las {n} ciudades de {ccaa_name} por ROI</h2>
  <p>Ranking completo del DATA Ren Data ordenado por rentabilidad bruta. La ROI bruta se calcula sobre vivienda estándar de 100m² (alquiler×12÷precio×100). Pulsa en cualquier ciudad para acceder a su ficha completa.</p>

  <div class="tbl-wrap">
    <table class="cmp">
      <thead>
        <tr>
          <th>#</th><th>Ciudad</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th>
        </tr>
      </thead>
      <tbody>
{rows_html}      </tbody>
    </table>
  </div>

  <h2 id="fiscalidad">Fiscalidad específica de {ccaa_name}</h2>

  <div class="tax-box">
    <h3>🏛️ Régimen tributario</h3>
    <p>{info["fiscal_notes"]}</p>
    <p><strong>Recomendación:</strong> consulta siempre con asesor fiscal antes de cerrar la operación. La fiscalidad autonómica puede afectar materialmente al retorno neto.</p>
  </div>

  <h2 id="regulacion">Regulación específica</h2>
  <p>{info["regulacion"]}</p>

  <h2 id="inversor">Perfil del inversor ideal para {ccaa_name}</h2>

  <p>El mercado de {ccaa_name} es para tres tipos de inversor principales:</p>

{perfiles_html}

  <div class="pro-con">
    <div class="pc-col pro">
      <h3>Ventajas de invertir en {ccaa_name}</h3>
      <ul>
        <li><strong>ROI medio:</strong> {fmt_pct(avg_roi)}% bruto, {"superior" if avg_roi >= 5.8 else "moderado"} respecto a la media nacional (5,8%).</li>
        <li><strong>Ticket de entrada:</strong> precio medio {fmt_eu(avg_p)}€/m², {"asequible" if avg_p < 1800 else "moderado" if avg_p < 2500 else "elevado"} comparado con la media nacional (1.900€/m²).</li>
        <li><strong>{n} ciudades analizadas:</strong> abanico amplio para diversificar.</li>
        <li><strong>Liquidez:</strong> {avg_d:.0f} días de venta media, {"superior a la media" if avg_d < 23 else "alineada con la media"}.</li>
        <li><strong>Revalorización:</strong> +{fmt_pct(avg_vp)}% anual de subida media de precio.</li>
      </ul>
    </div>
    <div class="pc-col con">
      <h3>Riesgos a vigilar</h3>
      <ul>
        <li><strong>ITP del {info["itp"]}%:</strong> {"favorable frente" if info["itp"] < 8 else "alineado con" if info["itp"] <= 10 else "superior a"} la media española.</li>
        <li><strong>Concentración sectorial:</strong> los motores económicos son específicos de la región. Diversifica entre tipos de mercado.</li>
        <li><strong>Despoblación rural:</strong> evita municipios con tendencia poblacional negativa estructural.</li>
        <li><strong>Regulación cambiante:</strong> verifica antes de comprar si hay zonas tensionadas o restricciones VUT.</li>
        <li><strong>Yield bruto vs neto:</strong> recuerda descontar gastos (IBI, comunidad, mantenimiento, vacancia, impuestos): el ROI neto suele estar 1,5-2 puntos por debajo del bruto.</li>
      </ul>
    </div>
  </div>

  <h2 id="conclusion">Conclusión</h2>

  <p>El mercado inmobiliario de <strong>{ccaa_name}</strong> en 2026 se sitúa en <strong>{fmt_pct(avg_roi)}% de ROI medio</strong> con un precio medio de <strong>{fmt_eu(avg_p)}€/m²</strong>. {"Es una de las comunidades con mayor ROI de España" if avg_roi >= 6.0 else "Ofrece un equilibrio razonable entre yield y revalorización" if avg_roi >= 5.5 else "Su yield modesto se compensa con marca, demanda y revalorización"}.</p>

  <p>Para refinar tu decisión, consulta la <a href="ccaa-{ccaa_slug}.html">ficha completa de {ccaa_name}</a> con todas las ciudades, comparativas y filtros. También puedes usar el <a href="comparador.html">comparador</a> para enfrentar hasta 4 ciudades simultáneamente.</p>

  <div class="art-cta">
    <h3>¿Buscas la mejor ciudad para tu inversión?</h3>
    <p>Compara hasta 4 ciudades simultáneamente o explora el ranking completo de {total_cities} plazas analizadas.</p>
    <a href="comparador.html">Abrir comparador →</a>
  </div>

</article>

{build_footer_html(total_cities)}

</body>
</html>
'''

    return head + body


def main():
    rows = parse_data()
    total = len(rows)
    print(f"Total cities in DATA[]: {total}")

    by_ccaa = {}
    for r in rows:
        by_ccaa.setdefault(r["cc"], []).append(r)

    # Skip País Vasco (already exists with this canonical name)
    skip = {"País Vasco"}

    # Cities ccaa names that have no proper article slug (Ceuta, Melilla)
    skip.update({"Ceuta", "Melilla"})

    generated = 0
    for ccaa_name, cities in by_ccaa.items():
        if ccaa_name in skip:
            print(f"  [skip] {ccaa_name}")
            continue
        info = CCAA_INFO.get(ccaa_name)
        if not info or not info["slug"]:
            print(f"  [WARN] No info for {ccaa_name}")
            continue
        out = BETA / f"mercado-inmobiliario-{info['slug']}-2026.html"
        html = build_article(ccaa_name, info, cities, total)
        out.write_text(html, encoding="utf-8")
        generated += 1
        print(f"  [ok] {out.name} ({len(cities)} ciudades)")

    print(f"\nGenerated: {generated} articles")


if __name__ == "__main__":
    main()
