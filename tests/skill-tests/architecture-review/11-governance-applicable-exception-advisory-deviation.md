---
id: architecture-review-11-governance-applicable-exception-advisory-deviation
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Approved, Scoped, Unexpired Exception Legitimately Deviates From a Mentor Advisory Recommendation

## Input Material

> Context discovery reports a Mentor Advisory (not Mandatory) recommendation that new services avoid a shared database with other services. A declared exception, `status: approved`, `scope: reporting-service`, not expired, states: "The reporting service shares the primary database with the orders service, read-only, due to a documented near-term migration plan (ticket ARCH-77)." The design under review is the reporting service, sharing the orders database read-only, exactly as described.

## Pass Criteria

- Recognizes the exception as legitimately applicable and in scope, targeting an Advisory-level (not Mandatory) recommendation — a tier the exception mechanism can legitimately suspend.
- Does not report a blocking finding for the shared database; at most notes the documented, approved deviation for transparency.
- Distinguishes this from a Prohibited Override (fixture 05): this exception targets Advisory guidance, not a Mentor Mandatory isolation requirement.

## Fail Signals

- Treating the exception as a Prohibited Override without checking what tier it actually targets.
- Flagging the shared database as a Blocking Finding despite the approved, scoped, unexpired exception covering it.
