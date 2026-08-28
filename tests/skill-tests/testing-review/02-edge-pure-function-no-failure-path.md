---
id: testing-review-02-edge-pure-function-no-failure-path
category: edge
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Pure Total Function With No Failure-Path Tests

## Input Material

> Review the test coverage for `function sum(a, b) { return a + b; }` — a pure, total function with no I/O, no external dependency, and no invalid-input path (any two numbers are valid). Its tests cover several representative input pairs including zero and negative numbers.

## Pass Criteria

- Does not flag missing failure-path test coverage — Edge Cases explicitly excludes manufacturing a failure-path finding for a unit with no plausible failure mode.
- Evaluates the existing boundary-value coverage (zero, negative numbers) on its own merits.

## Fail Signals

- Flagging "no failure path tested" as a finding for a function that has no plausible failure mode.
- Recommending speculative failure-mode tests (e.g. "test what happens if the network is down") for a pure function with no I/O.
