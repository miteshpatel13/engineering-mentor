---
id: jmeter-performance-testing-01-normal-workflow-based-test-plan
category: normal
skill_under_test: skills/jmeter-performance-testing/SKILL.md
---

# Scenario: Designing a Multi-Step Workflow Load Test

## Input Material

> Design a performance test plan for an e-commerce checkout platform. The developer proposes hitting `GET /products/123` with 500 concurrent threads to measure application capacity.

## Pass Criteria

- Rejects single-endpoint bombardment as unrepresentative of actual production usage.
- Mandates multi-step workflow scenario design (Login $\rightarrow$ Search $\rightarrow$ Add to Cart $\rightarrow$ Checkout $\rightarrow$ Order Confirmation).
- Parameterizes virtual user data via CSV datasets to avoid cache-friendly duplicate requests.

## Fail Signals

- Testing isolated single endpoints and claiming the results represent full application capacity.
