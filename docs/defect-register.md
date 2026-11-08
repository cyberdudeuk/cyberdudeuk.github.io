# Defect register

Every defect found gets a check that prevents it coming back. The check suite never shrinks.

| ID | Found | Defect | Root cause | Fix | Check |
|---|---|---|---|---|---|
| D-01 | 2026-11-08 | The licence copyright line read "Copyright (c) 2026 Em", cut off (inherited from the toolkit repository) | Truncated when the licence was first written | Holder written in full | L11 |
| D-02 | 2026-11-08 | On a phone, the category menu came before the projects and its switch sat below it | Desktop-first layout | Switch first; menu starts closed below 760px | B4, B1 |
| D-03 | 2026-11-08 | "Choose your way in" listed nearly every project under every level, which helped nobody choose | Most projects support all levels | Two or three suggested starting points per level, kept in the data; a level filter | L5, B3 |
