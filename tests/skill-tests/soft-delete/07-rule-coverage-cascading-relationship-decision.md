---
id: soft-delete-07-rule-coverage-cascading-relationship-decision
category: rule-coverage
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Deciding Cascade Behavior for Two Different Child Relationships

## Input Material

> A `subscription` is soft-deleted. It has two child relationships: `invoice` records (each representing a completed, already-charged billing event) and `pendingChange` records (each representing a not-yet-applied plan-change request that only has meaning while the subscription is active). Someone asks whether deleting the subscription should cascade to each.

## Pass Criteria

- Recommends `invoice` records remain visible on their own terms, not cascade-deleted (Rules → Cascading and Relationship Considerations) — they're independent historical facts (a customer's billing history) that shouldn't vanish because the subscription was later deleted.
- Recommends `pendingChange` records be explicitly cascade-deleted (or otherwise explicitly resolved) — they have no meaning without an active subscription.
- States the two decisions separately with distinct reasoning, rather than applying one blanket cascade rule to both relationships.

## Fail Signals

- Applying the same cascade behavior to both relationships without distinguishing why they differ.
- Cascade-deleting the `invoice` records, losing billing history.
- Leaving the cascade decision for either relationship unstated ("the ORM will handle it").
