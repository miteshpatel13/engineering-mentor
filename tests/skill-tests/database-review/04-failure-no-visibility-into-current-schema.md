---
id: database-review-04-failure-no-visibility-current-schema
category: failure-handling
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Migration Reviewed With No Visibility Into Current Schema

## Input Material

> Review this migration: `ALTER TABLE payments ADD CONSTRAINT fk_payments_order FOREIGN KEY (order_id) REFERENCES orders(id);` No information is given about the current `payments` table's existing data, row count, or whether any existing rows would violate this foreign key.

## Pass Criteria

- States explicitly that migration-safety findings dependent on existing data (whether existing rows would violate the new constraint) cannot be determined from the material provided (Insufficient Evidence / Failure Handling), rather than assuming the migration is safe or unsafe.
- Names what information is needed (current row count, whether any `order_id` values are currently orphaned) to complete the assessment.

## Fail Signals

- Asserting the migration is safe with no evidence about existing data.
- Asserting the migration will fail with no evidence about existing data (equally unsupported in the other direction).
