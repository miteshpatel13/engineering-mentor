---
id: implementation-plan-review-02-edge-plan-contradicted-by-codebase
category: edge
skill_under_test: skills/implementation-plan-review/SKILL.md
---

# Scenario: Plan assertion contradicted by codebase context

## Input Material

> `plan.md` says "`calculate_price()` has no other callers, so its signature can change freely." Codebase orientation (Graft caller trace, confirmed in source) shows `calculate_price()` is also called by `jobs/revenue_report.py` and `api/quotes.py`.

## Pass Criteria

- Reports the contradiction as a finding with the file evidence, rated HIGH because tasks derived from the wrong picture would break two consumers.
- Recommends the plan account for both callers (or keep a compatible signature).

## Fail Signals

- Accepting the plan's assertion without checking.
- Reporting the Graft result without noting it was verified against source.
