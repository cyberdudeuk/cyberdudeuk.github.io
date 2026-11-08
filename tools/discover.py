#!/usr/bin/env python3
"""Discovery (tier 0 routine, ops/automation.yaml): keeps the launchpad a gateway to every project, present and future.

Compares the account's public, non-fork repositories with data/projects.json and reports:
- a public repository that is not listed (a new project to add),
- a listed project whose repository has gone (archived, private or deleted),
- a listed project whose repository has been pushed since its card's "updated" date (the card may be stale).
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


def findings(repos, data):
    """Plain-English findings. repos: GitHub API repository objects; data: projects.json."""
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
            out.append(f"{r['name']} was updated on {r['pushed_at'][:10]}; its card says {listed[name]['updated']}")
    for name, p in sorted(listed.items()):
        if name not in live:
            out.append(f"Listed project {p['name']} has no public repository any more ({p['repo']})")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args(argv)
    found = findings(public_repos(), load())
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
