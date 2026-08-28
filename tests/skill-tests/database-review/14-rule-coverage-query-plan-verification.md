---
id: database-review-14-rule-coverage-query-plan-verification
category: rule-coverage
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Indexed Column Wrapped in a Function, No Execution-Plan Evidence

## Input Material

> A query filters `WHERE LOWER(email) = LOWER($1)` against a `users` table. An index exists on `email` (not on `LOWER(email)`). No execution plan, `EXPLAIN` output, or equivalent evidence is included anywhere in the material to show whether the index is actually used for this query.

## Pass Criteria

- Flags the absence of execution-plan evidence per Rules → Query-Plan Verification, distinct from Indexes and Query Patterns (which is about whether an index *exists* for the pattern).
- States specifically that wrapping the indexed column in `LOWER()` is a known way to silently bypass a plain index on `email`, making plan verification particularly important here, not just generically desirable.
- Does not claim certainty the index is or isn't used — states this as unverified rather than assuming either outcome.

## Fail Signals

- Treating the existence of an index on `email` as sufficient without noting the function-wrap risk or the missing plan evidence.
- Fabricating a definitive claim ("the index is not used") with no execution-plan evidence to support it.
