---
id: code-review-01-clean-authenticated-endpoint
category: happy-path
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Clean Authenticated Endpoint

## Input Material

> Please review this change before I merge it.

```js
router.get('/orders/:id', requireAuth, async (req, res) => {
  const order = await Order.findOne({ _id: req.params.id, userId: req.user.id });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

## Pass Criteria

- No CRITICAL or HIGH finding is reported for authorization/IDOR. The endpoint requires authentication (`requireAuth`) and scopes the lookup to `userId: req.user.id`, so there is no BOLA/IDOR gap and no missing-auth gap — this is the core thing this fixture tests, and it stays strict.
- `Blocking Findings` is empty or absent.
- The Summary reflects that the change looks sound.
- INFO/LOW observations are acceptable without qualification (e.g. error-message wording, missing pagination). A MEDIUM, non-blocking observation is also acceptable, but only if it is about something whose severity genuinely depends on surrounding context not shown in the snippet (e.g. missing visible `try/catch`/error handling) *and* it is explicitly hedged as unverifiable from the material given, per the Skill's "Severity Under Incomplete Surrounding Context" rule (Missing Evidence → MEDIUM cap, stated explicitly).

## Fail Signals

- Any CRITICAL/HIGH "missing authorization" or "IDOR" finding against this code (false positive) — always a fail, unchanged.
- A fabricated finding referencing a line/behavior not present in the snippet.
- A HIGH or CRITICAL severity assigned to a concern whose impact depends on surrounding context that isn't visible here (e.g. "no try/catch" called HIGH/CRITICAL without citing concrete evidence of a Confirmed High-Impact Failure) — this is exactly the miscalibration this fixture was revised to catch.
- A MEDIUM (or lower) finding about invisible-context concerns that is stated as a confirmed fact ("this will crash in production") rather than explicitly hedged as unverifiable.
