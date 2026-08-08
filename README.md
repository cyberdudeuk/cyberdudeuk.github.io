# Public AI Utility Toolkit

[![Version](https://img.shields.io/badge/version-2.0.0-0b3d91)](CHANGELOG.md)
[![Licence: MIT](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![Content: OGL v3.0](https://img.shields.io/badge/content-OGL%20v3.0-blue)](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
[![WCAG 2.2 AA](https://img.shields.io/badge/accessibility-WCAG%202.2%20AA-00703c)](ACCESSIBILITY.md)

**[Open the toolkit →](https://cyberdudeuk.github.io/)**

A public-good, government-grade knowledge utility for AI-assisted public services. It turns policy and
standards into things you can actually use: a risk-based human review model, evidence and transparency
generators, an equality and accessibility screen, a quantum readiness assessment, and a tiered library of
68 authoritative sources.

## Four non-negotiable principles

1. **Humans remain accountable.** AI never grants authority a person does not already hold.
2. **AI outputs are verified, not trusted by default.** Every claim traces to a citable source.
3. **Public value, equality and accessibility are built in** — screened before delivery, not audited after.
4. **Evidence, metadata and provenance are mandatory** for anything material or public-facing.

## What is in the portal

| Section | What it gives you |
| --- | --- |
| Start here | Six role-based routes and six common tasks with time estimates |
| Knowledge | Authority tiering (0–3), conflict resolution and drift triggers |
| Toolkit | 18 catalogued assets, each anchored to the standards it implements |
| Tools | Six working, client-side tools — see below |
| Assurance | The H0–H5 review model, reviewer checklist, failure patterns and a RACI |
| Catalogue | Minimum viable metadata for any AI asset, with a worked YAML example |
| UCD & DEIA | Design and research practice, accessibility commitments and AI-specific equity risks |
| Practice | Code of practice: core duties, prohibited behaviours, agent rules, code rules, speaking up |
| Resources | 68 tiered sources, searchable and filterable |
| Transparency | Ownership, versioning, licence, privacy, limitations and changelog |
| Roadmap | 23 identified gaps prioritised with MoSCoW |
| Glossary & FAQ | 22 terms and 8 answers |
| Contact | Bug, accessibility, feature, correction, security and direct-message routes |

## The six tools

| Tool | What it does | Time |
| --- | --- | --- |
| Human review triage | Scores audience, impact, data classification, reversibility and six escalating factors to return an H0–H5 level with mandatory follow-on actions | 2 min |
| Evidence pack generator | Produces a copy-ready AI-use declaration and evidence record | 3 min |
| DEIA impact screen | Tests ten exclusion risks and tells you whether a full equality impact assessment is needed | 5 min |
| Transparency record generator | Drafts an ATRS-shaped public record | 10 min |
| Quantum readiness assessor | Scores harvest-now-decrypt-later exposure against NCSC migration milestones | 5 min |
| Plain-language checker | Reading age, sentence length, passive voice, unexplained acronyms, jargon and non-inclusive phrasing | 1 min |

> **Privacy:** every tool runs entirely in your browser. Nothing you type is sent anywhere, stored on a
> server, or logged. There are no analytics and no third-party requests.

## Repository contents

| File | Purpose |
| --- | --- |
| `index.html` | The complete portal. All content is in the HTML and readable without JavaScript. |
| `styles.css` | Design tokens, light/dark/high-contrast themes, components and print styles. |
| `app.js` | Progressive enhancement: preferences, navigation, search, filtering, the tools and contact routing. |
| `CHANGELOG.md` | Versioned record of every notable change. |
| `CONTRIBUTING.md` | How to propose changes, and the evidence standard contributions must meet. |
| `ACCESSIBILITY.md` | Accessibility statement, testing approach, known gaps and escalation. |
| `SECURITY.md` | Coordinated disclosure policy and scope. |
| `SUPPORT.md` | Where to get help and how quickly to expect a reply. |
| `CODE_OF_CONDUCT.md` | Expected behaviour in this community. |
| `.github/ISSUE_TEMPLATE/` | Structured forms for bugs, accessibility barriers, features and corrections. |

## Configuration

All deployment-specific settings live in one block at the top of `app.js`:

```js
var PAUT_CONFIG = {
  repo: 'cyberdudeuk/cyberdudeuk.github.io',
  mailbox: '',        // team mailbox for direct messages; leave empty to route via GitHub only
  maskMailbox: true,  // display the address masked, assemble it only on request
  formEndpoint: '',   // optional HTTPS endpoint if you later want server-side submission
  responseDays: 5     // published first-response target for accessibility reports
};
```

**Set `mailbox` to your team inbox** to enable the direct message route. Until it is set, the contact
form still composes the message and offers a copy or a GitHub issue instead.

## Local preview

Open `index.html` directly in a browser, or serve the directory:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Deployment

Deployed to GitHub Pages by `.github/workflows/pages.yml`, which publishes the repository root on pushes
to `main` and can be triggered manually with `workflow_dispatch`.

## Accessibility

This portal targets WCAG 2.2 AA. It offers light, dark and high-contrast themes, a larger-text setting,
full keyboard operation, visible focus indicators, labelled landmarks, ARIA live regions on tool results,
reduced-motion and forced-colours support, and a print stylesheet. See [ACCESSIBILITY.md](ACCESSIBILITY.md).

**Found a barrier?** [Report it](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=accessibility_issue.yml) — accessibility
defects are treated as priority, with a target first response of 5 working days.

## Contributing

Contributions are welcome, especially corrections with a source. Read [CONTRIBUTING.md](CONTRIBUTING.md)
first — the short version is that every factual claim needs a tiered, dated, authoritative source.

| I want to… | Route |
| --- | --- |
| Report a bug | [Bug report](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=bug_report.yml) |
| Report an accessibility barrier | [Accessibility issue](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=accessibility_issue.yml) |
| Suggest a feature or resource | [Feature request](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=feature_request.yml) |
| Correct out-of-date content | [Content correction](https://github.com/cyberdudeuk/cyberdudeuk.github.io/issues/new?template=content_correction.yml) |
| Report a vulnerability | [Security policy](https://github.com/cyberdudeuk/cyberdudeuk.github.io/security/policy) — do not open a public issue |
| Ask something privately | The contact form on the [portal](https://cyberdudeuk.github.io/#contact) |

## Governance

| | |
| --- | --- |
| Owner | Public AI Utility Toolkit working group |
| Version | 2.0.0 |
| Last reviewed | 2026-08-08 |
| Next review due | 2026-11-08 |
| Content licence | [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) |
| Code licence | [MIT](LICENSE) |

## Limitations

This is a concept portal, not a statutory instrument. It does not replace your organisation’s policies,
your data protection officer, your security team or your legal advice. Some linked standards sit behind
paywalls. Links were verified on 2026-08-08 — always confirm you are reading the current version at the source.
