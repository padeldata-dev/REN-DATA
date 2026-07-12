#!/usr/bin/env python3
"""Adds a 'Ciudades relacionadas' paragraph at the end of each ficha's editorial body.

Strategy:
1. Read all 587 entries from index.html DATA[]
2. For each city, pick 5 related cities = same CCAA + closest ROI (excluding self)
3. Find the ed-body closing </p> tag (the "Ciudades alternativas" line) and replace
   with an enhanced "Ciudades relacionadas" block.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"
INDEX = BETA / "index.html"


def fmt_pct(n):
    return f"{n:.1f}".replace(".", ",")


def parse_data():
    html = INDEX.read_text(encoding="utf-8")
    pat = re.compile(r'\{n:"([^"]+)",cc:"([^"]+)",reg:"([^"]+)",roi:([\d.]+),'
                     r'p:(\d+),alq:(\d+),vp:([\d.]+),va:([\d.]+),'
                     r'd:(\d+),sl:"([^"]+)"')
    rows = []
    for m in pat.finditer(html):
        rows.append({
            "n": m.group(1), "cc": m.group(2),
            "roi": float(m.group(4)), "p": int(m.group(5)), "alq": int(m.group(6)),
            "sl": m.group(10),
        })
    return rows


def pick_related(target, all_rows, n=5):
    """Pick N related cities: same CCAA preferred, closest ROI."""
    same_ccaa = [r for r in all_rows if r["cc"] == target["cc"] and r["sl"] != target["sl"]]
    same_ccaa.sort(key=lambda r: abs(r["roi"] - target["roi"]))
    related = same_ccaa[:n]
    if len(related) < n:
        # fill from rest by closest ROI
        others = [r for r in all_rows if r["cc"] != target["cc"] and r["sl"] != target["sl"]]
        others.sort(key=lambda r: abs(r["roi"] - target["roi"]))
        related.extend(others[:n - len(related)])
    return related


def build_related_block(city, related):
    """Build a 'Ciudades relacionadas' HTML block."""
    items = []
    for r in related:
        items.append(
            f'<a href="/rentabilidad-{r["sl"]}.html" '
            f'style="color:var(--blue);text-decoration:none;font-weight:600">'
            f'{r["n"]} ({fmt_pct(r["roi"])}%)</a>'
        )
    inner = " · ".join(items)
    return (
        '\n      <p style="margin-top:.75rem;padding-top:.75rem;border-top:1px solid var(--border);'
        'font-size:.85rem;color:var(--text2)"><strong>Ciudades relacionadas:</strong> '
        + inner + '</p>'
    )


# Pattern: replace the line "<strong>Ciudades alternativas:</strong> ...</p>" with our enhanced
# block. We append our block right after that <p> if it exists, or before the closing </div>
# of ed-body.

ALT_RE = re.compile(
    r'(<p style="margin-top:1rem;padding-top:1rem;border-top:1px solid var\(--border\);'
    r'font-size:\.85rem"><strong>Ciudades alternativas:</strong>[^<]*<a[^>]*>[^<]*</a>'
    r'(?:\s*·\s*<a[^>]*>[^<]*</a>)*</p>)'
)

MARKER = "Ciudades relacionadas:"


def main():
    rows = parse_data()
    by_slug = {r["sl"]: r for r in rows}
    fichas = sorted(BETA.glob("rentabilidad-*.html"))
    print(f"Processing {len(fichas)} fichas...")

    added = 0
    skipped = 0
    no_alt = 0
    for f in fichas:
        slug = f.stem.replace("rentabilidad-", "")
        # Skip comparison article rentabilidad-madrid-vs-barcelona-2026 etc.
        if "vs" in slug or slug not in by_slug:
            skipped += 1
            continue
        html = f.read_text(encoding="utf-8")
        if MARKER in html:
            skipped += 1
            continue

        city = by_slug[slug]
        related = pick_related(city, rows, 5)
        block = build_related_block(city, related)

        m = ALT_RE.search(html)
        if m:
            # Insert our block right after the alternativas <p>
            new_html = html[:m.end()] + block + html[m.end():]
        else:
            # Fallback: insert right before </div> closing ed-body
            # ed-body closing pattern
            ed_close = re.search(r'(</div>)\s*<!-- ed-body end -->', html)
            if ed_close:
                new_html = html[:ed_close.start()] + block + "\n    " + html[ed_close.start():]
            else:
                # Try generic: insert right after first </p> following <div class="ed-body">
                start = html.find('<div class="ed-body">')
                if start == -1:
                    no_alt += 1
                    continue
                # Find the closing </div> of ed-body by depth counting
                pos = start; depth = 0; end = -1
                while pos < len(html):
                    no_tag = html.find("<div", pos)
                    nc = html.find("</div>", pos)
                    if nc == -1:
                        break
                    if no_tag != -1 and no_tag < nc:
                        depth += 1; pos = no_tag + 4
                    else:
                        depth -= 1; pos = nc + 6
                        if depth == 0:
                            end = nc; break
                if end == -1:
                    no_alt += 1
                    continue
                new_html = html[:end] + block + "\n    " + html[end:]

        if new_html != html:
            f.write_text(new_html, encoding="utf-8")
            added += 1
            if added % 50 == 0:
                print(f"  added {added}")

    print(f"\nAdded related-cities to {added} fichas. Skipped: {skipped}. No alt block: {no_alt}")


if __name__ == "__main__":
    main()
