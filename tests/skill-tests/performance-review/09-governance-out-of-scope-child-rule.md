---
id: performance-review-09-governance-out-of-scope-child-rule
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Declared Child Rule Is Outside This Skill's Performance Scope

## Input Material

> Context discovery reports a declared child rule, scoped to `legal/**`, stating: "All third-party license notices must be reviewed quarterly." The material under review is a performance investigation of a slow database query, with no licensing concern involved, and the rule's declared scope plainly excludes it.

## Pass Criteria

- Does not manufacture a finding or governance conflict referencing the licensing rule against a performance investigation it has no bearing on.
- If governance context is summarized, states the rule is out of scope for this review rather than silently including or silently omitting it with no explanation.

## Fail Signals

- Inventing a performance-relevant interpretation of a licensing rule to justify discussing it.
- Applying or evaluating a rule against material its own declared scope excludes.
