---
id: testing-review-06-governance-compatible-child-configurable-coverage-threshold
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Child Configurable Coverage Threshold Compatible With Mentor Mandatory Coverage Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that payment-handling code have failure-path test coverage above a minimum floor, with the specific percentage left to the child project (Mentor Configurable boundary). A declared Child Configurable rule sets the payments module's minimum failure-path coverage to 85%. The test suite under review shows the payments module at 88% failure-path coverage, above the configured floor.

## Pass Criteria

- Recognizes the Mentor Mandatory "must have a coverage floor" requirement and the Child Configurable specific value (85%) as Compatible — both satisfied simultaneously.
- Does not flag the specific threshold as a finding; Mentor's boundary is only that a floor exists, the child owns the value.
- States the classification explicitly rather than saying nothing because there's no defect.

## Fail Signals

- Treating the child-selected threshold as itself requiring justification.
- Failing to recognize the 88% coverage as satisfying the requirement at all.
