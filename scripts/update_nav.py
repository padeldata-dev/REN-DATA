#!/usr/bin/env python3
"""
Migración masiva de navegación para rendata_beta/.
- Reemplaza <nav>...</nav> con bloque canónico unificado
- Inyecta <link href="/css/nav.css"> al final del <head> si no existe
- Inyecta <script src="/js/nav-dropdown.js" defer> si no existe
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "rendata_beta"

CANONICAL_NAV = '''<nav>
    <button class="mob-menu-btn" onclick="this.closest('nav').classList.toggle('open')" aria-label="Menú" aria-expanded="false">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
    <div class="mob-nav-links">
      <a href="/">🏠 Ciudades</a>
      <a href="/ranking.html">📊 Ranking</a>
      <a href="/analisis.html">📈 Análisis</a>
      <a href="/comparador.html">⚖️ Comparar</a>
      <a href="/glosario.html">📖 Glosario</a>
      <a href="/guia-inversor.html">🎯 Guía inversor</a>
      <a href="/sobre.html">ℹ️ Sobre</a>
      <details class="mob-nav-details">
        <summary>🗺️ Comunidades</summary>
        <a href="/ccaa-andalucia.html"><img src="/img/flags/andalucia.png" class="nav-flag" alt="" loading="lazy"> Andalucía</a>
        <a href="/ccaa-aragon.html"><img src="/img/flags/aragon.png" class="nav-flag" alt="" loading="lazy"> Aragón</a>
        <a href="/ccaa-asturias.html"><img src="/img/flags/asturias.png" class="nav-flag" alt="" loading="lazy"> Asturias</a>
        <a href="/ccaa-baleares.html"><img src="/img/flags/baleares.png" class="nav-flag" alt="" loading="lazy"> Baleares</a>
        <a href="/ccaa-canarias.html"><img src="/img/flags/canarias.png" class="nav-flag" alt="" loading="lazy"> Canarias</a>
        <a href="/ccaa-cantabria.html"><img src="/img/flags/cantabria.png" class="nav-flag" alt="" loading="lazy"> Cantabria</a>
        <a href="/ccaa-castilla-la-mancha.html"><img src="/img/flags/castilla-la-mancha.png" class="nav-flag" alt="" loading="lazy"> Castilla-La Mancha</a>
        <a href="/ccaa-castilla-y-leon.html"><img src="/img/flags/castilla-y-leon.png" class="nav-flag" alt="" loading="lazy"> Castilla y León</a>
        <a href="/ccaa-cataluna.html"><img src="/img/flags/cataluna.png" class="nav-flag" alt="" loading="lazy"> Cataluña</a>
        <a href="/ccaa-comunitat-valenciana.html"><img src="/img/flags/comunitat-valenciana.png" class="nav-flag" alt="" loading="lazy"> C. Valenciana</a>
        <a href="/ccaa-extremadura.html"><img src="/img/flags/extremadura.png" class="nav-flag" alt="" loading="lazy"> Extremadura</a>
        <a href="/ccaa-galicia.html"><img src="/img/flags/galicia.png" class="nav-flag" alt="" loading="lazy"> Galicia</a>
        <a href="/ccaa-la-rioja.html"><img src="/img/flags/la-rioja.png" class="nav-flag" alt="" loading="lazy"> La Rioja</a>
        <a href="/ccaa-madrid.html"><img src="/img/flags/madrid.png" class="nav-flag" alt="" loading="lazy"> Madrid</a>
        <a href="/ccaa-murcia.html"><img src="/img/flags/murcia.png" class="nav-flag" alt="" loading="lazy"> Murcia</a>
        <a href="/ccaa-navarra.html"><img src="/img/flags/navarra.png" class="nav-flag" alt="" loading="lazy"> Navarra</a>
        <a href="/ccaa-pais-vasco.html"><img src="/img/flags/pais-vasco.png" class="nav-flag" alt="" loading="lazy"> País Vasco</a>
      </details>
    </div>
    <a href="/">Ciudades</a>
    <a href="/ranking.html">Ranking</a>
    <a href="/analisis.html">Análisis</a>
    <div class="nav-dropdown">
      <button class="nav-drop-btn" type="button" aria-expanded="false">Comunidades ▾</button>
      <div class="nav-drop-menu">
        <a href="/ccaa-andalucia.html"><img src="/img/flags/andalucia.png" class="nav-flag" alt="" loading="lazy"> Andalucía</a>
        <a href="/ccaa-madrid.html"><img src="/img/flags/madrid.png" class="nav-flag" alt="" loading="lazy"> Madrid</a>
        <a href="/ccaa-cataluna.html"><img src="/img/flags/cataluna.png" class="nav-flag" alt="" loading="lazy"> Cataluña</a>
        <a href="/ccaa-comunitat-valenciana.html"><img src="/img/flags/comunitat-valenciana.png" class="nav-flag" alt="" loading="lazy"> C. Valenciana</a>
        <a href="/ccaa-canarias.html"><img src="/img/flags/canarias.png" class="nav-flag" alt="" loading="lazy"> Canarias</a>
        <a href="/ccaa-baleares.html"><img src="/img/flags/baleares.png" class="nav-flag" alt="" loading="lazy"> Baleares</a>
        <a href="/ccaa-pais-vasco.html"><img src="/img/flags/pais-vasco.png" class="nav-flag" alt="" loading="lazy"> País Vasco</a>
        <a href="/ccaa-galicia.html"><img src="/img/flags/galicia.png" class="nav-flag" alt="" loading="lazy"> Galicia</a>
        <a href="/ccaa-castilla-y-leon.html"><img src="/img/flags/castilla-y-leon.png" class="nav-flag" alt="" loading="lazy"> Castilla y León</a>
        <a href="/ccaa-aragon.html"><img src="/img/flags/aragon.png" class="nav-flag" alt="" loading="lazy"> Aragón</a>
        <a href="/ccaa-murcia.html"><img src="/img/flags/murcia.png" class="nav-flag" alt="" loading="lazy"> Murcia</a>
        <a href="/ccaa-castilla-la-mancha.html"><img src="/img/flags/castilla-la-mancha.png" class="nav-flag" alt="" loading="lazy"> Castilla-La Mancha</a>
        <a href="/ccaa-extremadura.html"><img src="/img/flags/extremadura.png" class="nav-flag" alt="" loading="lazy"> Extremadura</a>
        <a href="/ccaa-asturias.html"><img src="/img/flags/asturias.png" class="nav-flag" alt="" loading="lazy"> Asturias</a>
        <a href="/ccaa-cantabria.html"><img src="/img/flags/cantabria.png" class="nav-flag" alt="" loading="lazy"> Cantabria</a>
        <a href="/ccaa-navarra.html"><img src="/img/flags/navarra.png" class="nav-flag" alt="" loading="lazy"> Navarra</a>
        <a href="/ccaa-la-rioja.html"><img src="/img/flags/la-rioja.png" class="nav-flag" alt="" loading="lazy"> La Rioja</a>
      </div>
    </div>
    <a href="/comparador.html">Comparador</a>
    <a href="/glosario.html">Glosario</a>
    <a href="/guia-inversor.html">Guía</a>
    <a href="/sobre.html">Sobre</a>
  </nav>'''

NAV_CSS_LINK = '<link rel="stylesheet" href="/css/nav.css">'
NAV_JS_SCRIPT = '<script src="/js/nav-dropdown.js" defer></script>'

NAV_RE = re.compile(r"<nav\b[^>]*>.*?</nav>", re.DOTALL | re.IGNORECASE)
HEAD_END_RE = re.compile(r"</head>", re.IGNORECASE)


def process_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    original = text
    actions = []

    # 1) Replace <nav>...</nav>
    matches = NAV_RE.findall(text)
    if matches:
        text = NAV_RE.sub(CANONICAL_NAV, text, count=1)
        # If multiple nav tags (rare), warn
        if len(matches) > 1:
            actions.append(f"WARN: {len(matches)} nav tags found, only first replaced")
        else:
            actions.append("nav-replaced")
    else:
        actions.append("WARN: no nav found")

    # 2) Inject nav.css link if not present
    if 'href="/css/nav.css"' not in text and "href='/css/nav.css'" not in text:
        text = HEAD_END_RE.sub(f"{NAV_CSS_LINK}\n</head>", text, count=1)
        actions.append("nav-css-injected")

    # 3) Inject nav-dropdown.js if not present
    if 'src="/js/nav-dropdown.js"' not in text and "src='/js/nav-dropdown.js'" not in text:
        text = HEAD_END_RE.sub(f"{NAV_JS_SCRIPT}\n</head>", text, count=1)
        actions.append("nav-js-injected")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return {"path": str(path.relative_to(ROOT)), "actions": actions, "changed": True}
    return {"path": str(path.relative_to(ROOT)), "actions": actions, "changed": False}


def main():
    if not ROOT.is_dir():
        print(f"ERROR: {ROOT} not found", file=sys.stderr)
        sys.exit(1)

    html_files = sorted(ROOT.glob("*.html"))
    total = len(html_files)
    changed = 0
    warnings = []
    print(f"Found {total} HTML files in {ROOT}")

    for p in html_files:
        r = process_file(p)
        if r["changed"]:
            changed += 1
        for a in r["actions"]:
            if a.startswith("WARN"):
                warnings.append(f"{r['path']}: {a}")

    print(f"Changed: {changed}/{total}")
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")


if __name__ == "__main__":
    main()
