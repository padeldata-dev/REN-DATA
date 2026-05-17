#!/usr/bin/env python3
"""Corrige errores criticos B1 (barrios) y B2 (poblaciones) en las 5 fichas afectadas."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "rendata_beta"

# B1: barrio inventado -> barrio real
B1_FIXES = {
    "colmenar-viejo": ("Los Pajaritos", "La Estación"),
    "vila-real": ("El Grao de Vila-real", "Madrigal"),
    "ceuta": ("La Laguna", "El Centro"),
    "melilla": ("La Laguna", "Centro"),
}

# B2: poblacion incorrecta -> poblacion real INE 2025
B2_FIXES = {
    "santa-coloma-de-gramenet": ("289.510", "123.981"),
    "melilla":                   ("109.950", "86.780"),
    "valdemoro":                 ("60.419",  "85.972"),
    "ceuta":                     ("109.950", "83.595"),
}


def fix_b1(slug: str, before: str, after: str) -> int:
    path = ROOT / f"rentabilidad-{slug}.html"
    text = path.read_text(encoding="utf-8")
    n = text.count(before)
    if n == 0:
        print(f"[B1] {slug}: no occurrences of '{before}'")
        return 0
    text = text.replace(before, after)
    path.write_text(text, encoding="utf-8")
    print(f"[B1] {slug}: reemplazadas {n} apariciones de '{before}' -> '{after}'")
    return n


def fix_b2(slug: str, before: str, after: str) -> int:
    path = ROOT / f"rentabilidad-{slug}.html"
    text = path.read_text(encoding="utf-8")
    n = text.count(before)
    if n == 0:
        print(f"[B2] {slug}: no occurrences of '{before}'")
        return 0
    text = text.replace(before, after)
    path.write_text(text, encoding="utf-8")
    print(f"[B2] {slug}: reemplazadas {n} apariciones de '{before}' -> '{after}'")
    return n


def fix_sant_vicent_demo() -> int:
    """Anade el demo-card de Habitantes al inicio del demo-grid en sant-vicent."""
    path = ROOT / "rentabilidad-sant-vicent-del-raspeig.html"
    text = path.read_text(encoding="utf-8")
    if "60.247" in text and 'Habitantes' in text:
        # Comprobar si ya hay demo-card de Habitantes
        if re.search(r'<div class="demo-val">60\.247</div>\s*<div class="demo-label">Habitantes', text):
            print("[B2] sant-vicent: demo-card Habitantes ya existe, skip")
            return 0
    hab_card = (
        '<div class="demo-grid">\n'
        '      <div class="demo-card">\n'
        '        <div class="demo-icon">👥</div>\n'
        '        <div class="demo-val">60.247</div>\n'
        '        <div class="demo-label">Habitantes</div>\n'
        '        <div class="demo-trend" style="color:var(--green)">+1.8% anual</div>\n'
        '      </div>\n'
        '      <div class="demo-card">'
    )
    new_text, n = re.subn(
        r'<div class="demo-grid">\s*\n\s*<div class="demo-card">',
        hab_card,
        text,
        count=1,
    )
    if n == 0:
        print("[B2] sant-vicent: NO demo-grid pattern match (?)")
        return 0
    path.write_text(new_text, encoding="utf-8")
    print("[B2] sant-vicent: anadido demo-card Habitantes (60.247)")
    return 1


def main():
    total = 0
    print("=== B1 — Barrios ===")
    for slug, (before, after) in B1_FIXES.items():
        total += fix_b1(slug, before, after)
    print("\n=== B2 — Poblaciones ===")
    for slug, (before, after) in B2_FIXES.items():
        total += fix_b2(slug, before, after)
    total += fix_sant_vicent_demo()
    print(f"\nTotal substituciones: {total}")


if __name__ == "__main__":
    main()
