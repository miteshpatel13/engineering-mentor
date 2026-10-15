---
id: data-access-reliability-01-normal-scheduled-job-pool-self-deadlock
category: normal
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: Daily Messaging Job Freezes Every Endpoint on Every Instance

## Input Material

> A daily scheduled job, run in-process by every application instance, loads all subscribed (user × company) pairs and, for each pair, calls `executeTask(pair)` without awaiting it. `executeTask` creates a manual query runner, reads the pair's settings through it, then calls `checkCondition()`, which creates a *second* query runner to run a condition query, then sends a message through an HTTP API client that has no timeout, and finally releases the first runner in `finally`. The connection pool has 30 connections. Production shows, once a day at the job's scheduled time, 50–110 requests across 20–36 unrelated endpoints stalling 30 seconds to 8 minutes on all instances simultaneously.

## Pass Criteria

- Identifies hold-and-wait pool self-deadlock: each task holds one connection while needing a second from the same pool, so with more concurrent tasks than pool connections every connection is held by a waiter (Rules → Hold-and-Wait).
- Identifies the unbounded un-awaited fan-out as the reason the task count exceeds the pool (Rules → Bounded Concurrency) and the external call without a timeout made while holding a connection.
- Connects the symptom shape (clustered stalls across unrelated endpoints, all instances, fixed time) to this cause using the Diagnostic signatures, and notes the job runs once per instance (Rules → Once-Per-Period Execution).
- Recommends: awaited work with a small concurrency bound; per-query connection borrowing instead of manual runners; no connection held across the HTTP call; a timeout on the client; a once-per-period guard.

## Fail Signals

- Recommending a larger pool or an index as the fix.
- Treating the stalls as slow queries on the endpoints that stalled.
- Missing the second-connection dependency and blaming only the external call.
