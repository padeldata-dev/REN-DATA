#!/usr/bin/env python3
"""Inyecta Google Analytics (gtag.js) en todos los HTML de rendata_beta/."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "rendata_beta"

GTAG_SNIPPET = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0M57323B51"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-0M57323B51');
</script>'''

MARKER = "G-0M57323B51"
HEAD_END_RE = re.compile(r"</head>", re.IGNORECASE)


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False  # ya inyectado, idempotente
    if not HEAD_END_RE.search(text):
        print(f"WARN: no </head> in {path.name}", file=sys.stderr)
        return False
    new_text = HEAD_END_RE.sub(f"{GTAG_SNIPPET}\n</head>", text, count=1)
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    files = sorted(ROOT.glob("*.html"))
    changed = 0
    for p in files:
        if process(p):
            changed += 1
    print(f"Injected gtag in {changed}/{len(files)} files")


if __name__ == "__main__":
    main()
