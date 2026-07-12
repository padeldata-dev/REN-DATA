"""
FASE 3 — Bloque "Ayudas para comprar en {CCAA}" + 3 FAQ comprador.

BLOQUE 1: insertar bloque de ayudas (Aval ICO + deducción autonómica IRPF +
          hipoteca joven CCAA + IVA/AJD vivienda nueva) antes de la FAQ.
BLOQUE 4: añadir 3 FAQ comprador (índices 10, 11, 12) al final de la sección
          existente (Fase 1 dejó 0-9 ocupados).

Datos por CCAA basados en información pública vigente 2024-2026. Donde no se
tiene una cifra exacta verificada, se etiqueta "Consulta con tu CCAA".
"""

from __future__ import annotations
import re
import sys
import glob
from pathlib import Path

ROOT       = Path(__file__).resolve().parents[1]
FICHAS_DIR = ROOT / "rendata_beta"

# ---------- Regex --------------------------------------------------------

RE_CITY    = re.compile(r'<div class="banner-title">([^<]+)</div>')
RE_CCAA    = re.compile(r'<div class="sl">(?:ITP|IPSI|IGIC) al comprar en ([^<]+)</div>')
RE_PISO    = re.compile(r'id="hi-precio"\s+type="number"\s+value="(\d+)"')

# Anchor for ayudas: just before <!-- FAQ -->
RE_FAQ_BLOCK_START = re.compile(r'(\s*<!-- FAQ -->)')
# Anchor for 3 new FAQ items: just before </div></div>\n  </div>\n  \n\n  <div class="disc">
RE_FAQ_CLOSE = re.compile(
    r'(</div>)(</div>\s*\n\s*</div>\s*\n\s*\n\s*<div class="disc">)'
)

HAS_AYUDAS_TOKEN = 'id="ayudas-compra"'
HAS_NEW_FAQ_TOKEN = 'toggleFaq(10)'


# ---------- Datos por CCAA ----------------------------------------------

# Cada entrada: {deduccion: {tit, desc, reqs[]}, joven: {tit, desc}, iva: desc}
# IPC, importes y porcentajes verificados con webs oficiales autonómicas
# 2024-2026. Cuando una cifra concreta es dudosa -> "Consulta con tu CCAA".

CCAA_AYUDAS = {
    "Andalucía": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes <35",
            "desc": "Andalucía permite deducir el 5% de las cantidades satisfechas por compra de vivienda habitual protegida para menores de 35 años o víctimas de violencia.",
            "reqs": ["Menor de 35 años", "Vivienda calificada como protegida (VPO)", "Base imponible ≤ 19.000€ (individual) / 24.000€ (conjunta)"],
        },
        "joven": {
            "tit": "Bono joven alquiler + ayudas compra rural",
            "desc": "Bono Alquiler Joven Estatal vigente. Ayudas autonómicas para compra en municipios menores de 5.000 hab. Consulta convocatorias en juntadeandalucia.es."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,2% en Andalucía. Tipo reducido AJD 0,3% para familias numerosas y discapacidad.",
    },
    "Aragón": {
        "deduccion": {
            "tit": "Deducción IRPF nacimiento + adquisición rural",
            "desc": "Aragón ofrece deducción autonómica por compra de vivienda habitual en municipios menores de 3.000 habitantes y por familias con hijos.",
            "reqs": ["Vivienda habitual en municipio rural", "Base liquidable individual ≤ 21.000€", "Consulta con tu CCAA para importes actualizados"],
        },
        "joven": {
            "tit": "Plan de Vivienda Joven Aragón",
            "desc": "Ayudas a la compra de primera vivienda para menores de 36 años y familias numerosas. Cuantía y convocatoria anual: aragon.es/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Aragón. Tipo reducido AJD 0,1-0,5% para jóvenes <35, familias numerosas y discapacidad.",
    },
    "Asturias": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes y zonas en riesgo",
            "desc": "Asturias permite deducir hasta el 5% por compra de vivienda habitual para menores de 35 años y residentes en municipios despoblados.",
            "reqs": ["Menor de 35 años o familia numerosa", "Base imponible máxima limitada", "Consulta con tu CCAA"],
        },
        "joven": {
            "tit": "Ayudas a la emancipación joven",
            "desc": "Bono Alquiler Joven Estatal + programas autonómicos de ayuda a compra en concejos rurales. Más info en asturias.es."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,2% en Asturias. Tipo reducido para jóvenes y vivienda habitual protegida.",
    },
    "Islas Baleares": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes <36",
            "desc": "Baleares ofrece deducción autonómica del 6,5% por compra o rehabilitación de vivienda habitual para menores de 36 años, hasta 600€/año.",
            "reqs": ["Menor de 36 años", "Vivienda habitual", "Base liquidable individual ≤ 33.000€ / conjunta ≤ 52.800€"],
        },
        "joven": {
            "tit": "Plan Habitatge Jove Balears",
            "desc": "Avales y ayudas para acceso a primera vivienda en jóvenes. Programa Bonificat. Consulta caib.es/habitatge."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,2% en Baleares. ITP escalado para 2ª mano (8-11,5% según valor).",
    },
    "Canarias": {
        "deduccion": {
            "tit": "Deducción IRPF compra vivienda habitual",
            "desc": "Canarias permite deducir el 1,75% (3,5% en menores 35 y otros colectivos) de las cantidades aportadas para compra de vivienda habitual nueva o usada.",
            "reqs": ["Vivienda habitual del contribuyente", "Base imponible máxima limitada", "Inmueble ubicado en Canarias"],
        },
        "joven": {
            "tit": "Plan de Vivienda Canarias",
            "desc": "Subvenciones para compra de vivienda joven y bono alquiler joven. Información en gobiernodecanarias.org."
        },
        "iva": "Canarias aplica IGIC 7% (no IVA) en vivienda nueva + AJD ~0,75%. ITP 2ª mano 6,5%. Tipos reducidos para jóvenes y familia numerosa.",
    },
    "Cantabria": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes y discapacidad",
            "desc": "Cantabria ofrece deducción autonómica del 10% (hasta 1.080€) por compra/rehabilitación de vivienda habitual para jóvenes <36, discapacitados y familias numerosas en zonas rurales.",
            "reqs": ["Menor de 36 años, discapacidad ≥33% o familia numerosa", "Base imponible máxima limitada", "Vivienda en municipios <2.000 hab. en algunos supuestos"],
        },
        "joven": {
            "tit": "Cantabria Joven Vivienda",
            "desc": "Plan autonómico de ayudas a la compra para menores de 35 en zonas con riesgo de despoblamiento. cantabria.es/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Cantabria. Tipo reducido ITP/AJD 5% en zonas rurales para jóvenes.",
    },
    "Castilla-La Mancha": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes <36",
            "desc": "Castilla-La Mancha permite deducir hasta 540€ por compra de vivienda habitual para menores de 36 años en municipios pequeños.",
            "reqs": ["Menor de 36 años", "Vivienda habitual en municipio <10.000 hab.", "Base liquidable conjunta ≤ 27.000€"],
        },
        "joven": {
            "tit": "Plan Vivienda Joven CLM",
            "desc": "Subvención directa hasta 10.800€ para compra de primera vivienda en municipios menores de 10.000 habitantes. castillalamancha.es."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Castilla-La Mancha. Tipo reducido AJD 0,75% para jóvenes y familias numerosas.",
    },
    "Castilla y León": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes en zonas rurales",
            "desc": "Castilla y León ofrece una deducción autonómica del 15% por compra de primera vivienda habitual para menores de 36 años en municipios <10.000 hab.",
            "reqs": ["Menor de 36 años", "Vivienda en municipio <10.000 hab.", "Base liquidable ≤ 18.900€ / conjunta ≤ 31.500€", "Máximo 9.000€ deducibles totales"],
        },
        "joven": {
            "tit": "Programa Rehabita Joven",
            "desc": "Ayudas a la compra de primera vivienda joven en zonas rurales con hasta 10.800€. Consulta tramitacastillayleon.jcyl.es."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Castilla y León. Tipo reducido 0,01% para jóvenes <36 y familia numerosa.",
    },
    "Cataluña": {
        "deduccion": {
            "tit": "Sin deducción autonómica vigente por compra",
            "desc": "Cataluña suprimió la deducción IRPF por compra de vivienda habitual. Permanecen ayudas al alquiler joven y deducciones por rehabilitación/discapacidad.",
            "reqs": ["Sin deducción IRPF general", "Sí ayudas al alquiler joven", "Consulta habitatge.gencat.cat"],
        },
        "joven": {
            "tit": "Bonificación AJD jóvenes Cataluña",
            "desc": "AJD reducido al 0,5% para jóvenes <32 que compren primera vivienda. Avales Catalunya 20% adicional al ICO para jóvenes."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Cataluña. ITP 10% en 2ª mano (11% para inmuebles >1M€).",
    },
    "C. Valenciana": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes y discapacidad",
            "desc": "Comunitat Valenciana permite deducir el 5% por adquisición de primera vivienda habitual para jóvenes <35 (hasta 102€/año), o el 5% para discapacitados (hasta 204€/año).",
            "reqs": ["Menor de 35 años", "Primera vivienda habitual", "Base liquidable ≤ 15.039€ / conjunta ≤ 21.483€"],
        },
        "joven": {
            "tit": "Plan EVha — Entitat Valenciana d'Habitatge",
            "desc": "Avales y ayudas adicionales al ICO para compra de primera vivienda joven. Consulta gva.es/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en C. Valenciana. ITP 10% en 2ª mano. Tipo reducido AJD 0,1% para jóvenes y familia numerosa.",
    },
    "Extremadura": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes y familias",
            "desc": "Extremadura ofrece deducción del 3% (hasta 540€) por compra de vivienda habitual para jóvenes <36, familias numerosas y discapacidad.",
            "reqs": ["Menor de 36 años, familia numerosa o discapacidad ≥65%", "Vivienda habitual", "Base liquidable ≤ 19.000€ individual"],
        },
        "joven": {
            "tit": "Plan Joven Extremadura",
            "desc": "Subvenciones de hasta 12.000€ para compra de primera vivienda joven en municipios pequeños. juntaex.es/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Extremadura. ITP escalado 8-11% en 2ª mano. Bonificación para jóvenes y vivienda habitual.",
    },
    "Galicia": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes vivienda protegida",
            "desc": "Galicia permite deducir el 15% de cantidades aportadas para compra de vivienda protegida habitual, hasta un máximo de 9.000€ totales.",
            "reqs": ["Vivienda protegida (VPO)", "Jóvenes <36 con bonificación adicional", "Base imponible máxima limitada"],
        },
        "joven": {
            "tit": "Bono Aluga Xove + ayuda compra rural",
            "desc": "Ayuda directa de hasta 10.800€ para compra de primera vivienda en municipios <10.000 hab. Información en igvs.xunta.gal."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Galicia. ITP general 9% (reducido a 8% en vivienda habitual jóvenes).",
    },
    "La Rioja": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes <36 zonas rurales",
            "desc": "La Rioja permite deducir el 5% por compra de vivienda habitual en municipios pequeños para menores de 36 años, hasta 452€.",
            "reqs": ["Menor de 36 años", "Vivienda en municipio <10.000 hab.", "Base liquidable conjunta ≤ 24.000€"],
        },
        "joven": {
            "tit": "Plan Vivienda Joven La Rioja",
            "desc": "Ayudas autonómicas al acceso a primera vivienda joven y avales propios. larioja.org/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1% en La Rioja. ITP 7% en 2ª mano (uno de los más bajos de España).",
    },
    "C. de Madrid": {
        "deduccion": {
            "tit": "Plan Vive Madrid + sin deducción IRPF",
            "desc": "C. de Madrid suprimió la deducción IRPF por compra. A cambio, mantiene ayudas directas: Plan Vive (vivienda en alquiler asequible) y Plan Mi Primera Vivienda (préstamos avalados al 95% para jóvenes <35).",
            "reqs": ["Jóvenes <35 para Mi Primera Vivienda", "Aval autonómico hasta el 15% adicional al ICO", "Ingresos máximos 4 IPREM"],
        },
        "joven": {
            "tit": "Mi Primera Vivienda Madrid",
            "desc": "Programa autonómico que avala hasta el 15% adicional al ICO para jóvenes <35 — total hasta 35% sin entrada. Vivienda hasta 390.000€. comunidad.madrid/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 0,75% en Madrid (uno de los más bajos). ITP 6% en 2ª mano. Bonificaciones para jóvenes y familia numerosa.",
    },
    "R. de Murcia": {
        "deduccion": {
            "tit": "Deducción IRPF jóvenes <35",
            "desc": "Región de Murcia permite deducir el 5% por compra de primera vivienda habitual para menores de 35 años, hasta 300€/año.",
            "reqs": ["Menor de 35 años", "Primera vivienda habitual", "Base imponible ≤ 24.107€ / conjunta ≤ 30.000€"],
        },
        "joven": {
            "tit": "Plan Vivienda Joven Murcia",
            "desc": "Ayudas autonómicas para compra de primera vivienda en jóvenes <35 — hasta 10.800€. carm.es/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 1,5% en Murcia. ITP 8% en 2ª mano. Bonificación AJD 0,1% para jóvenes y familia numerosa.",
    },
    "Navarra": {
        "deduccion": {
            "tit": "Deducción IRPF foral por vivienda habitual",
            "desc": "Navarra (régimen foral) permite deducir el 15% por compra de vivienda habitual, hasta 1.200€/año. Adicional 3% para jóvenes <30 y familias numerosas.",
            "reqs": ["Vivienda habitual (residencia efectiva)", "Base imponible máxima limitada", "Inscripción en el Registro de Compromiso de Compra"],
        },
        "joven": {
            "tit": "Ayudas a la emancipación joven Navarra",
            "desc": "Programa autonómico de ayudas a la compra para jóvenes <36 y subvenciones por rehabilitación. navarra.es/vivienda."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 0,5% en Navarra (régimen foral). ITP 6% en 2ª mano (uno de los más bajos).",
    },
    "País Vasco": {
        "deduccion": {
            "tit": "Deducción IRPF foral compra vivienda habitual",
            "desc": "País Vasco (régimen foral, 3 diputaciones forales) permite deducir el 18% por compra de vivienda habitual, base máxima 1.530€/año. Hay deducciones adicionales para <30 años y familias numerosas.",
            "reqs": ["Vivienda habitual del contribuyente", "Adquisición o préstamo hipotecario", "Límite base anual: 1.530€ (8.000€ acumulado por contribuyente)"],
        },
        "joven": {
            "tit": "Etxebide vivienda protegida + ayudas jóvenes",
            "desc": "Sistema vasco de vivienda protegida con precios tasados. Programa Etxebizidea para acceso joven con financiación adaptada. etxebide.euskadi.eus."
        },
        "iva": "IVA general 10% en vivienda nueva + AJD 0,5% (régimen foral). ITP 4% en vivienda habitual 2ª mano (más bajo de España).",
    },
    "Ceuta": {
        "deduccion": {
            "tit": "Deducción IRPF residentes en Ceuta",
            "desc": "Ceuta aplica la deducción general estatal del 60% en IRPF a residentes. La compra de vivienda habitual no tiene deducción específica adicional.",
            "reqs": ["Residencia efectiva en Ceuta", "Vivienda habitual del contribuyente", "Consulta con tu administración local"],
        },
        "joven": {
            "tit": "Plan Vivienda Ciudad de Ceuta",
            "desc": "Ayudas locales puntuales a la compra de primera vivienda para jóvenes. Consulta en ceuta.es."
        },
        "iva": "Ceuta aplica IPSI (no IVA) al 0,5% en vivienda nueva (uno de los tipos más bajos de España). ITP IPSI también reducido.",
    },
    "Melilla": {
        "deduccion": {
            "tit": "Deducción IRPF residentes en Melilla",
            "desc": "Melilla aplica la deducción general estatal del 60% en IRPF a residentes. No hay deducción autonómica específica por compra de vivienda habitual.",
            "reqs": ["Residencia efectiva en Melilla", "Vivienda habitual del contribuyente", "Consulta con tu administración local"],
        },
        "joven": {
            "tit": "Plan Vivienda Ciudad Autónoma de Melilla",
            "desc": "Ayudas locales puntuales a la compra de primera vivienda y rehabilitación. melilla.es."
        },
        "iva": "Melilla aplica IPSI (no IVA) en vivienda nueva (tipo bonificado). ITP IPSI 4-5% en 2ª mano.",
    },
}

# Fallback si una CCAA no aparece en el dict
FALLBACK = {
    "deduccion": {
        "tit": "Deducción IRPF autonómica",
        "desc": "Consulta con tu CCAA las deducciones autonómicas vigentes por compra de vivienda habitual para jóvenes, familias numerosas y otros colectivos.",
        "reqs": ["Consulta con tu CCAA para condiciones actualizadas"],
    },
    "joven": {
        "tit": "Programa de vivienda joven",
        "desc": "Consulta con tu CCAA las ayudas vigentes a la compra de primera vivienda para menores de 35 años."
    },
    "iva": "IVA general 10% en vivienda nueva + AJD variable según CCAA (típicamente 1-1,5%). Consulta con tu CCAA para tipos reducidos aplicables.",
}


# ---------- Block builder -----------------------------------------------

CSS_BLOCK = """<style>
.ayudas-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin:1.25rem 0}
.ayuda-card{background:var(--white,#fff);border:1px solid var(--border,#e2e8f0);border-radius:14px;padding:1.15rem 1.2rem;box-shadow:0 1px 3px rgba(0,0,0,.04);display:flex;flex-direction:column}
.ayuda-card.ayuda-estatal{border-left:3px solid var(--blue,#1a56db)}
.ayuda-card.ayuda-autonomico{border-left:3px solid var(--green,#059669)}
.ayuda-card.ayuda-joven{border-left:3px solid #d97706}
.ayuda-card.ayuda-iva{border-left:3px solid #7c3aed}
.ayuda-hdr{display:flex;align-items:center;gap:.55rem;margin-bottom:.55rem;flex-wrap:wrap}
.ayuda-tag{font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;padding:.22rem .55rem;border-radius:99px;background:#f1f5f9;color:var(--text2,#475569);border:1px solid var(--border,#e2e8f0)}
.ayuda-card.ayuda-estatal .ayuda-tag{background:#eff6ff;color:#1a56db;border-color:#bfdbfe}
.ayuda-card.ayuda-autonomico .ayuda-tag{background:#ecfdf5;color:#059669;border-color:#a7f3d0}
.ayuda-card.ayuda-joven .ayuda-tag{background:#fffbeb;color:#92400e;border-color:#fde68a}
.ayuda-card.ayuda-iva .ayuda-tag{background:#f3e8ff;color:#6d28d9;border-color:#ddd6fe}
.ayuda-tit{font-size:1rem;font-weight:800;color:var(--text,#0e1828);letter-spacing:-.02em;margin:0;line-height:1.25}
.ayuda-desc{font-size:.82rem;color:var(--text2,#475569);line-height:1.55;margin:.4rem 0 .65rem}
.ayuda-req{list-style:none;padding:0;margin:0}
.ayuda-req li{font-size:.74rem;color:var(--text2,#475569);padding:.28rem 0 .28rem 1rem;position:relative;line-height:1.45;border-top:1px solid var(--border,#e2e8f0)}
.ayuda-req li:first-child{border-top:none}
.ayuda-req li::before{content:"✓";position:absolute;left:0;color:var(--green,#059669);font-weight:700}
.ayuda-req li strong{color:var(--text,#0e1828)}
.ayudas-note{font-size:.72rem;color:var(--muted,#64748b);background:var(--white,#fff);border:1px solid var(--border,#e2e8f0);border-radius:8px;padding:.8rem 1rem;line-height:1.55;margin-top:.55rem}
@media(max-width:760px){.ayudas-grid{grid-template-columns:1fr}}
</style>
"""


def build_ayudas_block(city: str, ccaa: str) -> str:
    data = CCAA_AYUDAS.get(ccaa, FALLBACK)
    ded = data["deduccion"]
    jov = data["joven"]
    iva = data["iva"]
    reqs_html = "\n".join(f'        <li>{r}</li>' for r in ded["reqs"])
    return f'''
{CSS_BLOCK}<!-- AYUDAS PARA COMPRAR EN {ccaa.upper()} -->
  <div class="section" id="ayudas-compra">
    <div class="sec-hdr">
      <div class="sec-eye">Ayudas y financiación</div>
      <h2>Ayudas para comprar en {ccaa}</h2>
      <p>Programas estatales y autonómicos vigentes para comprador de primera vivienda en {city}.</p>
    </div>
    <div class="ayudas-grid">
      <div class="ayuda-card ayuda-estatal">
        <div class="ayuda-hdr">
          <span class="ayuda-tag">Estatal</span>
          <h3 class="ayuda-tit">Aval ICO 20% primera vivienda</h3>
        </div>
        <p class="ayuda-desc">Aval del Estado por el 20% del valor de la vivienda (hasta el 25% en familias con menores), permitiendo financiar hasta el 100% sin entrada propia. Programa vigente hasta 2027.</p>
        <ul class="ayuda-req">
          <li>Menor de 35 años <strong>o</strong> familia con menores a cargo</li>
          <li>Primera vivienda habitual</li>
          <li>Renta máxima: 4,5x IPREM anual (~37.800€ individual)</li>
          <li>Valor máximo vivienda: hasta 250.000€ (varía por zona ICO)</li>
        </ul>
      </div>
      <div class="ayuda-card ayuda-autonomico">
        <div class="ayuda-hdr">
          <span class="ayuda-tag">Autonómica · {ccaa}</span>
          <h3 class="ayuda-tit">{ded["tit"]}</h3>
        </div>
        <p class="ayuda-desc">{ded["desc"]}</p>
        <ul class="ayuda-req">
{reqs_html}
        </ul>
      </div>
      <div class="ayuda-card ayuda-joven">
        <div class="ayuda-hdr">
          <span class="ayuda-tag">Hipoteca joven · {ccaa}</span>
          <h3 class="ayuda-tit">{jov["tit"]}</h3>
        </div>
        <p class="ayuda-desc">{jov["desc"]}</p>
      </div>
      <div class="ayuda-card ayuda-iva">
        <div class="ayuda-hdr">
          <span class="ayuda-tag">Vivienda nueva</span>
          <h3 class="ayuda-tit">IVA y AJD aplicables</h3>
        </div>
        <p class="ayuda-desc">{iva}</p>
      </div>
    </div>
    <p class="ayudas-note"><strong>Importante:</strong> los importes, requisitos y condiciones pueden variar cada año fiscal y dependen de tu situación personal. Esta página es informativa, no constituye asesoramiento fiscal ni jurídico. Antes de solicitar cualquier ayuda, consulta la convocatoria vigente en la web oficial de {ccaa} o con un asesor.</p>
  </div>

'''


# ---------- FAQ comprador (índices 10, 11, 12) --------------------------

def build_faq_extra(city: str, ccaa: str, precio_piso: int) -> str:
    data = CCAA_AYUDAS.get(ccaa, FALLBACK)
    q10 = (
        '<div class="faq-item" onclick="toggleFaq(10)">\n'
        '  <div class="faq-q" id="fq-10">\n'
        f'    <span>¿Qué ayudas existen para comprar piso en {ccaa}?</span>\n'
        '    <svg class="faq-arrow" id="fa-10" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
        '  </div>\n'
        f'  <div class="faq-a" id="fa-body-10">Las principales ayudas para comprar una vivienda en {ccaa} son tres: (1) <strong>Aval ICO 20% estatal</strong> para jóvenes &lt;35 o familias con menores, que evita aportar entrada; (2) <strong>{data["deduccion"]["tit"]}</strong>: {data["deduccion"]["desc"]}; (3) <strong>{data["joven"]["tit"]}</strong>: {data["joven"]["desc"]} Revisa el bloque "Ayudas para comprar en {ccaa}" más arriba para detalles, requisitos y enlaces oficiales.</div>\n'
        '</div>'
    )
    q11 = (
        '<div class="faq-item" onclick="toggleFaq(11)">\n'
        '  <div class="faq-q" id="fq-11">\n'
        f'    <span>¿Cuánto tiempo tarda el proceso de compra en {city}?</span>\n'
        '    <svg class="faq-arrow" id="fa-11" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
        '  </div>\n'
        f'  <div class="faq-a" id="fa-body-11">El proceso completo de compra en {city} (como en el resto de España) suele tardar entre <strong>6 y 10 semanas</strong> desde la firma de arras hasta la escritura ante notario: 1-2 semanas para due diligence (nota simple, ITE, certificado energético), 4-6 semanas para tramitar la hipoteca y tasación, y 1-2 semanas adicionales para coordinar firma con notario y registro. Si la operación es al contado el plazo se reduce a 3-5 semanas. Días en mercado de {city}: consulta el indicador "Días en mercado" más arriba — refleja la velocidad de venta media.</div>\n'
        '</div>'
    )
    q12 = (
        '<div class="faq-item" onclick="toggleFaq(12)">\n'
        '  <div class="faq-q" id="fq-12">\n'
        f'    <span>¿Es mejor comprar obra nueva o segunda mano en {city}?</span>\n'
        '    <svg class="faq-arrow" id="fa-12" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
        '  </div>\n'
        f'  <div class="faq-a" id="fa-body-12">Cada opción tiene ventajas según tu perfil. <strong>Obra nueva</strong> en {city}: paga IVA 10% + AJD (típicamente 1-1,5% según {ccaa}), garantía decenal del promotor, certificado energético A/B con menores facturas, sin obras pendientes. Suele ser <strong>10-25% más cara</strong> que la segunda mano comparable. <strong>Segunda mano</strong>: paga ITP (varía del 4% en País Vasco al 10% en Cataluña/C. Valenciana), entrega inmediata, suele estar mejor ubicada (cascos históricos, barrios consolidados), pero requiere inspección técnica si tiene &gt;20 años y posibles reformas. Para vivienda habitual a largo plazo, la segunda mano céntrica suele ser más eficiente; para inversión en alquiler turístico o familias jóvenes, la obra nueva en zonas en crecimiento tiene más sentido.</div>\n'
        '</div>'
    )
    return q10 + q11 + q12


# ---------- Transform ---------------------------------------------------

def transform_ficha(html: str, slug: str) -> tuple[str, dict]:
    info = {"slug": slug, "ok": False}

    m_city = RE_CITY.search(html)
    m_ccaa = RE_CCAA.search(html)
    m_piso = RE_PISO.search(html)
    if not (m_city and m_ccaa and m_piso):
        info["error"] = (
            f"missing city={bool(m_city)} ccaa={bool(m_ccaa)} piso={bool(m_piso)}"
        )
        return html, info

    city = m_city.group(1).strip()
    ccaa = m_ccaa.group(1).strip()
    precio_piso = int(m_piso.group(1))

    info.update(city=city, ccaa=ccaa)

    out = html
    n_ayudas = 0
    n_faq = 0

    # BLOQUE 1: insertar bloque ayudas antes de <!-- FAQ -->
    if HAS_AYUDAS_TOKEN not in out:
        block = build_ayudas_block(city, ccaa)
        new_out, n_ayudas = RE_FAQ_BLOCK_START.subn(
            lambda mm: block + mm.group(1), out, count=1
        )
        if n_ayudas == 1:
            out = new_out

    # BLOQUE 4: insertar 3 FAQ comprador
    if HAS_NEW_FAQ_TOKEN not in out:
        faqs = build_faq_extra(city, ccaa, precio_piso)
        new_out, n_faq = RE_FAQ_CLOSE.subn(
            lambda mm: mm.group(1) + faqs + mm.group(2), out, count=1
        )
        if n_faq == 1:
            out = new_out

    info["ayudas"] = n_ayudas
    info["faq"] = n_faq
    info["ok"] = (
        (n_ayudas == 1 or HAS_AYUDAS_TOKEN in html) and
        (n_faq == 1 or HAS_NEW_FAQ_TOKEN in html)
    )
    return out, info


# ---------- Driver ------------------------------------------------------

def main(argv: list[str]) -> int:
    only = set(argv[1:])

    files = sorted(FICHAS_DIR.glob("rentabilidad-*.html"))
    if only:
        files = [f for f in files if f.stem in only]

    ok = 0
    skipped = []
    fail = []

    for path in files:
        slug = path.stem.removeprefix("rentabilidad-")
        try:
            html = path.read_text(encoding="utf-8")
            # Skip article-style files (no banner-title or hi-precio)
            if 'class="banner-title"' not in html or 'id="hi-precio"' not in html:
                skipped.append(slug)
                continue
            new, info = transform_ficha(html, slug)
            if info["ok"] and new != html:
                path.write_text(new, encoding="utf-8")
                ok += 1
            elif info["ok"]:
                ok += 1
            else:
                fail.append(info)
        except Exception as e:  # noqa
            fail.append({"slug": slug, "error": repr(e)})

    print(f"Processed: {ok}/{len(files)} fichas OK")
    if skipped:
        print(f"Skipped (no ficha template): {len(skipped)} - {skipped[:3]}")
    if fail:
        print(f"FAILURES ({len(fail)}):")
        for f in fail[:20]:
            print("  ", f)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
