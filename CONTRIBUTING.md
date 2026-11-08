# Contributing

1. Questions and corrections: the [contact form](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=contact.yml) or the [listing form](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=listing.yml).
2. To change the launchpad, edit `data/projects.json` (or `tools/build.py` for layout), run `python3 tools/build.py` and open a pull request. Never edit `index.html` or `404.html` by hand; a check rebuilds them and fails if they differ.
3. Write each summary from the project's own README, and give its status as the project states it.
4. Plain English, sentence case, roles not names, no email addresses.
5. Run the checks in the [advanced guide](docs/user-guide/advanced.md) before you open the pull request.
6. If you fix a defect, add a check that would have caught it, and add it to [the defect register](docs/defect-register.md).
