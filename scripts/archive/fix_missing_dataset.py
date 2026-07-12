#!/usr/bin/env python3
"""Fixes 22 cities missing Dataset JSON-LD block. Injects it before }]</script>."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_20k_30k_metadata.json"


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def build_dataset(c):
    name = c["name"]; ccaa = c["ccaa"]
    return (
        ',{\n  "@context":"https://schema.org",\n  '
        f'"@type":"Dataset",'
        f'"name":"Mercado inmobiliario {name} 2026",'
        f'"description":"Datos de precio m², rentabilidad por alquiler y evolución del mercado inmobiliario en {name}, {ccaa}.",'
        f'"keywords":["rentabilidad inmobiliaria {name}","precio vivienda {name}","invertir {name}","alquiler {name}"],'
        f'"temporalCoverage":"2026",'
        f'"spatialCoverage":"{name}, {ccaa}, España",'
        f'"publisher":{{"@type":"Organization","name":"Ren Data","url":"https://rendata.es"}}'
        '\n}'
    )


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    fixed = 0
    for c in cities:
        p = BETA / f"rentabilidad-{c['slug']}.html"
        if not p.is_file():
            continue
        html = p.read_text(encoding="utf-8")
        if '"@type":"Dataset"' in html:
            continue
        # Inject Dataset right before }]</script>
        dataset = build_dataset(c)
        new_html, n = re.subn(
            r'(\n\}\]</script>)',
            rf'{dataset}\g<1>',
            html, count=1,
        )
        if n == 0:
            # Try simpler closing pattern
            new_html, n = re.subn(
                r'(\}\]</script>)',
                rf'{dataset}\n\g<1>',
                html, count=1,
            )
        if n == 0:
            print(f"[ERR] {c['slug']}: could not inject Dataset")
            continue
        p.write_text(new_html, encoding="utf-8")
        fixed += 1
        print(f"[fix] {c['slug']}: injected Dataset")
    print(f"\nTotal fixed: {fixed}")


if __name__ == "__main__":
    main()
