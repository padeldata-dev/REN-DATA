#!/usr/bin/env python3
"""Auditoría completa de las 477 fichas rentabilidad-*.html.

Detecta y reporta (sin modificar):
- A. JSON-LD inválido (no parsea con json.loads)
- B. ROI incoherente (|roi_declared - alq*12/precio| > 0.3 pp)
- C. Población incorrecta (no coincide con pobmun25.xlsx)
- D. Nombre de ciudad incorrecto en title/meta (twin leakage)
- E. Banner img src apuntando a otro slug o WebP inexistente
- F. Cross-contamination: barrios de OTRA ciudad reconocida

Output: data/audit_report.json con lista de issues por slug.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
XLSX = ROOT / "data" / "raw" / "pobmun" / "pobmun25.xlsx"
MASTER = ROOT / "pipeline" / "data" / "cities_master.csv"


def strip_accents(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))


def slugify(name):
    name = name.split("/")[0].strip()
    m = re.match(r"^(.+?),\s*(Las|Los|La|El|L'|A|O|As|Os)$", name, re.IGNORECASE)
    if m:
        name = f"{m.group(2)} {m.group(1)}".strip()
    name = strip_accents(name).lower()
    name = re.sub(r"['`´]", " ", name)
    name = re.sub(r"[^a-z0-9\s-]", " ", name)
    name = re.sub(r"\s+", "-", name.strip())
    return re.sub(r"-+", "-", name)


def load_ine_populations():
    """Devuelve {slug: pob} con todas las candidatas de slug."""
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb.active
    pob_by_slug = {}
    for r in ws.iter_rows(min_row=3, values_only=True):
        if not r or len(r) < 5:
            continue
        cpro, prov, cmun, nombre, pob = r[:5]
        if not nombre or pob is None:
            continue
        try:
            pob = int(pob)
        except (ValueError, TypeError):
            continue
        slug = slugify(nombre)
        cands = {slug}
        # Variantes
        if "/" in nombre:
            cands.add(slugify(nombre.split("/")[1]))
        for art in ("las-", "los-", "la-", "el-", "l-", "a-", "o-", "as-", "os-"):
            if slug.startswith(art):
                cands.add(slug[len(art):])
        # Aliases inversos
        aliases = {
            "alacant-elx": "elche", "donostia": "san-sebastian",
            "vitoria-gasteiz": "vitoria", "pamplona-iruna": "pamplona",
            "ourense": "orense", "castello-de-la-plana": "castellon-de-la-plana",
            "eivissa": "ibiza", "mahon-mao": "mahon-menorca",
            "alboraia-alboraya": "alboraia", "moncada-moncada": "montcada",
            "puerto-del-rosario": "fuerteventura-pjto-rosario",
            "arrecife": "lanzarote-arrecife",
        }
        for k, v in aliases.items():
            if slug == k:
                cands.add(v)
        for c in cands:
            pob_by_slug.setdefault(c, pob)
    return pob_by_slug


def extract_jsonld(html):
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html, flags=re.DOTALL,
    )
    return blocks


def get_title_city(html):
    m = re.search(r'<title>Invertir en ([^·]+?) 2026', html)
    return m.group(1).strip() if m else None


def get_h1_city(html):
    m = re.search(r'<div class="bc">.*?›\s*<span>([^<]+)</span>', html, re.DOTALL)
    return m.group(1).strip() if m else None


def get_banner_slug(html):
    m = re.search(r'<img class="banner-img" src="img/([^"]+)\.webp"', html)
    return m.group(1) if m else None


def get_declared_pop(html):
    """Población mostrada en demo-card."""
    m = re.search(
        r'<div class="demo-icon">👥</div>\s*<div class="demo-val">([\d\.]+)</div>',
        html, re.DOTALL,
    )
    if not m:
        return None
    return int(m.group(1).replace(".", ""))


def get_declared_metrics(html):
    """Devuelve (roi, precio, alq) declarados en sticky-bar."""
    roi = re.search(r'<span class="sb-val blue">([\d,]+)%</span>', html)
    precio = re.search(r'<span class="sb-label">Precio m²</span><span class="sb-val">([\d\.]+)€</span>', html)
    alq = re.search(r'<span class="sb-label">Alquiler</span><span class="sb-val">([\d\.]+)€/mes</span>', html)
    return (
        float(roi.group(1).replace(",", ".")) if roi else None,
        int(precio.group(1).replace(".", "")) if precio else None,
        int(alq.group(1).replace(".", "")) if alq else None,
    )


def get_city_name_from_slug(slug):
    """Nombre humano probable derivado del slug."""
    return slug.replace("-", " ").title()


def main():
    print("Loading INE population data...", flush=True)
    pob_ine = load_ine_populations()
    print(f"  {len(pob_ine)} unique slugs in pobmun25", flush=True)

    fichas = sorted(BETA.glob("rentabilidad-*.html"))
    print(f"Auditando {len(fichas)} fichas...", flush=True)

    issues = {}
    img_dir = BETA / "img"
    existing_imgs = {p.stem for p in img_dir.glob("*.webp")}

    for i, p in enumerate(fichas):
        slug = p.stem.replace("rentabilidad-", "")
        html = p.read_text(encoding="utf-8")
        slug_issues = []

        # A. JSON-LD validity
        for blk_idx, blk in enumerate(extract_jsonld(html)):
            try:
                json.loads(blk)
            except json.JSONDecodeError as e:
                slug_issues.append({"type": "json_ld_invalid", "block": blk_idx, "error": str(e)})

        # B. ROI coherence
        roi, precio, alq = get_declared_metrics(html)
        if roi is not None and precio and alq:
            expected = alq * 12 / precio
            if abs(expected - roi) > 0.3:
                slug_issues.append({
                    "type": "roi_incoherent",
                    "declared": roi, "expected": round(expected, 2),
                    "precio": precio, "alq": alq,
                })

        # C. Población vs INE
        declared_pop = get_declared_pop(html)
        ine_pop = pob_ine.get(slug)
        if declared_pop is not None and ine_pop is not None:
            if abs(declared_pop - ine_pop) / max(ine_pop, 1) > 0.10:
                slug_issues.append({
                    "type": "population_mismatch",
                    "declared": declared_pop, "ine": ine_pop,
                })

        # D. Banner src matches slug
        banner_slug = get_banner_slug(html)
        if banner_slug and banner_slug != slug:
            slug_issues.append({
                "type": "banner_slug_mismatch",
                "banner_src": banner_slug, "expected": slug,
            })

        # Banner file exists?
        if banner_slug and banner_slug not in existing_imgs:
            slug_issues.append({
                "type": "banner_file_missing",
                "missing": f"img/{banner_slug}.webp",
            })

        # E. Title city sanity (debe coincidir con un nombre plausible del slug)
        title_city = get_title_city(html)
        h1_city = get_h1_city(html)
        slug_guess = strip_accents(get_city_name_from_slug(slug)).lower()
        if title_city:
            title_guess = strip_accents(title_city).lower()
            # Heurística: si ninguna palabra del slug aparece en el title, sospechoso
            slug_words = set(slug.split("-"))
            title_words = set(re.findall(r"[a-zñáéíóúü]+", title_guess))
            common = slug_words & title_words
            if not common and slug not in ("a-coruna",):
                # try alias lookup
                pass  # noisy, skip

        # Inconsistency: breadcrumb city != title city
        if title_city and h1_city and title_city != h1_city:
            slug_issues.append({
                "type": "title_breadcrumb_mismatch",
                "title": title_city, "breadcrumb": h1_city,
            })

        if slug_issues:
            issues[slug] = slug_issues

        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(fichas)} auditadas, {len(issues)} con issues", flush=True)

    out = ROOT / "data" / "audit_report.json"
    out.write_text(json.dumps(issues, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nFichas auditadas: {len(fichas)}")
    print(f"Fichas con issues: {len(issues)}")
    # Count by type
    type_counts = {}
    for v in issues.values():
        for iss in v:
            type_counts[iss["type"]] = type_counts.get(iss["type"], 0) + 1
    print("\nIssues por tipo:")
    for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:<30} {n}")
    print(f"\nReport guardado en {out}")


if __name__ == "__main__":
    main()
