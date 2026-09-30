---
type: llm
---

PASS if the response flags all three: (1) adding `tenant_id BIGINT NOT NULL` with no default/backfill will fail on or break existing rows, (2) dropping `users_email_key` removes email uniqueness and risks duplicate accounts / data integrity, and (3) a plain `CREATE INDEX` on a 40M-row live table locks writes (recommends `CONCURRENTLY` or equivalent); and treats at least one of these as blocking.
FAIL if any of the three issues is missed or if the migration is approved as safe.
