#!/usr/bin/env python3
"""Build index.html and 404.html from data/projects.json, data/workshop.json and data/owner.json.

The page is static: every project, the coverage map and the workshop are in the HTML and readable without JavaScript.
app.js only adds search, filtering, sorting, the view and menu switches, the theme switch and motion.
Run: python3 tools/build.py  (then python3 tools/check_site.py)
"""
import datetime as dt
import hashlib
import html
import io
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://cyberdudeuk.github.io/'
REPO = 'https://github.com/cyberdudeuk/cyberdudeuk.github.io'
CONTACT = REPO + '/issues/new?template=contact.yml'
OLD_TOOLKIT_SECTIONS = ['start-here', 'knowledge', 'toolkit', 'tools', 'assurance', 'catalogue', 'ucd', 'practice', 'resources',
                        'signals', 'transparency', 'roadmap', 'glossary', 'contact', 'tool-triage', 'tool-evidence', 'tool-deia',
                        'tool-atrs', 'tool-pqc', 'tool-plain']
NEW_TOOLKIT = 'https://cyberdudeuk.github.io/ai-capability-governance/'
LEVELS = ('Beginner', 'Intermediate', 'Advanced')
e = html.escape

ICONS = {  # simple 24px line icons, drawn here so the page makes no third-party requests
    'shield': '<path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    'schema': '<rect x="3" y="3" width="7" height="5" rx="1"/><rect x="14" y="16" width="7" height="5" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/><path d="M6.5 8v8M6.5 12h11v4"/>',
    'database': '<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v14c0 1.7 3.1 3 7 3s7-1.3 7-3V5M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/>',
    'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/>',
    'hub': '<circle cx="12" cy="12" r="2.5"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M6.5 6.5l3.7 3.7M17.5 6.5l-3.7 3.7M6.5 17.5l3.7-3.7M17.5 17.5l-3.7-3.7"/>',
    'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M8 21h8"/>',
    'groups': '<circle cx="8" cy="8" r="3"/><circle cx="16.5" cy="9" r="2.5"/><path d="M2.5 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6M13.5 14.5c.9-.4 1.9-.5 3-.5 2.8 0 5 2.2 5 5"/>',
    'science': '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7 15h10"/>',
    'megaphone': '<path d="M3 11v2a1 1 0 0 0 1 1h3l7 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M17.5 9a4 4 0 0 1 0 6M7 14l1 5h3l-1-4"/>',
    'compass': '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    'person': '<circle cx="12" cy="8" r="3.5"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>',
    'award': '<circle cx="12" cy="9" r="5.5"/><path d="M8.5 13.5L7 21l5-2.5 5 2.5-1.5-7.5"/>',
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'out': '<path d="M7 17L17 7M9 7h8v8"/>',
    'code': '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/>',
    'star': '<path d="M12 3l2.6 5.6 6 .7-4.5 4.1 1.2 6L12 16.5 6.7 19.4l1.2-6L3.4 9.3l6-.7z"/>',
    'grid': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    'list': '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
    'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
}
KINDS = [('tool', 'Working tool'), ('proto', 'Prototype'), ('proposed', 'Proposed, not endorsed'), ('personal', 'Personal project'), ('exp', 'Experiment')]


def asset(name):
    """The file's address with a fingerprint of its contents, so a browser never pairs a new page with an old cached
    stylesheet or script (D-15). GitHub Pages lets browsers keep files for 10 minutes."""
    return f'{name}?v={hashlib.sha256((ROOT / name).read_bytes()).hexdigest()[:10]}'


def icon(name, size=20, label=None):
    a = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {a}>{ICONS[name]}</svg>')


def kind(status):
    """The status as each project states it, grouped into one of five kinds for colour and the status chart."""
    s = status.lower()
    for prefix, k in (('working', 'tool'), ('proposed', 'proposed'), ('personal', 'personal'), ('experiment', 'exp'), ('prototype', 'proto')):
        if s.startswith(prefix):
            return k
    raise ValueError(f'status "{status}" does not start with a known kind')


def qr_svg(url):
    import segno
    buf = io.BytesIO()
    q = segno.make(url, error='m')
    q.save(buf, kind='svg', scale=4, border=1, xmldecl=False, svgns=True, dark='#0b0c0c', light='#ffffff')
    w, h = q.symbol_size(scale=4, border=1)
    s = buf.getvalue().decode()
    return s.replace(f'width="{w}" height="{h}"', f'width="88" height="88" viewBox="0 0 {w} {h}" role="img" aria-label="QR code for {e(url)}"', 1)


def barcode_svg(text):
    import barcode
    from barcode.writer import SVGWriter
    buf = io.BytesIO()
    barcode.get('code128', text, writer=SVGWriter()).write(buf, options={'write_text': False, 'module_height': 12, 'quiet_zone': 2})
    s = buf.getvalue().decode()
    s = s[s.find('<svg'):]
    m = re.search(r'width="([\d.]+)mm" height="([\d.]+)mm"', s)
    return s.replace(m.group(0), f'width="168" height="48" viewBox="0 0 {m.group(1)} {m.group(2)}" preserveAspectRatio="none" role="img" aria-label="Barcode {e(text)}"', 1)


def constellation(cats, count, newc, total):
    """The hero illustration, drawn from the data: one node per area, sized by its number of projects;
    amber lines lead to areas with something new."""
    live = [c for c in cats if count[c]]
    cx, cy, r = 280, 230, 168
    lines, flows, nodes, links = [], [], [], []
    pts = []
    for i, c in enumerate(live):
        a = -math.pi / 2 + 2 * math.pi * i / len(live)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pts.append((x, y))
        lines.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')
        if newc[c]:
            flows.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')
        rad = 9 + 5 * (count[c] - 1)
        lx, ly = cx + (r + 26 + rad) * math.cos(a), cy + (r + 26 + rad) * math.sin(a)
        anchor = 'start' if math.cos(a) > .3 else ('end' if math.cos(a) < -.3 else 'middle')
        ly += 4 + (6 if math.sin(a) > .6 else (-2 if math.sin(a) < -.6 else 0))
        nodes.append(f'<g class="node c-{e(c)}" style="animation-delay:{i * .4:.1f}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" class="n"/>'
                     f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}">{e(cats[c]["short"])}</text></g>')
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        qx, qy = cx + (mx - cx) * 1.12, cy + (my - cy) * 1.12
        links.append(f'<path d="M{x1:.1f} {y1:.1f} Q{qx:.1f} {qy:.1f} {x2:.1f} {y2:.1f}"/>')
    return f'''<svg class="constellation" viewBox="0 0 560 460" aria-hidden="true" focusable="false">
<circle cx="{cx}" cy="{cy}" r="212" class="orbit"/><circle cx="{cx}" cy="{cy}" r="{r}" class="ring"/><circle cx="{cx}" cy="{cy}" r="100" class="orbit"/>
<g class="spokes">{"".join(lines)}</g><g class="links">{"".join(links)}</g><g class="flows">{"".join(flows)}</g>
{"".join(nodes)}
<circle cx="{cx}" cy="{cy}" r="66" class="halo"/><circle cx="{cx}" cy="{cy}" r="54" class="core"/>
<text x="{cx}" y="{cy + 4}" text-anchor="middle" class="core-n">{total}</text><text x="{cx}" y="{cy + 24}" text-anchor="middle" class="core-l">projects</text>
</svg>'''


def card(p, cats):
    c = cats[p['category']]
    k = kind(p['status'])
    lv = ''.join(f'<li class="lvl lvl-{x.lower()}">{e(x)}</li>' for x in p['levels'])
    new = '<span class="flag">New</span>' if p.get('new') else ''
    links = []
    if p.get('site'):
        links.append(f'<a class="btn btn-primary" href="{e(p["site"])}">Open the site{icon("out", 16)}<span class="visually-hidden">: {e(p["name"])}</span></a>')
    links.append(f'<a class="btn" href="{e(p["repo"])}">{icon("code", 16)}Repository<span class="visually-hidden">: {e(p["name"])}</span></a>')
    how = f'<p class="how">{e(p["how"])}</p>' if p.get('how') else ''
    upd = dt.date.fromisoformat(p['updated'])
    livedot = '<span class="dot live" aria-hidden="true"></span>' if p.get('site') else '<span class="dot" aria-hidden="true"></span>'
    return f'''<article class="card c-{e(p["category"])}" id="p-{e(p["id"])}" data-category="{e(p["category"])}" data-status="{e(p["status"])}" data-updated="{e(p["updated"])}" data-name="{e(p["name"])}" data-levels="{e(" ".join(x.lower() for x in p["levels"]))}" data-site="{"yes" if p.get("site") else "no"}">
  <div class="card-top"><span class="tile" aria-hidden="true">{icon(c["icon"], 22)}</span>{new}</div>
  <h3>{e(p["name"])}</h3>
  <p class="sum">{e(p["summary"])}</p>
  <dl class="facts"><div><dt>Status</dt><dd><span class="pill k-{k}">{livedot}{e(p["status"])}</span></dd></div><div><dt>For</dt><dd>{e(p["audience"])}</dd></div><div><dt>Updated</dt><dd><time datetime="{e(p["updated"])}">{upd.day} {upd:%B %Y}</time></dd></div><div><dt>Licence</dt><dd>{e(p["licence"])}</dd></div></dl>
  <ul class="levels" aria-label="Levels this project supports">{lv}</ul>
  {how}<div class="actions">{"".join(links)}</div>
</article>'''


def build():
    d = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))
    w = json.loads((ROOT / 'data' / 'workshop.json').read_text(encoding='utf-8'))
    owner = json.loads((ROOT / 'data' / 'owner.json').read_text(encoding='utf-8'))
    cats = {c['id']: c for c in d['categories']}
    projects = sorted(d['projects'], key=lambda p: p['updated'], reverse=True)
    count = {c: sum(1 for p in projects if p['category'] == c) for c in cats}
    newc = {c: any(p.get('new') for p in projects if p['category'] == c) for c in cats}
    live = sum(1 for p in projects if p.get('site'))
    areas = sum(1 for c in cats if count[c])
    items = w['items']
    upd = dt.date.fromisoformat(d['updated'])
    nlevel = {x: sum(1 for p in projects if x in p['levels']) for x in LEVELS}
    byid = {p['id']: p for p in projects}

    drawer = ''.join(
        f'<li><a href="#cat-{e(c)}" class="c-{e(c)}" data-filter-cat="{e(c)}"><span class="tile sm" aria-hidden="true">{icon(cats[c]["icon"], 16)}</span><span>{e(cats[c]["label"])}</span>'
        f'{"<span class=flag>New</span>" if newc[c] else ""}<span class="count" aria-label="{count[c]} projects">{count[c]}</span></a></li>'
        for c in cats if count[c])
    chips = (f'<button type="button" class="chip cchip" data-cat="all" aria-pressed="true">All areas <span class="ct">{len(projects)}</span></button>' + ''.join(
        f'<button type="button" class="chip cchip c-{e(c)}" data-cat="{e(c)}" aria-pressed="false">{icon(cats[c]["icon"], 16)}{e(cats[c]["label"])} <span class="ct">{count[c]}</span></button>'
        for c in cats if count[c]))
    lchips = (f'<button type="button" class="seg lchip" data-level="all" aria-pressed="true">Any level <span class="ct">{len(projects)}</span></button>' + ''.join(
        f'<button type="button" class="seg lchip" data-level="{x.lower()}" aria-pressed="false">{x} <span class="ct">{nlevel[x]}</span></button>' for x in LEVELS))
    sections = ''.join(
        f'<section class="cat-block c-{e(c)}{" span2" if count[c] > 1 else ""}" id="cat-{e(c)}" aria-labelledby="h-{e(c)}"><h3 class="cat-h" id="h-{e(c)}"><span class="tile" aria-hidden="true">{icon(cats[c]["icon"], 20)}</span>{e(cats[c]["label"])} <span class="count">{count[c]}</span></h3>'
        f'<div class="grid">{"".join(card(p, cats) for p in projects if p["category"] == c)}</div></section>'
        for c in cats if count[c])

    def pick(level):
        return ''.join(f'<li><a href="#p-{e(i)}">{e(byid[i]["name"])}</a></li>' for i in d['ways_in'][level])

    # Featured: the most recently updated new project that has a live site and highlights.
    feat = next((p for p in projects if p.get('new') and p.get('site') and p.get('highlights')), None)
    featured = ''
    if feat:
        fk = kind(feat['status'])
        hl = ''.join(f'<li class="hl hl-{i}">{icon(n, 24)}<span>{e(t)}</span></li>' for i, (t, n) in enumerate(zip(feat['highlights'], ('layers', 'schema', 'database', 'hub'))))
        featured = f'''<section class="featured c-{e(feat["category"])}" id="featured" aria-labelledby="h-featured">
   <div class="feat-body">
    <p class="feat-meta"><span class="flag">New</span><span class="pill k-{fk}"><span class="dot" aria-hidden="true"></span>{e(feat["status"])}</span><span class="muted">Updated {dt.date.fromisoformat(feat["updated"]).day} {dt.date.fromisoformat(feat["updated"]):%B %Y}</span></p>
    <p class="eyebrow">Featured · {e(cats[feat["category"]]["label"])}</p>
    <h2 id="h-featured">{e(feat["name"])}</h2>
    <p class="feat-sum">{e(feat["summary"])}</p>
    <p class="feat-for"><strong>For:</strong> {e(feat["audience"])}</p>
    <div class="actions"><a class="btn btn-primary" href="{e(feat["site"])}">Open the site{icon("out", 16)}<span class="visually-hidden">: {e(feat["name"])}</span></a><a class="btn" href="{e(feat["repo"])}">{icon("code", 16)}Repository<span class="visually-hidden">: {e(feat["name"])}</span></a></div>
   </div>
   <div class="feat-art"><p class="visually-hidden">What it includes:</p><ul class="hls">{hl}</ul></div>
  </section>'''

    # Coverage map: every area against every level, counted from the data. Each count links to its area.
    rows = []
    for c in cats:
        if not count[c]:
            continue
        cells = []
        for x in LEVELS:
            n = sum(1 for p in projects if p['category'] == c and x in p['levels'])
            lab = f'{cats[c]["label"]}, {x}: {n} {"project" if n == 1 else "projects"}'
            if n:
                cells.append(f'<td><a class="cell n{min(n, 2)}" href="#cat-{e(c)}" data-cell-cat="{e(c)}" data-cell-level="{x.lower()}" data-n="{n}" aria-label="{e(lab)}">{n}</a></td>')
            else:
                cells.append(f'<td><span class="cell n0" data-n="0" aria-label="{e(lab)}">–</span></td>')
        rows.append(f'<tr class="c-{e(c)}"><th scope="row"><span class="tile sm" aria-hidden="true">{icon(cats[c]["icon"], 15)}</span>{e(cats[c]["label"])}</th>{"".join(cells)}</tr>')
    kcount = {k: sum(1 for p in projects if kind(p['status']) == k) for k, _ in KINDS}
    bar = ''.join(f'<span class="seg-bar k-{k}" style="flex:{kcount[k]}" title="{e(l)}: {kcount[k]}"></span>' for k, l in KINDS if kcount[k])
    legend = ''.join(f'<li><span class="sw k-{k}" aria-hidden="true"></span><span>{e(l)}</span><strong data-kind="{k}">{kcount[k]}</strong></li>' for k, l in KINDS if kcount[k])
    bar_label = ', '.join(f'{kcount[k]} {l.lower()}' for k, l in KINDS if kcount[k])

    workshop = ''.join(
        f'<article class="wcard" id="w-{e(i["id"])}"><div class="card-top"><span class="tile" aria-hidden="true">{icon(i["icon"], 20)}</span><span class="cat">{e(i["area"])}</span></div>'
        f'<h3>{e(i["name"])}</h3><p>{e(i["summary"])}</p><span class="pill k-wip">{e(w["status"])}</span></article>'
        for i in items)

    jsonld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': f'{owner["display_name"]}: projects', 'url': SITE,
              'dateModified': d['updated'], 'inLanguage': 'en-GB',
              'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(projects), 'itemListElement': [
                  {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'CreativeWork', 'name': p['name'], 'url': p.get('site') or p['repo'],
                                                                    'codeRepository': p['repo'], 'abstract': p['summary'], 'genre': cats[p['category']]['label']}}
                  for i, p in enumerate(projects)]}}
    about_role = f'<p class="role">{e(owner["role"])}</p>' if owner.get('role') else ''
    navlinks = '<a href="#projects">Projects</a><a href="#ways-in">Ways in</a><a href="#coverage">Coverage</a><a href="#workshop">Workshop</a><a href="#about">About</a><a href="#contact">Contact</a>'
    favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23e9a23b'/%3E"
               "%3Cpath d='M10 11L22 11L16 22Z' fill='none' stroke='%230a1824' stroke-width='2'/%3E%3Ccircle cx='10' cy='11' r='3' fill='%230a1824'/%3E"
               "%3Ccircle cx='22' cy='11' r='3' fill='%230a1824'/%3E%3Ccircle cx='16' cy='22' r='3' fill='%230a1824'/%3E%3C/svg%3E")
    mark = ('<svg class="mark" width="40" height="40" viewBox="0 0 40 40" aria-hidden="true" focusable="false"><rect width="40" height="40" rx="11"/>'
            '<path d="M13 14L27 14L20 27Z"/><circle cx="13" cy="14" r="3.4"/><circle cx="27" cy="14" r="3.4"/><circle cx="20" cy="27" r="3.4"/></svg>')
    page = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(owner["display_name"])}: projects for better public services</title>
<meta name="description" content="Open tools, standards and guidance for data and AI in UK public services, plus personal public-good projects: every project by {e(owner["display_name"])} in one place.">
<meta name="version" content="{e(d["version"])}">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(owner["display_name"])}: projects for better public services"><meta property="og:url" content="{SITE}">
<meta property="og:description" content="Open tools, standards and guidance for data and AI in UK public services.">
<meta property="og:image" content="{SITE}og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{len(projects)} projects across {areas} areas of work, drawn as a constellation">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a1824">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{favicon}">
<link rel="preload" href="fonts/space-grotesk-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset("styles.css")}">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>/* Old links to the Public AI Utility Toolkit (which lived here until November 2026) go to its new address. */
(function(){{var h=(location.hash||'').slice(1);var old={json.dumps(OLD_TOOLKIT_SECTIONS)};if(old.indexOf(h)>-1){{location.replace('{NEW_TOOLKIT}#'+h);}}}})();
/* A theme chosen with the switch is applied before the page paints. Nothing is stored unless you use the switch. */
(function(){{try{{var t=localStorage.getItem('theme');if(t==='dark'||t==='light')document.documentElement.setAttribute('data-theme',t);}}catch(x){{}}}})();</script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="progress" aria-hidden="true"></div>
<header class="masthead">
 <div class="wrap mast">
  <a class="brand" href="#top">{mark}<span>{e(owner["display_name"])}<small>Projects for better public services</small></span></a>
  <nav class="global" aria-label="Sections">{navlinks}</nav>
  <details class="navmenu"><summary>{icon("menu", 20)}Menu</summary><nav aria-label="Sections (menu)">{navlinks}</nav></details>
  <button type="button" class="theme js-only" id="themeToggle" role="switch" aria-checked="false">{icon("moon", 18)}<span>Dark mode</span></button>
 </div>
</header>
<section class="hero" id="top" aria-labelledby="h-top">
 <div class="wrap hero-in">
  <div class="hero-text">
   <p class="eyebrow"><span class="dot live" aria-hidden="true"></span>Launchpad · updated <time datetime="{e(d["updated"])}">{upd.day} {upd:%B %Y}</time></p>
   <h1 id="h-top">Open tools and guidance for data and AI in public services</h1>
   <p class="lede">Every project I build, in one place: standards, playbooks, working tools and personal public-good projects. Each lives in its own repository with its own site, built in the open and checked before it is published.</p>
   <div class="actions"><a class="btn btn-amber" href="#projects">Browse all projects{icon("arrow", 18)}</a><a class="btn btn-ghost" href="#ways-in">Not sure where to start?</a></div>
   <div class="stats">
    <div class="s1"><span class="num" data-count="{len(projects)}">{len(projects)}</span><span class="lbl">public projects</span></div>
    <div class="s2"><span class="num" data-count="{live}">{live}</span><span class="lbl">with a live site</span></div>
    <div class="s3"><span class="num" data-count="{areas}">{areas}</span><span class="lbl">areas of work</span></div>
    <div class="s4"><span class="num" data-count="{len(items)}">{len(items)}</span><span class="lbl">in the workshop</span></div>
   </div>
  </div>
  <figure class="hero-art">{constellation(cats, count, newc, len(projects))}
   <figcaption>Each node is an area of work, sized by its number of projects. Amber lines lead to areas with something new. Drawn from the data.</figcaption></figure>
 </div>
 <div class="wrap"><p class="moved">Looking for the <strong>Public AI Utility Toolkit</strong>? It is now <a href="{NEW_TOOLKIT}">AI Capability Governance and Implementation</a>, with its own address.</p></div>
</section>
<div class="wrap layout">
 <aside class="side" aria-label="Projects by category">
  <button type="button" class="toggle js-only" id="drawerToggle" role="switch" aria-checked="true" aria-controls="drawer"><span class="track" aria-hidden="true"><span class="knob"></span></span><span>Category menu: <span id="drawerState">shown</span></span></button>
  <div class="drawer" id="drawer">
   <p class="drawer-h">Areas of work</p>
   <ul>{drawer}</ul>
  </div>
 </aside>
 <main id="main" tabindex="-1">
  {featured}

  <section id="ways-in" aria-labelledby="h-ways">
   <h2 id="h-ways">Choose your way in</h2>
   <p class="intro">Every project says which levels it supports. Start where you are; the suggestions are a good first stop.</p>
   <div class="grid three">
    <article class="way w-b"><div class="way-top"><span class="lvl lvl-beginner">Beginner</span><span class="big">{nlevel["Beginner"]}</span></div><h3>New to the subject, or to GitHub</h3><p>Plain-English sites you can use in a browser, with no account and nothing to install.</p><p class="small"><strong>Suggested starting points</strong></p><ul>{pick("Beginner")}</ul><p class="small"><button type="button" class="linkish js-only" data-level-go="beginner">Show all {nlevel["Beginner"]} projects at this level</button></p></article>
    <article class="way w-i"><div class="way-top"><span class="lvl lvl-intermediate">Intermediate</span><span class="big">{nlevel["Intermediate"]}</span></div><h3>Using it in your work</h3><p>Guidance, registers and tools for a team, an asset or a return.</p><p class="small"><strong>Suggested starting points</strong></p><ul>{pick("Intermediate")}</ul><p class="small"><button type="button" class="linkish js-only" data-level-go="intermediate">Show all {nlevel["Intermediate"]} projects at this level</button></p></article>
    <article class="way w-a"><div class="way-top"><span class="lvl lvl-advanced">Advanced</span><span class="big">{nlevel["Advanced"]}</span></div><h3>Building, assuring or reusing</h3><p>Open data, schemas, checks and code you can run, adapt or contribute to.</p><p class="small"><strong>Suggested starting points</strong></p><ul>{pick("Advanced")}</ul><p class="small"><button type="button" class="linkish js-only" data-level-go="advanced">Show all {nlevel["Advanced"]} projects at this level</button></p></article>
   </div>
  </section>

  <section id="projects" aria-labelledby="h-projects">
   <div class="sec-head"><h2 id="h-projects">Projects</h2><p class="intro">Search, filter and sort all {len(projects)} public projects.</p></div>
   <div class="controls js-only">
    <div class="row">
     <label class="search">{icon("search", 18)}<span class="visually-hidden">Search projects</span><input type="search" id="q" placeholder="Search projects" autocomplete="off"><kbd aria-hidden="true">/</kbd></label>
     <label class="sort">Sort by <select id="sort"><option value="updated">Most recently updated</option><option value="name">Name, A to Z</option></select></label>
    </div>
    <div role="group" aria-label="Filter by area" class="chips">{chips}</div>
    <div class="row">
     <div role="group" aria-label="Filter by level" class="segs">{lchips}</div>
     <button type="button" class="toggle" id="liveToggle" role="switch" aria-checked="false"><span class="track" aria-hidden="true"><span class="knob"></span></span><span>Live site only</span></button>
     <div role="group" aria-label="View" class="segs view"><button type="button" class="seg vbtn" data-view="cards" aria-pressed="true">{icon("grid", 16)}Cards</button><button type="button" class="seg vbtn" data-view="compact" aria-pressed="false">{icon("list", 16)}Compact</button></div>
    </div>
   </div>
   <p class="shown js-only" aria-live="polite" id="shown">Showing all {len(projects)} projects</p>
   <div class="blocks">{sections}</div>
   <div class="empty js-only" id="empty" hidden><p><strong>No projects match.</strong> Try fewer filters or another word.</p><button type="button" class="btn btn-primary" id="reset">Clear all filters</button></div>
   <p class="note">The list is open data: <a href="data/projects.json">projects.json</a>. A weekly check flags any new public repository that is not yet listed, so future projects appear here once a person has added them.</p>
  </section>

  <section id="coverage" aria-labelledby="h-coverage">
   <div class="sec-head"><h2 id="h-coverage">Coverage map</h2><p class="intro">Which areas have something for each level, and where the work stands. Select a number to see those projects.</p></div>
   <div class="cov">
    <div class="panel matrix-wrap"><table class="matrix"><caption>Projects by area and level</caption>
     <thead><tr><th scope="col">Area</th>{"".join(f'<th scope="col">{x}</th>' for x in LEVELS)}</tr></thead>
     <tbody>{"".join(rows)}</tbody></table></div>
    <div class="panel status"><h3>Where the work stands</h3>
     <div class="bar" role="img" aria-label="Status of the {len(projects)} projects: {e(bar_label)}">{bar}</div>
     <ul class="legend">{legend}</ul>
     <p class="small muted">Status as each project states it. Prototype and proposed mean not finished and not official.</p></div>
   </div>
  </section>

  <section id="workshop" aria-labelledby="h-workshop">
   <div class="sec-head"><p class="eyebrow amber">Coming next</p><h2 id="h-workshop">In the workshop</h2>
   <p class="intro">Work in development elsewhere that is not public yet, so there is nothing to link to. Each will get its own repository and site when it is ready; it then moves up into Projects. Interested in one? Use the <a href="{CONTACT}">contact form</a>.</p></div>
   <div class="grid wgrid">{workshop}</div>
  </section>

  <section id="about" aria-labelledby="h-about">
   <h2 id="h-about">About</h2>
   <div class="grid two">
    <article class="panel"><h3>Who makes these</h3>{about_role}<p>{e(owner["about"])}</p></article>
    <article class="panel"><h3>How to read this page</h3><ul>
     <li>Status is as each project states it. <strong>Prototype</strong> and <strong>proposed</strong> mean not finished and not official.</li>
     <li>Summaries are written from each project's own README.</li>
     <li>None of these is an official government service, policy or endorsement unless the project says so.</li>
     <li>Forks and private repositories are not listed.</li>
    </ul></article>
   </div>
  </section>

  <section id="contact" class="contact" aria-labelledby="h-contact">
   <div><h2 id="h-contact">Contact</h2>
   <p>Use the <a href="{CONTACT}">contact form</a>. It opens a GitHub issue, which is public, so do not include personal data. There is no email route. For a problem with one project, use that project's own contact form, linked from its site.</p></div>
   <a class="btn btn-amber" href="{CONTACT}">{icon("chat", 18)}Open the contact form</a>
  </section>
 </main>
</div>
<footer class="footer">
 <div class="wrap foot">
  <div class="foot-text">
   <p><strong>Disclaimer.</strong> Made in a personal capacity. These projects are not official government services or policy, and listing a project does not mean any organisation endorses it.</p>
   <p><strong>Transparency.</strong> This page is built from <a href="data/projects.json">projects.json</a> and <a href="data/workshop.json">workshop.json</a> by <code>tools/build.py</code> and checked before it is published. Written with help from Claude (Anthropic). The illustration and icons are drawn in code from the data; there are no photographs and no generated images. No cookies, analytics or third-party requests; the dark mode switch remembers your choice in this browser only if you use it.</p>
   <p><strong>Licences.</strong> This launchpad: code MIT, text OGL v3.0. Typeface: Space Grotesk, SIL Open Font License 1.1 (<a href="fonts/OFL.txt">licence</a>). Each project has its own licence, shown on its card.</p>
   <p><strong>Contact.</strong> <a href="{CONTACT}">Contact form</a> · <a href="{REPO}">Repository</a> · <a href="{REPO}/blob/main/ACCESSIBILITY.md">Accessibility statement</a></p>
  </div>
  <div class="colophon" aria-label="Colophon">{qr_svg(SITE)}<div class="bc">{barcode_svg("CYBERDUDEUK-" + d["version"])}<span>cyberdudeuk · v{e(d["version"])} · {e(d["updated"])}</span></div></div>
 </div>
</footer>
<script src="{asset("app.js")}"></script>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(page, encoding='utf-8')
    notfound = f'''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found: {e(owner["display_name"])}</title><link rel="stylesheet" href="/{asset("styles.css")}">
<script>/* Old toolkit links: send them to its new address with the same section. */
(function(){{var h=(location.hash||'').slice(1);var old={json.dumps(OLD_TOOLKIT_SECTIONS)};if(location.pathname==='/'&&old.indexOf(h)>-1){{location.replace('{NEW_TOOLKIT}#'+h);}}}})();</script>
</head><body><main class="wrap nf" id="main"><p class="eyebrow">Error 404</p><h1>Page not found</h1>
<p>The address may be mistyped, or the page may have moved.</p>
<ul><li><a href="/">See every project</a></li><li>The Public AI Utility Toolkit is now <a href="{NEW_TOOLKIT}">AI Capability Governance and Implementation</a></li><li><a href="{CONTACT}">Tell us about a broken link</a></li></ul>
</main></body></html>
'''
    (ROOT / '404.html').write_text(notfound, encoding='utf-8')
    return len(projects)


if __name__ == '__main__':
    print(f'built {build()} projects')
