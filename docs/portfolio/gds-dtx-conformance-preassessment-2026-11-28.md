# GDS-DTX conformance pre-assessment for the three CDDO migration candidates

**Assessment date:** 28 November 2026  
**Framework:** `cyberdudeuk/github-repos-asset-catalogue/tools/conformance.py`  
**Framework source:** `alphagov/gds-way@7bc40fb` (25 November 2026)  
**Scope:** exactly the three repositories below. No other `co-cddo` repositories are in scope.

> **Assessment state: PRE-ASSESSMENT — NOT A SCORED CONFORMANCE RUN.**  
> This document records evidence retrieved directly from the repositories and identifies likely failures and unresolved checks. It does not claim that the 25-check script has been executed against complete local checkouts. The GitHub connector can read selected files but does not provide a complete repository checkout/tree for these source repositories in this session; a sparse file sample would create false failures. Do not publish a READY/NOT READY badge from this pre-assessment. Run the catalogue checker against full, current checkouts with a complete metadata file before issuing the formal four-artifact result.

## Method and status vocabulary

The canonical checker evaluates 25 checks: SC-01–SC-07, GT-01–GT-02, UG-01, GA-01–GA-07, TD-01–TD-03, MS-01, VD-01, AD-01, and DX-01–DX-02. It records PASS, FAIL, EXCEPTION, N/A or MANUAL. A setting not evidenced by GitHub metadata must remain MANUAL. GDS-DTX-specific DX checks are advisory and do not determine the verdict.

Formal output, once run on full checkouts, is `docs/conformance/report.md`, `result.json`, `badge.svg` and `badge.json` in each repository. The checker must first pass `python3 -I tools/conformance.py --self-test`.

## Candidate 1 — co-cddo/MoG-Navigator

**Repository facts:** public; default branch `main`; MIT licence; source admin permission is reported for the connected account. README identifies a public-record/synthetic-data purpose and explicitly disclaims government commissioning, endorsement and affiliation. It names GUVNR / Whitehall Connect as a reference consumer. CI runs on push and pull request; a separate scheduled/manual harvest workflow remains dry-run. The CI workflow explicitly grants `contents: read`. Its third-party actions use version tags (`@v4`), not full commit SHAs. No branch protection was reported in the forensic review.

| Check | Preliminary status | Evidence / next action |
| --- | --- | --- |
| SC-01 README | PASS | Substantive README present. |
| SC-02 commit messages | MANUAL | Supply recent commit summaries via the metadata script. |
| SC-03 MIT and OGL | FAIL* | MIT is present; no OGL file was found in the inspected root. Confirm copyright/licensing basis and record an approved exception if OGL is inapplicable. |
| SC-04 security contact | FAIL* | No SECURITY.md was found in the inspected root; establish a working private reporting route. |
| SC-05 third-party release information | FAIL* | A named reference consumer exists; no CHANGELOG was found in the inspected root. Confirm consumer impact and add release notes/versioning or a justified exception. |
| SC-06 contributing | FAIL* | No CONTRIBUTING file found in the inspected root. |
| SC-07 public CI | PASS | `.github/workflows/ci.yml` runs on push and pull_request. |
| GT-01 default branch | PASS | Default branch is `main`. |
| GT-02 commit summary length | MANUAL | Requires commit metadata. |
| UG-01 branch protection | FAIL* | Main was reported unprotected; verify current rulesets/branch protection. |
| GA-01 action SHA pinning | FAIL* | `actions/checkout@v4`, `actions/setup-node@v4`, `actions/upload-artifact@v4` are not full-SHA pinned. |
| GA-02 least-privilege permissions | PASS | CI and harvest workflows declare `contents: read`. |
| GA-03 risky triggers | PASS | Inspected triggers are push, pull_request, schedule and workflow_dispatch; no risky trigger identified. |
| GA-04 script injection | PASS | No unsafe event-field interpolation identified in inspected run steps. |
| GA-05 personal access tokens | PASS | No PAT use identified in inspected workflows. |
| GA-06 AWS authentication | N/A / verify | No AWS authentication path identified in inspected workflows. Confirm full workflow scan. |
| GA-07 workflow CODEOWNERS | FAIL* | No CODEOWNERS file found in the inspected root. |
| TD-01 dependency updates | FAIL* | No Dependabot configuration found in the inspected root. |
| TD-02 dependency cooldown | FAIL* | No Dependabot configuration found in the inspected root. |
| TD-03 Dependabot PR limit | FAIL* | No Dependabot configuration found in the inspected root. |
| MS-01 handling instructions | N/A | Repository is public. |
| VD-01 security.txt | N/A / verify | No GitHub Pages site was reported; confirm current publishing configuration. |
| AD-01 architecture decisions | FAIL* | No ADR location/file found in the inspected root. |
| DX-01 detect-secrets pre-commit | FAIL* | No pre-commit configuration found in the inspected root. |
| DX-02 Actions allowlist | MANUAL | Organisation allowlist is an organisation-level setting and was not verified. |

* Preliminary finding from the inspected paths, not a formal checker result. The complete checkout may contain files at other supported paths, and the formal checker must decide.

**Migration-specific gates:** preserve the MIT licence and non-government disclaimer; retain the independent canon and publish/consume boundary; verify the GUVNR feed URL and stale-data behaviour after transfer; retain the dry-run harvest posture. Do not enable external harvesting or secrets as part of migration.

## Candidate 2 — co-cddo/ocdo-data-foundations

**Repository facts:** public; default branch `main`; MIT licence; connected account has push but not admin permission. Inspected README contains only the repository heading. The only workflow found is GitHub's starter `blank.yml`, with push/pull_request/workflow_dispatch triggers, `actions/checkout@v4`, and no explicit permissions block. No substantive build/test/validation process was found in the inspected material.

| Check | Preliminary status | Evidence / next action |
| --- | --- | --- |
| SC-01 README | FAIL* | README is only a heading and is below the checker’s 50-word threshold. |
| SC-02 commit messages | MANUAL | Supply recent commit summaries. |
| SC-03 MIT and OGL | FAIL* | MIT is present; no OGL file was found in the inspected root. Confirm licensing basis and exception route. |
| SC-04 security contact | FAIL* | No SECURITY.md found in the inspected root; establish a working private reporting route. |
| SC-05 third-party release information | MANUAL | Owner must confirm whether third parties depend on this repository; if they do, provide changelog/release information. |
| SC-06 contributing | FAIL* | No CONTRIBUTING file found in the inspected root. |
| SC-07 public CI | PASS | Starter workflow is configured for push and pull_request, but it does not constitute substantive tests. |
| GT-01 default branch | PASS | Default branch is `main`. |
| GT-02 commit summary length | MANUAL | Requires commit metadata. |
| UG-01 branch protection | FAIL* | Main was reported unprotected; verify current rulesets/branch protection. |
| GA-01 action SHA pinning | FAIL* | Starter workflow uses `actions/checkout@v4`, not a full commit SHA. |
| GA-02 least-privilege permissions | FAIL* | Workflow has no explicit permissions block. |
| GA-03 risky triggers | PASS | Inspected triggers are push, pull_request and workflow_dispatch. |
| GA-04 script injection | PASS | No unsafe event-field interpolation identified in inspected run steps. |
| GA-05 personal access tokens | PASS | No PAT use identified in inspected workflow. |
| GA-06 AWS authentication | N/A / verify | No AWS authentication path identified. Confirm full workflow scan. |
| GA-07 workflow CODEOWNERS | FAIL* | No CODEOWNERS file found in the inspected root. |
| TD-01 dependency updates | FAIL* | No Dependabot configuration found in the inspected root. |
| TD-02 dependency cooldown | FAIL* | No Dependabot configuration found in the inspected root. |
| TD-03 Dependabot PR limit | FAIL* | No Dependabot configuration found in the inspected root. |
| MS-01 handling instructions | N/A | Repository is public. |
| VD-01 security.txt | N/A / verify | No Pages site was reported; confirm current publishing configuration. |
| AD-01 architecture decisions | FAIL* | No ADR location/file found in the inspected root. |
| DX-01 detect-secrets pre-commit | FAIL* | No pre-commit configuration found in the inspected root. |
| DX-02 Actions allowlist | MANUAL | Organisation allowlist is not visible from repository content. |

* Preliminary finding from inspected paths only; formal checker must run on a complete checkout.

**Migration-specific gates:** before deciding transfer versus controlled recreation, establish the repository’s purpose, accountable owner, consumers, authoritative assets and whether substantive work exists elsewhere. Preserve its history until that decision is made. Source admin permission is a separate gate.

## Candidate 3 — co-cddo/ukgov-metadata-exchange-model

**Repository facts:** public; default branch `main`; protected main; OGL-UK-3.0 is recorded in the repository/packaging metadata; the package metadata declares version `0.1.0`. README documents LinkML, Poetry, generated schemas, examples, MkDocs and a published GitHub Pages site. The repository has 17 visible branches, a prerelease and 32 open issues in the forensic snapshot. The documentation workflow is described as deploying on commits to main. Connected account has push but not admin permission.

| Check | Preliminary status | Evidence / next action |
| --- | --- | --- |
| SC-01 README | PASS | Substantive README present. |
| SC-02 commit messages | MANUAL | Supply recent commit summaries. |
| SC-03 MIT and OGL | FAIL* | OGL is evidenced in package metadata; MIT has not been evidenced. Confirm code/content rights and whether a recorded exception is appropriate. |
| SC-04 security contact | MANUAL | SECURITY.md/private reporting route not yet verified. |
| SC-05 third-party release information | MANUAL | Published docs and downstream consumers make impact assessment necessary; inspect changelog, release notes, issues and tags. |
| SC-06 contributing | MANUAL | README documents developer setup but a standalone CONTRIBUTING file has not been verified. |
| SC-07 public CI | MANUAL | README identifies a deploy workflow on main; verify whether tests run on pull_request. Deployment alone is not sufficient evidence of public CI tests. |
| GT-01 default branch | PASS | Default branch is `main`. |
| GT-02 commit summary length | MANUAL | Requires commit metadata. |
| UG-01 branch protection | PASS | Main was reported protected; verify current rulesets/branch protection. |
| GA-01 action SHA pinning | MANUAL | Full deploy workflow file and all workflow files still need inspection. |
| GA-02 least-privilege permissions | MANUAL | Deploy workflow is reported to request `contents: write`; inspect exact permissions and justify the write scope. |
| GA-03 risky triggers | MANUAL | Inspect all workflow trigger declarations. |
| GA-04 script injection | MANUAL | Inspect all executable workflow `run:` blocks. |
| GA-05 personal access tokens | MANUAL | Inspect all workflow secret references. |
| GA-06 AWS authentication | MANUAL | Inspect all workflow authentication paths. |
| GA-07 workflow CODEOWNERS | MANUAL | Verify CODEOWNERS coverage for workflows. |
| TD-01 dependency updates | MANUAL | Dependabot configuration not yet verified. |
| TD-02 dependency cooldown | MANUAL | Dependabot configuration not yet verified. |
| TD-03 Dependabot PR limit | MANUAL | Dependabot configuration not yet verified. |
| MS-01 handling instructions | N/A | Repository is public. |
| VD-01 security.txt | MANUAL | Public Pages site exists; verify `.well-known/security.txt` and the required disclosure destination. |
| AD-01 architecture decisions | MANUAL | Inspect repository for ADRs or equivalent recorded decisions. |
| DX-01 detect-secrets pre-commit | MANUAL | Verify pre-commit configuration. |
| DX-02 Actions allowlist | MANUAL | Organisation allowlist must be checked by an organisation owner. |

* Preliminary licensing observation only. The formal checker and rights review must determine the actual result.

**Migration-specific gates:** retain all branches, tags, issues, release history, protected-branch rules, Pages configuration and deployment semantics. Preserve the existing Pages URL or prove a redirect/continuity plan before transfer. Do not rename the model or change its standards status during migration. The endorsed xGov MEM remains the baseline until a formal standards decision changes it. The YAML 1.2 issue in `endpointURL` remains a source defect to fix in a separately reviewed change, not as an incidental migration edit.

## Formal execution required before a READY verdict

For each full checkout:

1. Run `python3 -I tools/conformance.py --self-test` and retain the successful output.
2. Generate metadata with `sh tools/conformance_meta.sh OWNER/REPO > meta.json`. The metadata process is read-only. Verify the result contains visibility, default branch, branch protection, private vulnerability reporting, issue setting and recent commit summaries.
3. Run `python3 -I tools/conformance.py PATH/TO/REPO --meta meta.json --write`.
4. Review every FAIL and MANUAL with the repository owner. Record only genuine, approved exceptions in `docs/compliance/exceptions.yaml` with rationale, review date and reference.
5. Commit the four generated outputs and README badge in a reviewable branch/PR in the source repository.
6. Rerun after remediation and after transfer, then compare source and destination outputs.

## Current execution boundary

This pre-assessment is written into the portfolio migration evidence because the source-repository integration did not permit a complete checkout or branch write in this session. It is not a substitute for the four generated artifacts inside each source repository. The existing portfolio PR remains a draft; no source repository was modified, no report badge was published, and no transfer or standards change was performed.

The intended receiving owner is the user. The target-side permission baseline is the user's stated `gds-dtx/data-asset-management-hub` access model; target-side authority and organisation-level settings still need to be verified through a working connection. Source admin rights remain a separate requirement for candidates 2 and 3.
