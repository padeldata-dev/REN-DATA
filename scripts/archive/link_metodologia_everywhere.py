#!/usr/bin/env python3
"""Add a 'Metodología' link to nav and footer of all rendata_beta/*.html.

Patterns we handle:
- Standard nav with <a href="/glosario.html">Glosario</a> — insert Metodología before Glosario
- Mobile nav with emoji <a href="/glosario.html">📖 Glosario</a> — same logic
- Footer with "Glosario" link — insert Metodología link
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BETA = ROOT / "rendata_beta"

# Skip files that already have metodologia.html (newly created or already updated)
# We'll add idempotently anyway: if 'metodologia.html' already appears, skip that file.


def add_nav_link(html):
    """Insert Metodología link in main nav before Glosario (standard pattern)."""
    if "/metodologia.html" in html:
        return html, False
    new_html = html
    changed = False

    # Pattern 1: standard desktop nav `<a href="/glosario.html">Glosario</a>`
    new_html, n = re.subn(
        r'(<a href="/glosario\.html">Glosario</a>)',
        r'<a href="/metodologia.html">Metodología</a>\n    \1',
        new_html, count=1,
    )
    if n > 0:
        changed = True

    # Pattern 2: mobile nav with emoji
    new_html, n = re.subn(
        r'(<a href="/glosario\.html">📖 Glosario</a>)',
        r'<a href="/metodologia.html">📊 Metodología</a>\n      \1',
        new_html, count=1,
    )
    if n > 0:
        changed = True

    return new_html, changed


def add_footer_link(html):
    """Insert Metodología link in footer links section before Privacidad/Aviso legal."""
    if html.count('href="/metodologia.html"') >= 2 or html.count('href="metodologia.html"') >= 2:
        return html, False  # already has multiple
    changed = False
    # Standard footer with <a href="privacidad.html">Privacidad</a>
    new_html, n = re.subn(
        r'(<a href="privacidad\.html">Privacidad</a>)',
        r'<a href="metodologia.html">Metodología</a>\n      \1',
        html, count=1,
    )
    if n > 0:
        changed = True
        return new_html, changed

    # Alternative: <a href="/privacidad.html">Privacidad</a>
    new_html, n = re.subn(
        r'(<a href="/privacidad\.html">Privacidad</a>)',
        r'<a href="/metodologia.html">Metodología</a>\n      \1',
        html, count=1,
    )
    if n > 0:
        changed = True

    return new_html, changed


def main():
    files = sorted(BETA.glob("*.html"))
    # Skip metodologia.html (itself) and contacto.html (already has the link), widget-demo (already has it)
    skip = {"metodologia.html"}

    nav_added = footer_added = both = 0
    untouched = 0
    skipped_files = 0

    for p in files:
        if p.name in skip:
            skipped_files += 1
            continue
        html = p.read_text(encoding="utf-8")
        html2, nav_changed = add_nav_link(html)
        html3, footer_changed = add_footer_link(html2)
        if nav_changed or footer_changed:
            p.write_text(html3, encoding="utf-8")
            if nav_changed and footer_changed:
                both += 1
            elif nav_changed:
                nav_added += 1
            else:
                footer_added += 1
        else:
            untouched += 1

    print(f"Files processed: {len(files) - skipped_files}")
    print(f"  Nav + footer updated: {both}")
    print(f"  Only nav updated:     {nav_added}")
    print(f"  Only footer updated:  {footer_added}")
    print(f"  Untouched:            {untouched}")


if __name__ == "__main__":
    main()
