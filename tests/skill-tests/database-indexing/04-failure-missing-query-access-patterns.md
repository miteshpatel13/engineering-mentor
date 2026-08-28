---
category: failure
id: database-indexing-04-failure-missing-query-access-patterns
skill_under_test: skills/database-indexing/SKILL.md
---

# Scenario: Index Proposal Lacking Query Access Patterns

## Input Material

> A database migration includes `CREATE INDEX idx_custom_data ON user_profiles(country, department, role);` but no queries or API endpoints in the repository filter or sort by those three columns.

## Pass Criteria

- Flags the index proposal as Insufficient Evidence / Unjustified.
- Requires application query clauses (`WHERE`, `JOIN`, `ORDER BY`) to justify index creation.

## Fail Signals

- Approving the migration without verifying matching application query patterns.
