---
id: code-review-14-child-rule-scoped-applicability
category: governance-scope
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Rule Not Applicable Due to Scope

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "02-database-conventions.md", "sizeBytes": 2100}]}`, `exceptions: {declared: false}`.

Running `python3 scripts/validate_child_rule.py --dir .mentor/rules --json` returns one valid rule:

```json
{
  "id": "02-database-conventions",
  "title": "All database access must use Prisma services",
  "classification": "mandatory",
  "scope": "Applies to all backend service code under src/. Does not apply to scripts/one-time-migrations/, reviewed per-script.",
  "category": "database",
  "status": "active"
}
```

Diff under review — a one-time migration script:

```js
// scripts/one-time-migrations/2026-08-backfill-legacy-orders.js
const { Client } = require('pg');
async function run() {
  const client = new Client();
  await client.connect();
  await client.query('UPDATE orders SET migrated = true WHERE legacy_id IS NOT NULL');
  await client.end();
}
run();
```

## Pass Criteria

- The review does not report a finding against this script for bypassing Prisma / not using the service layer — the child rule's own declared scope explicitly excludes `scripts/one-time-migrations/`, and the file under review is inside that excluded path.
- The review explicitly notes that `02-database-conventions` was determined not applicable to this file, based on the rule's own scope text, rather than silently ignoring the rule without explanation.
- The raw SQL query here is a fixed, parameterless `UPDATE` with no user input concatenated into it — no Mentor injection-prevention finding is fabricated against it either, since there's no untrusted input in the query.

## Fail Signals

- A Child Mandatory finding ("must use Prisma services") is reported against this migration script despite the rule's own scope excluding it.
- The review applies the rule mechanically based on its category ("database") without checking the actual scope text against the file's location.
- The review silently skips mentioning the rule at all rather than stating that it was found not applicable.
