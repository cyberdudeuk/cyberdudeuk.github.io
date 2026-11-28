# GDS-DTX conformance assessment — superseded preliminary note

**Date:** 28 November 2026  
**Status:** Superseded by the complete-tree checker-equivalent assessment reports.

The earlier sparse pre-assessment tables in this file were provisional and are withdrawn. They were based on selected file reads and did not correctly distinguish the exact checker strengths and metadata semantics. Do not use their individual check statuses.

The authoritative current evidence replay is now recorded in [the three-repository conformance results index](conformance/README.md), with one report, machine-readable result and badge pair per in-scope repository:

- [co-cddo/MoG-Navigator](conformance/mog-navigator/report.md) — **NOT READY**, MUST 7/10, SHOULD/CONSIDER 2/10.
- [co-cddo/ocdo-data-foundations](conformance/ocdo-data-foundations/report.md) — **NOT READY**, MUST 5/10, SHOULD/CONSIDER 3/10.
- [co-cddo/ukgov-metadata-exchange-model](conformance/ukgov-metadata-exchange-model/report.md) — **NOT READY**, MUST 4/10, SHOULD/CONSIDER 3/11.

## Correct method

The assessment uses the exact current `tools/conformance.py` logic from `cyberdudeuk/github-repos-asset-catalogue`, with the 25 checks and GDS Way source pinned to `alphagov/gds-way@7bc40fb` (25 November 2026). The complete recursive source trees, relevant source files, repository metadata, branch-protection state and available recent commit summaries were retrieved from GitHub.

The report is a **checker-equivalent evidence replay**, not a claim that the native CLI command or its `--self-test` was executed in the source repositories. GitHub integration attempts to create the source branches were denied with HTTP 403 `Resource not accessible by integration`. The reports are therefore stored in the portfolio migration branch pending an authorised source-side run and PR. No source repository was changed.

The current checker distinguishes MUST, SHOULD and CONSIDER strengths; it requires MIT and OGL evidence for public repositories; it treats settings without evidence conservatively; and it records GDS-DTX-only checks separately from the GDS Way verdict. The reports include the metadata limitations, notably that private vulnerability reporting could not be retrieved through this connector.

## Scope and migration controls

The scope remains exactly these three CDDO repositories and no others:

1. `co-cddo/MoG-Navigator`
2. `co-cddo/ocdo-data-foundations`
3. `co-cddo/ukgov-metadata-exchange-model`

No readiness is asserted for transfer. Do not change licence terms, enable workflows, modify production behaviour, rename the metadata model, change standards status, or transfer repositories as a side effect of conformance remediation. Use the repository-specific migration actions in each report and the three-repository transfer runbook.

## Native source-side completion

For each repository, an authorised maintainer must:

1. Run `python3 -I tools/conformance.py --self-test`.
2. Run `sh tools/conformance_meta.sh OWNER/REPO > meta.json` with the authorised GitHub CLI.
3. Run `python3 -I tools/conformance.py PATH/TO/REPO --meta meta.json --write`.
4. Review every FAIL and MANUAL; record only approved exceptions with rationale, review date and reference.
5. Commit the four canonical `docs/conformance/` artefacts and README badge through a source-repository PR.
6. Rerun after remediation and after transfer.

The user remains the intended receiving-side owner. No separate GDS-DTX sponsor is assumed; effective organisation/repository authority and the source-side write permissions are still required.
