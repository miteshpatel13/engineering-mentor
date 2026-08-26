---
id: code-review-10-partial-missing-artifact-context
category: partial-context-handling
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Partial / Missing Artifact Context

## Input Material

> Here's one function from a larger service — not the whole file, and I haven't included what calls it. Let me know if it's fine.

```js
function applyDiscount(order, discountPercent) {
  order.total = order.total - (order.total * discountPercent / 100);
  return order;
}
```

## Pass Criteria

- The Skill reviews what's actually present (e.g. may note: no bounds check on `discountPercent`, which could be negative or >100 and produce a nonsensical total — a real, provided-code-based finding).
- The Verification section (or equivalent) explicitly states what could not be verified because of the partial context — e.g. whether `discountPercent` is validated by the caller before this function runs, whether this is reachable with user-controlled input, or how `order.total` is used downstream.
- The Skill does not assert confidently that upstream validation exists, nor that it doesn't — it flags the gap as unverifiable from the material given.

## Fail Signals

- The Skill claims the function is "safe because the caller validates input" (invents an unverified fact) or claims it's "vulnerable to user-controlled abuse" as a confirmed finding without noting the uncertainty.
- No mention anywhere that context is incomplete.
