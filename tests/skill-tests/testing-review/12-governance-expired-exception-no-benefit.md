---
id: testing-review-12-governance-expired-exception-no-benefit
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Expired Exception Provides No Protection From a Mentor Mandatory Finding

## Input Material

> Context discovery reports a Mentor Mandatory requirement that payment-handling code have failure-path test coverage. A declared exception, `status: approved`, `expiresAt: 2026-02-10` (a date the material states is in the past relative to this review), states: "The refunds module is exempt from failure-path coverage pending a planned rewrite." The module under review still has no failure-path tests, consistent with what the now-expired exception described.

## Pass Criteria

- Recognizes the exception's expiration and treats it as providing no current benefit.
- Reports the missing-failure-path-coverage finding at its correct severity, exactly as if no exception existed.
- States explicitly that a matching exception was found but is expired, rather than silently omitting mention of it or silently treating it as still active.

## Fail Signals

- Treating the expired exception as still active and omitting or softening the finding.
- Silently ignoring the exception's existence rather than stating it is expired and therefore inapplicable.
