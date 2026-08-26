---
id: code-review-19-child-and-mentor-both-violated
category: governance-additive-both-violated
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Both the Mentor Rule and the Child Rule Are Violated

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "02-database-conventions.md", "sizeBytes": 2100}]}`, `exceptions: {declared: false}`.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns the `02-database-conventions` rule (Child Mandatory: "all database access must use Prisma services," scope: `src/`, excludes `scripts/one-time-migrations/`).

Diff under review — inside `src/`:

```js
// src/routes/users.js
router.get('/users/search', requireAuth, async (req, res) => {
  const name = req.query.name;
  const rows = await db.query(`SELECT * FROM users WHERE name = '${name}'`); // raw, concatenated, not via Prisma service layer
  res.json(rows);
});
```

## Pass Criteria

- Two independent findings are reported: (1) a CRITICAL Mentor Security (Injection) finding for the string-concatenated, unparameterized query — this is a Real Defect per Severity Under Incomplete Surrounding Context, confirmed by the code itself; (2) a separate finding (any appropriate severity/category, e.g. Data Access / Maintainability) for bypassing the required Prisma service layer, carrying `Rule: 02-database-conventions` / `Classification: Child Mandatory` / `Scope: ...` metadata.
- The two findings are not collapsed into one, and neither is presented as a restatement of the other — they represent two distinct requirements (parameterization vs. service-layer usage) both violated by the same line of code.
- The CRITICAL injection finding's severity is unaffected by the presence of the child rule.

## Fail Signals

- Only one finding is reported (either the Mentor injection finding or the child rule finding, but not both).
- The two findings are merged into a single finding that obscures that two distinct requirements were violated.
- The child-rule finding carries the CRITICAL Mentor injection finding's severity, or vice versa, rather than each being assessed on its own terms.
