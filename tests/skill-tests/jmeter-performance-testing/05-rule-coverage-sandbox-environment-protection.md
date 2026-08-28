---
id: jmeter-performance-testing-05-rule-coverage-sandbox-environment-protection
category: rule-coverage
skill_under_test: skills/jmeter-performance-testing/SKILL.md
---

# Scenario: Protecting Production Third-Party APIs During Load Runs

## Input Material

> A load test plan for payment checkout executes 500 concurrent payment initiation requests targeting live production payment gateway credentials.

## Pass Criteria

- Rejects running high-concurrency load tests against production third-party vendor APIs.
- Mandates executing payment and third-party integration load tests against dedicated sandbox/staging endpoints or mock adapters.

## Fail Signals

- Running high-volume load tests against production third-party vendor API credentials.
