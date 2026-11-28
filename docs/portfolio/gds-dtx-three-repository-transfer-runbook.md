# GDS-DTX: three-repository transfer execution pack

**Prepared:** 28 November 2026  
**Target organisation:** `gds-dtx`  
**Receiving-side accountable owner:** the user (as explicitly confirmed)  
**Scope:** exactly the three repositories listed below. No other `co-cddo` repository is included.

This is the operational companion to the portfolio architecture and forensic assessment. It supersedes any wording in earlier drafts that describes a separate receiving-side sponsor as a prerequisite. The receiving-side owner is the user; the outstanding gate is the user's effective organisation-level and repository-level authority, together with source-side authority where not already present.

## 1. Execution status at this checkpoint

| Work item | Status | Evidence / next action |
|---|---|---|
| Scope and receiving owner | Complete | User confirmed only the three named CDDO repositories are in scope and that the user is the receiving-side owner. |
| Public forensic baseline | Complete for initial planning | See `cddo-migration-forensic-delta-2026-11-28.md`. Repeat immediately before execution. |
| MoG-Navigator source administration | Available to connected identity at last permission check | Source admin was true. Recheck immediately before transfer. |
| OCDO Data Foundations source administration | Blocked | Connected identity had push but not admin. Source owner/admin must grant admin or initiate transfer. |
| UK MEM source administration | Blocked | Connected identity had push but not admin. Source owner/admin must grant admin or initiate transfer. |
| GDS-DTX receiving authority | Blocked / unverified | Org membership listing returned no memberships; direct reads of `gds-dtx/data-asset-management-hub` and `gds-dtx/legacy-register` returned 404. This may be connector visibility, but receiving authority cannot be asserted. |
| Transfer operation | Not available in connected GitHub actions | No repository-transfer or organisation-administration action is exposed. |
| Migration artefacts | Portfolio-side conformance evidence prepared; source-side artefacts blocked | Per-repository 25-check reports, JSON results, badges, metadata inputs and full tree manifests are in `docs/portfolio/conformance/`; source branch creation returned HTTP 403. |
| Production/consumer cutover | Not started | No transfer, rename, visibility change, Pages cutover, workflow arming, branch deletion or standards change has been performed. |

**Do not mark any repository as migrated until the destination URL, owner, access, history, settings, integrations and consumer checks have been verified.**

## 2. Repository-specific transfer manifests

### A. `co-cddo/MoG-Navigator` — first transfer candidate

**Baseline recorded**
- Public; MIT; default branch `main`; one branch, unprotected.
- Last inspected head: `fefdc8e98d2f7e58e95483f505dc1046bec6482e`.
- No GitHub Releases and no Pages site at the recorded inspection.
- Workflows: `.github/workflows/ci.yml` and `.github/workflows/harvest.yml`.
- Harvest workflow is a dry-run with `contents: read`; keep it that way throughout migration.
- README carries an explicit statement that the project is not commissioned by, endorsed by, or affiliated with a government department. Preserve it.
- Documented reference consumer: GUVNR / Whitehall Connect reads `mog/mog-feed.json` from its own origin.

**Pre-transfer gate**
1. Recheck source admin, default branch, exact head SHA, branch/tag inventory, releases, issues, workflow state and repository visibility.
2. Confirm the receiving organisation accepts a public MIT repository and retains the non-endorsement disclaimer.
3. Confirm the exact destination repository name and the user's effective admin/owner access there.
4. Record every known feed consumer and any hard-coded repository/raw-content URLs.
5. Confirm source and target organisation policies for Actions, scheduled workflows, artifacts, Pages, webhooks, apps and repository rules.

**Transfer and post-transfer verification**
1. Use GitHub's native repository transfer process with source and destination authority. Preserve history; do not recreate unless the transfer is formally rejected and a controlled alternative is approved.
2. Confirm destination default branch and compare the destination head/tree with the recorded source snapshot.
3. Confirm the old URL redirects and that README, licence and disclaimer remain intact.
4. Run CI; confirm scheduled harvest remains dry-run and no external credential or write permission has been introduced.
5. Fetch the feed from the new canonical location and perform the documented GUVNR/Whitehall Connect consumer smoke test.
6. Update only confirmed hard-coded links and consumer configuration; retain a rollback/forward-fix record.

**Current disposition:** NOT READY under the conformance replay (MUST 7/10). Resolve SC-03, SC-04 and SC-05, then rerun the native checker before final pre-flight. Not transferred.

### B. `co-cddo/ocdo-data-foundations` — shell/prototype; decision before transfer

**Baseline recorded**
- Public; MIT; default branch `main`; approximately 3 KB.
- Two unprotected branches, `main` and `enhance/tooling-accessibility-schema`, both at `39a05f88e554884a9ab6a1975d26114f6e93c3e4`.
- Tree contains only `README.md` (23 bytes), `LICENSE` and `.github/workflows/blank.yml`.
- The workflow is a GitHub starter placeholder; it does not validate a data-foundations product.
- No releases, Pages site or issues in the recorded inspection.

**Decision gate**
1. Establish intended product scope, accountable product owner, users, expected schemas/data assets and whether substantive work exists elsewhere.
2. Determine whether this repository is an intentionally minimal seed, an abandoned scaffold, or a pointer to work held in another system.
3. Compare the intended outcome with existing GDS-DTX capabilities without assuming the inaccessible DAM hub or another repository is equivalent.
4. Choose and record one option:
   - **Transfer intact** if preserving the shell and its provenance is useful and the receiving owner explicitly wants it; or
   - **Create an approved successor** only after product scope and destination ownership are defined, preserving the source repository/history as an archival reference or redirect as appropriate.
5. Do not invent product content or present the placeholder workflow's green run as product validation.

**Authority gate:** connected identity had push but not admin permission at the last check. A source owner/admin must grant the required authority or perform the transfer.

**Current disposition:** NOT READY under the conformance replay (MUST 5/10). Establish product purpose/owner, resolve SC-01, SC-03, SC-04, SC-05 and GA-02, then decide transfer versus controlled successor. Not transferred and no successor created.

### C. `co-cddo/ukgov-metadata-exchange-model` — standards-critical

**Baseline recorded**
- Public; checked-in licence is OGL-UK-3.0; default branch `main`, protected.
- Last inspected main head: `3e6c6f5eb6dda6e90ca956d0273f3698fd584212`.
- 17 visible branches, including `gh-pages`; one prerelease `v0.1.0` dated 8 November 2023; 32 open issues at inspection.
- Published Pages URL: `https://co-cddo.github.io/ukgov-metadata-exchange-model/`.
- Docs deployment publishes from `main` and requests `contents: write`.
- Issue #100 reports a YAML 1.2 strict-parser compatibility defect in the `endpointURL` description. Resolve or explicitly disposition before declaring migration-ready.
- Issue #78 is an open standards/product identity discussion. Do not treat a repository rename as part of migration.
- Existing standards boundary: xGov MEM remains the endorsed baseline; a proposed DCAT-AP-UK direction must not silently replace it. NDL PubSec MCP and other consumers must continue to use the endorsed model until a formal standards decision.

**Pre-transfer gate**
1. Obtain source repository admin authority and written acceptance from the current standards steward and the user's receiving-side standards/engineering authority.
2. Reconfirm licence, protected branch rules, all branches/tags/releases, open issues/PRs, Pages branch, Actions workflows, DNS/custom-domain configuration, deployment permissions and secret/variable names (never values).
3. Build a verified consumer register: NDL PubSec MCP, JSON Schema/SHACL artefact consumers, validators, documentation links, raw URLs, badges and any external tooling.
4. Agree the canonical destination name and URL strategy. Preserve the existing Pages URL through transfer or provide an approved managed redirect/continuity mechanism before retiring it.
5. Resolve or formally disposition issue #100 with strict YAML 1.2 parser validation in addition to the existing LinkML/PyYAML path.
6. Record the standards decision boundary in the destination README/docs and all affected consumer contracts.

**Transfer and post-transfer verification**
1. Transfer intact; preserve protected `main`, `gh-pages`, branches, tags, prerelease, issues, PR discussions and licence attribution.
2. Verify Pages build and published content, custom domain/DNS if applicable, Actions permissions and deployment credentials recreated through approved channels.
3. Run model tests, strict YAML parser validation, generated JSON Schema/SHACL checks and downstream MCP integration tests.
4. Verify NDL PubSec MCP still resolves and validates against the currently endorsed xGov MEM baseline.
5. Update consumer URLs only after old and new endpoints are both tested; maintain the old published URL for the agreed transition period.
6. Do not rename the repository, switch standards identity, merge DCAT-AP-UK, delete branches or change the endorsement status as part of transfer.

**Authority gate:** connected identity had push but not admin permission at the last check. Source owner/admin action is required.

**Current disposition:** NOT READY under the conformance replay (MUST 4/10). Resolve SC-03, SC-04, SC-05, GA-01, GA-02 and GA-03, with licensing and security review; standards and site-continuity approvals plus source admin are also required. Not transferred.

## 3. Common destination readiness checklist

The receiving owner should verify these directly in GDS-DTX before scheduling a transfer:

- [ ] The user's account has the organisation role required to accept transfers and administer repositories, equivalent in practical capability to the intended `data-asset-management-hub` benchmark.
- [ ] The organisation's repository creation/transfer policy and any approval workflow are understood.
- [ ] Destination repository names and visibility are agreed; public visibility is not changed by default.
- [ ] Required teams and collaborators are defined using least privilege.
- [ ] Rulesets, protected branches, CODEOWNERS and required checks are recreated or verified.
- [ ] Actions permissions, allowed actions, runner availability, schedules and artifact retention are confirmed.
- [ ] Pages policy, custom domains, DNS and deployment permissions are confirmed where applicable.
- [ ] Environments, secrets and variables are re-provisioned through approved secret-management channels; record names only in this pack.
- [ ] Packages, webhooks, GitHub Apps, OAuth callbacks, Dependabot, CodeQL and external integrations are checked.
- [ ] Records retention, audit requirements, support route, incident ownership and cost/billing constraints are accepted.
- [ ] A named rollback/forward-fix decision-maker and a migration window are recorded.

## 4. Transfer-day checklist

For each repository, capture the following in the restricted operational record immediately before the action:

- [ ] Source owner/admin and destination owner/admin both confirmed.
- [ ] Exact source URL, destination slug, visibility, default branch and head SHA captured.
- [ ] Branches, tags, releases, LFS, submodules, issues, PRs and discussions inventoried.
- [ ] Pages, domains, package coordinates, workflow files, environments and integration endpoints inventoried.
- [ ] Open changes frozen or explicitly allowed to proceed.
- [ ] Consumer owners notified and smoke-test operators available.
- [ ] Native transfer executed by an authorised account.
- [ ] Destination metadata, refs, history, access and policies verified.
- [ ] CI, deployment, Pages, packages and consumer smoke tests passed.
- [ ] Old URL redirects and published artefacts remain accessible.
- [ ] Exceptions, failures, approvals and final owner acceptance recorded.

## 5. Hard stops

Stop the affected repository's transfer or cutover if any of the following is true:
- receiving organisation or repository authority is not verified;
- source-side admin authority is missing;
- classification, licence or ownership is unresolved;
- required standards/service/security approval is missing;
- a consumer or canonical URL would break without an approved continuity plan;
- protected material would be copied into an inappropriate destination;
- a transfer would silently change visibility, standards status, product identity or production behaviour.

These are gates for the affected repository, not reasons to stop safe documentation and pre-flight work on the others.

## 6. Explicitly excluded actions

This pack does not authorise moving any other `co-cddo` repository; creating an unapproved successor; merging products; changing visibility; renaming the standards model; arming the MoG harvester; deleting branches; merging open PRs; changing production deployments or billing; or copying private/OFFICIAL/OFFICIAL-SENSITIVE material into public repositories.


## 7. GDS-DTX conformance baseline and remediation gate

The same 25-check framework used in the user's `cyberdudeuk` portfolio is applied to each candidate. The complete reports and reproducibility inputs are in `docs/portfolio/conformance/` on the portfolio PR branch.

| Repository | Replayed verdict | MUST met | MUST failures | Transfer effect |
|---|---|---:|---|---|
| `co-cddo/MoG-Navigator` | **NOT READY** | 7/10 | SC-03, SC-04, SC-05 | Resolve licensing, security reporting and third-party release/change information before transfer readiness. |
| `co-cddo/ocdo-data-foundations` | **NOT READY** | 5/10 | SC-01, SC-03, SC-04, SC-05, GA-02 | Define purpose and owner; improve README; resolve licence/security/release requirements and workflow permissions. |
| `co-cddo/ukgov-metadata-exchange-model` | **NOT READY** | 4/10 | SC-03, SC-04, SC-05, GA-01, GA-02, GA-03 | Resolve licence, security and release evidence; pin third-party action; tighten workflow permissions; review risky triggers. |

The result reports are checker-equivalent evidence replays based on the complete recursive Git trees, relevant source files, GitHub metadata, branch protection and available recent commit summaries. Each repository folder also contains `meta.json` and `source-manifest.json`. They are not represented as native CLI runs: the connector denied branch creation in each source repository with HTTP 403. The native `python3 -I tools/conformance.py --self-test` and `--write` commands still need to be run from an authorised checkout, followed by source-side PRs containing the canonical `docs/conformance/` artefacts.

The conformance baseline is an additional readiness gate, not permission to change licences, standards, production workflows or repository settings without the appropriate owner review. GDS-DTX-specific DX checks are advisory and do not determine the verdict. Re-run the checker after remediation and again after transfer.
