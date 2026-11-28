# Portfolio architecture and consolidation plan

**Status:** Proposed for maintainer review  
**Prepared:** 28 November 2026  
**Scope:** Repositories visible under the `cyberdudeuk` account  
**Decision principle:** one coherent ecosystem; separate repositories where separation creates real value.

This document is a proposal, not an instruction to merge or retire repositories. It deliberately avoids destructive changes. Repository history, URLs, licences, external consumers, deployment dependencies, secrets, data classification and stakeholder ownership must be checked before any consolidation is executed.

## 1. Executive recommendation

Do not combine the portfolio into one monorepo. Keep independently deployable products, distinct audiences, security boundaries, standards proposals and experimental work separate. Consolidate duplicated *shared infrastructure* instead: metadata schemas, design tokens, accessibility checks, provenance rules, CI workflows, release conventions, source registries and reusable components.

The portfolio should be managed as a small number of product families:

1. **Discovery and adoption:** GitHub Repos Asset Catalogue, Public Sector Tech Hub, the account launchpad, OpenGovernment UK.
2. **Data management and interoperability:** DAM Capability Playbooks, DAM Policy Explorer, CDO Connect Hub, Data Quality Commons, DCAT-AP-UK, DAM Returns Pipeline.
3. **Public-sector intelligence and operating environment:** Legacy Technology Observatory, Legacy Code Observatory, govukOS, NDL PubSec MCP and its private counterpart.
4. **AI governance and knowledge:** AI Capability Governance, Knowledge Web, chatbot.
5. **People, participation and public-good services:** UK Youth Parliament: Amplify, Young Person 360, Whole-life 360, Earning Learning Training, Starting a Business UK, Black History and Heritage Hub, Awards and Recognition Hub, ICIP, Plainspoken.
6. **Portfolio and shared foundations:** cyberdudeuk.github.io, .github, personal portfolio, w3id.org, archived tutorials and experiments.

The first consolidation should be organisational and technical, not a repository merge: define the product map, a shared metadata contract, common engineering standards and clear repository lifecycle labels.

## 2. Merge, keep separate, or integrate?

| Relationship | Recommendation | Rationale |
|---|---|---|
| GitHub Repos Asset Catalogue ↔ Public Sector Tech Hub | **Keep separate; integrate** | Catalogue is the broad inventory/discovery engine. Tech Hub is a curated adoption experience for public-sector technology. Share metadata and ingestion APIs; keep separate user journeys and release cadence. |
| GitHub Repos Asset Catalogue ↔ internal catalogue | **Keep separate; integrate cautiously** | Preserve the public/private boundary. Share schemas and sanitised build tooling, never internal source records, credentials, vulnerability details or unpublished operational data. |
| Legacy Technology Observatory ↔ Legacy Code Observatory | **Keep successor; retire redirect repo when safe** | The legacy-code project appears to be a predecessor/redirect. Keep its redirect and historical notice until backlinks, package references and deployment routes are checked; then archive rather than merge histories. |
| DAM Capability Playbooks ↔ DAM Policy Explorer | **Keep separate initially; integrate content model** | Playbooks are broad capability guidance; Policy Explorer is a focused navigation/exploration experience. They can share policy identifiers, evidence records and taxonomy. Consider folding the Explorer into the Playbooks only if user research shows the same audience, content lifecycle and deployment needs. |
| DAM Capability Playbooks ↔ CDO Connect Hub | **Keep separate; integrate workflows** | Playbooks are reference guidance; CDO Connect Hub is a community/operational workspace. Link guidance to tasks and decisions, but do not turn the playbooks into a community platform. |
| DAM Returns Pipeline ↔ CDO Connect Hub | **Keep separate; integrate through controlled interfaces** | The pipeline handles operational returns and potentially sensitive records; the Hub serves coordination and guidance. Use APIs or exports with explicit data contracts, least privilege and audit trails. Do not combine storage or permissions by default. |
| Data Quality Commons ↔ DAM Capability Playbooks | **Keep separate; integrate** | One is a reusable quality framework/toolkit; the other is broader data-asset capability guidance. Share measures, maturity definitions and validation fixtures. |
| DCAT-AP-UK ↔ catalogue / Tech Hub / NDL PubSec MCP | **Keep as a distinct standards proposal; integrate as an optional mapping** | A metadata standard/proposal must retain its own governance and versioning. Consumers can map to it, but should not silently treat a proposal as an endorsed national standard. |
| NDL PubSec MCP ↔ NDL PubSec MCP Private | **Keep separate** | Distinct visibility and handling boundaries matter. Share public code only where safe and intentionally released. Never mirror private records or secrets into the public project. |
| NDL PubSec MCP ↔ catalogue / OpenGovernment UK / observatories | **Keep separate; integrate as a read-only interface** | MCP is an access/interaction layer, not the authoritative data store. Expose provenance-aware read-only tools over public sources, with rate limits and explicit freshness. |
| AI Capability Governance ↔ Knowledge Web | **Keep separate; integrate** | Governance content and knowledge-graph/navigation infrastructure are different layers. The governance project should consume or publish structured knowledge using stable schemas; Knowledge Web should remain domain-neutral. |
| AI Capability Governance ↔ chatbot | **Keep separate unless chatbot is only a demo** | Governance controls and a conversational interface have different security, evaluation and operational requirements. If the chatbot exists solely to demonstrate AI governance, consider moving the demo into the governance repo as an example app, not merging unrelated application history. |
| govukOS ↔ all other products | **Keep distinct; integrate by contracts** | govukOS is a broad operating-environment proposition. Other repositories should remain independently usable. Integrate via documented APIs, identifiers, shared design system and federated identity only when proven necessary. |
| Whole-life 360 ↔ Young Person 360 ↔ Earning Learning Training | **Keep separate; align shared journey model** | They address different populations, life stages and safeguarding requirements. Share non-identifying service taxonomy and journey components; retain separate consent, privacy, content and safeguarding models. |
| UK Youth Parliament: Amplify ↔ Young Person 360 | **Keep separate** | Youth participation and an individual/service journey model are different purposes. Any integration must be opt-in, transparent and designed with young people. |
| Awards and Recognition Hub ↔ other public-good services | **Keep separate; share source/provenance tooling** | Its data model and editorial workflow are distinctive. Reuse source monitoring and accessibility infrastructure rather than merging its content. |
| Starting a Business UK ↔ Earning Learning Training | **Keep separate; cross-link** | Different audiences and task journeys. Cross-link relevant employment/self-employment pathways; do not combine their content ownership or eligibility logic. |
| Black History and Heritage Hub ↔ other public-good projects | **Keep separate** | Preserve its distinct editorial purpose and community governance. Share technical foundations only; content decisions should remain with appropriately informed contributors. |
| Plainspoken ↔ ICIP | **Keep separate** | Coaching and identity-safe organisational feedback are distinct products with different privacy and evaluation needs. |
| Launchpad ↔ personal portfolio | **Keep separate; cross-link** | Launchpad is the canonical project directory; personal portfolio is a professional narrative. Avoid maintaining duplicate project inventories manually. |
| .github ↔ every repository | **Centralise shared defaults** | Use for reusable issue/PR templates and community files where appropriate. Keep project-specific security policies, licences and operational instructions in each repo. |
| w3id.org | **Keep separate** | Permanent identifier infrastructure has an external community and governance context; do not absorb it into the portfolio. |
| Innovation Lab / Desktop Tutorial | **Review for archive or explicit purpose** | If no active user, owner, release plan or dependency exists, mark maintenance-only or archive after checking links and consumers. |

## 3. Target architecture

### 3.1 Product layers

- **Authoritative source layer:** source registries, repository metadata, public-body records, standards and evidence references.
- **Knowledge and policy layer:** DAM playbooks, AI governance, data-quality methods, legacy technology evidence and standards mappings.
- **Service and workflow layer:** returns pipeline, CDO Connect Hub, govukOS capabilities and user-facing task journeys.
- **Discovery and access layer:** Asset Catalogue, Public Sector Tech Hub, launchpad and NDL PubSec MCP.
- **Experience layer:** distinct public-facing products for their specific audiences.

No user-facing application should become the accidental authoritative source for another product's data. Each data domain needs an owner, stable identifier, schema, source-of-truth declaration and change process.

### 3.2 Shared contracts to define once

Create versioned, documented contracts for:

1. **Project metadata:** canonical name, repository URL, service URL, owner, audience, status, maturity, licence, accessibility statement, data classification, support route, last verified date and lifecycle tier.
2. **Evidence/provenance:** claim, source, source type, authority, URL, retrieved/checked date, reviewer, confidence, expiry/review date and supersession state.
3. **Public-sector entity identifiers:** stable IDs, aliases, jurisdiction, effective dates and source references.
4. **Data quality:** validation rules, severity, measurement method, result, exception, owner and remediation status.
5. **API/MCP responses:** source attribution, freshness timestamp, confidence/limitations, rate-limit behaviour and error semantics.
6. **Accessibility and service status:** WCAG target, audit date, known issues, user research date and operational status.

Use JSON Schema or another machine-readable schema format with examples and automated compatibility tests. Do not create a new bespoke standard if an established standard already fits.

## 4. Repository boundaries and data protection

- Public repositories contain only intentionally public code, documentation and data.
- Private repositories must not publish their content, metadata or deployment artefacts without an explicit review.
- Keep operational returns, personal data, vulnerability reports, credentials, tokens and unpublished evidence out of public build pipelines.
- Use least-privilege tokens and short-lived credentials where possible.
- Treat MCP tools as an interface with explicit allowlists, input validation, output filtering, rate limits and auditability.
- Never let a generated catalogue or AI assistant convert an unverified claim into an authoritative fact.
- Separate illustrative journeys from real case data, especially in youth and life-event projects.

## 5. Shared engineering improvements

### 5.1 Central reusable workflows

Use the `.github` repository or a dedicated shared-workflows repository for reusable CI workflows where the platform supports it. Standardise:

- Markdown/link and metadata validation.
- JSON/YAML schema validation.
- Unit tests and build checks.
- Dependency update automation.
- Secret scanning and dependency review.
- CodeQL or equivalent static analysis where appropriate to the language.
- Accessibility smoke tests and scheduled full audits.
- Licence and provenance checks.
- Release notes and version tagging.
- Scheduled source-link and evidence freshness checks.

Pin third-party actions to immutable commit SHAs where practical. Avoid a single shared workflow that makes every repository fail for irrelevant checks; compose small workflows by project type.

### 5.2 Minimum repository health contract

Every actively maintained repository should have:

- A concise README with purpose, intended users, status, limitations and support route.
- A clear licence and contribution policy appropriate to its content.
- A security policy and private vulnerability-reporting route.
- A CODEOWNERS or equivalent ownership declaration where appropriate.
- CI that passes on the default branch.
- Dependency and secret scanning appropriate to its stack.
- A documented release/deployment process and rollback route.
- Tests for critical business rules and data transformations.
- Accessibility expectations for user-facing interfaces.
- A data/provenance statement where external evidence or data is used.
- A lifecycle tier and next review date.

### 5.3 Evidence lifecycle

Every time-sensitive external claim should carry its source and verification date. Create a common process to flag:
- sources that return errors or redirects;
- sources not reviewed within their expected interval;
- changed legal/policy documents;
- contradictory sources;
- claims without an authoritative source;
- evidence that is illustrative, inferred or modelled rather than observed.

Do not automatically delete stale evidence. Mark it stale, preserve the audit trail and request review.

## 6. Portfolio lifecycle model

Assign each repository one explicit tier:

| Tier | Meaning | Minimum expectation |
|---|---|---|
| Flagship | Core strategic product or infrastructure | Monthly review, release discipline, user feedback and clear roadmap |
| Active | Maintained product or service | Passing CI, quarterly review, issue triage and owner |
| Incubating | Experiment or proof of concept | Time-boxed hypothesis, success criteria and decision date |
| Maintenance | Useful but not actively expanding | Security/dependency fixes, link checks and clear support boundary |
| Archived | No longer maintained | Archive notice, successor link and preserved history |

Do not infer maturity from commit count, repository age, stars or a badge alone.

## 7. Proposed sequencing

### Phase 0 — Baseline and safety (first)
- Verify the full owned-repository inventory, including pagination and private/archived status.
- Capture default branch, tags/releases, open PRs/issues, workflows, dependencies and current branch protections.
- Identify secrets, personal data and sensitive data flows without copying sensitive values into reports.
- Map external links, consumers, deployments and domain dependencies.
- Record a baseline so later reports can measure improvement.

**Exit condition:** every repository has an owner, purpose, visibility, lifecycle tier and known dependency map.

### Phase 1 — Stabilise (next)
- Fix failing default-branch checks and release-blocking accessibility/privacy defects.
- Resolve high-risk provenance and source freshness issues.
- Ensure every active repo has a security policy and correct private reporting route.
- Separate private/public build inputs and audit token permissions.

**Exit condition:** flagship and active repositories have passing required checks and no untriaged critical/high-risk issue.

### Phase 2 — Integrate shared foundations
- Define project metadata and evidence/provenance schemas.
- Publish common reusable CI workflows and accessibility checks.
- Agree shared design tokens and component boundaries.
- Introduce machine-readable service/repository relationships.

**Exit condition:** at least the discovery, governance and data-management families consume the same versioned contracts.

### Phase 3 — Integrate product experiences
- Catalogue publishes verified records that Tech Hub can curate.
- Observatories and OpenGovernment UK expose provenance-aware records to NDL PubSec MCP.
- DAM playbooks, Policy Explorer, Data Quality Commons and CDO Connect Hub share taxonomy and evidence references.
- govukOS consumes services through documented contracts rather than absorbing their codebases.

**Exit condition:** at least two real cross-repository user journeys work end-to-end and are tested.

### Phase 4 — Retire duplication
- Archive superseded repositories only after successor links and consumer checks.
- Remove duplicate schemas and manual copies after migration and compatibility checks.
- Retain distinct repositories when there are different owners, audiences, release cadences, legal obligations or security classifications.

**Exit condition:** every consolidation has a migration note, redirect plan, rollback point and explicit maintainer approval.

## 8. Decision rules for any actual repository merge

A merge is justified only when all are true:

1. The repositories serve substantially the same users and purpose.
2. They share the same security/data classification and access model.
3. They have compatible licences and ownership.
4. Their release cadence and deployment model are compatible.
5. The merge reduces real duplication rather than creating a larger coupled codebase.
6. A migration plan covers history, issues, PRs, tags, releases, links, deployments and downstream consumers.
7. The target repository has capacity and clear ownership.

Prefer integration over merging when the projects have distinct audiences, different trust boundaries, separate deployments, independent standards governance or different data sensitivity.

## 9. Immediate decision register

| Decision | Proposed disposition | Approval needed before execution |
|---|---|---|
| Asset Catalogue and Public Sector Tech Hub | Keep separate; share metadata, ingestion and verification | No merge; agree API/schema |
| Public and internal catalogue | Preserve separate trust boundaries | Explicit security review before any shared data |
| Legacy Code Observatory | Keep redirect; consider archive after link/dependency audit | Yes, before archiving |
| DAM Policy Explorer | Keep for now; assess user overlap with Playbooks | User evidence before any merge |
| DAM Returns Pipeline and CDO Connect Hub | Separate systems; integrate via controlled contract | Security/data-flow review |
| NDL public and private MCP | Keep separate | Explicit security approval for any code/data transfer |
| govukOS and component projects | Keep distinct; integrate by API/contracts | Architecture and threat-model review |
| Innovation Lab / Desktop Tutorial | Decide incubating, maintenance or archive | Owner confirmation and consumer check |
| Whole-life 360 / Young Person 360 | Keep separate; share non-identifying taxonomy only | Safeguarding/privacy review |

## 10. Measures of success

Track outcomes rather than repository volume:

- Percentage of active repositories with passing default-branch checks.
- Percentage with a current security policy, licence, owner and support route.
- Percentage of evidence records within review date.
- Broken-source rate and median time to resolve.
- Accessibility defects by severity and time to remediation.
- Number of duplicated schemas/components retired.
- Number of verified cross-project integrations.
- User task success, repeat use and external contributions.
- Time spent maintaining duplicated workflows and data.
- Number of repositories with no owner or no declared lifecycle.

## 11. What this plan does not authorise

This proposal does not authorise deletion, archival, public release of private content, transfer of sensitive data, default-branch rewrites, force pushes, licence changes, secret changes, production deployments or merging of pull requests. Those require a separate, explicit review of the exact repository and proposed change.

---

**Bottom line:** preserve product boundaries; consolidate standards, metadata, evidence handling and engineering automation. Integrate by stable contracts first. Merge only when user purpose, ownership, security classification, release cadence and maintenance responsibility genuinely align.
