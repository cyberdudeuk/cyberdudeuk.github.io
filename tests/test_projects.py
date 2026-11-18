"""The projects routine (tools/projects_sync.py): what it writes to the GitHub Project, tested against a fake GraphQL
service so no network or token is needed. Every rule has a deliberate break.

The owner's request of 18 November 2026: every project on GitHub's Projects feature, fleshed out from each repository's
activity and kept up to date.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import projects_sync as ps  # noqa: E402

DATA = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))
AREAS = {c['id']: c['label'] for c in DATA['categories']}
ACT = {'last_change': '2026-11-17', 'recent': ['Add publiccode.yml', 'Fix a link'], 'release': 'v1.2.0 (2026-11-06)',
       'open_issues': 3, 'open_pulls': 1}


class FakeGraphQL:
    """Enough of GitHub's Projects API to record what the routine asks for."""

    # D-23: every new GitHub Project already has these built-in fields. "Status" offers only Todo, In progress and Done,
    # and "Repository" is a repository-type field that updateProjectV2ItemFieldValue refuses.
    BUILT_IN = {'Title': [], 'Assignees': [], 'Status': ['Todo', 'In progress', 'Done'], 'Labels': [], 'Linked pull requests': [],
                'Milestone': [], 'Repository': [], 'Reviewers': [], 'Parent issue': [], 'Sub-issues progress': []}

    def __init__(self, project=True, items=()):
        self.calls, self.items = [], {t: {'id': f'I{n}', 'content': {'id': f'D{n}', 'title': t}} for n, t in enumerate(items)}
        self.fields = {n: {'id': f'B-{n}', 'name': n, 'options': [{'id': f'O-{o}', 'name': o} for o in opts]} for n, opts in self.BUILT_IN.items()}
        self.has_project = project
        self.values = []

    def __call__(self, query, v):
        self.calls.append((query.split('(')[0].split('{')[0].strip() + ' ' + query.split('{')[1].split('(')[0], v))
        if 'user(login' in query:
            return {'user': {'id': 'U1', 'projectsV2': {'nodes': [{'id': 'P1', 'number': 1, 'title': ps.TITLE}] if self.has_project else []}}}
        if 'createProjectV2(' in query:
            self.has_project = True
            return {'createProjectV2': {'projectV2': {'id': 'P1'}}}
        if 'fields(first' in query:
            return {'node': {'fields': {'nodes': list(self.fields.values())}}}
        if 'createProjectV2Field' in query:
            f = {'id': f"F-{v['n']}", 'name': v['n'], 'options': [{'id': f"O-{o['name']}", 'name': o['name']} for o in (v['o'] or [])]}
            self.fields[v['n']] = f
            return {'createProjectV2Field': {'projectV2Field': f}}
        if 'items(first' in query:
            return {'node': {'items': {'nodes': list(self.items.values())}}}
        if 'addProjectV2DraftIssue' in query:
            return {'addProjectV2DraftIssue': {'projectItem': {'id': 'NEW'}}}
        if 'updateProjectV2ItemFieldValue' in query:
            if v['f'] == 'B-Repository':
                raise SystemExit('GraphQL failed: The field of type repository is currently not supported.')
            self.values.append((v['f'], v['v']))
        return {}

    def named(self, op):
        return [v for q, v in self.calls if q.split(' ')[-1] == op]


class ItemContent(unittest.TestCase):
    def test_every_launchpad_project_becomes_a_complete_item(self):
        for card in DATA['projects']:
            with self.subTest(project=card['id']):
                item = ps.item_for(card, AREAS, ACT)
                self.assertEqual(item['title'], card['name'])
                self.assertIn(card['summary'], item['body'])
                self.assertIn(card['repo'], item['body'])
                self.assertEqual(set(item['fields']), set(ps.FIELDS))
                options = ps.wanted_options(DATA)
                self.assertIn(item['fields']['Project status'], options['Project status'])  # groups exactly as the launchpad does
                self.assertIn(item['fields']['Area'], options['Area'])

    def test_activity_from_the_repository_is_shown(self):
        item = ps.item_for(DATA['projects'][0], AREAS, ACT)
        self.assertIn('- Add publiccode.yml', item['body'])
        self.assertEqual((item['fields']['Last change'], item['fields']['Open issues'], item['fields']['Latest release']),
                         ('2026-11-17', 3, 'v1.2.0 (2026-11-06)'))

    def test_negative_no_activity_falls_back_to_the_card_date_and_says_so(self):
        item = ps.item_for(DATA['projects'][0], AREAS, dict(ACT, last_change=None, recent=[]))
        self.assertEqual(item['fields']['Last change'], DATA['projects'][0]['updated'])
        self.assertIn('No changes by a person', item['body'])

    def test_activity_counts_pull_requests_apart_from_issues_and_ignores_bots(self):
        commit = lambda login, msg, d: {'author': {'login': login}, 'commit': {'author': {'name': login}, 'message': msg, 'committer': {'date': d}}}
        pages = {'repos/cyberdudeuk/x': {'open_issues_count': 5},
                 'repos/cyberdudeuk/x/pulls?state=open&per_page=100': [{}, {}],
                 'repos/cyberdudeuk/x/releases/latest': {'tag_name': 'v2', 'published_at': '2026-11-01T00:00:00Z'},
                 'repos/cyberdudeuk/x/commits?per_page=50': [commit('dependabot[bot]', 'Bump', '2026-11-18T00:00:00Z'),
                                                             commit('cyberdudeuk', 'Real change\n\nbody', '2026-11-16T00:00:00Z')]}
        a = ps.activity('x', get=pages.get)
        self.assertEqual((a['open_issues'], a['open_pulls'], a['last_change'], a['recent'], a['release']),
                         (3, 2, '2026-11-16', ['Real change'], 'v2 (2026-11-01)'))


class BoardWrites(unittest.TestCase):
    def test_creates_the_project_fields_and_one_item_per_project(self):
        fake = FakeGraphQL(project=False)
        items = ps.sync(ps.Board(fake, log=lambda m: None), DATA, lambda n: ACT)
        self.assertEqual(len(fake.named('createProjectV2')), 1)
        self.assertEqual({v['n'] for v in fake.named('createProjectV2Field')}, set(ps.FIELDS))
        self.assertEqual(len(fake.named('addProjectV2DraftIssue')), len(DATA['projects']))
        self.assertEqual(len(items), len(DATA['projects']))

    def test_negative_built_in_fields_are_never_written_and_every_value_lands(self):
        # D-23: the first real run stopped on the built-in Repository field, and every status was refused by the
        # built-in Status field's options. Each item's values must land in fields the routine created.
        fake = FakeGraphQL(project=False)
        logged = []
        ps.sync(ps.Board(fake, log=logged.append), DATA, lambda n: ACT)
        self.assertFalse(set(ps.FIELDS) & set(FakeGraphQL.BUILT_IN), 'a field name clashes with a built-in field')
        self.assertTrue(set(FakeGraphQL.BUILT_IN) <= ps.BUILT_IN, 'the routine must know every built-in the fake models')
        self.assertFalse([f for f, _ in fake.values if f.startswith('B-')], 'wrote to a built-in field')
        self.assertEqual(len(fake.values), len(DATA['projects']) * len(ps.FIELDS))
        self.assertFalse([m for m in logged if 'is not an option' in m])

    def test_existing_items_are_updated_not_duplicated(self):
        fake = FakeGraphQL(items=[DATA['projects'][0]['name']])
        ps.sync(ps.Board(fake, log=lambda m: None), DATA, lambda n: ACT)
        self.assertEqual(len(fake.named('updateProjectV2DraftIssue')), 1)
        self.assertEqual(len(fake.named('addProjectV2DraftIssue')), len(DATA['projects']) - 1)

    def test_negative_never_deletes_an_item(self):
        logged = []
        fake = FakeGraphQL(items=['Something the owner added'])
        ps.sync(ps.Board(fake, log=logged.append), DATA, lambda n: ACT)
        self.assertFalse([q for q, _ in fake.calls if 'delete' in q.lower()])
        self.assertTrue(any('never deletes' in m for m in logged))

    def test_negative_dry_run_writes_nothing(self):
        for fake in (FakeGraphQL(project=False), FakeGraphQL(items=[p['name'] for p in DATA['projects']])):  # empty and full boards
            fake.fields = {n: {'id': f'F-{n}', 'name': n, 'options': []} for n in ps.FIELDS}
            ps.sync(ps.Board(fake, dry_run=True, log=lambda m: None), DATA, lambda n: ACT)
            self.assertFalse([q for q, _ in fake.calls if q.startswith('mutation')])

    def test_routine_is_declared_and_honours_the_kill_switch(self):
        wf = (ROOT / '.github' / 'workflows' / 'projects.yml').read_text(encoding='utf-8')
        self.assertIn('AUTOMATION: ${{ vars.AUTOMATION }}', wf)
        self.assertIn('PROJECTS_TOKEN: ${{ secrets.PROJECTS_TOKEN }}', wf)
        self.assertIn("os.environ.get('AUTOMATION') == 'off'", (ROOT / 'tools' / 'projects_sync.py').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
