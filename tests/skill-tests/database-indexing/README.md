# database-indexing Skill — Regression Fixtures

5 narrative fixture specifications for `skills/database-indexing/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Generalized from external source material with all project-specific schema details removed and replaced with technology-agnostic relational database indexing patterns.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-composite-index-ordering.md` | Normal — designing a composite index for a multi-column query with filter and sort |
| 02 | `02-edge-low-selectivity-flag-indexing.md` | Edge case — filtering on boolean and status flags without standalone index bloat |
| 03 | `03-adversarial-pressure-to-index-everything.md` | Adversarial — schedule pressure to add unneeded standalone indexes on a high-write table |
| 04 | `04-failure-missing-query-access-patterns.md` | Failure handling — query access pattern not established in material |
| 05 | `05-rule-coverage-foreign-key-indexing.md` | Rule coverage — ensuring foreign key columns used in joins are properly indexed |
