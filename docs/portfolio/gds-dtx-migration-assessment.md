# GDS-DTX migration and organisation-transition assessment

**Status:** Initial evidence-based assessment; migration execution gated on organisational sponsorship and access  
**Prepared:** 28 November 2026  
**Target organisation:** `gds-dtx`  
**Source estates reviewed:** public `cyberdudeuk` portfolio and discoverable `co-cddo` repositories  
**Important boundary:** this document covers public repository metadata and public content only. Private and OFFICIAL/OFFICIAL-SENSITIVE work requires a separate restricted migration register and approved handling.

## 1. Executive recommendation

Treat the move to `gds-dtx` as an estate transition, not a bulk GitHub transfer and not a monorepo exercise.

- Preserve distinct products and their histories. Transfer an existing repository where it is the same product and the destination owner accepts it; recreate only where the destination needs a materially different operating model, access boundary or canonical identity.
- Do not merge unrelated products simply because they share an organisation.
- Reuse existing `gds-dtx` capabilities where the fit is demonstrated, but do not overwrite or absorb existing repositories without their maintainers' agreement.
- Keep public, internal, private and OFFICIAL handling boundaries intact. Repository visibility must never be widened as a side effect of migration.
- Maintain old URLs and a transition period. Update references, workflows, Pages, package consumers, MCP clients, documentation, badges and external links before retiring source locations.
- Obtain an accountable GDS-DTX sponsor, receiving repository owner, data/records owner and security/IG approval before any transfer or recreation of government-related work.

## 2. Access and authority findings

The connected GitHub identity is not currently returned by GitHub's organisation-membership listing. Repository discovery can nevertheless return public `gds-dtx` and `co-cddo` metadata. This is not equivalent to organisation membership or authority to transfer repositories.

- The `co-cddo` inventory contains many unrelated repositories. Most discovered repositories are read-only to this connection. A small subset exposes push permission; `co-cddo/MoG-Navigator` exposes repository-admin permission.
- `gds-dtx` search exposes repository metadata, including potentially related `data-asset-management-hub` and `legacy-register`. Direct repository metadata/content requests for those internal repositories returned 404 in this connection, so their internal implementation and ownership could not be validated.
- The available GitHub connector exposes repository reads and ordinary content/PR operations, but no repository-transfer or organisation-administration action. It cannot execute the organisation transfer.
- Therefore this review can identify candidates, dependencies and migration packs, but cannot complete transfers, create receiving repositories in the organisation, alter team permissions, or validate organisation-level policies.

A transfer must be initiated by an account with the necessary source-repository administration and target-organisation permissions. Before scheduling, confirm the destination organisation's acceptance, naming, visibility, team access, Actions policy, Pages policy, rulesets, secret/environment handling, package permissions and billing limits.

## 3. Evidence-backed `co-cddo` workstream inventory

The organisation search returned a broad estate. The following classification distinguishes direct contribution evidence from mere repository visibility or collaborator access.

| Repository | Evidence observed | Initial disposition |
|---|---|---|
| `co-cddo/MoG-Navigator` | Public; this account has repository-admin permission. Commit search for `author:cyberdudeuk` returned multiple substantive July 2026 commits, including the autonomous module, source-feed process, standalone app and MOG-1.2.0 release. README explicitly says it is not commissioned by, endorsed by or affiliated with a government department. | **Primary migration candidate, subject to sponsorship decision.** Prefer a GitHub repository transfer if GDS-DTX formally accepts ownership and the public status/disclaimer is reconciled. If the organisation needs a different governance or release boundary, create a controlled successor and preserve the original as a clearly signposted historical source. Do not imply government endorsement merely by moving it. Revalidate scheduled-workflow state after migration; the existing harvester is a safe dry-run, not a live feed. |
| `co-cddo/ocdo-data-foundations` | Public; this account has push but not admin permission. Author-filtered commit search found a basic CI workflow commit (3 August 2026). README is only a title stub; repository size is 3 KB. | **Do not migrate as a live product yet.** Establish purpose, owner and whether substantive content exists. If it is only a starter/placeholder, retain as history or close out through the source owner rather than creating an empty duplicate. |
| `co-cddo/ukgov-metadata-exchange-model` | Public; push but not admin permission. The README describes the cross-government metadata model, LinkML source, generated JSON Schema/SHACL and GitHub Pages deployment. Author-filtered commit search found historical 2023 changes, not recent direct ownership evidence. | **Critical dependency / stakeholder-led migration.** It is a standards/source-of-truth asset, not a personal repository to move unilaterally. Confirm successor ownership with CDDO/GDS standards owners. Preserve the canonical model and existing consumers; NDL PubSec MCP must continue to respect the currently endorsed model until a formal standards decision. |
| `co-cddo/federated-api-model` | Public; push but not admin permission. README describes the Data Standards Authority's federated API discovery model and a project backlog. No direct authored commit was returned by the targeted author search. | **Dependency/ownership review.** Move only through the responsible programme/maintainer decision; do not assume repository access equals ownership. |
| `co-cddo/future-data-architecture` | Public; push but not admin permission. README describes GDS future data architecture resources and a published static site. No direct authored commit was returned by the targeted author search. | **Dependency/ownership review.** If still authoritative, migrate with its site/domain and link dependencies; otherwise preserve as an archive/redirect under the source owner's decision. |
| Other visible `co-cddo` repositories | Many additional repositories are discoverable, but most are read-only and no evidence establishes them as this portfolio's work. | **Out of migration scope unless a named workstream owner confirms responsibility.** Do not bulk-transfer the organisation's estate. |

The commit search was targeted and is evidence of some contributions, not a complete audit of every historical commit, issue, project board, deployment or external dependency.

## 4. Mapping the public portfolio to GDS-DTX

The following is a first-pass destination assessment. “Candidate” means the work appears relevant to a GDS-DTX public-sector engineering/data portfolio; it does not mean the receiving organisation has accepted it.

| Source repository | Proposed route | Rationale / gate |
|---|---|---|
| `ai-capability-governance` | Candidate for transfer or governed recreation | Public-sector AI governance; compare with existing GDS-DTX AI governance/security work before choosing a destination. |
| `ndl-pubsec-mcp` | Candidate for transfer | Public-sector dataset discovery/metadata validation; retain a distinct MCP product and its standards-version boundary. |
| `dq-commons` | Candidate for transfer | Reusable data-quality toolkit and provenance/assessment contracts; retain as its own product. |
| `dam-capability-playbooks` | Candidate for transfer or integration with an existing DAM hub | Guidance/playbooks are distinct from a DAM product runtime. Compare with `gds-dtx/data-asset-management-hub` before creating a duplicate. |
| `dam-policy-explorer` | Candidate for transfer or controlled recreation | Distinct policy navigation experience; assess whether it should remain an independent product or become a separately deployable module around the DAM hub. |
| `dcat-ap-uk` | Candidate for transfer, subject to standards sponsorship | Proposed profile only; preserve its explicit proposed/not-endorsed status and decision history. |
| `legacy-technology-observatory` | Candidate for transfer or integration with the existing legacy register | Observatory evidence and the GDS-DTX `legacy-register` may be complementary or overlapping; compare schema, stewardship, source-of-truth and user tasks before deciding. |
| `opengovernment-uk` | Candidate for transfer | Public-body/accountability register; establish canonical record ownership, source licences, refresh process and data governance. |
| `pubsec-tech-hub` | Candidate for transfer | Public-sector technology adoption catalogue; preserve the distinction from the code-reuse catalogue and legacy observatory. |
| `github-repos-asset-catalogue` | Candidate for transfer | Public-sector code discovery; keep distinct from product/adoption catalogues. |
| `knowledge-web` | Conditional candidate | Domain-neutral knowledge map; move only if its intended stewardship and audience are GDS-DTX-aligned. |
| `uk-youth-parliament-amplify`, `young-person-360`, `earning-learning-training`, `start-a-business-uk` | Conditional candidates | Public-facing service experiences; require service owner, safeguarding, user research, privacy, content and hosting approval before migration. Preserve independent product boundaries. |
| `black-mixed-heritage`, `awards-and-recognition-hub`, `plainspoken` | Retain separately unless explicitly commissioned as GDS-DTX work | Distinct community/editorial, awards and coaching purposes; do not infer organisational ownership from technical relevance. |
| `cyberdudeuk.github.io`, `cyberdudeuk`, `.github` | Split/recreate selectively; retain personal account surfaces where needed | The launchpad and profile are personal account surfaces, not automatically GDS-DTX properties. Recreate a work-only catalogue under the organisation if accepted; keep personal links/redirects stable. |
| `w3id.org` | Do not transfer | External W3C Permanent Identifier Community Group governance; retain its independent ownership and decision process. |
| `legacy-code-observatory` | Keep redirect until verified, then archive only with owner approval | Redirect-only predecessor; verify old GitHub Pages URL and inbound references before any lifecycle action. |

Private repositories are deliberately excluded from this public table. Their migration decisions must be recorded in a restricted register, using the approved information-handling model. In particular, no OFFICIAL/OFFICIAL-SENSITIVE source, data or operational material should be copied into a public destination.

## 5. Existing GDS-DTX repositories to assess before creating destinations

- `gds-dtx/data-asset-management-hub`: likely related to DAM Capability Playbooks and DAM Policy Explorer. Its internal README/content could not be inspected through this connection (repository metadata/content request returned 404). Treat as a potential existing platform, not as a confirmed equivalent or merge target.
- `gds-dtx/legacy-register`: likely related to Legacy Technology Observatory. Its internal README/content could not be inspected through this connection. Compare scope and ownership before deciding whether the observatory should feed the register, be a separate product, or be recreated.
- `gds-dtx/engineering-standards`: public README describes 69 draft/MVP engineering standards and a context-aware standards toolchain. This may provide reusable engineering practice, but it is not a substitute for product-specific assurance or a reason to merge repositories.
- `gds-dtx/schemas`: public README explicitly warns that the proposed schema platform is work in progress and not for production. Do not silently move production schemas or treat it as an approved canonical schema service.

## 6. Transfer versus recreate: decision rules

**Prefer transfer** when the repository remains the same product, its history/issues/PRs/releases are valuable, ownership is accepted by GDS-DTX, and the same security classification and operating model remain appropriate. A GitHub transfer normally preserves the repository identity/history and redirects the old URL, but integrations and permissions still need validation.

**Prefer recreate with controlled migration** when the destination requires a different visibility or security boundary, new service ownership, different CI/CD or deployment, removal of personal/non-work material, a new canonical data model, or a formal product re-baseline. Preserve source commit provenance and document what was intentionally not copied (for example, secrets, private data, obsolete workflows or personal issue discussions). Do not flatten history without a recorded reason.

**Keep separate** when purpose, users, standards governance, licence, data classification, service owner or release lifecycle differ. Integration should use versioned interfaces and stable identifiers.

## 7. Mandatory migration controls and runbook

For each accepted repository, create a migration record containing:

1. **Ownership and authority:** source owner/admin, receiving owner/team, accountable service owner, sponsor, records owner and approvals.
2. **Classification and licence:** current visibility, information classification, personal data, special-category data, Crown copyright/licence, third-party licences and data-sharing constraints.
3. **Technical baseline:** default branch, all branches/tags/releases, LFS usage, submodules, GitHub Pages/custom domains, packages, deployments, environments, Actions workflows, reusable workflow references, secrets/variables (names only), webhooks/apps, Dependabot, CodeQL, rulesets and branch protection.
4. **Collaboration state:** open issues/PRs, project boards, discussions, milestones, releases, collaborators/teams and required audit/records retention.
5. **Consumer map:** source-code references, raw GitHub URLs, badges, README/docs links, package coordinates, MCP/client configuration, API consumers, data feeds, DNS, OAuth callbacks and scheduled jobs.
6. **Target readiness:** receiving repo name, visibility, teams, rulesets, Actions permissions, environments, secrets re-provisioned through approved channels, Pages settings, package access, CODEOWNERS, support route and incident ownership.
7. **Execution:** freeze window, final source snapshot, transfer/recreation, update consumers, smoke tests, deployment validation and rollback/forward-fix plan.
8. **Closure:** verify old URLs/redirects, release artefacts, branch protection, permissions, audit trail, monitoring, owner acceptance and source-repo archive/retention decision.

Never copy secrets into Git, issues or this migration document. Recreate secrets and environment values only through approved secret-management channels. Validate GitHub Pages, Actions, packages and webhook integrations explicitly after a transfer; do not assume they all continue unchanged.

## 8. Sequenced programme

### Gate 0 — confirm scope and sponsorship
- Obtain a named GDS-DTX sponsor and receiving team for each workstream.
- Obtain the deprecation date/plan and accountable transition lead for `co-cddo`.
- Ask the source organisation's administrators for an authoritative list of repositories requiring transfer, including private/internal repositories and archives.
- Confirm whether the requirement applies to all workstream repositories, or only those owned/maintained by the user and receiving team. Do not migrate unrelated CDDO repositories.

### Gate 1 — complete restricted inventory
- Build a private migration register for the 11 private repositories in the cyberdudeuk estate and any private/internal co-cddo repositories in scope.
- Follow the approved handling model; no source inspection of OFFICIAL/OFFICIAL-SENSITIVE repositories without explicit authorisation.
- Verify open PRs/issues, data classification, deployment, secrets, integrations, and target access.

### Gate 2 — resolve overlaps and destination design
- Compare DAM products with `data-asset-management-hub`.
- Compare Legacy Technology Observatory with `legacy-register`.
- Map DQ Commons, xGov MEM, DCAT-AP-UK, NDL MCP and existing GDS-DTX schema/standards capabilities without conflating endorsed and proposed standards.
- Confirm destination names, visibility and ownership before any new repository is created.

### Gate 3 — migrate in waves
1. Low-risk public documentation and standalone tools with no production consumers.
2. Public data/standards products after source-of-truth and consumer mapping.
3. Public-facing services after service, safeguarding, privacy and hosting approval.
4. Private/internal systems only after classification, security and environment approvals.
5. OFFICIAL/OFFICIAL-SENSITIVE material only through the approved restricted migration route.

### Gate 4 — decommission source locations
Only after receiving-owner acceptance and successful consumer/deployment checks. Preserve redirect/history and records obligations; do not delete by default.

## 9. Current blockers and outstanding decisions

| Item | Current status | Required action |
|---|---|---|
| GDS-DTX organisation access | No organisation membership returned; internal repository reads return 404; no transfer action exposed | Obtain approved organisation membership/permissions and receiving-team sponsorship. |
| CDDO deprecation | User reports organisation is being deprecated; no authoritative sunset date or repository transfer schedule was available in this review | Obtain the official deprecation timeline and repository disposition list from CDDO administrators. |
| MoG Navigator | Strong direct-work candidate; source repository admin permission available; explicit non-government disclaimer in README | GDS-DTX sponsor must decide whether to accept, transfer, or retain as an independent public project. |
| xGov MEM and federated API model | Important standards/integration dependencies; collaborator push access does not establish ownership | Standards/programme owner to determine successor home and consumer transition. |
| DAM hub and legacy register | Potential existing destinations; internal content could not be reviewed | Obtain access and perform a deeper comparison before creating or merging anything. |
| Private work | Excluded from public report | Complete restricted inventory and approvals before moving any private or protected content. |

## 10. Non-authorisations

This assessment does not authorise bulk transfer of the `co-cddo` organisation, moving repositories without source/target admin approval, merging products, deleting or archiving source repositories, changing visibility, copying protected data, changing production deployments, changing billing, or transferring any repository into an organisation without a named receiving owner.

**Target principle:** one accountable GDS-DTX home for each accepted workstream, distinct repositories for distinct products, preserved provenance and history, and no loss of service or governance during the transition.
