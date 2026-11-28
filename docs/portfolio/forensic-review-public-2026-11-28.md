# Public portfolio forensic review

**Review date:** 28 November 2026  
**Status:** Evidence review; no production changes authorised  
**Coverage:** The 23 public repositories visible under the account at the time of review. Private project names, content and operational details are intentionally excluded from this public report.

## 1. Executive conclusion

The evidence does **not** support merging the public portfolio into a monorepo or combining the main products. The repositories represent different product types and data domains: code discovery, software adoption, legacy risk, public-body accountability, data quality, metadata standards, AI governance, knowledge mapping and audience-specific public services.

The strongest opportunity is to integrate by stable contracts:

- project metadata and product declarations;
- evidence and provenance;
- stable public-body and dataset identifiers;
- data-quality assessment outputs;
- standards mappings with explicit status and version;
- glossary ownership and routing;
- accessibility, security and release checks.

The clearest low-risk consolidation is to remove duplicated *maintenance effort*, not repository boundaries. The 360º glossary copy should be checked automatically against its canonical launchpad source. The profile README should continue to be generated from the launchpad rather than maintained independently. The redirect-only Legacy Code Observatory should be archived only after its redirect and inbound links have been verified.

## 2. Method and limits

The review used GitHub repository metadata, default-branch README files, root and recursive repository trees, selected source-of-truth files, integration references, workflow definitions, recent Actions run metadata, and selected open issue/pull-request records.

It checked:
- repository purpose, audience and declared maturity;
- product boundaries and explicit architecture decisions;
- code/data/standards source-of-truth files;
- integration and duplication references;
- presence of tests, workflows, schemas and build manifests;
- recent CI and deployment outcomes;
- licences, provenance, accessibility and security documentation where declared.

This was not a line-by-line source-code audit. Code was not checked out and executed locally; external deployment tenants, production data, secrets, private services and live user journeys were not independently tested. A green workflow is evidence that its configured checks passed, not proof of security, accessibility or service readiness. Private material is deliberately not reproduced in this public artifact.

## 3. Product-family findings

### 3.1 Discovery, adoption and modernisation

These products have explicit, complementary roles and should remain distinct.

| Repository | Observed purpose | Decision |
|---|---|---|
| [github-repos-asset-catalogue](https://github.com/cyberdudeuk/github-repos-asset-catalogue) | Inventory and plain-English discovery of public-sector code that may be reused; includes an offline-capable public catalogue | **Keep distinct.** It is a code/repository inventory, not an adoption marketplace. |
| [pubsec-tech-hub](https://github.com/cyberdudeuk/pubsec-tech-hub) | Adoption catalogue for products, platforms and components public bodies make and run | **Keep distinct; integrate metadata.** Its README describes a separate adoption task and a publiccode.yml harvest. |
| [legacy-technology-observatory](https://github.com/cyberdudeuk/legacy-technology-observatory) | Evidence and analysis about legacy technology beyond code: networks, devices, operational technology, skills and migration | **Keep distinct; integrate links and keys.** It already cross-links to the other discovery products. |
| [opengovernment-uk](https://github.com/cyberdudeuk/opengovernment-uk) | Sourced register of public bodies, accountability, funding and ownership, with machine-readable feeds | **Keep distinct; integrate by identifiers and feeds.** It is a register domain, not a software catalogue. |
| [cyberdudeuk.github.io](https://github.com/cyberdudeuk/cyberdudeuk.github.io) | Public launchpad built from `data/projects.json`; also hosts the shared glossary and routing data | **Keep as the portfolio directory.** It is not a replacement for the specialist catalogues. |
| [legacy-code-observatory](https://github.com/cyberdudeuk/legacy-code-observatory) | README and site files state that it only redirects to Legacy Technology Observatory | **Redirect now; archive later.** Verify inbound links and GitHub Pages behaviour first. |

The three-way distinction between code to reuse, products to adopt and legacy to replace is explicitly documented by the projects themselves. OpenGovernment UK adds public-body accountability and ownership, a different data domain. Combining these would blur rather than simplify the user journeys.

The Tech Hub README states that its 24 November 2026 snapshot had twelve UK repository listings and none supplied a `publiccode.yml`; the initial listings were therefore curated and labelled as such. Keep that distinction visible. Do not fabricate harvested metadata or silently change curated records into verified declarations.

### 3.2 Data management, quality and interoperability

| Repository | Observed purpose | Decision |
|---|---|---|
| [dam-capability-playbooks](https://github.com/cyberdudeuk/dam-capability-playbooks) | Specialist DAM capability guidance, policy interpretation, learning and implementation pathways | **Keep distinct; integrate guidance and references.** |
| [dam-policy-explorer](https://github.com/cyberdudeuk/dam-policy-explorer) | Focused navigation and support for the DAM Policy, including a return journey | **Keep distinct.** It is a narrower user-facing policy experience. |
| [dq-commons](https://github.com/cyberdudeuk/dq-commons) | Executable data-quality toolkit, rules, packs, portfolio assessment and machine-readable results | **Keep distinct; integrate outputs.** Its engine and assessment model are not just guidance content. |
| [dcat-ap-uk](https://github.com/cyberdudeuk/dcat-ap-uk) | YAML-led source of truth generating a proposed UK DCAT application profile, SHACL, JSON Schema, contexts and validation artefacts | **Keep distinct; protect proposal status.** |
| [ndl-pubsec-mcp](https://github.com/cyberdudeuk/ndl-pubsec-mcp) | Read-only TypeScript MCP server for public-sector dataset discovery and metadata validation against xGov MEM | **Keep distinct; integrate read-only feeds.** |

There is already meaningful integration:
- DAM Capability Playbooks says its sector supplements include quality rules the Data Quality Commons kit can run.
- Its learning pathways signpost Data Quality Commons, DCAT-AP-UK, xGov MEM, NDL PubSec MCP, the Asset Catalogue, AI Capability Governance and Knowledge Web.
- Data Quality Commons contains a machine-readable NDL chart-data portfolio definition and generated quality-assessment artefacts.
- NDL PubSec MCP is a dataset discovery and metadata-validation layer, not the authoritative data store.

Do not merge these tools. Share dataset identifiers, policy/requirement references, rule identifiers, provenance and assessment-result formats.

**Standards caution:** DCAT-AP-UK 1.3.0-rc.1 describes itself as proposed and not endorsed. Its profile explicitly says the xGov MEM remains the endorsed model until a formal decision. NDL PubSec MCP should not silently replace its current xGov MEM validation with the proposed profile. Any future mapping should be versioned and clearly labelled.

### 3.3 AI governance and knowledge

| Repository | Observed purpose | Decision |
|---|---|---|
| [ai-capability-governance](https://github.com/cyberdudeuk/ai-capability-governance) | Public guidance and tools for governing AI and AI use in public services | **Keep distinct; integrate vocabulary and references.** |
| [knowledge-web](https://github.com/cyberdudeuk/knowledge-web) | Offline, ontology-backed knowledge map with controlled vocabularies and declared knowledge gaps | **Keep distinct.** It is a reusable knowledge/navigation layer, not an AI governance product. |

The right integration is through shared concepts, metadata and knowledge exports. Combining the repositories would couple a governance product to a domain-neutral knowledge engine unnecessarily.

### 3.4 People, participation and public-good services

| Repository | Observed purpose | Decision |
|---|---|---|
| [uk-youth-parliament-amplify](https://github.com/cyberdudeuk/uk-youth-parliament-amplify) | Youth voice portal, local routes map and petition snapshot | **Keep distinct.** It has its own audience and safeguarding context. |
| [young-person-360](https://github.com/cyberdudeuk/young-person-360) | Evidence-led view of children and young people held, lost or unseen by systems | **Keep distinct; cross-link.** |
| [earning-learning-training](https://github.com/cyberdudeuk/earning-learning-training) | Routes into work, learning, training and self-employment for ages 16–24 | **Keep distinct; cross-link.** |
| [start-a-business-uk](https://github.com/cyberdudeuk/start-a-business-uk) | Sourced, multi-page journey for starting and running a business in the UK | **Keep distinct; cross-link.** |
| [black-mixed-heritage](https://github.com/cyberdudeuk/black-mixed-heritage) | Year-round Black history, heritage and culture hub with its own editorial and community context | **Keep distinct.** |
| [awards-and-recognition-hub](https://github.com/cyberdudeuk/awards-and-recognition-hub) | Sourced awards calendar, recognition guidance and nomination workflows | **Keep distinct.** |
| [plainspoken](https://github.com/cyberdudeuk/plainspoken) | Phone-first speaking coach with practice routines, progress and local data controls | **Keep distinct.** |

These are not interchangeable applications. Their users, subject matter, privacy expectations and editorial/safeguarding requirements differ. Reuse accessible components and build practices, not content or data stores.

The three published life-course portals already define ownership of topics and use a shared glossary/routing model. The launchpad's `data/shared-glossary.json` and the copy in Starting a Business UK had the same Git blob SHA during this review. That proves the copies matched at the review point, not that future updates are automatically propagated. Add a hash/freshness check or generate the copy from the canonical source.

### 3.5 Portfolio foundations and external infrastructure

| Repository | Observed purpose | Decision |
|---|---|---|
| [cyberdudeuk](https://github.com/cyberdudeuk/cyberdudeuk) | GitHub profile README generated from the launchpad's project data | **Keep distinct; retain one-way generation.** |
| [.github](https://github.com/cyberdudeuk/.github) | Default community health files for repositories without project-specific files | **Keep as defaults.** Do not centralise project-specific licences or security instructions here. |
| [w3id.org](https://github.com/cyberdudeuk/w3id.org) | Permanent identifier redirect service operated by the W3C Permanent Identifier Community Group | **Keep under its external governance.** It is not an internal service to absorb. |

DCAT-AP-UK records a proposed w3id namespace and a submitted redirect request. Treat identifier resolution as dependent on the external community's decision; do not present proposed identifiers as live until confirmed.

## 4. Engineering and CI observations

Recent workflow metadata inspected on 28 November showed successful recent main-branch runs for the public Asset Catalogue, Public Sector Tech Hub, Legacy Technology Observatory, AI Capability Governance, Data Quality Commons, DAM Capability Playbooks, DCAT-AP-UK and Black History and Heritage Hub. Recent checks for OpenGovernment UK, Plainspoken and the published life-course portals were also successful in the sampled runs.

The NDL PubSec MCP main-branch push run inspected on 28 November succeeded. A Dependabot pull-request run failed at its dependency-install step. Treat this as a PR-specific dependency issue, not as evidence that the main branch was failing.

The launchpad proposal PR's dependency review, documentation-kit and CodeQL checks passed; the main Checks workflow was still in progress when this report was prepared.

These are point-in-time CI observations. They do not establish full production readiness or prove that unconfigured risks are absent.

## 5. Recommended shared foundations

1. **Project metadata contract:** use launchpad project data for the launchpad; use publiccode.yml where a project is genuinely publishing software for reuse and the declaration is appropriate.
2. **Evidence contract:** source, publisher, authority, retrieval date, verification date, confidence, claim type, review date and supersession state.
3. **Identifier contract:** use owning-register identifiers rather than name matching; publish aliases and effective dates.
4. **Quality-result contract:** rule ID, dataset ID, severity, result, method, timestamp, provenance and remediation state.
5. **Standards status contract:** distinguish endorsed, proposed, draft, deprecated and locally adopted profiles.
6. **Accessibility and service-health contract:** audit date, WCAG target, known issues, user research and operational status.

## 6. Prioritised actions

| Priority | Action | Why |
|---|---|---|
| 1 | Add a CI integrity check for the shared glossary copy | Low-risk, prevents silent drift across the life-course portals |
| 2 | Document the discovery trio's shared keys and feed contracts | The three products are already linked but have separate data purposes |
| 3 | Define a small provenance schema that can be mapped into existing formats | Improves evidence traceability without forcing a new universal data model |
| 4 | Publish a clear standards-status field in integrations | Prevents proposed DCAT-AP-UK material being mistaken for an endorsed standard |
| 5 | Integrate DQ Commons outputs with DAM/NDL references by identifiers | Strong value with low coupling |
| 6 | Keep the profile README generated from launchpad data | Avoids duplicate manual project inventories |
| 7 | Archive the redirect-only Legacy Code Observatory only after URL checks | Removes obsolete maintenance without breaking old links |
| 8 | Reassess reusable CI workflows as small opt-in components | Avoids forcing different technology stacks through one oversized pipeline |

## 7. Merge decision

**No public product repository is recommended for immediate merging.** The evidence supports integration by contracts and a small number of low-risk duplication controls. The redirect-only Legacy Code Observatory is an archive candidate, not a merge candidate.

Before any repository is merged or archived, verify licence compatibility, issue/PR history, releases, tags, URLs, downstream consumers, deployments, data classification, owners and rollback.

## 8. What this review does not authorise

No repository has been merged, archived, deleted, made public, had its default branch rewritten or had production code changed as part of this review. This report is an evidence-based proposal only.
