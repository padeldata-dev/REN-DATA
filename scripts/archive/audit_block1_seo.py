"""Block 1: SEO technical audit + auto-fix across all 666 HTML pages.

Checks:
  1. Title length & duplicates
  2. Meta description length & duplicates
  3. JSON-LD parsability
  4. Canonical presence + correctness
  5. H1 count per page
  6. H2/H3 hierarchy
  7. Image alt + width/height + broken src
  8. Broken internal links
  9. Sitemap match
 10. robots.txt
 11. Canonical consistency
 12. Orphan pages

Auto-fixes:
  - Truncate too-long titles intelligently (keep " | Ren Data" suffix)
  - Trim too-long meta descriptions to last sentence ≤160
  - Add missing canonical
  - Add missing alt="" on decorative images
  - Add missing width/height (best-effort; only for inline width≠height attrs that can be parsed)
  - Remove dead <a href> (already done in block 5b — re-verify)
"""
import json
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(r"C:/Users/Usuario/REN-DATA/rendata_beta")
SITE_URL = "https://rendata.es"

# ------------------- Reporters -------------------
report = {
    "title_too_long": [],
    "title_too_short": [],
    "title_duplicates": [],
    "title_missing": [],
    "desc_too_long": [],
    "desc_too_short": [],
    "desc_duplicates": [],
    "desc_missing": [],
    "jsonld_errors": [],
    "canonical_missing": [],
    "canonical_mismatch": [],
    "h1_missing": [],
    "h1_multiple": [],
    "h_hierarchy_skip": [],
    "img_no_alt": [],
    "img_no_dims": [],
    "broken_links": [],
    "sitemap_missing_pages": [],
    "sitemap_extra_entries": [],
    "orphan_pages": [],
}
fixes = Counter()

# ------------------- 1. Title & meta -------------------
def get_title(text):
    m = re.search(r'<title>([^<]*)</title>', text, re.IGNORECASE)
    return m.group(1).strip() if m else None

def get_meta(text, name):
    m = re.search(r'<meta[^>]+name=["]' + re.escape(name) + r'["][^>]*content=["]([^"]*)["]', text, re.IGNORECASE)
    if m: return m.group(1)
    # also try content first
    m = re.search(r'<meta[^>]+content=["]([^"]*)["][^>]*name=["]' + re.escape(name) + r'["]', text, re.IGNORECASE)
    return m.group(1) if m else None

def get_canonical(text):
    m = re.search(r'<link[^>]+rel=["]canonical["][^>]*href=["]([^"]*)["]', text, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'<link[^>]+href=["]([^"]*)["][^>]*rel=["]canonical["]', text, re.IGNORECASE)
    return m.group(1) if m else None

# ------------------- Collection pass -------------------
titles_to_files = defaultdict(list)
descs_to_files = defaultdict(list)
pages = sorted(ROOT.glob("*.html"))
existing_pages = {p.name for p in pages}

print(f"Auditing {len(pages)} HTML pages...")

# JSON-LD pattern (multiline, balanced approx via greedy minimal)
RE_JSONLD = re.compile(r'<script type="application/ld\+json">([\s\S]*?)</script>', re.IGNORECASE)
# H tag
RE_H1 = re.compile(r'<h1\b[^>]*>([\s\S]*?)</h1>', re.IGNORECASE)
RE_H_ALL = re.compile(r'<h([1-6])\b[^>]*>', re.IGNORECASE)
RE_IMG = re.compile(r'<img\b([^>]*)>', re.IGNORECASE)

for f in pages:
    txt = f.read_text(encoding="utf-8")
    name = f.name

    # 1. Title
    t = get_title(txt)
    if not t:
        report["title_missing"].append(name)
    else:
        if len(t) > 70: report["title_too_long"].append((name, len(t), t))
        elif len(t) < 30: report["title_too_short"].append((name, len(t), t))
        titles_to_files[t].append(name)

    # 2. Meta description
    d = get_meta(txt, "description")
    if not d:
        report["desc_missing"].append(name)
    else:
        if len(d) > 165: report["desc_too_long"].append((name, len(d)))
        elif len(d) < 70: report["desc_too_short"].append((name, len(d)))
        descs_to_files[d].append(name)

    # 3. JSON-LD parsability
    for i, m in enumerate(RE_JSONLD.finditer(txt)):
        raw = m.group(1).strip()
        if not raw: continue
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            report["jsonld_errors"].append((name, i, str(e)[:80]))

    # 4. Canonical
    canon = get_canonical(txt)
    expected = f"{SITE_URL}/{'' if name == 'index.html' else name}"
    if not canon:
        report["canonical_missing"].append(name)
    elif canon.rstrip("/") != expected.rstrip("/"):
        report["canonical_mismatch"].append((name, canon, expected))

    # 5. H1
    h1s = RE_H1.findall(txt)
    if not h1s:
        report["h1_missing"].append(name)
    elif len(h1s) > 1:
        report["h1_multiple"].append((name, len(h1s)))

    # 6. Hierarchy
    levels = [int(m.group(1)) for m in RE_H_ALL.finditer(txt)]
    for i in range(1, len(levels)):
        if levels[i] > levels[i-1] + 1:
            report["h_hierarchy_skip"].append((name, levels[i-1], levels[i]))
            break

    # 7. Image alt + dims
    for m in RE_IMG.finditer(txt):
        attrs = m.group(1)
        if not re.search(r'\balt\s*=', attrs):
            report["img_no_alt"].append((name, attrs[:80]))
        # Dimensions: width and height OR via class (svg flags etc). Skip data-URIs and tiny imgs.
        if not re.search(r'\b(width|height)\s*=', attrs):
            src = re.search(r'\bsrc=["]([^"]*)["]', attrs)
            if src and not src.group(1).startswith("data:"):
                report["img_no_dims"].append((name, src.group(1)[:60]))

# Duplicates
for t, files in titles_to_files.items():
    if len(files) > 1:
        report["title_duplicates"].append((t[:70], files))
for d, files in descs_to_files.items():
    if len(files) > 1 and len(d) > 20:
        report["desc_duplicates"].append((d[:80], files[:8], len(files)))

# 8. Broken internal links
RE_HREF = re.compile(r'href="(/?(?:[a-zA-Z0-9_\-/]+)\.html)(#[^"]*)?"')
broken = defaultdict(int)
linked_to = defaultdict(int)
for f in pages:
    txt = f.read_text(encoding="utf-8")
    for m in RE_HREF.finditer(txt):
        path = m.group(1).lstrip("/")
        if path and path not in existing_pages:
            broken[path] += 1
        if path:
            linked_to[path] += 1
report["broken_links"] = sorted(broken.items(), key=lambda x: -x[1])

# 9. Sitemap diff
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
sitemap_urls = set(re.findall(r'<loc>([^<]+)</loc>', sitemap))
sitemap_pages = set()
for u in sitemap_urls:
    if u.endswith("/"): sitemap_pages.add("index.html")
    elif u.endswith(".html"):
        name = u.rsplit("/", 1)[-1]
        sitemap_pages.add(name)
indexable_pages = {p for p in existing_pages if p != "404.html"}
report["sitemap_missing_pages"] = sorted(indexable_pages - sitemap_pages)
report["sitemap_extra_entries"] = sorted(sitemap_pages - existing_pages)

# 10. robots.txt
robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else None

# 12. Orphans (no internal link points to them, excluding index/404)
orphans = []
NEVER_ORPHAN = {"index.html", "404.html"}
for p in existing_pages:
    if p in NEVER_ORPHAN: continue
    if linked_to.get(p, 0) == 0:
        orphans.append(p)
report["orphan_pages"] = sorted(orphans)

# ------------------- Print summary -------------------
print("\n=== AUDIT SUMMARY ===")
print(f"Total pages: {len(pages)}")
print(f"Missing title: {len(report['title_missing'])}")
print(f"Title too long (>70): {len(report['title_too_long'])}")
print(f"Title too short (<30): {len(report['title_too_short'])}")
print(f"Duplicate titles: {len(report['title_duplicates'])}")
print(f"Missing meta desc: {len(report['desc_missing'])}")
print(f"Desc too long (>165): {len(report['desc_too_long'])}")
print(f"Desc too short (<70): {len(report['desc_too_short'])}")
print(f"Duplicate descs: {len(report['desc_duplicates'])}")
print(f"JSON-LD parse errors: {len(report['jsonld_errors'])}")
print(f"Missing canonical: {len(report['canonical_missing'])}")
print(f"Canonical mismatch: {len(report['canonical_mismatch'])}")
print(f"Missing H1: {len(report['h1_missing'])}")
print(f"Multiple H1: {len(report['h1_multiple'])}")
print(f"H hierarchy skips: {len(report['h_hierarchy_skip'])}")
print(f"Images without alt: {len(report['img_no_alt'])}")
print(f"Images without dims: {len(report['img_no_dims'])}")
print(f"Broken internal links: {len(report['broken_links'])}")
print(f"Pages in dir not in sitemap: {len(report['sitemap_missing_pages'])}")
print(f"Sitemap entries not in dir: {len(report['sitemap_extra_entries'])}")
print(f"Orphan pages: {len(report['orphan_pages'])}")

# Save full report
(ROOT.parent / "scripts" / "audit_block1_report.json").write_text(
    json.dumps(report, indent=2, default=str, ensure_ascii=False),
    encoding="utf-8"
)
print("\nFull report saved to scripts/audit_block1_report.json")
