---
id: validation-01-normal-two-layer-validation-architecture
category: normal
skill_under_test: skills/validation/SKILL.md
---

# Scenario: Separating Structural DTO Validation from Service Business Rules

## Input Material

> Design an API endpoint for creating a project subscription. The request includes `organization_id`, `plan_code`, and `user_seats`. The system must verify that:
> 1. `organization_id` is a valid UUID, `plan_code` is a valid enum, `user_seats` is an integer >= 1.
> 2. The organization has an active billing method on file and has not exceeded its plan quota.

## Pass Criteria

- Separates shape checks (UUID, Enum, Min Integer) into DTO layer (`400 Bad Request`).
- Places domain checks (billing method, plan quota) into Service layer (`422 Unprocessable Entity` or `409 Conflict`).
- Explains why merging both passes into a single controller check violates validation architecture.

## Fail Signals

- Performing database business-rule queries inside the DTO structural validator.
- Returning generic `500 Internal Server Error` for malformed DTO fields.
