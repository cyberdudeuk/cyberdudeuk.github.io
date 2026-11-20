---
artefact:id: P13-PRD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P13 Public Good Works launchpad
grade: G3
profile: personal and creative
---

# Product requirements (PRD): Public Good Works launchpad

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Problem and outcome
Projects live in many repositories, so people can't see what exists or where to start.

Outcome sought: Visitors find the right project and start using it in one step. See [01-theory-of-change.md](01-theory-of-change.md).

## Users
- Visitors new to the projects
- People deciding whether a project fits their work
- Contributors adding projects

User evidence: [02-ur-bundle.md](02-ur-bundle.md).

## Scope
**In:**
- Project cards, filters by area and level
- Beginner, intermediate and advanced guides
- Organisation-wide contact form

**Out:**
- Hosting projects
- Endorsement claims

## Requirements
Derived from what this repository says it does (V: README and ADRs). The last column is the check that proves each one, where one exists. U means no check was found that clearly covers it; that is a gap to close, not a pass.

| ID | Requirement | Priority | Verified by |
|---|---|---|---|
| P13-R01 | Build from one open data file | Must | tests/test_projects.py |
| P13-R02 | Filter by area and level | Should | tests/test_site.py |
| P13-R03 | Discover new projects automatically | Should | discover.yml |
| P13-R04 | Contact form only | Must | tests/test_site.py (U) |

## Non-functional requirements
- Self-contained; vendored fonts
- CodeQL, Scorecard

## Status
Live; listing does not mean endorsement (V: README)
