---
id: code-review-20-classification-vs-severity-independence
category: governance-classification-severity-separation
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Governance Classification Stays Independent of Finding Severity

## Input Material

Reviewing a change in a child repository. `context-discovery` reports `mentorConfigured: true`, `projectProfile.valid: true`, `childRules: {declared: true, files: [{"path": "03-testing-requirements.md", "sizeBytes": 1600}]}`, `exceptions: {declared: false}`.

`scripts/validate_child_rule.py --dir .mentor/rules --json` returns the `03-testing-requirements` rule (Child Advisory: "prefer integration tests over deep mocking for service-layer code," scope: `src/services/**`).

Diff under review — a service method with a genuinely unrelated CRITICAL security defect, reviewed alongside a deeply-mocked test for it:

```js
// src/services/authService.js
async function login(username, password) {
  const user = await db.query(`SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`); // raw SQL, both fields concatenated, injectable, and comparing plaintext passwords
  return user[0] || null;
}

// src/services/authService.test.js
test('login queries the database', async () => {
  const mockQuery = jest.fn().mockResolvedValue([{ id: 1 }]);
  db.query = mockQuery;
  await login('alice', 'secret');
  expect(mockQuery).toHaveBeenCalled();
});
```

## Pass Criteria

- The SQL injection / plaintext-password-comparison defect in `login()` is reported at CRITICAL under Blocking Findings — its severity is driven entirely by what the code does (raw concatenated SQL comparing plaintext passwords), not by the fact that the Advisory testing rule is the reason a reviewer's attention was on this file.
- The deep-mocking test pattern is, at most, noted as an INFO/LOW, Non-Blocking observation citing the Child Advisory rule (`03-testing-requirements`) — it is not elevated to CRITICAL merely because it sits in the same review as a CRITICAL finding, and the CRITICAL finding is not downgraded merely because the rule that drew attention here is only Advisory.
- The review does not conflate "the applicable child rule here is Advisory" with "findings in this area must be low severity" — the two are explicitly treated as independent axes (governance classification vs. finding severity).

## Fail Signals

- The CRITICAL SQL injection / plaintext password finding is reported at a lower severity because the nearby child rule is only Advisory.
- The mocking-style observation is elevated to CRITICAL or Blocking because it's adjacent to a CRITICAL finding.
- The review states or implies that a rule's classification (Mandatory/Advisory) directly determines the severity of findings related to it.
