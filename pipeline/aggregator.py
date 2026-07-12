"""
Aggregator: combina las fuentes en un dataset único {slug: campos}.

Política de merge (precio, en orden de preferencia):
  1. MIVAU (oficial)
  2. Notariado (cruzado)
  3. Observatorio CCAA correspondiente
  4. Valor histórico × ratio variación CCAA (estimado)
  5. Valor actual del master (sin cambio)

Política de merge (alquiler):
  1. Observatorio CCAA correspondiente
  2. Estimado: precio_nuevo × (alquiler_actual / precio_actual_historico)
  3. Valor actual del master

Población: SIEMPRE INE.
"""
import csv
from datetime import date
from pathlib import Path
from .config import SUP_M2, PROCESSED_DIR
from .cities import load_cities
from .sources import ine, mivau, notariado
from .sources.observatorios import madrid, cataluna, andalucia

def calc_roi(precio, alquiler, sup=SUP_M2):
    if not precio or not alquiler: return None
    return round(alquiler * 12 / (precio * sup) * 1000) / 10

def aggregate(quarter: str = None) -> list:
    """
    Devuelve list[dict] con los campos finales por ciudad.
    quarter: "2026Q2" — usado para fecha del snapshot
    """
    if quarter is None:
        m = date.today().month
        q = (m - 1) // 3 + 1
        quarter = f"{date.today().year}Q{q}"
    print(f"\n=== AGGREGATING DATA FOR {quarter} ===\n")

    cities = load_cities()
    n = len(cities)

    # Cargar todas las fuentes
    print("--- Población ---")
    pops_raw = ine.fetch_populations()
    pops = ine.match_to_cities(pops_raw, cities)

    print("\n--- Precio compra ---")
    mivau_raw = mivau.fetch_prices()
    mivau_match = mivau.match_to_cities(mivau_raw, cities) if mivau_raw else {}

    print("\n--- Notariado (cruzado) ---")
    not_raw = notariado.fetch()
    print(f"[NOTARIADO] {len(not_raw)} ámbitos cargados")

    print("\n--- Observatorios ---")
    madrid_raw = madrid.fetch()
    madrid_match = madrid.match_to_cities(madrid_raw, cities) if madrid_raw else {}
    # API CKAN de la Comunidad de Madrid: series regionales agregadas
    # (compraventas, superficie media, intereses, duración hipotecas, % fijo/variable).
    # No tiene granularidad municipal pero queda snapshotted en data/raw.
    madrid_api = madrid.fetch_observatorio_api()
    cat_raw = cataluna.fetch()
    cat_match = cataluna.match_to_cities(cat_raw, cities) if cat_raw else {}
    and_raw = andalucia.fetch()
    and_match = andalucia.match_to_cities(and_raw, cities) if and_raw else {}

    # Combinar
    rows_out = []
    for c in cities:
        slug = c["slug"]
        new_p = None
        new_a = None
        fuente_p = None
        fuente_a = None

        # Precio: MIVAU > observatorio CCAA > histórico
        if slug in mivau_match:
            new_p = mivau_match[slug]; fuente_p = "MIVAU"
        elif slug in madrid_match and madrid_match[slug].get("precio"):
            new_p = madrid_match[slug]["precio"]; fuente_p = "Madrid_obs"
        elif slug in cat_match and cat_match[slug].get("precio"):
            new_p = cat_match[slug]["precio"]; fuente_p = "Cataluna_obs"
        elif slug in and_match and and_match[slug].get("precio"):
            new_p = and_match[slug]["precio"]; fuente_p = "Andalucia_obs"
        else:
            new_p = c.get("precio_actual"); fuente_p = "historico"

        # Alquiler: observatorio CCAA > estimado por ratio histórico
        #
        # NOTA Cataluña (INCASOL, dataset qww9-bvhh): mide la media de TODAS
        # las fianzas de alquiler registradas y vigentes (incluye contratos
        # antiguos por debajo de mercado). El baseline actual del sitio usa
        # precio de anuncio (tipo Idealista), sistemáticamente más alto.
        # Verificado 2026-07-12: aplicar este dato directo produce una caída
        # sistemática de mediana -26,5% (hasta -51,7%) en las 75 ciudades
        # catalanas con match — no es un movimiento real de mercado, es un
        # cambio de metodología. Desactivado como fuente de merge hasta que
        # se decida un factor de recalibración o una migración consistente
        # de metodología para toda España. El fetch queda arreglado y el
        # snapshot se sigue guardando en data/raw/ para análisis posterior.
        if slug in madrid_match and madrid_match[slug].get("alquiler"):
            new_a = madrid_match[slug]["alquiler"]; fuente_a = "Madrid_obs"
        elif slug in and_match and and_match[slug].get("alquiler"):
            new_a = and_match[slug]["alquiler"]; fuente_a = "Andalucia_obs"
        else:
            # Estimado: si el precio cambió, escalar el alquiler proporcionalmente
            old_p = c.get("precio_actual")
            old_a = c.get("alquiler_actual")
            if old_p and old_a and new_p:
                ratio = new_p / old_p
                # alquiler suele moverse menos que el precio (factor 0.85)
                new_a = round(old_a * (1 + (ratio - 1) * 0.85))
                fuente_a = "estimado_ratio"
            else:
                new_a = old_a; fuente_a = "historico"

        # Variaciones anuales (vs valor actual del master)
        # Solo se recalculan si hay una fuente nueva real: comparar el valor
        # contra sí mismo cuando fuente_p=="historico" daría 0.0 y borraría
        # la variación interanual ya conocida.
        old_p = c.get("precio_actual")
        old_a = c.get("alquiler_actual")
        if fuente_p != "historico" and new_p and old_p:
            var_p = round((new_p / old_p - 1) * 100, 1)
        else:
            var_p = c.get("var_precio_anual")
        if fuente_a not in ("historico", "estimado_ratio") and new_a and old_a:
            var_a = round((new_a / old_a - 1) * 100, 1)
        else:
            var_a = c.get("var_alquiler_anual")

        # ROI
        new_roi = calc_roi(new_p, new_a)

        # Días mercado: NO actualizable. Mantener actual con flag.
        dias = c.get("dias_mercado")

        rows_out.append({
            "slug": slug,
            "nombre": c["nombre"],
            "ccaa": c["ccaa"],
            "poblacion": pops.get(slug, ""),
            "precio_m2": new_p,
            "alquiler_medio": new_a,
            "roi": new_roi,
            "var_precio_anual": var_p,
            "var_alquiler_anual": var_a,
            "dias_mercado": dias,
            "dias_mercado_flag": "Estimado",  # nunca real, siempre marcado
            "fuente_precio": fuente_p,
            "fuente_alquiler": fuente_a,
            "fecha_extraccion": date.today().isoformat(),
            "trimestre": quarter,
        })

    # Estadísticas de cobertura
    print("\n=== COBERTURA ===")
    n_real_p = sum(1 for r in rows_out if r["fuente_precio"] != "historico")
    n_real_a = sum(1 for r in rows_out if r["fuente_alquiler"] not in ("historico","estimado_ratio"))
    n_pop = sum(1 for r in rows_out if r["poblacion"])
    print(f"  Población:     {n_pop}/{n} ({100*n_pop/n:.0f}%)")
    print(f"  Precio real:   {n_real_p}/{n} ({100*n_real_p/n:.0f}%)")
    print(f"  Alquiler real: {n_real_a}/{n} ({100*n_real_a/n:.0f}%)")
    print(f"  Días mercado:  marcado 'Estimado' (no actualizable sin scraping)\n")

    return rows_out

def write_csv(rows: list, quarter: str = None) -> Path:
    if quarter is None:
        m = date.today().month
        q = (m - 1) // 3 + 1
        quarter = f"{date.today().year}Q{q}"
    fp = PROCESSED_DIR / f"cities_{quarter}.csv"
    if rows:
        with open(fp, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"[OUT] CSV escrito: {fp} ({len(rows)} ciudades)")
    return fp

def write_snapshot(rows: list, quarter: str = None) -> Path:
    """Snapshot histórico para calcular variaciones futuras."""
    from .config import SNAPSHOTS_DIR
    if quarter is None:
        m = date.today().month
        q = (m - 1) // 3 + 1
        quarter = f"{date.today().year}Q{q}"
    fp = SNAPSHOTS_DIR / f"snapshot_{quarter}.csv"
    if rows:
        with open(fp, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"[OUT] Snapshot histórico: {fp}")
    return fp

if __name__ == "__main__":
    rows = aggregate()
    write_csv(rows)
    write_snapshot(rows)
