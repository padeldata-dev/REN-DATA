#!/usr/bin/env python3
"""Auditoria de las 7 fichas nuevas."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "rendata_beta"
SLUGS = [
    "santa-coloma-de-gramenet",
    "melilla",
    "valdemoro",
    "ceuta",
    "sant-vicent-del-raspeig",
    "colmenar-viejo",
    "vila-real",
]

# Datos esperados (precio_m2, alquiler_mes, roi_esperado)
EXPECTED = {
    "santa-coloma-de-gramenet": (2700, 1200, 5.3),
    "melilla":                  (1300, 700,  6.5),
    "valdemoro":                (2100, 950,  5.4),
    "ceuta":                    (1500, 780,  6.2),
    "sant-vicent-del-raspeig":  (1800, 870,  5.8),
    "colmenar-viejo":           (2400, 1050, 5.2),
    "vila-real":                (1200, 600,  6.0),
}

JSONLD_RE = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def audit_jsonld(slug, text):
    """Extrae y valida bloques JSON-LD."""
    issues = []
    blocks = JSONLD_RE.findall(text)
    if not blocks:
        issues.append("no JSON-LD found")
        return issues
    for i, raw in enumerate(blocks):
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            issues.append(f"JSON-LD block #{i+1}: {e.msg} at pos {e.pos}")
    return issues


def audit_roi(slug, text):
    """Verifica que el ROI matematicamente coincide para 100m² piso."""
    issues = []
    precio, alq, roi_esp = EXPECTED[slug]
    # ROI = (alq * 12) / (precio * 100) * 100
    roi_calc = (alq * 12) / (precio * 100) * 100
    if abs(roi_calc - roi_esp) > 0.1:
        issues.append(
            f"ROI inconsistente: esperado {roi_esp}%, "
            f"matematico {roi_calc:.2f}% (con precio {precio}€ y alq {alq}€)"
        )
    return issues, roi_calc


def audit_breadcrumb(slug, text):
    issues = []
    m = re.search(r'<div class="bc">(.*?)</div>', text, re.DOTALL)
    if not m:
        issues.append("no breadcrumb visible")
        return issues
    bc = m.group(1)
    if slug in ("ceuta", "melilla"):
        # No deben tener parent CCAA
        if "ccaa-" in bc:
            issues.append(f"breadcrumb apunta a CCAA (deberia ser solo Inicio>Ciudad): {bc.strip()}")
    else:
        if "ccaa-" not in bc:
            issues.append(f"breadcrumb sin parent CCAA: {bc.strip()}")
    return issues


def audit_banner_img(slug, text):
    issues = []
    m = re.search(r'<img class="banner-img"[^>]*>', text)
    if not m:
        issues.append("banner-img tag not found")
        return issues
    tag = m.group(0)
    expected_src = f"img/{slug}.webp"
    if expected_src not in tag:
        issues.append(f"banner src no apunta a {expected_src}: {tag}")
    if "width=" not in tag or "height=" not in tag:
        issues.append(f"banner sin width/height: {tag}")
    if "fetchpriority=" not in tag:
        issues.append(f"banner sin fetchpriority: {tag}")
    return issues


def audit_data_entry(slug):
    """Verifica que slug esta en DATA[] de index.html."""
    issues = []
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(rf'sl:"{re.escape(slug)}"', idx)
    if not m:
        issues.append(f"slug '{slug}' no aparece en DATA[] de index.html")
        return issues
    # Extraer la entrada completa
    line_start = idx.rfind("{", 0, m.start())
    line_end = idx.find("}", m.start())
    entry = idx[line_start:line_end+1]
    required = ["n:", "cc:", "reg:", "roi:", "p:", "alq:", "vp:", "va:", "d:", "sl:"]
    for f in required:
        if f not in entry:
            issues.append(f"DATA entry sin campo {f}: {entry[:100]}")
    return issues


def audit_sitemap(slug):
    issues = []
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"rentabilidad-{slug}.html" not in sm:
        issues.append(f"sitemap sin rentabilidad-{slug}.html")
    return issues


def audit_ccaa_links(slug):
    """Verifica enlaces desde paginas CCAA."""
    issues = []
    ccaa_map = {
        "santa-coloma-de-gramenet": "ccaa-cataluna.html",
        "valdemoro": "ccaa-madrid.html",
        "colmenar-viejo": "ccaa-madrid.html",
        "sant-vicent-del-raspeig": "ccaa-comunitat-valenciana.html",
        "vila-real": "ccaa-comunitat-valenciana.html",
    }
    if slug not in ccaa_map:
        return issues  # Ceuta/Melilla no tienen CCAA page
    ccaa_html = (ROOT / ccaa_map[slug]).read_text(encoding="utf-8")
    if f"/rentabilidad-{slug}.html" not in ccaa_html:
        issues.append(f"{ccaa_map[slug]} no enlaza a rentabilidad-{slug}.html")
    return issues


# Plantillas twin de cada ciudad
TWINS = {
    "santa-coloma-de-gramenet": ["L'Hospitalet", "Hospitalet"],
    "melilla": ["Cádiz", "Cadiz"],
    "valdemoro": ["Arganda", "Arganda del Rey"],
    "ceuta": ["Cádiz", "Cadiz"],
    "sant-vicent-del-raspeig": ["Burjassot"],
    "colmenar-viejo": ["Tres Cantos"],
    "vila-real": ["Burriana"],
}


def audit_residual_twin(slug, text):
    """Detecta menciones residuales de la ciudad twin (excepto cuando es legitima)."""
    issues = []
    twins = TWINS.get(slug, [])
    for twin in twins:
        # Contar ocurrencias del nombre de la twin
        count = text.count(twin)
        if count > 0:
            # Solo es problema si NO esta en "sim-card" o "cerc-card" o "ciudad alternativa"
            # Esos son enlaces a ciudades vecinas, perfectamente legitimos
            # Solo reportar las primeras 3 ocurrencias con contexto
            for m in re.finditer(re.escape(twin), text):
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                context = text[start:end].replace("\n", " ")
                # Filtrar contextos legitimos
                if any(legit in context for legit in [
                    "sim-card", "cerc-card", "cerc-name", "rentabilidad-",
                    "Alternativ", "alternativ", "cmp-city", "cercanos"
                ]):
                    continue
                issues.append(f"posible residuo de '{twin}': …{context}…")
                if len([i for i in issues if twin in i]) >= 3:
                    break
    return issues


def main():
    print(f"Auditoria de {len(SLUGS)} fichas nuevas\n")
    total_issues = 0
    for slug in SLUGS:
        path = ROOT / f"rentabilidad-{slug}.html"
        if not path.is_file():
            print(f"[FAIL] {slug}: archivo no existe")
            total_issues += 1
            continue
        text = path.read_text(encoding="utf-8")
        issues = []
        issues += [("JSON-LD", i) for i in audit_jsonld(slug, text)]
        roi_issues, roi_calc = audit_roi(slug, text)
        issues += [("ROI",     i) for i in roi_issues]
        issues += [("BC",      i) for i in audit_breadcrumb(slug, text)]
        issues += [("BANNER",  i) for i in audit_banner_img(slug, text)]
        issues += [("DATA[]",  i) for i in audit_data_entry(slug)]
        issues += [("SITEMAP", i) for i in audit_sitemap(slug)]
        issues += [("CCAA",    i) for i in audit_ccaa_links(slug)]
        issues += [("RESIDUO", i) for i in audit_residual_twin(slug, text)]
        if not issues:
            print(f"[OK]  {slug}  (ROI mat. {roi_calc:.2f}%)")
        else:
            print(f"[!!]  {slug}  (ROI mat. {roi_calc:.2f}%)")
            for cat, msg in issues:
                print(f"        [{cat}] {msg}")
            total_issues += len(issues)
    print(f"\nTotal de problemas: {total_issues}")


if __name__ == "__main__":
    main()
