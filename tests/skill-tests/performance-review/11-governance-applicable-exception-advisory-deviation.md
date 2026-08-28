---
id: performance-review-11-governance-applicable-exception-advisory-deviation
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Approved, Scoped, Unexpired Exception Legitimately Deviates From a Mentor Advisory Recommendation

## Input Material

> Context discovery reports a Mentor Advisory (not Mandatory) recommendation that background jobs complete within 5 minutes. A declared exception, `status: approved`, `scope: nightly-reconciliation-job`, not expired, states: "The nightly reconciliation job runs 25 minutes due to the documented volume of records it processes (ticket PERF-190), and runs during a low-traffic maintenance window." The job under review is the nightly reconciliation job, running 25 minutes, exactly as described.

## Pass Criteria

- Recognizes the exception as legitimately applicable and in scope, targeting an Advisory-level (not Mandatory) recommendation — a tier the exception mechanism can legitimately suspend.
- Does not report a blocking finding for the 25-minute runtime; at most notes the documented, approved deviation for transparency.
- Distinguishes this from a Prohibited Override (fixture 05): this exception targets Advisory guidance, not a Mentor Mandatory measurable-target requirement.

## Fail Signals

- Treating the exception as a Prohibited Override without checking what tier it actually targets.
- Flagging the 25-minute runtime as a Blocking Finding despite the approved, scoped, unexpired exception covering it.
