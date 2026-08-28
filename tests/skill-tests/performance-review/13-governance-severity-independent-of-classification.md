---
id: performance-review-13-governance-severity-independent-of-classification
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Governance Classification and Finding Severity Are Independent Axes

## Input Material

> Context discovery reports a Child Advisory rule: "Prefer investigating checkout-flow performance reports with extra care." This Advisory prompt is why the investigation under review was conducted closely, revealing that the checkout confirmation endpoint has no defined p95 target and no post-change verification step at all despite a recent latency-affecting change — a Mentor Mandatory Measurable Targets and Post-Change Verification violation on a payment-critical path.

## Pass Criteria

- Assigns the finding a severity reflecting the actual risk (an unverified latency-affecting change on a payment-critical path with no target to catch a regression), not a low severity merely because the rule that prompted inspection was only Advisory.
- Does not state or imply that the Advisory classification of the triggering rule determines the severity of what was found.
- Governance classification (Advisory) and finding severity remain visibly independent in the output.

## Fail Signals

- Downgrading the finding's severity because the governance context that prompted the review was Advisory.
- Conflating "this rule is only Advisory" with "this finding is only minor."
