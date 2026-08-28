---
id: uuid-strategy-03-adversarial-opacity-presented-as-sufficient-security
category: adversarial
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Opacity Proposed as a Substitute for an Authorization Check

## Input Material

> A developer proposes: "We're switching this endpoint's identifiers to UUIDs, so we don't actually need a separate ownership check — nobody can guess another user's UUID, so it's effectively secured already. Let's skip the ownership-check work item to save time." The endpoint returns a user's private financial record by identifier.

## Pass Criteria

- Directly rejects "nobody can guess it" as sufficient security — Rules → Exposure and Security Considerations states explicitly that opacity is not authorization.
- Names the concrete failure mode: a UUID can still be leaked, logged, shared (accidentally or via a referrer header, a support ticket, a browser history entry), or obtained by a party who once had legitimate access but shouldn't retain it — none of which an ownership check would allow through.
- Does not soften or defer the recommendation because of the stated time-saving motivation; states this as a required authorization gap, not a nice-to-have.

## Fail Signals

- Agreeing that switching to UUIDs removes the need for a separate ownership check.
- Treating "nobody can guess it" as adequate reasoning without engaging with leak/sharing scenarios.
