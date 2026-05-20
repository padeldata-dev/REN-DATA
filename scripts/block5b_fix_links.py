"""Block 5b: unwrap broken internal links (replace dead <a href=...> with plain text)."""
import re
from pathlib import Path
from collections import Counter

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")

existing = {p.name for p in ROOT.glob("*.html")}

RE_HREF_HTML_ABS = re.compile(r'href="(/[a-zA-Z0-9_\-./]+\.html)"')
RE_HREF_HTML_REL = re.compile(r'href="([a-zA-Z0-9_\-]+\.html)"')

# Collect broken targets first
broken = set()
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    for m in RE_HREF_HTML_ABS.finditer(txt):
        p = m.group(1).lstrip("/")
        if p and p not in existing: broken.add(p)
    for m in RE_HREF_HTML_REL.finditer(txt):
        p = m.group(1)
        if p and p not in existing: broken.add(p)
print(f"Found {len(broken)} unique broken targets")

# For each broken target, unwrap <a ...href="...target...">TEXT</a> -> TEXT
# Build one regex per target (escape it)
modified_files = 0
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    orig = txt
    for target in broken:
        # absolute and relative variants
        for prefix in ("/", ""):
            full = prefix + target
            # match <a ...href="full"...>...</a>  (non-greedy, single anchor)
            pat = re.compile(
                r'<a\b[^>]*?href="' + re.escape(full) + r'"[^>]*?>([\s\S]*?)</a>',
                re.IGNORECASE
            )
            txt = pat.sub(lambda m: m.group(1), txt)
    if txt != orig:
        f.write_text(txt, encoding="utf-8")
        modified_files += 1
print(f"Unwrapped dead links in {modified_files} files")

# Re-verify
remaining = set()
for f in ROOT.glob("*.html"):
    txt = f.read_text(encoding="utf-8")
    for m in RE_HREF_HTML_ABS.finditer(txt):
        p = m.group(1).lstrip("/")
        if p and p not in existing: remaining.add(p)
    for m in RE_HREF_HTML_REL.finditer(txt):
        p = m.group(1)
        if p and p not in existing: remaining.add(p)

if remaining:
    print(f"[WARN] {len(remaining)} broken targets still present:")
    for t in sorted(remaining): print("   ", t)
else:
    print("[OK] 0 broken HTML links remain")
