---
id: implementation-plan-review-01-normal-plan-with-migration-and-price-gaps
category: normal
skill_under_test: skills/implementation-plan-review/SKILL.md
---

# Scenario: Plan with security, migration, and deployment gaps

## Input Material

> `specs/004-customer-pricing/plan.md` adds table `customer_prices(customer_id, sku, price)`; runs `ALTER TABLE orders ADD COLUMN price_source TEXT NOT NULL` on a 30M-row live table; lets the client submit `unit_price` on order creation "to support negotiated prices"; has no rollback or observability section. `spec.md` requires negotiated prices to apply at checkout.

## Pass Criteria

- HIGH (or CRITICAL) Security finding: client-supplied price must be recalculated server-side.
- HIGH Migration Safety finding: NOT NULL without default/backfill on existing rows.
- Findings or recommendations for the missing unique constraint on (customer_id, sku), the missing rollback plan, and the missing observability.
- Verdict: Revise before tasks; every finding uses only CRITICAL/HIGH/MEDIUM/LOW/INFO.

## Fail Signals

- Approving the plan.
- Using non-canonical severity labels.
- Editing plan.md.
