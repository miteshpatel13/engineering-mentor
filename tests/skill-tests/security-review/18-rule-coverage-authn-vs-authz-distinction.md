---
id: security-review-18-rule-coverage-authn-vs-authz-distinction
category: rule-coverage
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Authentication and Authorization Failures Must Be Reported as Distinct Finding Categories

## Input Material

> Two independent endpoints are under review in the same change.
>
> Endpoint A (`GET /api/internal/reports/:id`): has no authentication check at all — any caller, with no session, token, or credential of any kind, can call it directly and receive the report data. The material confirms no middleware or check of any kind runs before the handler.
>
> Endpoint B (`GET /api/orders/:id`): requires a valid authenticated session (the material confirms an authentication check runs and rejects unauthenticated requests), but then returns whichever order matches `:id` with no check that the authenticated caller owns that order — any logged-in user can read any other user's order by changing the ID.

## Pass Criteria

- Reports Endpoint A as an Authentication (AuthN) finding: no caller identity is established at all before the handler runs. Does not call this "IDOR" or "authorization" — there is no caller to authorize because none was authenticated.
- Reports Endpoint B as an Authorization (AuthZ/IDOR) finding: the caller's identity is established (authentication succeeds), but the system fails to check whether that identity is *allowed* to access the specific resource. Does not call this a "missing authentication" finding — authentication is present and working in the material.
- Produces two distinct findings, each in its own correct category (per Rules → Authentication vs. Authorization and Expected Output's Category field), never merged into one finding or one label covering both.
- Both findings receive a severity independently, based on their own actual exposure — not inherited from each other.

## Fail Signals

- Labeling Endpoint A's finding "IDOR," "authorization," or "AuthZ."
- Labeling Endpoint B's finding "missing authentication" or "AuthN."
- Merging both endpoints into a single finding or a single loosely-worded "access control" category that doesn't specify which failure mode applies to which endpoint.
- Using "authentication" and "authorization" interchangeably anywhere in the output for either endpoint.
