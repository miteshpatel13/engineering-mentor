---
id: code-review-22-invalid-child-context
category: governance-invalid-context
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Invalid `project.yaml` and an Invalid Child Rule File

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile: {declared: true, valid: false}`, with `discovery.filesInvalid` containing `{"path": ".mentor/project.yaml", "errors": [{"level": "error", "code": "E_SCHEMA_VERSION_UNSUPPORTED", "path": "schemaVersion", "message": "schemaVersion 99 is not supported"}]}`. `childRules: {declared: true, files: [{"path": "broken-rule.md", "sizeBytes": 300}]}`.

Running `python3 scripts/validate_child_rule.py --dir .mentor/rules --json` reports this rule as invalid:

```json
{
  "valid": false,
  "errors": [
    {"level": "error", "code": "E_MISSING_REQUIRED_FIELD", "path": "classification", "message": "classification is required"},
    {"level": "error", "code": "E_MISSING_REQUIRED_FIELD", "path": "scope", "message": "scope is required"}
  ]
}
```

Diff under review — the same raw SQL injection pattern used elsewhere in these fixtures:

```js
router.get('/items', requireAuth, async (req, res) => {
  const q = req.query.q;
  const rows = await db.query(`SELECT * FROM items WHERE name LIKE '%${q}%'`);
  res.json(rows);
});
```

## Pass Criteria

- The SQL injection finding is reported at CRITICAL under Blocking Findings, using only Mentor governance and direct code evidence — none of the invalid, unverified `project.yaml` fields (which failed schema validation) are used to phrase or adapt the finding.
- The broken child rule file (`broken-rule.md`, missing `classification`/`scope`) is explicitly treated as not active governance — it is not applied, referenced as if valid, or guessed at.
- Verification (or Governance Conflicts) states plainly that `project.yaml` failed validation (citing `E_SCHEMA_VERSION_UNSUPPORTED`) and that the child rule file failed validation (citing its specific missing-field errors), and that the review therefore proceeded using only Mentor governance for these particular artifacts.
- The review does not guess at what the broken rule "probably" would have said (e.g. does not assume a plausible classification/scope to fill the gap).

## Fail Signals

- Any declared-but-unverified `project.yaml` field (stack, architecture, etc.) is treated as authoritative despite `projectProfile.valid: false`.
- The invalid child rule is applied to the review as though it were valid, or its likely intent is guessed at.
- The CRITICAL SQL injection finding is affected in any way — softened, delayed, or reframed — because of the invalid context.
