#!/usr/bin/env python3
"""Integrate 110 new 15k-20k cities into index/CCAA/sitemap."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
from integrate_100_fichas import (
    update_index_data, update_ccaa_pages,
)
from integrate_41_fichas import update_sitemap

# Patch META for the 100-fichas integrator
import integrate_100_fichas
integrate_100_fichas.META = ROOT / "data" / "cities_15k_20k_metadata.json"


def main():
    cities = json.loads(integrate_100_fichas.META.read_text(encoding="utf-8"))
    n_idx = update_index_data(cities)
    print(f"[index.html] added {n_idx} DATA entries")
    ccaa_changes = update_ccaa_pages(cities)
    for fn, n in ccaa_changes.items():
        print(f"[{fn}] added {n} rows")
    n_sm = update_sitemap(cities)
    print(f"[sitemap.xml] added {n_sm} URLs")


if __name__ == "__main__":
    main()
