#!/usr/bin/env python3
"""Make og.jpg, the 1200x630 picture shown when the launchpad is shared, from the same data and illustration as the page.

Run after changing the projects: python3 tools/og.py  (uses the runner's Chrome, CHROME). The image is committed;
tools/check_site.py (L20) checks it exists at the right size.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402


def page():
    d = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))
    owner = json.loads((ROOT / 'data' / 'owner.json').read_text(encoding='utf-8'))
    cats = {c['id']: c for c in d['categories']}
    count = {c: sum(1 for p in d['projects'] if p['category'] == c) for c in cats}
    newc = {c: any(p.get('new') for p in d['projects'] if p['category'] == c) for c in cats}
    live = sum(1 for p in d['projects'] if p.get('site'))
    areas = sum(1 for c in cats if count[c])
    art = build.constellation(cats, count, newc, len(d['projects']))
    font = (ROOT / 'fonts' / 'space-grotesk-latin-wght.woff2').as_uri()
    css = (ROOT / 'styles.css').read_text(encoding='utf-8').replace('url("fonts/space-grotesk-latin-wght.woff2")', f'url("{font}")')
    return f'''<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8"><style>{css}
body{{margin:0;width:1200px;height:630px;background:var(--night);overflow:hidden}}
.og{{display:flex;align-items:center;gap:24px;height:630px;padding:0 64px;color:#fff;position:relative}}
.og::before{{content:"";position:absolute;inset:0;background:radial-gradient(60% 70% at 78% 45%,rgba(79,209,181,.12),transparent 70%)}}
.og h1{{font-size:62px;max-width:13ch;margin:18px 0 22px}}.og .art{{flex:0 0 520px}}.og .txt{{flex:1;position:relative}}
.og .stats{{grid-template-columns:repeat(3,minmax(0,1fr));max-width:460px}}
*{{animation:none!important}}</style></head><body class="hero">
<div class="og"><div class="txt"><p class="brand"><svg class="mark" width="44" height="44" viewBox="0 0 40 40"><rect width="40" height="40" rx="11"/><path d="M13 14L27 14L20 27Z"/><circle cx="13" cy="14" r="3.4"/><circle cx="27" cy="14" r="3.4"/><circle cx="20" cy="27" r="3.4"/></svg><span>{owner.get("site_name") or owner["display_name"]}<small>by {owner["display_name"]} · projects for better public services</small></span></p>
<h1>{owner.get("tagline") or "Open tools and guidance for data and AI in public services"}</h1>
<div class="stats"><div class="s1"><span class="num">{len(d["projects"])}</span><span class="lbl">public projects</span></div><div class="s2"><span class="num">{live}</span><span class="lbl">with a live site</span></div><div class="s3"><span class="num">{areas}</span><span class="lbl">areas of work</span></div></div></div>
<div class="art">{art}</div></div></body></html>'''


async def shoot():
    from playwright.async_api import async_playwright
    tmp = ROOT / '.og.html'
    tmp.write_text(page(), encoding='utf-8')
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--no-sandbox'])
            pg = await b.new_page(viewport={'width': 1200, 'height': 630})
            await pg.goto(tmp.as_uri(), wait_until='load')
            await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=str(ROOT / 'og.jpg'), type='jpeg', quality=88)
            await b.close()
    finally:
        tmp.unlink()


if __name__ == '__main__':
    asyncio.run(shoot())
    print('wrote og.jpg')
