---
id: testing-review-09-governance-out-of-scope-child-rule
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Declared Child Rule Is Outside This Skill's Test-Coverage Scope

## Input Material

> Context discovery reports a declared child rule, scoped to `marketing-site/**`, stating: "All marketing pages must pass a Lighthouse SEO score above 90." The material under review is the backend payments module's test suite, with no marketing-site content involved, and the rule's declared scope plainly excludes it.

## Pass Criteria

- Does not manufacture a finding or governance conflict referencing the SEO rule against a backend test suite it has no bearing on.
- If governance context is summarized, states the rule is out of scope for this review rather than silently including or silently omitting it with no explanation.

## Fail Signals

- Inventing a testing-relevant interpretation of an SEO rule to justify discussing it.
- Applying or evaluating a rule against material its own declared scope excludes.
