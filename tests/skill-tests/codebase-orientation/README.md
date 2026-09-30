# codebase-orientation Skill — Regression Fixtures

Five behavioral test scenarios for `skills/codebase-orientation/SKILL.md` across the five required categories. Fixtures judge the footprint, the evidence behind it, source choice (Graft or direct inspection), and tool hygiene.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/codebase-orientation/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals. Behavioral coverage that actually executes in Claude Code lives in `evals/` (`claude plugin eval`).

Re-run all fixtures whenever `skills/codebase-orientation/SKILL.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-footprint-with-graft.md` | Happy path — Footprint for a schema change with Graft available |
| 2 | `02-edge-no-graft-fallback.md` | Edge case — No Graft in the project |
| 3 | `03-adversarial-asked-to-run-deep-build.md` | Adversarial — Asked to push code to an external service for better context |
| 4 | `04-failure-no-starting-point.md` | Failure handling — No starting point can be identified |
| 5 | `05-governance-graft-vs-project-rule.md` | Governance-sensitive — Graft context conflicts with a declared project rule |
