---
id: third-party-integration-02-edge-rate-limiting-and-exponential-backoff
category: edge
skill_under_test: skills/third-party-integration/SKILL.md
---

# Scenario: Handling HTTP 429 Rate Limiting with Full Jitter and Retry-After

## Input Material

> An integration synchronizes 10,000 inventory items with an external supplier ERP API every hour. During peak sync, the supplier returns `HTTP 429 Too Many Requests` with header `Retry-After: 12`. Propose the rate-limiting and retry architecture.

## Pass Criteria

- **Client-Side Throttling**: Implements a client-side rate limiter (token bucket or leaky bucket) configured to the supplier's published throughput limits to prevent triggering 429 errors proactively.
- **Retry-After Header Handling**: Parses the `Retry-After` header (handling both integer seconds and HTTP-date formats) and pauses subsequent outbound dispatches.
- **Exponential Backoff with Full Jitter**: Applies random jitter to wait durations to avoid thundering-herd synchronization when multiple workers resume.
- **Classification**: Classifies HTTP 429 as a retryable transient error, capped by maximum retry attempts (e.g., 3–5 retries) before routing to a dead-letter queue.

## Fail Signals

- Immediately retrying failed 429 requests in a tight loop without delay or backoff.
- Using deterministic exponential backoff without jitter, causing synchronized burst collisions.
- Treating HTTP 429 as a permanent non-retryable error and abandoning the entire sync batch.
- Ignoring the supplier's `Retry-After` header.
