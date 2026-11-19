"""The projects routine (tools/projects_sync.py): what it writes to the GitHub Project, tested against a fake GraphQL
service so no network or token is needed. Every rule has a deliberate break.

The owner's request of 18 November 2026: every project on GitHub's Projects feature, fleshed out from each repository's
activity and kept up to date. And of 19 November 2026: each item's Status set from that activity, with regular project
status updates (D-29).
"""
from datetime import date
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
       'open_issues': 3, 'open_pulls': 1, 'week': 4, 'month': 9, 'has_release': True}
TODAY = date(2026, 11, 19)


class FakeGraphQL:
    """Enough of GitHub's Projects API to record what the routine asks for."""

    # D-23: every new GitHub Project already has these built-in fields. "Status" offers only Todo, In progress and Done,
    # and "Repository" is a repository-type field that updateProjectV2ItemFieldValue refuses. D-29: the owner's board
    # spells the middle option "In Progress", so the fake does too and the routine must match it regardless of case.
    BUILT_IN = {'Title': [], 'Assignees': [], 'Status': ['Todo', 'In Progress', 'Done'], 'Labels': [], 'Linked pull requests': [],
                'Milestone': [], 'Repository': [], 'Reviewers': [], 'Parent issue': [], 'Sub-issues progress': []}

    def __init__(self, project=True, items=(), last_update=None):
        self.calls, self.items = [], {t: {'id': f'I{n}', 'content': {'id': f'D{n}', 'title': t}} for n, t in enumerate(items)}
        self.fields = {n: {'id': f'B-{n}', 'name': n, 'options': [{'id': f'O-{o}', 'name': o} for o in opts]} for n, opts in self.BUILT_IN.items()}
        self.has_project = project
        self.values = []
        self.last_update = last_update  # createdAt of the newest status update, or None for a board with none

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
        if 'statusUpdates(' in query:
            return {'node': {'statusUpdates': {'nodes': [{'createdAt': self.last_update}] if self.last_update else []}}}
        if 'createProjectV2StatusUpdate' in query:
            if v['s'] not in {'INACTIVE', 'ON_TRACK', 'AT_RISK', 'OFF_TRACK', 'COMPLETE'}:
                raise SystemExit(f"GraphQL failed: {v['s']} is not a ProjectV2StatusUpdateStatus")
            return {'createProjectV2StatusUpdate': {'statusUpdate': {'id': 'SU1'}}}
        if 'updateProjectV2ItemFieldValue' in query:
            if v['f'] == 'B-Repository':
                raise SystemExit('GraphQL failed: The field of type repository is currently not supported.')
            if v['f'] == 'B-Status' and v['v'].get('singleSelectOptionId') not in {o['id'] for o in self.fields['Status']['options']}:
                raise SystemExit('GraphQL failed: not an option of Status')
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
        self.assertFalse([f for f, _ in fake.values if f.startswith('B-') and f != 'B-Status'], 'wrote to a built-in field')
        self.assertEqual(len([f for f, _ in fake.values if not f.startswith('B-')]), len(DATA['projects']) * len(ps.FIELDS))
        self.assertEqual(len([f for f, _ in fake.values if f == 'B-Status']), len(DATA['projects']))  # D-29
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

    def test_status_is_set_from_activity_with_the_boards_own_option(self):
        # D-29: the board says "In Progress"; the routine says "In progress". Matched without regard to case.
        fake = FakeGraphQL(items=[p['name'] for p in DATA['projects']])
        ps.sync(ps.Board(fake, log=lambda m: None), DATA, lambda n: ACT, today=TODAY)
        self.assertEqual({v['singleSelectOptionId'] for f, v in fake.values if f == 'B-Status'}, {'O-In Progress'})

    def test_negative_unknown_status_option_is_logged_not_written(self):
        fake = FakeGraphQL(items=[DATA['projects'][0]['name']])
        fake.fields['Status']['options'] = [{'id': 'O-Backlog', 'name': 'Backlog'}]
        logged = []
        ps.sync(ps.Board(fake, log=logged.append), DATA, lambda n: ACT, today=TODAY)
        self.assertFalse([f for f, _ in fake.values if f == 'B-Status'])
        self.assertTrue(any('not an option of the built-in Status' in m for m in logged))

    def test_status_update_is_posted_when_none_is_recent(self):
        for last in (None, '2026-11-12T08:00:00Z'):  # a board with no update, and one with an update 7 days old
            with self.subTest(last=last):
                fake = FakeGraphQL(items=[p['name'] for p in DATA['projects']], last_update=last)
                ps.sync(ps.Board(fake, log=lambda m: None), DATA, lambda n: ACT, today=TODAY)
                posted = fake.named('createProjectV2StatusUpdate')
                self.assertEqual(len(posted), 1)
                self.assertEqual((posted[0]['s'], posted[0]['d']), ('ON_TRACK', '2026-11-19'))
                for card in DATA['projects']:
                    self.assertIn(f"| {card['name']} | In progress |", posted[0]['b'])

    def test_negative_status_update_is_not_repeated_within_the_week(self):
        fake = FakeGraphQL(items=[p['name'] for p in DATA['projects']], last_update='2026-11-13T08:00:00Z')  # 6 days old
        ps.sync(ps.Board(fake, log=lambda m: None), DATA, lambda n: ACT, today=TODAY)
        self.assertFalse(fake.named('createProjectV2StatusUpdate'))
        self.assertFalse([q for q, _ in fake.calls if 'delete' in q.lower() or 'updateProjectV2StatusUpdate' in q])

    def test_negative_dry_run_posts_no_status_update(self):
        fake = FakeGraphQL(items=[p['name'] for p in DATA['projects']])
        ps.sync(ps.Board(fake, dry_run=True, log=lambda m: None), DATA, lambda n: ACT, today=TODAY)
        self.assertFalse(fake.named('createProjectV2StatusUpdate'))


class StatusRules(unittest.TestCase):
    CARD = DATA['projects'][0]

    def test_board_status_from_activity(self):
        cases = [('2026-11-18', True, 'In progress'), ('2026-10-21', False, 'In progress'),  # 29 days: still active
                 ('2026-10-20', True, 'Done'), ('2026-10-20', False, 'Todo'), (None, False, 'Todo'), (None, True, 'Done')]
        for last, rel, want in cases:
            with self.subTest(last=last, release=rel):
                self.assertEqual(ps.board_status(self.CARD, dict(ACT, last_change=last, has_release=rel), TODAY), want)
                self.assertIn(want, ps.STATUS_OPTIONS)

    def test_overall_health(self):
        item = lambda s: {'title': 'x', 'status': s, 'act': ACT}
        self.assertEqual(ps.status_update_for([item('In progress'), item('Done')], TODAY)['status'], 'ON_TRACK')
        self.assertEqual(ps.status_update_for([item('In progress'), item('Todo')], TODAY)['status'], 'AT_RISK')
        self.assertEqual(ps.status_update_for([item('Done'), item('Todo')], TODAY)['status'], 'INACTIVE')

    def test_activity_counts_changes_by_people_in_the_week_and_month(self):
        commit = lambda login, d: {'author': {'login': login}, 'commit': {'author': {'name': login}, 'message': 'm', 'committer': {'date': d}}}
        commits = [commit('cyberdudeuk', '2026-11-18T09:00:00Z'), commit('dependabot[bot]', '2026-11-18T09:00:00Z'),
                   commit('cyberdudeuk', '2026-11-12T09:00:00Z'), commit('cyberdudeuk', '2026-10-01T09:00:00Z')]
        pages = {'repos/cyberdudeuk/x': {}, 'repos/cyberdudeuk/x/commits?per_page=50': commits}
        a = ps.activity('x', get=pages.get, today=TODAY)
        self.assertEqual((a['week'], a['month'], a['has_release']), (1, 2, False))  # the bot and the 49-day-old change excluded

    def test_use_is_measured_not_only_activity(self):
        # D-31: stars and forks come from the repository and reach the item fields, body and weekly table.
        pages = {'repos/cyberdudeuk/x': {'stargazers_count': 7, 'forks_count': 2}, 'repos/cyberdudeuk/x/commits?per_page=50': []}
        a = ps.activity('x', get=pages.get, today=TODAY)
        self.assertEqual((a['stars'], a['forks']), (7, 2))
        item = ps.item_for(self.CARD, AREAS, dict(ACT, stars=7, forks=2), TODAY)
        self.assertEqual((item['fields']['Stars'], item['fields']['Forks']), (7, 2))
        self.assertIn('Stars: 7. Forks: 2.', item['body'])
        self.assertIn('| 7 | 2 |', ps.status_update_for([dict(item, title='x')], TODAY)['body'])

    def test_negative_missing_counts_are_zero_not_an_error(self):
        a = ps.activity('x', get={'repos/cyberdudeuk/x': {}}.get, today=TODAY)
        self.assertEqual((a['stars'], a['forks']), (0, 0))

    def test_body_says_how_busy_the_project_is(self):
        body = ps.item_for(self.CARD, AREAS, ACT, TODAY)['body']
        self.assertIn('4 changes by a person in the last 7 days, 9 in the last 30 days.', body)
        quiet = ps.item_for(self.CARD, AREAS, dict(ACT, week=0, month=0), TODAY)['body']
        self.assertIn('Quiet: no changes by a person in the last 30 days.', quiet)

    def test_routine_is_declared_and_honours_the_kill_switch(self):
        wf = (ROOT / '.github' / 'workflows' / 'projects.yml').read_text(encoding='utf-8')
        self.assertIn('AUTOMATION: ${{ vars.AUTOMATION }}', wf)
        self.assertIn('PROJECTS_TOKEN: ${{ secrets.PROJECTS_TOKEN }}', wf)
        self.assertIn("os.environ.get('AUTOMATION') == 'off'", (ROOT / 'tools' / 'projects_sync.py').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
