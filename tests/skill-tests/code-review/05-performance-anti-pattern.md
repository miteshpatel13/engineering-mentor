---
id: code-review-05-performance-anti-pattern
category: performance-detection
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Performance Anti-Pattern (N+1)

## Input Material

> This powers the main dashboard, loaded on every page view for every logged-in user. Please review before merge.

```js
async function getOrdersWithItems(userId) {
  const orders = await Order.find({ userId });
  for (const order of orders) {
    order.items = await Item.find({ orderId: order.id }); // one query per order
  }
  return orders;
}
```

## Pass Criteria

- A finding is reported with Category Performance, identifying the N+1 query pattern (one `Item.find` per order instead of a single batched query).
- The finding uses a canonical severity (MEDIUM or HIGH is reasonable given it's on a hot, high-traffic path — the specific level is a judgment call, but it must not be omitted, and must not be CRITICAL since there's no data-loss/security dimension).
- Recommended remediation describes batching (e.g. a single `Item.find({ orderId: { $in: orderIds } })` or a join/populate).

## Fail Signals

- The N+1 pattern is not identified at all.
- The finding is tagged CRITICAL (miscategorized as a correctness/security issue) or omitted from both Findings sections.
