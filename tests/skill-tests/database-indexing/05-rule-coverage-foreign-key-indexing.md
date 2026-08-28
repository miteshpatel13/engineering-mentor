---
id: database-indexing-05-rule-coverage-foreign-key-indexing
category: rule-coverage
skill_under_test: skills/database-indexing/SKILL.md
---

# Scenario: Ensuring Foreign Key Columns Are Indexed

## Input Material

> A schema migration creates a `line_items` table with a foreign key `order_id REFERENCES orders(id)`, but does not define an index on `order_id`.

## Pass Criteria

- Recommends creating an explicit index on `order_id`.
- Explains that relational engines do not automatically index FK columns, leading to table scans on parent-child joins and deletes.

## Fail Signals

- Assuming relational database engines automatically index foreign key columns.
- Dismissing foreign key indexing as optional for relational tables.
