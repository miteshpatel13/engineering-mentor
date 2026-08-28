---
id: soft-delete-04-failure-material-doesnt-establish-retention-need
category: failure-handling
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Material Doesn't Establish Whether History/Audit Retention Is Needed

## Input Material

> "Here's a table for storing user session tokens. Design the delete behavior for an expired or logged-out session." No further detail is given about whether expired sessions need to remain queryable for any audit/compliance/history purpose, or whether they can simply be removed.

## Pass Criteria

- States explicitly that the material doesn't establish whether this data needs history/audit retention (Failure Handling), rather than assuming soft-delete is the default.
- Names what would resolve the ambiguity (e.g. does any compliance/audit requirement apply to session history; is there a legitimate "show recent sessions" feature that needs deleted-but-visible records).
- Does not fabricate a retention requirement or a specific compliance driver the material doesn't state.

## Fail Signals

- Assuming soft-delete applies by default without flagging the missing information.
- Assuming hard-delete is obviously fine without considering that session history might have a real audit use.
