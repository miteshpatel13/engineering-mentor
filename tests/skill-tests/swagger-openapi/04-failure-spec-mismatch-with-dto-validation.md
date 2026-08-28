---
id: swagger-openapi-04-failure-spec-mismatch-with-dto-validation
category: failure
skill_under_test: skills/swagger-openapi/SKILL.md
---

# Scenario: Inconsistency Between Validation Decorators and OpenAPI Metadata

## Input Material

> A DTO field `email` has `@IsDefined()` and `@IsNotEmpty()` validation decorators, but its OpenAPI decorator reads `@ApiProperty({ required: false })`.

## Pass Criteria

- Identifies the mismatch between runtime DTO validation (required) and OpenAPI metadata (optional) as a defect.
- Mandates exact alignment between validation constraints and OpenAPI property documentation.

## Fail Signals

- Allowing OpenAPI property optionality metadata to contradict DTO validation rules.
