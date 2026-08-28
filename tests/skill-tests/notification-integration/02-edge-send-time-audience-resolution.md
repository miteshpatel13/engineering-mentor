---
id: notification-integration-02-edge-send-time-audience-resolution
category: edge
skill_under_test: skills/notification-integration/SKILL.md
---

# Scenario: Send-Time Dynamic Audience Filter Resolution

## Input Material

> An admin creates a scheduled announcement broadcast targeting "Users with unpaid invoices." The broadcast is created on Monday and scheduled to dispatch on Friday. The developer resolves the recipient list on Monday during creation and saves static user IDs.

## Pass Criteria

- Flags pre-resolving recipient lists at creation time as a defect.
- Requires storing structured audience filter rules (`AudienceFilter`) and resolving recipient lists dynamically at send time on Friday.
- Explains that pre-resolving misses new eligible users and sends messages to users who paid between Monday and Friday.

## Fail Signals

- Storing static recipient lists at broadcast creation time for scheduled dispatches.
