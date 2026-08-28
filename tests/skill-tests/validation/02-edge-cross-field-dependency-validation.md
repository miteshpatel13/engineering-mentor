---
id: validation-02-edge-cross-field-dependency-validation
category: edge
skill_under_test: skills/validation/SKILL.md
---

# Scenario: Validating Cross-Field Logical Dependencies

## Input Material

> An event booking endpoint accepts `start_date`, `end_date`, and `requires_hotel`. If `requires_hotel = true`, `hotel_checkin_date` is mandatory and must fall between `start_date` and `end_date`.

## Pass Criteria

- Requires service-layer cross-field validation for date range ordering (`end_date > start_date`).
- Enforces conditional dependency rule: `hotel_checkin_date` is required only when `requires_hotel = true`.
- Strips or rejects `hotel_checkin_date` if submitted when `requires_hotel = false`.

## Fail Signals

- Relying on single-field DTO decorators alone for multi-field date range ordering.
- Accepting hotel check-in dates when hotel accommodation is not requested.
