#!/usr/bin/env python3
"""Static checks for the launchpad (L1 to L23). Each names the defect or risk it guards against (docs/defect-register.md);
tests/test_site.py proves every check fails on a deliberate break.

Run: python3 tools/check_site.py [root]   (exit 1 on any failure)
"""
import html as htmllib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_WORKFLOWS = {'pages.yml', 'checks.yml', 'discover.yml', 'triage.yml', 'digest.yml', 'labels.yml', 'codeql.yml', 'scorecard.yml', 'dependency-review.yml', 'projects.yml'}
LEVELS = {'Beginner', 'Intermediate', 'Advanced'}
FIELDS = ('id', 'name', 'category', 'status', 'updated', 'summary', 'audience', 'levels', 'repo', 'licence')
EMAIL = re.compile(r'[\w.+-]+@[A-Za-z][\w-]*(\.[\w-]+)*\.[A-Za-z]{2,}\b')


def problems(root):
    root = Path(root)
    s = (root / 'index.html').read_text(encoding='utf-8')
    nf = (root / '404.html').read_text(encoding='utf-8')
    readme = (root / 'README.md').read_text(encoding='utf-8')
    d = json.loads((root / 'data' / 'projects.json').read_text(encoding='utf-8'))
    out = []

    def check(ok, msg):
        if not ok:
            out.append(msg)

    # L1: contact is by form only; no email address anywhere a reader sees.
    for name, text in (('index.html', s), ('404.html', nf), ('README.md', readme)):
        check(not EMAIL.search(text), f'L1 email address in {name}')
    # L2: the page is built from the data, never edited by hand. Rebuild in a copy and compare.
    tmp = Path(tempfile.mkdtemp())
    try:
        for f in ('data', 'tools'):
            shutil.copytree(root / f, tmp / f)
        for f in ('styles.css', 'app.js'):
            shutil.copy(root / f, tmp / f)
        r = subprocess.run([sys.executable, str(tmp / 'tools' / 'build.py')], capture_output=True, text=True)
        check(r.returncode == 0, f'L2 build failed: {r.stderr[-200:]}')
        if r.returncode == 0:
            check((tmp / 'index.html').read_text(encoding='utf-8') == s, 'L2 index.html is out of step with data/projects.json: run python3 tools/build.py')
            check((tmp / '404.html').read_text(encoding='utf-8') == nf, 'L2 404.html is out of step: run python3 tools/build.py')
    finally:
        shutil.rmtree(tmp)
    # L3: every project is complete and honest about where it lives.
    cats = {c['id'] for c in d['categories']}
    ids = [p.get('id') for p in d['projects']]
    check(len(ids) == len(set(ids)), 'L3 duplicate project ids')
    for p in d['projects']:
        pid = p.get('id', '?')
        for f in FIELDS:
            check(bool(p.get(f)), f'L3 {pid} missing {f}')
        check(p.get('category') in cats, f'L3 {pid} has an unknown category')
        check(set(p.get('levels', [])) <= LEVELS and p.get('levels'), f'L3 {pid} levels must be Beginner, Intermediate or Advanced')
        check(p.get('repo', '').startswith('https://github.com/cyberdudeuk/'), f'L3 {pid} repo is not in github.com/cyberdudeuk')
        check(not p.get('site') or p['site'].startswith('https://cyberdudeuk.github.io/'), f'L3 {pid} site is not on cyberdudeuk.github.io')
        check(bool(p.get('site')) or bool(p.get('how')), f'L3 {pid} has no site, so it must say how to use it ("how")')
        check(re.fullmatch(r'\d{4}-\d{2}-\d{2}', p.get('updated', '')) is not None, f'L3 {pid} updated is not a date')
    # L4: every project is on the page, with its links.
    for p in d['projects']:
        check(f'id="p-{p["id"]}"' in s, f'L4 {p["id"]} is not on the page')
        check(htmllib.escape(p['repo']) in s, f'L4 {p["id"]} repository link is not on the page')
        if p.get('site'):
            check(htmllib.escape(p['site']) in s, f'L4 {p["id"]} site link is not on the page')
    # L5: suggested starting points name real projects that support that level.
    byid = {p['id']: p for p in d['projects']}
    for lvl in LEVELS:
        for i in d.get('ways_in', {}).get(lvl, []):
            check(i in byid and lvl in byid[i]['levels'], f'L5 ways_in {lvl} names {i}, which is not a project at that level')
    # L6: old links to the toolkit that lived here still reach it.
    for name, text in (('index.html', s), ('404.html', nf)):
        check('https://cyberdudeuk.github.io/ai-capability-governance/#' in text and 'tool-triage' in text, f'L6 {name} lacks the old toolkit redirect')
    # L7: every issue form linked exists.
    for t in sorted(set(re.findall(r'issues/new\?template=([\w.-]+\.yml)', s + nf + readme))):
        check((root / '.github' / 'ISSUE_TEMPLATE' / t).exists(), f'L7 linked issue form {t} does not exist')
    # L8: README is organised by level and its local links resolve.
    check(all(f'## {x}' in readme for x in LEVELS), 'L8 README lacks a Beginner, Intermediate or Advanced section')
    for link in re.findall(r'\]\((?!https?:|#)([^)#\s]+)', readme):
        check((root / link).exists(), f'L8 README links to {link}, which does not exist')
    # L9: the workflow inventory matches the files; L10: publishing checks first and pins every action.
    wf = {x.name for x in (root / '.github' / 'workflows').glob('*.y*ml')}
    check(wf == EXPECTED_WORKFLOWS, f'L9 workflows differ from the inventory: {sorted(wf ^ EXPECTED_WORKFLOWS)}')
    pw = root / '.github' / 'workflows' / 'pages.yml'
    if pw.exists():
        t = pw.read_text(encoding='utf-8')
        for u in re.findall(r'uses:\s*(\S+)', t):
            check(re.search(r'@[0-9a-f]{40}$', u) is not None, f'L10 pages.yml action not pinned to a full commit: {u}')
        check('path: _site' in t and 'python tools/check_site.py' in t, 'L10 pages.yml must check first and publish only _site')
    # L12 (D-04): a step that creates the virtual environment and installs into it in the same step installs into the
    # system Python, because a GITHUB_PATH change only applies from the next step; later steps then miss the packages.
    for w in sorted((root / '.github' / 'workflows').glob('*.y*ml')):
        for step in re.split(r'\n\s*- ', w.read_text(encoding='utf-8')):
            check(not ('-m venv' in step and 'pip install' in step), f'L12 {w.name}: a step creates the venv and installs into it; split them')
    # L13 (D-05): sequential Dependabot merges left two pins for the same package, so pip refused to install anything.
    names = [re.split(r'[=<>~!\[ ]', l.strip())[0].lower() for l in (root / 'requirements.txt').read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    check(len(names) == len(set(names)), f'L13 requirements.txt pins a package more than once: {sorted({n for n in names if names.count(n) > 1})}')
    # L14 (D-05): the same merges left pages.yml with two copies of the configure and upload steps.
    for w in sorted((root / '.github' / 'workflows').glob('*.y*ml')):
        for job in re.split(r'\n  [\w-]+:\n', w.read_text(encoding='utf-8')):
            uses = re.findall(r'uses:\s*([^@\s]+)@', job)
            dup = sorted({u for u in uses if uses.count(u) > 1})
            check(not dup, f'L14 {w.name}: the same action is used twice in one job: {dup}')
    # L15 (D-06): the contact form's project list still named the BHM 2026 Hub after the project was renamed, and lacked
    # the new Amplify portal. Every project must be selectable on the form, by its current name.
    cf = root / '.github' / 'ISSUE_TEMPLATE' / 'contact.yml'
    form = cf.read_text(encoding='utf-8') if cf.exists() else ''  # a missing form is reported by L7
    for p in (d['projects'] if form else []):
        check(f'- {p["name"]}' in form, f'L15 contact form does not list {p["name"]}')
    # L16: no third-party requests (the footer promises none). Tags match in any case (D-14). Stylesheets, scripts, images, fonts and CSS urls must be local.
    css = (root / 'styles.css').read_text(encoding='utf-8')
    for name, text in (('index.html', s), ('404.html', nf)):
        for tag in re.findall(r'<(?:link|script|img|source|iframe)\b[^>]*>', text, re.I):
            for u in re.findall(r'(?:src|href)\s*=\s*["\']([^"\']+)', tag, re.I):
                check(not re.match(r'(https?:)?//', u, re.I) or 'rel="canonical"' in tag.lower(), f'L16 {name} loads a third-party resource: {u}')
    for u in re.findall(r'url\(\s*["\']?([^"\')]+)', css):
        check(not re.match(r'(https?:)?//', u), f'L16 styles.css loads a third-party resource: {u}')
    # L17: the workshop lists work that is not public yet. Nothing in it may link anywhere (a private workspace link would
    # leak or break), every item is complete and on the page, and none repeats a public project.
    wpath = root / 'data' / 'workshop.json'
    wraw = wpath.read_text(encoding='utf-8') if wpath.exists() else ''
    check(bool(wraw), 'L17 data/workshop.json is missing')
    if wraw:
        w = json.loads(wraw)
        check(not re.search(r'https?:|claude\.ai|www\.', wraw), 'L17 workshop.json contains a link; workshop items must not link anywhere')
        check('not yet public' in w.get('status', ''), 'L17 workshop status must say the work is not yet public')
        wids = [i.get('id') for i in w.get('items', [])]
        check(len(wids) == len(set(wids)), 'L17 duplicate workshop ids')
        names = {p['name'].lower() for p in d['projects']}
        for i in w.get('items', []):
            for f in ('id', 'name', 'area', 'icon', 'summary'):
                check(bool(i.get(f)), f'L17 workshop item {i.get("id", "?")} missing {f}')
            check(i.get('name', '').lower() not in names, f'L17 workshop item {i.get("name")} is already a public project')
            check(f'id="w-{i.get("id")}"' in s, f'L17 workshop item {i.get("id")} is not on the page')
    # L18: the headline numbers and the status chart are the data's numbers, not typed by hand.
    cats_used = {p['category'] for p in d['projects']}
    want = [len(d['projects']), sum(1 for p in d['projects'] if p.get('site')), len(cats_used), len(json.loads(wraw)['items']) if wraw else -1]
    got = [int(x) for x in re.findall(r'class="num" data-count="(\d+)">(?:\d+)<', s)]
    check(got == want, f'L18 headline numbers {got} do not match the data {want}')
    kinds = [int(x) for x in re.findall(r'<strong data-kind="\w+">(\d+)</strong>', s)]
    check(sum(kinds) == len(d['projects']), f'L18 status chart counts {sum(kinds)} projects, the data has {len(d["projects"])}')
    # L19: every coverage map cell holds the number of projects in that area at that level.
    for c in cats_used:
        for lvl in sorted(LEVELS):
            n = sum(1 for p in d['projects'] if p['category'] == c and lvl in p['levels'])
            m = re.search(r'aria-label="[^"]*, ' + lvl + r': (\d+) project', s[s.find(f'<tr class="c-{c}"'):])
            check(m is not None and int(m.group(1)) == n, f'L19 coverage cell {c}/{lvl} should be {n}')
    # L20: the typeface is self-hosted with its licence, and the share image exists at 1200x630.
    for u in re.findall(r'url\("?(fonts/[^")]+)', css):
        check((root / u).exists(), f'L20 font file {u} is missing')
    check((root / 'fonts' / 'OFL.txt').exists(), 'L20 fonts/OFL.txt (the typeface licence) is missing')
    og = root / 'og.jpg'
    if og.exists():
        b = og.read_bytes()
        size = None
        i = 2
        while i < len(b) - 9:
            if b[i] == 0xFF and b[i + 1] in (0xC0, 0xC2):
                size = (int.from_bytes(b[i + 7:i + 9], 'big'), int.from_bytes(b[i + 5:i + 7], 'big'))
                break
            i += 2 + int.from_bytes(b[i + 2:i + 4], 'big') if b[i] == 0xFF else 1
        check(size == (1200, 630), f'L20 og.jpg is {size}, not 1200x630: run python3 tools/og.py')
    else:
        check(False, 'L20 og.jpg is missing: run python3 tools/og.py')
    # L21 (D-12): every local file the page uses is copied into the published site. The publish step copies a fixed list,
    # so a new font or image passed every check here and would still have been missing from the live site.
    if pw.exists():
        m = re.search(r'cp -r ([^\n]+?) _site/', pw.read_text(encoding='utf-8'))
        shipped = set(m.group(1).split()) if m else set()
        refs = set()
        for text in (s, nf):
            for tag in re.findall(r'<(?:link|script|img|source)\b[^>]*>', text, re.I):
                refs.update(re.findall(r'(?:src|href)="(?!https?:|//|data:|#|/)([^"?#]+)', tag, re.I))
            refs.update(re.findall(r'<a [^>]*href="(?!https?:|//|#|/)([^"?#]+)"', text))
            refs.update(re.findall(r'content="https://cyberdudeuk\.github\.io/([^"/]+\.(?:jpg|png))"', text))
        refs.update(re.findall(r'url\("?(?!https?:|data:)([^")]+)', css))
        for r in sorted(refs):
            check(r.split('/')[0] in shipped, f'L21 {r} is used by the page but pages.yml does not publish it')
    # L22 (D-15): the stylesheet and script are linked with a fingerprint of their current contents, so a changed file
    # gets a new address and no browser pairs the new page with an old cached copy.
    import hashlib
    for name, text in (('index.html', s), ('404.html', nf)):
        for f in ('styles.css', 'app.js') if name == 'index.html' else ('styles.css',):
            want = hashlib.sha256((root / f).read_bytes()).hexdigest()[:10]
            check(re.search(re.escape(f) + r'\?v=' + want + '"', text) is not None, f'L22 {name} does not link {f} with its current fingerprint: run python3 tools/build.py')
    # L23 (D-17): every project card carries its own generated signature, drawn without cropping, and every section
    # heading has its icon; the portal's name comes from data/owner.json.
    for p in d['projects']:
        check(f'data-sig="{p["id"]}"' in s, f'L23 {p["id"]} has no signature art on its card')
    check('preserveAspectRatio="xMidYMid slice"' not in s.split('<main')[1], 'L23 signature art is cropped (slice); use meet')
    main = s[s.find('<main'):s.find('</main>')]
    for hid, h in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', main):
        check('class="h-ico"' in h or hid == 'h-featured', f'L23 section heading {hid} has no icon')
    owner = json.loads((root / 'data' / 'owner.json').read_text(encoding='utf-8'))
    if owner.get('site_name'):
        check(f'<title>{htmllib.escape(owner["site_name"])}' in s, 'L23 the page title does not start with site_name from data/owner.json')
    # L24: every public profile in data/owner.json is linked from the page with rel="me" and named in schema.org sameAs,
    # so the launchpad, GitHub, DEV, ORCID and LinkedIn point at each other (D-24).
    ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    same_as = json.loads(ld.group(1)).get('creator', {}).get('sameAs', []) if ld else []
    for p in owner.get('profiles', []):
        check(f'<a rel="me" href="{htmllib.escape(p["url"])}">' in s, f'L24 profile {p["name"]} is not linked from the page with rel="me"')
        check(p['url'] in same_as, f'L24 profile {p["name"]} is not in the page\'s schema.org sameAs')
    # L11: the licence names its holder in full (D-01: it read "Copyright (c) 2026 Em").
    lic = (root / 'LICENSE').read_text(encoding='utf-8')
    m = re.search(r'Copyright \(c\) \d{4} (.+)', lic)
    check(m is not None and len(m.group(1).strip()) >= 4, 'L11 LICENSE copyright holder is missing or cut off')
    return out


def main(argv=None):
    root = (argv or sys.argv[1:] or ['.'])[0]
    p = problems(root)
    n = len(json.loads((Path(root) / 'data' / 'projects.json').read_text(encoding='utf-8'))['projects'])
    print('FAIL\n' + '\n'.join(p) if p else f'PASS: 23 checks, {n} projects')
    return 1 if p else 0


if __name__ == '__main__':
    sys.exit(main())
