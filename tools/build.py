#!/usr/bin/env python3
"""Build index.html and 404.html from data/projects.json and data/owner.json.

The page is static: every project is in the HTML and readable without JavaScript. app.js only adds filtering,
sorting and the drawer toggle. Run: python3 tools/build.py  (then python3 tools/check_site.py)
"""
import datetime as dt
import html
import io
import json
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
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'code': '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5"/>',
}


def icon(name, size=20, label=None):
    a = f'role="img" aria-label="{e(label)}"' if label else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {a}>{ICONS[name]}</svg>')


def qr_svg(url):
    import segno
    buf = io.BytesIO()
    q = segno.make(url, error='m')
    q.save(buf, kind='svg', scale=4, border=1, xmldecl=False, svgns=True, dark='#0b0c0c')
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


def card(p, cats):
    c = cats[p['category']]
    lv = ''.join(f'<li class="lvl lvl-{x.lower()}">{e(x)}</li>' for x in p['levels'])
    new = '<span class="flag">New</span>' if p.get('new') else ''
    links = []
    if p.get('site'):
        links.append(f'<a class="btn btn-primary" href="{e(p["site"])}">Open the site{icon("arrow", 16)}<span class="visually-hidden">: {e(p["name"])}</span></a>')
    links.append(f'<a class="btn" href="{e(p["repo"])}">{icon("code", 16)}Repository<span class="visually-hidden">: {e(p["name"])}</span></a>')
    how = f'<p class="how">{e(p["how"])}</p>' if p.get('how') else ''
    upd = dt.date.fromisoformat(p['updated'])
    return f'''<article class="card" id="p-{e(p["id"])}" data-category="{e(p["category"])}" data-status="{e(p["status"])}" data-updated="{e(p["updated"])}" data-name="{e(p["name"])}" data-levels="{e(" ".join(x.lower() for x in p["levels"]))}">
  <div class="card-top"><span class="cat">{icon(c["icon"], 18)}{e(c["label"])}</span>{new}</div>
  <h3>{e(p["name"])}</h3>
  <p>{e(p["summary"])}</p>
  <dl class="facts"><div><dt>Status</dt><dd>{e(p["status"])}</dd></div><div><dt>For</dt><dd>{e(p["audience"])}</dd></div><div><dt>Updated</dt><dd><time datetime="{e(p["updated"])}">{upd.day} {upd:%B %Y}</time></dd></div><div><dt>Licence</dt><dd>{e(p["licence"])}</dd></div></dl>
  <ul class="levels" aria-label="Levels this project supports">{lv}</ul>
  {how}<div class="actions">{"".join(links)}</div>
</article>'''


def build():
    d = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))
    owner = json.loads((ROOT / 'data' / 'owner.json').read_text(encoding='utf-8'))
    cats = {c['id']: c for c in d['categories']}
    projects = sorted(d['projects'], key=lambda p: p['updated'], reverse=True)
    count = {c: sum(1 for p in projects if p['category'] == c) for c in cats}
    newc = {c: any(p.get('new') for p in projects if p['category'] == c) for c in cats}
    live = sum(1 for p in projects if p.get('site'))
    upd = dt.date.fromisoformat(d['updated'])
    drawer = ''.join(
        f'<li><a href="#cat-{e(c)}" data-filter-cat="{e(c)}">{icon(cats[c]["icon"], 18)}<span>{e(cats[c]["label"])}</span>'
        f'{"<span class=flag>New</span>" if newc[c] else ""}<span class="count" aria-label="{count[c]} projects">{count[c]}</span></a></li>'
        for c in cats if count[c])
    chips = '<button type="button" class="chip cchip" data-cat="all" aria-pressed="true">All · ' + str(len(projects)) + '</button>' + ''.join(
        f'<button type="button" class="chip cchip" data-cat="{e(c)}" aria-pressed="false">{e(cats[c]["label"])} · {count[c]}</button>' for c in cats if count[c])
    lchips = '<button type="button" class="chip lchip" data-level="all" aria-pressed="true">Any level</button>' + ''.join(
        f'<button type="button" class="chip lchip" data-level="{x.lower()}" aria-pressed="false">{x} · {sum(1 for p in projects if x in p["levels"])}</button>' for x in ('Beginner', 'Intermediate', 'Advanced'))
    sections = ''.join(
        f'<section class="cat-block" id="cat-{e(c)}" aria-labelledby="h-{e(c)}"><h3 class="cat-h" id="h-{e(c)}">{icon(cats[c]["icon"], 22)}{e(cats[c]["label"])} <span class="count">{count[c]}</span></h3>'
        f'<div class="grid">{"".join(card(p, cats) for p in projects if p["category"] == c)}</div></section>'
        for c in cats if count[c])

    byid = {p['id']: p for p in projects}

    def pick(level):
        return ''.join(f'<li><a href="#p-{e(i)}">{e(byid[i]["name"])}</a></li>' for i in d['ways_in'][level])

    def nlevel(level):
        return sum(1 for p in projects if level in p['levels'])
    jsonld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': f'{owner["display_name"]}: projects', 'url': SITE,
              'dateModified': d['updated'], 'inLanguage': 'en-GB',
              'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(projects), 'itemListElement': [
                  {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'CreativeWork', 'name': p['name'], 'url': p.get('site') or p['repo'],
                                                                    'codeRepository': p['repo'], 'abstract': p['summary'], 'genre': cats[p['category']]['label']}}
                  for i, p in enumerate(projects)]}}
    about_role = f'<p class="role">{e(owner["role"])}</p>' if owner.get('role') else ''
    page = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(owner["display_name"])}: projects for better public services</title>
<meta name="description" content="A launchpad for every project by {e(owner["display_name"])}: AI governance, data standards, data management and quality, code reuse, knowledge mapping, skills and community work.">
<meta name="version" content="{e(d["version"])}">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(owner["display_name"])}: projects"><meta property="og:url" content="{SITE}">
<meta name="theme-color" content="#0b0c0c">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%231d70b8'/%3E%3Cpath d='M9 16h14M17 10l6 6-6 6' stroke='white' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3C/svg%3E">
<link rel="stylesheet" href="styles.css">
<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>/* Old links to the Public AI Utility Toolkit (which lived here until November 2026) go to its new address. */
(function(){{var h=(location.hash||'').slice(1);var old={json.dumps(OLD_TOOLKIT_SECTIONS)};if(old.indexOf(h)>-1){{location.replace('{NEW_TOOLKIT}#'+h);}}}})();</script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header class="masthead">
 <div class="wrap mast">
  <a class="brand" href="#top"><span class="mark" aria-hidden="true">{icon("arrow", 20)}</span><span>{e(owner["display_name"])}<small>Projects for better public services</small></span></a>
  <nav class="global" aria-label="Sections">
   <a href="#projects">Projects</a><a href="#ways-in">Ways in</a><a href="#about">About</a><a href="#contact">Contact</a>
  </nav>
 </div>
</header>
<div class="wrap layout">
 <div class="toggle-row js-only"><button type="button" class="toggle" id="drawerToggle" role="switch" aria-checked="true" aria-controls="drawer"><span class="track" aria-hidden="true"><span class="knob"></span></span><span>Category menu: <span id="drawerState">shown</span></span></button></div>
 <aside class="drawer" id="drawer" aria-label="Projects by category">
  <p class="drawer-h">On this page</p>
  <ul>{drawer}</ul>
 </aside>
 <main id="main" tabindex="-1">
  <section class="hero" id="top" aria-labelledby="h-top">
   <p class="eyebrow">Launchpad · updated {upd.day} {upd:%B %Y}</p>
   <h1 id="h-top">Projects for better public services</h1>
   <p class="lede">One place to find every project I build, now and in future: guidance, open standards and working tools for data and AI in the public sector, and some personal projects. Each lives in its own repository with its own site.</p>
   <div class="stats"><div><span class="num">{len(projects)}</span><span class="lbl">projects</span></div><div><span class="num">{live}</span><span class="lbl">with a live site</span></div><div><span class="num">{sum(1 for c in cats if count[c])}</span><span class="lbl">areas of work</span></div></div>
   <p class="moved">Looking for the <strong>Public AI Utility Toolkit</strong>? It is now <a href="{NEW_TOOLKIT}">AI Capability Governance and Implementation</a>, with its own address.</p>
  </section>

  <section id="ways-in" aria-labelledby="h-ways">
   <h2 id="h-ways">Choose your way in</h2>
   <p>Every project says which levels it supports. Start where you are; the suggestions are a good first stop.</p>
   <div class="grid three">
    <article class="way"><span class="lvl lvl-beginner">Beginner</span><h3>New to the subject, or to GitHub</h3><p>Plain-English sites you can use in a browser, with no account and nothing to install.</p><p class="small"><strong>Suggested starting points</strong></p><ul>{pick("Beginner")}</ul><p class="small"><button type="button" class="linkish js-only" data-level-go="beginner">Show all {nlevel("Beginner")} projects at this level</button></p></article>
    <article class="way"><span class="lvl lvl-intermediate">Intermediate</span><h3>Using it in your work</h3><p>Guidance, registers and tools for a team, an asset or a return.</p><p class="small"><strong>Suggested starting points</strong></p><ul>{pick("Intermediate")}</ul><p class="small"><button type="button" class="linkish js-only" data-level-go="intermediate">Show all {nlevel("Intermediate")} projects at this level</button></p></article>
    <article class="way"><span class="lvl lvl-advanced">Advanced</span><h3>Building, assuring or reusing</h3><p>Open data, schemas, checks and code you can run, adapt or contribute to.</p><p class="small"><strong>Suggested starting points</strong></p><ul>{pick("Advanced")}</ul><p class="small"><button type="button" class="linkish js-only" data-level-go="advanced">Show all {nlevel("Advanced")} projects at this level</button></p></article>
   </div>
  </section>

  <section id="projects" aria-labelledby="h-projects">
   <h2 id="h-projects">Projects</h2>
   <div class="controls js-only">
    <div role="group" aria-label="Filter by area" class="chips">{chips}</div>
    <div role="group" aria-label="Filter by level" class="chips">{lchips}</div>
    <label class="sort">Sort by <select id="sort"><option value="updated">Most recently updated</option><option value="name">Name, A to Z</option></select></label>
   </div>
   <p class="shown js-only" aria-live="polite" id="shown">Showing all {len(projects)} projects</p>
   {sections}
   <p class="note">The list is open data: <a href="data/projects.json">projects.json</a>. A weekly check flags any new public repository that is not yet listed, so future projects appear here once a person has added them.</p>
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

  <section id="contact" aria-labelledby="h-contact">
   <h2 id="h-contact">Contact</h2>
   <p>Use the <a href="{CONTACT}">contact form</a>. It opens a GitHub issue, which is public, so do not include personal data. There is no email route. For a problem with one project, use that project's own contact form, linked from its site.</p>
  </section>
 </main>
</div>
<footer class="footer">
 <div class="wrap foot">
  <div class="foot-text">
   <p><strong>Disclaimer.</strong> Made in a personal capacity. These projects are not official government services or policy, and listing a project does not mean any organisation endorses it.</p>
   <p><strong>Transparency.</strong> This page is built from <a href="data/projects.json">projects.json</a> by <code>tools/build.py</code> and checked before it is published. Written with help from Claude (Anthropic). No cookies, analytics or third-party requests.</p>
   <p><strong>Licences.</strong> This launchpad: code MIT, text OGL v3.0. Each project has its own licence, shown on its card.</p>
   <p><strong>Contact.</strong> <a href="{CONTACT}">Contact form</a> · <a href="{REPO}">Repository</a> · <a href="{REPO}/blob/main/ACCESSIBILITY.md">Accessibility statement</a></p>
  </div>
  <div class="colophon" aria-label="Colophon">{qr_svg(SITE)}<div class="bc">{barcode_svg("CYBERDUDEUK-" + d["version"])}<span>cyberdudeuk · v{e(d["version"])} · {e(d["updated"])}</span></div></div>
 </div>
</footer>
<script src="app.js"></script>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(page, encoding='utf-8')
    notfound = f'''<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found: {e(owner["display_name"])}</title><link rel="stylesheet" href="/styles.css">
<script>/* Old toolkit links: send them to its new address with the same section. */
(function(){{var h=(location.hash||'').slice(1);var old={json.dumps(OLD_TOOLKIT_SECTIONS)};if(location.pathname==='/'&&old.indexOf(h)>-1){{location.replace('{NEW_TOOLKIT}#'+h);}}}})();</script>
</head><body><main class="wrap" id="main" style="padding:48px 20px"><h1>Page not found</h1>
<p>The address may be mistyped, or the page may have moved.</p>
<ul><li><a href="/">See every project</a></li><li>The Public AI Utility Toolkit is now <a href="{NEW_TOOLKIT}">AI Capability Governance and Implementation</a></li><li><a href="{CONTACT}">Tell us about a broken link</a></li></ul>
</main></body></html>
'''
    (ROOT / '404.html').write_text(notfound, encoding='utf-8')
    return len(projects)


if __name__ == '__main__':
    print(f'built {build()} projects')
