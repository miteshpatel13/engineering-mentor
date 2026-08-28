---
name: database-indexing
description: The general engineering pattern for database index strategy — indexing for actual query patterns, composite index column ordering, low-selectivity filtering, soft-delete interaction, write overhead tradeoffs, and index verification. Reference material consumed by database-review and performance-review.
category: Domain Patterns
skillType: Domain Pattern
---

# Database Indexing

## Purpose

Produce the shared, reusable reference pattern for database index design — indexing to serve actual query patterns (filters, joins, sorting, pagination) rather than indexing columns reflexively. This exists as its own Skill because indexing strategy is a foundational data-tier concern that `database-review` (schema correctness, index choices) and `performance-review` (query latency, write overhead, execution plans) both reference when evaluating database code. This Skill provides the technical foundation both point to, following `docs/Skill Taxonomy.md` Section 2's composition model.

## Scope

**In scope:** index selection based on query patterns, composite index column ordering (equality vs range vs sort), selectivity analysis, indexing foreign keys and primary keys, combining soft-delete or status flags into composite indexes, balancing read acceleration against write maintenance overhead, and index verification via execution plans (`EXPLAIN`).

**Out of scope:** reviewing a specific migration or query in a target codebase — that is `skills/database-review/SKILL.md`'s concern; evaluating server-level buffer pool tuning or disk IOPS — `skills/performance-review/SKILL.md`'s concern. This Skill teaches the pattern and produces no review findings of its own.

## When to Use

Use when:
- Designing indexes for a new or modified database table.
- Analyzing access patterns for filtered, sorted, or paginated endpoints.
- Evaluating why a database query is performing a full table scan or filesort.
- Deciding whether a proposed index is justified against its write-overhead cost.
- Referencing indexing rules during a database review or performance audit.

Do not use for non-relational key-value stores where indexing concepts do not apply in the same relational form.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The indexing patterns (selectivity, composite ordering, FK coverage) apply across relational databases. When specific engine context (e.g. MySQL, PostgreSQL) or ORM configuration is available via `skills/context-discovery/SKILL.md`, recommendations adapt to engine-specific capabilities (such as partial indexes or expression indexes), but the core principles remain valid in the abstract.

## Workflow

1. **Identify actual query patterns:** Extract the exact `WHERE`, `JOIN ON`, `GROUP BY`, and `ORDER BY` clauses from application queries.
2. **Evaluate primary and foreign key coverage:** Confirm primary keys (clustered/unique) and foreign key columns are indexed to optimize join resolution.
3. **Analyze column selectivity:** Calculate or estimate distinct value ratios. Avoid standalone indexes on low-cardinality columns (e.g. booleans, small enums).
4. **Design composite indexes:** For multi-column queries, order columns: equality-filtered columns first, range-filtered columns second, and sort/pagination columns last.
5. **Account for soft-delete & status flags:** Incorporate soft-delete (`is_deleted`) or status fields into composite indexes alongside high-selectivity columns rather than indexing low-cardinality flags alone.
6. **Balance write overhead:** Audit total indexes per table. Avoid redundant indexes covered by existing composite prefixes.

## Rules

### Index Actual Query Patterns, Not Columns Alone

Indexes must be designed around documented application access patterns. Adding an index because a column "might be filtered on someday" adds write-overhead latency and storage cost without providing read benefits. Every index must map to a specific `WHERE`, `JOIN`, or `ORDER BY` requirement.

### Foreign Key Indexing

All foreign key columns used in relational joins should be indexed. Many relational database engines (such as MySQL InnoDB) do not automatically index foreign key columns for join performance, and missing FK indexes cause expensive full-table scans during parent-child joins and cascading check operations.

### Composite Index Column Ordering

Multi-column composite indexes must follow the access pattern structure:
1. **Equality columns first:** Columns filtered with exact equality (`=`, `IS NULL`).
2. **Range columns second:** Columns filtered with inequality or range conditions (`>`, `<`, `BETWEEN`, `LIKE 'prefix%'`).
3. **Sort columns last:** Columns specified in `ORDER BY` to allow index-based sorting and prevent in-memory filesorts.

Putting a range column before an equality column in a composite index prevents the database engine from using subsequent index columns for equality lookups.

### Low-Selectivity and Flag Columns

Standalone indexes on low-cardinality columns (booleans, status enums with few distinct values) have poor selectivity. Database query optimizers will routinely skip such indexes in favor of full table scans. Low-selectivity columns should only be indexed as trailing (or leading) elements in a composite index alongside high-selectivity fields (e.g., `INDEX (tenant_id, status)` rather than `INDEX (status)`).

### Soft-Delete Integration

When a table uses soft-delete (`is_deleted` flag or `deleted_at` timestamp), queries almost universally append `WHERE is_deleted = false`. Do not create a standalone index on `is_deleted`. Instead, incorporate the soft-delete column into composite indexes serving specific lookups (e.g., `INDEX (organization_id, is_deleted)` or via generated conditional unique keys as outlined in `skills/soft-delete/SKILL.md`).

### Avoiding Redundant Index Prefixes

A composite index on `(A, B, C)` can serve queries filtering on `(A)`, `(A, B)`, and `(A, B, C)`. Adding separate standalone indexes on `(A)` or `(A, B)` creates redundant indexes that waste memory and increase write overhead.

### Write Overhead Tradeoff

Every index must be updated on every `INSERT`, `UPDATE`, and `DELETE` operation. On high-throughput write tables, excessive indexing degrades write performance and increases index fragmentation. Limit indexing to essential access paths.

## Constraints

- Never recommend standalone indexes on boolean or low-cardinality flag fields.
- Do not present specific database engine syntax as mandatory universal syntax; use engine-agnostic SQL concepts while noting engine-specific capabilities as examples.
- Do not add indexes without an explicit accompanying query pattern requirement.

## Governance Integration

This Skill supplies reference material (Domain Pattern) consumed by Review-type Skills (`database-review`, `performance-review`) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** The rules in this Skill represent strongly recommended database design practices grounded in `context/standards/Database Standards.md`.
- **Child Rules:** Projects may define specific naming conventions (e.g. `idx_<table_name>_<col1>_<col2>`) or index density limits in `.mentor/rules/`. Compatible child rules narrow naming without altering indexing mechanics.

## Validation

This Skill produces no artifact directly. Its patterns are verified when database schemas and queries meet the following:
- Every index matches a documented query access path.
- Foreign keys participating in joins are indexed.
- Composite index columns are ordered equality -> range -> sort.
- No redundant prefix indexes exist.

## Edge Cases

- **Covering Indexes:** When a query selects only columns present in a composite index, the database engine can fulfill the query entirely from the index (index-only scan), bypassing table data pages entirely.
- **Prefix Matching on Strings:** Indexing long text/string columns should use prefix indexing (e.g., first 20 characters) or hash indexing to limit index size while preserving selectivity.
- **Large Sorts with Offset Pagination:** Deep pagination (`LIMIT 10000 OFFSET 50000`) degrades even with indexes; keyset pagination (`WHERE id > last_seen_id ORDER BY id LIMIT 50`) is preferred for large datasets.

## Failure Handling

When query patterns or execution plans cannot be determined from available schema/code artifacts, state Insufficient Evidence rather than assuming index requirements, per the Mentor Operating Model No Invention Rule.

## Expected Output

Reference material. Consuming Review Skills (`database-review`, `performance-review`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Composite Index for Filtered List Endpoint
```sql
-- Query: Retrieve active orders for a customer, ordered by order date desc
-- SELECT * FROM orders WHERE customer_id = ? AND status = 'COMPLETED' AND is_deleted = 0 ORDER BY created_at DESC;

-- Correct Composite Index: (Equality fields first, sort field last)
CREATE INDEX idx_orders_customer_status_deleted_created 
ON orders (customer_id, status, is_deleted, created_at DESC);
```

### Negative Example: Poor Column Ordering and Low Selectivity
```sql
-- INCORRECT: Standalone index on low-selectivity boolean
CREATE INDEX idx_orders_deleted ON orders (is_deleted);

-- INCORRECT: Range column before equality column in composite index
-- Query filters WHERE created_at > ? AND customer_id = ?
CREATE INDEX idx_orders_wrong_order ON orders (created_at, customer_id);
```

## Related Skills

- `skills/database-review/SKILL.md` — Related: Consumes this Skill to evaluate schema migrations and query efficiency.
- `skills/performance-review/SKILL.md` — Related: Consumes this Skill when analyzing query latency, EXPLAIN plans, and write overhead.
- `skills/soft-delete/SKILL.md` — Related: Provides the soft-delete generated column and query scoping patterns that interact with indexing.
