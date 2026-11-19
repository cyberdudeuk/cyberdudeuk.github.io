#!/usr/bin/env python3
"""Browser checks: render the launchpad in Chrome at 1280, 390 and 320px and fail on
B1 the page scrolling sideways, B2 a console error, B3 the filters not filtering, B4 the drawer switch not working,
B5 an old toolkit link (#tool-triage) not reaching the toolkit's new address,
B6 search not finding a project, B7 the dark mode switch not changing the theme, B8 motion running when the reader
asks for reduced motion (including the live dot's ring, D-09), B9 one-project areas each taking a whole row again (D-08),
B10 a coverage map number not filtering to its projects, B11 a project hidden when JavaScript is off,
B12 an animated headline number not landing on the data's number,
B13 an automated accessibility rule failing (axe-core, vendored in tools/vendor) on the page in light, dark and phone views
and on the 404 page (D-11: the 404 heading was white on white),
B14 the back-to-top button not returning to the top, or its arrow not centred and upright (D-18), B15 a ways-in ring drawn empty (D-16),
B16 a note page losing its reading layout: paragraphs more than 32px apart (D-27: the homepage's 64px flex gap fell between
every paragraph), text lines wider than 80 characters, or the page scrolling sideways at 320px,
B17 (D-29) the spotlight's next button or dots not moving to the next slide, its Play button offered under reduced
motion, or the section links and the theme switch falling onto different rows (or off screen) at any width from
320 to 1280px: links fold into the menu before they would wrap.

Run: python3 tools/check_browser.py [--break NAME]
--break injects a deliberate fault so CI proves each check fails when it should. Uses the runner's Chrome (CHROME).
"""
import argparse
import asyncio
import functools
import http.server
import json
import os
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AXE = ROOT / 'tools' / 'vendor' / 'axe.min.js'
AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice']
NEW = 'https://cyberdudeuk.github.io/ai-capability-governance/#tool-triage'
NOTE = 'notes/one-home-for-my-open-work.html'
BREAKS = {
    'overflow': "document.querySelector('#main').insertAdjacentHTML('beforeend','<div style=\"width:2000px;height:2px\"></div>')",
    'consoleerror': "console.error('deliberate break')",
    'filters': "document.querySelectorAll('.cchip,.lchip').forEach(function(c){c.replaceWith(c.cloneNode(true));})",
    'drawer': "var t=document.getElementById('drawerToggle'); t.replaceWith(t.cloneNode(true));",
    'search': "var q=document.getElementById('q'); q.replaceWith(q.cloneNode(true));",
    'theme': "var t=document.getElementById('themeToggle'); t.replaceWith(t.cloneNode(true));",
    'motion': "document.body.animate([{opacity:1},{opacity:.99}],{duration:60000});",
    'density': "document.head.insertAdjacentHTML('beforeend','<style>.cat-block{grid-column:1/-1!important}</style>')",
    'coverage': "document.querySelectorAll('a.cell').forEach(function(c){c.replaceWith(c.cloneNode(true));})",
    'counters': "document.querySelector('.num[data-count]').textContent='999'",
    'a11y': "document.head.insertAdjacentHTML('beforeend','<style>.intro{color:#eeeeee!important}</style>')",
    'totop': "var t=document.getElementById('toTop'); var c=t.cloneNode(true); c.removeAttribute('href'); t.replaceWith(c);",
    'arrow': "document.head.insertAdjacentHTML('beforeend','<style>.totop .ico{position:absolute;left:0;top:0;transform:rotate(-90deg)}</style>')",
    'rings': "document.querySelectorAll('.ring .rv').forEach(function(r){r.style.setProperty('--len','0');})",
    'spotlight': "var n=document.getElementById('spotNext'); n.replaceWith(n.cloneNode(true));",
    'masthead': "document.documentElement.classList.remove('nav-fold');document.head.insertAdjacentHTML('beforeend','<style>.global{display:flex!important}.navmenu{display:none!important}</style>')",
    'notegap': "document.head.insertAdjacentHTML('beforeend','<style>main.note-page .prose{display:flex;flex-direction:column;gap:64px}</style>')",
}
CODES = {'overflow': 'B1', 'consoleerror': 'B2', 'filters': 'B3', 'drawer': 'B4', 'redirect': 'B5', 'search': 'B6', 'theme': 'B7',
         'motion': 'B8', 'density': 'B9', 'coverage': 'B10', 'nojs': 'B11', 'counters': 'B12', 'a11y': 'B13', 'totop': 'B14', 'arrow': 'B14', 'rings': 'B15', 'notegap': 'B16', 'spotlight': 'B17', 'masthead': 'B17'}


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


async def run(brk):
    from playwright.async_api import async_playwright
    srv = serve()
    base = f'http://127.0.0.1:{srv.server_address[1]}/'
    nprojects = len(json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))['projects'])
    found = []

    async def page(b, w=1280, h=900, **kw):
        ctx = await b.new_context(viewport={'width': w, 'height': h}, **kw)
        await ctx.route('https://cyberdudeuk.github.io/**', lambda r: r.fulfill(status=200, body='moved'))
        pg = await ctx.new_page()
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        return ctx, pg, errs

    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--no-sandbox'])
        for w, h, name in ((1280, 900, 'desktop'), (390, 844, 'phone'), (320, 640, 'small phone')):
            ctx, pg, errs = await page(b, w, h)
            await pg.goto(base + 'index.html', wait_until='load')
            if brk in BREAKS and brk not in ('motion', 'counters', 'search', 'coverage', 'theme', 'a11y', 'totop', 'rings', 'arrow'):
                await pg.evaluate(BREAKS[brk])
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            if sw > w:
                found.append(f'B1 {name}: page is {sw}px wide on a {w}px screen')
            if name == 'desktop':
                total = await pg.locator('.card').count()
                # B9 (D-08): two one-project areas share a row instead of each taking a whole row
                tops = await pg.evaluate("[document.getElementById('cat-ai').getBoundingClientRect().top, document.getElementById('cat-standards').getBoundingClientRect().top]")
                if abs(tops[0] - tops[1]) > 2:
                    found.append(f'B9 one-project areas do not share a row (tops {tops})')
                await pg.click('button.cchip[data-cat="data"]')
                await pg.click('button.lchip[data-level="beginner"]')
                vis = await pg.locator('.card:visible').count()
                if not 0 < vis < total:
                    found.append(f'B3 filters did not filter ({vis} of {total} visible)')
                before = await pg.evaluate('document.getElementById("drawer").hidden')
                await pg.click('#drawerToggle')
                after = await pg.evaluate('document.getElementById("drawer").hidden')
                if before == after:
                    found.append('B4 the category menu switch did not change the menu')
                # B6: search finds one project by a word in its name
                await pg.reload(wait_until='load')
                if brk == 'search':
                    await pg.evaluate(BREAKS[brk])
                await pg.fill('#q', 'plainspoken')
                vis = await pg.locator('.card:visible').count()
                if vis != 1:
                    found.append(f'B6 search for "plainspoken" showed {vis} projects, not 1')
                # B10: a coverage map number filters to exactly that many projects
                await pg.reload(wait_until='load')
                if brk == 'coverage':
                    await pg.evaluate(BREAKS[brk])
                cell = pg.locator('a.cell[data-cell-cat="data"][data-cell-level="intermediate"]')
                want = int(await cell.get_attribute('data-n'))
                await cell.click()
                vis = await pg.locator('.card:visible').count()
                if vis != want:
                    found.append(f'B10 coverage number {want} showed {vis} projects')
                # B7: the dark mode switch changes the theme and the page colour
                await pg.reload(wait_until='load')
                if brk == 'theme':
                    await pg.evaluate(BREAKS[brk])
                bg1 = await pg.evaluate('getComputedStyle(document.body).backgroundColor')
                await pg.click('#themeToggle')
                bg2 = await pg.evaluate('getComputedStyle(document.body).backgroundColor')
                if bg1 == bg2:
                    found.append('B7 the dark mode switch did not change the theme')
                # B12: animated headline numbers land on the data's numbers
                await pg.reload(wait_until='load')
                await pg.wait_for_timeout(1800)
                if brk == 'counters':
                    await pg.evaluate(BREAKS[brk])
                bad = await pg.evaluate("Array.from(document.querySelectorAll('.num[data-count]')).filter(function(n){return n.textContent!==n.getAttribute('data-count');}).length")
                if bad:
                    found.append(f'B12 {bad} headline number(s) did not land on the data')
            if errs:
                found.append(f'B2 {name}: console errors: {errs[:3]}')
            await ctx.close()
        # B8 (D-09): with reduced motion requested, nothing moves
        ctx, pg, errs = await page(b, reduced_motion='reduce')
        await pg.goto(base + 'index.html', wait_until='load')
        await pg.wait_for_timeout(300)
        if brk == 'motion':
            await pg.evaluate(BREAKS[brk])
        moving = await pg.evaluate("document.getAnimations().filter(function(a){return a.playState==='running';}).length")
        ring = await pg.evaluate("getComputedStyle(document.querySelector('.dot.live'),'::after').display")
        reveal = await pg.locator('.reveal').count()
        if moving or ring != 'none' or reveal:
            found.append(f'B8 motion under reduced motion: {moving} running animations, live ring display {ring}, {reveal} reveal effects')
        await ctx.close()
        # B11: with JavaScript off, every project is on show and no control that needs it appears
        ctx, pg, errs = await page(b, java_script_enabled=False)
        if brk == 'nojs':
            async def hide(route):
                r = await route.fetch()
                body = (await r.text()).replace('<article class="card', '<article hidden class="card', 1)
                await route.fulfill(response=r, body=body)
            await pg.route('**/index.html', hide)
        await pg.goto(base + 'index.html', wait_until='load')
        vis = await pg.locator('.card:visible').count()
        ctl = await pg.locator('.js-only:visible').count()
        if vis != nprojects or ctl:
            found.append(f'B11 without JavaScript {vis} of {nprojects} projects show and {ctl} script-only controls appear')
        await ctx.close()
        # B14: back to top appears after scrolling and returns to the top
        ctx, pg, errs = await page(b)
        await pg.goto(base + 'index.html', wait_until='load')
        if brk in ('totop', 'arrow'):
            await pg.evaluate(BREAKS[brk])
        await pg.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
        await pg.wait_for_timeout(500)
        geo = await pg.evaluate("""(() => { const b = document.getElementById('toTop'), i = b && b.querySelector('.ico');
            if (!b || !i) return null; const r = b.getBoundingClientRect(), q = i.getBoundingClientRect();
            return {dx: Math.abs((r.left + r.right) / 2 - (q.left + q.right) / 2), dy: Math.abs((r.top + r.bottom) / 2 - (q.top + q.bottom) / 2), t: getComputedStyle(i).transform}; })()""")
        if not geo or geo['dx'] > 2 or geo['dy'] > 2 or geo['t'] not in ('none', 'matrix(1, 0, 0, 1, 0, 0)'):
            found.append(f'B14 the back-to-top arrow is not centred and upright: {geo}')
        try:
            await pg.click('#toTop', timeout=2000)
            await pg.wait_for_timeout(1500)
            y = await pg.evaluate('window.scrollY')
        except Exception:
            y = -1
        if not 0 <= y < 50:
            found.append(f'B14 back to top left the page at {y}')
        await ctx.close()
        # B15 (D-16): the ways-in rings show their share (a colour and a non-zero arc)
        ctx, pg, errs = await page(b, reduced_motion='reduce')
        await pg.goto(base + 'index.html', wait_until='load')
        if brk == 'rings':
            await pg.evaluate(BREAKS[brk])
        bad = await pg.evaluate("Array.from(document.querySelectorAll('.ring .rv')).filter(function(r){var c=getComputedStyle(r);return c.stroke==='none'||!(parseFloat(c.strokeDasharray)>0);}).length")
        if bad:
            found.append(f'B15 {bad} ways-in ring(s) drawn empty')
        await ctx.close()
        # B17 (D-29): the spotlight moves on request and never rotates by itself under reduced motion
        ctx, pg, errs = await page(b)
        await pg.goto(base + 'index.html', wait_until='load')
        if brk == 'spotlight':
            await pg.evaluate(BREAKS[brk])
        cur = "Array.from(document.querySelectorAll('.sdot')).findIndex(function(d){return d.getAttribute('aria-current')==='true';})"
        await pg.click('#spotNext')
        await pg.wait_for_timeout(900)
        if await pg.evaluate(cur) != 1:
            found.append('B17 the spotlight next button did not move to slide 2')
        await pg.click('.sdot[data-slide="0"]')
        await pg.wait_for_timeout(900)
        if await pg.evaluate(cur) != 0:
            found.append('B17 the spotlight dots did not move to slide 1')
        await ctx.close()
        ctx, pg, errs = await page(b, reduced_motion='reduce')
        await pg.goto(base + 'index.html', wait_until='load')
        if await pg.locator('#spotPlay:visible').count():
            found.append('B17 the spotlight offers rotation under reduced motion')
        await ctx.close()
        # B17 (D-29): the masthead stays on one row; links fold into the menu before they would wrap
        # D-33: it held with one font and failed on the CI runner's wider one, so it runs with the wide font and larger text.
        for w, font, zoom in ((320, '', 1), (390, '', 1), (901, '', 1), (1000, '', 1), (1081, '', 1), (1181, '', 1), (1280, '', 1),
                              (1081, 'DejaVu Sans', 1), (1181, 'DejaVu Sans', 1), (1240, 'DejaVu Sans', 1), (1280, 'DejaVu Sans', 1), (1280, '', 1.25)):
            ctx, pg, errs = await page(b, w, 800)
            if font or zoom != 1:
                css = (f'body,button,.global a{{font-family:"{font}",sans-serif!important}}' if font else '') + f'html{{font-size:{zoom * 100:.0f}%}}'
                await pg.add_init_script('document.addEventListener("DOMContentLoaded",function(){var st=document.createElement("style");'
                                         f'st.textContent={json.dumps(css)};document.head.appendChild(st);}});')
            await pg.goto(base + 'index.html', wait_until='load')
            await pg.wait_for_timeout(150)
            if font and font not in await pg.evaluate("getComputedStyle(document.querySelector('.global a')).fontFamily"):
                found.append(f'B17 the {font} test font was not applied')
            if brk == 'masthead':
                await pg.evaluate(BREAKS[brk])
            geo = await pg.evaluate("""(() => { const vis = q => { const el = document.querySelector(q); const r = el && el.getBoundingClientRect(); return r && r.width ? r : null; };
                const n = vis('nav.global') || vis('.navmenu'), t = vis('#themeToggle');
                return {gap: n && t ? Math.abs((n.top + n.bottom) / 2 - (t.top + t.bottom) / 2) : 999, right: t ? t.right : 999}; })()""")
            if geo['gap'] > 8 or geo['right'] > w:
                found.append(f'B17 the masthead links and the theme switch are not on one row at {w}px{" with " + font if font else ""}{f" at {zoom:.0%} text" if zoom != 1 else ""}: {geo}')
            await ctx.close()
        # B13 (D-11): automated accessibility rules pass in every view, and on the 404 page
        for view, w, scheme, path in (('light', 1280, 'light', 'index.html'), ('dark', 1280, 'dark', 'index.html'),
                                      ('phone', 390, 'light', 'index.html'), ('404', 1280, 'light', '404.html')):
            ctx, pg, errs = await page(b, w, 900, color_scheme=scheme, reduced_motion='reduce')
            await pg.goto(base + path, wait_until='load')
            if brk == 'a11y' and path == 'index.html':
                await pg.evaluate(BREAKS[brk])
            await pg.add_script_tag(path=str(AXE))
            res = await pg.evaluate('(tags) => axe.run(document, {runOnly: {type: "tag", values: tags}}).then(r => r.violations.map(v => v.id + " (" + v.nodes.length + ")"))', AXE_TAGS)
            if res:
                found.append(f'B13 {view}: accessibility rules failed: {res}')
            await ctx.close()
        # B16 (D-27): note pages keep their reading layout at every width
        for w in (1280, 390, 320):
            ctx, pg, errs = await page(b, w, 900, reduced_motion='reduce')
            await pg.goto(base + NOTE, wait_until='load')
            if brk == 'notegap':
                await pg.evaluate(BREAKS[brk])
            gap = await pg.evaluate("Math.max.apply(null, Array.from(document.querySelectorAll('.prose > p + p')).map(function(p){return p.getBoundingClientRect().top - p.previousElementSibling.getBoundingClientRect().bottom;}))")
            if gap > 32:
                found.append(f'B16 note paragraphs are {gap:.0f}px apart at {w}px (max 32)')
            chars = await pg.evaluate("(function(){var p=document.querySelector('.prose p');var cs=getComputedStyle(p);var c=document.createElement('canvas').getContext('2d');c.font=cs.fontSize+' '+cs.fontFamily;return p.clientWidth/c.measureText('abcdefghijklmnopqrstuvwxyz ').width*27;})()")
            if chars > 80:
                found.append(f'B16 note lines are about {chars:.0f} characters at {w}px (max 80)')
            if await pg.evaluate('document.documentElement.scrollWidth > innerWidth + 1'):
                found.append(f'B16 note page scrolls sideways at {w}px')
            await ctx.close()
        for view, w, scheme in (('note light', 1280, 'light'), ('note dark', 1280, 'dark'), ('note phone', 390, 'light')):
            ctx, pg, errs = await page(b, w, 900, color_scheme=scheme, reduced_motion='reduce')
            await pg.goto(base + NOTE, wait_until='load')
            await pg.add_script_tag(path=str(AXE))
            res = await pg.evaluate('(tags) => axe.run(document, {runOnly: {type: "tag", values: tags}}).then(r => r.violations.map(v => v.id + " (" + v.nodes.length + ")"))', AXE_TAGS)
            if res:
                found.append(f'B13 {view}: accessibility rules failed: {res}')
            await ctx.close()
        # B5: old toolkit links still reach the toolkit
        ctx, pg, errs = await page(b)
        url = base + ('index.html#nothing-old' if brk == 'redirect' else 'index.html#tool-triage')
        await pg.goto(url, wait_until='load')
        await pg.wait_for_timeout(300)
        if pg.url != NEW:
            found.append(f'B5 old toolkit link stayed at {pg.url}')
        await b.close()
    srv.shutdown()
    return found


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--break', dest='brk', choices=sorted(CODES))
    a = ap.parse_args(argv)
    found = asyncio.run(run(a.brk))
    if a.brk:
        ok = any(x.startswith(CODES[a.brk]) for x in found)
        print(f'Vaccination {a.brk}: {"caught" if ok else "NOT CAUGHT"}')
        return 0 if ok else 1
    print('FAIL\n' + '\n'.join(found) if found else f'PASS: {len(CODES)} browser checks at 3 widths')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
