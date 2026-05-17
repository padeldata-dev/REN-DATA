#!/usr/bin/env python3
"""Lista municipios espanoles con poblacion > 50.000 que NO tienen pagina rentabilidad-*.html."""
import re
import unicodedata
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "raw" / "pobmun" / "pobmun25.xlsx"
HTML_DIR = ROOT / "rendata_beta"

# Mapeo CPRO (INE) -> CCAA
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


def _strip_accents(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def _normalize_article(name: str) -> str:
    """Normaliza 'X, Las/El/La/Los/L' -> 'Las/El/... X'."""
    m = re.match(r"^(.+?),\s*(Las|Los|La|El|L'|A|O|As|Os)$", name, re.IGNORECASE)
    if m:
        body, art = m.group(1), m.group(2)
        return f"{art} {body}".strip()
    return name


def slugify(name: str) -> str:
    """Convierte un nombre a slug estilo rendata."""
    name = name.split("/")[0].strip()
    name = _normalize_article(name)
    name = _strip_accents(name)
    name = name.lower()
    name = re.sub(r"['`´]", " ", name)
    name = re.sub(r"[^a-z0-9\s-]", " ", name)
    name = re.sub(r"\s+", "-", name.strip())
    name = re.sub(r"-+", "-", name)
    return name


# Slugs alternativos comunes (alias)
ALIASES = {
    "a-coruna": ["coruna", "la-coruna"],
    "alcala-de-henares": ["alcala"],
    "palma": ["palma-de-mallorca"],
    "las-palmas-de-gran-canaria": ["las-palmas-gc", "las-palmas"],
    "santa-cruz-de-tenerife": ["santa-cruz"],
    "san-cristobal-de-la-laguna": ["la-laguna"],
    "logrono": ["logrono"],
    "vitoria-gasteiz": ["vitoria"],
    "donostia-san-sebastian": ["san-sebastian"],
    "pamplona-iruna": ["pamplona"],
    "ourense": ["ourense", "orense"],
    "castello-de-la-plana": ["castellon-de-la-plana", "castellon"],
    "elx-elche": ["elche"],
    "alacant-alicante": ["alicante"],
    "valencia": ["valencia"],
    "xativa": ["xativa", "jativa"],
    "l-hospitalet-de-llobregat": ["l-hospitalet-de-llobregat", "hospitalet-de-llobregat"],
    "sant-cugat-del-valles": ["sant-cugat-del-valles"],
    "el-prat-de-llobregat": ["el-prat-de-llobregat", "prat-de-llobregat"],
}


def candidate_slugs(name: str) -> list[str]:
    """Devuelve lista de slugs candidatos a probar."""
    base = slugify(name)
    cands = {base}
    # Si el nombre tiene parte bilingue "X/Y", probar la segunda
    if "/" in name:
        cands.add(slugify(name.split("/")[1]))
    # Tambien sin el articulo (las-rozas vs rozas)
    for art in ("las-", "los-", "la-", "el-", "l-", "a-", "o-", "as-", "os-"):
        if base.startswith(art):
            cands.add(base[len(art):])
    # Variantes catalanas/euskera comunes -> castellano
    cc_map = {
        "ll": "ll",  # mantener
    }
    # Aliases manuales bidireccionales
    extra = {
        "palmas-de-gran-canaria": ["las-palmas-gc", "las-palmas", "las-palmas-de-gran-canaria"],
        "hospitalet-de-llobregat": ["l-hospitalet-de-llobregat", "hospitalet"],
        "coruna": ["a-coruna"],
        "rozas": ["las-rozas"],
        "san-fernando": ["san-fernando-cadiz", "san-fernando-de-henares"],
        "cornella-de-llobregat": ["cornell-de-llobregat"],
        "ejido": ["el-ejido"],
        "puerto-de-santa-maria": ["el-puerto-de-santa-maria"],
        "arona": ["arona-tenerife-sur"],
        "arrecife": ["lanzarote-arrecife"],
        "prat-de-llobregat": ["el-prat-de-llobregat"],
        "linea-de-la-concepcion": ["la-linea-de-la-concepcion"],
        "eivissa": ["ibiza"],
        "vila-real": ["villarreal"],
        "donostia-san-sebastian": ["san-sebastian"],
        "pamplona-iruna": ["pamplona"],
        "vitoria-gasteiz": ["vitoria"],
        "castello-de-la-plana": ["castellon-de-la-plana", "castellon"],
        "elx-elche": ["elche"],
        "alacant-alicante": ["alicante"],
        "xativa": ["jativa"],
        "ourense": ["orense"],
        "ciutadella-de-menorca": ["ciutadella-de-menorca"],
        "fuerteventura": ["fuerteventura-pjto-rosario"],
        "puerto-del-rosario": ["fuerteventura-pjto-rosario"],
        "san-bartolome-de-tirajana": ["san-bartolome-de-tirajana"],
        "san-cristobal-de-la-laguna": ["la-laguna"],
    }
    for needle, alts in extra.items():
        if needle in base or base in needle:
            cands.update(alts)
        for a in alts:
            if a in base or base in a:
                cands.add(needle)
    # Si nombre original sin articulo termina en algo, probar tambien
    no_art = _strip_accents(name.split("/")[0].split(",")[0]).lower()
    no_art = re.sub(r"[^a-z0-9\s-]", " ", no_art)
    no_art = re.sub(r"\s+", "-", no_art.strip())
    cands.add(no_art)
    return list(cands)


def page_exists(name: str) -> tuple[bool, str | None]:
    for s in candidate_slugs(name):
        if (HTML_DIR / f"rentabilidad-{s}.html").is_file():
            return True, s
    return False, None


def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb.active

    # Filtrar municipios > 50.000 hab
    rows = []
    for r in ws.iter_rows(min_row=3, values_only=True):
        cpro, provincia, cmun, nombre, pob, hombres, mujeres = r
        if not cpro or not nombre or not pob:
            continue
        try:
            pob = int(pob)
        except (ValueError, TypeError):
            continue
        if pob < 50000:
            continue
        ccaa = CPRO_CCAA.get(str(cpro).zfill(2), "??")
        rows.append((nombre, pob, provincia, ccaa))

    rows.sort(key=lambda x: -x[1])

    # Comprobar cuales no tienen pagina
    missing = []
    present = []
    for name, pob, prov, ccaa in rows:
        ok, matched_slug = page_exists(name)
        if ok:
            present.append((name, pob, ccaa, matched_slug))
        else:
            slug = slugify(name)
            missing.append((name, pob, ccaa, slug))

    print(f"Total municipios >50k habitantes: {len(rows)}")
    print(f"Con pagina rentabilidad-*.html: {len(present)}")
    print(f"SIN pagina: {len(missing)}")
    print()
    print("=== FALTAN ===")
    print(f"{'#':>3}  {'Nombre':<45} {'Poblacion':>10}  {'CCAA':<20}  slug propuesto")
    print("-" * 110)
    for i, (name, pob, ccaa, slug) in enumerate(missing, 1):
        print(f"{i:>3}  {name:<45} {pob:>10,}  {ccaa:<20}  {slug}")


if __name__ == "__main__":
    main()
