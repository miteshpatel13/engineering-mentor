---
id: dynamic-form-engine-04-failure-hardcoded-field-type-switch-blocks
category: failure
skill_under_test: skills/dynamic-form-engine/SKILL.md
---

# Scenario: Adding Field Types via Monolithic Switch Statements

## Input Material

> A developer introduces a new `SIGNATURE` field type by adding a new `case 'SIGNATURE':` branch into 14 different `switch(fieldType)` statements across controllers, services, and validation helpers.

## Pass Criteria

- Flags monolithic switch statements across multiple files as an architectural defect.
- Mandates implementing new field types via a self-contained `FieldTypeRegistry` encapsulating rendering, validation, and serialization.

## Fail Signals

- Approving scattered `switch` or `if/else` logic for extending field types instead of a registry pattern.
