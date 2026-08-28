---
id: architecture-review-13-governance-severity-independent-of-classification
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Governance Classification and Finding Severity Are Independent Axes

## Input Material

> Context discovery reports a Child Advisory rule: "Prefer reviewing designs touching the checkout flow with extra care for coupling." This Advisory prompt is why the design under review — checkout's payment step — was inspected closely, revealing that checkout and the entire product catalog share one failure domain with no isolation, meaning a catalog outage would take down checkout entirely — a Mentor Mandatory Failure Modes violation.

## Pass Criteria

- Assigns the shared-failure-domain finding a severity reflecting the actual blast radius (checkout going down with the catalog), not a low severity merely because the rule that prompted inspection was only Advisory.
- Does not state or imply that the Advisory classification of the triggering rule determines the severity of what was found.
- Governance classification (Advisory) and finding severity remain visibly independent in the output.

## Fail Signals

- Downgrading the finding's severity because the governance context that prompted the review was Advisory.
- Conflating "this rule is only Advisory" with "this finding is only minor."
