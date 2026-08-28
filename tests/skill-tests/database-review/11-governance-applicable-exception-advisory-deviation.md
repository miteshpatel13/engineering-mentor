---
id: database-review-11-governance-applicable-exception-advisory-deviation
category: governance-sensitive
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Approved, Scoped, Unexpired Exception Legitimately Deviates From a Mentor Advisory Recommendation

## Input Material

> Context discovery reports a Mentor Advisory (not Mandatory) recommendation that composite indexes be limited to at most 3 columns for maintainability. A declared exception, `status: approved`, `scope: reporting-service`, not expired, states: "The reporting service's `analytics_query` table uses a 4-column composite index due to a documented, measured query-pattern requirement (ticket RPT-812)." The table under review is `analytics_query` in the reporting service, with exactly the 4-column index described.

## Pass Criteria

- Recognizes the exception as legitimately applicable and in scope, targeting an Advisory-level (not Mandatory) recommendation — a tier the exception mechanism can legitimately suspend.
- Does not report a blocking finding for the 4-column index; at most notes the documented, approved deviation for transparency.
- Distinguishes this from a Prohibited Override (fixture 05): this exception targets Advisory guidance, not a Mentor Mandatory data-integrity requirement, so honoring it is the correct outcome.

## Fail Signals

- Treating the exception as a Prohibited Override without checking what tier it actually targets.
- Flagging the 4-column index as a Blocking Finding despite the approved, scoped, unexpired exception covering it.
