#!/usr/bin/env python3
"""Genera las 10 fichas de la provincia de Málaga (expansión julio 2026).

Reutiliza generate_41_fichas.generate_one y después sustituye el editorial
y la Perspectiva Ren Data por textos únicos escritos a mano (campos `ed`
y `persp` del metadata JSON). Ajusta la fecha del banner a Julio 2026 y
garantiza el bloque Dataset en el JSON-LD.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_malaga_metadata.json"

sys.path.insert(0, str(Path(__file__).parent / "archive"))
import generate_41_fichas as g41  # noqa: E402
g41.ROOT = ROOT
g41.BETA = BETA
from generate_41_fichas import generate_one, fmt_eu, fmt_pct  # noqa: E402


def find_div_block(html, start_marker):
    si = html.find(start_marker)
    if si == -1:
        return None, None
    pos = si
    depth = 0
    while pos < len(html):
        no = html.find("<div", pos)
        nc = html.find("</div>", pos)
        if nc == -1:
            return None, None
        if no != -1 and no < nc:
            depth += 1
            pos = no + 4
        else:
            depth -= 1
            pos = nc + 6
            if depth == 0:
                return si, pos
    return None, None


def custom_ed_body(city):
    stats = (
        f'<div class="ed-stat"><div class="ed-stat-val">{fmt_pct(city["roi"])}%</div><div class="ed-stat-lbl">rentabilidad bruta</div></div>'
        f'<div class="ed-stat"><div class="ed-stat-val">{fmt_eu(city["precio"])}€</div><div class="ed-stat-lbl">precio medio m²</div></div>'
        f'<div class="ed-stat"><div class="ed-stat-val">{fmt_eu(city["alq"])}€/mes</div><div class="ed-stat-lbl">alquiler medio</div></div>'
        f'<div class="ed-stat"><div class="ed-stat-val">{city["dias"]}</div><div class="ed-stat-lbl">días media venta</div></div>'
    )
    paras = "\n".join(f"      <p>{p}</p>" for p in city["ed"])
    tags_html = "".join(f'<span class="ed-tag">{t}</span>' for t in city["tags"])
    alts = " · ".join(
        f'<a href="/rentabilidad-{slug}.html" style="color:var(--blue);text-decoration:none;font-weight:600">{n}</a>'
        for n, slug in city["alt"]
    )
    return (
        '<div class="ed-body">\n'
        f'      <div class="ed-highlight">\n        {stats}\n      </div>\n'
        f'{paras}\n'
        f'      <p>{tags_html}</p>\n'
        f'      <p style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border);font-size:.85rem"><strong>Ciudades alternativas:</strong> {alts}</p>\n'
        '    </div>'
    )


def replace_ed_body_custom(html, city):
    si, end = find_div_block(html, '<div class="ed-body">')
    if si is None:
        print(f"  [warn] {city['slug']}: no ed-body found")
        return html
    return html[:si] + custom_ed_body(city) + html[end:]


def replace_perspectiva_custom(html, city):
    new_p = f'<div class="tend-perspectiva">💡 <strong>Perspectiva Ren Data:</strong> {city["persp"]}</div>'
    out, n = re.subn(r'<div class="tend-perspectiva">.*?</div>', new_p, html, count=1, flags=re.DOTALL)
    if n == 0:
        print(f"  [warn] {city['slug']}: no tend-perspectiva found")
    return out


def ensure_dataset(html, c):
    if '"@type":"Dataset"' in html:
        return html
    name = c["name"]
    ccaa = c["ccaa"]
    dataset = (
        ',{\n'
        '  "@context":"https://schema.org",\n'
        f'  "@type":"Dataset","name":"Mercado inmobiliario {name} 2026",'
        f'"description":"Datos de precio m², rentabilidad por alquiler y evolución del mercado inmobiliario en {name}, {ccaa}.",'
        f'"keywords":["rentabilidad inmobiliaria {name}","precio vivienda {name}","invertir {name}","alquiler {name}"],'
        f'"temporalCoverage":"2026",'
        f'"spatialCoverage":"{name}, {ccaa}, España",'
        f'"publisher":{{"@type":"Organization","name":"Ren Data","url":"https://rendata.es"}}\n'
        '}'
    )
    new_html, n = re.subn(r'(\})(\s*)(\]</script>)', rf'\g<1>{dataset}\g<2>\g<3>', html, count=1)
    return new_html if n else html


def fix_dates(html):
    for old in ("Mayo 2026", "Junio 2026"):
        html = html.replace(old, "Julio 2026")
    return html


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    available = {p.stem.replace("rentabilidad-", "") for p in BETA.glob("rentabilidad-*.html")}
    ok = err = 0
    for city in cities:
        if city["twin"] not in available:
            print(f"[ERROR] {city['slug']}: twin '{city['twin']}' no existe")
            err += 1
            continue
        try:
            html = generate_one(city)
            html = replace_ed_body_custom(html, city)
            html = replace_perspectiva_custom(html, city)
            html = ensure_dataset(html, city)
            html = fix_dates(html)
            out = BETA / f"rentabilidad-{city['slug']}.html"
            out.write_text(html, encoding="utf-8")
            print(f"[ok] {city['slug']} (twin {city['twin']}, {html.count(chr(10))+1} líneas)")
            ok += 1
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ERROR] {city['slug']}: {e}")
            err += 1
    print(f"\n=== OK={ok} ERR={err} ===")


if __name__ == "__main__":
    main()
