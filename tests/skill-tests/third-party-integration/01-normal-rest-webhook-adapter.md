---
id: third-party-integration-01-normal-rest-webhook-adapter
category: normal
skill_under_test: skills/third-party-integration/SKILL.md
---

# Scenario: Normal Asynchronous Webhook Ingestion & Adapter Isolation

## Input Material

> Design an integration with an external shipping provider (e.g. ShipFast). The provider sends `shipment.delivered` webhooks when parcels are delivered, and exposes a REST API to generate return shipping labels. The system needs to update internal order statuses and notify customers.

## Pass Criteria

- **Adapter / ACL Isolation**: Defines a generic `ShippingProviderPort` interface used by core domain services, with a concrete `ShipFastAdapter` encapsulating all vendor-specific HTTP calls, DTOs, and serialization.
- **Asynchronous Webhook Ingestion**: Webhook handler immediately verifies the HMAC signature, checks idempotency via database unique constraint on `(provider, event_id)`, acknowledges with HTTP 200/202, and enqueues a background job for domain processing.
- **Explicit Timeouts & Error Mapping**: Outbound label creation client configures explicit connect (<= 5s) and read (<= 30s) timeouts, and maps HTTP errors into typed domain exceptions.
- **Zero Hardcoding**: Credentials (API key, webhook secret) are injected via environment variables or secrets manager, never hardcoded.

## Fail Signals

- Executing shipment status updates and customer notification logic synchronously within the webhook HTTP request thread.
- Importing ShipFast SDK or HTTP client directly inside internal order services or domain controllers.
- Omitting webhook signature verification or processing duplicate webhook IDs without unique constraint checks.
- Omitting explicit HTTP connection and read timeouts.
