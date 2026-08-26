---
id: code-review-08-severity-taxonomy-consistency
category: taxonomy-compliance
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Severity Taxonomy Consistency

## Input Material

> Review before merge.

```js
app.post('/admin/reset-password', (req, res) => {
  // No authentication check at all on an admin-only operation
  const q = `UPDATE users SET password = '${req.body.newPassword}' WHERE email = '${req.body.email}'`;
  db.query(q, (err) => {
    if (err) return res.status(500).send('error');
    res.send('ok'); // no response body validation, plaintext password stored
  });
});
console.log('debug: reset endpoint hit', req.body); // leftover debug log, wrong scope entirely (style-only issue)
```

## Pass Criteria

- Multiple findings are produced, spanning at least: a CRITICAL (missing authentication on an admin operation and/or SQL injection and/or plaintext password storage — any combination is acceptable as long as CRITICAL is used correctly) and at least one lower-severity finding (e.g. LOW/INFO for the misplaced/leftover debug log).
- Every single severity label used anywhere in the output is one of exactly: CRITICAL, HIGH, MEDIUM, LOW, INFO.
- No occurrence of "Major", "Minor", "Blocker", "Required", "Optional", "P0", "P1", "Severe", or any other non-canonical label.

## Fail Signals

- Any non-canonical severity word appears anywhere in the output.
- Findings are listed without any severity at all.
