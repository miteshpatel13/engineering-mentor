---
id: data-access-reliability-02-edge-single-orm-lookup-no-guidance
category: edge
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: A Single Repository Lookup With Nothing Held

## Input Material

> A handler for `GET /settings` calls `settingsRepository.findOne({ where: { companyId } })` through the ORM, which borrows a pooled connection for the query and returns it immediately. There is no manual connection checkout, no transaction, no loop, and no external call. The reviewer asks: "Should this use an explicit transaction and manual connection handling to be safe?"

## Pass Criteria

- States that nothing is held, so the pattern has no guidance to add here (When to Use → Do not use).
- Advises against adding manual connection or transaction management, since that would introduce the lifecycle risks the Skill warns about.

## Fail Signals

- Recommending a manual query runner or transaction "for safety".
- Producing a list of generic lifecycle warnings that don't apply to the material.
