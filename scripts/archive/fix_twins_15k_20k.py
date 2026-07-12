#!/usr/bin/env python3
"""Validates and fixes twin references in 15k-20k metadata.

For each city in cities_15k_20k_metadata.json, ensure twin exists in beta.
If twin points to another city in the SAME batch, replace with an existing
slug from the same CCAA with similar profile.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_15k_20k_metadata.json"


def main():
    data = json.loads(META.read_text(encoding="utf-8"))
    existing = {p.stem.replace("rentabilidad-", "") for p in BETA.glob("rentabilidad-*.html")}
    batch = {c["slug"] for c in data}

    # Map of in-batch twin -> existing fallback
    fallbacks = {
        "cabra": "lucena",
        "atarfe": "armilla",
        "pineda-de-mar": "calella",
        "galdakao": "basauri",
        "burlada": "pamplona",
        "teguise": "lanzarote-arrecife",
        "marchena": "carmona",
        "mairena-del-alcor": "alcala-de-guadaira",
        "hernani": "errenteria",
        "cangas": "cangas-do-morrazo",
        "alhama-de-murcia": "totana",
        "l-alfas-del-pi": "altea",
        "calatayud": "calatayud",  # exists
        "mollerussa": "lleida",
        "la-garriga": "granollers",
        "cardedeu": "granollers",
        "malgrat-de-mar": "pineda-de-mar",  # use existing
        "ames": "santiago-de-compostela",
        "ribeira": "vilagarcia-de-arousa",
        "lalin": "vilagarcia-de-arousa",
        "san-andres-del-rabanedo": "leon",
        "mollet-del-valles": "mollet-del-valles",
        "meco": "alcala-de-henares",
        "villanueva-de-la-canada": "villaviciosa-de-odon",
        "camargo": "torrelavega",
        "baena": "lucena",
        "calafell": "calafell",
        "poio": "sanxenxo",
        "estepona": "estepona",
        "erandio": "leioa",
        "arahal": "marchena",
        "durango": "durango",
        "candelaria": "guimar",
        "buñol": "requena",
        "cieza": "cieza",
        "esparreguera": "esplugues-de-llobregat",
        "tarrega": "lleida",
        "manzanares": "tomelloso",
        "tomelloso": "tomelloso",
        "vilanova-i-la-geltru": "vilanova-i-la-geltru",
        "guardamar-del-segura": "guardamar-del-segura",
        "alboraia": "burjassot",
        "san-lorenzo-de-el-escorial": "san-lorenzo-de-el-escorial",
        "olot": "olot",
        "granollers": "granollers",
        "o-porrino": "vigo",
        "sanxenxo": "sanxenxo",
        "oleiros": "oleiros",
        "catarroja": "catarroja",
        "medina-del-campo": "medina-del-campo",
        "linares": "linares",
        "tomares": "tomares",
        "calella": "calella",
        "lebrija": "lebrija",
        "isla-cristina": "isla-cristina",
        "armilla": "armilla",
        "alzira": "alzira",
        "molina-de-segura": "molina-de-segura",
        "la-rinconada": "la-rinconada",
        "amposta": "tortosa",
        "vallirana": "molins-de-rei",
        "vera": "vera",
        "eibar": "eibar",
        "tacoronte": "la-orotava",
        "utebo": "calatayud",
        "barbastro": "barbastro",
        "villalbilla": "alcala-de-henares",
        "siero": "siero",
        "manlleu": "vic",
        "collado-villalba": "collado-villalba",
        "villarrobledo": "villarrobledo",
        "santa-perpetua-de-mogoda": "barbera-del-valles",
        "tarancon": "cuenca",
        "alfafar": "catarroja",
        "arcos-de-la-frontera": "arcos-de-la-frontera",
        "canovelles": "granollers",
        "vilagarcia-de-arousa": "vilagarcia-de-arousa",
        "bormujos": "bormujos",
        "calahorra": "calahorra",
        "llanes": "llanes",
        "langreo": "langreo",
        "nigran": "vigo",
        "molins-de-rei": "molins-de-rei",
        "tolosa": "tolosa",
        "la-zubia": "la-zubia",
        "la-orotava": "la-orotava",
        "la-oliva": "la-oliva",
        "el-ejido": "el-ejido",
        "callosa-de-segura": "orihuela",
        "orihuela": "orihuela",
        "almoradi": "orihuela",
        "betera": "paterna",
        "el-rosario": "guimar",
        "fuente-alamo-de-murcia": "totana",
    }

    fixed = 0
    for c in data:
        twin = c["twin"]
        if twin in existing:
            continue
        # Twin is missing or in-batch - find fallback
        fb = fallbacks.get(twin)
        if not fb or fb not in existing:
            # Try another fallback by CCAA
            ccaa_fb_map = {
                "Andalucía": "marchena",
                "Cataluña": "granollers",
                "C. Valenciana": "paterna",
                "Galicia": "vigo",
                "Castilla y León": "medina-del-campo",
                "Castilla-La Mancha": "tomelloso",
                "C. de Madrid": "alcala-de-henares",
                "País Vasco": "eibar",
                "Asturias": "siero",
                "Canarias": "telde",
                "Aragón": "calatayud",
                "Islas Baleares": "inca",
                "Cantabria": "torrelavega",
                "Extremadura": "merida",
                "Navarra": "pamplona",
                "La Rioja": "calahorra",
                "R. de Murcia": "molina-de-segura",
            }
            fb = ccaa_fb_map.get(c["ccaa"], "naron")
        if fb in existing:
            print(f"  {c['slug']}: {twin} -> {fb}")
            c["twin"] = fb
            fixed += 1
        else:
            print(f"  [WARN] {c['slug']}: fallback {fb} also missing")
            c["twin"] = "naron"
            fixed += 1

    META.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFixed: {fixed}")


if __name__ == "__main__":
    main()
