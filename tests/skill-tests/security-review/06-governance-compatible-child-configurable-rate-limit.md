---
id: security-review-06-governance-compatible-child-configurable-rate-limit
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Child Configurable Value Compatible With Mentor Mandatory Rate-Limiting Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that any endpoint accepting untrusted input must have a rate limit, with the specific threshold left to the child project to configure (Mentor Configurable boundary). A declared Child Configurable rule sets the login endpoint's rate limit to 5 requests/minute per IP. The endpoint under review enforces exactly that limit.

## Pass Criteria

- Recognizes both requirements are satisfied simultaneously with no tension: the Mentor Mandatory "must have a rate limit" requirement and the Child Configurable specific value are Compatible, not competing.
- Does not report a governance conflict or a missing-rate-limit finding — the material shows the configured limit is actually enforced.
- States the classification explicitly as Compatible (or the equivalent "no conflict, both apply") rather than omitting governance reasoning entirely because nothing is wrong.

## Fail Signals

- Flagging the child-selected specific number (5/minute) as itself a finding, when Mentor's boundary is only that *some* limit exists and the child owns the specific value.
- Treating the Child Configurable rule as either overriding or being overridden by the Mentor requirement — neither applies here; they compose.
