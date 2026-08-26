---
id: code-review-06-false-positive-resistance
category: false-positive-discipline
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: False-Positive Resistance

## Input Material

> Review before merge.

```js
router.get('/orders/:id', requireAuth, async (req, res) => {
  const order = await Order.findOne({ _id: req.params.id, userId: req.user.id });
  if (!order) return res.status(404).json({ error: 'Not found' });

  const auditQuery = `SELECT * FROM audit_log WHERE order_id = ?`;
  db.query(auditQuery, [req.params.id], (err, rows) => {
    if (err) return res.status(500).json({ error: 'Internal error' });
    res.json({ order, audit: rows });
  });
});
```

## Pass Criteria

- No CRITICAL/HIGH "SQL injection" finding — `auditQuery` uses a parameterized placeholder (`?`) with the value passed separately, not string concatenation. This stays strict.
- No CRITICAL/HIGH "missing authorization" finding — the order lookup is scoped to `userId: req.user.id`, same pattern as fixture 01. This stays strict.
- The Summary reflects that the change looks sound. INFO/LOW observations are acceptable without qualification (e.g. mixed callback/async style). A MEDIUM, non-blocking observation is also acceptable under the same condition as fixture 01: only for a concern whose severity genuinely depends on invisible surrounding context (e.g. missing visible `try/catch`), and only when explicitly hedged as unverifiable, per "Severity Under Incomplete Surrounding Context."

## Fail Signals

- A CRITICAL/HIGH injection finding against the parameterized query (misreading `?` placeholders as string concatenation).
- A CRITICAL/HIGH authorization finding against the already-scoped order lookup.
- A HIGH/CRITICAL severity assigned to the missing-`try/catch` observation without citing concrete evidence of a Confirmed High-Impact Failure.
