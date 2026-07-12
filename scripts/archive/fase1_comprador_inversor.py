"""
FASE 1 — Re-orientacion comprador+inversor para 587 fichas rentabilidad-*.html

Cambios por ficha (sin inventar datos nuevos):
 (A) hero-desc                  -> mensaje compra+inversion
 (B) banner-sub                 -> 'Comprar o invertir'
 (C) 4o caso de uso             -> 'Comprador para vivir' con datos de la ciudad
 (D) 2 nuevas FAQ comprador     -> momento + ahorro necesario
 (E) Selector visual de modo    -> tabs 'Quiero vivir aqui' / 'Quiero invertir'

Sin ocultar nada. Solo reorganizar y reencuadrar.
"""

from __future__ import annotations
import re
import sys
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FICHAS_DIR = ROOT / "rendata_beta"

# ---------- Extraction helpers ---------------------------------------------

RE_CITY        = re.compile(r'<div class="banner-title">([^<]+)</div>')
RE_PRECIO_TIPO = re.compile(r'id="hi-precio"\s+type="number"\s+value="(\d+)"')
RE_ITP_PCT     = re.compile(r'<div class="itp-val">(\d+(?:[.,]\d+)?)<span class="itp-pct">')
RE_ITP_CCAA    = re.compile(r'<div class="sl">(ITP|IPSI|IGIC) al comprar en ([^<]+)</div>')
RE_HERO_DESC   = re.compile(
    r'<p class="hero-desc">Análisis completo para inversores[^<]*</p>'
)
RE_BANNER_SUB_AID = re.compile(
    r'(<div class="banner-sub">[^<]*?)· Análisis de inversión inmobiliaria ·([^<]*?</div>)'
)
RE_HERO_END_TO_MAIN = re.compile(
    r'(</div>\s*\n</div>\s*\n\s*<div class="bc">)'
)
# Caso de uso anchor: closing of casos-grid + warning block
RE_CASOS_GRID_CLOSE = re.compile(
    r'(</div>)(</div>\s*\n\s*<div style="margin-top:\.85rem;[^"]*">\s*\n\s*⚠️ Estimaciones)'
)
# FAQ anchor: closing of faq-section + disc
RE_FAQ_SECTION_CLOSE = re.compile(
    r'(</div>)(</div>\s*\n\s*</div>\s*\n\s*\n\s*<div class="disc">)'
)


def euro(n: float) -> str:
    """Format integer euros with Spanish thousand-separators (5.960)."""
    return f"{int(round(n)):,}".replace(",", ".")


def cuota_hipoteca(precio: float, ltv: float = 0.80,
                   tipo: float = 0.032, plazo_anios: int = 25) -> float:
    capital = precio * ltv
    r = tipo / 12.0
    n = plazo_anios * 12
    return capital * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


# ---------- Snippet builders -----------------------------------------------

def build_caso_comprador(city: str, precio: int, ccaa: str,
                         itp_pct: str, tax_label: str = "ITP") -> str:
    entrada = precio * 0.20
    gastos = precio * 0.08
    ahorro = entrada + gastos
    cuota = cuota_hipoteca(precio)
    coste_intereses = cuota * 25 * 12 - precio * 0.80
    return (
        '<div class="caso-card">\n'
        '  <div class="caso-header">\n'
        '    <div class="caso-emoji">🏠</div>\n'
        '    <div>\n'
        '      <div class="caso-label">Comprador para vivir</div>\n'
        f'      <div class="caso-budget">{euro(precio)}€ · piso tipo en {city}</div>\n'
        '    </div>\n'
        '    <span class="caso-badge viable">Vivienda habitual</span>\n'
        '  </div>\n'
        '  <div class="caso-body">\n'
        f'    <div class="caso-row"><span class="caso-rl">Precio piso típico</span><span class="caso-rv">{euro(precio)}€</span></div>\n'
        f'    <div class="caso-row"><span class="caso-rl">Entrada mínima (20%)</span><span class="caso-rv" style="color:var(--blue)">{euro(entrada)}€</span></div>\n'
        f'    <div class="caso-row"><span class="caso-rl">Gastos compra (~8%)</span><span class="caso-rv" style="color:var(--red)">-{euro(gastos)}€</span></div>\n'
        f'    <div class="caso-row"><span class="caso-rl">Ahorro total necesario</span><span class="caso-rv" style="color:var(--green)">{euro(ahorro)}€</span></div>\n'
        f'    <div class="caso-row"><span class="caso-rl">{tax_label} {ccaa}</span><span class="caso-rv">{itp_pct}%</span></div>\n'
        '  </div>\n'
        '  <div class="caso-footer">\n'
        '    <div class="caso-roi-wrap">\n'
        f'      <div class="caso-roi-val" style="color:var(--blue)">{euro(cuota)}€</div>\n'
        '      <div class="caso-roi-label">Cuota/mes · 25 años · 3,2%</div>\n'
        '    </div>\n'
        '    <div class="caso-roi-wrap">\n'
        f'      <div class="caso-roi-val">{euro(coste_intereses)}€</div>\n'
        '      <div class="caso-roi-label">Intereses totales</div>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'
    )


def build_faq_extra(city: str, precio: int) -> str:
    entrada = precio * 0.20
    gastos = precio * 0.08
    ahorro = entrada + gastos
    cuota = cuota_hipoteca(precio)
    q8 = (
        '<div class="faq-item" onclick="toggleFaq(8)">\n'
        '  <div class="faq-q" id="fq-8">\n'
        f'    <span>¿Es buen momento para comprar piso en {city} si quiero vivir en él?</span>\n'
        '    <svg class="faq-arrow" id="fa-8" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
        '  </div>\n'
        f'  <div class="faq-a" id="fa-body-8">Para un comprador de vivienda habitual en {city}, las condiciones favorables son tres: pre-aprobación bancaria de la hipoteca, ahorro suficiente para entrada + gastos (~28% del precio del piso) y horizonte de permanencia mínimo de 5-7 años para amortizar los gastos de compra. Revisa la evolución del precio del m², los días en mercado y la guía de compra paso a paso más arriba — los datos de {city} en esta página te ayudarán a decidir si esperar o comprar ahora.</div>\n'
        '</div>'
    )
    q9 = (
        '<div class="faq-item" onclick="toggleFaq(9)">\n'
        '  <div class="faq-q" id="fq-9">\n'
        f'    <span>¿Cuánto necesito ahorrar para comprar un piso en {city}?</span>\n'
        '    <svg class="faq-arrow" id="fa-9" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>\n'
        '  </div>\n'
        f'  <div class="faq-a" id="fa-body-9">Para un piso típico en {city} (~{euro(precio)}€) necesitas aproximadamente: <strong>entrada del 20% ({euro(entrada)}€)</strong> + <strong>gastos de compra ~8% ({euro(gastos)}€)</strong> → un ahorro total cercano a <strong>{euro(ahorro)}€</strong>. La hipoteca al 80% del precio a 25 años y 3,2% TAE quedaría en torno a <strong>{euro(cuota)}€/mes</strong>. Usa la calculadora de hipoteca de esta misma página para ajustar entrada, plazo y tipo a tu caso concreto.</div>\n'
        '</div>'
    )
    return q8 + q9


def build_mode_tabs() -> str:
    """Selector visual. No oculta nada — destaca y desplaza la vista."""
    return (
        '\n<!-- MODE SELECTOR comprador/inversor -->\n'
        '<div class="mode-selector-wrap">\n'
        '  <div class="mode-selector">\n'
        '    <span class="mode-selector-label">¿Para qué buscas datos?</span>\n'
        '    <div class="mode-tabs">\n'
        '      <button class="mode-tab active" data-mode="comprador" onclick="setMode(\'comprador\',this)">🏠 Quiero vivir aquí</button>\n'
        '      <button class="mode-tab" data-mode="inversor" onclick="setMode(\'inversor\',this)">📈 Quiero invertir</button>\n'
        '    </div>\n'
        '  </div>\n'
        '  <p class="mode-selector-hint">Toda la información sigue visible — selecciona tu perfil para ir directo a lo que más te interesa.</p>\n'
        '</div>\n'
        '<style>\n'
        '.mode-selector-wrap{max-width:1200px;margin:1rem auto 0;padding:0 1.5rem}\n'
        '.mode-selector{background:#fff;border:1px solid var(--border,#e2e8f0);border-radius:14px;padding:.85rem 1.15rem;display:flex;align-items:center;gap:1.1rem;flex-wrap:wrap;box-shadow:0 1px 3px rgba(0,0,0,.04)}\n'
        '.mode-selector-label{font-size:.72rem;font-weight:700;color:var(--text,#0f172a);text-transform:uppercase;letter-spacing:.07em}\n'
        '.mode-tabs{display:flex;gap:.45rem;flex-wrap:wrap}\n'
        '.mode-tab{padding:.5rem 1rem;border:1px solid var(--border,#e2e8f0);border-radius:99px;background:#f8fafc;font-size:.82rem;font-weight:600;cursor:pointer;transition:all .18s ease;color:var(--text2,#475569);font-family:inherit}\n'
        '.mode-tab:hover{border-color:var(--blue,#1a56db);color:var(--blue,#1a56db)}\n'
        '.mode-tab.active{background:var(--blue,#1a56db);color:#fff;border-color:var(--blue,#1a56db);box-shadow:0 2px 6px rgba(26,86,219,.25)}\n'
        '.mode-selector-hint{max-width:1200px;margin:.55rem auto 1.25rem;padding:0 1.5rem;font-size:.7rem;color:var(--muted,#64748b);text-align:center}\n'
        '@media(max-width:560px){.mode-selector{flex-direction:column;align-items:flex-start;gap:.7rem}.mode-tab{flex:1 1 auto;text-align:center}}\n'
        '</style>\n'
        '<script>\n'
        'function setMode(mode,btn){\n'
        '  document.querySelectorAll(".mode-tab").forEach(function(b){b.classList.remove("active")});\n'
        '  btn.classList.add("active");\n'
        '  var targetId = mode==="comprador" ? "calculadoras" : "zonas";\n'
        '  var t = document.getElementById(targetId);\n'
        '  if(t){var y = t.getBoundingClientRect().top + window.scrollY - 80; window.scrollTo({top:y,behavior:"smooth"});}\n'
        '}\n'
        '</script>\n'
    )


# ---------- Per-file transform ---------------------------------------------

def transform(html: str, slug: str) -> tuple[str, dict]:
    info = {"slug": slug, "ok": False}

    m_city = RE_CITY.search(html)
    m_pre  = RE_PRECIO_TIPO.search(html)
    m_itp  = RE_ITP_PCT.search(html)
    m_ccaa = RE_ITP_CCAA.search(html)

    if not (m_city and m_pre and m_itp and m_ccaa):
        info["error"] = (
            f"missing city={bool(m_city)} precio={bool(m_pre)} "
            f"itp={bool(m_itp)} ccaa={bool(m_ccaa)}"
        )
        return html, info

    city      = m_city.group(1).strip()
    precio    = int(m_pre.group(1))
    # Preserve original tax % as written (handles "0,5" and "10")
    itp_pct   = m_itp.group(1)
    tax_label = m_ccaa.group(1)
    ccaa      = m_ccaa.group(2).strip()
    info.update(city=city, precio=precio, itp=itp_pct, ccaa=ccaa, tax=tax_label)

    out = html

    # (A) hero-desc
    new_hero = (
        f'<p class="hero-desc">Datos completos para comprar o invertir en {city}: '
        'precio del m², rentabilidad por barrio, gastos de compra, hipoteca y mercado por zonas.</p>'
    )
    new_out, n_hero = RE_HERO_DESC.subn(new_hero, out, count=1)
    if n_hero == 1:
        out = new_out
    info["hero_desc"] = n_hero

    # (B) banner-sub
    new_out, n_sub = RE_BANNER_SUB_AID.subn(r"\1· Comprar o invertir ·\2", out, count=1)
    if n_sub == 1:
        out = new_out
    info["banner_sub"] = n_sub

    # (C) 4o caso de uso
    caso = build_caso_comprador(city, precio, ccaa, itp_pct, tax_label)
    new_out, n_caso = RE_CASOS_GRID_CLOSE.subn(
        lambda mm: mm.group(1) + caso + mm.group(2), out, count=1
    )
    if n_caso == 1:
        out = new_out
    info["caso_uso"] = n_caso

    # (D) 2 FAQ extra
    faqs = build_faq_extra(city, precio)
    new_out, n_faq = RE_FAQ_SECTION_CLOSE.subn(
        lambda mm: mm.group(1) + faqs + mm.group(2), out, count=1
    )
    if n_faq == 1:
        out = new_out
    info["faq"] = n_faq

    # (E) Mode tabs — insertar antes de <div class="main">
    if 'class="mode-selector-wrap"' not in out:
        tabs = build_mode_tabs()
        new_out, n_tabs = re.subn(
            r'(<div class="main">)',
            tabs + r'\1', out, count=1
        )
        if n_tabs == 1:
            out = new_out
        info["mode_tabs"] = n_tabs
    else:
        info["mode_tabs"] = "already-present"

    info["ok"] = all([
        info.get("hero_desc") == 1,
        info.get("banner_sub") == 1,
        info.get("caso_uso") == 1,
        info.get("faq") == 1,
        info.get("mode_tabs") in (1, "already-present"),
    ])
    return out, info


# ---------- Driver ---------------------------------------------------------

def main(argv: list[str]) -> int:
    only = set(argv[1:])  # optional slugs to restrict to

    files = sorted(FICHAS_DIR.glob("rentabilidad-*.html"))
    if not files:
        print("No fichas found", file=sys.stderr)
        return 1

    if only:
        files = [f for f in files if f.stem in only or f.name in only]

    ok = 0
    skipped = []
    fail = []
    for path in files:
        slug = path.stem
        try:
            html = path.read_text(encoding="utf-8")
            # Skip articles/non-ficha files that match the glob accidentally
            if 'class="banner-title"' not in html or 'id="hi-precio"' not in html:
                skipped.append(slug)
                continue
            new, info = transform(html, slug)
            if info["ok"] and new != html:
                path.write_text(new, encoding="utf-8")
                ok += 1
            elif not info["ok"]:
                fail.append(info)
        except Exception as e:  # noqa
            fail.append({"slug": slug, "error": repr(e)})

    print(f"Processed: {ok}/{len(files)} fichas OK")
    if skipped:
        print(f"Skipped (no ficha template): {len(skipped)} — {', '.join(skipped[:5])}{'…' if len(skipped) > 5 else ''}")
    if fail:
        print(f"FAILURES ({len(fail)}):")
        for f in fail[:20]:
            print("  ", f)
        if len(fail) > 20:
            print(f"  ... and {len(fail) - 20} more")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
