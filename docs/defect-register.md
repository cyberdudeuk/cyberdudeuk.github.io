# Defect register

Every defect found gets a check that prevents it coming back. The check suite never shrinks.

| ID | Found | Defect | Root cause | Fix | Check |
|---|---|---|---|---|---|
| D-01 | 2026-11-08 | The licence copyright line read "Copyright (c) 2026 Em", cut off (inherited from the toolkit repository) | Truncated when the licence was first written | Holder written in full | L11 |
| D-02 | 2026-11-08 | On a phone, the category menu came before the projects and its switch sat below it | Desktop-first layout | Switch first; menu starts closed below 760px | B4, B1 |
| D-03 | 2026-11-08 | "Choose your way in" listed nearly every project under every level, which helped nobody choose | Most projects support all levels | Two or three suggested starting points per level, kept in the data; a level filter | L5, B3 |
| D-04 | 2026-11-08 | First Checks and Publish runs failed: segno not found, so nothing was published | The workflows created the Python environment and installed into it in the same step; a PATH change only applies from the next step, so packages went to the system Python | Install in its own step | L12 |
| D-05 | 2026-11-08 | After the first Dependabot pull requests were merged one after another, `requirements.txt` pinned PyYAML and Playwright twice each, so pip refused to install and every Checks and Publish run failed. `pages.yml` also had two copies of its configure and upload steps. A test hard-coded one deploy-pages commit, so any update broke it | Each Dependabot pull request was opened against the first commit and merged without the checks passing first (they could not pass until D-04 was fixed) | One pin per package; one step each; the test matches any pinned commit | L13, L14 |
