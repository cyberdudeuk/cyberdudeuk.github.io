"""Vaccination tests: every launchpad check passes on the real site and fails on a deliberate break; discovery behaves.

Run: python -m unittest discover -s tests
"""
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import check_site  # noqa: E402
import discover  # noqa: E402

FILES = ['requirements.txt', 'index.html', '404.html', 'app.js', 'styles.css', 'README.md', 'LICENSE', 'CHANGELOG.md', 'ACCESSIBILITY.md', 'SECURITY.md',
         'CONTRIBUTING.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md', 'CITATION.cff', 'data', 'tools', '.github', 'docs', 'ops']


class Site(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        for f in FILES:
            src = ROOT / f
            if src.is_dir():
                shutil.copytree(src, self.tmp / f, ignore=shutil.ignore_patterns('__pycache__'))
            elif src.exists():
                shutil.copy(src, self.tmp / f)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, name, old, new):
        p = self.tmp / name
        t = p.read_text(encoding='utf-8')
        self.assertIn(old, t, f'vaccine anchor missing in {name}: {old[:50]}')
        p.write_text(t.replace(old, new, 1), encoding='utf-8')

    def data(self, change):
        p = self.tmp / 'data' / 'projects.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        change(d)
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')

    def fails_with(self, code):
        found = check_site.problems(self.tmp)
        self.assertTrue(any(x.startswith(code) for x in found), f'{code} did not fail: {found}')

    def test_the_real_site_passes(self):
        self.assertEqual(check_site.problems(ROOT), [])

    def test_L1_email(self):
        self.edit('index.html', '<p><strong>Disclaimer.</strong>', '<p>someone@example.gov.uk <strong>Disclaimer.</strong>')
        self.fails_with('L1')

    def test_L2_page_edited_by_hand(self):
        self.edit('index.html', 'Projects for better public services</h1>', 'Hand-edited</h1>')
        self.fails_with('L2')

    def test_L3_incomplete_project(self):
        self.data(lambda d: d['projects'][0].pop('summary'))
        self.fails_with('L3')

    def test_L3_no_site_and_no_how(self):
        self.data(lambda d: d['projects'][5].pop('how'))
        self.fails_with('L3')

    def test_L5_bad_starting_point(self):
        self.data(lambda d: d['ways_in']['Advanced'].append('plainspoken'))
        self.fails_with('L5')

    def test_L6_redirect_removed(self):
        self.edit('404.html', 'tool-triage', 'tool-nothing')
        self.fails_with('L6')

    def test_L7_missing_issue_form(self):
        (self.tmp / '.github' / 'ISSUE_TEMPLATE' / 'contact.yml').unlink()
        self.fails_with('L7')

    def test_L8_readme_dead_link(self):
        (self.tmp / 'CHANGELOG.md').unlink()
        self.fails_with('L8')

    def test_L9_unlisted_workflow(self):
        (self.tmp / '.github' / 'workflows' / 'extra.yml').write_text('name: x\n', encoding='utf-8')
        self.fails_with('L9')

    def test_L10_unpinned_action(self):
        # Matches whatever commit the action is pinned to, so a Dependabot update does not break the test (D-05).
        import re
        p = self.tmp / '.github' / 'workflows' / 'pages.yml'
        t, n = re.subn(r'actions/deploy-pages@[0-9a-f]{40}', 'actions/deploy-pages@v5', p.read_text(encoding='utf-8'))
        self.assertEqual(n, 1)
        p.write_text(t, encoding='utf-8')
        self.fails_with('L10')

    def test_L13_duplicate_pin(self):
        p = self.tmp / 'requirements.txt'
        shutil.copy(ROOT / 'requirements.txt', p)
        p.write_text(p.read_text(encoding='utf-8') + 'PyYAML==6.0.2\n', encoding='utf-8')
        self.fails_with('L13')

    def test_L14_duplicate_step(self):
        import re
        p = self.tmp / '.github' / 'workflows' / 'pages.yml'
        t = p.read_text(encoding='utf-8')
        line = re.search(r'      - uses: actions/configure-pages@[^\n]+\n', t).group(0)
        p.write_text(t.replace(line, line + line, 1), encoding='utf-8')
        self.fails_with('L14')

    def test_L15_contact_form_out_of_step(self):
        self.edit('.github/ISSUE_TEMPLATE/contact.yml', '        - Black History and Heritage Hub\n', '        - BHM 2026 Hub\n')
        self.fails_with('L15')

    def test_L11_truncated_licence(self):
        self.edit('LICENSE', 'Copyright (c) 2026 cyberdudeuk and contributors', 'Copyright (c) 2026 Em')
        self.fails_with('L11')


class VenvStep(unittest.TestCase):
    setUp, tearDown, edit, fails_with = Site.setUp, Site.tearDown, Site.edit, Site.fails_with

    def test_L12_install_in_venv_step(self):
        self.edit('.github/workflows/checks.yml', 'echo "$RUNNER_TEMP/venv/bin" >> "$GITHUB_PATH"\n      - name: Install pinned tools into the environment\n        run: pip install -r requirements.txt',
                  'echo "$RUNNER_TEMP/venv/bin" >> "$GITHUB_PATH"\n          pip install -r requirements.txt')
        self.fails_with('L12')


def repo(name, pushed='2026-11-01T00:00:00Z', **kw):
    return dict({'name': name, 'html_url': f'https://github.com/cyberdudeuk/{name}', 'pushed_at': pushed, 'fork': False, 'private': False, 'archived': False}, **kw)


class Discover(unittest.TestCase):
    DATA = {'projects': [{'name': 'Alpha', 'repo': 'https://github.com/cyberdudeuk/alpha', 'updated': '2026-11-05'}],
            'excluded': {'repos': ['w3id.org (fork)']}}

    def test_nothing_to_do(self):
        self.assertEqual(discover.findings([repo('alpha'), repo('cyberdudeuk.github.io')], self.DATA), [])

    def test_negative_new_repo_found(self):
        f = discover.findings([repo('alpha'), repo('beta')], self.DATA)
        self.assertTrue(any('New public repository' in x and 'beta' in x for x in f))

    def test_negative_forks_private_and_excluded_are_ignored(self):
        f = discover.findings([repo('alpha'), repo('x', fork=True), repo('y', private=True), repo('w3id.org')], self.DATA)
        self.assertEqual(f, [])

    def test_negative_stale_card_and_gone_repo(self):
        self.assertTrue(any('its card says' in x for x in discover.findings([repo('alpha', pushed='2026-11-07T00:00:00Z')], self.DATA)))
        self.assertTrue(any('no public repository' in x for x in discover.findings([], self.DATA)))


if __name__ == '__main__':
    unittest.main()
