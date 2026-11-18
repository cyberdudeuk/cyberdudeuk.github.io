#!/usr/bin/env python3
"""Discovery (tier 0 routine, ops/automation.yaml): keeps the launchpad a gateway to every project, present and future.

Compares the account's public, non-fork repositories with data/projects.json and reports:
- a public repository that is not listed (a new project to add),
- a listed project whose repository has gone (archived, private or deleted),
- a listed project whose repository has a change by a person since its card's "updated" date (the card may be stale).
  Pushes made only by bots (Dependabot, GitHub Actions) do not count: they would flag every card every week (D-07).
It opens or updates one issue labelled routine. With --propose (tier 2) it also prepares the change on the
routine/discover branch: a draft card for each new repository, drafted only from what the repository states, and the
date of the last change by a person on each listed card. It never changes main and never removes or rewords a card:
a person reviews the branch and merges it.

Run: python3 tools/discover.py            (needs GH_TOKEN; opens or updates the issue)
     python3 tools/discover.py --propose  (also pushes the proposal branch; honours the AUTOMATION kill switch)
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


CARD_SPDX = {'MIT': 'MIT', 'OGL v3.0': 'OGL-UK-3.0', 'CC BY 4.0': 'CC-BY-4.0', 'Apache 2.0': 'Apache-2.0',
             'PolyForm Noncommercial': 'PolyForm-Noncommercial-1.0.0'}


def card_licences(text):
    """The SPDX identifiers a card's licence text names, e.g. 'MIT code, OGL v3.0 content' -> {'MIT', 'OGL-UK-3.0'}."""
    return {spdx for words, spdx in CARD_SPDX.items() if words.lower() in text.lower()}


def publiccode_licences(name):
    """The SPDX identifiers in the repository's own publiccode.yml (legal.license), or None if it has none (D-22)."""
    r = subprocess.run(['gh', 'api', f'repos/{OWNER}/{name}/contents/publiccode.yml', '-H', 'Accept: application/vnd.github.raw'],
                       capture_output=True, text=True)
    if r.returncode:
        return None
    for line in r.stdout.splitlines():
        if line.strip().startswith('license:'):
            return {x.strip() for x in line.split(':', 1)[1].replace("'", '').split(' AND ') if x.strip()}
    return None


def fact_drift(r, card, stated_licences=None):
    """Facts the repository itself states that the card contradicts (D-19). Dates alone missed these: the card for
    ndl-pubsec-mcp kept 'no published site' and 'No licence stated' while its Pages site was live and its licence MIT."""
    out = []
    home = (r.get('homepage') or '').strip()
    if r.get('has_pages') and home and not card.get('site'):
        out.append(f"{r['name']} has a site at {home}; its card lists none")
    spdx = ((r.get('license') or {}).get('spdx_id') or '')
    if spdx and spdx != 'NOASSERTION' and 'no licence' in card.get('licence', '').lower():
        out.append(f"{r['name']} is licensed {spdx}; its card says {card['licence']!r}")
    # D-22: the GitHub API names only the code licence, so a card wrong about the content licence went unseen.
    if stated_licences and card_licences(card.get('licence', '')) != stated_licences:
        out.append(f"{r['name']} states its licences as {' AND '.join(sorted(stated_licences))} in publiccode.yml; "
                   f"its card says {card['licence']!r}")
    return out


def findings(repos, data, last_change=None, licences=None):
    """Plain-English findings. repos: GitHub API repository objects; data: projects.json.
    last_change(name) gives the date of the last change by a person; without it, the push date is used.
    licences(name) gives the licences the repository states in its publiccode.yml, or None."""
    listed = {p['repo'].rstrip('/').split('/')[-1].lower(): p for p in data['projects']}
    excluded = {x.split(' ')[0].lower() for x in data.get('excluded', {}).get('repos', [])}
    live = {r['name'].lower(): r for r in repos if not r.get('fork') and not r.get('private') and not r.get('archived')}
    out = []
    for name, r in sorted(live.items()):
        if name == SELF.lower() or name in excluded:
            continue
        if name not in listed:
            out.append(f"New public repository not on the launchpad: {r['name']} ({r['html_url']})")
        else:
            out.extend(fact_drift(r, listed[name], licences(r['name']) if licences else None))
            if r.get('pushed_at', '')[:10] > listed[name]['updated']:
                when = last_change(r['name']) if last_change else r['pushed_at'][:10]
                if when and when > listed[name]['updated']:
                    out.append(f"{r['name']} was updated on {when}; its card says {listed[name]['updated']}")
    for name, p in sorted(listed.items()):
        if name not in live:
            out.append(f"Listed project {p['name']} has no public repository any more ({p['repo']})")
    return out


PROPOSAL_BRANCH = 'routine/discover'
DRAFT_STATUS = 'Experiment: new, not yet reviewed'
DRAFT_AUDIENCE = 'To be confirmed by the owner'


def draft_card(r, updated):
    """A card for a new repository, drafted only from what the repository states about itself. Nothing is invented:
    what the repository does not say is labelled for the owner to fill in before merging."""
    name = r['name']
    spdx = ((r.get('license') or {}).get('spdx_id') or '')
    home = (r.get('homepage') or '').strip()
    site = home if r.get('has_pages') and home.startswith('https://cyberdudeuk.github.io/') else ''
    card = {'id': name.lower(), 'name': name.replace('-', ' ').strip().capitalize(), 'category': 'experiments',
            'status': DRAFT_STATUS, 'since': (r.get('created_at') or updated)[:4], 'updated': updated,
            'summary': (r.get('description') or '').strip() or 'No description yet: drafted from the repository, to be written.',
            'audience': DRAFT_AUDIENCE, 'levels': ['Beginner'], 'site': site, 'repo': r['html_url'],
            'licence': spdx if spdx and spdx != 'NOASSERTION' else 'No licence stated', 'new': True,
            'highlights': list(r.get('topics') or [])[:4]}
    if not site:
        card['how'] = 'See the repository README.'
    return card


def propose(repos, data, last_change=None):
    """The change the owner is asked to approve (tier 2): a draft card for each new public repository and the date of
    the last change by a person on each listed card. It never removes or rewords a card. Returns (data, changes)."""
    new = json.loads(json.dumps(data))
    listed = {p['repo'].rstrip('/').split('/')[-1].lower(): p for p in new['projects']}
    excluded = {x.split(' ')[0].lower() for x in new.get('excluded', {}).get('repos', [])}
    changes = []
    for r in sorted(repos, key=lambda x: x['name'].lower()):
        name = r['name'].lower()
        if r.get('fork') or r.get('private') or r.get('archived') or name == SELF.lower() or name in excluded:
            continue
        when = (last_change(r['name']) if last_change else None) or r.get('pushed_at', '')[:10]
        if name not in listed:
            new['projects'].append(draft_card(r, when))
            changes.append(f"Draft card for {r['name']}: check its name, category, status, audience, levels and summary")
        elif when and when > listed[name]['updated']:
            changes.append(f"{listed[name]['name']}: updated {listed[name]['updated']} -> {when}")
            listed[name]['updated'] = when
    if changes:
        new['updated'] = max([new.get('updated', '')] + [p['updated'] for p in new['projects']])
    return new, changes


def push_proposal(data, changes):
    """Write the proposal to its own branch, rebuilt and checked. The repository does not let Actions open pull
    requests (docs/repo-settings.md), so the issue carries a one-click link for the owner to open it."""
    (ROOT / 'data' / 'projects.json').write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    subprocess.run([sys.executable, str(ROOT / 'tools' / 'build.py')], check=True)
    git = ['git', '-c', 'user.name=github-actions[bot]', '-c', 'user.email=41898282+github-actions[bot]@users.noreply.github.com']
    subprocess.run(['git', 'checkout', '-q', '-B', PROPOSAL_BRANCH], check=True)
    subprocess.run(['git', 'add', 'data/projects.json', 'index.html', '404.html'], check=True)
    subprocess.run([*git, 'commit', '-q', '-m', 'Launchpad: proposed cards and dates from the discovery routine\n\n' +
                    '\n'.join(f'- {c}' for c in changes)], check=True)
    repo = os.environ.get('GITHUB_REPOSITORY', f'{OWNER}/{SELF}')
    url = f"https://x-access-token:{os.environ['GH_TOKEN']}@github.com/{repo}.git"  # never printed: output is captured
    subprocess.run(['git', 'push', '-q', '--force', url, f'HEAD:refs/heads/{PROPOSAL_BRANCH}'], check=True, capture_output=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--propose', action='store_true', help='also push a proposed change to the routine/discover branch')
    a = ap.parse_args(argv)
    repos, data = public_repos(), load()
    found = findings(repos, data, last_change_by_person, publiccode_licences)
    proposal = ''
    if a.propose and not a.dry_run and os.environ.get('AUTOMATION') != 'off':
        new, changes = propose(repos, data, last_change_by_person)
        if changes:
            push_proposal(new, changes)
            repo = os.environ.get('GITHUB_REPOSITORY', f'{OWNER}/{SELF}')
            proposal = (f'\n\n**A proposed change is ready** on the `{PROPOSAL_BRANCH}` branch. '
                        f'[Open the pull request](https://github.com/{repo}/compare/main...{PROPOSAL_BRANCH}?expand=1), '
                        'check every drafted card, then merge. The profile README follows within a day.\n\n' +
                        '\n'.join(f'- {c}' for c in changes))
    body = ('Found by the discovery routine (tier 2, ops/automation.yaml). It never changes main: it prepares a branch '
            'for a person to review and merge.\n\n' +
            ('\n'.join(f'- {f}' for f in found) or 'Nothing to do.') + proposal)
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
