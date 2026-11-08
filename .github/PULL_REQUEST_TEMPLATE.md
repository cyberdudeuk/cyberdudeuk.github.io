## What this changes

## Why

## Checklist
- [ ] I edited `data/projects.json` (or `tools/build.py`), ran `python3 tools/build.py`, and did not edit `index.html` by hand
- [ ] A project's summary is written from its own README, and its status is as the project states it
- [ ] Plain English, sentence case, roles not names, no email addresses
- [ ] If this fixes a defect, a check that catches it is in the same pull request and `docs/defect-register.md` is updated
- [ ] `python3 tools/check_site.py && python3 -m unittest discover -s tests && python3 tools/check_browser.py` passes
