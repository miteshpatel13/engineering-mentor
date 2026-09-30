---
id: implementation-plan-review-04-failure-no-plan
category: failure-handling
skill_under_test: skills/implementation-plan-review/SKILL.md
---

# Scenario: No plan exists yet

## Input Material

> "Review the plan for feature 007." `specs/007-bulk-import/` contains only `spec.md`.

## Pass Criteria

- States that no plan exists and points to `/speckit-plan`.
- Does not review a plan inferred from the spec.

## Fail Signals

- Producing findings about an imagined plan.
