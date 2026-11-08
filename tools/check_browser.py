#!/usr/bin/env python3
"""Browser checks: render the launchpad in Chrome at 1280, 390 and 320px and fail on
B1 the page scrolling sideways, B2 a console error, B3 the filters not filtering, B4 the drawer switch not working,
B5 an old toolkit link (#tool-triage) not reaching the toolkit's new address.

Run: python3 tools/check_browser.py [--break overflow|consoleerror|filters|drawer|redirect]
--break injects a deliberate fault so CI proves each check fails when it should. Uses the runner's Chrome (CHROME).
"""
import argparse
import asyncio
import functools
import http.server
import os
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEW = 'https://cyberdudeuk.github.io/ai-capability-governance/#tool-triage'
BREAKS = {
    'overflow': "document.querySelector('#top').insertAdjacentHTML('beforeend','<div style=\"width:2000px;height:2px\"></div>')",
    'consoleerror': "console.error('deliberate break')",
    'filters': "document.querySelectorAll('.cchip,.lchip').forEach(function(c){c.replaceWith(c.cloneNode(true));})",
    'drawer': "var t=document.getElementById('drawerToggle'); t.replaceWith(t.cloneNode(true));",
}
CODES = {'overflow': 'B1', 'consoleerror': 'B2', 'filters': 'B3', 'drawer': 'B4', 'redirect': 'B5'}


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
    found = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get('CHROME', '/usr/bin/google-chrome'), args=['--no-sandbox'])
        for w, h, name in ((1280, 900, 'desktop'), (390, 844, 'phone'), (320, 640, 'small phone')):
            ctx = await b.new_context(viewport={'width': w, 'height': h})
            await ctx.route('https://cyberdudeuk.github.io/**', lambda r: r.fulfill(status=200, body='moved'))
            pg = await ctx.new_page()
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(base + 'index.html', wait_until='load')
            if brk in BREAKS:
                await pg.evaluate(BREAKS[brk])
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            if sw > w:
                found.append(f'B1 {name}: page is {sw}px wide on a {w}px screen')
            if errs:
                found.append(f'B2 {name}: console errors: {errs[:3]}')
            if name == 'desktop':
                total = await pg.locator('.card').count()
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
            await ctx.close()
        ctx = await b.new_context()
        await ctx.route('https://cyberdudeuk.github.io/**', lambda r: r.fulfill(status=200, body='moved'))
        pg = await ctx.new_page()
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
    print('FAIL\n' + '\n'.join(found) if found else 'PASS: 5 browser checks at 3 widths')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
