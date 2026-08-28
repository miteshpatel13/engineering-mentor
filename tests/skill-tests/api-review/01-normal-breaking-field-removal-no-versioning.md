---
id: api-review-01-normal-breaking-field-removal-no-versioning
category: normal
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Field Removed From a Public API With No Deprecation

## Input Material

> A proposed change removes the `legacyId` field from the response of `GET /v1/customers/:id`, a documented public API with known external consumers. No deprecation period, migration notice, or new API version is proposed — the field simply disappears in the next deploy.

## Pass Criteria

- Flags this as a Versioning/Compatibility finding at HIGH — removing a field from a public, externally-consumed API with no accommodation breaks existing consumers.
- Recommends a concrete fix: a deprecation period, or introducing a new API version, before actual removal.

## Fail Signals

- Approving the removal because the field is "legacy" without addressing the breaking-change risk to existing consumers.
- Failing to distinguish this from an internal-only, no-external-consumer scenario.
