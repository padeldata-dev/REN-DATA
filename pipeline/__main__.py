"""
CLI: python -m pipeline <comando>

Comandos:
  fetch      Descarga + parsea fuentes y genera el CSV processed
  apply      Aplica el CSV processed a rendata_beta/ (DATA[] + 329 fichas)
  run        fetch + apply (todo en uno)
  audit      Muestra el estado de cobertura sin escribir
"""
import sys
import argparse
from datetime import date
from .cities import load_cities
from .aggregator import aggregate, write_csv, write_snapshot
from .updater import update_index_data, update_fichas, update_master

def cmd_fetch(args):
    rows = aggregate(quarter=args.quarter)
    write_csv(rows, quarter=args.quarter)
    write_snapshot(rows, quarter=args.quarter)

def cmd_apply(args):
    # Carga el CSV procesado y aplica
    import csv
    from .config import PROCESSED_DIR
    q = args.quarter or _current_quarter()
    fp = PROCESSED_DIR / f"cities_{q}.csv"
    if not fp.exists():
        print(f"ERROR: {fp} no existe. Ejecuta primero `python -m pipeline fetch`")
        sys.exit(1)
    rows = []
    with open(fp, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in ("precio_m2","alquiler_medio","roi","var_precio_anual","var_alquiler_anual","dias_mercado","poblacion"):
                if r.get(k):
                    try: r[k] = float(r[k]) if "." in r[k] else int(r[k])
                    except: pass
            rows.append(r)
    master = load_cities()
    print(f"\n=== APPLYING {len(rows)} rows to rendata_beta/ ===\n")
    update_index_data(rows)
    update_fichas(rows, master)
    update_master(rows, master)

def cmd_run(args):
    cmd_fetch(args)
    cmd_apply(args)

def cmd_audit(args):
    rows = aggregate(quarter=args.quarter)
    # Solo imprime stats, no escribe nada

def _current_quarter():
    m = date.today().month
    return f"{date.today().year}Q{(m - 1) // 3 + 1}"

def main():
    p = argparse.ArgumentParser(prog="python -m pipeline")
    p.add_argument("cmd", choices=["fetch","apply","run","audit"])
    p.add_argument("--quarter", help="ej. 2026Q2 (default: trimestre actual)")
    args = p.parse_args()
    {"fetch": cmd_fetch, "apply": cmd_apply, "run": cmd_run, "audit": cmd_audit}[args.cmd](args)

if __name__ == "__main__":
    main()
