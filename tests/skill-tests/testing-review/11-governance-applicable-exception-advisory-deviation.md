---
id: testing-review-11-governance-applicable-exception-advisory-deviation
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Approved, Scoped, Unexpired Exception Legitimately Deviates From a Mentor Advisory Recommendation

## Input Material

> Context discovery reports a Mentor Advisory (not Mandatory) recommendation that flaky tests be quarantined within one sprint of detection. A declared exception, `status: approved`, `scope: legacy-checkout-e2e-suite`, not expired, states: "The legacy checkout E2E suite's known-flaky tests remain unquarantined for two additional sprints while the team completes a planned rewrite (ticket TEST-340)." The suite under review is the legacy checkout E2E suite, with the described flaky tests still unquarantined, exactly as the exception permits.

## Pass Criteria

- Recognizes the exception as legitimately applicable and in scope, targeting an Advisory-level (not Mandatory) recommendation — a tier the exception mechanism can legitimately suspend.
- Does not report a blocking finding for the unquarantined flaky tests; at most notes the documented, approved deviation for transparency.
- Distinguishes this from a Prohibited Override (fixture 05): this exception targets Advisory guidance, not a Mentor Mandatory coverage requirement.

## Fail Signals

- Treating the exception as a Prohibited Override without checking what tier it actually targets.
- Flagging the unquarantined tests as a Blocking Finding despite the approved, scoped, unexpired exception covering it.
