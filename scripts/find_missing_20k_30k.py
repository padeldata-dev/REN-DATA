#!/usr/bin/env python3
"""Lista municipios espanoles 20.000-30.000 habitantes SIN pagina rentabilidad-*.html."""
import json
import re
import unicodedata
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "raw" / "pobmun" / "pobmun25.xlsx"
HTML_DIR = ROOT / "rendata_beta"

CPRO_CCAA = {
    "01": "País Vasco", "02": "Castilla-La Mancha", "03": "C. Valenciana",
    "04": "Andalucía", "05": "Castilla y León", "06": "Extremadura",
    "07": "Islas Baleares", "08": "Cataluña", "09": "Castilla y León",
    "10": "Extremadura", "11": "Andalucía", "12": "C. Valenciana",
    "13": "Castilla-La Mancha", "14": "Andalucía", "15": "Galicia",
    "16": "Castilla-La Mancha", "17": "Cataluña", "18": "Andalucía",
    "19": "Castilla-La Mancha", "20": "País Vasco", "21": "Andalucía",
    "22": "Aragón", "23": "Andalucía", "24": "Castilla y León",
    "25": "Cataluña", "26": "La Rioja", "27": "Galicia",
    "28": "C. de Madrid", "29": "Andalucía", "30": "R. de Murcia",
    "31": "Navarra", "32": "Galicia", "33": "Asturias",
    "34": "Castilla y León", "35": "Canarias", "36": "Galicia",
    "37": "Castilla y León", "38": "Canarias", "39": "Cantabria",
    "40": "Castilla y León", "41": "Andalucía", "42": "Castilla y León",
    "43": "Cataluña", "44": "Aragón", "45": "Castilla-La Mancha",
    "46": "C. Valenciana", "47": "Castilla y León", "48": "País Vasco",
    "49": "Castilla y León", "50": "Aragón",
    "51": "Ceuta", "52": "Melilla",
}


def _strip_accents(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def _normalize_article(name):
    m = re.match(r"^(.+?),\s*(Las|Los|La|El|L'|A|O|As|Os)$", name, re.IGNORECASE)
    if m:
        return f"{m.group(2)} {m.group(1)}".strip()
    return name


def slugify(name):
    name = name.split("/")[0].strip()
    name = _normalize_article(name)
    name = _strip_accents(name)
    name = name.lower()
    name = re.sub(r"['`´]", " ", name)
    name = re.sub(r"[^a-z0-9\s-]", " ", name)
    name = re.sub(r"\s+", "-", name.strip())
    name = re.sub(r"-+", "-", name)
    return name


def candidate_slugs(name):
    base = slugify(name)
    cands = {base}
    if "/" in name:
        cands.add(slugify(name.split("/")[1]))
    for art in ("las-", "los-", "la-", "el-", "l-", "a-", "o-", "as-", "os-"):
        if base.startswith(art):
            cands.add(base[len(art):])
    aliases = {
        "alacant-elx": ["elche"],
        "elche": ["elche", "elx-elche"],
        "alacant": ["alicante"],
        "donostia": ["san-sebastian"],
        "vitoria-gasteiz": ["vitoria"],
        "pamplona-iruna": ["pamplona"],
        "iruna": ["pamplona"],
        "ourense": ["orense"],
        "castello-de-la-plana": ["castellon-de-la-plana", "castellon"],
        "ciutadella-de-menorca": ["ciutadella-de-menorca"],
        "eivissa": ["ibiza"],
        "mahon-mao": ["mahon-menorca"],
        "vila-real": ["vila-real"],
        "puerto-del-rosario": ["fuerteventura-pjto-rosario"],
        "arrecife": ["lanzarote-arrecife"],
    }
    for k, vs in aliases.items():
        if base == k or base in vs:
            cands.update(vs)
            cands.add(k)
    no_art = _strip_accents(name.split("/")[0].split(",")[0]).lower()
    no_art = re.sub(r"[^a-z0-9\s-]", " ", no_art)
    no_art = re.sub(r"\s+", "-", no_art.strip())
    cands.add(no_art)
    return list(cands)


def page_exists(name):
    for s in candidate_slugs(name):
        if (HTML_DIR / f"rentabilidad-{s}.html").is_file():
            return True, s
    return False, None


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb.active
    rows = []
    for r in ws.iter_rows(min_row=3, values_only=True):
        cpro, provincia, cmun, nombre, pob, hombres, mujeres = r
        if not cpro or not nombre or not pob:
            continue
        try:
            pob = int(pob)
        except (ValueError, TypeError):
            continue
        if pob < 20000 or pob >= 30000:
            continue
        ccaa = CPRO_CCAA.get(str(cpro).zfill(2), "??")
        rows.append((nombre, pob, provincia, ccaa, cpro))

    rows.sort(key=lambda x: -x[1])

    missing = []
    present = []
    for name, pob, prov, ccaa, cpro in rows:
        ok, matched = page_exists(name)
        if ok:
            present.append((name, pob, ccaa, matched))
        else:
            missing.append((name, pob, prov, ccaa, slugify(name), cpro))

    print(f"Total municipios 20k-30k habitantes: {len(rows)}")
    print(f"Con pagina existente: {len(present)}")
    print(f"SIN pagina: {len(missing)}\n")
    print("=== MISSING ===")
    print(f"{'#':>3}  {'Slug':<35} {'Nombre':<40} {'Pop':>8}  {'CCAA':<22} {'Prov'}")
    print("-" * 130)
    for i, (name, pob, prov, ccaa, slug, cpro) in enumerate(missing, 1):
        print(f"{i:>3}  {slug:<35} {name:<40} {pob:>8,}  {ccaa:<22} {prov}")

    out = []
    for name, pob, prov, ccaa, slug, cpro in missing:
        out.append({
            "slug": slug,
            "nombre": name.split("/")[0].strip(),
            "ccaa": ccaa,
            "provincia": prov,
            "poblacion": pob,
            "cpro": str(cpro).zfill(2),
        })
    (ROOT / "data" / "missing_20k_30k.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nJSON guardado en data/missing_20k_30k.json")


if __name__ == "__main__":
    main()
