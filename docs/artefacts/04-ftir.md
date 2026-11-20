---
artefact:id: P13-FTIR-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P13 Public Good Works launchpad
grade: G3
profile: personal and creative
---

# Functional, technical and integration requirements (FTIR): Public Good Works launchpad

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

Requirements are stated once, in [03-prd.md](03-prd.md). This document says how each is met and checked.

## Functional

| ID | Requirement | Priority | Verified by | State |
|---|---|---|---|---|
| F01 | Build from one open data file | Must | tests/test_projects.py | Has a check |
| F02 | Filter by area and level | Should | tests/test_site.py | Has a check |
| F03 | Discover new projects automatically | Should | discover.yml | Has a check |
| F04 | Contact form only | Must | tests/test_site.py (U) | Check named; coverage unconfirmed (U) |

## Technical

| ID | Requirement | State |
|---|---|---|
| T01 | Code scanning | Present (V: .github/workflows) |
| T02 | Dependency review on pull requests | Present (V: .github/workflows) |
| T03 | OpenSSF Scorecard | Present (V: .github/workflows) |
| T04 | Automated release | Not present |
| T05 | Published by workflow (Pages) | Present (V: .github/workflows) |
| T06 | Documentation kit checked in CI | Present (V: .github/workflows) |

Workflows present (V): `checks.yml`, `codeql.yml`, `dependency-review.yml`, `digest.yml`, `discover.yml`, `labels.yml`, `pages.yml`, `projects.yml`, `scorecard.yml`, `triage.yml`.

Tests present (V): `test_automation.py`, `test_projects.py`, `test_site.py`.

## Integration

| ID | Integration | Direction | State |
|---|---|---|---|
| I01 | Every project site | Links out | Live |
| I02 | Estate register | Same project list | From this change |
