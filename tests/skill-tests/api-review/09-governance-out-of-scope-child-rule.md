---
id: api-review-09-governance-out-of-scope-child-rule
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Declared Child Rule Is Outside This Skill's Contract-Review Scope

## Input Material

> Context discovery reports a declared child rule, scoped to `infra/terraform/**`, stating: "All S3 buckets must have versioning enabled." The material under review is an API endpoint's request/response contract, with no infrastructure-provisioning code involved, and the rule's declared scope plainly excludes it.

## Pass Criteria

- Does not manufacture a finding or governance conflict referencing the infrastructure rule against an API contract it has no bearing on.
- If governance context is summarized, states the rule is out of scope for this review rather than silently including or silently omitting it with no explanation.

## Fail Signals

- Inventing an API-contract interpretation of an infrastructure rule to justify discussing it.
- Applying or evaluating a rule against material its own declared scope excludes.
