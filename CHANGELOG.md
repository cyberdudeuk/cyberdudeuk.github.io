# Changelog

## 1.3.1 — 15 November 2026

- The back-to-top arrow is centred and points up (D-18).

## 1.3.0 — 15 November 2026

- A name for the portal: **Public Good Works**, by cyberdudeuk. It is set in `data/owner.json` (`site_name`, `tagline`), so it can be changed in one place.
- More imagery and motion, all drawn in code: a twinkling starfield and a wave edge in the hero, with gentle parallax on
  the constellation; a generated constellation "signature" unique to each project on its card; icons that draw themselves
  in on every section heading; progress rings for each level; a growing status chart and settling coverage map; a moving
  dashed edge and "being built" dots on workshop items; a pointer spotlight on cards; a back-to-top button with a scroll
  ring; and a faint constellation in the footer. All of it stops under reduced motion.
- Fixes found while building: ways-in rings drawn empty (D-16) and signature art cropped (D-17).
- Checks: L23 (signatures, heading icons, the name from the data), B14 (back to top) and B15 (rings), each proved to fail on
  a deliberate break.

## 1.2.1 — 15 November 2026

- The stylesheet and script are linked with a fingerprint of their contents, so after an update no browser shows the new
  page with an old cached stylesheet (D-15).

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
  picture would not have been published (D-12); the live dot's ring stayed under reduced motion (D-09); the new third-party check missed upper-case tags (D-14).
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
