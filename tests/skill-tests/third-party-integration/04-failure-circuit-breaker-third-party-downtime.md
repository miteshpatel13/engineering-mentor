---
id: third-party-integration-04-failure-circuit-breaker-third-party-downtime
category: failure
skill_under_test: skills/third-party-integration/SKILL.md
---

# Scenario: Third-Party Downtime, Cascading Failures, and Circuit Breaker

## Input Material

> An external tax calculation service (TaxSaaS) experiences a major outage, returning HTTP 503 or timing out on every checkout request. Because the checkout endpoint calls TaxSaaS synchronously on every page load, application worker threads are becoming exhausted and the entire shopping application is crashing. Propose a resilient failure recovery architecture.

## Pass Criteria

- **Circuit Breaker Pattern**: Recommends wrapping the outbound TaxSaaS client in a circuit breaker that transitions from CLOSED to OPEN when error/timeout rates exceed a threshold (e.g., 50% over 20 requests), fast-failing subsequent calls without consuming threads.
- **Graceful Degradation**: Defines a fallback strategy (e.g., estimating tax based on cached rates or postal code tables, or flagging order for asynchronous tax recalculation before fulfillment) rather than hard-crashing checkout.
- **Explicit Aggressive Timeouts**: Restricts synchronous call timeouts (e.g., 2s connect, 3s read) so failing requests terminate rapidly before thread pools exhaust.
- **Decoupling**: Recommends moving non-blocking tax filing/reporting out of the synchronous checkout path into background queues.

## Fail Signals

- Continuing to issue synchronous network requests with long or default timeouts during an active vendor outage.
- Recommending infinite or unbounded retries on user-facing synchronous paths.
- Failing to provide a graceful degradation or fallback strategy for the business process.
