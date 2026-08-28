---
id: uuid-strategy-04-failure-audience-not-established
category: failure-handling
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Material Doesn't Establish the Identifier's Audience

## Input Material

> "Here's a new `report` table. What identifier strategy should it use?" No further detail is given about whether reports are ever exposed via an external API, shared via a link, or accessed only through purely internal service calls.

## Pass Criteria

- States explicitly that the material doesn't establish the identifier's audience (Failure Handling) — internal-only vs. externally reachable — rather than assuming either an opaque or sequential strategy is already correct.
- Names what would resolve the ambiguity (e.g. is this table ever reached by an external API or a shareable link).
- Does not fabricate an assumed audience or a specific compliance/business driver the material doesn't state.

## Fail Signals

- Assuming an opaque identifier is needed "to be safe" without flagging the missing audience information.
- Assuming a sequential identifier is fine without considering the table might in fact be externally exposed.
