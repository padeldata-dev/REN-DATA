#!/usr/bin/env python3
"""Corrige las poblaciones declaradas en cada ficha usando INE pobmun25.xlsx.

Reemplaza el valor en demo-card '<div class="demo-icon">👥</div><div class="demo-val">XXX</div>'
con la población real INE. Tambien actualiza, si aparecen, los párrafos editoriales que
mencionan "<strong>NNN habitantes</strong>".
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
REPORT = ROOT / "data" / "audit_report.json"


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
        if "/" in nombre:
            cands.add(slugify(nombre.split("/")[1]))
        for art in ("las-", "los-", "la-", "el-", "l-", "a-", "o-", "as-", "os-"):
            if slug.startswith(art):
                cands.add(slug[len(art):])
        for c in cands:
            pob_by_slug.setdefault(c, pob)
    # Manual aliases (slug en site -> nombre INE)
    manual = {
        "elche": "elche", "alicante": "alicante", "san-sebastian": "donostia",
        "vitoria": "vitoria-gasteiz", "pamplona": "pamplona-iruna",
        "orense": "ourense", "castellon": "castello-de-la-plana",
        "castellon-de-la-plana": "castello-de-la-plana",
        "ibiza": "eivissa", "mahon-menorca": "mahon-mao",
        "fuerteventura-pjto-rosario": "puerto-del-rosario",
        "lanzarote-arrecife": "arrecife",
        "cangas-do-morrazo": "cangas",
        "alboraia": "alboraia-alboraya",
        "montcada": "moncada-moncada",
        "moncada": "moncada-moncada",
        "a-coruna": "coruna-a",
    }
    # build reverse INE map for direct lookups
    return pob_by_slug


def fmt_eu(n):
    return f"{n:,}".replace(",", ".")


def main():
    pob_ine = load_ine_populations()
    issues = json.loads(REPORT.read_text(encoding="utf-8"))

    # Augment with extra slug aliases observed in site:
    extra = {
        "cangas-do-morrazo": pob_ine.get("cangas"),
        "fuerteventura-pjto-rosario": pob_ine.get("puerto-del-rosario"),
        "lanzarote-arrecife": pob_ine.get("arrecife"),
        "elche": pob_ine.get("elx-elche") or pob_ine.get("alacant-elx") or pob_ine.get("elche"),
        "alicante": pob_ine.get("alacant-alicante") or pob_ine.get("alacant") or pob_ine.get("alicante"),
        "san-sebastian": pob_ine.get("donostia-san-sebastian") or pob_ine.get("donostia"),
        "vitoria": pob_ine.get("vitoria-gasteiz"),
        "pamplona": pob_ine.get("pamplona-iruna") or pob_ine.get("iruna"),
        "orense": pob_ine.get("ourense"),
        "castellon": pob_ine.get("castello-de-la-plana") or pob_ine.get("castellon-de-la-plana"),
        "castellon-de-la-plana": pob_ine.get("castello-de-la-plana") or pob_ine.get("castellon-de-la-plana"),
        "ibiza": pob_ine.get("eivissa"),
        "mahon-menorca": pob_ine.get("mahon-mao") or pob_ine.get("mao"),
        "a-coruna": pob_ine.get("coruna-a") or pob_ine.get("a-coruna"),
    }
    for k, v in extra.items():
        if v:
            pob_ine[k] = v

    fixed = 0
    failed = []
    for slug, lst in issues.items():
        pop_issue = next((i for i in lst if i["type"] == "population_mismatch"), None)
        if not pop_issue:
            continue
        real_pop = pob_ine.get(slug)
        if not real_pop:
            failed.append((slug, "no INE pop"))
            continue
        p = BETA / f"rentabilidad-{slug}.html"
        html = p.read_text(encoding="utf-8")
        declared = pop_issue["declared"]
        declared_str = fmt_eu(declared)
        new_str = fmt_eu(real_pop)
        if declared_str == new_str:
            continue

        # demo-card pop
        new_html = re.sub(
            r'(<div class="demo-icon">👥</div>\s*<div class="demo-val">)[\d\.]+(</div>)',
            rf'\g<1>{new_str}\g<2>',
            html, count=1, flags=re.DOTALL,
        )

        # Editorial paragraph "<strong>NNN habitantes</strong>"
        new_html = re.sub(
            rf'<strong>{re.escape(declared_str)} habitantes</strong>',
            f'<strong>{new_str} habitantes</strong>',
            new_html,
        )

        if new_html != html:
            p.write_text(new_html, encoding="utf-8")
            fixed += 1
            if fixed % 30 == 0:
                print(f"  fixed {fixed}", flush=True)

    print(f"\nPoblaciones corregidas: {fixed}")
    if failed:
        print(f"\nNo se pudo obtener pop INE para {len(failed)}:")
        for s, why in failed[:20]:
            print(f"  {s}: {why}")


if __name__ == "__main__":
    main()
