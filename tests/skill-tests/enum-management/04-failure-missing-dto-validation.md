---
id: enum-management-04-failure-missing-dto-validation
category: failure
skill_under_test: skills/enum-management/SKILL.md
---

# Scenario: Missing Enum DTO Validation at API Boundary

## Input Material

> An endpoint DTO accepts `status: number` with `@IsInt()` validation. The underlying field is backed by `OrderStatus` which has valid values `{1, 2, 3}`. Sending `status: 99` bypasses validation and attempts a DB insert.

## Pass Criteria

- Flags missing enum boundary validation as a defect.
- Requires explicit enum validation (e.g. `@IsEnum(OrderStatus)`) to reject invalid integers with `400 Bad Request` at the DTO layer.

## Fail Signals

- Relying on database foreign keys or constraints alone to catch out-of-range integers.
