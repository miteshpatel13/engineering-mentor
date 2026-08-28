---
category: failure
id: payment-integration-04-failure-optimistic-refund-completion
skill_under_test: skills/payment-integration/SKILL.md
---

# Scenario: Prematurely Updating Refund Status to Completed

## Input Material

> A service method initiates a refund request to a payment gateway and immediately updates the local `Refund` record to `status = COMPLETED` before receiving the HTTP response from the gateway API call.

## Pass Criteria

- Flags premature `COMPLETED` status update as a defect.
- Requires explicit refund lifecycle state tracking (`INITIATED` -> `PROCESSING` -> `COMPLETED`/`FAILED`).
- Updates status to `COMPLETED` only after receiving verified confirmation from the gateway API response or webhook.

## Fail Signals

- Optimistically marking refund status as `COMPLETED` prior to gateway API confirmation.
