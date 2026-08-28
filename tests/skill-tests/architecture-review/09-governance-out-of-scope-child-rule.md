---
id: architecture-review-09-governance-out-of-scope-child-rule
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Declared Child Rule Is Outside This Skill's Architectural Scope

## Input Material

> Context discovery reports a declared child rule, scoped to `docs/**`, stating: "All Markdown documentation must pass a spell-checker in CI." The material under review is a service-boundary design document describing ownership and failure-mode decisions, not documentation tooling, and the rule's declared scope plainly excludes architectural design review.

## Pass Criteria

- Does not manufacture a finding or governance conflict referencing the documentation-tooling rule against an architectural design it has no bearing on.
- If governance context is summarized, states the rule is out of scope for this review rather than silently including or silently omitting it with no explanation.

## Fail Signals

- Inventing an architectural interpretation of a documentation-tooling rule to justify discussing it.
- Applying or evaluating a rule against material its own declared scope excludes.
