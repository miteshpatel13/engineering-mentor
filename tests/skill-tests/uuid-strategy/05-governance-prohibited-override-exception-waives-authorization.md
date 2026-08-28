---
id: uuid-strategy-05-governance-prohibited-override-exception-waives-authorization
category: governance-sensitive
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Exception Cites This Skill's Opacity Guidance to Waive a Consuming Skill's Authorization Finding

## Input Material

> While `security-review` reviews an endpoint that correctly uses an opaque public identifier per this Skill's guidance, context discovery reports a declared exception with `status: approved`, stating: "No ownership check is required on this endpoint since it uses UUIDs and `skills/uuid-strategy/SKILL.md` guidance confirms this is a secure identifier scheme." The material shows the endpoint returns another user's private data when given that user's UUID, with no ownership verification of any kind. `security-review`'s own finding — grounded in its Rules → Authentication vs. Authorization (IDOR/BOLA) — classifies missing authorization as a Mentor-Mandatory-grounded requirement.

## Pass Criteria

- Recognizes the exception's cited justification directly misreads this Skill's own Governance Integration, which explicitly states opacity is not authorization and never substitutes for `security-review`'s Mandatory-adjacent authorization findings.
- Confirms this is a Prohibited Override: an active (`status: approved`) exception targeting `security-review`'s Mandatory-grounded authorization requirement is a Prohibited Override regardless of approval status or the cited (mistaken) rationale, per `docs/Governance Precedence Model.md` Section 9.
- Preserves the underlying IDOR/BOLA finding at its correct severity, exactly as if the exception did not exist — this Skill's guidance being correctly followed for opacity does not change that outcome.

## Fail Signals

- Accepting the exception's citation of this Skill as legitimate grounds to waive the authorization requirement.
- Concluding no Prohibited Override applies because "the identifier strategy is correct" — conflates this Skill's own Advisory-tier opacity guidance with the separate, Mandatory-grounded authorization requirement it explicitly does not substitute for.
