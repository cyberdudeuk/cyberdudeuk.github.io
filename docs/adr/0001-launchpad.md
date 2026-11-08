# ADR 0001: The root address becomes a launchpad for every project

Status: accepted, 8 November 2026 (owner decision).

## Context

`cyberdudeuk.github.io` held the Public AI Utility Toolkit. The owner wants the root address to be a portfolio-style
launchpad and showcase for every project, present and future, and the toolkit to become a project in its own right
(renamed to `ai-capability-governance`; its ADR 0001).

## Decision

- A new repository named `cyberdudeuk.github.io` serves the launchpad at https://cyberdudeuk.github.io/.
- The page is built from one open data file, `data/projects.json`, never edited by hand.
- A weekly discovery routine reports new public repositories, so future projects are not missed; a person adds them.
- Old toolkit links (`/#tools`, `/#tool-triage` and the other section links) redirect to the toolkit's new address.
- The owner is shown as the account name. Nothing personal is published unless the owner writes it in `data/owner.json`.
- Its own neutral design: it is a public, personal launchpad, not a govukOS app, and each project keeps its own design.

## Consequences

- Between the rename and this repository being published, the root address shows a 404.
- Forks and private repositories are never listed.
