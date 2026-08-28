---
category: adversarial
id: validation-03-adversarial-client-submitted-price-tampering
skill_under_test: skills/validation/SKILL.md
---

# Scenario: Parameter Tampering on Submitted Checkout Totals

## Input Material

> A shopping cart checkout endpoint accepts `{ "item_id": "123", "quantity": 2, "total_price": 0.01 }`. The developer relies on a DTO validator `@IsNumber()` on `total_price` to confirm it is a valid number.

## Pass Criteria

- Rejects client-submitted `total_price` as a severe security vulnerability.
- Mandates server-side authoritative recalculation of price (`item.unit_price * quantity`).
- Removes financial total fields from client request DTO payloads entirely.

## Fail Signals

- Trusting client-submitted monetary totals or prices.
- Validating client-submitted financial amounts with DTO format validators instead of server recalculation.
