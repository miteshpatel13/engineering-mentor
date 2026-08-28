---
id: database-review-08-governance-advisory-no-conflict-naming-convention
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Child Advisory Concurrency-Control Preference Diverges From Generic Guidance Without a Mandatory Conflict

## Input Material

> Context discovery reports a declared Child Advisory rule: "Prefer optimistic concurrency control (a `version` integer column, incremented and checked on every update) over row-level locking for update conflicts on user-editable records in this project, since our access pattern is mostly read-heavy with rare true collisions, and pessimistic locks measurably hurt throughput under our load in past incidents." The migration and query under review implement a read-then-write update on a user-editable `documents` table using a `version` column: the update statement includes `WHERE id = :id AND version = :expectedVersion`, and the application code rejects the update (rather than silently proceeding) when zero rows are affected — a correctly implemented optimistic-concurrency mechanism, consistent with the child's stated preference. Rules → Transactions and Concurrency flags a read-then-write sequence on a concurrently-modifiable value only when "no locking or optimistic-concurrency mechanism" is present.

## Pass Criteria

- Recognizes the `version`-column pattern as a real, correctly-implemented optimistic-concurrency mechanism that directly satisfies Rules → Transactions and Concurrency's concern about unprotected read-then-write sequences — this requires checking the actual mechanism (the `WHERE ... AND version = :expectedVersion` clause and the zero-rows-affected rejection), not merely noting that a Child Advisory rule exists.
- Recognizes the Child Advisory preference for optimistic over pessimistic concurrency control as a legitimate, stated project convention (`docs/Governance Precedence Model.md` Section 8) — no Mentor Mandatory requirement mandates row-level locking specifically; Mentor's actual requirement is that *some* protection against a lost-update race exists.
- Does not report a missing-locking finding, since a real concurrency-control mechanism is present and correctly implemented — distinguishes this from a case where the child rule exists but no actual mechanism backs it up (which would still be a finding despite the rule).
- Does not manufacture a governance conflict where the child's stated preference and the material's actual implementation agree.

## Fail Signals

- Flagging the absence of row-level locking as a defect, ignoring that a correctly-implemented optimistic-concurrency mechanism is present and satisfies the same underlying Rule.
- Treating the Child Advisory rule's mere existence as sufficient evidence of compliance without checking whether the material actually implements the mechanism the rule describes (e.g. passing this fixture even if the `version` check or the zero-rows-affected rejection were missing from the material).
- Manufacturing a governance-conflict callout when the child rule and the material are in full agreement.
