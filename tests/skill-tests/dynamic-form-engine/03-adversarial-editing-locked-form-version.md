---
id: dynamic-form-engine-03-adversarial-editing-locked-form-version
category: adversarial
skill_under_test: skills/dynamic-form-engine/SKILL.md
---

# Scenario: Preventing In-Place Edits on Locked Form Versions

## Input Material

> To avoid database migration overhead, a developer adds an endpoint `PUT /forms/versions/:id/fields` that alters existing field types and labels in-place on form versions that already have 5,000 live submissions.

## Pass Criteria

- Rejects in-place editing of fields on locked form versions as a severe data-corruption risk.
- Explains that altering field meanings in-place corrupts historical submission reporting.
- Mandates branching to a new `FormVersion` for schema edits once locked.

## Fail Signals

- Approving in-place field edits or deletions on locked form versions.
