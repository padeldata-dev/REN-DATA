"""Mass-fix script for rendata_beta/rentabilidad-*.html
Applies 7 fixes uniformly across all 329 files. Idempotent: re-running has no extra effect.
"""
import re
import glob
import os
import sys
from collections import Counter

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rendata_beta')
FILES = sorted(glob.glob(os.path.join(DIR, 'rentabilidad-*.html')))

# Per-file counters
stats = Counter()


def fix_og_description(text):
    """Fix 1: remove the trailing >> in og:description meta tag."""
    new, n = re.subn(
        r'(<meta property="og:description"[^>]*content="[^"]*")>>',
        r'\1>',
        text
    )
    if n:
        stats['og_description'] += 1
    return new


def fix_mes_typo(text):
    """Fix 2: '/mes*€/mes' -> '€/mes' (e.g. '1.417/mes*€/mes' -> '1.417€/mes')."""
    new, n = re.subn(r'/mes\*€/mes', r'€/mes', text)
    if n:
        stats['mes_typo'] += 1
    return new


def fix_remove_relacionadas(text):
    """Fix 3: drop the entire 'Ciudades relacionadas' section.
    Anchors: from '<!-- CIUDADES RELACIONADAS -->' up to '<div class="disc"><strong>Aviso legal'.
    """
    pattern = re.compile(
        r'\s*<!-- CIUDADES RELACIONADAS -->.*?(?=\s*<div class="disc"><strong>Aviso legal)',
        re.DOTALL
    )
    new, n = pattern.subn('\n  ', text)
    if n:
        stats['relacionadas_removed'] += 1
    return new


def extract_hero(text):
    """Pull authoritative values from the hero block."""
    roi = re.search(
        r'<div class="sl">Rentabilidad bruta estimada</div><div class="sv">([\d,]+%)</div>',
        text
    )
    precio = re.search(
        r'<div class="sl">Precio m²</div><div class="sv"[^>]*>(\d[\d.,]*€)</div>',
        text
    )
    return (
        roi.group(1) if roi else None,
        precio.group(1) if precio else None,
    )


def fix_sync_editorial(text):
    """Fix 4 & 5: overwrite editorial highlight + paragraph mentions with hero values."""
    hero_roi, hero_precio = extract_hero(text)
    if not hero_roi or not hero_precio:
        return text

    changed = False

    # ed-stat: rentabilidad bruta
    new, n = re.subn(
        r'(<div class="ed-stat-val">)[\d,]+%(</div><div class="ed-stat-lbl">rentabilidad bruta</div>)',
        rf'\g<1>{hero_roi}\g<2>',
        text
    )
    if n:
        text = new
        changed = True

    # ed-stat: precio medio m²
    new, n = re.subn(
        r'(<div class="ed-stat-val">)\d[\d.,]*€(</div><div class="ed-stat-lbl">precio medio m²</div>)',
        rf'\g<1>{hero_precio}\g<2>',
        text
    )
    if n:
        text = new
        changed = True

    # paragraph: <strong>X€/m²</strong>
    new, n = re.subn(
        r'<strong>\d[\d.,]*€/m²</strong>',
        f'<strong>{hero_precio}/m²</strong>',
        text
    )
    if n:
        text = new
        changed = True

    # paragraph: rentabilidad bruta del <strong>X%</strong>
    new, n = re.subn(
        r'(rentabilidad bruta del\s*)<strong>[\d,]+%</strong>',
        rf'\g<1><strong>{hero_roi}</strong>',
        text
    )
    if n:
        text = new
        changed = True

    if changed:
        stats['editorial_synced'] += 1
    return text


def fix_dedupe_zones(text):
    """Fix 6: dedupe entries in the JS const zones=[...] array by 'nombre' field."""
    m = re.search(r'(const zones=\[)(.*?)(\];)', text, re.DOTALL)
    if not m:
        return text

    body = m.group(2)
    entries = re.findall(r'\{[^}]+\}', body)
    if not entries:
        return text

    seen = set()
    unique = []
    for entry in entries:
        nm = re.search(r'nombre:"([^"]+)"', entry)
        if not nm:
            unique.append(entry)
            continue
        key = nm.group(1)
        if key in seen:
            continue
        seen.add(key)
        unique.append(entry)

    if len(unique) == len(entries):
        return text  # nothing to dedupe

    new_block = m.group(1) + '\n  ' + ',\n  '.join(unique) + '\n' + m.group(3)
    text = text[:m.start()] + new_block + text[m.end():]
    stats['zones_deduped'] += 1
    return text


def fix_remove_population(text):
    """Fix 7: remove the Habitantes demo-card if value is implausibly low (<5000)."""
    pattern = re.compile(
        r'\s*<div class="demo-card">\s*'
        r'<div class="demo-icon">👥</div>\s*'
        r'<div class="demo-val">([\d.,]+)</div>\s*'
        r'<div class="demo-label">Habitantes</div>\s*'
        r'<div class="demo-trend"[^>]*>[^<]*</div>\s*'
        r'</div>',
        re.DOTALL
    )
    m = pattern.search(text)
    if not m:
        return text

    raw = m.group(1).replace('.', '').replace(',', '')
    if not raw.isdigit():
        return text
    if int(raw) >= 5000:
        return text

    text = text[:m.start()] + text[m.end():]
    stats['population_removed'] += 1
    return text


def process(path):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    text = original
    text = fix_og_description(text)
    text = fix_mes_typo(text)
    text = fix_remove_relacionadas(text)
    text = fix_sync_editorial(text)
    text = fix_dedupe_zones(text)
    text = fix_remove_population(text)

    if text != original:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        return True
    return False


def main():
    if not FILES:
        print(f"No files matched in {DIR}")
        sys.exit(1)
    print(f"Processing {len(FILES)} files in {DIR}")
    changed_count = 0
    for path in FILES:
        if process(path):
            changed_count += 1
    print(f"\nFiles modified: {changed_count}/{len(FILES)}")
    print("Per-fix counters:")
    for k in [
        'og_description', 'mes_typo', 'relacionadas_removed',
        'editorial_synced', 'zones_deduped', 'population_removed',
    ]:
        print(f"  {k:25s} {stats[k]}")


if __name__ == '__main__':
    main()
