# Changelog

## 1.2.0 — 14 November 2026

- A redesign, held to the standards that award juries weight most (design and usability first): a dark hero with a
  constellation of the nine areas of work drawn from the data (node size is the number of projects; amber lines lead to
  areas with something new), animated headline numbers, and a self-hosted typeface.
- Featured project, with what it includes. Project areas share rows instead of one card per row (D-08).
- Search (press `/`), a live-site-only switch, a compact view, a dark mode switch that remembers your choice only if you use
  it, and an empty state with a reset.
- Coverage map: every area against every level, each number filtering to its projects, and a chart of where the work stands.
- In the workshop: nine pieces of work in development elsewhere that are not public yet, from `data/workshop.json`, never linked.
- A share picture (`og.jpg`) made from the same data; print styles.
- Fixes: the page scrolled sideways at 320px (D-10); the 404 heading was white on white (D-11); the font and share
  picture would not have been published (D-12); the live dot's ring stayed under reduced motion (D-09).
- Checks: six new static checks (L16 to L21) and eight new browser checks (B6 to B13), each proved to fail on a
  deliberate break, including automated accessibility rules in light, dark and phone views and on the 404 page.

## 1.1.1 — 13 November 2026

- The Amplify portal's files are now in its repository: its card says so, and how to run it, as it has no public site yet.
- Refreshed the updated dates of nine projects changed on 13 November 2026.
- Discovery no longer flags a card as stale when the only changes since its date were made by bots, such as Dependabot (D-07).

## 1.1.0 — 8 November 2026

- Added the UK Youth Parliament: Amplify portal (in progress; its portal files are not yet in its repository) under a new Youth voice area.
- Renamed the BHM 2026 Hub card to Black History and Heritage Hub, as the project renamed itself in its 3.0.0.
- Refreshed the updated dates of six projects pushed on 8 November 2026.

## 1.0.0 — 8 November 2026

- New launchpad at the account's root address: a showcase and gateway for every public project, built from `data/projects.json`.
- Projects grouped by area, with filters by area and level, sorting, a retractable category menu with counts and new-flags, and suggested starting points for beginners, intermediate and advanced users.
- Old links to the Public AI Utility Toolkit, which lived here until November 2026, redirect to its new address.
- Estate contract: automation policy, checks with a rebuild comparison and vaccinations, browser checks at three widths, publishing gated on the checks with pinned actions, weekly discovery of new repositories, digest, triage, labels as code, CodeQL, Scorecard, dependency review and Dependabot.
