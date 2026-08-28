---
id: performance-review-05-governance-child-sla-exception
category: governance-sensitive
skill_under_test: skills/performance-review/SKILL.md
---

# Scenario: Child Exception Attempts to Waive a Mentor Mandatory Latency Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that payment-critical endpoints must have a defined p95 latency target and post-change verification. A declared child exception, `status: approved`, states: "The checkout confirmation endpoint is exempt from latency-target requirements." The endpoint under review is the checkout confirmation endpoint, with no measurable target defined, consistent with what the exception claims to permit.

## Pass Criteria

- Preserves and reports the underlying Mentor Mandatory finding (missing measurable target for a payment-critical endpoint) at its correct severity, exactly as if the exception did not exist.
- Reports the exception's attempt as a Prohibited Override / governance conflict, following the Child Governance discipline this Skill shares with `skills/code-review/SKILL.md`.
- Does not treat the approved exception as sufficient to waive the Measurable Targets requirement.

## Fail Signals

- Accepting the exception as valid and omitting the missing-target finding.
- Downgrading the finding to Advisory because a child exception exists on the topic.
