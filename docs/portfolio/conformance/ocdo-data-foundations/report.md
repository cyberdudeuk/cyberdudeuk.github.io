# GDS-DTX conformance assessment: co-cddo/ocdo-data-foundations

<badge>**NOT READY**</badge> — 5 of 10 applicable MUST checks met; 3 of 10 applicable SHOULD/CONSIDER checks passed.

**Assessment date:** 28 November 2026  
**Framework:** `cyberdudeuk/github-repos-asset-catalogue/tools/conformance.py`  
**GDS Way baseline:** `alphagov/gds-way@7bc40fb` (25 November 2026)  
**Source branch:** `main`

## Evidence and execution qualification

This is a **checker-equivalent evidence replay**, not a claim that the native CLI command `python3 -I tools/conformance.py --write` was executed inside this source repository. The complete recursive Git tree, all files relevant to the 25 checks, repository metadata, branch-protection state and the latest available commit summaries were retrieved. The statuses below follow the current checker logic and its supplied metadata schema.

The GitHub integration denied branch creation in all three source repositories with HTTP 403 `Resource not accessible by integration`. Therefore these assessment files are recorded in the portfolio migration PR, not committed into the source repositories. No source code, workflow or repository setting was changed. The checker self-test and source-side `--write` still need to be run from an authorised checkout before these reports are treated as source-published conformance artefacts.

## Check results

| Check | Strength | GDS Way / GDS-DTX requirement | Status | Evidence |
| --- | --- | --- | --- | --- |
| GA-01 | MUST | [Third-party actions pinned to a full commit SHA](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#pinning-actions) (reviewed 2025-08-04) | PASS | all third-party actions pinned to a SHA |
| GA-02 | MUST | [Workflow permissions set to only what is needed](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#permissions) (reviewed 2025-08-04) | FAIL | no top-level permissions: ['blank.yml']; write-all: [] |
| GA-03 | MUST | [No risky triggers](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#triggers) (reviewed 2025-08-04) | PASS | no risky triggers |
| GA-04 | MUST | [No script injection from user-controlled event fields](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#script-injections) (reviewed 2025-08-04) | PASS | no user-controlled fields interpolated into commands |
| GA-05 | MUST | [No personal access tokens in workflows](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#personal-access-tokens) (reviewed 2025-08-04) | PASS | only GITHUB_TOKEN or app tokens |
| GA-06 | MUST | [AWS reached with OIDC, not access keys](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#authenticating-with-aws-and-other-external-services) (reviewed 2025-08-04) | N/A | no AWS access keys |
| MS-01 | MUST | [Non-public repositories have HANDLING_INSTRUCTIONS.md](https://gds-way.digital.cabinet-office.gov.uk/standards/managing-sensitive-information.html) (reviewed 2025-10-01) | N/A | public repository |
| SC-01 | MUST | [README](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | FAIL | README.md (one word; the checker requires at least 50) |
| SC-02 | MUST | [Informative commit messages](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | PASS | 2 of 2 recent summaries say what changed |
| SC-03 | MUST | [MIT and OGL licence files](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | FAIL | MIT: yes, LICENSE; OGL: no |
| SC-04 | MUST | [An email address for security bug reports](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | FAIL | no SECURITY.md; no email or Cabinet Office VDP route documented; private vulnerability reporting setting not retrievable (metadata null) |
| SC-05 | MUST | [If third parties are affected: changelog, release notes, known issues, semantic version](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | FAIL | changelog: none; semantic version in it: no; public issues: yes |
| AD-01 | SHOULD | [Architecture decisions recorded](https://gds-way.digital.cabinet-office.gov.uk/standards/architecture-decisions.html) (reviewed n/a) | FAIL | no decision records folder |
| GT-01 | SHOULD | [Default branch is main](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/working-with-git.html#default-branch-name) (reviewed 2025-02-18) | PASS | default branch main |
| GT-02 | SHOULD | [Commit summaries of 50 characters or fewer](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/working-with-git.html#structure) (reviewed 2025-02-18) | PASS | 2 of 2 recent summaries are 50 characters or fewer |
| SC-06 | SHOULD | [Contributing guidelines](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | FAIL | no CONTRIBUTING file |
| SC-07 | SHOULD | [Tests run in public CI](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/#publish-open-source-code) (reviewed 2026-03-19) | PASS | CI on push or pull request: blank.yml |
| TD-01 | SHOULD | [Automated dependency updates](https://gds-way.digital.cabinet-office.gov.uk/standards/tracking-dependencies.html) (reviewed 2026-09-22) | FAIL | no Dependabot or Renovate config |
| TD-02 | SHOULD | [Dependency update cooldown](https://gds-way.digital.cabinet-office.gov.uk/standards/tracking-dependencies.html) (reviewed 2026-09-22) | FAIL | no cooldown |
| TD-03 | SHOULD | [Open update pull request limit of 10 or more](https://gds-way.digital.cabinet-office.gov.uk/standards/tracking-dependencies.html) (reviewed 2026-09-22) | FAIL | default limit of 5 |
| VD-01 | SHOULD | [Published sites point security.txt at the Cabinet Office programme](https://gds-way.digital.cabinet-office.gov.uk/standards/vulnerability-disclosure.html) (reviewed 2025-02-18) | N/A | no published site |
| GA-07 | CONSIDER | [CODEOWNERS covers .github/workflows](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/using-github-actions.html#user-permissions) (reviewed 2025-08-04) | FAIL | CODEOWNERS missing or does not cover .github/workflows |
| UG-01 | CONSIDER | [Main branch protected](https://gds-way.digital.cabinet-office.gov.uk/standards/source-code/use-github.html#configuring-github-repositories) (reviewed 2025-07-19) | FAIL | main is not protected |
| DX-01 | GDS-DTX | [Pre-commit hooks with detect-secrets](https://github.com/gds-dtx/gds-dtx-github-users-tf/blob/main/.pre-commit-config.yaml) (reviewed observed 27 Nov 2026) | FAIL | no pre-commit detect-secrets hook |
| DX-02 | GDS-DTX | [Third-party actions listed for the gds-dtx Actions allowlist](https://github.com/gds-dtx/gds-dtx-github-users-tf/issues/13) (reviewed observed 27 Nov 2026) | PASS | third-party actions to allowlist: none |

## Verdict

- **NOT READY**.
- MUST checks met: 5/10.
- SHOULD/CONSIDER checks passed: 3/10.
- Unresolved MUST failures: SC-01, SC-03, SC-04, SC-05, GA-02.
- Unresolved MUST manual checks: none.

## Migration-specific actions

- Replace the title-only README with purpose, scope, ownership, consumers, support and contribution guidance.
- Add explicit least-privilege workflow permissions; replace the starter workflow with substantive validation only after the product purpose is confirmed.
- Establish whether third parties depend on this repository; until an owner records otherwise, the checker treats them as potentially affected.
- Resolve licence, security-reporting and changelog requirements before any transfer.
- Decide transfer intact versus a controlled successor only after ownership and consumer discovery; preserve source history.

## Evidence inputs

- Recursive source tree at the current `main` head.
- Full contents of README, licence files and all workflow files.
- GitHub repository metadata: public visibility, default branch, issues and Pages state.
- Main branch protection endpoint.
- Up to 30 recent commit summaries from GitHub.
- No exception register was present in the retrieved source tree. No exceptions were invented. The private-vulnerability-reporting setting was not retrievable through this connector; the checker metadata therefore leaves it null, and no SECURITY.md/email/VDP route is evidenced.

## Required source-side completion

1. Run `python3 -I tools/conformance.py --self-test` from the catalogue checkout.
2. Run `sh tools/conformance_meta.sh co-cddo/ocdo-data-foundations > meta.json` with an authorised GitHub CLI session.
3. Run `python3 -I tools/conformance.py PATH/TO/ocdo-data-foundations --meta meta.json --write`.
4. Review and remediate MUST failures; record only approved, dated, referenced exceptions in `docs/compliance/exceptions.yaml`.
5. Commit the four canonical files under `docs/conformance/` and the README badge through a source-repository PR.
6. Rerun after transfer and compare source and destination results.

**No readiness is asserted for migration.** All three repositories are currently **NOT READY** under the reproduced checker result; this is a pre-transfer baseline, not a transfer authorisation.
