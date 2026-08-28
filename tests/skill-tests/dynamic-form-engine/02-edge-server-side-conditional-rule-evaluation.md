---
id: dynamic-form-engine-02-edge-server-side-conditional-rule-evaluation
category: edge
skill_under_test: skills/dynamic-form-engine/SKILL.md
---

# Scenario: Server-Side Conditional Rule Re-Evaluation

## Input Material

> A form contains a boolean question `has_dietary_restrictions` and a conditional text field `dietary_details` marked `required = true` when `has_dietary_restrictions = true`. User B submits `has_dietary_restrictions = false` and leaves `dietary_details` blank.

## Pass Criteria

- Re-evaluates conditional logic rules server-side using submitted values.
- Determines that `dietary_details` is hidden based on `has_dietary_restrictions = false`.
- Waives the `required = true` validation check for `dietary_details` because it is conditionally hidden.

## Fail Signals

- Validating mandatory requirements on fields that server-side conditional logic determines to be hidden.
- Relying on client-asserted field visibility flags instead of server-side rule execution.
