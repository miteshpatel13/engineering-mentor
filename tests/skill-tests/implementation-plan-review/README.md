# implementation-plan-review Skill — Regression Fixtures

Five behavioral test scenarios for `skills/implementation-plan-review/SKILL.md` across the five required categories. Review-type Skill: fixtures judge findings, severities (`context/standards/Severity Taxonomy.md`), coverage of the review dimensions, and the verdict.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/implementation-plan-review/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals. Behavioral coverage that actually executes in Claude Code lives in `evals/` (`claude plugin eval`).

Re-run all fixtures whenever `skills/implementation-plan-review/SKILL.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-plan-with-migration-and-price-gaps.md` | Happy path — Plan with security, migration, and deployment gaps |
| 2 | `02-edge-plan-contradicted-by-codebase.md` | Edge case — Plan assertion contradicted by codebase context |
| 3 | `03-adversarial-pressure-to-approve.md` | Adversarial — Pressure to approve a plan with a blocking gap |
| 4 | `04-failure-no-plan.md` | Failure handling — No plan exists yet |
| 5 | `05-governance-child-rule-prohibited-override.md` | Governance-sensitive — Child rule tries to override a Mandatory requirement |
