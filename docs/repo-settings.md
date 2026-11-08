# Repository settings: owner checklist

These can only be set by the owner. The build session could not change repository settings.

1. **Create** a new public repository named `cyberdudeuk.github.io` **after** renaming the old one to `ai-capability-governance`. Leave it empty (no README, licence or .gitignore), so the prepared history can be pushed.
2. **Pages**: Settings, Pages, Source: GitHub Actions.
3. **About**: description "A launchpad for every cyberdudeuk project: data and AI for public services, and personal work."; website https://cyberdudeuk.github.io/; topics: portfolio, launchpad, public-sector, uk-government, open-data, data-governance, ai-governance.
4. **Features**: Issues on; Discussions off; Wiki off. **Merge**: squash only; delete branches after merge.
5. **Security**: dependency graph on (Dependency review fails without it), Dependabot alerts and security updates, private vulnerability reporting, secret scanning and push protection.
6. **Ruleset "Protect main"**: block deletion and force pushes; require a pull request; require the Checks status once it has run.

No email address belongs in any of these.
