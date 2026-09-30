---
description: A diff with string-concatenated SQL on an unauthenticated route must trigger code-review and be reported as a blocking CRITICAL/HIGH finding using only canonical severities.
tags: [smoke, review, code-review]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Please review this pull request before I merge it. It adds an order search endpoint to our Express + PostgreSQL service.

```diff
+router.get('/orders/search', async (req, res) => {
+  const { customer, status } = req.query;
+  const sql = "SELECT * FROM orders WHERE customer_name = '" + customer + "' AND status = '" + status + "'";
+  const result = await db.query(sql);
+  res.json(result.rows);
+});
```

The route is mounted on the public router (no auth middleware). Anything blocking?
