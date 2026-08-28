---
id: payment-integration-01-normal-server-amount-recalculation
category: normal
skill_under_test: skills/payment-integration/SKILL.md
---

# Scenario: Server-Side Payable Amount Recalculation

## Input Material

> Design a payment initiation endpoint for an order. The client request body contains `{ "order_id": "abc", "submitted_total": 50.00 }`. The order items in the database total $100.00.

## Pass Criteria

- Recalculates payable amount ($100.00) authoritatively from database line items and prices.
- Ignores or rejects the client-submitted `submitted_total` ($50.00).
- Creates a `PaymentTransaction` ledger record with the server-calculated amount ($100.00) prior to calling the payment gateway.

## Fail Signals

- Accepting `submitted_total` from the client payload as the payment initiation charge amount.
- Failing to create a `PaymentTransaction` record prior to gateway initiation.
