---
id: performance-review-02-edge-premature-optimization-no-measurement
category: edge
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Optimization Proposed With No Measured Problem

## Input Material

> A developer proposes adding a caching layer in front of a `GET /products` endpoint "because it's probably going to be slow at scale." No measurement, load test, or current latency figure is provided.

## Pass Criteria

- Flags this directly as premature optimization — Rules → Measurable Targets applies before an optimization is evaluated.
- States that a measurable baseline (current latency, expected load) is needed before the optimization can be assessed as necessary or evaluated for relevance.
- Does not simply approve the caching layer as a reasonable-sounding improvement.

## Fail Signals

- Approving or recommending the caching layer without first requiring a measured baseline.
- Treating "probably slow at scale" as sufficient evidence of an actual problem.
