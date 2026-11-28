# CDDO migration forensic delta — 28 November 2026

This supplement records a deeper public-repository inspection for the three explicitly in-scope repositories only. It does not authorise a transfer, visibility change, production cutover, standards change, or merge. Other `co-cddo` repositories remain out of scope.

## Executive disposition

| Repository | Current evidence | Migration disposition |
|---|---|---|
| `co-cddo/MoG-Navigator` | Public, MIT, one unprotected `main` branch, no releases, no Pages site, 2 workflows, small static/JSON canon application; source-side admin permission is available to the connected identity | First transfer candidate, conditional on the user's receiving-side organisation/repository authority and target-policy acceptance |
| `co-cddo/ocdo-data-foundations` | Public, MIT, 3 KB, two unprotected branches at the same commit, README is a 23-byte stub, one placeholder CI workflow, no releases or Pages | Do not transfer as a substantive product yet; classify as a shell/prototype and establish intended successor/ownership before deciding whether to transfer intact or recreate |
| `co-cddo/ukgov-metadata-exchange-model` | Public, OGL-UK-3.0, protected `main`, 17 visible branches, one prerelease, 32 open issues, active Pages deployment and several CI/deploy workflows; source-side admin permission is not available to the connected identity | Standards-critical; migration must be owner-led with explicit standards and site continuity approval |

## MoG-Navigator

Repository metadata at inspection:
- Default branch `main`, head `fefdc8e98d2f7e58e95483f505dc1046bec6482e`; one branch, not protected.
- Public, MIT, 106 KB reported repository size; no GitHub Releases and `has_pages=false`.
- No open issues; the visible latest scheduled `mog-harvest` run (28 September 2026) succeeded.
- Complete recursive tree returned without truncation. It includes the app, ecosystem blueprint, canon JSON/JS mirrors, feed, provenance stamp, feed registry, release tooling, and conformance tests.
- Workflows: `.github/workflows/ci.yml` and `.github/workflows/harvest.yml`.
- CI uses Node 20, checks generated derivatives/version integrity, runs conformance and feed checks, and emits a canon checksum artifact.
- Harvest is explicitly dry-run. Workflow permissions are `contents: read`; no external calls or canon writes occur. The commented-out future arming path references X/YouTube credentials but no secret values were accessed. Do not arm this during migration.
- README expressly says the project is not commissioned by, endorsed by, or affiliated with any government department. It also distinguishes the public MoG Navigator from a deliberately private sibling. Preserve the disclaimer and do not move or disclose the private sibling.
- README identifies GUVNR / Whitehall Connect as the reference consumer, reading `mog/mog-feed.json` from its own origin. This is a concrete integration dependency to validate before and after any transfer.

Transfer checklist:
1. Confirm the user's receiving-side authority, destination repository name, required teams and public-repository acceptance; no separate sponsor is assumed.
2. Confirm that the receiving organisation will preserve public visibility, MIT licensing and the non-endorsement disclaimer.
3. Confirm whether any consumers depend on the current repository URL; the documented GUVNR consumer is the first known dependency.
4. Transfer the repository intact; do not rewrite its history or combine it with another product.
5. Revalidate Actions permissions, scheduled/manual workflow execution, artifact upload, default branch, release process and any external references after transfer. Keep harvesting dry-run.

## OCDO Data Foundations

Repository metadata at inspection:
- Public, MIT, default branch `main`, 3 KB, last pushed 3 August 2026.
- Two branches: `main` and `enhance/tooling-accessibility-schema`; both point to the same commit `39a05f88e554884a9ab6a1975d26114f6e93c3e4`; neither is protected.
- Complete recursive tree has only three files: `README.md` (23 bytes), `LICENSE`, and `.github/workflows/blank.yml`.
- The sole CI workflow is GitHub's starter template: it echoes placeholder text and does not build, test or validate a data-foundations product.
- One visible CI run on 3 August 2026 succeeded, but this is only evidence that the placeholder workflow ran successfully.
- No releases, no Pages site, no issues, and no meaningful public README description.

Disposition:
- There is not enough repository substance to justify treating this as a mature product transfer.
- Before a decision, establish the intended product scope, accountable owner, expected users, data/schema assets, and whether the repository is an abandoned scaffold or a placeholder for work held elsewhere.
- If it is only a shell, prefer a clean successor under GDS-DTX after approval, retaining the source repository as an archival reference or transferring the shell intact only if the receiving owner specifically wants it. Do not invent or populate a data-foundations product as part of migration.

## UK Cross-Government Metadata Exchange Model

Repository metadata at inspection:
- Public, default branch `main`, protected; current default-branch head `3e6c6f5eb6dda6e90ca956d0273f3698fd584212`.
- 17 visible branches, including `gh-pages`, two cyberdudeuk patch branches, LinkML development branches and multiple Dependabot branches. Branches are not all protected; preserve branch refs and review their purpose before pruning anything.
- One published prerelease: `v0.1.0` (8 November 2023), titled “Initial Base Line Release”.
- 32 open issues at repository metadata inspection; the returned recent issue page includes open dependency PRs, an open model YAML validity issue (#100), an open repository rename / DCAT-UK Application Profile discussion (#78), and an open PR to delete the Docker image workflow (#99).
- Repository licence file explicitly contains Open Government Licence v3.0 (OGL-UK-3.0). Repository metadata reports `NOASSERTION`; use the actual checked-in licence text and preserve its attribution and non-endorsement terms.
- README documents the public GitHub Pages site at `https://co-cddo.github.io/ukgov-metadata-exchange-model/`; `mkdocs.yml` hard-codes that `site_url` and the current GitHub repository URL. The `gh-pages` branch exists.
- Documentation deployment runs on pushes to `main`, installs Poetry/docs dependencies, builds generated documentation and publishes it using `make mkd-gh-deploy`. It requests `contents: write`.
- Main test workflow uses Python 3.10, Poetry and `make test`. Other workflows include CodeQL, Docker build/publish, greetings and documentation deployment.
- On 27 November 2026, the returned recent workflow page shows successful CodeQL and greetings runs on a Dependabot branch, while Docker Image CI and the model build/test workflow failed on that same branch SHA. Do not label this a default-branch failure without checking the exact run/branch context. The main-branch workflow run visible from 22 November succeeded.
- Issue #100 reports a YAML 1.2 strict-parser defect in the `endpointURL` description at line 348. The issue says PyYAML (used by LinkML) accepts it, but stricter YAML parsers reject it; this has already surfaced as a compatibility issue for an external MCP consumer. It should be resolved or explicitly dispositioned before declaring the model migration-ready.
- Issue #78 is an open discussion about whether the next iteration should be a separate product/release and whether to rename the repository to a DCAT-UK Application Profile. This is a governance decision, not a migration implementation detail. Do not rename or switch canonical standards identity during transfer.
- Issue #86's overhaul tracker is closed, but its body records six workstreams including model validation, documentation, governance/release management and community workflow.

Standards and continuity controls:
1. Treat the currently endorsed xGov Metadata Exchange Model as the active baseline until the relevant standards authority formally decides otherwise. A proposed DCAT-AP-UK direction must not be silently substituted.
2. Obtain written acceptance from the current standards owner and the receiving GDS-DTX standards owner before changing repository ownership, canonical name, or published model identity.
3. Record every external consumer and validator, including the known NDL PubSec MCP integration and any downstream schema/SHACL/JSON Schema consumers.
4. Decide whether the current GitHub Pages URL must remain live, be redirected, or be replaced with a managed stable domain. Preserve old published URLs and generated artefacts throughout the transition.
5. Preserve `main` protection, the `gh-pages` deployment history, tags/releases, branch history and all issue/PR discussions. Recheck Pages configuration, DNS/custom domain, deployment permissions and GitHub Actions secrets by name only; never export secret values.
6. Review open dependency PRs and issue #100 as a separate maintenance stream; do not bulk-merge dependency updates as part of migration.
7. Keep DCAT-AP-UK proposal status and xGov MEM endorsement status explicit in every catalogue, documentation page and integration contract.

## Access and execution blockers

The connected GitHub identity currently has source-side repository-admin permission for MoG-Navigator, but only push permission for OCDO Data Foundations and the Metadata Exchange Model. The user is the intended receiving-side owner; target-organisation admin capability and repository acceptance remain unverified in the connected session. Consequently:
- MoG-Navigator can be prepared for a transfer, but the receiving-side acceptance and policy checks remain outstanding.
- The other two repositories require source-owner/admin participation for a direct transfer.
- No transfer, rename, visibility change, workflow arming, Pages cutover, branch deletion, PR merge or standards change is performed by this supplement.

## Evidence limits

This is a public GitHub API/content inspection. It does not establish private organisation policies, secret values, webhook payloads, external DNS control, production runtime state, or the complete set of consumers. A successful placeholder workflow is not evidence of product readiness. Repeat the checks immediately before any authorised transfer.


## Conformance assessment update (28 November 2026)

The three repositories have now been assessed against the exact 25-check GDS Way/GDS-DTX framework used in the `cyberdudeuk` portfolio. The full per-repository reports, JSON results, badge SVG/JSON, checker metadata inputs and recursive source-tree manifests are indexed at [`docs/portfolio/conformance/`](conformance/README.md).

| Repository | Result | MUST met | MUST failures |
|---|---|---:|---|
| `co-cddo/MoG-Navigator` | **NOT READY** | 7/10 | SC-03, SC-04, SC-05 |
| `co-cddo/ocdo-data-foundations` | **NOT READY** | 5/10 | SC-01, SC-03, SC-04, SC-05, GA-02 |
| `co-cddo/ukgov-metadata-exchange-model` | **NOT READY** | 4/10 | SC-03, SC-04, SC-05, GA-01, GA-02, GA-03 |

The canonical checker self-test and `--write` passed in [workflow run #46160267470](https://github.com/cyberdudeuk/cyberdudeuk.github.io/actions/runs/46160267470) against full temporary clones pinned to the three source commits. All three 25-check result sets and verdicts matched. Canonical reports/results/badges were uploaded as artifact `cddo-conformance-canonical-output` (ID `15269515207`). The connector still denied source branch creation with HTTP 403, so no source repository was modified and the source-side PR commits remain outstanding. See each report for the exact evidence and limitations.
