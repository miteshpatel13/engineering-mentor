---
id: security-review-01-normal-idor-missing-ownership-check
category: normal
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Endpoint Missing Object-Ownership Check

## Input Material

> `GET /invoices/:id` fetches an invoice by ID from the path and returns it to the authenticated caller. The material shows the handler checks that the caller is authenticated but does not check that the invoice belongs to that caller.

## Pass Criteria

- Flags this as AuthZ/IDOR, at HIGH or above — any authenticated caller can access another user's invoice by changing the ID.
- Explicitly distinguishes this as an authorization failure, not an authentication failure (the caller is authenticated; the gap is authorization).
- Recommends a concrete fix: an ownership check scoped to the authenticated caller.

## Fail Signals

- Conflating this with an authentication issue.
- Treating the presence of an authentication check as sufficient and not flagging the missing ownership check.
