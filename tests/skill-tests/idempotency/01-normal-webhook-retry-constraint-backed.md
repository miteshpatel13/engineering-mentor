---
id: idempotency-01-normal-webhook-retry-constraint-backed
category: normal
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Designing a Webhook Handler That May Be Redelivered

## Input Material

> Design an inbound payment-provider webhook handler. The provider's own documentation states it may redeliver the same event (same `event_id`) if it doesn't receive a `200` acknowledgment in time. The handler currently has no deduplication of any kind — it processes every inbound call as a brand-new event and triggers a downstream "mark invoice paid" side effect each time.

## Pass Criteria

- Identifies `event_id` as the correct request identity (Rules → Request Identity) — a provider-supplied reference, not a freshly generated value.
- Recommends constraint-backed enforcement (Rules → Constraint-Backed Enforcement) — a uniqueness constraint on a processed-events table or equivalent atomic mechanism — not a plain "check if seen, then process" sequence.
- Recommends silent no-op replay behavior (Rules → Replay Behavior) — redelivery is expected provider behavior and carries no new information for the caller, so a redelivered event should return success without re-triggering the "mark invoice paid" side effect.
- States the enforcement and the side effect should be atomic with each other (Rules → Atomicity), not two separately-committed steps.

## Fail Signals

- Recommending a fresh server-generated identifier as the deduplication key instead of the provider's `event_id`.
- Recommending a "check then insert" sequence with no atomicity reasoning.
- Treating the redelivery as an anomaly to reject/error on, rather than the expected, designed-for case it is.
