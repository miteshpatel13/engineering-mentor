---
id: database-review-19-edge-new-table-no-existing-data
category: edge
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Brand-New Table With No Existing Data — Existing-Data Migration Concerns Don't Apply

## Input Material

> A migration creates a brand-new table `feature_flags` with a `NOT NULL` column `enabled` and no default value, and adds a foreign key to an existing `services` table. The material confirms this is the table's creation migration — the table has never existed before this migration, so it holds zero rows at the moment this migration runs, and no other code in the repository yet references it (this is the first migration to introduce it).

## Pass Criteria

- Does not flag the `NOT NULL` column with no default as a Migration Safety risk — per the Skill's own named Edge Case ("New table with no existing data at all"), migration-safety concerns tied to *existing* data (a rewrite/lock against rows that already exist, backward compatibility with a previous schema version during rollout) don't apply to a table's own creation migration, since there is no existing data to violate the constraint and no prior schema version consumers to break.
- States this explicitly (e.g. "no existing-data risk — this is the table's creation migration") rather than reflexively applying the same NOT-NULL-no-default finding this Skill would correctly raise against an *already-populated* table (contrast with fixture 01).
- Still evaluates the table for genuine, applicable concerns independent of existing-data risk: the foreign key to `services`, the `enabled` column's type/nullability choice as a design decision, and any index needs — Edge Case treatment narrows which findings apply, it does not exempt the migration from review entirely.

## Fail Signals

- Flagging the `NOT NULL` column with no default as if this were an already-populated table being altered (reflexively applying fixture 01's finding pattern without checking whether the table is new).
- Treating "new table" as a reason to skip review of the migration altogether, rather than narrowing specifically which findings apply.
