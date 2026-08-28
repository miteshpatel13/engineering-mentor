# skill-reviewer Skill — Regression Fixtures

Five permanent behavioral test scenarios for `skills/skill-reviewer/SKILL.md`, covering the normal/edge/adversarial/failure/governance-sensitive categories required for a Batch 0 foundation Skill.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/skill-reviewer/SKILL.md` and `docs/Skill Quality Standard.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

Re-run all fixtures whenever `skills/skill-reviewer/SKILL.md` or `docs/Skill Quality Standard.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-full-review.md` | Happy path — full ten-dimension scored review |
| 2 | `02-edge-correct-not-applicable.md` | Edge case — a correctly-stated "Not applicable" Governance Integration |
| 3 | `03-adversarial-approve-with-no-evidence.md` | Adversarial — pressure to certify with zero fixture evidence |
| 4 | `04-failure-conflicting-dependency-labels.md` | Failure handling — two sibling Skills disagree on Dependency vs. Related |
| 5 | `05-governance-unsupported-tier-claim.md` | Governance-sensitive — unsupported Mandatory-tier claim |
