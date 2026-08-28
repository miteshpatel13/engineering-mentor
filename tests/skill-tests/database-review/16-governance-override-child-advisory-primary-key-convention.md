---
id: database-review-16-governance-override-child-advisory-primary-key-convention
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Legitimate Child Advisory Override of Mentor Advisory Guidance (Category 3 — Override)

## Input Material

> Context discovery reports Mentor Advisory guidance: "Prefer UUID primary keys over auto-incrementing integers for new tables where feasible, to avoid exposing sequential, enumerable identifiers." A declared Child Advisory rule (`classification: advisory`, `status: active`) states: "This project's schema uses auto-incrementing bigint primary keys for every existing table, and all internal tooling (bulk-import scripts, admin dashboards, foreign-key relationships) assumes sequential integer IDs — new tables use bigint auto-increment primary keys for consistency with the rest of the schema." The migration under review creates a new table with a bigint auto-increment primary key, consistent with the child's stated convention. Nothing in the material suggests the new table's IDs are exposed in a context where enumerability itself is a security concern (e.g. no public-facing URL directly exposes the raw ID with no authorization check).

## Pass Criteria

- Recognizes this as a legitimate Override (`docs/Governance Precedence Model.md` Section 8, Section 10 category 3): the Child Advisory convention replaces Mentor's generic Advisory preference on primary-key style, requiring no exception.
- Does not report a finding recommending UUIDs instead — the superseded Mentor Advisory guidance is not reported as a separate, competing finding.
- Still evaluates the table for genuine data-integrity concerns (constraints, indexes, nullability) independent of the primary-key style question — Override applies narrowly to the PK-style preference, not to the rest of the review.

## Fail Signals

- Flagging the bigint auto-increment key as a finding or "inconsistency" with generic best practice, ignoring the project's own stated, legitimate convention.
- Manufacturing a governance conflict or requiring an exception for a legitimate Advisory-level Override.
