#!/usr/bin/env python3
"""Projects board routine (tier 1, ops/automation.yaml): keeps the owner's GitHub Project "Public Good Works" in step
with the launchpad and with what is happening in each repository.

One draft item per launchpad project. Its fields hold the status and area from the launchpad card, and the activity
read from the repository: the date of the last change by a person, the latest release, open issues and open pull
requests. Its body holds the card's summary and links, plus the last few changes by a person (commit subjects). The
routine adds items and refreshes them; it never deletes an item or a field, so anything the owner adds is kept.

GitHub's Projects API is GraphQL only and the workflow token cannot reach a user's project, so it needs a classic
personal access token with the "project" scope in the repository secret PROJECTS_TOKEN. Without it, the routine says
so and stops. Honours the AUTOMATION kill switch: set to "off", it reports what it would change and changes nothing.

Run: python3 tools/projects_sync.py            (needs GH_TOKEN for reading repositories, PROJECTS_TOKEN for the board)
     python3 tools/projects_sync.py --dry-run  (prints the items it would write, changes nothing)
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402  (status kinds, so the board groups exactly as the launchpad does)
import discover  # noqa: E402  (the same "last change by a person" rule, D-07)

OWNER = 'cyberdudeuk'
TITLE = 'Public Good Works'
SHORT = 'Every public cyberdudeuk project, kept in step with the launchpad and each repository by a daily routine.'
FIELDS = {'Status': 'SINGLE_SELECT', 'Area': 'SINGLE_SELECT', 'Last change': 'DATE', 'Latest release': 'TEXT',
          'Open issues': 'NUMBER', 'Open pull requests': 'NUMBER', 'Licence': 'TEXT', 'Site': 'TEXT', 'Repository': 'TEXT'}
RECENT = 5


def gh_json(path):
    r = subprocess.run(['gh', 'api', path], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None


def activity(name, get=gh_json):
    """What the repository shows about its own activity, read through the REST API with the workflow token."""
    repo = get(f'repos/{OWNER}/{name}') or {}
    pulls = get(f'repos/{OWNER}/{name}/pulls?state=open&per_page=100') or []
    rel = get(f'repos/{OWNER}/{name}/releases/latest') or {}
    commits = get(f'repos/{OWNER}/{name}/commits?per_page=50') or []
    by_people = [c for c in commits if (c.get('author') or {}).get('login') not in discover.BOTS
                 and c['commit']['author']['name'] not in discover.BOTS]
    return {'last_change': by_people[0]['commit']['committer']['date'][:10] if by_people else None,
            'recent': [c['commit']['message'].splitlines()[0][:120] for c in by_people[:RECENT]],
            'release': f"{rel['tag_name']} ({rel['published_at'][:10]})" if rel.get('tag_name') else 'No release yet',
            'open_issues': max(0, (repo.get('open_issues_count') or 0) - len(pulls)),  # the API counts pull requests as issues
            'open_pulls': len(pulls)}


def item_for(card, areas, act):
    """The draft item for one project: title, body and field values. Pure, so it is tested without the network."""
    kind = build.kind(card['status'])
    links = [f"- Repository: {card['repo']}"] + ([f"- Site: {card['site']}"] if card.get('site') else [])
    recent = '\n'.join(f'- {m}' for m in act['recent']) or '- No changes by a person in the last 50 commits.'
    body = (f"{card['summary']}\n\n**For:** {card['audience']}\n**Status, as the project states it:** {card['status']}\n\n"
            + '\n'.join(links) + f"\n\n### Recent changes by a person\n{recent}\n\n"
            "_Kept up to date daily by the projects routine in cyberdudeuk/cyberdudeuk.github.io. Edits here are overwritten; "
            "change the launchpad card or the repository instead._")
    fields = {'Status': dict(build.KINDS)[kind], 'Area': areas.get(card['category'], card['category']),
              'Latest release': act['release'], 'Open issues': act['open_issues'], 'Open pull requests': act['open_pulls'],
              'Licence': card['licence'], 'Site': card.get('site') or 'None', 'Repository': card['repo']}
    if act['last_change'] or card.get('updated'):
        fields['Last change'] = act['last_change'] or card['updated']
    return {'title': card['name'], 'body': body, 'fields': fields}


def wanted_options(data):
    return {'Status': [label for _, label in build.KINDS], 'Area': [c['label'] for c in data['categories']]}


class Board:
    """The GitHub Project, reached through GraphQL. gql(query, variables) returns the "data" object."""

    def __init__(self, gql, dry_run=False, log=print):
        self.gql, self.dry, self.log = gql, dry_run, log

    def project(self, options):
        user = self.gql('query($l:String!){user(login:$l){id projectsV2(first:50){nodes{id number title}}}}', {'l': OWNER})['user']
        found = next((p for p in user['projectsV2']['nodes'] if p['title'] == TITLE), None)
        if found:
            return found['id']
        self.log(f'Creating the project "{TITLE}"')
        if self.dry:
            return None
        pid = self.gql('mutation($o:ID!,$t:String!){createProjectV2(input:{ownerId:$o,title:$t}){projectV2{id}}}',
                       {'o': user['id'], 't': TITLE})['createProjectV2']['projectV2']['id']
        self.gql('mutation($p:ID!,$s:String!){updateProjectV2(input:{projectId:$p,shortDescription:$s,public:true}){projectV2{id}}}',
                 {'p': pid, 's': SHORT})
        return pid

    def fields(self, pid, options):
        q = ('query($p:ID!){node(id:$p){... on ProjectV2{fields(first:50){nodes{... on ProjectV2FieldCommon{id name}'
             ' ... on ProjectV2SingleSelectField{options{id name}}}}}}}')
        have = {f['name']: f for f in self.gql(q, {'p': pid})['node']['fields']['nodes'] if f}
        for name, kind in FIELDS.items():
            if name in have:
                continue
            self.log(f'Adding the field "{name}"')
            if self.dry:
                continue
            opts = [{'name': o, 'color': 'GRAY', 'description': ''} for o in options.get(name, [])]
            m = ('mutation($p:ID!,$n:String!,$k:ProjectV2CustomFieldType!,$o:[ProjectV2SingleSelectFieldOptionInput!]){'
                 'createProjectV2Field(input:{projectId:$p,name:$n,dataType:$k,singleSelectOptions:$o}){'
                 'projectV2Field{... on ProjectV2FieldCommon{id name} ... on ProjectV2SingleSelectField{options{id name}}}}}')
            have[name] = self.gql(m, {'p': pid, 'n': name, 'k': kind, 'o': opts or None})['createProjectV2Field']['projectV2Field']
        return have

    def items(self, pid):
        q = 'query($p:ID!){node(id:$p){... on ProjectV2{items(first:100){nodes{id content{... on DraftIssue{id title}}}}}}}'
        return {n['content']['title']: n for n in self.gql(q, {'p': pid})['node']['items']['nodes'] if n.get('content')}

    def upsert(self, pid, fields, existing, item):
        if item['title'] in existing:
            node = existing[item['title']]
            if not self.dry:
                self.gql('mutation($d:ID!,$t:String!,$b:String!){updateProjectV2DraftIssue(input:{draftIssueId:$d,title:$t,body:$b}){draftIssue{id}}}',
                         {'d': node['content']['id'], 't': item['title'], 'b': item['body']})
            item_id = node['id']
        else:
            self.log(f'Adding the item "{item["title"]}"')
            if self.dry:
                return
            item_id = self.gql('mutation($p:ID!,$t:String!,$b:String!){addProjectV2DraftIssue(input:{projectId:$p,title:$t,body:$b}){projectItem{id}}}',
                               {'p': pid, 't': item['title'], 'b': item['body']})['addProjectV2DraftIssue']['projectItem']['id']
        for name, value in item['fields'].items():
            f = fields.get(name)
            if not f or self.dry:
                continue
            if FIELDS[name] == 'SINGLE_SELECT':
                opt = next((o['id'] for o in f.get('options', []) if o['name'] == value), None)
                if not opt:
                    self.log(f'"{value}" is not an option of "{name}": add it in the board settings')
                    continue
                v = {'singleSelectOptionId': opt}
            else:
                v = {{'DATE': 'date', 'NUMBER': 'number', 'TEXT': 'text'}[FIELDS[name]]: value}
            self.gql('mutation($p:ID!,$i:ID!,$f:ID!,$v:ProjectV2FieldValue!){updateProjectV2ItemFieldValue(input:'
                     '{projectId:$p,itemId:$i,fieldId:$f,value:$v}){projectV2Item{id}}}', {'p': pid, 'i': item_id, 'f': f['id'], 'v': v})


def sync(board, data, act_for):
    options = wanted_options(data)
    areas = {c['id']: c['label'] for c in data['categories']}
    pid = board.project(options)
    fields = board.fields(pid, options) if pid else {}
    existing = board.items(pid) if pid else {}
    items = [item_for(card, areas, act_for(card['repo'].rstrip('/').split('/')[-1])) for card in data['projects']]
    for item in items:
        if pid:
            board.upsert(pid, fields, existing, item)
    for title in sorted(set(existing) - {i['title'] for i in items}):
        board.log(f'"{title}" is on the board but not on the launchpad: left as it is (the routine never deletes)')
    return items


def gql_with(token):
    def gql(query, variables):
        payload = {'query': query, 'variables': variables}  # sent on stdin, so values are never parsed by a shell
        r = subprocess.run(['gh', 'api', 'graphql', '--input', '-'], input=json.dumps(payload), capture_output=True, text=True,
                           env=dict(os.environ, GH_TOKEN=token))
        out = json.loads(r.stdout or '{}')
        if r.returncode or out.get('errors'):
            raise SystemExit(f"GraphQL failed: {out.get('errors') or r.stderr.strip()[:300]}")
        return out['data']
    return gql


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(argv)
    data = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))
    off = os.environ.get('AUTOMATION') == 'off'
    token = os.environ.get('PROJECTS_TOKEN', '')
    if not token and not a.dry_run:
        print('::warning::PROJECTS_TOKEN is not set, so the Projects board was not updated. Add a classic personal access '
              'token with the "project" scope as the repository secret PROJECTS_TOKEN.')
        return 0
    dry = a.dry_run or off
    if off:
        print('Kill switch is off: reporting only, changing nothing.')
    if not token:
        for item in [item_for(c, {x['id']: x['label'] for x in data['categories']}, activity(c['repo'].rstrip('/').split('/')[-1]))
                     for c in data['projects']]:
            print(json.dumps(item, indent=1, ensure_ascii=False))
        return 0
    sync(Board(gql_with(token), dry_run=dry), data, activity)
    return 0


if __name__ == '__main__':
    sys.exit(main())
