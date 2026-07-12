"""Block 4: content audit — residual texts, ficha sections completeness, widget data."""
import re
import json
from pathlib import Path
from collections import Counter

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

# 1. Search for incorrect residual texts
PATTERNS = {
    "329 ciudades": r"\b329\s+ciudades\b",
    "más de 300": r"m[áa]s\s+de\s+300\b",
    "más de 500": r"m[áa]s\s+de\s+500\b",     # if not "587"
    "Idealista":  r"\bIdealista\b",
    "Fotocasa":   r"\bFotocasa\b",
    "Habitaclia": r"\bHabitaclia\b",
}

hits = {k: [] for k in PATTERNS}
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    for name, pat in PATTERNS.items():
        if re.search(pat, txt, re.IGNORECASE):
            hits[name].append(f.name)

print("=== RESIDUAL TEXT SEARCH ===")
for k, v in hits.items():
    print(f"  '{k}': {len(v)} files")
    for f in v[:5]: print(f"     {f}")

# 2. Ficha sections completeness — check rentabilidad-*.html for key blocks
FICHA_SECTIONS = {
    "editorial":           r"editorial|opinión|opinion|editorial-",
    "perspectiva":         r"perspectiva\s+Ren\s+Data|perspectiva-rendata|perspectiva ren data",
    "ayudas":              r"ayuda(s)?\s+CCAA|ayuda(s)?\s+(jóvenes|para|de)|ITP-reducido|bono",
    "faq":                 r"FAQPage|<details[^>]*>|@type\":\s*\"Question",
    "puedo permitirme":    r"puedo\s+permitirme|¿\s*Puedo\s+permitirme|presupuesto-comprar",
}

ficha_results = {k: 0 for k in FICHA_SECTIONS}
ficha_files = list(ROOT.glob("rentabilidad-*.html"))
ficha_total = len(ficha_files)

ficha_missing = {k: [] for k in FICHA_SECTIONS}
for f in ficha_files:
    txt = f.read_text(encoding="utf-8")
    for k, pat in FICHA_SECTIONS.items():
        if re.search(pat, txt, re.IGNORECASE):
            ficha_results[k] += 1
        else:
            ficha_missing[k].append(f.name)

print(f"\n=== FICHA SECTIONS ({ficha_total} city pages) ===")
for k, count in ficha_results.items():
    pct = count*100/ficha_total if ficha_total else 0
    print(f"  {k}: {count}/{ficha_total} ({pct:.0f}%)")
    if count < ficha_total:
        sample = ficha_missing[k][:3]
        print(f"     Missing sample: {sample}")

# 3. Widget data file
widget_files = ["widget.js", "widget-data.json", "widget-demo.html"]
print("\n=== WIDGET FILES ===")
for name in widget_files:
    p = ROOT / name
    print(f"  {name}: {'exists' if p.exists() else 'MISSING'}", end="")
    if p.exists():
        print(f"  size={p.stat().st_size} bytes")
    else:
        print()

# 4. Widget data cities count
wd = ROOT / "widget-data.json"
if wd.exists():
    try:
        data = json.loads(wd.read_text(encoding="utf-8"))
        if isinstance(data, list):
            print(f"  widget-data.json: {len(data)} cities")
        elif isinstance(data, dict):
            for key in data:
                if isinstance(data[key], list):
                    print(f"  widget-data.json['{key}']: {len(data[key])} entries")
    except json.JSONDecodeError as e:
        print(f"  widget-data.json: PARSE ERROR {e}")

# 5. Tools — verify they reference DATA[] correctly (cosmetic check)
print("\n=== TOOLS DATA REFERENCES ===")
for name in ["simulador-comprar-vs-alquilar.html", "calculadora-hipoteca.html"]:
    p = ROOT / name
    if not p.exists(): continue
    txt = p.read_text(encoding="utf-8")
    has_fetch = "fetch('/'" in txt or 'fetch("/"' in txt
    has_DATA_regex = "const DATA=" in txt or "DATA=\\s*" in txt
    needs_data = name == "simulador-comprar-vs-alquilar.html"
    if needs_data:
        print(f"  {name}: fetch('/') = {has_fetch} | DATA regex = {has_DATA_regex}")

# 6. Count cities in index.html DATA[]
idx = ROOT / "index.html"
txt = idx.read_text(encoding="utf-8")
m = re.search(r"const DATA=\s*(\[[\s\S]*?\]);", txt)
if m:
    try:
        # Quick brace count
        body = m.group(1)
        n_entries = body.count("{n:")
        print(f"\n  index.html DATA[] entries: {n_entries}")
    except Exception as e:
        print(f"  Couldn't count DATA entries: {e}")
