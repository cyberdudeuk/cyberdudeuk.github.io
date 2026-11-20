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
import build  # noqa: E402
import notes  # noqa: E402
import discover  # noqa: E402

FILES = ['requirements.txt', 'index.html', '404.html', 'app.js', 'styles.css', 'README.md', 'LICENSE', 'CHANGELOG.md', 'ACCESSIBILITY.md', 'SECURITY.md',
         'CONTRIBUTING.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md', 'CITATION.cff', 'data', 'tools', '.github', 'docs', 'ops', 'fonts', 'og.jpg', 'notes', 'feed.xml']


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

    def test_L25_note_missing_from_feed(self):
        # D-25: a note written here but missing from the feed never reaches the sites that import it.
        self.edit('feed.xml', '<id>https://cyberdudeuk.github.io/notes/one-home-for-my-open-work.html</id>', '<id>gone</id>')
        self.fails_with('L25')

    def test_L25_note_published_elsewhere_must_stay_out_of_the_feed(self):
        self.edit('feed.xml', '</feed>', '<entry><id>https://dev.to/cyberdudeuk/making-a-portfolio-of-open-public-sector-projects-that-keeps-itself-honest-3l4a</id></entry></feed>')
        self.fails_with('L25')

    def test_L25_note_page_missing(self):
        (self.tmp / 'notes' / 'one-home-for-my-open-work.html').unlink()
        self.fails_with('L25')

    def test_L25_note_page_not_its_own_canonical(self):
        self.edit('notes/one-home-for-my-open-work.html', '<link rel="canonical" href="https://cyberdudeuk.github.io/notes/', '<link rel="canonical" href="https://dev.to/x/')
        self.fails_with('L25')

    def test_L25_feed_not_published(self):
        self.edit('.github/workflows/pages.yml', ' notes feed.xml ', ' ')
        self.fails_with('L25')

    def test_L25_build_refuses_unsafe_notes(self):
        # Fail closed: bad ids, unknown block types (no HTML), off-list or http links, and notes that are both
        # published here and elsewhere are refused before anything is written.
        good = {'id': 'ok', 'title': 'T', 'summary': 'S', 'date': '2026-11-19', 'body': [{'p': 'x'}]}
        bad = [dict(good, id='Bad Id'), dict(good, body=[{'script': 'x'}]), dict(good, body=[{'p': {'html': 1}}]),
               dict(good, date='19/11/2026'), dict(good, home='https://dev.to/x'),
               {k: v for k, v in good.items() if k != 'body'} | {'home': 'http://dev.to/x'},
               {k: v for k, v in good.items() if k != 'body'} | {'home': 'https://evil.example/x'},
               dict(good, links=[{'text': 'x', 'url': 'javascript:alert(1)'}])]
        for n in bad:
            (self.tmp / 'data' / 'posts.json').write_text(json.dumps({'posts': [n]}), encoding='utf-8')
            with self.assertRaises((SystemExit, ValueError), msg=n):
                notes.load(self.tmp)

    def test_L25_note_text_is_escaped(self):
        n = {'id': 'x', 'title': '<b>T</b>', 'summary': 'S', 'date': '2026-11-19', 'body': [{'p': '<script>alert(1)</script>'}]}
        html_out = notes.body_html(n) + notes.cards('https://cyberdudeuk.github.io/', [n])
        self.assertNotIn('<script>', html_out)
        self.assertNotIn('<b>T</b>', html_out)

    def test_L25_summary_repeated_in_body(self):
        # D-27: the note page showed its summary, then the same sentence again as the first paragraph.
        def repeat(d):
            d['posts'][0]['body'].insert(0, {'p': d['posts'][0]['summary']})
        p = self.tmp / 'data' / 'posts.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        repeat(d)
        p.write_text(json.dumps(d), encoding='utf-8')
        self.fails_with('L25')

    def test_stories_need_evidence_and_consent(self):
        # D-28: a case study is published only with a source, evidence anyone can open and the date of consent.
        good = {'id': 's1', 'project': 'dq-commons', 'who': 'A team', 'what': 'Used it.', 'outcome': 'It helped.',
                'evidence': 'https://example.gov.uk/x', 'consent': '2026-11-19'}
        ids = {'dq-commons'}
        p = self.tmp / 'data' / 'stories.json'
        p.write_text(json.dumps({'stories': [good]}), encoding='utf-8')
        self.assertEqual(len(notes.load_stories(self.tmp, ids)), 1)
        for bad in (dict(good, evidence=''), dict(good, evidence='http://x.gov.uk'), {k: v for k, v in good.items() if k != 'consent'},
                    dict(good, project='nope'), dict(good, outcome=''), dict(good, id='Bad Id')):
            p.write_text(json.dumps({'stories': [bad]}), encoding='utf-8')
            with self.assertRaises((SystemExit, ValueError), msg=bad):
                notes.load_stories(self.tmp, ids)

    def test_note_names_only_listed_projects(self):
        p = self.tmp / 'data' / 'posts.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        d['posts'][0]['projects'] = ['not-a-project']
        p.write_text(json.dumps(d), encoding='utf-8')
        with self.assertRaises(SystemExit):
            notes.load(self.tmp, {'dq-commons'})

    def test_L24_profile_link_missing(self):
        # D-24: a public profile listed in owner.json but not linked from the page breaks the cross-links.
        self.edit('index.html', '<a rel="me" href="https://dev.to/cyberdudeuk">', '<a href="https://dev.to/cyberdudeuk">')
        self.fails_with('L24')

    def test_L24_profile_missing_from_same_as(self):
        self.edit('index.html', '"https://dev.to/cyberdudeuk"', '"https://dev.to/someone-else"')
        self.fails_with('L24')

    def test_L24_build_refuses_unsafe_profile_link(self):
        # Fail closed: only https links to known hosts reach the page.
        for bad in ('javascript:alert(1)', 'http://dev.to/cyberdudeuk', 'https://evil.example/cyberdudeuk'):
            with self.assertRaises(SystemExit):
                build.profiles({'profiles': [{'name': 'X', 'url': bad}]})

    def test_L26_board_missing_from_gateway(self):
        # D-29: the project board and the notes were not reachable from the top of the page.
        self.edit('index.html', '<li><a class="door" href="https://github.com/users/cyberdudeuk/projects/4">', '<li><a class="door" href="#about">')
        self.fails_with('L26')

    def test_L26_notes_missing_from_gateway(self):
        self.edit('index.html', '<a class="door" href="#notes">', '<a class="door" href="#about">')
        self.fails_with('L26')

    def test_L26_no_board_in_owner_file(self):
        p = self.tmp / 'data' / 'owner.json'
        d = json.loads(p.read_text(encoding='utf-8'))
        d.pop('board')
        p.write_text(json.dumps(d), encoding='utf-8')
        self.fails_with('L26')

    def test_L26_feedback_form_missing(self):
        # D-29: the page offered only the contact form, while each project offers ideas, bugs and accessibility forms.
        self.edit('index.html', 'issues/new?template=idea.yml', 'issues/new?template=contact.yml')
        self.fails_with('L26')

    def test_L26_spotlight_without_note_slide(self):
        self.edit('index.html', 'id="s-note"', 'id="s-other"')
        self.fails_with('L26')

    def test_L26_build_refuses_unsafe_board_link(self):
        # Fail closed: only a GitHub Projects address reaches the page.
        for bad in ('javascript:alert(1)', 'http://github.com/users/cyberdudeuk/projects/4', 'https://evil.example/users/x/projects/4',
                    'https://github.com/users/cyberdudeuk/projects/4?x=1', 'https://github.com/cyberdudeuk'):
            with self.assertRaises(SystemExit):
                build.board({'board': {'name': 'Board', 'url': bad}})
        self.assertIsNone(build.board({}))

    def test_L27_footer_back_to_ogl(self):
        # D-30: the footer put the launchpad's own text under OGL v3.0, which fits Crown copyright, not personal work.
        self.edit('index.html', 'text <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.', 'text OGL v3.0.')
        self.fails_with('L27')

    def test_L27_readme_disagrees(self):
        self.edit('README.md', '| Text | [CC BY 4.0]', '| Text | [CC BY-SA 4.0]')
        self.fails_with('L27')

    def test_L1_email(self):
        self.edit('index.html', '<p><strong>Disclaimer.</strong>', '<p>someone@example.gov.uk <strong>Disclaimer.</strong>')
        self.fails_with('L1')

    def test_L2_page_edited_by_hand(self):
        self.edit('index.html', 'data and AI in public services</h1>', 'Hand-edited</h1>')
        self.fails_with('L2')

    def test_L3_incomplete_project(self):
        self.data(lambda d: d['projects'][0].pop('summary'))
        self.fails_with('L3')

    def test_L3_no_site_and_no_how(self):
        # D-20: the break makes its own case (no site, no "how"), so it holds when every project has a live site.
        def no_site_no_how(d):
            d['projects'][5]['site'] = ''
            d['projects'][5].pop('how', None)
        self.data(no_site_no_how)
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

    def test_L16_third_party_font(self):
        self.edit('index.html', '<link rel="stylesheet" href="styles.css?v=', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter&v=')
        self.fails_with('L16')

    def test_L16_upper_case_tag_cannot_slip_past(self):
        self.edit('404.html', '</head>', '<SCRIPT SRC="https://example.com/x.js"></SCRIPT></head>')
        self.fails_with('L16')

    def test_L16_third_party_css_url(self):
        self.edit('styles.css', 'url("fonts/space-grotesk-latin-wght.woff2")', 'url("https://example.com/font.woff2")')
        self.fails_with('L16')

    def test_L17_workshop_link(self):
        self.edit('data/workshop.json', '"name": "govukOS",', '"name": "govukOS", "url": "https://claude.ai/artifact/x",')
        self.fails_with('L17')

    def test_L17_workshop_repeats_a_project(self):
        self.edit('data/workshop.json', '"name": "govukOS",', '"name": "Plainspoken",')
        self.fails_with('L17')

    def test_L18_headline_number_typed_by_hand(self):
        # D-19: the anchor is read from the data, not typed, so a project gaining a site cannot break the vaccine.
        live = sum(1 for p in json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))['projects'] if p.get('site'))
        self.edit('index.html', f'class="num" data-count="{live}">{live}<', f'class="num" data-count="{live + 1}">{live + 1}<')
        self.fails_with('L18')

    def test_L19_coverage_cell_wrong(self):
        # D-34: the count is read from the data, so listing a new data project cannot break this vaccine (as D-19, D-20).
        n = sum(1 for p in json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))['projects']
                if p['category'] == 'data' and 'Beginner' in p['levels'])
        self.edit('index.html', f'Data management and quality, Beginner: {n} projects', f'Data management and quality, Beginner: {n + 1} projects')
        self.fails_with('L19')

    def test_L20_share_image_missing(self):
        (self.tmp / 'og.jpg').unlink()
        self.fails_with('L20')

    def test_L20_font_missing(self):
        (self.tmp / 'fonts' / 'space-grotesk-latin-wght.woff2').unlink()
        self.fails_with('L20')

    def test_L21_asset_not_published(self):
        self.edit('.github/workflows/pages.yml', 'data fonts og.jpg .nojekyll', 'data .nojekyll')
        self.fails_with('L21')

    def test_L22_stylesheet_changed_without_rebuild(self):
        p = self.tmp / 'styles.css'
        p.write_text(p.read_text(encoding='utf-8') + '\n/* changed */\n', encoding='utf-8')
        self.fails_with('L22')

    def test_L22_no_fingerprint(self):
        t = (self.tmp / 'index.html').read_text(encoding='utf-8')
        import re
        (self.tmp / 'index.html').write_text(re.sub(r'app\.js\?v=\w+', 'app.js', t), encoding='utf-8')
        self.fails_with('L22')

    def test_L23_card_without_signature(self):
        self.edit('index.html', 'data-sig="plainspoken"', 'data-sig="nothing"')
        self.fails_with('L23')

    def test_L23_heading_without_icon(self):
        self.edit('index.html', '<h2 id="h-coverage"><span class="h-ico"', '<h2 id="h-coverage"><span class="h-none"')
        self.fails_with('L23')

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

    def test_too_few_topics_flagged(self):
        # D-26: a listed repository with fewer than three topics is hard to find on GitHub.
        f = discover.findings([repo('alpha', topics=['one'])], self.DATA)
        self.assertTrue(any('GitHub topic' in x for x in f), f)
        self.assertEqual(discover.findings([repo('alpha', topics=['a', 'b', 'c'])], self.DATA), [])

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

    def test_bot_only_push_is_not_flagged(self):
        # D-07: a Dependabot merge after the card's date is not a change to the project.
        f = discover.findings([repo('alpha', pushed='2026-11-07T00:00:00Z')], self.DATA, last_change=lambda n: '2026-11-04')
        self.assertEqual(f, [])

    def test_negative_card_missing_live_site_or_licence_is_flagged(self):
        # D-19: the card said no site and no licence while the repository had both.
        stale = {'projects': [dict(self.DATA['projects'][0], site='', licence='No licence stated')], 'excluded': {}}
        r = repo('alpha', has_pages=True, homepage='https://cyberdudeuk.github.io/alpha/', license={'spdx_id': 'MIT'})
        f = discover.findings([r], stale)
        self.assertTrue(any('has a site at https://cyberdudeuk.github.io/alpha/' in x for x in f))
        self.assertTrue(any('is licensed MIT' in x for x in f))

    def test_card_matching_repository_facts_is_not_flagged(self):
        ok = {'projects': [dict(self.DATA['projects'][0], site='https://cyberdudeuk.github.io/alpha/', licence='MIT')], 'excluded': {}}
        r = repo('alpha', has_pages=True, homepage='https://cyberdudeuk.github.io/alpha/', license={'spdx_id': 'MIT'})
        self.assertEqual(discover.findings([r], ok), [])
        # NOASSERTION is GitHub's "a licence file it cannot classify": not proof of a licence, so not flagged.
        unclear = {'projects': [dict(self.DATA['projects'][0], licence='No licence stated')], 'excluded': {}}
        self.assertEqual(discover.findings([repo('alpha', license={'spdx_id': 'NOASSERTION'})], unclear), [])

    def test_negative_change_by_person_is_flagged(self):
        f = discover.findings([repo('alpha', pushed='2026-11-07T00:00:00Z')], self.DATA, last_change=lambda n: '2026-11-06')
        self.assertTrue(any('updated on 2026-11-06' in x for x in f))


class LicenceDrift(unittest.TestCase):
    """D-22: the dq-commons card said OGL v3.0 content after the project moved to CC BY 4.0, and the catalogue card said
    MIT only while its content is OGL v3.0. The GitHub API names the code licence only, so neither was seen."""
    CARD = {'name': 'Alpha', 'repo': 'https://github.com/cyberdudeuk/alpha', 'updated': '2026-11-05', 'licence': 'MIT code, OGL v3.0 content'}

    def test_card_text_maps_to_spdx(self):
        self.assertEqual(discover.card_licences('MIT code, CC BY 4.0 content'), {'MIT', 'CC-BY-4.0'})
        self.assertEqual(discover.card_licences('Apache 2.0'), {'Apache-2.0'})

    def test_matching_licences_are_not_flagged(self):
        self.assertEqual(discover.fact_drift(repo('alpha'), self.CARD, {'MIT', 'OGL-UK-3.0'}), [])
        self.assertEqual(discover.fact_drift(repo('alpha'), self.CARD, None), [])  # no publiccode.yml: nothing to compare

    def test_negative_content_licence_drift_is_flagged(self):
        f = discover.fact_drift(repo('alpha'), self.CARD, {'MIT', 'CC-BY-4.0'})
        self.assertTrue(any('CC-BY-4.0 AND MIT in publiccode.yml' in x for x in f))
        f = discover.fact_drift(repo('alpha'), dict(self.CARD, licence='MIT'), {'MIT', 'OGL-UK-3.0'})
        self.assertTrue(any("its card says 'MIT'" in x for x in f))

    def test_findings_use_the_licence_lookup(self):
        data = {'projects': [self.CARD], 'excluded': {}}
        self.assertTrue(discover.findings([repo('alpha')], data, licences=lambda n: {'MIT', 'CC-BY-4.0'}))
        self.assertEqual(discover.findings([repo('alpha')], data, licences=lambda n: {'MIT', 'OGL-UK-3.0'}), [])


class Propose(unittest.TestCase):
    """Tier 2 discovery (18 Nov 2026): the owner asked for new repositories to reach the launchpad and profile without
    retyping them. The routine drafts; a person merges. These pin what it may and may not do to the list."""
    DATA = {'updated': '2026-11-05', 'projects': [{'id': 'alpha', 'name': 'Alpha', 'repo': 'https://github.com/cyberdudeuk/alpha',
                                                   'updated': '2026-11-05', 'summary': 'Written by a person.'}],
            'excluded': {'repos': ['w3id.org (fork)']}}

    def test_new_repository_gets_a_complete_honest_draft(self):
        r = repo('beta-tool', description='Does beta things.', license={'spdx_id': 'MIT'}, topics=['data', 'uk'], created_at='2026-11-10T00:00:00Z')
        new, changes = discover.propose([repo('alpha'), r], self.DATA, last_change=lambda n: '2026-11-12' if n == 'beta-tool' else None)
        card = new['projects'][-1]
        self.assertEqual((card['id'], card['summary'], card['licence'], card['updated']), ('beta-tool', 'Does beta things.', 'MIT', '2026-11-12'))
        for f in check_site.FIELDS:  # passes the launchpad's own completeness rule (L3)
            self.assertTrue(card.get(f), f)
        self.assertEqual(build.kind(card['status']), 'exp')  # status maps to a known kind, so the page builds
        self.assertIn('owner', card['audience'])           # what the repository does not say is labelled, not invented
        self.assertTrue(card.get('how'))                     # no site, so it says how to use it
        self.assertTrue(any('beta-tool' in c for c in changes))

    def test_negative_never_removes_or_rewords_a_card(self):
        new, _ = discover.propose([], self.DATA)              # alpha's repository is gone
        self.assertEqual(new['projects'], self.DATA['projects'])
        new, _ = discover.propose([repo('alpha')], self.DATA, last_change=lambda n: '2026-11-09')
        self.assertEqual(new['projects'][0]['summary'], 'Written by a person.')

    def test_negative_only_a_change_by_a_person_moves_the_date(self):
        new, changes = discover.propose([repo('alpha', pushed='2026-11-09T00:00:00Z')], self.DATA, last_change=lambda n: '2026-11-04')
        self.assertEqual((new['projects'][0]['updated'], changes), ('2026-11-05', []))  # bot-only push (D-07)
        new, changes = discover.propose([repo('alpha', pushed='2026-11-09T00:00:00Z')], self.DATA, last_change=lambda n: '2026-11-09')
        self.assertEqual(new['projects'][0]['updated'], '2026-11-09')
        self.assertEqual(new['updated'], '2026-11-09')

    def test_negative_forks_private_archived_excluded_and_self_get_no_card(self):
        repos = [repo('x', fork=True), repo('y', private=True), repo('z', archived=True), repo('w3id.org'), repo('cyberdudeuk.github.io')]
        new, changes = discover.propose(repos, self.DATA)
        self.assertEqual((len(new['projects']), changes), (1, []))

    def test_does_not_change_the_data_it_was_given(self):
        before = json.dumps(self.DATA, sort_keys=True)
        discover.propose([repo('gamma')], self.DATA)
        self.assertEqual(json.dumps(self.DATA, sort_keys=True), before)

    def test_workflow_proposes_on_its_own_branch_and_honours_the_kill_switch(self):
        wf = (ROOT / '.github' / 'workflows' / 'discover.yml').read_text(encoding='utf-8')
        self.assertIn('discover.py --propose', wf)
        self.assertIn('AUTOMATION: ${{ vars.AUTOMATION }}', wf)
        src = (ROOT / 'tools' / 'discover.py').read_text(encoding='utf-8')
        self.assertIn("os.environ.get('AUTOMATION') != 'off'", src)
        self.assertNotIn("'main'", src.split('def push_proposal')[1].split('def main')[0])  # never pushes main


if __name__ == '__main__':
    unittest.main()
