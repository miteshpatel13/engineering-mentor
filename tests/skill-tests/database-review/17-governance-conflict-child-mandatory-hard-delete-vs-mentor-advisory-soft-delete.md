---
id: database-review-17-governance-conflict-child-mandatory-hard-delete-vs-mentor-advisory-soft-delete
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Genuine Conflict Between Child Mandatory Convention and Mentor Advisory Guidance (Category 4 — Conflict)

## Input Material

> Context discovery reports Mentor Advisory guidance: "Prefer soft deletes (a `deletedAt` timestamp column) over hard deletes for user-facing records, to preserve recoverability and support later audit or restoration." A declared Child Mandatory rule (`classification: mandatory` in its own frontmatter, `status: active` — mandatory for this child project, not a Mentor Mandatory or security/safety-classified requirement) states: "All personal-data records in this schema must be hard-deleted on user request, with no `deletedAt`/soft-delete column anywhere in the schema — this project's data-retention policy requires that a deletion request physically removes the row, and a soft-delete column would leave the data recoverable, which the policy prohibits." The migration under review performs a hard delete on a user-facing table with no soft-delete column, consistent with the child rule.

## Pass Criteria

- Recognizes this is genuinely a Conflict (`docs/Governance Precedence Model.md` Section 10 category 4), not an Override: the child rule is Child Mandatory, a different tier than the Child-Advisory-replaces-Mentor-Advisory Override case, and it disagrees with Mentor's Advisory soft-delete preference rather than merely narrowing it.
- States both sides explicitly rather than silently picking one: Mentor Advisory prefers soft deletes; the Child Mandatory rule requires hard deletes; the two disagree. Per Section 11, the conflict is surfaced, not silently resolved by omission.
- Recognizes that Child Mandatory outranks Mentor Advisory in the precedence order (`docs/Governance Precedence Model.md` Section 4), so the hard-delete approach is what the project actually follows here — but reports this as the outcome of a surfaced conflict, not as if Mentor's guidance never existed.
- Does not treat this as a Prohibited Override — the superseded Mentor requirement here is Advisory, not Mandatory/security/data-integrity-classified in the Mentor-Mandatory sense, so Section 9's prohibited-override treatment does not apply. (Contrast with fixture 05, where the exception targets an actual Mentor Mandatory data-integrity requirement.)

## Fail Signals

- Reporting a finding that the table "should" use soft deletes, phrased as a defect, with no acknowledgment that the child's Mandatory data-retention rule legitimately governs here.
- Silently applying the child's hard-delete convention with no surfaced conflict at all, as if this were an ordinary Override (fixture 16) rather than a genuine, stated disagreement.
- Misclassifying the child rule as a Prohibited Override or as illegitimate — disagreeing with a Mentor *Advisory* point is not the same as attempting to override a Mentor *Mandatory* one.
