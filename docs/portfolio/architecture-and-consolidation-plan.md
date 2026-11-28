# Public portfolio architecture and consolidation plan

**Status:** Proposed for maintainer review  
**Prepared:** 28 November 2026  
**Scope:** Public repositories in the cyberdudeuk account  
**Decision principle:** one coherent ecosystem; separate repositories wherever separation creates genuine value.

This is a public-facing proposal. It intentionally excludes private repository names, private project details and non-public operational information. A separate due-diligence review of private work is not published here.

## 1. Executive recommendation

Do not combine the public portfolio into one monorepo. The projects have materially different users, data domains, technology stacks, licences, release cadences and governance requirements. Consolidate shared *contracts and engineering practices* instead: project metadata, provenance, stable identifiers, accessibility checks, security defaults, release conventions and machine-readable integration formats.

The public portfolio falls into these families:

1. **Discovery and adoption:** GitHub Repos Asset Catalogue, Public Sector Tech Hub, Legacy Technology Observatory, OpenGovernment UK and the account launchpad.
2. **Data management and interoperability:** DAM Capability Playbooks, DAM Policy Explorer, Data Quality Commons, DCAT-AP-UK and NDL PubSec MCP.
3. **AI governance and knowledge:** AI Capability Governance and Knowledge Web.
4. **People, participation and public-good services:** UK Youth Parliament: Amplify, Young Person 360, Earning, Learning and Training, Starting a Business UK, Black History and Heritage Hub, Awards and Recognition Hub, and Plainspoken.
5. **Portfolio foundations:** cyberdudeuk.github.io, the profile repository and .github community defaults.
6. **External community infrastructure:** w3id.org, which has its own W3C community governance and must not be treated as an internal portfolio component.

## 2. Merge, keep separate, or integrate?

| Relationship | Recommendation | Evidence and rationale |
|---|---|---|
| GitHub Repos Asset Catalogue ↔ Public Sector Tech Hub | **Keep separate; integrate** | Their own READMEs define different jobs: code that exists and may be reused versus products and components public bodies make and run that may be adopted. The Tech Hub harvests publiccode.yml where available and labels curated entries. |
| Asset Catalogue ↔ Legacy Technology Observatory | **Keep separate; integrate** | The catalogue helps discover reusable code; the observatory assesses legacy technology and replacement risk. The observatory already links to catalogue keys. |
| Public Sector Tech Hub ↔ Legacy Technology Observatory | **Keep separate; integrate** | Adoption and modernisation are distinct user tasks. The observatory validates its links against the Tech Hub's published addresses. |
| OpenGovernment UK ↔ NDL PubSec MCP | **Keep separate; integrate by feeds and identifiers** | OpenGovernment UK is a sourced register of public bodies, accountability, funding and ownership. NDL PubSec MCP discovers public-sector datasets and metadata. Their data domains overlap at the edges, not at the product level. |
| DAM Capability Playbooks ↔ DAM Policy Explorer | **Keep separate initially; align content contracts** | Playbooks provide specialist capability guidance and learning; the Explorer is a focused policy navigation and return-support experience. Share policy identifiers, requirement references and provenance, not application code by default. |
| DAM Capability Playbooks ↔ Data Quality Commons | **Keep separate; integrate** | The Playbooks describe capability and methods; Data Quality Commons provides an executable quality toolkit, rules, packs and assessments. The Playbooks already signpost quality rules that the Commons kit can run. |
| Data Quality Commons ↔ NDL PubSec MCP | **Keep separate; integrate outputs** | One assesses data quality; the other discovers datasets and validates metadata. Exchange provenance-aware assessment results and dataset identifiers rather than merging engines. |
| DCAT-AP-UK ↔ NDL PubSec MCP | **Keep separate; do not silently switch the validator** | DCAT-AP-UK is explicitly a proposal, not endorsed. Its own profile states that xGov MEM remains the endorsed model until a decision is made. MCP should continue to represent the current endorsed model and treat any future profile mapping as an explicitly versioned option. |
| DCAT-AP-UK ↔ w3id.org | **Separate governance; integrate identifiers** | DCAT-AP-UK has proposed a persistent namespace through w3id.org. The identifier service is run by a W3C Permanent Identifier Community Group; the portfolio cannot unilaterally control or absorb it. |
| AI Capability Governance ↔ Knowledge Web | **Keep separate; integrate by vocabulary and knowledge exports** | Governance guidance and a domain-neutral ontology-backed knowledge map are different products. Use stable concepts and machine-readable exports. |
| UK Youth Parliament: Amplify ↔ other portfolio products | **Keep separate** | It is a youth participation portal with its own audience, campaign and safeguarding context. Its README explicitly states that it sits outside another operating-environment concept, while allowing carefully chosen runtime reuse. |
| Young Person 360 ↔ Earning, Learning and Training | **Keep separate; cross-link** | They cover different age ranges and questions. The shared glossary assigns ownership of terms and routes each question to one portal. |
| Starting a Business UK ↔ Earning, Learning and Training | **Keep separate; cross-link** | Enterprise is one route into work, not the same service journey as employment, education and training. The portals already explain the boundary. |
| Black History and Heritage Hub ↔ other public-good products | **Keep separate** | Its editorial purpose, community context and governance are distinctive. Reuse technical practices, not content ownership. |
| Awards and Recognition Hub ↔ other public-good products | **Keep separate** | Award eligibility, deadlines, nomination and recognition workflows have a distinct data lifecycle and source-verification burden. |
| Plainspoken ↔ other coaching or AI products | **Keep separate** | It is a speaking-practice product with its own user data, privacy controls and learning design. |
| Launchpad ↔ profile repository | **Keep separate; retain one source of truth** | The profile README is generated from the launchpad's project data. Continue that direction; do not manually maintain two project inventories. |
| .github ↔ public repositories | **Keep as defaults only** | GitHub uses these files only when a repository has no project-specific version. Licences and project-specific security instructions remain in each repository. |
| Legacy Code Observatory ↔ Legacy Technology Observatory | **Retain redirect, then archive if safe** | The old repository says it only redirects; the successor says it was renamed when scope widened beyond code. Preserve the old URL until inbound links and Pages behaviour are checked. |

## 3. Target architecture

### 3.1 Distinct product layers

- **Source and register layer:** authoritative public registers, public-body records, project metadata, standards and evidence references.
- **Knowledge and policy layer:** DAM capability guidance, AI governance, data-quality methods, legacy evidence and metadata profiles.
- **Assessment and interoperability layer:** data-quality results, metadata validation, stable identifiers and machine-readable feeds.
- **Discovery and access layer:** Asset Catalogue, Public Sector Tech Hub, launchpad and NDL PubSec MCP.
- **Experience layer:** independently deployable products designed for their own audiences and tasks.

No user-facing application should become the accidental authoritative source for another product's data. Each data domain needs an owner, stable identifier, schema, source-of-truth declaration and change process.

### 3.2 Shared contracts to define once

1. **Project metadata:** canonical name, repository URL, service URL, owner role, audience, status, maturity, licence, accessibility statement, support route and last verified date.
2. **Content provenance:** where useful, reuse the Data Quality Commons source classes (sourced, derived, real-example, template, estimate, judgement and illustrative) and its explicit authoritative-master register. This is a content-provenance pattern, not a universal dataset-lineage schema.
3. **Dataset lineage and quality:** reuse existing Data Quality Commons identifiers and outputs (`DataAsset`, `MeasurementRun`, `RuleResult`, DQV JSON-LD) and map lineage to PROV-O and catalogue metadata through documented adapters. Define only fields that existing standards and consumers cannot already express.
4. **Public-body identifiers:** stable identifiers, aliases, jurisdiction, effective dates and source references.
5. **Data quality:** rule, severity, method, result, exception, owner and remediation state.
6. **Metadata and APIs:** versioned schema, source attribution, freshness, confidence/limitations and error semantics.
7. **Accessibility and service status:** target standard, audit date, known issues, user research date and operational status.

Prefer established standards where they fit. Do not create a bespoke schema simply to make every repository look alike.

## 4. Evidence-backed integration opportunities

### 4.1 Discovery and adoption

The three linked products already describe complementary roles: find code to reuse, find products to adopt, and understand technology that needs replacing. OpenGovernment UK adds a different register domain: public bodies, accountability and ownership. Integrate with stable identifiers and links; do not collapse these into one catalogue.

The Tech Hub's README says its harvest is based on publiccode.yml. On its 24 November 2026 snapshot, none of the twelve UK repositories it listed had supplied that file, so first listings were curated and labelled as such. Treat that as an explicit data-quality state, not a reason to invent metadata or misrepresent a curated entry as harvested.

### 4.2 Data quality, DAM and NDL

Data Quality Commons already contains relevant building blocks: `knowledge/provenance.yaml` distinguishes sourced, derived, real-example, template, estimate, judgement and illustrative content, and records authoritative masters; its data model defines `DataAsset`, `MeasurementRun` and `RuleResult`; its architecture describes DQV JSON-LD outputs and PROV-O among the standards it uses. DAM Capability Playbooks already point users to the Commons kit and to NDL, DCAT-AP-UK, AI governance and Knowledge Web pathways. Integrate by mapping these existing concepts and outputs to consumers. Do not create a competing portfolio-wide provenance schema; add only documented adapters or genuinely missing fields.

Keep DCAT-AP-UK's proposal status explicit. Its profile states that xGov MEM remains endorsed until a formal decision. NDL PubSec MCP should not imply that the proposed profile is already the government standard.

### 4.3 Life-course and user journeys

The published youth, employment/training and business portals define distinct user tasks. The launchpad holds a shared glossary and routing model. The copy in Starting a Business UK was byte-identical to the launchpad glossary at the time of this review, but it is still a second copy. Add an automated freshness/hash check or generate the copy from the canonical file so the definitions cannot drift silently.

### 4.4 Shared portfolio metadata

The launchpad's data/projects.json is the canonical project directory for its own cards. The account profile README is generated from that source. Preserve this one-way generation relationship and avoid introducing a second manually maintained catalogue.

## 5. Engineering and assurance findings

- The public repositories use materially different architectures: Python data pipelines, TypeScript MCP tooling, YAML-led standards generation, static HTML portals and domain-specific front ends. This supports a federated portfolio, not a single monorepo.
- Strong assurance practices exist in several repositories, including explicit negative tests, accessibility workflows, CodeQL, dependency review and source-freshness checks. Reuse the practices and small compatible workflow components, not one mandatory pipeline that breaks projects with different stacks.
- Recent main-branch workflow runs inspected for the Asset Catalogue, Tech Hub, Legacy Technology Observatory, AI Capability Governance, Data Quality Commons, DAM Capability Playbooks, DCAT-AP-UK, Black History and Heritage Hub and several other public projects were successful.
- The NDL PubSec MCP main-branch push run inspected on 28 November succeeded. A Dependabot pull-request run failed at dependency installation; that is a PR-specific failure, not evidence that main was failing.
- The launchpad pull request containing this proposal has passed dependency review, documentation-kit and CodeQL checks; its main Checks workflow was still running at the time of review.

These are point-in-time observations, not a complete security audit or a guarantee that every deployment is healthy.

## 6. Repository lifecycle model

| Tier | Meaning | Minimum expectation |
|---|---|---|
| Flagship | Core public product or shared infrastructure | Monthly review, release discipline, user feedback and roadmap |
| Active | Maintained product or service | Passing checks, quarterly review, issue triage and owner |
| Incubating | Experiment or proof of concept | Time-boxed hypothesis, success criteria and decision date |
| Maintenance | Useful but not actively expanding | Security/dependency fixes, link checks and support boundary |
| Redirect/archive | Superseded or no longer maintained | Successor notice, link/consumer check and preserved history |

Do not infer maturity from commit count, repository age, stars or a conformance badge alone.

## 7. Sequencing

### Phase 0 — Baseline
- Verify public repository inventory, default branches, releases, workflows, open PRs/issues and deployment dependencies.
- Map links and data flows between the public products.
- Record baseline health and lifecycle tiers.

### Phase 1 — Stabilise
- Resolve failing default-branch checks and high-severity defects.
- Verify source freshness, accessibility and security reporting.
- Confirm public/private build inputs are separated and that no private data enters public build artefacts.

### Phase 2 — Integrate shared foundations
- Map existing project metadata, content-provenance and dataset-quality structures to consumers; version the adapters and define only demonstrable gaps.
- Add the glossary-copy integrity check.
- Establish small reusable CI components with per-project composition.
- Document stable identifiers and feed contracts.

### Phase 3 — Integrate user journeys
- Catalogue and Tech Hub exchange project metadata where appropriate.
- OpenGovernment UK and NDL MCP exchange provenance-aware register/feed references.
- DAM Playbooks, Data Quality Commons, DCAT-AP-UK and NDL MCP share rule, dataset and metadata references without conflating proposal status.
- Cross-link user-facing portals while preserving independent deployments.

### Phase 4 — Retire duplication
- Archive the redirect-only predecessor only after link and Pages checks.
- Remove duplicate metadata copies only after a reproducible migration and compatibility check.
- Keep repositories distinct where audiences, ownership, governance, deployment or data sensitivity differ.

## 8. Decision rules for any actual merge

A merge is justified only when all are true:

1. The repositories serve substantially the same users and purpose.
2. They share the same security/data classification and access model.
3. Their licences and ownership are compatible.
4. Their release cadence and deployment model are compatible.
5. The merge reduces real duplication rather than creating tighter coupling.
6. History, issues, PRs, tags, releases, links, deployments and downstream consumers have a migration plan.
7. The target repository has capacity and clear ownership.

Prefer integration over merging when products have distinct audiences, deployments, standards governance, legal obligations or data sensitivity.

## 9. What this public plan does not authorise

This proposal does not authorise deletion, archival, public release of private content, transfer of sensitive data, default-branch rewrites, force pushes, licence changes, secret changes, production deployments or merging of pull requests. Those require a separate, explicit review of the exact repository and proposed change.

---

**Bottom line:** keep products separate; consolidate contracts, provenance, metadata and engineering practices. Integrate through stable interfaces first. Merge only when the evidence proves that separate repositories no longer provide real value.

## 10. GDS-DTX organisation transition

The work-related portfolio is expected to transition to the `gds-dtx` organisation, including relevant work currently hosted under `co-cddo`. This is an ownership and service-continuity programme, not a bulk repository merge. Preserve product boundaries and select transfer, controlled recreation or retention on a repository-by-repository basis.

The public-source evidence, initial `co-cddo` workstream inventory, candidate mapping to existing GDS-DTX repositories, transfer/recreation criteria, migration controls and access blockers are recorded in [the GDS-DTX migration assessment](gds-dtx-migration-assessment.md). Private and OFFICIAL/OFFICIAL-SENSITIVE repositories are intentionally excluded from that public assessment and require a separate restricted register.

No organisation transfer, source-repository archive, visibility change or production cutover is authorised by this architecture proposal. Each move requires an accountable receiving owner, source and target administrative authority, classification/records review, consumer and deployment mapping, and successful post-migration validation.
