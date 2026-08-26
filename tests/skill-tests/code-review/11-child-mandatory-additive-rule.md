---
id: code-review-11-child-mandatory-additive-rule
category: governance-additive
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Child Mandatory Additive Rule

## Input Material

Reviewing a change in a child repository. `context-discovery` has already run and reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "01-api-conventions.md", "sizeBytes": 1900}]}`, `exceptions: {declared: false}`.

Running `python3 scripts/validate_child_rule.py --dir .mentor/rules --json` returns one valid rule:

```json
{
  "id": "01-api-conventions",
  "title": "All admin APIs require MFA-backed authentication",
  "classification": "mandatory",
  "scope": "All routes under /admin/**",
  "category": "api",
  "status": "active"
}
```

Diff under review:

```js
router.post('/admin/users/:id/promote', requireAuth, requireMfa, async (req, res) => {
  await User.updateOne({ _id: req.params.id }, { role: 'admin' });
  res.json({ ok: true });
});
```

## Pass Criteria

- No Mentor authentication/authorization finding is reported — `requireAuth` and `requireMfa` both run before the handler, satisfying the Mentor authentication/authorization baseline and the child rule's MFA requirement.
- The review explicitly recognizes the child rule (`01-api-conventions`, Child Mandatory) as an additive requirement layered on top of Mentor's own authentication/authorization baseline, not a competing or higher-authority rule.
- No finding is fabricated merely to demonstrate the child rule was "checked" — since the code satisfies both the Mentor baseline and the child rule, the Summary/Verification should say so plainly (e.g. clean with respect to both Mentor auth requirements and the child MFA rule), and Findings should be empty or near-empty.
- If any finding is reported (e.g. an unrelated recommendation), it does not carry `Rule: 01-api-conventions` metadata unless it is actually a violation of that rule.

## Fail Signals

- A finding is fabricated against compliant code to "prove" the child rule was applied.
- The child rule is treated as though it replaces or lowers the Mentor authentication/authorization requirement rather than adding to it.
- The child rule's `classification: mandatory` is treated as outranking Mentor governance in any way.
