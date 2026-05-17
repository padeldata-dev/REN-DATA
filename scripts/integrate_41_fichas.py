#!/usr/bin/env python3
"""Integrate 41 new cities into:
- rendata_beta/index.html DATA[]
- rendata_beta/ccaa-*.html tables
- rendata_beta/sitemap.xml
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_30k_50k_metadata.json"


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


CCAA_FILES = {
    "pais-vasco": "ccaa-pais-vasco.html",
    "cataluna": "ccaa-cataluna.html",
    "andalucia": "ccaa-andalucia.html",
    "baleares": "ccaa-baleares.html",
    "canarias": "ccaa-canarias.html",
    "galicia": "ccaa-galicia.html",
    "comunitat-valenciana": "ccaa-comunitat-valenciana.html",
    "castilla-la-mancha": "ccaa-castilla-la-mancha.html",
    "madrid": "ccaa-madrid.html",
    "cantabria": "ccaa-cantabria.html",
}


def update_index_data(cities):
    p = BETA / "index.html"
    html = p.read_text(encoding="utf-8")
    # Find the closing ]; line of DATA
    # we know it's on line 726 - let's find it via marker
    end_marker = "];\n\nconst gradMap"
    idx = html.find(end_marker)
    if idx == -1:
        # alt search
        idx = html.find("];")
        # Need to find the right ]; - the one that closes DATA
        m = re.search(r'sl:"vila-real",pob:\d+,itp:\d+\},\s*\];', html)
        if m:
            idx = m.end() - 2
    if idx == -1:
        raise RuntimeError("Could not find end of DATA[]")
    # check existing slugs in DATA to avoid dupes
    existing_slugs = set(re.findall(r'sl:"([^"]+)"', html[:idx+5]))

    lines = []
    for c in cities:
        slug = c["slug"]
        if slug in existing_slugs:
            continue
        n = c["name"].replace('"', '\\"')
        ccaa = c["ccaa"]
        # region tag
        region = c.get("region", "centro")
        # Map region to current registered regions in DATA (centro/norte/levante/andalucia/islas/costa/metro/interior)
        # Use the city's region directly; existing DATA uses these
        reg = region
        roi = fmt_pct(c["roi"]).replace(",", ".")  # use point for JS number
        itp = c["itp_pct"]
        itp_str = str(int(itp)) if int(itp) == itp else f"{itp}"
        line = (
            f'  {{n:"{n}",cc:"{ccaa}",reg:"{reg}",roi:{roi},'
            f'p:{c["precio"]},alq:{c["alq"]},vp:{c["vp"]},va:{c["va"]},'
            f'd:{c["dias"]},sl:"{slug}",pob:{c["pop"]},itp:{itp_str}}},'
        )
        lines.append(line)

    insert = "\n".join(lines) + "\n"
    # Find exact "vila-real" entry's terminating newline then insert before ];
    pattern = re.compile(r'(sl:"vila-real"[^\n]*\},\s*\n)(\];)')
    new_html, n = pattern.subn(rf'\g<1>{insert}\g<2>', html, count=1)
    if n == 0:
        # generic insert: find "];\n\nconst gradMap"
        new_html = html.replace(end_marker, insert + end_marker, 1)
    p.write_text(new_html, encoding="utf-8")
    return len(lines)


def update_ccaa_pages(cities):
    """Insert rows in ccaa-*.html tables ordered by ROI (desc)."""
    changes = {}
    by_ccaa = {}
    for c in cities:
        by_ccaa.setdefault(c["ccaa_slug"], []).append(c)

    for ccaa_slug, group in by_ccaa.items():
        fn = CCAA_FILES.get(ccaa_slug)
        if not fn:
            print(f"[warn] no ccaa file for {ccaa_slug}")
            continue
        p = BETA / fn
        if not p.exists():
            print(f"[warn] {fn} missing")
            continue
        html = p.read_text(encoding="utf-8")

        # Avoid duplicates
        for c in sorted(group, key=lambda x: -x["roi"]):
            slug = c["slug"]
            if f"/rentabilidad-{slug}.html" in html:
                continue
            row = build_ccaa_row(c)
            # Find table and insert in appropriate position based on ROI
            # Simple approach: insert just before </tbody>
            new_html, n = re.subn(
                r'(\s*)(</tbody>)',
                rf'\g<1>{row}\g<1>\g<2>',
                html, count=1,
            )
            if n > 0:
                html = new_html
            else:
                # try <table class="city-table"> + </table>
                new_html, n = re.subn(
                    r'(</table>)',
                    rf'  {row}\n  \g<1>',
                    html, count=1,
                )
                if n > 0:
                    html = new_html

            # Also insert link in "Otras ciudades" list if present
            otras_pattern = re.compile(r'(<h[23][^>]*>[^<]*[Oo]tras ciudades[^<]*</h[23]>\s*<ul[^>]*>)', re.DOTALL)
            mo = otras_pattern.search(html)
            if mo:
                link = f'\n    <li><a href="rentabilidad-{slug}.html">{c["name"]}</a></li>'
                ip = mo.end()
                # check not duplicate
                if f"rentabilidad-{slug}.html" not in html[ip:ip+5000]:
                    html = html[:ip] + link + html[ip:]
        p.write_text(html, encoding="utf-8")
        changes[fn] = len(group)
    return changes


def build_ccaa_row(c):
    """Build a <tr> row matching the city-table format."""
    name = c["name"]; slug = c["slug"]; prov = c["prov"]
    roi = fmt_pct(c["roi"])
    precio = fmt_eu(c["precio"])
    alq = fmt_eu(c["alq"])
    return (
        f'<tr>'
        f'<td><a href="rentabilidad-{slug}.html"><strong>{name}</strong></a> <span style="color:var(--muted);font-size:.78rem">({prov})</span></td>'
        f'<td><strong style="color:var(--blue)">{roi}%</strong></td>'
        f'<td>{precio}€</td>'
        f'<td>{alq}€</td>'
        f'</tr>'
    )


def update_sitemap(cities):
    p = BETA / "sitemap.xml"
    xml = p.read_text(encoding="utf-8")
    lines = []
    for c in cities:
        slug = c["slug"]
        if f"rentabilidad-{slug}.html" in xml:
            continue
        lines.append(
            f'  <url>\n'
            f'    <loc>https://rendata.es/rentabilidad-{slug}.html</loc>\n'
            f'    <lastmod>2026-05-17</lastmod>\n'
            f'    <changefreq>monthly</changefreq>\n'
            f'    <priority>0.7</priority>\n'
            f'  </url>'
        )
    if not lines:
        return 0
    block = "\n".join(lines) + "\n"
    new_xml = xml.replace("</urlset>", block + "</urlset>", 1)
    p.write_text(new_xml, encoding="utf-8")
    return len(lines)


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    n_idx = update_index_data(cities)
    print(f"[index.html] added {n_idx} DATA entries")
    ccaa_changes = update_ccaa_pages(cities)
    for fn, n in ccaa_changes.items():
        print(f"[{fn}] added {n} rows")
    n_sm = update_sitemap(cities)
    print(f"[sitemap.xml] added {n_sm} URLs")


if __name__ == "__main__":
    main()
