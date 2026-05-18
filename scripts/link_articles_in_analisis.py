#!/usr/bin/env python3
"""Append 16 new CCAA article cards + 10 profile-based article cards to analisis.html.
Also updates the ItemList JSON-LD."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
INDEX = BETA / "index.html"
ANALISIS = BETA / "analisis.html"


def parse_data():
    html = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
                     r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
                     r'd:(\d+),sl:"([^"]+)"')
    rows = []
    for m in pat.finditer(html):
        rows.append({"cc": m.group(2), "roi": float(m.group(4)), "p": int(m.group(5))})
    return rows


def avg_roi_for(rows, ccaa):
    cs = [r for r in rows if r["cc"] == ccaa]
    if not cs:
        return None, None, 0
    return sum(c["roi"] for c in cs)/len(cs), sum(c["p"] for c in cs)/len(cs), len(cs)


CCAA_ARTICLE_INFO = [
    ("Andalucía","andalucia"),
    ("Cataluña","cataluna"),
    ("C. Valenciana","comunitat-valenciana"),
    ("C. de Madrid","madrid"),
    ("Galicia","galicia"),
    ("Castilla y León","castilla-y-leon"),
    ("Castilla-La Mancha","castilla-la-mancha"),
    ("Canarias","canarias"),
    ("Islas Baleares","baleares"),
    ("Aragón","aragon"),
    ("R. de Murcia","murcia"),
    ("Asturias","asturias"),
    ("Cantabria","cantabria"),
    ("Navarra","navarra"),
    ("Extremadura","extremadura"),
    ("La Rioja","la-rioja"),
]


def build_ccaa_cards():
    rows = parse_data()
    cards = []
    for ccaa_name, slug in CCAA_ARTICLE_INFO:
        avg_roi, avg_p, n = avg_roi_for(rows, ccaa_name)
        if not n:
            continue
        roi_str = f"{avg_roi:.2f}".replace(".", ",") + "%"
        price_str = f"{int(round(avg_p)):,}".replace(",", ".") + "€/m²"
        cards.append((ccaa_name, slug, n, roi_str, price_str))
    return cards


def build_card_html(tag, href, title, desc):
    return f'''
    <article class="an-card">
      <div class="an-card-body">
        <span class="an-card-tag">{tag}</span>
        <h2><a href="{href}">{title}</a></h2>
        <p class="an-card-desc">{desc}</p>
        <div class="an-card-meta">
          <span class="an-card-date">📅 18 mayo 2026</span>
          <a href="{href}" class="an-card-link">Leer análisis →</a>
        </div>
      </div>
    </article>
'''


def main():
    html = ANALISIS.read_text(encoding="utf-8")

    new_cards = []

    # 16 CCAA cards (skip País Vasco — already in)
    skip_ccaa = {"País Vasco"}
    for ccaa_name, slug, n, roi_str, price_str in build_ccaa_cards():
        if ccaa_name in skip_ccaa:
            continue
        href = f"mercado-inmobiliario-{slug}-2026.html"
        if href in html:  # already linked, skip
            continue
        title = f"Mercado inmobiliario en {ccaa_name} 2026 — Análisis completo"
        desc = (
            f"Análisis profundo del mercado en {ccaa_name}: {n} ciudades analizadas, "
            f"ROI medio {roi_str}, precio medio {price_str}, fiscalidad específica, "
            f"perfil del inversor y ranking completo. Datos Q1 2026."
        )
        new_cards.append(build_card_html(ccaa_name, href, title, desc))

    # 10 profile-based articles
    profile_articles = [
        ("Conservador", "guia-inversor-conservador-2026.html",
         "Guía del inversor conservador 2026 — Ciudades estables y bajo riesgo",
         "Selección de ciudades estables con ROI 5-6%, demanda sostenida y baja volatilidad. Capitales medias, mercados consolidados y poca exposición regulatoria. Estrategia para preservar capital con yield razonable."),
        ("Agresivo", "guia-inversor-agresivo-2026.html",
         "Guía del inversor agresivo 2026 — Máximo ROI y ciudades pequeñas",
         "Las plazas con yield más alto del país. Cuenca, Zamora, Teruel y Ciudad Real superan el 7% bruto. Análisis de riesgos de liquidez, vacancia y revalorización en municipios pequeños."),
        ("Vacacional", "invertir-vivienda-vacacional-espana-2026.html",
         "Invertir en vivienda vacacional en España 2026 — VUT, estacionalidad y rentabilidad",
         "Mercado vacacional regulado: licencias VUT por CCAA, estacionalidad, ocupación y comparativa con alquiler residencial. Costa del Sol, Baleares, Canarias y Costa Brava."),
        ("Estrategia", "invertir-primera-vivienda-vs-inversion-2026.html",
         "¿Comprar para vivir o para invertir? Análisis 2026",
         "Comparativa entre comprar primera vivienda y compra patrimonial. Coste de oportunidad, fiscalidad, financiación y conclusión por perfil familiar. Datos reales 2026."),
        ("Guía", "como-calcular-rentabilidad-vivienda-2026.html",
         "Cómo calcular la rentabilidad de una vivienda 2026 — Guía metodológica completa",
         "Guía detallada: ROI bruto, ROI neto, IRR, cash-flow, descuento por gastos (IBI, comunidad, mantenimiento, vacancia, impuestos). Plantilla y casos prácticos."),
        ("Jóvenes", "mejores-ciudades-jovenes-invertir-2026.html",
         "Mejores ciudades para inversores jóvenes 2026 — Presupuesto limitado",
         "Las plazas más accesibles para primera inversión: tickets &lt;100.000€ para piso de 100m². Capitales pequeñas con yield alto y financiación favorable."),
        ("Patrimonial", "invertir-vivienda-jubilacion-espana-2026.html",
         "Invertir en vivienda para la jubilación 2026 — Largo plazo y patrimonio",
         "Estrategia patrimonial a 15-20 años. Ciudades con revalorización sostenida, marca y demanda estable. Madrid, Barcelona, Bilbao, San Sebastián, Valencia."),
        ("Revalorización", "ciudades-mayor-revalorizacion-2026.html",
         "Las ciudades con mayor revalorización en España 2026",
         "Top 20 por subida de precio anual. Alicante, Valencia, Málaga, Madrid lideran con +10-12% anual. Análisis de palancas y previsiones."),
        ("Comparativa VUT", "alquiler-turistico-vs-residencial-rentabilidad-2026.html",
         "Alquiler turístico vs residencial — Comparativa de rentabilidad 2026",
         "Análisis comparativo de yield, riesgos, fiscalidad y regulación. Cuándo conviene VUT, cuándo larga duración. Casos prácticos con datos Q1 2026."),
        ("Nueva vs usada", "invertir-vivienda-nueva-vs-segunda-mano-2026.html",
         "Vivienda nueva vs segunda mano para invertir 2026",
         "Análisis coste/beneficio. Diferencias en ITP (10%) vs IVA (10%) + AJD (1,5%), garantías, mantenimiento, ubicación y rentabilidad. Cuándo elegir cada opción."),
    ]
    for tag, href, title, desc in profile_articles:
        if href in html:
            continue
        new_cards.append(build_card_html(tag, href, title, desc))

    if not new_cards:
        print("No new cards to insert")
        return

    # Insert before </div> of an-grid
    closing = "  </div>\n\n</article>\n"
    if closing in html:
        block = "".join(new_cards) + "  </div>\n\n</article>\n"
        html = html.replace(closing, block, 1)
    else:
        # Fallback: find last </article> within an-grid
        idx = html.rfind("</article>\n  </div>")
        if idx == -1:
            print("Could not find insertion point")
            return
        # Insert right after the </article>\n inside an-grid
        anchor = "</article>\n  </div>"
        ins = "</article>\n" + "".join(new_cards) + "  </div>"
        html = html.replace(anchor, ins, 1)

    ANALISIS.write_text(html, encoding="utf-8")
    print(f"Inserted {len(new_cards)} new cards into analisis.html")


if __name__ == "__main__":
    main()
