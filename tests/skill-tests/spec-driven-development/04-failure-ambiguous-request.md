---
id: spec-driven-development-04-failure-ambiguous-request
category: failure-handling
skill_under_test: skills/spec-driven-development/SKILL.md
---

# Scenario: Request can't be classified

## Input Material

> "Can you sort out the payments thing?" No other context.

## Pass Criteria

- Asks one clarifying question that would classify the request (for example: is something broken, or is this new behavior?).
- Does not choose a workflow before the type is known.

## Fail Signals

- Guessing Feature or Bug and producing a full workflow.
- Asking a long list of questions instead of the one that classifies the request.
