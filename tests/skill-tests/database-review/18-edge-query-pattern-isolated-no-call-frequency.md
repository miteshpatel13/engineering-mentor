---
id: database-review-18-edge-query-pattern-isolated-no-call-frequency
category: edge
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: N+1 Pattern Reviewed With No Visibility Into Actual Call Frequency

## Input Material

> A code review shows an ORM lazy-loading pattern: for each `order` in a fetched list of orders, the code accesses `order.customer.name` in a loop, triggering one additional query per order (a classic N+1 pattern per Rules → N+1 Query Risk). The material provides only this code snippet — no information about how many orders are typically in the list, how often this code path runs, or current production traffic to it.

## Pass Criteria

- Flags the N+1 pattern as a finding regardless of the missing call-frequency information — per the named Edge Case in `skills/database-review/SKILL.md`, "an N+1 pattern is still flagged... regardless of current call volume" because it is a correctness/scalability risk inherent to the pattern itself, not contingent on proof of current impact.
- Sets the finding's severity to reflect that actual production impact/scale could not be established from the material — states explicitly that call frequency and typical collection size are not knowable from what was provided, rather than assuming either a worst-case ("this runs constantly on huge lists") or best-case ("this probably never matters") scenario.
- Cites the actual code pattern (the loop triggering a per-item query) as the evidence for the finding, not merely "ORM lazy-loading has a bad reputation for this."

## Fail Signals

- Declining to flag the N+1 pattern at all because call frequency isn't documented — the Skill's own Edge Cases section explicitly rules this out.
- Assuming worst-case production scale with no evidence to assign a severity higher than the material supports.
- Citing the ORM's general reputation for N+1 risk instead of the specific loop-triggers-a-query pattern actually shown in the material.
