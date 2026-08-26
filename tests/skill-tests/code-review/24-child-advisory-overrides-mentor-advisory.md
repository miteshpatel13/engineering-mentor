---
id: code-review-24-child-advisory-overrides-mentor-advisory
category: governance-advisory-override
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Advisory Rule Legitimately Replaces Mentor Advisory Guidance

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "locking-strategy.md", "sizeBytes": 600}]}`, `exceptions: {declared: false}`.

Mentor's own generic Advisory guidance (non-security, style/pattern-level) recommends optimistic locking (a version column checked on update) for typical update paths, as a general default absent a project-specific reason to prefer something else.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns:

```json
{
  "id": "locking-strategy",
  "title": "Always use pessimistic locking for financial-ledger tables",
  "classification": "advisory",
  "scope": "All writes to the ledger_entries and account_balances tables",
  "category": "database",
  "status": "active"
}
```

Diff under review — a ledger update using `SELECT ... FOR UPDATE` (pessimistic locking) rather than a version-column check:

```js
await db.transaction(async (trx) => {
  const account = await trx.raw('SELECT * FROM account_balances WHERE id = ? FOR UPDATE', [accountId]);
  await trx('account_balances').where({ id: accountId }).update({ balance: newBalance });
});
```

## Pass Criteria

- The review does not report a finding recommending optimistic locking instead — Mentor's generic Advisory locking preference is legitimately and visibly overridden here by the Child Advisory rule (`locking-strategy`), which is exactly the kind of Advisory-tier override `docs/Governance Precedence Model.md` Section 8 describes as not requiring a formal exception.
- If the review mentions the locking strategy at all, it credits the child rule as the reason pessimistic locking is the expected pattern for ledger tables in this project, rather than treating the code as deviating from a default it should be following.
- No exception entry is expected or requested for this — Advisory-level overrides are visible-but-informal by design.

## Fail Signals

- A finding recommends switching to optimistic locking, treating Mentor's generic Advisory guidance as still controlling despite the applicable, more specific Child Advisory rule.
- The review demands a formal exception before accepting the child's locking-strategy preference.
- The review frames this as a "Conflict" requiring surfacing both sides, rather than a legitimate, resolved Override (per `docs/Governance Precedence Model.md` Section 10's distinction between Override and Conflict).
