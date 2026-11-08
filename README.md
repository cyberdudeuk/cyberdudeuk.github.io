# cyberdudeuk: projects for better public services

[![Checks](https://github.com/cyberdudeuk/cyberdudeuk.github.io/actions/workflows/checks.yml/badge.svg)](https://github.com/cyberdudeuk/cyberdudeuk.github.io/actions/workflows/checks.yml)
[![Licence: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)

**One place to find every project, now and in future.** Guidance, open standards and working tools for data and AI in
the public sector, and some personal projects. Each lives in its own repository with its own site.

### [Open the launchpad →](https://cyberdudeuk.github.io/)

| | |
|---|---|
| **What it is** | A showcase and gateway for every public project in this account, built from one open data file |
| **Status** | Live. Not an official government service; listing a project does not mean anyone endorses it |
| **Contact** | By [contact form](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=contact.yml) only. There is no email route |
| **Moved** | The Public AI Utility Toolkit that used to live here is now [AI Capability Governance and Implementation](https://cyberdudeuk.github.io/ai-capability-governance/). Old links redirect |

## Choose your way in

| If you… | You are | Start with | Read here |
|---|---|---|---|
| want to see what is here and try something in a browser | **Beginner** | The launchpad's suggested beginner projects | [Beginner](#beginner-finding-a-project), and the [beginner guide](docs/user-guide/beginner.md) |
| want to use a project in your work, or check whether one fits | **Intermediate** | Filter by area and level, then open a project's own site | [Intermediate](#intermediate-using-the-projects-in-your-work), and the [intermediate guide](docs/user-guide/intermediate.md) |
| want to add a project, reuse the list, or understand how it is kept current | **Advanced** | `data/projects.json` and `tools/` | [Advanced](#advanced-adding-projects-and-reusing-the-list), and the [advanced guide](docs/user-guide/advanced.md) |

## Beginner: finding a project

- Every project is a card: what it does, who it is for, its status, when it was last updated and its licence.
- **Open the site** takes you to the project. **Repository** shows its code and documents.
- Each card shows the levels it supports: Beginner, Intermediate or Advanced.
- Nothing on the launchpad tracks you: no cookies, analytics or third-party requests.

## Intermediate: using the projects in your work

| Area | Projects |
|---|---|
| AI governance | [AI Capability Governance and Implementation](https://cyberdudeuk.github.io/ai-capability-governance/) |
| Data standards and metadata | [DCAT-AP-UK](https://cyberdudeuk.github.io/dcat-ap-uk/) (proposed, not endorsed) |
| Data management and quality | [Data Asset Management capability playbooks](https://cyberdudeuk.github.io/dam-capability-playbooks/), [Public Sector Data Quality Commons](https://cyberdudeuk.github.io/dq-commons/) |
| Finding and reusing code | [GitHub Repos Asset Catalogue](https://cyberdudeuk.github.io/github-repos-asset-catalogue/) |
| Knowledge mapping | [The Knowledge Web](https://github.com/cyberdudeuk/knowledge-web) (a single file in the repository) |
| Skills and development | [Plainspoken](https://cyberdudeuk.github.io/plainspoken/) |
| Community and heritage | [BHM 2026 Hub](https://cyberdudeuk.github.io/black-mixed-heritage/) |
| Experiments | [Public sector MCP server](https://github.com/cyberdudeuk/ndl-pubsec-mcp) |

Status is as each project states it. *Prototype* and *proposed* mean not finished and not official. To use a project at
work, read its own README and status first.

## Advanced: adding projects and reusing the list

### How it works

| Path | What it is |
|---|---|
| `data/projects.json` | The list: every project, its category, status, levels, links and licence. Also the suggested starting points |
| `data/owner.json` | What the page says about its owner. Nothing personal is published unless it is written here |
| `tools/build.py` | Builds `index.html` and `404.html` from the data. Never edit those by hand |
| `tools/check_site.py` | 14 static checks, including a rebuild that must match the committed page |
| `tools/check_browser.py` | Browser checks in Chrome at 1280, 390 and 320px: no sideways scroll, no console errors, filters, the menu switch, and old toolkit links |
| `tools/discover.py` | Weekly: lists public repositories missing from the list, gone from it, or newer than their card |
| `tests/` | Vaccination tests: every check must fail on a deliberate break |
| `ops/automation.yaml` | Every workflow, its tier, when it runs and what it may change |
| `docs/` | [Decisions](docs/adr/0001-launchpad.md), [defect register](docs/defect-register.md), [settings checklist](docs/repo-settings.md) |

### Add a new project

1. Add an entry to `data/projects.json` (copy an existing one; every field is checked).
2. Run `python3 tools/build.py`, then the checks below.
3. Open a pull request. Publishing happens when it is merged and every check passes again.

The weekly discovery routine opens an issue when a new public repository appears, so no project is missed.

### Build and check locally

```bash
pip install -r requirements.txt
python3 tools/build.py
python3 tools/check_site.py
python3 -m unittest discover -s tests -v
python3 tools/check_browser.py   # needs Chrome; set CHROME to its path
```

### Reuse the list

`data/projects.json` is open data, and the page carries the same list as schema.org JSON-LD, so other sites and tools
can read it.

## Governance and licence

| | |
|---|---|
| Code licence | [MIT](LICENSE) |
| Text | Open Government Licence v3.0. Each project has its own licence, shown on its card |
| Accessibility | [Accessibility statement](ACCESSIBILITY.md) |
| Security | [SECURITY.md](SECURITY.md) |
| Support | [SUPPORT.md](SUPPORT.md) |
| Conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Changes | [CHANGELOG.md](CHANGELOG.md) |
| Citation | [CITATION.cff](CITATION.cff) |
