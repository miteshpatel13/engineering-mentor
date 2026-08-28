---
id: database-indexing-01-normal-composite-index-ordering
category: normal
skill_under_test: skills/database-indexing/SKILL.md
---

# Scenario: Designing a Composite Index for a Filtered and Sorted Query

## Input Material

> Design an index for an order history lookup query:
> `SELECT * FROM orders WHERE customer_id = ? AND status = 'SHIPPED' AND created_at >= ? ORDER BY created_at DESC;`
> The table has millions of rows. Currently, there is only a primary key on `id`.

## Pass Criteria

- Orders columns in the composite index correctly: equality filters (`customer_id`, `status`) first, followed by range/sort filter (`created_at`).
- Recommends a single composite index `(customer_id, status, created_at)` rather than multiple single-column indexes.
- Explains that placing `created_at` before `status` would prevent index usage for the equality check on `status`.

## Fail Signals

- Recommending separate single-column indexes on `customer_id`, `status`, and `created_at`.
- Placing the range column (`created_at`) first in the composite index column order.
- Ignoring the `ORDER BY` requirement when specifying the composite index.
