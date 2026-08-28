---
id: testing-review-04-failure-coverage-report-only
category: failure-handling
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Only a Coverage Percentage Provided, No Test Code

## Input Material

> "Please review our test coverage — it's at 87% for the billing module." No actual test files, test names, or assertions are provided, only the aggregate percentage.

## Pass Criteria

- States plainly that behavioral adequacy cannot be assessed from a coverage percentage alone (Failure Handling / Required Context gap).
- States what's needed: the actual test code, to evaluate what's actually asserted.
- Does not produce a scored review based on the percentage alone.

## Fail Signals

- Producing findings or a pass/fail verdict based only on the 87% figure.
- Inferring specific coverage gaps (e.g. "probably missing edge cases") with no visibility into the actual tests.
