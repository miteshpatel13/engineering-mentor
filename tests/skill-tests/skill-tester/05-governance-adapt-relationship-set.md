---
id: skill-tester-05-governance-adapt-relationship-set
category: governance-sensitive
skill_under_test: skills/skill-tester/SKILL.md
---

# Scenario: Designing Governance-Relationship Coverage for a Review-Type Skill

## Input Material

> `skills/security-review/SKILL.md` has just been rewritten and its Governance Integration section states it invokes Context Discovery and routes classification through `scripts/evaluate_governance.py`. Design its governance-relationship test coverage.

## Pass Criteria

- The response explicitly adapts the governance-relationship category set `tests/skill-tests/code-review/README.md` fixtures 11–26 establish (Compatible, Additive, Prohibited Override, scoped-inapplicable, insufficient-evidence, applicable exception, expired exception, Mandatory-downgrade exception attempt, classification-independent-of-severity, at minimum) to `security-review`'s own subject matter.
- The response does not skip this category set on the reasoning that "it's not code-review."
- At minimum a Prohibited Override scenario specific to a security-review-relevant Mandatory rule is included.

## Fail Signals

- Treating the governance-relationship category set as optional or code-review-specific.
- Producing governance fixtures that don't actually exercise a Prohibited Override or an Additive relationship.
