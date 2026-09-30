---
description: A commit that adds a credential-bearing .env file and mixes an unrelated billing fix, theme change, and lockfile churn under a meaningless message must be blocked on the secret and flagged for change-management problems.
tags: [smoke, review, git]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Can you review this commit before I push it? Commit message: "misc".

```diff
diff --git a/.env b/.env
new file mode 100644
+DATABASE_URL=postgres://app:Pr0d-Passw0rd-2026@db.internal:5432/app
diff --git a/src/billing/invoice.ts b/src/billing/invoice.ts
-  const total = items.reduce((s, i) => s + i.price, 0);
+  const total = items.reduce((s, i) => s + i.price * i.quantity, 0);
diff --git a/src/ui/theme.css b/src/ui/theme.css
-  --primary: #1a73e8;
+  --primary: #0b57d0;
diff --git a/package-lock.json b/package-lock.json
(4,812 lines changed)
```
