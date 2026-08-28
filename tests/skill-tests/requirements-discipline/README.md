# requirements-discipline Skill — Regression Fixtures

Five permanent behavioral test scenarios for `skills/requirements-discipline/SKILL.md`, covering the normal/edge/adversarial/failure/governance-sensitive categories required for a Batch 0 foundation Skill.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/requirements-discipline/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

Re-run all fixtures whenever `skills/requirements-discipline/SKILL.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-confirmed-classification.md` | Happy path — classifying an explicitly stated requirement |
| 2 | `02-edge-partial-open-point.md` | Edge case — an open point blocking only some downstream work |
| 3 | `03-adversarial-implicit-decision-pressure.md` | Adversarial — pressure to silently decide a material ambiguity |
| 4 | `04-failure-conflicting-sources.md` | Failure handling — two authoritative sources conflict |
| 5 | `05-governance-standard-backed-gap.md` | Governance-sensitive — an unstated requirement already governed by an existing Standard |
