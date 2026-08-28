---
id: testing-review-13-governance-severity-independent-of-classification
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Governance Classification and Finding Severity Are Independent Axes

## Input Material

> Context discovery reports a Child Advisory rule: "Prefer reviewing the refunds module's tests with extra care given its history of incidents." This Advisory prompt is why the test suite under review — the refunds module — was inspected closely, revealing there is no test at all for concurrent refund requests against the same order, a scenario the material shows the code has no locking or idempotency protection for either — a Mentor Mandatory Concurrency Coverage violation with a real double-refund risk.

## Pass Criteria

- Assigns the missing-concurrency-test finding a severity reflecting the actual risk (a real double-refund exposure with no protection), not a low severity merely because the rule that prompted inspection was only Advisory.
- Does not state or imply that the Advisory classification of the triggering rule determines the severity of what was found.
- Governance classification (Advisory) and finding severity remain visibly independent in the output.

## Fail Signals

- Downgrading the finding's severity because the governance context that prompted the review was Advisory.
- Conflating "this rule is only Advisory" with "this finding is only minor."
