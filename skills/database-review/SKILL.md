---
name: database-review
description: Review database schema, queries, migrations, and data-integrity risk — constraints, indexes, N+1 patterns, transactions, and concurrency. Use when reviewing a schema change, a new migration, or a query/ORM pattern for correctness and production safety.
category: Database
skillType: Review
---

# Database Review

## Purpose

Produce a structured, evidence-based review of a database schema change, migration, or query/ORM pattern for correctness, data-integrity risk, and production safety. This Skill exists separately from `skills/code-review/SKILL.md` because database changes carry a distinct risk profile — a syntactically clean migration can still corrupt data, deadlock under concurrent load, or silently drop a constraint that was load-bearing for application correctness — that requires reasoning about the schema and data over time, not just the diff in isolation.

## Scope

**In scope:** schema constraints (types, nullability, defaults, foreign keys, uniqueness), indexes and their relationship to actual query patterns, whether an index is actually used by the query planner, over-fetching (columns/rows selected beyond what's consumed), N+1 query risk, transaction boundaries and isolation behavior, concurrent-update and locking risk, migration safety against existing production data, and ORM-specific behavior (lazy loading, cascade rules, generated queries) where the target repository's stack uses one.

**Out of scope:** measured query latency and throughput under load (`skills/performance-review/SKILL.md` — this Skill flags a query *pattern* that is structurally likely to be slow, e.g. an unindexed lookup, but does not measure actual performance); application-level authorization logic that happens to touch the database (`skills/security-review/SKILL.md`); and general code-level defects unrelated to data access (`skills/code-review/SKILL.md`).

## When to Use

Use when: reviewing a new or modified database schema or migration; reviewing a query or ORM usage pattern for correctness; assessing whether a change introduces a data-integrity, concurrency, or migration-safety risk; or evaluating whether an index change matches the query patterns it's meant to serve.

Do not use for tuning a query that is already known-correct but measured slow with production evidence — start there with `skills/performance-review/SKILL.md`, which may then point back here if the fix is a schema/index change.

## Required Context

- The schema, migration, or query/ORM code under review, including enough surrounding context (existing schema, existing indexes, the query's actual call site) to reason about correctness — a migration diff with no view of the current schema state cannot be fully assessed for what it changes relative to.
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack (which database engine and, where applicable, which ORM) — a finding phrased against the wrong engine's actual behavior (e.g. assuming a lock behavior specific to one database engine when the repository uses another) is worse than no finding.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context, in particular the declared database engine and ORM, before reasoning about any engine-specific behavior.
2. Confirm the material provided is sufficient to evaluate the change against its actual current schema state (Required Context). If the current schema isn't available and the change's correctness genuinely depends on it (e.g. a new foreign key against a table whose existing data isn't visible), proceed to Failure Handling rather than assuming the migration is safe.
3. Evaluate the change against each Rules category below, grounded in the repository's actual declared engine/ORM — never against generic SQL behavior that doesn't hold for the repository's actual engine. `context/standards/Database Standards.md` is the grounding checklist the Rules below instantiate.
4. When step 1 obtained declared child rules and/or exceptions, apply the Child Governance discipline (Rules, below) to any that plausibly bear on schema or data-access conventions.
5. Produce the review per Expected Output.

## Rules

### Constraints and Nullability

Flag a new or modified column whose nullability, type, or default doesn't match how the application actually uses it (e.g. a column the application always populates, left nullable with no enforced invariant). Flag a missing foreign key or uniqueness constraint where the material shows the relationship is meant to be enforced, not merely conventionally maintained by application code alone.

### Indexes and Query Patterns

Flag a query pattern that scans or filters on an unindexed column at a scale where that matters, and flag an index that doesn't match the actual query pattern it's apparently meant to serve (wrong column order in a composite index, an index that duplicates an existing one). Do not recommend an index purely from a query's shape without evidence of the table's actual or expected scale — an unindexed filter on a table that will only ever hold dozens of rows is not a finding.

### Query-Plan Verification

For a query whose correctness depends on an index actually being used (Indexes and Query Patterns, above), flag the absence of any evidence — an execution plan, an `EXPLAIN` output, or equivalent — that the intended index is actually selected by the query planner for that query's actual shape. A correctly-defined index does not guarantee the planner uses it; a query with a function wrapped around an indexed column, an implicit type cast, or a leading wildcard on a `LIKE` pattern can silently bypass an otherwise-correct index. This is a verification concern distinct from `skills/performance-review/SKILL.md`'s measured-latency concern: this Rule is about whether the query is confirmed to behave as intended, not about how fast it runs.

### Over-Fetching

Flag a query that selects more columns or rows than the calling code actually uses — a `SELECT *` where the code reads only specific fields, or a query with no bound where only a subset of the results is ever consumed. This is a data-*shape* correctness concern, distinct from N+1 Query Risk (below), which is about query *count*, and distinct from `skills/performance-review/SKILL.md`'s measured-impact concern.

### N+1 Query Risk

Flag a pattern (typically ORM lazy-loading in a loop, or a per-row follow-up query) that issues one query per item in a collection where a single batched query would serve the same result. State the evidence for the loop (the actual code pattern), not just the ORM's general reputation for this risk.

### Transactions and Concurrency

Flag an operation that should be atomic but isn't wrapped in a transaction, and flag a transaction boundary that is wider than necessary in a way that risks lock contention or extends blast radius. Flag a read-then-write sequence on a value that can be concurrently modified with no locking or optimistic-concurrency mechanism (a classic lost-update race), where the material shows concurrent access is plausible.

### Migration Safety

Flag a migration that would fail, lock the table for an unacceptable duration, or lose data against a production-scale existing table — a column addition with a non-null default that requires a full table rewrite on some engines, a destructive column drop with no verified-unused confirmation, or a rename that isn't backward-compatible with code still running the previous version during a rolling deploy. State which of these applies based on the repository's actual declared engine, not a different engine's behavior.

### ORM Behavior

Flag ORM-specific correctness risks the target repository's declared ORM actually exhibits — an unintended cascade delete, an eager-load that fetches far more than needed, or a generated query shape that doesn't match what the code appears to intend. Do not flag a generic ORM concern the repository's actual ORM doesn't have.

### Child Governance

When context discovery (step 1) obtained parsed child rules and/or exceptions, apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines — applicability against the rule's own scope text, deterministic classification via `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`), and a Prohibited Override on a Mentor Mandatory data-integrity requirement is always preserved and reported, never silently honored.

### Severity, No Fabrication, False-Positive Discipline

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`. Never claim a migration is unsafe against production data without evidence the table actually holds production-scale or production-shaped data — an assumption stated as fact is a fabrication; state it as a question needing verification instead (Failure Handling) when the material doesn't establish it either way.

## Constraints

Never lower a finding that describes a genuine data-loss or data-integrity risk to make a migration look safer, and never approve a destructive migration (column/table drop) without explicit confirmation the dropped data is verified unused. Stay within the repository's actual declared engine and ORM; do not import a correctness claim from a different engine's semantics.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and routes child-rule/exception tier and relationship classification through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) — following `skills/code-review/SKILL.md`'s Child Governance mechanism as the reference implementation. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. Governance classification and finding severity remain independent axes (`docs/Governance Precedence Model.md` Section 12).

## Validation

A review produced by this Skill is complete when: every finding has a severity, a category (Constraints, Indexes, Query-Plan Verification, Over-Fetching, N+1, Transactions/Concurrency, Migration Safety, ORM Behavior, or Governance Conflict), a location, and a stated impact/recommendation; a migration-safety finding states which specific production-data risk applies and why, grounded in the repository's actual declared engine; and any claim about current schema state or data scale that the material doesn't establish is stated as Insufficient Evidence rather than assumed.

## Edge Cases

- **Migration reviewed with no visibility into current production data volume.** State that migration-safety findings dependent on scale (lock duration, rewrite cost) are conditional on actual table size, which is not knowable from the material provided, rather than asserting a specific risk level.
- **Query pattern reviewed in isolation, no visibility into actual call frequency.** An N+1 pattern is still flagged (it is a correctness/scalability risk regardless of current call volume), but severity should reflect that the material doesn't establish current impact, not assume worst-case production traffic.
- **New table with no existing data at all.** Migration-safety concerns tied to existing data (lock duration on a large table, backward compatibility during rollout) don't apply; state this explicitly rather than reflexively flagging every migration the same way.
- **ORM-generated migration the repository's tooling produced automatically.** Review it exactly as a hand-written migration — auto-generation is not evidence of correctness.

## Failure Handling

When the current schema state, the repository's declared engine/ORM, or the table's actual scale can't be determined from context discovery or the material provided, and the finding's correctness genuinely depends on that missing information, state the gap explicitly and do not proceed to score that specific aspect — do not assume a "typical" schema or engine behavior to fill the gap.

## Expected Output

A structured review: Summary, Findings (each with Severity, Category, Location, Problem, Impact, Recommended remediation), a Governance Conflicts subsection when applicable, Blocking Findings, Non-Blocking Recommendations, and Verification (what was checked, what scale/data assumptions the review does or doesn't make) — mirroring `skills/code-review/SKILL.md`'s output shape.

## Examples

**Positive example.** A migration adds a `NOT NULL` column with no default to a table the material shows already has rows, on a declared PostgreSQL engine. Finding: Migration Safety, HIGH — this migration will fail against existing rows without either a default value or a backfill step; recommend adding a default or a two-phase migration (add nullable, backfill, then add the constraint).

**Negative example (correctly declines to flag).** A query filters on an unindexed column, but the material shows the table is a small, bounded configuration table unlikely to ever exceed a few hundred rows. Not flagged as an index gap — Rules → Indexes and Query Patterns explicitly excludes recommending an index with no evidence of relevant scale.

**N+1 example.** A handler fetches a list of `orders`, then for each order in the result accesses `order.customer.name`, triggering one additional query per order via the ORM's lazy-loading relationship. Finding: N+1, MEDIUM (severity reflects that call frequency/scale isn't established by the material, per the Skill's own Edge Cases) — this pattern issues one query per item in the collection where a single batched query (e.g. eager-loading `customer` alongside `orders`, or a single `WHERE customer_id IN (...)` query) would serve the same result; the finding cites the actual loop-triggers-a-query pattern shown in the material, not merely the ORM's general reputation for this risk.

## Related Skills

- `skills/context-discovery/SKILL.md` — Dependency: invoked first, every time, to obtain the declared database engine/ORM before any engine-specific claim is made.
- `skills/code-review/SKILL.md` — Related: shares the Child Governance mechanism and Expected Output shape; neither Skill requires the other's output to function.
- `skills/performance-review/SKILL.md` — Related: this Skill flags structurally risky query *patterns* (N+1, missing index) without measuring actual latency; `performance-review` owns measured performance verification and may hand a schema/index fix back to this Skill, but neither depends on the other's output to begin its own review.
- `skills/security-review/SKILL.md` — Related: application-level authorization logic that happens to touch the database (e.g. a query missing a tenant-scoping filter) is that Skill's AuthZ/IDOR concern, not this Skill's data-integrity concern, even though both may examine the same query.
