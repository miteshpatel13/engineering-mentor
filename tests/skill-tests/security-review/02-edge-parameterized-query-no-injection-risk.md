---
id: security-review-02-edge-parameterized-query-no-injection-risk
category: edge
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Fully Parameterized Query, No Injection Risk

## Input Material

> Review this code: `db.query("SELECT * FROM users WHERE email = $1", [userEmail])`, where `userEmail` comes directly from request input, using a parameterized query API with no string concatenation anywhere in the material.

## Pass Criteria

- Does not flag this as a SQL injection risk — the material shows a fully parameterized query with no concatenation of untrusted input into the query string.
- May note that the parameterization is correctly applied, without inventing a hypothetical injection vector not supported by the material.

## Fail Signals

- Flagging "possible SQL injection" against this code despite the parameterized query, i.e. a false positive with no supporting evidence in the material — Rules → False-Positive Discipline exists specifically to prevent this.
