#!/usr/bin/env python3
"""Audit the 41 generated fichas: JSON-LD validity, population, mejor zona, photo size."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
META = ROOT / "data" / "cities_30k_50k_metadata.json"


def main():
    cities = json.loads(META.read_text(encoding="utf-8"))
    issues = []
    summary = []
    for city in cities:
        slug = city["slug"]; name = city["name"]; pop = city["pop"]; mejor = city["mejor_zona"]
        f = BETA / f"rentabilidad-{slug}.html"
        if not f.exists():
            issues.append(f"{slug}: HTML not found")
            continue
        html = f.read_text(encoding="utf-8")
        lines = html.count("\n") + 1

        # JSON-LD validity
        ld_blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        ld_ok = True
        for blk in ld_blocks:
            try:
                json.loads(blk)
            except json.JSONDecodeError as e:
                issues.append(f"{slug}: JSON-LD invalid: {e}")
                ld_ok = False
                break

        # photo
        photo = BETA / "img" / f"{slug}.webp"
        photo_kb = photo.stat().st_size // 1024 if photo.exists() else 0

        # population in demo-card
        m_pop = re.search(r'<div class="demo-card">\s*<div class="demo-icon">👥</div>\s*<div class="demo-val">([\d\.]+)</div>', html, re.DOTALL)
        pop_in_html = int(m_pop.group(1).replace(".", "")) if m_pop else 0

        # Mejor zona in sticky-bar
        m_mz = re.search(r'<span class="sb-label">Mejor zona</span><span class="sb-val blue">([^·]+) · ', html)
        mejor_in_html = m_mz.group(1).strip() if m_mz else ""

        status = "OK"
        if not ld_ok:
            status = "FAIL JSON-LD"
        if pop_in_html != pop:
            issues.append(f"{slug}: pop mismatch (html={pop_in_html} vs meta={pop})")
            status = "WARN pop"
        if mejor_in_html != mejor:
            issues.append(f"{slug}: mejor_zona mismatch (html='{mejor_in_html}' vs meta='{mejor}')")
            status = "WARN zona"
        if lines < 1000:
            issues.append(f"{slug}: file too short ({lines} lines)")
            status = "WARN short"
        if photo_kb == 0:
            issues.append(f"{slug}: photo missing")
            status = "WARN photo"
        elif photo_kb > 250:
            issues.append(f"{slug}: photo too big ({photo_kb}KB)")
            status = "WARN photo size"

        summary.append((slug, photo_kb, lines, status))

    print("\n=== SUMMARY TABLE ===")
    print(f"{'slug':<32} {'KB':>5} {'lines':>6}  status")
    print("-" * 65)
    for s, kb, ln, st in summary:
        print(f"{s:<32} {kb:>5} {ln:>6}  {st}")

    print(f"\n=== ISSUES ({len(issues)}) ===")
    for i in issues:
        print("-", i)

    print(f"\nTotal: {len(summary)} fichas, {len(issues)} issues")


if __name__ == "__main__":
    main()
