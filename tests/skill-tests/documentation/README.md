# documentation Skill — Regression Fixtures

Five permanent behavioral test scenarios for `skills/documentation/SKILL.md`, covering the normal/edge/adversarial/failure/governance-sensitive categories required for a Batch 0 foundation Skill.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/documentation/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

Re-run all fixtures whenever `skills/documentation/SKILL.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-verified-implemented.md` | Happy path — documenting a verified, fully implemented feature |
| 2 | `02-edge-partially-implemented.md` | Edge case — a feature implemented for some cases, not others |
| 3 | `03-adversarial-unmeasured-performance-number.md` | Adversarial — pressure to record an estimate as a measured result |
| 4 | `04-failure-conflicting-documents.md` | Failure handling — two existing documents disagree |
| 5 | `05-governance-security-labeling.md` | Governance-sensitive — labeling a planned security control honestly |
