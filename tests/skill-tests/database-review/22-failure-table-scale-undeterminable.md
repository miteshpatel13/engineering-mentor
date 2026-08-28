---
id: database-review-22-failure-table-scale-undeterminable
category: failure
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Table's Actual Scale Cannot Be Determined, and the Finding's Correctness Genuinely Depends On It

## Input Material

> A migration adds a new non-unique index to an existing table `audit_events` on a `created_at` column, replacing a full-table-scan query pattern the material shows is currently used to filter recent events. The migration includes a lock-duration concern: on the declared engine (confirmed via context discovery), building this index without a concurrent/online index-creation option would hold a table-level lock for a duration roughly proportional to the table's current row count. The material provides no information at all about how many rows `audit_events` currently holds — no row count, no age of the table, no indication of high or low traffic.

## Pass Criteria

- States explicitly, per Failure Handling, that the migration-safety question of whether this specific index build's lock duration is "acceptable" genuinely depends on the table's current row count, which is not knowable from the material provided, and does not proceed to assign a specific risk level (e.g. "this will definitely cause a multi-minute outage") on that missing information.
- Does not default to assuming the table is small (and therefore skip the finding) or assuming it is enormous (and therefore assign the highest possible severity) — either assumption fills the gap with invention rather than stating the gap.
- Still flags the general, evidence-independent recommendation that is sound regardless of scale: using the engine's concurrent/online index-creation option (where available) avoids the scale-dependent lock-duration question entirely, and this recommendation doesn't require knowing the row count to be correct.

## Fail Signals

- Asserting a specific lock-duration risk level (e.g. "this will lock the table for several minutes") with no evidence of the table's actual row count.
- Silently treating the missing row-count information as license to skip the finding entirely, rather than stating the gap and still offering the scale-independent remediation (concurrent index creation).
