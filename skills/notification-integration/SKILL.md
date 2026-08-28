---
name: notification-integration
description: The general engineering pattern for provider-agnostic notification architecture — channel adapter isolation (Email, SMS, WhatsApp, Push), audience targeting resolution, delivery status tracking, template management, and opt-out preferences. Reference material consumed by architecture-review and security-review.
category: Domain Patterns
skillType: Domain Pattern
---

# Notification Integration

## Purpose

Produce the shared, reusable reference pattern for notification and messaging architectures across multi-channel systems (Email, SMS, WhatsApp, Push Notifications). This exists as its own Skill because notification integration requires strict provider adapter isolation (`architecture-review`), asynchronous queued dispatch, dynamic audience resolution, template pre-approval management, user preference/opt-out compliance (`security-review`), and multi-state delivery tracking.

## Scope

**In scope:** channel adapter interface isolation, provider-agnostic messaging services, structured audience targeting resolution, notification template management (merge variables and regulatory approvals), asynchronous scheduled dispatch, user communication preference handling (opt-in vs opt-out), and multi-stage delivery status tracking (`QUEUED`, `SENT`, `DELIVERED`, `FAILED`, `READ`).

**Out of scope:** provider-specific account configuration or API key management; client UI notification rendering. This Skill teaches the notification architecture pattern.

## When to Use

Use when:
- Designing a multi-channel notification or broadcast messaging subsystem.
- Integrating a new messaging provider (SendGrid, Twilio, AWS SNS, Firebase Cloud Messaging).
- Implementing asynchronous notification dispatch or scheduled batch messaging.
- Managing user communication preferences (opt-outs, quiet hours, channel preferences).
- Building notification delivery tracking and webhook status update handlers.

Do not use for synchronous real-time RPC APIs where messaging delivery tracking is not involved.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The core rules (adapter isolation, send-time audience resolution, explicit delivery status progression, user opt-out compliance) apply across messaging providers and backend stacks.

## Workflow

1. **Define Unified Notification Adapter Interface:** Establish a generic interface (e.g. `NotificationAdapter`) exposing unified dispatch methods (`send(recipient, template, parameters)`).
2. **Implement Isolated Channel Adapters:** Wrap provider-specific SDKs, API requests, and authentication within dedicated adapters (`EmailAdapter`, `SMSAdapter`, `PushAdapter`).
3. **Manage Notification Templates:** Maintain centralized templates with parameter merge fields, recording regulatory or provider approval identifiers (e.g. SMS DLT IDs, WhatsApp template names).
4. **Resolve Audience at Send Time:** Evaluate dynamic audience filters (e.g. target segments, location, activity) against current database records at the exact moment of dispatch.
5. **Check User Communication Preferences:** Enforce user channel opt-outs for promotional/informational broadcasts; bypass preferences only for mandatory transactional/security alerts (e.g. OTP, password reset).
6. **Track Delivery Status Asynchronously:** Record distinct recipient ledger entries with progressive statuses (`QUEUED` -> `SENT` -> `DELIVERED` -> `READ` / `FAILED`). Update statuses via provider webhooks.

## Rules

### Provider Adapter Isolation

Application business logic must never instantiate or invoke third-party messaging SDKs directly. All notification dispatching must pass through a generic `NotificationService` depending on channel-agnostic `NotificationAdapter` interfaces. Swapping an SMS gateway, Email provider, or Push service must require modifications only within the specific adapter class.

### Send-Time Dynamic Audience Resolution

Broadcast audience targeting criteria (e.g. `active_subscribers`, `unpaid_invoices`, `city`) must be stored as structured JSON filter rules and resolved to individual recipient ledger entries (`NotificationRecipient`) at dispatch time. Resolving audience lists at creation time creates stale lists that miss newly eligible users or send messages to users who became ineligible.

### Delivery Status Progression and Webhook Handling

Do not mark a notification status as `DELIVERED` based solely on a successful API response from the provider call.
- **Provider API Response Success:** Indicates the message was accepted for delivery (Status: `SENT`).
- **Provider Webhook Receipt:** Indicates actual delivery to the recipient's device/inbox (Status: `DELIVERED` or `READ`).

Delivery webhooks must update recipient status idempotently (`skills/idempotency/SKILL.md`) to handle out-of-order or duplicate webhook delivery notifications safely.

### User Communication Preferences and Opt-Outs

The system must check and honor user communication preferences prior to dispatching non-transactional messages:
- **Promotional / Marketing Messages:** Require explicit user opt-in or honor channel opt-outs.
- **Transactional / Security Alerts:** (e.g., OTP logins, password resets, payment receipts) Are mandatory system operational messages that bypass marketing opt-out preferences.

### Template Approval and Parameter Sanitization

Notification templates must decouple message content from code:
- Support parameter merge fields (e.g. `{{user_name}}`, `{{event_title}}`).
- Enforce sanitization of dynamic HTML/text parameters to prevent injection attacks (`skills/security-review/SKILL.md`).
- Track regulatory or gateway template approval metadata (e.g., registered SMS DLT IDs or WhatsApp Business template identifiers). Block dispatching via unapproved templates.

### Asynchronous Queueing for Batch Dispatches

Large-scale broadcast notifications must be offloaded to background job queues or asynchronous worker pools. Never attempt synchronous fan-out of thousands of notifications within an interactive HTTP API request.

## Constraints

- Never call third-party messaging SDKs directly inside controllers or core business services.
- Do not mark notification recipient status as `DELIVERED` immediately upon provider API request acceptance.
- Never bypass user opt-out preferences for marketing or non-essential messages.

## Governance Integration

This Skill supplies reference material (Domain Pattern) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent strongly recommended Advisory-tier standards for system architecture and security grounded in `context/standards/Architecture Standards.md` and `context/standards/Security Standards.md`.
- **Child Rules:** Projects may define specific messaging providers, default channels, or locale templates in `.mentor/rules/`.

## Validation

This Skill is validated during design and review when:
- Provider SDKs are encapsulated within adapter classes implementing a common interface.
- Audience targeting resolves at send-time rather than creation time.
- Delivery tracking distinguishes between provider acceptance (`SENT`) and device receipt (`DELIVERED`).
- Marketing dispatches verify user channel preferences.

## Edge Cases

- **Rate Limiting and Provider Throttling:** Adapters must handle provider HTTP 429 rate-limit responses by pushing failed dispatches back to worker queues with exponential backoff.
- **Fallback Channels:** If a primary notification channel fails (e.g. SMS delivery failure), the notification service may automatically fallback to a secondary channel (e.g. Email) if configured.

## Failure Handling

When notification delivery status or template approval states cannot be verified from available code, report Insufficient Evidence regarding message delivery, per the Mentor Operating Model No Invention Rule.

## Expected Output

Reference material. Consuming Review Skills (`architecture-review`, `security-review`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Adapter Abstraction and Asynchronous Delivery
```typescript
// Generic interface for all notification adapters
export interface NotificationAdapter {
  send(recipient: string, templateId: string, params: Record<string, any>): Promise<{ providerRef: string }>;
}

// Service using adapter interface for dispatch
export class NotificationService {
  constructor(private readonly adapters: Map<Channel, NotificationAdapter>) {}

  async dispatchNotification(channel: Channel, recipient: User, template: Template, params: any) {
    if (!template.isApproved) {
      throw new Error('Cannot send via unapproved template');
    }

    if (template.category !== 'TRANSACTIONAL' && recipient.hasOptedOut(channel)) {
      return; // Honor user preference
    }

    const adapter = this.adapters.get(channel);
    const { providerRef } = await adapter.send(recipient.contact, template.id, params);

    await this.logRecipientStatus(recipient.id, providerRef, DeliveryStatus.SENT);
  }
}
```

### Negative Example: Direct SDK Coupling and Immediate Delivered Status
```typescript
// BAD: Direct coupling to Twilio SDK inside controller route
import { Twilio } from 'twilio';

app.post('/send-sms', async (req, res) => {
  const client = new Twilio(accountSid, authToken);
  await client.messages.create({ body: req.body.text, to: req.body.to });
  
  // DEFECT: Marking DELIVERED immediately based on API call acceptance!
  await updateStatus(req.body.to, 'DELIVERED');
  res.send({ success: true });
});
```

## Related Skills

- `skills/architecture-review/SKILL.md` — Related: Reviews overall subsystem decoupling, adapter interfaces, and asynchronous job queuing.
- `skills/security-review/SKILL.md` — Related: Evaluates template content sanitization, credentials management, and privacy preference compliance.
- `skills/idempotency/SKILL.md` — Related: Provides atomic deduplication patterns for provider delivery webhooks.
- `skills/enum-management/SKILL.md` — Related: Governs standard channel and status enum definitions.
