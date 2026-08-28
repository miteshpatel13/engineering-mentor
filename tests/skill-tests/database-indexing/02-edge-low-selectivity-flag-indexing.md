---
id: database-indexing-02-edge-low-selectivity-flag-indexing
category: edge
skill_under_test: skills/database-indexing/SKILL.md
---

# Scenario: Indexing Soft-Delete and Status Flags

## Input Material

> A developer proposes adding `CREATE INDEX idx_is_deleted ON users(is_deleted);` and `CREATE INDEX idx_status ON users(status);` to accelerate admin queries that filter active users. The `users` table has 95% `is_deleted = false` and 4 distinct `status` enum values.

## Pass Criteria

- Rejects standalone indexes on `is_deleted` and `status` due to poor selectivity.
- Explains that query optimizers will perform full table scans when selectivity is low.
- Recommends incorporating `is_deleted` or `status` into composite indexes alongside high-selectivity columns (e.g. `tenant_id` or `email`).

## Fail Signals

- Approving standalone boolean or low-cardinality enum indexes.
- Claiming boolean indexes provide high read acceleration without composite context.
