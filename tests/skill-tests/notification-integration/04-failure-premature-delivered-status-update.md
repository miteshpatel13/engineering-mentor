---
category: failure
id: notification-integration-04-failure-premature-delivered-status-update
skill_under_test: skills/notification-integration/SKILL.md
---

# Scenario: Prematurely Updating Recipient Status to Delivered

## Input Material

> A dispatch worker calls `emailAdapter.send()`. When the provider API returns HTTP 200 `{"status": "accepted"}`, the worker updates the recipient record status to `DELIVERED`.

## Pass Criteria

- Flags marking status as `DELIVERED` from initial API call acceptance as a defect.
- Mandates updating status to `SENT` upon initial API call success, reserving `DELIVERED` or `READ` for asynchronous provider webhook receipts.

## Fail Signals

- Equating provider HTTP API acceptance with recipient device delivery.
