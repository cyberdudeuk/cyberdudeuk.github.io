# Advanced guide

## Add or change a project

Edit `data/projects.json`. Every project needs: `id`, `name`, `category` (one of the `categories`), `status` (as the
project states it), `updated` (YYYY-MM-DD), `summary` (from its README), `audience`, `levels` (Beginner, Intermediate,
Advanced), `repo` (under github.com/cyberdudeuk), `licence`, and either `site` (under cyberdudeuk.github.io) or `how`.
Then:

```bash
pip install -r requirements.txt
python3 tools/build.py
python3 tools/check_site.py
python3 -m unittest discover -s tests -v
python3 tools/check_browser.py   # needs Chrome; set CHROME to its path
```

Open a pull request. The publish workflow runs every check again before it deploys.

## Routines

Every workflow is in `ops/automation.yaml` with its tier. Discovery (Mondays) reports new public repositories, gone ones
and stale cards in one issue; it never edits the list. The kill switch is the repository variable `AUTOMATION` set to
`off`. Nothing merges itself.

Back: [the intermediate guide](intermediate.md).
