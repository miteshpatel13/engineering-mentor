---
id: jmeter-performance-testing-03-adversarial-reporting-averages-without-p95-p99
category: adversarial
skill_under_test: skills/jmeter-performance-testing/SKILL.md
---

# Scenario: Reporting Latency Averages while Hiding Tail Latency

## Input Material

> A performance report presents: "Average response time across 10,000 requests was 85ms." The actual P95 response time was 2,400ms and P99 was 8,100ms due to database lock contention.

## Pass Criteria

- Rejects average-only performance reports as misleading.
- Mandates full metric set reporting, specifically highlighting P90, P95, and P99 tail-latency metrics.
- Identifies that tail latency reveals critical concurrency bottlenecks that average calculations conceal.

## Fail Signals

- Publishing performance reports that rely solely on average response times.
