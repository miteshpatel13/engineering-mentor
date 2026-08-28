---
id: uuid-strategy-02-edge-internal-only-table-no-benefit
category: edge
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Internal Configuration Table With No External Surface

## Input Material

> A `feature_flags` table is read only by internal services over a private network; it has no external API, no external caller ever sees its identifiers, and its existence/count is not sensitive. A developer proposes giving it a random opaque primary key "for consistency with the rest of the schema, since most tables use one."

## Pass Criteria

- Concludes an opaque identifier is not warranted here (Rules → When an Opaque Identifier Is Warranted) — no external audience, no enumeration concern, no sensitivity.
- Names the real cost this "consistency" choice would incur for no benefit (Rules → Storage, Indexing, and Ordering — index fragmentation from random insert order).
- Does not treat "most other tables use one" as sufficient justification on its own.

## Fail Signals

- Recommending the opaque identifier anyway for stylistic consistency without weighing the stated cost against the absent benefit.
- Failing to name the specific cost (index fragmentation / insert-order randomness) this Skill's Rules actually identify.
