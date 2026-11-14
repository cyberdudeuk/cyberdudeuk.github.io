#!/usr/bin/env python3
"""Discovery (tier 0 routine, ops/automation.yaml): keeps the launchpad a gateway to every project, present and future.

Compares the account's public, non-fork repositories with data/projects.json and reports:
- a public repository that is not listed (a new project to add),
- a listed project whose repository has gone (archived, private or deleted),
- a listed project whose repository has a change by a person since its card's "updated" date (the card may be stale).
  Pushes made only by bots (Dependabot, GitHub Actions) do not count: they would flag every card every week (D-07).
It opens or updates one issue labelled routine. It never edits the list: a person adds or changes projects.

Run: python3 tools/discover.py            (needs GH_TOKEN; opens or updates the issue)
     python3 tools/discover.py --dry-run  (prints findings, changes nothing)
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNER = 'cyberdudeuk'
SELF = f'{OWNER}.github.io'
TITLE = 'Launchpad: projects to add or update'


def load():
    return json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))


def public_repos():
    r = subprocess.run(['gh', 'api', '--paginate', '--slurp', f'users/{OWNER}/repos?type=owner&per_page=100'],
                       check=True, capture_output=True, text=True)
    return [x for page in json.loads(r.stdout or '[]') for x in page]


BOTS = {'dependabot[bot]', 'github-actions[bot]'}


def last_change_by_person(name):
    """Date (YYYY-MM-DD) of the newest commit on the default branch not made by a bot, or None if none in the last 100."""
    r = subprocess.run(['gh', 'api', f'repos/{OWNER}/{name}/commits?per_page=100'], capture_output=True, text=True)
    if r.returncode:
        return None
    for c in json.loads(r.stdout or '[]'):
        if (c.get('author') or {}).get('login') not in BOTS and c['commit']['author']['name'] not in BOTS:
            return c['commit']['committer']['date'][:10]
    return None


def findings(repos, data, last_change=None):
    """Plain-English findings. repos: GitHub API repository objects; data: projects.json.
    last_change(name) gives the date of the last change by a person; without it, the push date is used."""
    listed = {p['repo'].rstrip('/').split('/')[-1].lower(): p for p in data['projects']}
    excluded = {x.split(' ')[0].lower() for x in data.get('excluded', {}).get('repos', [])}
    live = {r['name'].lower(): r for r in repos if not r.get('fork') and not r.get('private') and not r.get('archived')}
    out = []
    for name, r in sorted(live.items()):
        if name == SELF.lower() or name in excluded:
            continue
        if name not in listed:
            out.append(f"New public repository not on the launchpad: {r['name']} ({r['html_url']})")
        elif r.get('pushed_at', '')[:10] > listed[name]['updated']:
            when = last_change(r['name']) if last_change else r['pushed_at'][:10]
            if when and when > listed[name]['updated']:
                out.append(f"{r['name']} was updated on {when}; its card says {listed[name]['updated']}")
    for name, p in sorted(listed.items()):
        if name not in live:
            out.append(f"Listed project {p['name']} has no public repository any more ({p['repo']})")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(argv)
    found = findings(public_repos(), load(), last_change_by_person)
    body = ('Found by the discovery routine (tier 0, ops/automation.yaml). It changes nothing: a person updates '
            '`data/projects.json`, runs `python3 tools/build.py` and opens a pull request.\n\n' +
            ('\n'.join(f'- {f}' for f in found) or 'Nothing to do.'))
    print(body)
    if a.dry_run or not found:
        return 0
    repo = os.environ.get('GITHUB_REPOSITORY', f'{OWNER}/{SELF}')
    existing = subprocess.run(['gh', 'issue', 'list', '-R', repo, '--label', 'routine', '--state', 'open', '--search', TITLE,
                               '--json', 'number', '-q', '.[0].number'], capture_output=True, text=True).stdout.strip()
    if existing:
        subprocess.run(['gh', 'issue', 'comment', existing, '-R', repo, '--body', body], check=True)
    else:
        subprocess.run(['gh', 'issue', 'create', '-R', repo, '--title', TITLE, '--label', 'routine', '--body', body], check=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
