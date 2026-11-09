# Repository settings

These settings live in the repository settings, not in files. They were applied in the browser on 9 November 2026 and read
back through the API or the settings pages the same day. The build session cannot change them through the API (the
connection refuses settings writes), so any later change is made by hand and recorded here.

| Setting | Value | Status (9 November 2026) |
|---|---|---|
| Repository | `cyberdudeuk.github.io`, public, created after the old one was renamed to `ai-capability-governance` | Done |
| Pages | Source: GitHub Actions | Read back |
| Description | A launchpad for every cyberdudeuk project: data and AI for public services, and personal work. | Read back |
| Website | https://cyberdudeuk.github.io/ | Read back |
| Topics | accessibility, ai-governance, data-governance, github-pages, launchpad, open-data, open-source, portfolio, public-sector, uk-government | Read back |
| Features | Issues on; Discussions off; Wiki off | Read back |
| Merge | Squash only; delete branches after merge | Read back |
| Ruleset "Protect main" | Default branch: block deletion and force pushes; require a pull request (no approvals, as the owner is the only maintainer); require the `check` status from GitHub Actions; no bypass | Read back (ruleset 26820005) |
| Security | Dependency graph, Dependabot alerts, Dependabot security updates, private vulnerability reporting, secret scanning and push protection all on; CodeQL default setup off (the CodeQL workflow is used) | Read back |
| Actions | Allow GitHub-owned actions and `ossf/scorecard-action@*` only; require actions pinned to a full commit SHA (ADR 0002); default token read-only; Actions may not create or approve pull requests | Read back |

No email address belongs in any of these. Contact is by the contact form only.

## If a workflow is blocked

A new third-party action fails to start until it is added to the allowed list in Settings, Actions. Add it there and
in ADR 0002 in the same change. Every workflow declares its own permissions, so the read-only default token does not
limit them.
