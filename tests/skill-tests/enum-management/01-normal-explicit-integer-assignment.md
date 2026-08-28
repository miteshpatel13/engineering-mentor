---
id: enum-management-01-normal-explicit-integer-assignment
category: normal
skill_under_test: skills/enum-management/SKILL.md
---

# Scenario: Designing an Explicitly Assigned Code Enum

## Input Material

> A developer proposes a new `PaymentStatus` enum in code:
> `enum PaymentStatus { PENDING, SUCCESS, FAILED, REFUNDED }`
> The values will be persisted in a database column `payment_status_id`.

## Pass Criteria

- Requires explicit integer values for every member (`PENDING = 1, SUCCESS = 2, FAILED = 3, REFUNDED = 4`).
- Explains that implicit auto-increment values lead to silent data corruption if members are reordered or inserted in the middle.
- Recommends a standard integer column (e.g. `TINYINT UNSIGNED`) in the database with explicit comment mappings.

## Fail Signals

- Approving implicit auto-increment enum values.
- Recommending string literals or native SQL `ENUM` types without considering DDL lock drawbacks.
