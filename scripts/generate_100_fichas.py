#!/usr/bin/env python3
"""Generates 100 city fichas (20k-30k pop) using generate_41_fichas core logic but reading
cities_20k_30k_metadata.json. Reuses all helpers from generate_41_fichas.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_20k_30k_metadata.json"

sys.path.insert(0, str(Path(__file__).parent))
from generate_41_fichas import generate_one  # noqa: E402


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    available = {p.stem.replace("rentabilidad-", "") for p in BETA.glob("rentabilidad-*.html")}

    results = []
    for city in cities:
        twin = city["twin"]
        if twin not in available:
            # Should not happen after fix_twins, but safety net
            print(f"[warn] {city['slug']}: twin '{twin}' missing, fallback to naron", flush=True)
            city["twin"] = "naron"
        try:
            html = generate_one(city)
            out = BETA / f"rentabilidad-{city['slug']}.html"
            out.write_text(html, encoding="utf-8")
            lines = html.count("\n") + 1
            results.append(f"[ok] {city['slug']}: {lines} líneas")
            print(results[-1], flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            results.append(f"[ERROR] {city['slug']}: {e}")
            print(results[-1], flush=True)

    ok = sum(1 for r in results if r.startswith("[ok]"))
    err = sum(1 for r in results if r.startswith("[ERROR]"))
    print(f"\n=== summary ===")
    print(f"OK: {ok}  ERROR: {err}  TOTAL: {len(results)}")


if __name__ == "__main__":
    main()
