#!/usr/bin/env python3
"""Regenerate 22 cities that had no Dataset block, then correctly inject Dataset
AFTER BreadcrumbList's closing }, before array close ]."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_20k_30k_metadata.json"

sys.path.insert(0, str(Path(__file__).parent))
from generate_41_fichas import generate_one  # noqa: E402


def fmt_eu(n):
    if isinstance(n, float):
        n = int(round(n))
    return f"{n:,}".replace(",", ".")


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


CITIES_NEED_DATASET = [
    "cartama", "camas", "candelaria", "paiporta", "valls",
    "mejorada-del-campo", "el-masnou", "las-gabias", "san-juan-de-aznalfarache",
    "picassent", "sant-feliu-de-guixols", "amposta", "aljaraque", "maracena",
    "alfafar", "pajara", "vilassar-de-mar", "algete", "atarfe", "benicassim",
    "silla", "la-zubia",
]


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


def inject_dataset(html, c):
    """Inject Dataset block AFTER the BreadcrumbList closing } and BEFORE array close ]."""
    # We look for the JSON-LD script tag end: }]</script> where the } closes BreadcrumbList
    # and ] closes the array. Insert ',{Dataset}' between } and ].
    # Match: }\s*\]</script>
    dataset = build_dataset_block(c)
    # The dataset starts with ',{' and ends with '}' (no comma). So insert it right
    # AFTER the BreadcrumbList's closing }, before the array's closing ].
    # Use a regex that captures `}` then optional whitespace then `]</script>`.
    new_html, n = re.subn(
        r'(\})(\s*)(\]</script>)',
        rf'\g<1>{dataset}\g<2>\g<3>',
        html, count=1,
    )
    return new_html, n


def main():
    cities = {c["slug"]: c for c in json.loads(META.read_text(encoding="utf-8"))}

    fixed = 0
    for slug in CITIES_NEED_DATASET:
        c = cities[slug]
        # Step 1: regenerate from twin (drops the broken injection)
        html = generate_one(c)
        # Step 2: now inject Dataset correctly
        html2, n = inject_dataset(html, c)
        if n == 0:
            print(f"[ERR] {slug}: could not inject Dataset")
            continue
        out = BETA / f"rentabilidad-{slug}.html"
        out.write_text(html2, encoding="utf-8")
        fixed += 1
        print(f"[fix] {slug}: regenerated + Dataset injected")
    print(f"\nTotal fixed: {fixed}")


if __name__ == "__main__":
    main()
