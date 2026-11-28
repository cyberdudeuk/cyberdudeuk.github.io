# Three-repository GDS-DTX conformance results

**Date:** 28 November 2026  
**Framework:** `cyberdudeuk/github-repos-asset-catalogue/tools/conformance.py`  
**Baseline:** `alphagov/gds-way@7bc40fb` (25 November 2026)

| In-scope repository | Reproduced verdict | MUST met | SHOULD/CONSIDER passed | Report |
| --- | --- | ---: | ---: | --- |
| `co-cddo/MoG-Navigator` | **NOT READY** | 7/10 | 2/10 | [Report](mog-navigator/report.md) |
| `co-cddo/ocdo-data-foundations` | **NOT READY** | 5/10 | 3/10 | [Report](ocdo-data-foundations/report.md) |
| `co-cddo/ukgov-metadata-exchange-model` | **NOT READY** | 4/10 | 3/11 | [Report](ukgov-metadata-exchange-model/report.md) |

Each repository folder contains the 25-check Markdown report, checker-shaped result JSON, badge SVG/JSON, the metadata JSON used by the checker and a complete recursive source-tree manifest (path, mode, blob SHA and size). Each report includes evidence, migration-specific remediation and source-side execution steps.

**Qualification:** results are replayed from the current checker logic against the complete recursive Git tree, relevant source files and retrieved GitHub metadata. They are not claimed as native CLI executions. The GitHub integration returned HTTP 403 for branch creation in all three source repositories, so canonical artefacts have been recorded here in the portfolio branch pending an authorised source-repository PR. The native checker self-test and `--write` must still be run from an authorised checkout. No source repository was changed.

**Scope:** exactly the three repositories named above. No other `co-cddo` repository is included.
