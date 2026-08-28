---
id: notification-integration-01-normal-provider-adapter-isolation
category: normal
skill_under_test: skills/notification-integration/SKILL.md
---

# Scenario: Isolating Messaging Providers Behind Adapter Interfaces

## Input Material

> Design a notification system that supports SMS, Email, and Push notifications. A developer proposes calling specific provider SDKs (`SendGridMailService`, `TwilioSmsClient`) directly from business service methods.

## Pass Criteria

- Rejects direct calls to provider SDKs inside domain services.
- Mandates encapsulating provider SDKs behind generic `NotificationAdapter` interfaces (`EmailAdapter`, `SMSAdapter`, `PushAdapter`).
- Confirms that swapping an SMS or Email vendor requires changes only within its specific adapter class.

## Fail Signals

- Coupling business services or controllers directly to vendor-specific messaging SDKs.
