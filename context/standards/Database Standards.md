# Database Standards

- Protect data integrity with appropriate constraints.
- Choose data types deliberately.
- Index based on real access patterns.
- Inspect query plans for slow queries.
- Avoid N+1 queries.
- Fetch only necessary data.
- Use transactions when atomicity is required.
- Consider race conditions and locking.
- Acquire a connection as late as possible and release it exactly once, on every path (guaranteed-cleanup construct); never leak or double-release one.
- Roll back before every early exit from an open transaction, and send every write in the unit through the transaction's own handle.
- Never hold a connection or open transaction across an external call, a queue wait, or the need for a second connection from the same pool.
- Size connection pools so every pool on every instance, including deploy surges, fits the database's connection limit; one pool per process.
- Make migrations reproducible and safe.
- Run migrations and scheduled jobs once per deploy or period across all instances, not once per instance.
- Avoid destructive production changes without a verified plan.
- Understand generated SQL when using an ORM.
