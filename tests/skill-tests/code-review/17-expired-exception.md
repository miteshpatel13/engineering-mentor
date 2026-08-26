---
id: code-review-17-expired-exception
category: governance-exception-expired
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Expired Exception Provides No Benefit

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "02-database-conventions.md", "sizeBytes": 2100}]}`, `exceptions: {declared: true, path: ".mentor/exceptions.yaml", parsed: true, entryCount: 1}`.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns the same `02-database-conventions` rule as in the worked example (Child Mandatory, "all database access must use Prisma services", scope excludes `scripts/one-time-migrations/`).

`scripts/validate_exceptions_yaml.py .mentor/exceptions.yaml --json` returns one valid, expired entry:

```json
{
  "id": "old-migration-raw-sql",
  "rule": "02-database-conventions",
  "reason": "A one-time backfill script needed a raw SQL query Prisma's query builder couldn't express efficiently at the time.",
  "scope": "scripts/one-time-backfill-2025-06.js (script has since been deleted)",
  "owner": "data-team",
  "status": "expired",
  "createdAt": "2025-06-01",
  "expiresAt": "2025-07-01"
}
```

Diff under review — a new, unrelated application route that bypasses the Prisma service layer:

```js
// src/routes/reports.js
router.get('/reports/summary', requireAuth, async (req, res) => {
  const rows = await db.query('SELECT * FROM report_summary'); // raw SQL, not the Prisma service layer
  res.json(rows);
});
```

## Pass Criteria

- The child-rule finding (bypassing the required Prisma service layer, `02-database-conventions`) is reported normally, at whatever severity this Skill's judgment supports for a Child Mandatory violation — the expired exception provides it no protection, since the exception's own `scope` (a since-deleted one-time backfill script) does not cover this new route at all, and its `status` is `expired` regardless.
- The review does not treat the expired exception as relevant context for this finding — it does not mention the exception as if it softened or explained away the violation, since neither its scope nor its status supports that.
- If the exception is mentioned at all, it is only to note that it exists for a different, unrelated, already-expired scope and has no bearing on this finding.

## Fail Signals

- The finding is downgraded, softened, or treated as "already accepted" because a same-rule exception exists somewhere in `.mentor/exceptions.yaml`, without checking that its scope and status actually apply here.
- The review conflates "an exception exists for this rule" with "this specific violation is covered by an exception."
