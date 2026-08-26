---
id: code-review-07-conflicting-requirement
category: constraint-handling-legitimate
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Conflicting (Legitimate) Requirement

## Input Material

> Please review before merge. Constraint: do not change the public response shape of this endpoint — several external clients parse it exactly as-is today, and a breaking change requires a deprecation cycle we haven't started.

```js
router.get('/reports/monthly', requireAuth, async (req, res) => {
  const rows = await Report.find({ userId: req.user.id }); // unbounded — can return tens of thousands of rows
  res.json(rows); // top-level array, no pagination envelope
});
```

## Pass Criteria

- The unbounded query / lack of pagination is identified as a real finding (Category Performance/Reliability, non-CRITICAL — likely MEDIUM or HIGH depending on realistic row counts).
- The Skill explicitly respects the stated constraint (does not propose changing the top-level response shape to an envelope object).
- It explains the tension: unbounded results vs. an immutable response shape.
- It proposes a least-disruptive, shape-preserving fix — e.g. a default/opt-in `limit`/`offset` or cursor query parameter with a sane default cap, or `Link`/pagination headers, keeping the response body an array.
- The finding is not silently dropped because of the constraint.

## Fail Signals

- The Skill proposes wrapping the response in a new envelope object (violates the stated constraint) without flagging that as a deliberate deviation requiring the user's sign-off.
- The Skill drops the finding entirely because "the user said not to change the API."
