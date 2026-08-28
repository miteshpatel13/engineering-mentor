---
category: rule-coverage
id: notification-integration-05-rule-coverage-idempotent-delivery-webhooks
skill_under_test: skills/notification-integration/SKILL.md
---

# Scenario: Ingesting Duplicate Delivery Status Webhooks

## Input Material

> An inbound delivery webhook from a WhatsApp provider notifies `DELIVERED` for message `MSG_777`. The recipient record for `MSG_777` already has `status = DELIVERED` from a duplicate webhook received 2 seconds earlier.

## Pass Criteria

- Processes the duplicate delivery status webhook idempotently (`skills/idempotency/SKILL.md`).
- Acknowledges the webhook with success without re-triggering status counters or secondary actions.

## Fail Signals

- Failing to handle duplicate webhook status notifications idempotently.
