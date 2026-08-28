---
id: database-review-02-edge-small-config-table-no-index
category: edge
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Unindexed Filter on a Small Configuration Table

## Input Material

> Review this query: `SELECT * FROM feature_flags WHERE key = ?`. The `feature_flags` table has no index on `key`. The surrounding material states this table holds a fixed set of fewer than 50 application-defined feature flags, never user-generated data.

## Pass Criteria

- Does not recommend adding an index — Rules explicitly exclude recommending an index with no evidence of relevant scale, and this material establishes the table is small and bounded.
- May note the absence of an index without treating it as a finding, if it chooses to mention it at all.

## Fail Signals

- Flagging the missing index as a finding (with a severity) despite the stated small, bounded scale.
- Recommending an index "just in case" without engaging with the stated scale evidence.
