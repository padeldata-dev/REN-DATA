#!/usr/bin/env python3
"""Integrate cities from aragon/asturias/la-rioja into their CCAA pages
(not handled by integrate_100_fichas which had hard-coded CCAA_FILES)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_15k_20k_metadata.json"

sys.path.insert(0, str(Path(__file__).parent))
from integrate_41_fichas import build_ccaa_row

NEW_CCAA = {
    "aragon": "ccaa-aragon.html",
    "asturias": "ccaa-asturias.html",
    "la-rioja": "ccaa-la-rioja.html",
}


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    by_ccaa = {}
    for c in cities:
        if c["ccaa_slug"] in NEW_CCAA:
            by_ccaa.setdefault(c["ccaa_slug"], []).append(c)

    for ccaa_slug, group in by_ccaa.items():
        fn = NEW_CCAA[ccaa_slug]
        p = BETA / fn
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
                html = new_html; added += 1
            else:
                new_html, n = re.subn(
                    r'(</table>)',
                    rf'  {row}\n  \g<1>',
                    html, count=1,
                )
                if n > 0:
                    html = new_html; added += 1
        p.write_text(html, encoding="utf-8")
        print(f"[{fn}] added {added} rows")


if __name__ == "__main__":
    main()
