---
id: validation-05-rule-coverage-server-authoritative-recalculation
category: rule-coverage
skill_under_test: skills/validation/SKILL.md
---

# Scenario: Recomputing Permissions and Discount Calculations Server-Side

## Input Material

> An upgrade endpoint accepts `{ "user_id": "abc", "discount_percentage": 50, "assigned_role": "ADMIN" }`.

## Pass Criteria

- Refuses to accept `discount_percentage` or `assigned_role` from client input payload.
- Enforces that permissions, roles, and applicable discounts are computed authoritatively on the server based on authenticated session context and database rules.

## Fail Signals

- Accepting client-asserted permissions or discount percentages in API request payloads.
