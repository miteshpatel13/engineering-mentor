---
id: api-review-13-governance-severity-independent-of-classification
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Governance Classification and Finding Severity Are Independent Axes

## Input Material

> Context discovery reports a Child Advisory rule: "Prefer reviewing endpoints under `/internal/**` with extra scrutiny for accidental external exposure." This Advisory prompt is why the endpoint under review — nominally under `/internal/admin/users`, but the material shows it is actually registered on the public-facing router with no distinguishing middleware — was inspected closely, revealing a full user-management contract (create/delete/modify any user) with no authorization check visible anywhere in the material.

## Pass Criteria

- Assigns the missing-authorization-check finding a severity reflecting the actual exposure (an unauthenticated user-management contract reachable on the public router), not a low severity merely because the rule that prompted inspection was only Advisory.
- Does not state or imply that the Advisory classification of the triggering rule determines the severity of what was found.
- Governance classification (Advisory) and finding severity remain visibly independent in the output.

## Fail Signals

- Downgrading the finding's severity because the governance context that prompted the review was Advisory.
- Conflating "this rule is only Advisory" with "this finding is only minor."
