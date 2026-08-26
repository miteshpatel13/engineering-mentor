---
id: code-review-02-sql-injection
category: security-detection
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: SQL Injection

## Input Material

> Review this before merge.

```js
app.get('/users/search', (req, res) => {
  const q = `SELECT * FROM users WHERE name = '${req.query.name}'`;
  db.query(q, (err, rows) => res.json(rows));
});
```

## Pass Criteria

- At least one CRITICAL finding, Category Security (Injection), is reported.
- The finding is listed under `Blocking Findings`.
- Recommended remediation specifies a parameterized query / prepared statement (or equivalent for the stack), not just "sanitize input."

## Fail Signals

- The injection is reported below CRITICAL/HIGH, or omitted entirely.
- The finding uses a non-canonical severity label (e.g. "Blocker", "Major").
- The finding is placed only under Non-Blocking Recommendations.
