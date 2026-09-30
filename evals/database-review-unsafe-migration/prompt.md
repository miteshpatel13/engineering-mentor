---
description: A migration adding a NOT NULL column without default/backfill, dropping a uniqueness constraint, and building a blocking index must trigger database-review and be flagged as blocking.
tags: [review, database]
max_turns: 30
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
---

Review this migration for our production PostgreSQL database. The `users` table has about 40 million rows and serves live traffic.

```sql
ALTER TABLE users ADD COLUMN tenant_id BIGINT NOT NULL;
ALTER TABLE users DROP CONSTRAINT users_email_key;
CREATE INDEX idx_users_tenant ON users (tenant_id);
```

The app code change that ships with it starts writing `tenant_id` on new signups only.
