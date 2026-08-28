---
id: idempotency-04-failure-material-doesnt-establish-retry-plausibility
category: failure-handling
skill_under_test: skills/idempotency/SKILL.md
---

# Scenario: Material Doesn't Establish Whether the Operation Is Retry-Prone

## Input Material

> "Here's an endpoint that creates a support ticket." No further detail is given about the client(s) that call it, whether any retry logic exists on the caller side, whether it's reachable via any webhook/callback path, or whether resubmission is a realistic scenario for this specific integration.

## Pass Criteria

- States explicitly that the material doesn't establish whether this operation is plausibly retry-prone or duplicate-prone (Failure Handling), rather than assuming either that it needs idempotency treatment or that it doesn't.
- Names specifically what additional information would resolve the ambiguity (e.g. is this called from a client with automatic retry logic, from a webhook, or purely interactively with no retry path).
- Does not fabricate a request-identity mechanism or a retention window for an operation whose retry-proneness itself hasn't been established.

## Fail Signals

- Assuming the operation needs full idempotency treatment (or doesn't) without flagging the missing information.
- Inventing specifics (a client library's retry behavior, a caller's integration pattern) the material doesn't state.
