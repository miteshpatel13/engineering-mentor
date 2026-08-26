---
id: code-review-03-bola-idor
category: security-detection
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: BOLA / IDOR

## Input Material

> Review this new endpoint before merge.

```js
router.get('/invoices/:id', requireAuth, async (req, res) => {
  const invoice = await Invoice.findById(req.params.id);
  res.json(invoice);
});
```

## Pass Criteria

- A CRITICAL finding, Category Security (BOLA/IDOR or Broken Access Control), is reported: the endpoint is authenticated but does not verify the requester owns/may access the invoice identified by `:id`.
- The finding is listed under `Blocking Findings`.
- Recommended remediation specifies scoping the lookup to the authenticated user (or an explicit authorization check), analogous to fixture 01's pattern.

## Fail Signals

- No finding reported (the presence of `requireAuth` is mistaken for sufficient authorization).
- The finding is downgraded below CRITICAL/HIGH without justification.
