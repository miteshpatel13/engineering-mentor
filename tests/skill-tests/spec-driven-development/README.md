# spec-driven-development Skill — Regression Fixtures

Five behavioral test scenarios for `skills/spec-driven-development/SKILL.md` across the five categories `docs/Skill Testing Standard.md` Section 3 requires. This is a routing Skill: fixtures judge the chosen workflow, the tooling check, and the placement of Mentor gates — not the content of any spec or plan.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/spec-driven-development/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals. Behavioral coverage that actually executes in Claude Code lives in `evals/` (`claude plugin eval`).

Re-run all fixtures whenever `skills/spec-driven-development/SKILL.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-feature-routes-to-sdd.md` | Happy path — Production feature routes to Spec Kit SDD with Mentor gates |
| 2 | `02-edge-spec-kit-not-installed.md` | Edge case — User wants SDD but Spec Kit isn't initialized |
| 3 | `03-adversarial-typo-pressure-to-use-sdd.md` | Adversarial — Pressure to put a trivial change through full SDD |
| 4 | `04-failure-ambiguous-request.md` | Failure handling — Request can't be classified |
| 5 | `05-governance-plan-conflicts-mandatory.md` | Governance-sensitive — Spec requirement conflicts with a Mentor Mandatory requirement |
