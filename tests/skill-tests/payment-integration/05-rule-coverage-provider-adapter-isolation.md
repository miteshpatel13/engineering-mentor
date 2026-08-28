---
id: payment-integration-05-rule-coverage-provider-adapter-isolation
category: rule-coverage
skill_under_test: skills/payment-integration/SKILL.md
---

# Scenario: Encapsulating Gateway SDK Logic Behind Adapter Interfaces

## Input Material

> An order controller directly imports a specific payment provider SDK (`import Stripe from 'stripe'`) and calls provider methods inside controller route handlers.

## Pass Criteria

- Rejects direct calls to third-party payment SDKs inside controllers or core business services.
- Mandates encapsulating provider SDK calls, payload formatting, and signature algorithms behind a generic `PaymentProvider` interface adapter.

## Fail Signals

- Directly coupling controllers or domain services to specific third-party payment vendor SDKs.
