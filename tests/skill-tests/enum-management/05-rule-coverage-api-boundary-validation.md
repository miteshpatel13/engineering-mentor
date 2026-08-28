---
id: enum-management-05-rule-coverage-api-boundary-validation
category: rule-coverage
skill_under_test: skills/enum-management/SKILL.md
---

# Scenario: Business Logic Comparing Against String Names

## Input Material

> In a service class, a developer writes:
> `if (order.status === 'COMPLETED') { triggerFulfillment(); }`
> The `order.status` database column stores integer `4`.

## Pass Criteria

- Rejects string literal comparisons against integer-backed enum fields.
- Mandates comparison using typed enum constants: `order.status === OrderStatus.COMPLETED`.

## Fail Signals

- Approving magic string or magic number comparisons in business logic.
