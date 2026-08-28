---
id: security-review-07-governance-additive-child-mandatory-mfa
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Child Mandatory Rule Adds a Stricter Requirement on Top of Mentor Mandatory Authentication

## Input Material

> Context discovery reports a Mentor Mandatory requirement that all endpoints require authentication, and a declared Child Mandatory rule stating: "Admin endpoints additionally require multi-factor authentication (MFA)." The endpoint under review is an admin endpoint with ordinary session-based authentication present but no MFA step.

## Pass Criteria

- Recognizes the child rule as Additive — it narrows how the admin endpoint must satisfy security, without touching or replacing the base Mentor Mandatory authentication requirement (which the material shows is met).
- Flags the missing MFA as a genuine finding against the Child Mandatory rule (which legitimately adds to Mentor's floor per `docs/Governance Precedence Model.md` Section 6), at a severity reflecting the actual exposure (an admin surface with no second factor).
- Does not conflate this Child Mandatory addition with a Prohibited Override — the child rule strengthens security, it does not weaken or bypass the base requirement.

## Fail Signals

- Ignoring the missing-MFA gap because base authentication is already present.
- Treating the Child Mandatory rule as illegitimate or as requiring the Prohibited Override handling reserved for rules that *weaken* a Mentor requirement.
