---
id: performance-review-06-governance-compatible-child-configurable-target
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Child Configurable Latency Target Compatible With Mentor Mandatory Measurable-Target Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that payment-critical endpoints have a defined p95 latency target, with the specific number left to the child project (Mentor Configurable boundary). A declared Child Configurable rule sets the checkout endpoint's p95 target to 400ms. The investigation under review states the checkout endpoint's measured p95 is 350ms against exactly that configured 400ms target.

## Pass Criteria

- Recognizes the Mentor Mandatory "must have a defined target" requirement and the Child Configurable specific value (400ms) as Compatible — both satisfied simultaneously.
- Does not flag the specific target number as a finding; Mentor's boundary is only that a target exists, the child owns the value.
- States the classification explicitly rather than saying nothing because there's no defect.

## Fail Signals

- Treating the child-selected target value as itself requiring justification.
- Failing to recognize the endpoint as satisfying the measurable-target requirement at all.
