---
id: skill-tester-01-normal-fixture-design
category: happy-path
skill_under_test: skills/skill-tester/SKILL.md
---

# Scenario: Designing Fixtures for a Freshly Drafted Domain Pattern Skill

## Input Material

> `skills/identifier-strategy/SKILL.md` has just been drafted (Implemented stage): a Domain Pattern Skill with an Edge Cases section listing "a resource that must remain sortable by creation order despite using an opaque public identifier" and a Failure Handling section stating it declines to recommend an identifier scheme when the consuming system's query patterns aren't known. Design its test coverage.

## Pass Criteria

- Both testing tiers are considered explicitly (deterministic structural check via `scripts/validate_skill.py`, plus narrative coverage of judgment).
- The named Edge Case (sortable-by-creation-order) gets its own fixture, not just the generic category list.
- The named Failure Handling scenario (declining without known query patterns) gets its own fixture.
- Governance-relationship categories are explicitly stated as not applicable for this Skill and why, rather than silently omitted.
- Fixtures follow the `tests/skill-tests/<skill-name>/NN-description.md` file shape with Input Material / Pass Criteria / Fail Signals.

## Fail Signals

- Only covering the fixed generic category list while ignoring the Skill's own stated Edge Cases/Failure Handling content.
- Silently omitting governance-relationship coverage without stating why it doesn't apply.
