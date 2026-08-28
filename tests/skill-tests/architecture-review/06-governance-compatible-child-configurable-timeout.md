---
id: architecture-review-06-governance-compatible-child-configurable-timeout
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Child Configurable Timeout Value Compatible With Mentor Mandatory Failure-Isolation Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that cross-service calls have an explicit timeout to bound failure blast radius, with the specific duration left to the child project (Mentor Configurable boundary). A declared Child Configurable rule sets the payment-service client timeout to 3 seconds. The design under review shows the checkout flow's payment-service call configured with exactly that 3-second timeout.

## Pass Criteria

- Recognizes the Mentor Mandatory "must have an explicit timeout" requirement and the Child Configurable specific value (3s) as Compatible — both satisfied simultaneously.
- Does not flag the specific duration as a finding; Mentor's boundary is only that a timeout exists, the child owns the value.
- States the classification explicitly rather than saying nothing because there's no defect.

## Fail Signals

- Treating the child-selected timeout value as itself requiring justification.
- Failing to recognize the design as satisfying the failure-isolation requirement at all.
