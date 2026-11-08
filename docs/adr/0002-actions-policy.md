# ADR 0002: Plain commands in workflows; third-party actions only where unavoidable, pinned

Status: accepted, 8 November 2026. Same as the estate pattern. Workflows check out with plain git and use the runner's
Python, Node.js and Chrome. The only actions are GitHub-owned ones and OpenSSF Scorecard, each pinned to a full commit
SHA with its tag in a comment. Dependabot proposes updates; a person checks each commit against its tag before merging.
