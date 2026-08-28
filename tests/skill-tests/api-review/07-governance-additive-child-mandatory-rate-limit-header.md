---
id: api-review-07-governance-additive-child-mandatory-rate-limit-header
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Child Mandatory Rule Adds a Stricter Contract Requirement on Top of Mentor Baseline

## Input Material

> Context discovery reports a Mentor Mandatory requirement that error responses use a consistent shape across the API, and a declared Child Mandatory rule stating: "All public endpoints must additionally return `X-RateLimit-Remaining` and `X-RateLimit-Reset` response headers." The endpoint under review returns the correct, consistent error shape but includes neither rate-limit header anywhere in the material.

## Pass Criteria

- Recognizes the child rule as Additive — it adds a response-header requirement on top of the Mentor error-shape baseline, without replacing or weakening it (which the material shows is satisfied).
- Flags the missing rate-limit headers as a finding against the Child Mandatory rule.
- Does not treat the missing headers as negating that the base Mentor requirement was met.

## Fail Signals

- Ignoring the missing headers because the base error-shape requirement is otherwise satisfied.
- Misclassifying the Child Mandatory addition as a Prohibited Override.
