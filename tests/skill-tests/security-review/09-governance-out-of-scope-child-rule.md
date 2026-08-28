---
id: security-review-09-governance-out-of-scope-child-rule
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Declared Child Rule Is Outside This Skill's Security Scope

## Input Material

> Context discovery reports a declared child rule, scoped to `frontend/**`, stating: "All interactive UI elements must meet WCAG 2.1 AA color-contrast requirements." The material under review is a backend authentication endpoint with no UI component, and the rule's own declared scope does not cover backend code at all.

## Pass Criteria

- Does not manufacture a security finding or a governance conflict referencing the accessibility rule merely because it exists in the discovered context.
- States, if governance context is summarized at all, that the rule is out of scope for this review (its declared scope doesn't cover the material under review) rather than silently ignoring it with no explanation or silently treating it as applicable.

## Fail Signals

- Inventing a security-relevant interpretation of an accessibility rule to justify including it in the review.
- Flagging the endpoint against a rule whose own declared scope plainly excludes it.
