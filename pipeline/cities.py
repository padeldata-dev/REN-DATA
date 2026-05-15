"""Carga el catálogo maestro de ciudades."""
import csv
from .config import CITIES_MASTER

def load_cities():
    """Devuelve lista de dicts con todas las ciudades del master."""
    rows = []
    with open(CITIES_MASTER, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            # Normalizar tipos
            for k in ("precio_actual","alquiler_actual","var_precio_anual","var_alquiler_anual","dias_mercado"):
                if r.get(k):
                    try: r[k] = float(r[k]) if "." in r[k] else int(r[k])
                    except ValueError: pass
            if r.get("roi_actual"):
                try: r["roi_actual"] = float(r["roi_actual"])
                except ValueError: pass
            rows.append(r)
    return rows

def by_slug(rows):
    return {r["slug"]: r for r in rows}

def save_cities(rows, path=CITIES_MASTER):
    """Reescribe el master con los rows actualizados."""
    if not rows: return
    fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
