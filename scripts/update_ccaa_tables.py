#!/usr/bin/env python3
"""Inserta las nuevas ciudades en las tablas ccaa-*.html en posicion ordenada por ROI.

Idempotente: si la ciudad ya existe en la tabla, no la duplica.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"

# (slug, name, ccaa-page-file, precio, alq, roi, dias)
ADDITIONS = [
    ("santa-coloma-de-gramenet", "Santa Coloma de Gramenet", "ccaa-cataluna.html",
     2700, 1200, 5.3, 21),
    ("valdemoro", "Valdemoro", "ccaa-madrid.html",
     2100, 950, 5.4, 19),
    ("colmenar-viejo", "Colmenar Viejo", "ccaa-madrid.html",
     2400, 1050, 5.2, 19),
    ("sant-vicent-del-raspeig", "Sant Vicent del Raspeig", "ccaa-comunitat-valenciana.html",
     1800, 870, 5.8, 22),
    ("vila-real", "Vila-real", "ccaa-comunitat-valenciana.html",
     1200, 600, 6.0, 25),
]


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def roi_badge_class(roi):
    if roi >= 6.5:
        return "roi-high"
    elif roi >= 5.0:
        return "roi-med"
    else:
        return "roi-low"


def fmt_pct(roi):
    return f"{roi:.1f}".replace(".", ",")


def build_row(slug, name, precio, alq, roi, dias):
    return (
        f'<tr>\n'
        f'          <td><span class="rank-num">#X</span></td>\n'
        f'          <td><a class="city-name" href="/rentabilidad-{slug}.html">🏙️ {name}</a></td>\n'
        f'          <td>{fmt_eu(precio)}€/m²</td>\n'
        f'          <td>{fmt_eu(alq)}€/mes</td>\n'
        f'          <td><span class="roi-badge {roi_badge_class(roi)}">{fmt_pct(roi)}%</span></td>\n'
        f'          <td>{dias} días</td>\n'
        f'        </tr>'
    )


def parse_rows(tbody_content):
    """Parsea filas existentes y extrae (slug, name, roi, raw_html)."""
    row_re = re.compile(
        r'<tr>\s*'
        r'<td><span class="rank-num">#\d+</span></td>\s*'
        r'<td><a class="city-name" href="/rentabilidad-([^"]+)\.html">[^<]+([^<]+)</a></td>\s*'
        r'<td>[^<]+</td>\s*<td>[^<]+</td>\s*'
        r'<td><span class="roi-badge [^"]+">([\d,]+)%</span></td>\s*'
        r'<td>[^<]+</td>\s*</tr>',
        re.DOTALL,
    )
    rows = []
    for m in re.finditer(r'<tr>.*?</tr>', tbody_content, re.DOTALL):
        raw = m.group(0)
        slug_match = re.search(r'href="/rentabilidad-([^"]+)\.html"', raw)
        roi_match = re.search(r'<span class="roi-badge [^"]+">([\d,]+)%</span>', raw)
        if slug_match and roi_match:
            slug = slug_match.group(1)
            roi = float(roi_match.group(1).replace(",", "."))
            rows.append((slug, roi, raw))
    return rows


def insert_into_table(html, slug, name, precio, alq, roi, dias):
    """Inserta una fila nueva en la tabla city-table del HTML, en posicion ordenada por ROI desc.
    Idempotente: si slug ya existe, no toca."""
    if f'href="/rentabilidad-{slug}.html"' in html and f'class="rank-num">' in html:
        # Detectar si ya esta dentro de la tabla
        # (no en la lista 'Otras ciudades')
        # Buscamos especificamente el patron rank-num + slug en la misma fila
        if re.search(rf'<tr>[^<]*<td><span class="rank-num">#\d+</span></td>\s*<td><a class="city-name" href="/rentabilidad-{re.escape(slug)}\.html"',
                     html):
            return html, False  # ya existe

    # Localizar tbody
    m = re.search(r'<tbody>(.*?)</tbody>', html, re.DOTALL)
    if not m:
        return html, False
    tbody = m.group(1)
    rows = parse_rows(tbody)
    new_row = build_row(slug, name, precio, alq, roi, dias)
    # Encontrar posicion: la primera fila con ROI <= roi nueva
    insert_idx = len(rows)
    for i, (_, r_roi, _) in enumerate(rows):
        if r_roi < roi:
            insert_idx = i
            break
        # Si igual ROI: insertamos despues (mantenemos orden alfabetico aproximado)
    # Construir nueva lista
    new_rows_list = list(rows[:insert_idx]) + [(slug, roi, new_row)] + list(rows[insert_idx:])
    # Renumerar
    new_html_rows = []
    for i, (_, _, raw) in enumerate(new_rows_list, 1):
        renumbered = re.sub(
            r'<span class="rank-num">#[X\d]+</span>',
            f'<span class="rank-num">#{i}</span>',
            raw,
            count=1,
        )
        new_html_rows.append(renumbered)
    new_tbody = "\n        ".join([""] + new_html_rows).strip()
    # Construir tbody nuevo respetando indentacion existente
    new_tbody_block = "<tbody>" + tbody[:tbody.find("<tr>")] + "".join(
        new_html_rows[i] + ("" if i == len(new_html_rows) - 1 else "")
        for i in range(len(new_html_rows))
    ) + "</tbody>"
    # En realidad, el original concatena rows una tras otra con `</tr><tr>` enlace.
    # Vamos a reconstruir con `</tr><tr>` para mantener formato.
    # Pero ya tenemos cada fila completa <tr>...</tr> -> simplemente join sin nada extra.
    new_tbody_block = "<tbody>" + "".join(new_html_rows) + "</tbody>"
    # Pero esto pierde indentacion. Vamos a usar la misma indentacion del primer tr.
    # Mas simple: re.sub que reemplaza directamente.
    html_new = re.sub(
        r'<tbody>.*?</tbody>',
        new_tbody_block,
        html,
        count=1,
        flags=re.DOTALL,
    )
    return html_new, True


def update_other_cities_list(html, slug, name):
    """Añade el link a la lista 'Otras ciudades' si no existe."""
    if f'href="/rentabilidad-{slug}.html"' in html:
        # Comprobar si esta en lista (no en tabla). Buscar fuera de city-table.
        # Como heuristica: si aparece mas de una vez ya esta
        if html.count(f'href="/rentabilidad-{slug}.html"') >= 2:
            return html, False
        # Si aparece solo una vez (en la tabla), añadirla a la lista
    # Insertarlo en la lista 'Otras ciudades' (alfabéticamente)
    list_match = re.search(
        r'<h2[^>]*>Otras ciudades[^<]*</h2>\s*<div[^>]*>(.*?)</div>',
        html,
        re.DOTALL,
    )
    if not list_match:
        return html, False
    list_content = list_match.group(1)
    new_link = (
        f'\n    <a href="/rentabilidad-{slug}.html" '
        f'style="display:inline-block;padding:.4rem .85rem;background:#f0f6ff;'
        f'border:1px solid #bfdbfe;border-radius:8px;color:#1e40af;font-size:.82rem;'
        f'font-weight:600;text-decoration:none">{name}</a>'
    )
    if f'href="/rentabilidad-{slug}.html"' not in list_content:
        # Inserta al final de la lista (antes del </div>)
        new_list = list_content + new_link + "\n  "
        html = html.replace(list_match.group(1), new_list, 1)
        return html, True
    return html, False


def main():
    results = []
    for slug, name, ccaa_file, precio, alq, roi, dias in ADDITIONS:
        fp = BETA / ccaa_file
        html = fp.read_text(encoding="utf-8")
        original = html
        html, inserted = insert_into_table(html, slug, name, precio, alq, roi, dias)
        if inserted:
            results.append(f"[ok] {ccaa_file}: añadida {name} a tabla city-table")
        else:
            results.append(f"[skip] {ccaa_file}: {name} ya estaba en la tabla")
        # Other cities list update
        html, list_added = update_other_cities_list(html, slug, name)
        if list_added:
            results.append(f"       y añadida a lista 'Otras ciudades'")
        if html != original:
            fp.write_text(html, encoding="utf-8")
    print("\n".join(results))


if __name__ == "__main__":
    main()
