# Changelog

## 22 November 2026: defect numbers made unique (D-43)

- Two defects were each numbered twice. The board-status D-29 is now D-42, with its citations in the board routine,
  its tests and this changelog; the sideways-scroll D-31, cited nowhere, is now D-41. New check L29 keeps register
  numbers unique and fails if code, tests or the changelog cite a number the register lacks; two tests prove it.
- The triage and digest routines now say that D-018 is the estate decision in dam-capability-playbooks.

## 22 November 2026: Young Person 360º and Earning, learning and training are public

- Both 360º portals now have their own public repositories and sites, and move from the workshop to the projects
  list under Youth voice: [Young Person 360º: before the label](https://cyberdudeuk.github.io/young-person-360/) and
  [Earning, learning and training](https://cyberdudeuk.github.io/earning-learning-training/). Whole-life 360º stays
  in the workshop.
- Both are on the contact form.
- Fixed (D-40): the contact form's Amplify option parsed as a key and value, not text, so GitHub could not use the
  form as written. L15 now reads the parsed form; a new test proves it fails on the old line.

## 22 November 2026: one glossary for the 360º portals; Earning, learning and training

- New: `data/shared-glossary.json`, the single place where the 360º portals define the terms they share (BEET,
  CHEET, NEET, held status, departure event, arrival, returner, enterprise route, and the business terms used for
  starting safely). Each term has one owner portal; the others use the same words and link to it. It also states who
  owns which question, so a topic lives in one place. Check L28 keeps it consistent; two tests prove the check fails.
- Workshop: Earning or learning is now *Earning, learning and training*, for young people aged 16 to 24. Adults
  returning to work or learning belong to Whole-life 360º.

## 22 November 2026: Starting a business in the UK published; workshop brought up to date

- New card: Starting a business in the UK, now public at its own address, in a new area, *Starting and running a
  business* (olive, briefcase icon, checked in light and dark and in the hero diagram).
- Workshop: Start a business left it for Projects. My 360º gave way to Whole-life 360º, which took in its ideas. SHARE
  moved into govukOS, so it is now part of that card. RAIDU left the workshop: its public guidance lives in AI
  Capability Governance and Implementation; the rest is working material, not for publication.
  Young Person 360º now says what it covers.
- Contact form, README and share picture updated.
- The hero diagram is wider, so labels fit with any font; B19 now also measures them with DejaVu Sans, the font that
  showed the overflow on the CI runner (D-39).

## 22 November 2026: hero diagram labels fit, and every node is a link

- The "Open government" label no longer runs off the edge of the hero diagram: long labels near an edge wrap onto
  two lines (D-38).
- Each node in the diagram is now a link. An area with one project opens that project's site; Data management and
  quality, with three, opens its section of the list; the centre opens all projects. Keyboard focus shows an amber ring.
- New browser check B19 measures every label against the drawing at three widths and checks every node is a link.

## 22 November 2026: OpenGovernment UK listed, dates refreshed

- New card: OpenGovernment UK, one register of the UK state (every public body, who it answers to, who pays for it
  and who owns it), published today. It sits in a new area, *Open government and public bodies*, with its own icon
  and colours checked in light and dark mode. Added to the contact form's project list (L15) and the README.
- Updated dates on seven cards from their repositories' latest activity, superseding the proposal in issue #42.
- Share picture (og.jpg) regenerated.

## 22 November 2026: discovery proposals show only what changed

- The discovery routine's proposal now keeps data/projects.json in the layout it found it, so a date change is a
  one-line diff. Its proposal for issue #42 had rewritten all 586 lines to change seven dates (D-37).

## 20 November 2026: NDL PubSec MCP card corrected

- The NDL PubSec MCP card now says independent work, with MIT code and CC BY 4.0 content, as the project states. It
  had still said official GDS work under the Open Government Licence. Its summary and audience now cover the
  exchanges, standards and plain-English guide, and it is marked for all three levels.
- Discovery now reports a listed project with no publiccode.yml, rather than skipping the licence check in silence
  (D-36).

## 19 November 2026: DAM Policy Explorer listed

- The DAM Policy Explorer, a one-stop shop on the Data Asset Management Policy for coordinators, is now on the
  launchpad and in the contact form. It was public but unlisted, with no licence; it now has MIT code and OGL v3.0
  content. Register 1.4.0, 11 projects.
- AI Capability Governance, the GitHub Repos Asset Catalogue and Amplify now show CC BY 4.0 for their content, not
  the Open Government Licence: they are personal projects, not government work.
- A vaccine test hard-coded a coverage count and broke when the project was listed; it now reads the count from the
  data (D-34).
- With eleven projects the spotlight's controls ran 8px off a small phone screen; they now wrap, and a new browser
  check proves it with 30 extra dots (D-35).

## 19 November 2026: board status from activity, and weekly status updates

- The projects routine now sets each item's Status on the Public Good Works board from its repository's activity:
  In progress after a change by a person in the last 30 days; otherwise Done if it has a release, or Todo if not.
- Once a week it posts a project status update: overall health (on track, at risk if any project is waiting,
  inactive if nothing moved in 30 days) and a table of each project's status, changes in the last 7 days, last
  change, latest release, open issues and open pull requests. Earlier updates are never edited or deleted.
- Each item's description now says how busy the project has been: changes by a person in the last 7 and 30 days,
  last change, latest release, open issues and pull requests (D-42).
- Stars and forks are now read too, as a first measure of use rather than activity (D-31).

## 19 November 2026 (1.4.0): one gateway to all the work

- A gateway at the top of the page reaches every place the work lives: the projects, the notes, the public project
  board on GitHub Projects, and every repository (D-29).
- Spotlight replaces the single Featured panel: a carousel of the newest projects, the latest note and the project
  board, chosen from the data. It moves only when asked (buttons, dots, arrow keys), offers Play with a 7-second
  rotation that pauses while the pointer or keyboard focus is in the slides, and never rotates under reduced motion.
  Without JavaScript it is a strip you can scroll.
- Have your say: an idea and feature request form joins the bug, accessibility and card-correction forms, all offered
  on the page, not only the contact form. Ideas are tracked by the triage routine like the others.
- The project board is in the section links. The links fold into the menu whenever they would wrap, whatever the
  font or text size (D-33).
- The launchpad's own text is now CC BY 4.0, not OGL v3.0: it is personal work, not Crown copyright (D-30).
- New checks: L26 (gateway, spotlight, feedback forms), L27 (text licence), B17 (spotlight and masthead).

## 19 November 2026: note pages redesigned

- Note pages have their own reading layout in the launchpad's brand: the night-sky header with the brand mark, a
  signature drawing generated from the note's id, an "In short" summary, "On this page" links, section icons, a
  reading-progress bar and gentle reveal on scroll (both off under reduced motion), link cards, and the usual footer
  with disclaimer, transparency note, contact and QR code and barcode colophon. Lines are kept to a readable measure.
- Paragraphs were 64px apart and the summary appeared twice; both fixed, with a browser check (B16) and a site check
  (L25) so they stay fixed (D-27).
- "See it in action": a note can name the projects it is about; its page shows each one with who it is for, what
  it does and a link to try it live, all from projects.json. Real stories of projects in use can be added in
  data/stories.json, only with a source, evidence and the person's consent; until then the page asks readers to
  share theirs (D-28).

## 19 November 2026: Zenodo community and topic check

- Every Zenodo record is now in one Zenodo community, Public Good Works, linked from the About panel.
- Discovery flags any listed repository with fewer than three GitHub topics, so each stays findable by topic (D-26).

## 19 November 2026: Notes and a feed

- New Notes section: short notes about the work, written here first. Each has its own page under notes/ and an
  entry in feed.xml (Atom), which DEV imports with the note's page as the canonical original. A note first published
  elsewhere is listed with a link out and left out of the feed, so no site imports a duplicate. The first note says
  where the work appears and which copy to trust.
- Notes are plain text in data/posts.json; the build refuses HTML, unknown block types, bad ids and links that are
  not https to a known host. New check L25; the email (L1) and rebuild (L2) checks now cover notes and the feed (D-25).

## 18 November 2026: profiles linked both ways

- The About panel now links the owner's public profiles (GitHub, DEV Community, ORCID, LinkedIn) with `rel="me"`, and
  the page's schema.org data names them in `sameAs`, so search engines and other sites can tie them together. They
  are listed in data/owner.json; the build publishes only https links to known hosts. New check L24 fails if a listed
  profile is missing from the page or the schema.org data (D-24).

## 1.4.1 — 18 November 2026

- The projects routine's first real run stopped after creating the board and one item: two of its fields were named
  Status and Repository, which every GitHub Project already has as built-in fields (D-23). They are now Project status
  and Repository link, the routine refuses to start if a field name clashes with a built-in one, and the tests' fake
  GitHub service now has the built-in fields too, so the tests fail the way the real run did.

## 1.4.0 — 18 November 2026

- Discovery now runs daily and proposes, not only reports (tier 2): for each new public repository it drafts a card
  from what the repository states (name, description, licence, topics, site), labels what the repository does not say
  ("To be confirmed by the owner", status "Experiment: new, not yet reviewed"), moves each card's date to the last
  change by a person, rebuilds the page and pushes the result to the `routine/discover` branch. The routine issue
  links to open the pull request. It never changes main and never removes or rewords a card; the AUTOMATION kill
  switch stops it. The profile README follows the merged list. The owner's request of 18 November 2026.
- Two cards had the wrong content licence and are corrected: Public Sector Data Quality Commons (MIT code, CC BY 4.0
  content) and GitHub Repos Asset Catalogue (MIT code, OGL v3.0 content). Discovery now compares each card's licence
  with the licences the project states in its publiccode.yml, so this is caught next time (D-22).
- New projects routine (tier 1): every day, and whenever the project list changes on main, it keeps the GitHub Project
  "Public Good Works" in step. Each project is one item with its status and area (grouped as on the launchpad), licence
  and links, plus what its repository shows: the last change by a person, the latest release, open issues and pull
  requests, and the last five changes by a person. It adds and refreshes, never deletes. It needs a classic personal
  access token with the "project" scope in the PROJECTS_TOKEN secret; without one it warns and changes nothing.

## 1.3.4 — 15 November 2026

- Checks now run two linters, Ruff for Python and ESLint for JavaScript, and fail on any finding (D-21). The two
  findings they raised are fixed. Part of applying the secure development standard to every project.

## 1.3.3 — 15 November 2026

- The Knowledge Web and the UK Youth Parliament Amplify portal now have live sites on GitHub Pages (the owner's
  decision); their cards link to them. Ten projects, ten live sites.
- The L3 vaccine test makes its own siteless card instead of relying on one in the data (D-20).

## 1.3.2 — 15 November 2026

- The NDL PubSec MCP card was out of date: it said the project had no site and no licence, but its site is live and its
  code is MIT licensed (documentation OGL v3.0). The card now uses the project's own name, summary and status: an official GDS prototype, at alpha (D-19).
- Discovery now also reports a card that contradicts its repository: no site listed while the repository has a live
  Pages site, or "no licence" while the repository has one. Tested both ways.
- The headline-number test reads its anchor from the data, so a project gaining a site no longer breaks it.

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
