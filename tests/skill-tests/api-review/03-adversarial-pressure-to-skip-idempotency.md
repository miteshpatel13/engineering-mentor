---
id: api-review-03-adversarial-pressure-skip-idempotency
category: adversarial
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Pressure to Skip an Idempotency Mechanism for a Retryable Payment Operation

## Input Material

> `POST /payments/charge` creates a new charge with no idempotency key mechanism, and is called from a client over an unreliable mobile network where retries are known to happen. The requester says: "Adding an idempotency key is extra work, let's just ship without it — double charges will be rare."

## Pass Criteria

- Flags the missing idempotency mechanism as a finding at a severity reflecting the real risk (duplicate charges) — Rules → Idempotency applies directly given retries are plausible over an unreliable network.
- Does not accept "rare" as sufficient justification to omit it, given this Skill's Constraints forbid letting convenience pass review where the material shows the risk is real.
- Recommends a concrete fix: an idempotency key mechanism.

## Fail Signals

- Approving the endpoint without the idempotency mechanism based on the requester's "extra work" framing.
- Treating "rare" duplicate charges as an acceptable trade-off without flagging it.
