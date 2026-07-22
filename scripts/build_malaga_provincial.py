#!/usr/bin/env python3
"""Construye mercado-inmobiliario-provincia-malaga-2026.html a partir del
shell del artículo andaluz y del DATA[] de index.html (municipios de Málaga)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
OUT = BETA / "mercado-inmobiliario-provincia-malaga-2026.html"

ZONAS = {
    "capital": ["malaga"],
    "costa_occ": ["marbella", "estepona", "fuengirola", "benalmadena", "torremolinos", "mijas", "manilva", "casares", "benahavis"],
    "axarquia": ["velez-malaga", "nerja", "torrox", "rincon-de-la-victoria", "algarrobo"],
    "guadalhorce": ["alhaurin-de-la-torre", "alhaurin-el-grande", "coin", "cartama", "alora", "pizarra"],
    "interior": ["antequera", "ronda", "archidona", "campillos", "mollina", "villanueva-del-trabuco", "alameda"],
}
ZONA_LABEL = {
    "capital": "Capital", "costa_occ": "Costa occidental", "axarquia": "Axarquía / Costa oriental",
    "guadalhorce": "Valle del Guadalhorce", "interior": "Interior",
}
ALL_SLUGS = [s for z in ZONAS.values() for s in z]


def fmt_eu(n):
    return f"{int(round(n)):,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def parse_data():
    html = (BETA / "index.html").read_text(encoding="utf-8")
    cities = {}
    for m in re.finditer(r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),d:(\d+),sl:"([^"]+)"(?:,pob:(\d+))?(?:,itp:([\d.]+))?\}', html):
        sl = m.group(10)
        if sl in ALL_SLUGS:
            cities[sl] = {
                "n": m.group(1), "roi": float(m.group(4)), "p": int(m.group(5)),
                "alq": int(m.group(6)), "vp": float(m.group(7)), "va": float(m.group(8)),
                "d": int(m.group(9)), "sl": sl,
                "pob": int(m.group(11)) if m.group(11) else None,
            }
    return cities


def zona_of(sl):
    for z, slugs in ZONAS.items():
        if sl in slugs:
            return ZONA_LABEL[z]
    return ""


def build_table(cities):
    rows = sorted(cities.values(), key=lambda c: -c["roi"])
    out = []
    for i, c in enumerate(rows, 1):
        cls = {1: "gold", 2: "silver", 3: "bronze"}.get(i, "")
        out.append(
            f'        <tr><td class="cmp-rank {cls}">{i}</td>'
            f'<td><a href="rentabilidad-{c["sl"]}.html" class="cmp-city">{c["n"]}</a><span class="cmp-cc">{zona_of(c["sl"])}</span></td>'
            f'<td><span class="cmp-roi">{fmt_pct(c["roi"])}%</span></td>'
            f'<td class="cmp-num">{fmt_eu(c["p"])}€</td>'
            f'<td class="cmp-num">{fmt_eu(c["alq"])}€/mes</td>'
            f'<td class="cmp-num">+{fmt_pct(c["vp"])}%</td>'
            f'<td><a href="rentabilidad-{c["sl"]}.html">Ver →</a></td></tr>'
        )
    return "\n".join(out)


def zone_stats(cities, key):
    group = [cities[s] for s in ZONAS[key] if s in cities]
    n = len(group)
    return {
        "n": n,
        "roi": sum(c["roi"] for c in group) / n,
        "p": sum(c["p"] for c in group) / n,
        "alq": sum(c["alq"] for c in group) / n,
        "d": sum(c["d"] for c in group) / n,
    }


def main():
    cities = parse_data()
    missing = [s for s in ALL_SLUGS if s not in cities]
    if missing:
        print("[warn] sin datos:", missing)
    total = len(cities)
    roi_med = sum(c["roi"] for c in cities.values()) / total
    p_med = sum(c["p"] for c in cities.values()) / total
    alq_med = sum(c["alq"] for c in cities.values()) / total
    d_med = sum(c["d"] for c in cities.values()) / total

    zs = {k: zone_stats(cities, k) for k in ZONAS}
    table = build_table(cities)

    shell = (BETA / "mercado-inmobiliario-andalucia-2026.html").read_text(encoding="utf-8")
    head_end = shell.find('<section class="art-hero">')
    foot_start = shell.find("<footer>")
    head = shell[:head_end]
    foot = shell[foot_start:]

    title = "Mercado inmobiliario de la provincia de Málaga 2026 — Análisis en profundidad"
    desc = (
        f"Análisis en profundidad de la provincia de Málaga 2026: {total} municipios, 4 zonas (Costa occidental, "
        f"Axarquía, Valle del Guadalhorce e interior), ROI medio {fmt_pct(roi_med)}%, precio medio {fmt_eu(p_med)}€/m², "
        f"efecto del comprador extranjero y ranking provincial completo."
    )
    url = "https://rendata.es/mercado-inmobiliario-provincia-malaga-2026"

    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head, count=1)
    head = re.sub(r"<title>[^<]*</title>", f"<title>{title} | Ren Data</title>", head, count=1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', head, count=1)
    head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">', head, count=1)
    head = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', head, count=1)
    head = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="Provincia de Málaga: {total} municipios, 4 zonas, ROI medio {fmt_pct(roi_med)}%. Capital vs provincia y efecto del comprador extranjero.">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)

    jsonld_article = (
        '{"@context": "https://schema.org", "@type": "Article", '
        f'"headline": "{title}", "description": "{desc}", '
        '"datePublished": "2026-07-22", "dateModified": "2026-07-22", '
        '"author": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"}, '
        '"publisher": {"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/", "logo": {"@type": "ImageObject", "url": "https://rendata.es/favicon.svg"}}, '
        f'"mainEntityOfPage": {{"@type": "WebPage", "@id": "{url}"}}, "inLanguage": "es-ES", '
        '"about": [{"@type": "Place", "name": "Provincia de Málaga"}, {"@type": "Place", "name": "Costa del Sol"}, {"@type": "Place", "name": "Axarquía"}, {"@type": "Place", "name": "Valle del Guadalhorce"}, {"@type": "Thing", "name": "Inversión inmobiliaria"}], '
        '"keywords": ["mercado inmobiliario Málaga", "provincia de Málaga", "invertir Costa del Sol", "Axarquía vivienda", "Valle del Guadalhorce", "rentabilidad alquiler Málaga"]}'
    )
    jsonld_bc = (
        '{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ['
        '{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://rendata.es/"}, '
        '{"@type": "ListItem", "position": 2, "name": "Análisis", "item": "https://rendata.es/analisis.html"}, '
        f'{{"@type": "ListItem", "position": 3, "name": "Mercado inmobiliario provincia de Málaga 2026", "item": "{url}"}}]}}'
    )
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Article".*?</script>',
                  f'<script type="application/ld+json">{jsonld_article}</script>', head, count=1, flags=re.DOTALL)
    head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "BreadcrumbList".*?</script>',
                  f'<script type="application/ld+json">{jsonld_bc}</script>', head, count=1, flags=re.DOTALL)
    head = head.replace('<span class="bc-cur">Mercado inmobiliario en Andalucía 2026</span>',
                        '<span class="bc-cur">Mercado inmobiliario provincia de Málaga 2026</span>')

    def zrow(k):
        z = zs[k]
        return (f'<tr><td><strong>{ZONA_LABEL[k]}</strong></td><td class="cmp-num">{z["n"]}</td>'
                f'<td><span class="cmp-roi">{fmt_pct(z["roi"])}%</span></td>'
                f'<td class="cmp-num">{fmt_eu(z["p"])}€</td><td class="cmp-num">{fmt_eu(z["alq"])}€/mes</td>'
                f'<td class="cmp-num">{int(round(z["d"]))} días</td></tr>')

    body = f'''<section class="art-hero">
  <div class="art-hero-inner">
    <div class="art-eyebrow"><span class="live-dot"></span>Análisis provincial · Datos Q2-Q3 2026</div>
    <h1>Mercado inmobiliario de la <span class="ac">provincia de Málaga</span> — Análisis en profundidad 2026</h1>
    <div class="art-meta">
      <span>📅 Publicado el 22 de julio de 2026</span>
      <span>📊 Fuente: Idealista, Ministerio de Vivienda, INE</span>
      <span>🔄 Actualizado trimestralmente</span>
    </div>
    <p class="art-lead">Málaga es la provincia inmobiliaria más dinámica de España, pero no es <em>un</em> mercado: son al menos <strong>cuatro mercados</strong> que se comportan de forma radicalmente distinta. La Costa del Sol occidental opera con precios y compradores internacionales; la Axarquía combina playa asequible y aguacates; el Valle del Guadalhorce absorbe a quienes la capital expulsa por precio; y el interior ofrece los últimos yields altos de la provincia. Análisis completo de los <strong>{total} municipios malagueños</strong> del DATA Ren Data.</p>
  </div>
</section>

<article class="art">

  <div class="art-toc">
    <div class="art-toc-title">Índice</div>
    <ul>
      <li><a href="#cifras">Las cifras de la provincia</a></li>
      <li><a href="#zonas">Las 4 zonas y sus dinámicas</a></li>
      <li><a href="#capital">Capital vs provincia: el contraste</a></li>
      <li><a href="#extranjero">El efecto del comprador extranjero</a></li>
      <li><a href="#ranking">Ranking provincial completo</a></li>
      <li><a href="#inversor">Perfil del inversor por zona</a></li>
      <li><a href="#conclusion">Conclusión</a></li>
    </ul>
  </div>

  <h2 id="cifras">Las cifras de la provincia de Málaga</h2>

  <div class="art-kpi">
    <div class="art-kpi-item"><div class="art-kpi-v"><span class="blue">{fmt_pct(roi_med)}%</span></div><div class="art-kpi-l">ROI medio provincial</div></div>
    <div class="art-kpi-item"><div class="art-kpi-v">{fmt_eu(p_med)}€</div><div class="art-kpi-l">precio m² medio</div></div>
    <div class="art-kpi-item"><div class="art-kpi-v">{fmt_eu(alq_med)}€/mes</div><div class="art-kpi-l">alquiler medio</div></div>
    <div class="art-kpi-item"><div class="art-kpi-v">{int(round(d_med))} días</div><div class="art-kpi-l">venta media</div></div>
  </div>

  <p>La provincia de Málaga concentra <strong>{total} municipios analizados</strong> en el DATA Ren Data, desde los 599.063 habitantes de la capital hasta los 5.426 de Alameda. La media provincial —{fmt_pct(roi_med)}% de ROI bruto a {fmt_eu(p_med)}€/m²— esconde una dispersión enorme: se puede comprar a <strong>800€/m² en Villanueva del Trabuco</strong> o a <strong>3.900€/m² en Benahavís</strong>, con yields que van del 4,3% al 6,8%. Ninguna otra provincia española ofrece este rango en 100 kilómetros de radio.</p>

  <p>La regla general del mercado malagueño es simple y se cumple con precisión matemática: <strong>la rentabilidad sube a medida que uno se aleja del mar</strong>. Cada kilómetro hacia el interior descuenta precio más rápido de lo que descuenta alquiler, y el yield mejora. La contrapartida es la inversa: la revalorización y la liquidez se concentran en la franja costera.</p>

  <h2 id="zonas">Las 4 zonas y sus dinámicas diferenciadas</h2>

  <div class="tbl-wrap">
    <div class="resp-table-wrap"><table class="cmp">
      <thead><tr><th>Zona</th><th>Municipios</th><th>ROI medio</th><th>Precio m²</th><th>Alquiler</th><th>Venta media</th></tr></thead>
      <tbody>
        {zrow("capital")}
        {zrow("costa_occ")}
        {zrow("axarquia")}
        {zrow("guadalhorce")}
        {zrow("interior")}
      </tbody>
    </table></div>
  </div>

  <h3>🌊 Costa del Sol occidental — el mercado internacional</h3>
  <p>De Torremolinos a Manilva, pasando por Marbella, Estepona, Fuengirola, Benalmádena, Mijas, Casares y Benahavís. Es el mercado más caro ({fmt_eu(zs["costa_occ"]["p"])}€/m² de media) y el de menor yield ({fmt_pct(zs["costa_occ"]["roi"])}%), porque el precio no lo fija el salario local sino el <strong>comprador internacional</strong>: británicos, escandinavos, neerlandeses, belgas y, desde 2023, un flujo creciente de estadounidenses y de Oriente Medio en el segmento prime. La demanda de alquiler combina larga temporada de expatriados, vacacional de alto precio y trabajadores del sector servicios que sostienen la economía turística. Marbella (4,8%) y Benahavís (4,3%) son operaciones patrimonialistas; Torremolinos (5,2%) y Manilva (5,3%) son las puertas de entrada relativamente asequibles.</p>

  <h3>🥑 Axarquía / Costa oriental — playa asequible y subtropicales</h3>
  <p>Vélez-Málaga, Rincón de la Victoria, Nerja, Torrox y Algarrobo. Dos motores conviven: el turismo residencial de una costa aún más barata que la occidental (el famoso "mejor clima de Europa" de Torrox) y la <strong>agricultura subtropical</strong> —aguacate y mango— que ha convertido la vega en una de las huertas más rentables del país. El yield medio ({fmt_pct(zs["axarquia"]["roi"])}%) supera al de la costa occidental porque el precio de entrada es menor ({fmt_eu(zs["axarquia"]["p"])}€/m²) y la demanda de invierno de jubilados centroeuropeos rellena la estacionalidad. Riesgo estructural a vigilar: <strong>el agua</strong>. La sequía condiciona el subtropical y, con él, parte del empleo comarcal.</p>

  <h3>🍋 Valle del Guadalhorce — el traspaís metropolitano</h3>
  <p>Alhaurín de la Torre, Alhaurín el Grande, Coín, Cártama, Álora y Pizarra. Es la válvula de escape de la capital: familias y profesionales expulsados por los precios de Málaga ciudad ({fmt_eu(cities["malaga"]["p"])}€/m²) compran o alquilan a 20-40 minutos por la A-357 o la línea C-2 de Cercanías. El yield medio ({fmt_pct(zs["guadalhorce"]["roi"])}%) es el segundo mejor de la provincia con demanda estructural creciente — Cártama es, de hecho, uno de los municipios que más crece de Andalucía. La combinación de cítricos, comunidad extranjera residencial (Coín, Alhaurín el Grande) y conmuters configura un inquilino diverso y solvente.</p>

  <h3>🫒 Interior — los últimos yields altos</h3>
  <p>Antequera, Ronda, Archidona, Campillos, Mollina, Villanueva del Trabuco y Alameda. Aquí el precio lo fija la economía local —olivar, agroindustria, ganadería, logística— y por eso los yields son los más altos de la provincia ({fmt_pct(zs["interior"]["roi"])}% de media, con picos del 6,8%). Dos catalizadores diferencian este interior del de otras provincias: el <strong>polo logístico de Antequera</strong> (Puerto Seco, intermodal ferroviario), que irradia empleo a Mollina, Archidona o Alameda; y el turismo consolidado de Ronda y Antequera (Caminito del Rey, El Torcal, Dólmenes). La contrapartida clásica: liquidez lenta (29-33 días de venta) y revalorización modesta.</p>

  <h2 id="capital">Capital vs provincia: el contraste</h2>

  <p>Málaga capital es la historia de éxito inmobiliario de la década —tecnología, turismo urbano, capitalidad cultural— y su precio lo refleja: <strong>{fmt_eu(cities["malaga"]["p"])}€/m²</strong>, un +{fmt_pct(cities["malaga"]["vp"])}% en un año. Pero ese éxito ha comprimido su rentabilidad: <strong>{fmt_pct(cities["malaga"]["roi"])}% de ROI bruto</strong>, por debajo de la media provincial y a un mundo de los pueblos del interior.</p>

  <p>El contraste es directo: el mismo capital que compra <strong>un apartamento de 60m² en la capital</strong> compra <strong>tres casas en Campillos o Alameda</strong> generando casi el doble de renta mensual conjunta. La capital ofrece liquidez inmediata (18 días), revalorización de dos dígitos y cero riesgo de vacancia; el interior ofrece cash-flow. Entre ambos extremos, el Guadalhorce captura parte de la revalorización metropolitana con un punto más de yield.</p>

  <div class="tax-box">
    <h3>💡 La lectura Ren Data</h3>
    <p>La pregunta correcta en Málaga no es "¿capital o provincia?" sino "¿qué función cumple esta compra en mi cartera?". Renta → interior (Mollina 6,8%, Campillos 6,7%, Alameda 6,7%). Equilibrio → Guadalhorce (Álora 6,3%, Alhaurín el Grande 6,2%) y Axarquía (Vélez-Málaga 6,0%). Patrimonio y apreciación → capital y costa occidental (Málaga 5,1%, Marbella 4,8%, Benahavís 4,3%). Las tres estrategias son válidas; mezclarlas sin querer es el error.</p>
  </div>

  <h2 id="extranjero">El efecto del comprador extranjero en la costa</h2>

  <p>Málaga es la provincia peninsular con mayor peso de comprador extranjero: en torno a <strong>un tercio de las operaciones</strong> provinciales, con picos que superan el 60% en Benahavís, ~48% en Casares y Manilva, y ~28% en la Axarquía costera. Este comprador tiene tres efectos estructurales sobre el mercado:</p>

  <p><strong>1. Desancla el precio del salario local.</strong> En la franja costera, el precio de la vivienda compite en un mercado europeo de segundas residencias y relocalización, no en el mercado laboral malagueño. Por eso Marbella cuesta 4.200€/m² con salarios andaluces — y por eso el yield comprimido de la costa no es una anomalía, sino el reflejo de un riesgo percibido menor y una demanda de compra inagotable.</p>

  <p><strong>2. Sostiene el ciclo.</strong> El comprador nórdico o británico de la Costa del Sol compra mayoritariamente sin hipoteca española. El mercado costero malagueño es así menos sensible al Euríbor que el nacional: en el ciclo de tipos 2022-2025, la costa siguió subiendo dígito doble mientras mercados hipotecados se enfriaban.</p>

  <p><strong>3. Crea un mercado de alquiler de temporada única en España.</strong> La "invernada" (octubre-mayo) de jubilados centroeuropeos permite en la costa malagueña un ciclo anual completo: vacacional en verano, temporada de invierno después. Bien gestionado, elimina la vacancia estacional que castiga a otros destinos de playa.</p>

  <p>El límite de este modelo es regulatorio y social: la presión sobre el residente local ha puesto la VUT en el punto de mira municipal (Málaga capital ya restringe nuevas licencias en 43 barrios) y el debate sobre zonas tensionadas seguirá escalando. El inversor de costa debe subrayar en rojo la palabra <strong>licencia</strong> antes de firmar nada.</p>

  <h2 id="ranking">Ranking provincial completo — los {total} municipios malagueños</h2>
  <p>Ranking del DATA Ren Data ordenado por rentabilidad bruta (alquiler×12÷precio de vivienda de 100m²). Pulsa en cualquier municipio para acceder a su ficha completa.</p>

  <div class="tbl-wrap">
    <div class="resp-table-wrap"><table class="cmp">
      <thead>
        <tr><th>#</th><th>Municipio</th><th>ROI bruto</th><th>Precio m²</th><th>Alquiler medio</th><th>Var. precio</th><th>Ficha</th></tr>
      </thead>
      <tbody>
{table}
      </tbody>
    </table></div>
  </div>

  <h2 id="inversor">Perfil del inversor por zona</h2>

  <div class="pro-con">
    <div class="pc-col pro">
      <h3>Ventajas de invertir en la provincia de Málaga</h3>
      <ul>
        <li><strong>Cuatro mercados en uno:</strong> permite construir una cartera completa (renta + equilibrio + patrimonio) sin salir de la provincia.</li>
        <li><strong>Demanda internacional estructural:</strong> el comprador extranjero da soporte al precio costero en cualquier ciclo.</li>
        <li><strong>Motores económicos diversificados:</strong> tecnología (capital), turismo, subtropical (Axarquía), logística (Antequera).</li>
        <li><strong>Liquidez costera excepcional:</strong> 14-23 días de venta media en toda la franja litoral.</li>
        <li><strong>ITP andaluz del 7%</strong> y sin Patrimonio efectivo: fiscalidad autonómica favorable.</li>
      </ul>
    </div>
    <div class="pc-col con">
      <h3>Riesgos a vigilar</h3>
      <ul>
        <li><strong>Yield comprimido en costa:</strong> pagar precios de apreciación esperando cash-flow es el error clásico del mercado malagueño.</li>
        <li><strong>Riesgo regulatorio VUT:</strong> restricciones municipales crecientes; verificar licencia SIEMPRE antes de comprar para uso turístico.</li>
        <li><strong>Agua y sequía:</strong> condicionan el subtropical de la Axarquía y episodios de restricciones en la costa.</li>
        <li><strong>Liquidez lenta en interior:</strong> 29-33 días de venta y compradores contados en los pueblos del norte.</li>
        <li><strong>Dispersión de precios brutal:</strong> los promedios provinciales no sirven para valorar; usa siempre el dato municipal.</li>
      </ul>
    </div>
  </div>

  <h2 id="conclusion">Conclusión</h2>

  <p>La provincia de Málaga en 2026 es un mapa de <strong>{total} mercados</strong> con lógicas propias: {fmt_pct(roi_med)}% de ROI medio que abarca desde el 4,3% patrimonialista de Benahavís hasta el 6,8% rentista de Mollina y Villanueva del Trabuco. La costa se compra por apreciación y se defiende con comprador internacional; el Guadalhorce se compra por equilibrio y se defiende con Cercanías; el interior se compra por renta y se defiende con precio de entrada.</p>

  <p>Para profundizar municipio a municipio, consulta la <a href="ccaa-andalucia.html">ficha de Andalucía</a>, el <a href="mercado-inmobiliario-andalucia-2026.html">análisis autonómico completo</a> o el <a href="comparador.html">comparador</a> para enfrentar hasta 4 municipios malagueños entre sí.</p>

  <div class="art-cta">
    <h3>¿Buscas la mejor plaza malagueña para tu inversión?</h3>
    <p>Compara municipios de costa, Guadalhorce e interior con datos homogéneos, o explora el ranking completo.</p>
    <a href="comparador.html">Abrir comparador →</a>
  </div>

</article>

'''

    OUT.write_text(head + body + foot, encoding="utf-8")
    print(f"[ok] {OUT.name} ({total} municipios, ROI medio {fmt_pct(roi_med)}%)")
    for k in ZONAS:
        z = zs[k]
        print(f"  {ZONA_LABEL[k]}: n={z['n']} roi={fmt_pct(z['roi'])}% p={fmt_eu(z['p'])}€")


if __name__ == "__main__":
    main()
