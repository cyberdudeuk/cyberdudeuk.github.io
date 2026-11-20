---
artefact:id: P13-SAD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P13 Public Good Works launchpad
grade: G3
profile: personal and creative
---

# Solution architecture (SAD): Public Good Works launchpad

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Context
Projects live in many repositories, so people can't see what exists or where to start.

The solution is described in [03-prd.md](03-prd.md). It connects with: Every project site; Estate register.

## Architecturally significant decisions
These are the decisions already recorded in this repository (V):

- [0001-launchpad.md](../adr/0001-launchpad.md)
- [0002-actions-policy.md](../adr/0002-actions-policy.md)
- [0003-design.md](../adr/0003-design.md)

## Quality attributes

| Attribute | How it is met |
|---|---|
| Self-contained | Self-contained; vendored fonts |
| CodeQL, Scorecard | CodeQL, Scorecard |
| Contact | By form only; no email address anywhere (estate rule) |
| Documentation | This kit, checked in CI by `tools/artefact_check.py` |

## Constraints
- Live; listing does not mean endorsement (V: README).
- No personal data unless a DPIA has been done first.
- Contact by form only.

## Risks (proposed ratings)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Two project lists drift (launchpad data and estate register) | High | Medium | Generate one from the other (next step) |
