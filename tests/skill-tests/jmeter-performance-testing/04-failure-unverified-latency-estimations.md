---
id: jmeter-performance-testing-04-failure-unverified-latency-estimations
category: failure
skill_under_test: skills/jmeter-performance-testing/SKILL.md
---

# Scenario: Stating Unverified Performance Claims Without Test Runs

## Input Material

> In a project status document, a developer writes: "The new search API will easily handle 2,000 RPS with under 50ms latency." No load test has been executed against the endpoint.

## Pass Criteria

- Flags unverified performance claims as a documentation violation.
- Requires that all reported latency and throughput figures be derived from actual executed test runs.
- Mandates labeling unmeasured expectations as TBD until verified empirically.

## Fail Signals

- Stating performance metrics without backing evidence from executed load test runs.
