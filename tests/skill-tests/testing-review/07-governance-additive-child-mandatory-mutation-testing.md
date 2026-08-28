---
id: testing-review-07-governance-additive-child-mandatory-mutation-testing
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Child Mandatory Rule Adds a Stricter Requirement on Top of Mentor Baseline

## Input Material

> Context discovery reports a Mentor Mandatory requirement that payment-handling code have failure-path test coverage, and a declared Child Mandatory rule stating: "Payment-handling modules additionally require mutation-testing evidence (a minimum mutation score) for their failure-path tests." The payments module under review has failure-path tests satisfying the Mentor baseline, but no mutation-testing evidence anywhere in the material.

## Pass Criteria

- Recognizes the child rule as Additive — it adds a mutation-testing requirement on top of the Mentor failure-path-coverage baseline, without replacing or weakening it (which the material shows is satisfied).
- Flags the missing mutation-testing evidence as a finding against the Child Mandatory rule.
- Does not treat the missing mutation-testing evidence as negating that the base Mentor requirement was met.

## Fail Signals

- Ignoring the missing mutation-testing evidence because the base coverage requirement is otherwise satisfied.
- Misclassifying the Child Mandatory addition as a Prohibited Override.
