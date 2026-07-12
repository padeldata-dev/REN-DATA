"""Block 2: stagger article publication dates across May 2026 by category."""
import re
import random
from pathlib import Path

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

# Group 1 — primeros (1-10 mayo): top10, baratas, alquiler caro, costa, revalorización, universitarias, interior/costa, municipios pequeños, madrid vs barcelona, evolución precio
GROUP_A = [
    "top10-ciudades-rentables-2026.html",
    "ciudades-baratas-comprar-piso-espana-2026.html",
    "ciudades-alquiler-caro-espana-2026.html",
    "invertir-vivienda-costa-espana-2026.html",
    "ciudades-interior-vs-costa-rentabilidad-2026.html",
    "ciudades-mayor-revalorizacion-2026.html",
    "ciudades-universitarias-rentabilidad-alquiler-2026.html",
    "municipios-pequenos-alta-rentabilidad-2026.html",
    "rentabilidad-madrid-vs-barcelona-2026.html",
    "precio-vivienda-espana-evolucion-2026.html",
    "informe-rentabilidad-espana-q2-2026.html",
    "como-calcular-rentabilidad-vivienda-2026.html",
    "alquiler-turistico-vs-residencial-rentabilidad-2026.html",
]

# Group 2 — CCAA (5-15 mayo): mercado-inmobiliario-*, mejores-ccaa, castilla-leon-rentabilidad
GROUP_B_PATTERNS = [r"^mercado-inmobiliario-.*\.html$", r"^castilla-leon-rentabilidad", r"^mejores-ccaa-"]

# Group 3 — perfil inversor (8-18 mayo)
GROUP_C = [
    "guia-inversor-conservador-2026.html",
    "guia-inversor-agresivo-2026.html",
    "invertir-vivienda-vacacional-espana-2026.html",
    "invertir-vivienda-jubilacion-espana-2026.html",
    "invertir-vivienda-nueva-vs-segunda-mano-2026.html",
    "invertir-vivienda-canarias-2026.html",
    "invertir-primera-vivienda-vs-inversion-2026.html",
    "mejores-ciudades-jovenes-invertir-2026.html",
]

# Group 4 — comprador final (12-20 mayo)
GROUP_D = [
    "comprar-piso-primera-vez-espana-2026.html",
    "comprar-piso-joven-espana-2026.html",
    "barrios-baratos-madrid-barcelona-2026.html",
    "aval-ico-primera-vivienda-2026.html",
    "gastos-comprar-piso-por-comunidad-2026.html",
    "hipoteca-fija-vs-variable-2026.html",
    "cuanto-ahorrar-comprar-piso-espana-2026.html",
    "cuando-es-buen-momento-comprar-piso-2026.html",
]

# Discover all articles with datePublished and categorize
articles_with_dates = []
for f in sorted(ROOT.glob("*.html")):
    txt = f.read_text(encoding="utf-8")
    if '"datePublished"' in txt:
        articles_with_dates.append(f.name)

print(f"Found {len(articles_with_dates)} articles with datePublished")

# Categorize
def category(name):
    if name in GROUP_A: return "A"
    if name in GROUP_C: return "C"
    if name in GROUP_D: return "D"
    for p in GROUP_B_PATTERNS:
        if re.match(p, name): return "B"
    return None

# Date pools
def date_pool(start_day, end_day):
    return [f"2026-05-{d:02d}" for d in range(start_day, end_day + 1)]

POOLS = {
    "A": date_pool(1, 10),
    "B": date_pool(5, 15),
    "C": date_pool(8, 18),
    "D": date_pool(12, 20),
}

# Visible date label
SP_MONTH = "mayo"
def visible_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {SP_MONTH} 2026"

# Deterministic-ish assignment so re-runs are stable
random.seed(42)

assignments = {}
categorized = 0
uncat = []
for name in articles_with_dates:
    cat = category(name)
    if cat is None:
        uncat.append(name)
        continue
    pool = POOLS[cat]
    chosen = random.choice(pool)
    assignments[name] = (cat, chosen)
    categorized += 1

print(f"Categorized: {categorized} | Uncategorized: {len(uncat)}")
if uncat:
    print("UNCAT:", uncat)
    # Assign Group A as fallback for any uncategorized
    for name in uncat:
        assignments[name] = ("A", random.choice(POOLS["A"]))

# Apply
RE_DATE_PUB = re.compile(r'"datePublished":\s*"\d{4}-\d{2}-\d{2}"')
RE_DATE_MOD = re.compile(r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"')
RE_VISIBLE_DATE = re.compile(r'(<span[^>]*class="an-card-date"[^>]*>📅\s*)\d{1,2}\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+202\d(\s*</span>)')

# Also handle bare dates like "Publicado: 18 mayo 2026" inside article bodies
RE_PUB_LABEL = re.compile(r'(Publicado:?\s*)\d{1,2}\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+202\d', re.IGNORECASE)

modified = 0
for name, (cat, iso_date) in assignments.items():
    f = ROOT / name
    if not f.exists():
        continue
    txt = f.read_text(encoding="utf-8")
    orig = txt
    # JSON-LD datePublished & dateModified
    txt = RE_DATE_PUB.sub(f'"datePublished": "{iso_date}"', txt)
    txt = RE_DATE_MOD.sub(f'"dateModified": "{iso_date}"', txt)
    # Article body "Publicado: X" labels
    txt = RE_PUB_LABEL.sub(lambda m: m.group(1) + visible_date(iso_date), txt)
    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        modified += 1

print(f"Articles modified in their own page: {modified}")

# Now update visible dates inside analisis.html (the index page that lists all articles)
analisis = ROOT / "analisis.html"
if analisis.exists():
    txt = analisis.read_text(encoding="utf-8")
    orig = txt
    # Each card has a link to an article and a date span. Walk through cards.
    # Pattern: <a href="ARTICLE.html">...</a> ... <span class="an-card-date">📅 DD mes YYYY</span>
    # Use a single-pass approach: find each card block and update its date.
    # Cards typically look like:
    #   <h2><a href="article.html">...</a></h2>
    #   ...
    #   <span class="an-card-date">📅 18 mayo 2026</span>
    # We'll iterate over article filenames and substitute the first occurrence
    # following each href.
    new_txt = txt
    for name, (cat, iso_date) in assignments.items():
        # Find the href, then the next an-card-date
        pat = re.compile(
            r'(href="' + re.escape(name) + r'"[\s\S]{0,2500}?<span[^>]*class="an-card-date"[^>]*>📅\s*)\d{1,2}\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+202\d'
        )
        new_txt = pat.sub(lambda m: m.group(1) + visible_date(iso_date), new_txt, count=1)
    if new_txt != txt:
        analisis.write_text(new_txt, encoding="utf-8")
        print("analisis.html dates updated")

print("\nBLOCK 2 done.")
