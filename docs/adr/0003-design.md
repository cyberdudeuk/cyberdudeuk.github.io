# ADR 0003: A redesign held to award-jury standards, with no third-party requests

Status: proposed, 14 November 2026 (for the owner's decision in the pull request).

## Context

The owner asked for the launchpad to be raised to the level of award-winning sites. Award juries weight fundamentals
most: Awwwards scores design 40%, usability 30%, creativity 20% and content 10%; the Webby Awards judge content,
structure and navigation, visual design, functionality, interactivity and overall experience. The page already promises
no cookies, analytics or third-party requests, and must work without JavaScript.

## Decision

- Visual design: a dark hero and footer, a light (or dark) body, one accent per area, a self-hosted display typeface
  (Space Grotesk, SIL Open Font License) over system text. No third-party fonts, scripts or images (check L16).
- Creativity from the data, not decoration: the hero illustration is a constellation of the areas drawn from
  `projects.json`; the coverage map and status chart are computed (L18, L19). No photographs and no generated images.
- Motion with purpose and an off switch: numbers count up, cards enter, the illustration breathes. All of it stops under
  reduced motion (B8).
- Usability first: search, filters, a live-site switch, a compact view and a dark mode switch, all optional; every project
  is readable without JavaScript (B11); automated accessibility rules pass in every view (B13).
- The workshop lists work in development elsewhere, from `data/workshop.json`. It never links anywhere (L17), so no
  private workspace is exposed, and an item moves to `projects.json` when it gets its own public repository.

## Consequences

- One more data file to keep current, and `og.jpg` to refresh with `tools/og.py` when the projects change.
- axe-core is vendored in `tools/vendor` for the checks (not published, not analysed by CodeQL); update it by hand.
