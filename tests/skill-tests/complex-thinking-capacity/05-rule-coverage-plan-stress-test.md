---
id: complex-thinking-capacity-05-rule-coverage-plan-stress-test
category: rule-coverage
skill_under_test: skills/complex-thinking-capacity/SKILL.md
---

# Scenario: Stress-Test a Written Migration Plan (Mode D)

## Input Material

"Stress-test the thinking in this plan our lead wrote:

> We'll migrate all customers to the new billing service this weekend. The new service passed all unit tests, so risk is low. If anything breaks we'll fix it Monday. Finance wants it done before month-end close."

## Pass Criteria

- Recognizes Mode D and scores only D2, D5, D6, each with quoted evidence; reports D1, D3, D4 as not assessable from a written plan (not as low).
- D2 low: "passed all unit tests, so risk is low" takes the obvious answer; names the trap (unit tests don't cover data migration, integration or rollback).
- D5 low-to-mid: Finance's deadline and engineering risk are not reconciled into one answer (e.g., no staged rollout or dual-run).
- D6 1: furthest point reasoned about is "Monday".
- Computes the Thinking Level from D5 and D6, and gives the one change that would most raise each low score.
- Does not issue a blocking/non-blocking technical verdict; points to `implementation-plan-review` if one is wanted.

## Fail Signals

- Scoring D1, D3 or D4 from a written plan.
- Producing a CTC Score as if all six dimensions were observed.
- Turning the output into a severity-tagged technical review.
