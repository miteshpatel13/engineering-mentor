---
id: payment-integration-03-adversarial-cumulative-over-refunding
category: adversarial
skill_under_test: skills/payment-integration/SKILL.md
---

# Scenario: Preventing Over-Refunding Beyond Transaction Total

## Input Material

> An admin attempts to process a refund of $60.00 for transaction `TXN_100` (original amount: $100.00). A previous partial refund of $50.00 was already completed for `TXN_100`.

## Pass Criteria

- Calculates remaining net balance: `$100.00 - $50.00 = $50.00`.
- Rejects the proposed $60.00 refund request as exceeding the remaining net balance.
- Models refunds as child records of the parent transaction to maintain cumulative refund audit trails.

## Fail Signals

- Approving a refund that causes cumulative refunds to exceed the original transaction amount.
- Failing to sum prior non-failed refunds when evaluating refund limits.
