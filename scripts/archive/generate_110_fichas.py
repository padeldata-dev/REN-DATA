#!/usr/bin/env python3
"""Generates 110 city fichas (15k-20k pop) using generate_41_fichas core logic
and reading cities_15k_20k_metadata.json. Auto-injects Dataset block where
the twin lacks one.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_15k_20k_metadata.json"

sys.path.insert(0, str(Path(__file__).parent))
from generate_41_fichas import generate_one  # noqa: E402


def build_dataset_block(c):
    name = c["name"]; ccaa = c["ccaa"]
    return (
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


def ensure_dataset(html, c):
    if '"@type":"Dataset"' in html:
        return html
    dataset = build_dataset_block(c)
    new_html, n = re.subn(
        r'(\})(\s*)(\]</script>)',
        rf'\g<1>{dataset}\g<2>\g<3>',
        html, count=1,
    )
    return new_html if n else html


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    available = {p.stem.replace("rentabilidad-", "") for p in BETA.glob("rentabilidad-*.html")}

    ok = err = 0
    for city in cities:
        twin = city["twin"]
        if twin not in available:
            print(f"[warn] {city['slug']}: twin '{twin}' missing, fallback naron", flush=True)
            city["twin"] = "naron"
        try:
            html = generate_one(city)
            html = ensure_dataset(html, city)
            out = BETA / f"rentabilidad-{city['slug']}.html"
            out.write_text(html, encoding="utf-8")
            ok += 1
            if ok % 20 == 0:
                print(f"  {ok}/{len(cities)} generadas", flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ERROR] {city['slug']}: {e}", flush=True)
            err += 1

    print(f"\n=== summary: OK={ok} ERR={err} TOTAL={len(cities)} ===")


if __name__ == "__main__":
    main()
