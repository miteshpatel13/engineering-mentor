---
id: performance-review-07-governance-additive-child-mandatory-p99-target
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Child Mandatory Rule Adds a Stricter Target on Top of Mentor Baseline

## Input Material

> Context discovery reports a Mentor Mandatory requirement that payment-critical endpoints have a defined p95 latency target, and a declared Child Mandatory rule stating: "Payment-critical endpoints additionally require a defined p99 target, no more than 3x the p95 target." The checkout endpoint under review has a stated, measured p95 target and value (satisfying the Mentor baseline) but no p99 target defined anywhere in the material.

## Pass Criteria

- Recognizes the child rule as Additive — it adds a p99-target requirement on top of the Mentor p95 baseline, without replacing or weakening it (which the material shows is satisfied).
- Flags the missing p99 target as a finding against the Child Mandatory rule.
- Does not treat the missing p99 target as negating that the base Mentor requirement was met.

## Fail Signals

- Ignoring the missing p99 target because the base p95-target requirement is otherwise satisfied.
- Misclassifying the Child Mandatory addition as a Prohibited Override.
