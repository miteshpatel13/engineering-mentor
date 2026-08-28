---
id: performance-review-01-normal-profiling-trace-external-call
category: normal
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Diagnosing a Bottleneck From a Real Profiling Trace

## Input Material

> The checkout endpoint has a target of p95 < 500ms, currently measuring p95 = 2100ms. A profiling trace shows 80% of the request time spent in a single synchronous call to an external payment gateway; the rest of the request (validation, database writes) totals under 200ms.

## Pass Criteria

- Diagnoses the bottleneck as the synchronous external payment-gateway call, grounded in the stated profiling evidence.
- Does not propose optimizing the database writes or validation logic as the primary fix — that isn't where the evidence points.
- States a concrete verification step: re-measure p95 after the fix against the 500ms target.

## Fail Signals

- Guessing at a database or validation-layer bottleneck not supported by the profiling evidence.
- Proposing a fix with no stated verification/re-measurement step.
