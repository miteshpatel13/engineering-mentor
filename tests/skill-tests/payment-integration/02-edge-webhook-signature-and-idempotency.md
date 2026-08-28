---
id: payment-integration-02-edge-webhook-signature-and-idempotency
category: edge
skill_under_test: skills/payment-integration/SKILL.md
---

# Scenario: Ingesting Duplicate Payment Webhooks

## Input Material

> A payment gateway sends an inbound HTTP POST webhook notifying success for transaction reference `TXN_999`. The database transaction `TXN_999` already has `status = SUCCESS` from a previous webhook delivery 5 seconds ago.

## Pass Criteria

- Verifies the cryptographic signature header on the webhook before processing.
- Performs an atomic idempotency check on `TXN_999` (`skills/idempotency/SKILL.md`).
- Returns HTTP 200/Success to the gateway to acknowledge receipt.
- Executes zero duplicate side effects (no second invoice, no duplicate fulfillment notification).

## Fail Signals

- Skipping signature verification on inbound webhooks.
- Re-running post-payment success logic (re-issuing invoices, sending duplicate confirmation emails) on a replayed webhook.
- Returning an HTTP 500 error to the gateway on duplicate delivery, causing endless gateway retries.
