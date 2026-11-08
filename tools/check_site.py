#!/usr/bin/env python3
"""Static checks for the launchpad. Each names the defect or risk it guards against (docs/defect-register.md);
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

EXPECTED_WORKFLOWS = {'pages.yml', 'checks.yml', 'discover.yml', 'triage.yml', 'digest.yml', 'labels.yml', 'codeql.yml', 'scorecard.yml', 'dependency-review.yml'}
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
    # L11: the licence names its holder in full (D-01: it read "Copyright (c) 2026 Em").
    lic = (root / 'LICENSE').read_text(encoding='utf-8')
    m = re.search(r'Copyright \(c\) \d{4} (.+)', lic)
    check(m is not None and len(m.group(1).strip()) >= 4, 'L11 LICENSE copyright holder is missing or cut off')
    return out


def main(argv=None):
    root = (argv or sys.argv[1:] or ['.'])[0]
    p = problems(root)
    n = len(json.loads((Path(root) / 'data' / 'projects.json').read_text(encoding='utf-8'))['projects'])
    print('FAIL\n' + '\n'.join(p) if p else f'PASS: 14 checks, {n} projects')
    return 1 if p else 0


if __name__ == '__main__':
    sys.exit(main())
