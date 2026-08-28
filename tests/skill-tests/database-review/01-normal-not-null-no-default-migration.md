---
id: database-review-01-normal-not-null-no-default-migration
category: normal
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: NOT NULL Column Added With No Default

## Input Material

> Context discovery reports the repository's declared database engine as PostgreSQL. Review this migration: `ALTER TABLE users ADD COLUMN phone_verified BOOLEAN NOT NULL;` The `users` table is known (from the surrounding material) to already contain rows.

## Pass Criteria

- Flags this as a Migration Safety finding: the migration will fail against existing rows with no default value.
- States the concrete failure mode (existing rows have no value to satisfy the NOT NULL constraint).
- Recommends a concrete fix: add a default, or a two-phase migration (nullable → backfill → add constraint).

## Fail Signals

- Approving the migration without flagging the missing-default risk against existing data.
- Recommending a fix with no explanation of why the migration would fail.
