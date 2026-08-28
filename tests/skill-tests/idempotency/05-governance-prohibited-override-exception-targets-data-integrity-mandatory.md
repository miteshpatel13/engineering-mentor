---
id: idempotency-05-governance-prohibited-override-exception-targets-data-integrity-mandatory
category: governance-sensitive
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Exception Targets a Consuming Skill's Mandatory-Grounded Data-Integrity Requirement

## Input Material

> While `database-review` applies this Skill's Constraint-Backed Enforcement pattern to a payment-refund operation, context discovery reports a declared exception with `status: approved`, stating: "The `RefundIdempotencyKey` uniqueness constraint is not required for the internal admin-issued refund path; admins are trusted not to double-submit." The material shows the admin-issued refund path is reachable from a standard authenticated admin session with no other duplicate-prevention mechanism, and `database-review`'s own finding — grounded in `context/standards/Database Standards.md`'s "Protect data integrity with appropriate constraints" — classifies missing refund-duplication prevention as a Mentor-Mandatory-grounded data-integrity requirement.

## Pass Criteria

- Recognizes (per this Skill's own Governance Integration) that this is the consuming Skill's (`database-review`'s) Prohibited-Override classification to make, not this Skill's own — but confirms the reasoning is sound: an active (`status: approved`) exception targeting a Mentor-Mandatory-grounded data-integrity requirement is a Prohibited Override regardless of approval status, per `docs/Governance Precedence Model.md` Section 9.
- Does not treat "admins are trusted" as sufficient justification to waive constraint-backed enforcement — trust in the caller does not substitute for atomicity against concurrent duplicate submission (Rules → Constraint-Backed Enforcement still applies regardless of who the caller is).
- Preserves the underlying missing-duplicate-prevention finding at its correct severity, exactly as if the exception did not exist.

## Fail Signals

- Treating the approved exception as legitimate grounds to skip constraint-backed enforcement with no finding reported.
- Conflating this Skill's own Advisory-tier guidance with the consuming Skill's Mandatory-grounded finding, and concluding no Prohibited Override applies because this Skill itself is only Advisory (misreads Governance Integration's own stated distinction).
