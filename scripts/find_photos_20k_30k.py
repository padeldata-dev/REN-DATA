#!/usr/bin/env python3
"""Busca fotos en Wikimedia Commons para las 100 ciudades 20k-30k."""
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

USER_AGENT = "RenData/1.0 (https://rendata.es) Python/urllib"

CITIES_SEARCH = {
    "puente-genil": "Puente Genil Córdoba",
    "san-andres-del-rabanedo": "San Andrés del Rabanedo León",
    "sant-josep-de-sa-talaia": "Sant Josep de sa Talaia Ibiza",
    "lepe": "Lepe Huelva",
    "vicar": "Vícar Almería",
    "cartama": "Cártama Málaga",
    "martorell": "Martorell Barcelona",
    "almassora": "Almassora Castellón",
    "sant-antoni-de-portmany": "Sant Antoni de Portmany",
    "camas": "Camas Sevilla",
    "candelaria": "Candelaria Tenerife",
    "redondela": "Redondela Pontevedra",
    "sant-vicenc-dels-horts": "Sant Vicenç dels Horts",
    "mutxamel": "Mutxamel Alicante",
    "betera": "Bétera Valencia",
    "sestao": "Sestao Bizkaia",
    "paiporta": "Paiporta Valencia",
    "calp": "Calp Alicante",
    "la-pobla-de-vallbona": "Pobla de Vallbona",
    "molins-de-rei": "Molins de Rei",
    "ribeira": "Ribeira A Coruña",
    "sant-andreu-de-la-barca": "Sant Andreu de la Barca",
    "quart-de-poblet": "Quart de Poblet",
    "pielagos": "Piélagos Cantabria",
    "sant-joan-d-alacant": "Sant Joan d'Alacant",
    "cangas": "Cangas Pontevedra",
    "novelda": "Novelda Alicante",
    "ciempozuelos": "Ciempozuelos Madrid",
    "alboraia": "Alboraia Valencia",
    "onda": "Onda Castellón",
    "santa-perpetua-de-mogoda": "Santa Perpètua de Mogoda",
    "caravaca-de-la-cruz": "Caravaca de la Cruz",
    "villanueva-de-la-serena": "Villanueva de la Serena Badajoz",
    "valls": "Valls Tarragona",
    "castellar-del-valles": "Castellar del Vallès",
    "villarrobledo": "Villarrobledo Albacete",
    "galdar": "Gáldar Gran Canaria",
    "mejorada-del-campo": "Mejorada del Campo Madrid",
    "olesa-de-montserrat": "Olesa de Montserrat",
    "almonte": "Almonte Huelva",
    "galdakao": "Galdakao Bizkaia",
    "cambre": "Cambre A Coruña",
    "el-masnou": "El Masnou Maresme",
    "erandio": "Erandio Bizkaia",
    "tacoronte": "Tacoronte Tenerife",
    "icod-de-los-vinos": "Icod de los Vinos",
    "riba-roja-de-turia": "Riba-roja de Túria",
    "ibi": "Ibi Alicante",
    "los-barrios": "Los Barrios Cádiz",
    "alhama-de-murcia": "Alhama de Murcia",
    "moguer": "Moguer Huelva",
    "villanueva-de-la-canada": "Villanueva de la Cañada Madrid",
    "marin": "Marín Pontevedra",
    "san-miguel-de-abona": "San Miguel de Abona Tenerife",
    "las-gabias": "Las Gabias Granada",
    "san-juan-de-aznalfarache": "San Juan de Aznalfarache",
    "ponteareas": "Ponteareas Pontevedra",
    "picassent": "Picassent Valencia",
    "sant-feliu-de-guixols": "Sant Feliu de Guíxols",
    "amposta": "Amposta Tarragona",
    "almoradi": "Almoradí Alicante",
    "laguna-de-duero": "Laguna de Duero Valladolid",
    "valle-de-egues": "Sarriguren Navarra",
    "arroyo-de-la-encomienda": "Arroyo de la Encomienda Valladolid",
    "aljaraque": "Aljaraque Huelva",
    "las-torres-de-cotillas": "Las Torres de Cotillas",
    "esparreguera": "Esparreguera Barcelona",
    "guia-de-isora": "Guía de Isora Tenerife",
    "barbate": "Barbate Cádiz",
    "aspe": "Aspe Alicante",
    "maracena": "Maracena Granada",
    "alfafar": "Alfafar Valencia",
    "montcada": "Moncada Valencia",
    "ayamonte": "Ayamonte Huelva",
    "carcaixent": "Carcaixent Valencia",
    "pucol": "Puçol Valencia",
    "tias": "Puerto del Carmen Lanzarote",
    "pajara": "Morro Jable Fuerteventura",
    "cartaya": "Cartaya Huelva",
    "manlleu": "Manlleu Osona",
    "burlada": "Burlada Navarra",
    "vilassar-de-mar": "Vilassar de Mar",
    "mogan": "Puerto Rico Gran Canaria",
    "algete": "Algete Madrid",
    "l-alfas-del-pi": "Albir Alfàs del Pi",
    "sant-just-desvern": "Sant Just Desvern",
    "san-martin-de-la-vega": "San Martín de la Vega Madrid",
    "o-porrino": "O Porriño Pontevedra",
    "loja": "Loja Granada",
    "atarfe": "Atarfe Granada",
    "archena": "Archena Murcia",
    "franqueses-del-valles-les": "Les Franqueses del Vallès",
    "benicassim": "Benicàssim Castellón",
    "humanes-de-madrid": "Humanes de Madrid",
    "silla": "Silla Valencia",
    "la-zubia": "La Zubia Granada",
    "hernani": "Hernani Gipuzkoa",
    "lalin": "Lalín Pontevedra",
    "sant-quirze-del-valles": "Sant Quirze del Vallès",
    "a-estrada": "A Estrada Pontevedra",
}

ALT_QUERIES = ["{name}", "{name} panorámica", "vista {name}", "{name} centro"]


def search_wmc(query, limit=10):
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "format": "json",
    }
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  [ERR] {query}: {e}", file=sys.stderr)
        return None


def best_image(data):
    if not data or "query" not in data or "pages" not in data["query"]:
        return None
    pages = list(data["query"]["pages"].values())
    candidates = []
    for p in pages:
        ii = p.get("imageinfo", [])
        if not ii:
            continue
        info = ii[0]
        mime = info.get("mime", "")
        if "jpeg" not in mime and "jpg" not in mime:
            continue
        w = info.get("width", 0)
        h = info.get("height", 0)
        if h == 0:
            continue
        ratio = w / h
        if ratio < 1.2:
            continue
        title = p.get("title", "").lower()
        skip_words = ["coat", "escudo", "bandera", "flag", "logo", "mapa", "map", "ortof", "blason", "iglesia interior"]
        if any(s in title for s in skip_words):
            continue
        score = 0
        if w >= 2400:
            score += 10
        elif w >= 1800:
            score += 6
        elif w >= 1200:
            score += 2
        if ratio >= 2.0:
            score += 5
        elif ratio >= 1.5:
            score += 2
        boost = ["panoram", "vista", "skyline", "aerial", "view", "cityscape", "centro", "ayuntamiento", "casco", "pueblo", "plaza"]
        if any(b in title for b in boost):
            score += 3
        candidates.append((score, w, h, info["url"], p.get("title", "")))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0]


def find_for_city(slug, name):
    queries = [q.format(name=name) for q in ALT_QUERIES]
    best = None
    best_score = -1
    used_query = None
    for q in queries:
        data = search_wmc(q, limit=8)
        sel = best_image(data)
        if sel and sel[0] > best_score:
            best = sel
            best_score = sel[0]
            used_query = q
        if best_score >= 13:
            break
        time.sleep(0.15)
    return best, used_query


def main():
    out_path = ROOT / "data" / "city_photos_20k_30k.json"
    results = {}
    if out_path.exists():
        try:
            results = json.loads(out_path.read_text(encoding="utf-8"))
        except Exception:
            results = {}

    for slug, name in CITIES_SEARCH.items():
        if slug in results and results[slug]:
            print(f"[skip] {slug}: already found", flush=True)
            continue
        print(f"[search] {slug} ({name})", flush=True)
        result, q = find_for_city(slug, name)
        if result:
            score, w, h, url, title = result
            results[slug] = {
                "url": url,
                "width": w,
                "height": h,
                "title": title,
                "query": q,
                "score": score,
            }
            print(f"  -> [{score}] {w}x{h} {title}", flush=True)
        else:
            results[slug] = None
            print(f"  -> NONE FOUND", flush=True)
        # Save incrementally
        out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
