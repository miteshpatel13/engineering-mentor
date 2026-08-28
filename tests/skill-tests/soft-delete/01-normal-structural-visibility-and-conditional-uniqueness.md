---
id: soft-delete-01-normal-structural-visibility-and-conditional-uniqueness
category: normal
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Designing Soft-Delete for a Customer Account Table

## Input Material

> Design soft-delete for a `customers` table with a `email` column that must be unique among active customers. Deletions should be recoverable for a period, and deleted customers must never appear in normal listing/search queries used across the application (dozens of call sites).

## Pass Criteria

- Recommends structural query-visibility exclusion (Rules → Query Visibility) — a shared data-access mechanism (base repository/query scope), not a per-call-site filter across dozens of sites.
- Recommends a conditional/partial uniqueness mechanism for `email` (Rules → Natural-Key Uniqueness) so a deleted customer's email becomes reusable, rather than a plain unconditional `UNIQUE` constraint.
- States the mechanism choice depends on the declared engine's actual capability (native partial index vs. workaround) rather than assuming one universally.

## Fail Signals

- Recommending a per-call-site `WHERE` filter as sufficient given the stated dozens-of-call-sites scale.
- Recommending a plain unconditional `UNIQUE (email)` constraint with no reasoning about reuse after deletion.
