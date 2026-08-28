---
id: architecture-review-01-normal-shared-write-ownership
category: normal
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Two Services Write the Same Table

## Input Material

> A design document proposes an `OrderService` and a `FulfillmentService`, both writing directly to a shared `orders` table — `OrderService` updates order status on placement and cancellation, `FulfillmentService` updates the same status field when a shipment completes. No reconciliation or single-writer mechanism is described.

## Pass Criteria

- Identifies this as a Cohesion/Data Ownership finding: two independent write paths to the same field with no reconciliation mechanism.
- States the severity and the concrete risk (lost updates / inconsistent state under concurrent writes).
- Recommends a concrete fix: a single owning service with the other consuming via API/event, or an explicit reconciliation mechanism.

## Fail Signals

- Treating this as acceptable because each service's individual write logic is otherwise correct.
- Recommending a fix without naming the actual risk (lost updates / race).
