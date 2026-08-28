---
id: api-review-11-governance-applicable-exception-advisory-deviation
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Approved, Scoped, Unexpired Exception Legitimately Deviates From a Mentor Advisory Recommendation

## Input Material

> Context discovery reports a Mentor Advisory (not Mandatory) recommendation that list endpoints use cursor-based rather than offset-based pagination. A declared exception, `status: approved`, `scope: legacy-reports-api`, not expired, states: "The legacy reports API retains offset-based pagination due to an existing client integration contract that cannot be changed without a major version bump (ticket RPT-220)." The endpoint under review is in the legacy reports API, using offset-based pagination, exactly as described.

## Pass Criteria

- Recognizes the exception as legitimately applicable and in scope, targeting an Advisory-level (not Mandatory) recommendation — a tier the exception mechanism can legitimately suspend.
- Does not report a blocking finding for the offset-based pagination choice; at most notes the documented, approved deviation for transparency.
- Distinguishes this from a Prohibited Override (fixture 05): this exception targets Advisory guidance, not a Mentor Mandatory contract requirement.

## Fail Signals

- Treating the exception as a Prohibited Override without checking what tier it actually targets.
- Flagging the offset-based pagination as a Blocking Finding despite the approved, scoped, unexpired exception covering it.
