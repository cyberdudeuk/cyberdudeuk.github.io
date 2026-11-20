---
artefact:id: P13-TOC-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P13 Public Good Works launchpad
grade: G3
profile: personal and creative
---

# Theory of change: Public Good Works launchpad

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Problem
Projects live in many repositories, so people can't see what exists or where to start.

## Long-term outcome
Visitors find the right project and start using it in one step.

## Chain

| Inputs | Activities | Outputs | Short-term outcomes | Medium-term outcomes |
|---|---|---|---|---|
| One open data file of projects; each project's own site | Build a showcase and gateway from the data file; discover new projects; refresh last-change dates | index.html built by tools/build.py; project list for reuse | Visitors reach a project site from the launchpad | Every public project is listed with an accurate status |

## Assumptions (proposed; each one testable)

| # | Assumption | How to test it | Evidence today |
|---|---|---|---|
| A1 | A single launchpad reduces confusion | Short usability check with 3 visitors | Not tested |

## Measures (proposed)
- Every public repository listed or excluded with a reason (tests/test_projects.py)
- Last-change dates refreshed by routine

No target is set before a baseline exists.

## What would prove this wrong
If visitors arrive at project sites directly, keep the launchpad as a list only.

## Status
Live; listing does not mean endorsement (V: README). Live site: https://cyberdudeuk.github.io/
