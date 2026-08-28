---
id: database-review-15-rule-coverage-over-fetching
category: rule-coverage
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Query Selects All Columns and All Rows, Only a Subset Consumed

## Input Material

> A service function runs `SELECT * FROM orders WHERE customer_id = $1` and returns the full result set upstream, but the material shows the calling code only ever reads `order.id` and `order.status` from each row, and only ever displays the first 10 results to the user with no `LIMIT` in the query itself.

## Pass Criteria

- Flags the `SELECT *` as over-fetching columns beyond what the calling code consumes, per Rules → Over-Fetching.
- Separately flags the unbounded row fetch (no `LIMIT`) when only the first 10 are ever used.
- Distinguishes this from N+1 Query Risk — this is one query returning too much *shape*, not one query per item in a loop.

## Fail Signals

- Merging this into an N+1 finding when the material shows a single query, not a per-item loop.
- Missing either the column-level or row-level over-fetching aspect, reporting only one.
