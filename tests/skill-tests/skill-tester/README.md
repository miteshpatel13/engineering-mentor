# skill-tester Skill — Regression Fixtures

Five permanent behavioral test scenarios for `skills/skill-tester/SKILL.md`, covering the normal/edge/adversarial/failure/governance-sensitive categories required for a Batch 0 foundation Skill.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/skill-tester/SKILL.md` and `docs/Skill Testing Standard.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

Re-run all fixtures whenever `skills/skill-tester/SKILL.md` or `docs/Skill Testing Standard.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-fixture-design.md` | Happy path — designing coverage from a Skill's own Edge Cases/Failure Handling |
| 2 | `02-edge-uncategorized-edge-case.md` | Edge case — a named edge case with no matching fixed category |
| 3 | `03-adversarial-weak-pass-criteria.md` | Adversarial — a submitted fixture that would pass regardless of Skill quality |
| 4 | `04-failure-ambiguous-defect-source.md` | Failure handling — genuinely unclear Skill defect vs. fixture defect |
| 5 | `05-governance-adapt-relationship-set.md` | Governance-sensitive — adapting the governance-relationship category set for a new Review-type Skill |
