#!/usr/bin/env python3
"""Integrate 100 new 20k-30k cities into index/CCAA/sitemap. Adds new CCAA mappings."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from integrate_41_fichas import (
    fmt_eu, fmt_pct, build_ccaa_row, update_sitemap,
)

BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_20k_30k_metadata.json"


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
    "murcia": "ccaa-murcia.html",
    "extremadura": "ccaa-extremadura.html",
    "navarra": "ccaa-navarra.html",
    "castilla-y-leon": "ccaa-castilla-y-leon.html",
}


def update_index_data(cities):
    p = BETA / "index.html"
    html = p.read_text(encoding="utf-8")

    # Find the last entry in DATA[] and insert before its ];
    # Look for the closing ]; with const gradMap nearby (DATA closing)
    end_marker = "];\n\nconst gradMap"
    idx = html.find(end_marker)
    if idx == -1:
        # Try alternative end marker
        m = re.search(r'\}\s*,\s*\n\s*\]\s*;', html)
        if not m:
            raise RuntimeError("Could not find end of DATA[]")
        idx = m.end()

    existing_slugs = set(re.findall(r'sl:"([^"]+)"', html[:idx]))

    lines = []
    for c in cities:
        slug = c["slug"]
        if slug in existing_slugs:
            continue
        n = c["name"].replace('"', '\\"')
        ccaa = c["ccaa"]
        reg = c.get("region", "centro")
        roi = fmt_pct(c["roi"]).replace(",", ".")
        itp = c["itp_pct"]
        itp_str = str(int(itp)) if int(itp) == itp else f"{itp}"
        line = (
            f'  {{n:"{n}",cc:"{ccaa}",reg:"{reg}",roi:{roi},'
            f'p:{c["precio"]},alq:{c["alq"]},vp:{c["vp"]},va:{c["va"]},'
            f'd:{c["dias"]},sl:"{slug}",pob:{c["pop"]},itp:{itp_str}}},'
        )
        lines.append(line)

    if not lines:
        return 0
    insert = "\n".join(lines) + "\n"
    new_html = html.replace(end_marker, insert + end_marker, 1)
    p.write_text(new_html, encoding="utf-8")
    return len(lines)


def update_ccaa_pages(cities):
    changes = {}
    by_ccaa = {}
    for c in cities:
        by_ccaa.setdefault(c["ccaa_slug"], []).append(c)

    for ccaa_slug, group in by_ccaa.items():
        fn = CCAA_FILES.get(ccaa_slug)
        if not fn:
            print(f"[warn] no ccaa file mapping for {ccaa_slug}")
            continue
        p = BETA / fn
        if not p.exists():
            print(f"[warn] {fn} missing")
            continue
        html = p.read_text(encoding="utf-8")

        added = 0
        for c in sorted(group, key=lambda x: -x["roi"]):
            slug = c["slug"]
            if f"/rentabilidad-{slug}.html" in html or f'"rentabilidad-{slug}.html"' in html:
                continue
            row = build_ccaa_row(c)
            new_html, n = re.subn(
                r'(\s*)(</tbody>)',
                rf'\g<1>{row}\g<1>\g<2>',
                html, count=1,
            )
            if n > 0:
                html = new_html
                added += 1
            else:
                new_html, n = re.subn(
                    r'(</table>)',
                    rf'  {row}\n  \g<1>',
                    html, count=1,
                )
                if n > 0:
                    html = new_html
                    added += 1

            # Otras ciudades list
            otras_pattern = re.compile(r'(<h[23][^>]*>[^<]*[Oo]tras ciudades[^<]*</h[23]>\s*<ul[^>]*>)', re.DOTALL)
            mo = otras_pattern.search(html)
            if mo:
                link = f'\n    <li><a href="rentabilidad-{slug}.html">{c["name"]}</a></li>'
                ip = mo.end()
                if f"rentabilidad-{slug}.html" not in html[ip:ip+5000]:
                    html = html[:ip] + link + html[ip:]

        p.write_text(html, encoding="utf-8")
        changes[fn] = added
    return changes


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
