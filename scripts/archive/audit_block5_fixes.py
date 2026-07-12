"""Block 5: high-impact fixes detected by previous audits.

Main remaining issue: H hierarchy skips (h2 → h4 without h3) in 11 pages.
Fix: rewrite the offending h4 to h3 within the affected sections.
"""
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

H_SKIP_FILES = [
    "analisis.html",
    "barrios-baratos-madrid-barcelona-2026.html",
    "ciudades-interior-vs-costa-rentabilidad-2026.html",
    "comprar-piso-joven-espana-2026.html",
    "comprar-piso-primera-vez-espana-2026.html",
    "cuando-es-buen-momento-comprar-piso-2026.html",
    "cuanto-ahorrar-comprar-piso-espana-2026.html",
    "gastos-comprar-piso-por-comunidad-2026.html",
    "hipoteca-fija-vs-variable-2026.html",
    "metodologia.html",
    "rentabilidad-madrid-vs-barcelona-2026.html",
]

RE_H = re.compile(r'<h([1-6])\b([^>]*)>')

def fix_hierarchy(text):
    """Walk header sequence; if a header jumps >+1 level, downgrade it to prev+1."""
    matches = list(RE_H.finditer(text))
    if not matches: return text, 0
    out = []
    last = 0
    last_level = 0
    changes = 0
    for m in matches:
        out.append(text[last:m.start()])
        lvl = int(m.group(1))
        if last_level and lvl > last_level + 1:
            new_lvl = last_level + 1
            # Replace this tag and look ahead for its closing </hN>
            # But </hN> in source uses N matching the open tag; need to update both.
            close_pat = re.compile(r'</h' + str(lvl) + r'>', re.IGNORECASE)
            close_m = close_pat.search(text, m.end())
            if close_m:
                # Replace the close tag too — but only the FIRST occurrence in scope.
                # We do this in a second pass below.
                pass
            out.append(f'<h{new_lvl}{m.group(2)}>')
            changes += 1
            last_level = new_lvl
            # Track replacement for close tag (record level)
            # We'll handle close-tag rewrite by scanning the original text linearly.
        else:
            out.append(m.group(0))
            last_level = lvl
        last = m.end()
    out.append(text[last:])
    new = ''.join(out)
    if changes == 0:
        return new, 0
    # Second pass: any mismatched </hN> need to be closed correctly.
    # Since we changed <hX> to <h(X-1)>, the next </hX> must become </h(X-1)>.
    # We process pairs by walking from start using a simple stack — but for the
    # common case of jumps like h2→h4 with isolated h4 sections, we just rewrite
    # the FIRST </h4> after each rewritten <h4> open. We'll do this iteratively.
    # Actually simpler approach: re-do the whole rewrite tracking depth.
    matches2 = list(RE_H.finditer(text))
    # Build (start, end, old_level, new_level) for each header we want to remap.
    remaps = []
    last_level = 0
    for m in matches2:
        lvl = int(m.group(1))
        if last_level and lvl > last_level + 1:
            new_lvl = last_level + 1
            remaps.append((m.start(), m.end(), lvl, new_lvl))
            last_level = new_lvl
        else:
            last_level = lvl
    # For each remap, rewrite the open tag AND the next matching close tag.
    new_text = text
    offset = 0
    for start, end, old, new in remaps:
        # Open tag rewrite
        old_open = f'<h{old}'
        # Locate within current new_text using stored start (adjusted)
        s = start + offset
        new_text = new_text[:s] + new_text[s:].replace(f'<h{old}', f'<h{new}', 1)
        # Close tag: find next </hN> from position s onward
        close_idx = new_text.find(f'</h{old}>', s)
        if close_idx != -1:
            new_text = new_text[:close_idx] + f'</h{new}>' + new_text[close_idx+len(f'</h{old}>'):]
    return new_text, len(remaps)

fixed_count = 0
for name in H_SKIP_FILES:
    p = ROOT / name
    if not p.exists(): continue
    txt = p.read_text(encoding="utf-8")
    new, n = fix_hierarchy(txt)
    if n > 0 and new != txt:
        p.write_text(new, encoding="utf-8")
        fixed_count += 1
        print(f"   {name}: {n} headers re-leveled")

print(f"\nFixed hierarchy in {fixed_count} pages")
