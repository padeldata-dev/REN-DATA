#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calcula el Semáforo del Mercado Ren Data y genera semaforo-mercado.html.

Metodología (100% a partir de datos propios, ver semaforo-mercado.html):
- 40% Accesibilidad (índice Ren Data de Accesibilidad, invertido: menos accesible = más "caliente")
- 35% Variación de precio interanual media nacional (0% = frío, 15% = muy caliente)
- 25% Días en mercado media nacional (invertido: menos días = más "caliente")
Escala de temperatura 0-100. 0-33 verde, 34-66 amarillo, 67-100 rojo.
"""
import csv
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
SCRATCH = Path(r"C:\Users\Usuario\AppData\Local\Temp\claude\C--Users-Usuario-REN-DATA\209ab947-f175-4d83-8ecb-870b342fced2\scratchpad")
HEADER = (SCRATCH / "header.html").read_text(encoding="utf-8")
FOOTER = (SCRATCH / "footer.html").read_text(encoding="utf-8")

DATASET_PATH = ROOT / "data" / "semaforo_mercado.json"
HOY = "2026-07-13"
MES_LABEL = "Julio 2026"


def clamp(x, lo=0, hi=100):
    return max(lo, min(hi, x))


def compute():
    rows = list(csv.DictReader(open(ROOT / "pipeline/data/cities_master.csv", encoding="utf-8")))
    var_precio = [float(r["var_precio_anual"]) for r in rows if r["var_precio_anual"]]
    dias = [float(r["dias_mercado"]) for r in rows if r["dias_mercado"]]
    var_precio_media = sum(var_precio) / len(var_precio)
    dias_media = sum(dias) / len(dias)

    idx = json.load(open(ROOT / "data/indice_accesibilidad.json", encoding="utf-8"))
    indice_accesibilidad = idx["media_ponderada"]

    temp_accesibilidad = clamp(100 - indice_accesibilidad)
    temp_precio = clamp(var_precio_media / 15 * 100)
    temp_dias = clamp((40 - dias_media) / (40 - 10) * 100)

    W_ACC, W_PRECIO, W_DIAS = 0.40, 0.35, 0.25
    temperatura = W_ACC * temp_accesibilidad + W_PRECIO * temp_precio + W_DIAS * temp_dias
    temperatura = round(temperatura, 1)

    if temperatura <= 33:
        color, label_short = "verde", "Mercado favorable al comprador"
    elif temperatura <= 66:
        color, label_short = "amarillo", "Mercado neutral"
    else:
        color, label_short = "rojo", "Mercado favorable al vendedor (caro)"

    return {
        "fecha": HOY,
        "mes_label": MES_LABEL,
        "temperatura": temperatura,
        "color": color,
        "label": label_short,
        "componentes": {
            "indice_accesibilidad": indice_accesibilidad,
            "temp_accesibilidad": round(temp_accesibilidad, 1),
            "var_precio_anual_media": round(var_precio_media, 2),
            "temp_precio": round(temp_precio, 1),
            "dias_mercado_media": round(dias_media, 1),
            "temp_dias": round(temp_dias, 1),
            "n_ciudades": len(rows),
        },
        "pesos": {"accesibilidad": W_ACC, "variacion_precio": W_PRECIO, "dias_mercado": W_DIAS},
    }


def update_dataset(entry):
    if DATASET_PATH.exists():
        data = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    else:
        data = {"historial": []}
    data["historial"] = [h for h in data["historial"] if h["fecha"] != entry["fecha"]]
    data["historial"].append(entry)
    data["historial"].sort(key=lambda h: h["fecha"])
    DATASET_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


COLOR_DOT = {"verde": "g", "amarillo": "y", "rojo": "r"}
COLOR_EMOJI = {"verde": "🟢", "amarillo": "🟡", "rojo": "🔴"}
MARKER_POS = {"verde": 16.5, "amarillo": 50, "rojo": 83.5}


def historial_rows(historial):
    rows = []
    for h in reversed(historial):
        emoji = COLOR_EMOJI[h["color"]]
        rows.append(
            f'<tr><td>{h["mes_label"]}</td><td>{h["temperatura"]}/100</td>'
            f'<td>{emoji} {h["label"]}</td>'
            f'<td>{h["componentes"]["indice_accesibilidad"]}</td>'
            f'<td>+{h["componentes"]["var_precio_anual_media"]}%</td>'
            f'<td>{h["componentes"]["dias_mercado_media"]} días</td></tr>'
        )
    return "".join(rows)


def build_page(entry, historial):
    c = entry["componentes"]
    dot = COLOR_DOT[entry["color"]]
    emoji = COLOR_EMOJI[entry["color"]]
    marker = MARKER_POS[entry["color"]]

    desc = (
        f"Semáforo Ren Data del mercado inmobiliario español: {emoji} {entry['label']} "
        f"({entry['temperatura']}/100) en {entry['mes_label']}. Metodología abierta a partir de "
        f"datos propios de accesibilidad, variación de precio y días en mercado."
    )

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="{desc}">
<title>Semáforo Ren Data del Mercado Inmobiliario — {entry['mes_label']} | Ren Data</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Ren Data">
<meta property="og:title" content="Semáforo Ren Data del Mercado Inmobiliario">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://rendata.es/semaforo-mercado"><meta property="og:image" content="https://rendata.es/img/logo-rendata-transparente.png"><meta property="og:image:width" content="512"><meta property="og:image:height" content="512">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Semáforo Ren Data del Mercado Inmobiliario">
<meta name="twitter:description" content="{desc}">
<link rel="canonical" href="https://rendata.es/semaforo-mercado">
<link rel="stylesheet" href="/css/fonts.css">
<link rel="stylesheet" href="/css/semaforo.css">
<link rel="stylesheet" href="/css/nav.css">
<script src="/js/nav-dropdown.js" defer></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-0M57323B51");</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6236025065305645" crossorigin="anonymous"></script>
<script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "Semáforo Ren Data del Mercado Inmobiliario",
  "description": "Indicador mensual 0-100 de temperatura del mercado inmobiliario español, combinando el índice de accesibilidad Ren Data (40%), la variación de precio interanual media (35%) y los días en mercado medios (25%) de {c['n_ciudades']} ciudades.",
  "url": "https://rendata.es/semaforo-mercado",
  "keywords": ["semáforo mercado inmobiliario", "temperatura mercado vivienda España", "indicador precio vivienda"],
  "creator": {{"@type": "Organization", "name": "Ren Data", "url": "https://rendata.es/"}},
  "license": "https://rendata.es/aviso-legal.html",
  "temporalCoverage": "{entry['fecha']}",
  "spatialCoverage": {{"@type": "Place", "name": "España"}},
  "variableMeasured": ["Temperatura del mercado (0-100)", "Índice de accesibilidad", "Variación de precio interanual", "Días en mercado"]
}}</script>
</head>
<body>

<header>
  <a href="/" class="logo"><img src="/img/logo-rendata-transparente.png" height="32" alt="REN DATA"></a>
  {HEADER}
</header>

<section class="sem-hero">
  <div class="sem-hero-inner">
    <div class="sem-eyebrow">🚦 Indicador insignia · Ren Data</div>
    <h1>Semáforo Ren Data del Mercado Inmobiliario</h1>
    <p>Un solo número (0-100) que resume si, ahora mismo, el mercado español favorece a quien compra o a quien vende. Metodología 100% propia y transparente, actualizada mensualmente.</p>
    <div class="sem-badge-big">
      <div class="sem-dot {dot}"></div>
      <div class="sem-badge-text">
        <div class="sem-badge-label">{emoji} {entry['label']}</div>
        <div class="sem-badge-sub">Temperatura {entry['temperatura']}/100 · {entry['mes_label']}</div>
      </div>
    </div>
  </div>
</section>

<div class="sem-wrap">

  <h2 id="que-es">Qué mide este indicador</h2>
  <p class="lead">El Semáforo combina tres señales propias de Ren Data en un único número de 0 (mercado muy frío, favorable al comprador) a 100 (mercado muy caliente, favorable al vendedor y caro): la accesibilidad media a la vivienda, cuánto ha subido el precio en el último año, y cuánto tarda en venderse una vivienda media. No sustituye el análisis de tu ciudad concreta — para eso están las <a href="/ranking.html">587 fichas de ciudad</a> — pero da una foto rápida del momento del mercado a nivel nacional.</p>

  <div class="sem-scale">
    <div class="sem-scale-seg g">{"📍" if entry['color']=="verde" else ""}<br>0-33<br>🟢 Frío / comprador</div>
    <div class="sem-scale-seg y">{"📍" if entry['color']=="amarillo" else ""}<br>34-66<br>🟡 Neutral</div>
    <div class="sem-scale-seg r">{"📍" if entry['color']=="rojo" else ""}<br>67-100<br>🔴 Caliente / vendedor</div>
  </div>

  <h2 id="metodologia">Metodología completa</h2>
  <p>La temperatura se calcula combinando tres componentes, cada uno normalizado a una escala de 0 a 100 y ponderado:</p>

  <div class="sem-formula">
    <div class="sem-formula-eq">Temperatura = 0,40 × Temp_accesibilidad + 0,35 × Temp_precio + 0,25 × Temp_dias</div>
    <div class="sem-comp">
      <div class="sem-comp-card">
        <div class="sem-comp-w">40%</div>
        <div class="sem-comp-t">Accesibilidad (invertida)</div>
        <div class="sem-comp-d">100 − <a href="/indice-accesibilidad-vivienda.html">Índice Ren Data de Accesibilidad</a>. A menor accesibilidad, más "caliente" el mercado.</div>
        <div class="sem-comp-val">Índice actual: {c['indice_accesibilidad']}/100 → Temp {c['temp_accesibilidad']}</div>
      </div>
      <div class="sem-comp-card">
        <div class="sem-comp-w">35%</div>
        <div class="sem-comp-t">Variación de precio interanual</div>
        <div class="sem-comp-d">Media nacional de la variación de precio a 1 año de {c['n_ciudades']} ciudades. Escala lineal: 0% = 0 puntos, 15% = 100 puntos.</div>
        <div class="sem-comp-val">Media actual: +{c['var_precio_anual_media']}% → Temp {c['temp_precio']}</div>
      </div>
      <div class="sem-comp-card">
        <div class="sem-comp-w">25%</div>
        <div class="sem-comp-t">Días en mercado (invertido)</div>
        <div class="sem-comp-d">Media nacional de días que tarda en venderse una vivienda. Escala lineal invertida: 40 días = 0 puntos, 10 días = 100 puntos.</div>
        <div class="sem-comp-val">Media actual: {c['dias_mercado_media']} días → Temp {c['temp_dias']}</div>
      </div>
    </div>
  </div>

  <p>Los tres componentes usan exclusivamente <strong>datos propios de Ren Data</strong>: el mismo dataset de precio, alquiler y días en mercado de {c['n_ciudades']} ciudades que alimenta cada ficha individual, y el mismo <a href="/indice-accesibilidad-vivienda.html">Índice de Accesibilidad</a> ya publicado. No usamos ninguna fuente externa adicional para este cálculo — lo que permite total transparencia y trazabilidad de cada número.</p>

  <h2 id="historial">Seguimiento histórico</h2>
  <div class="sem-table-wrap">
  <table class="sem-table">
    <thead><tr><th>Mes</th><th>Temperatura</th><th>Estado</th><th>Índice accesibilidad</th><th>Var. precio media</th><th>Días mercado media</th></tr></thead>
    <tbody>{historial_rows(historial)}</tbody>
  </table>
  </div>
  <p style="font-size:.85rem;color:var(--muted)">Este indicador se publicó por primera vez en {entry['mes_label']}, por lo que el historial empieza en ese mes. Se actualizará cada vez que se actualice el dataset trimestral de Ren Data.</p>

  <div class="sem-note">
    <strong>⚠️ Cómo interpretarlo:</strong> un valor "neutral" (34-66) no significa que no pase nada — significa que las tres señales apuntan en direcciones distintas o moderadas. En este caso, la accesibilidad nacional es intermedia (58,6/100), el precio sube con fuerza (+{c['var_precio_anual_media']}% de media) pero las viviendas tardan en venderse un tiempo moderado ({c['dias_mercado_media']} días de media), lo que compensa parcialmente la señal de precio.
  </div>

  <h2 id="limitaciones">Limitaciones, con transparencia total</h2>
  <ul style="font-size:.95rem;color:var(--text2);line-height:1.85;padding-left:1.3rem">
    <li>Es un <strong>promedio nacional simple</strong> sobre {c['n_ciudades']} ciudades: no pondera por población, por lo que ciudades pequeñas pesan igual que Madrid o Barcelona en la media de precio y días en mercado.</li>
    <li>Los <strong>días en mercado</strong> son una estimación del dataset propio de Ren Data, no un dato oficial del Colegio de Registradores ni de portales inmobiliarios.</li>
    <li>No incorpora tipos de interés ni condiciones de acceso al crédito (más allá de lo que ya recoge el Índice de Accesibilidad) como componente independiente.</li>
    <li>Los umbrales de las escalas (0-15% en precio, 10-40 días en mercado) son un criterio propio de Ren Data, razonado pero no un estándar del sector — los explicamos aquí precisamente para que puedas juzgar si te parecen razonables.</li>
  </ul>

  <div class="sem-src">
    <strong>Fuentes:</strong> precio, alquiler y días en mercado — dataset propio de Ren Data, {entry['mes_label']}. Accesibilidad — <a href="/indice-accesibilidad-vivienda.html">Índice Ren Data de Accesibilidad a la Vivienda</a>. Este indicador es una herramienta de contexto informativo, no un indicador oficial ni un sustituto de asesoramiento financiero o inmobiliario.
  </div>

</div>
<footer>
{FOOTER}
</footer>

</body>
</html>
"""
    return html


def main():
    entry = compute()
    data = update_dataset(entry)
    page = build_page(entry, data["historial"])
    (BETA / "semaforo-mercado.html").write_text(page, encoding="utf-8")
    print(json.dumps(entry, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
