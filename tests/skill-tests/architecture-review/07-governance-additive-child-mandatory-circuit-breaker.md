---
id: architecture-review-07-governance-additive-child-mandatory-circuit-breaker
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Child Mandatory Rule Adds a Stricter Failure-Isolation Requirement on Top of Mentor Baseline

## Input Material

> Context discovery reports a Mentor Mandatory requirement that a service boundary have a defined failure mode (timeout, retry, or fallback), and a declared Child Mandatory rule stating: "Calls to third-party payment providers additionally require a circuit breaker." The design under review shows the payment-provider integration has a timeout and a fallback defined (satisfying Mentor's baseline) but no circuit breaker anywhere in the material.

## Pass Criteria

- Recognizes the child rule as Additive — it adds a circuit-breaker requirement on top of the Mentor failure-mode baseline, without replacing or weakening it (which the material shows is satisfied).
- Flags the missing circuit breaker as a finding against the Child Mandatory rule.
- Does not treat the missing circuit breaker as negating that the base Mentor requirement was met.

## Fail Signals

- Ignoring the missing circuit breaker because the base failure-mode requirement is otherwise satisfied.
- Misclassifying the Child Mandatory addition as a Prohibited Override.
