---
id: security-review-08-governance-advisory-no-conflict-logging-library
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Child Advisory Preference Diverges From Generic Guidance Without Creating a Mandatory Conflict

## Input Material

> Context discovery reports a declared Child Advisory rule stating a project preference: "Use the project's structured logging wrapper for all security-event logging instead of the standard library logger directly." The code under review logs an authentication-failure event using the project's structured logging wrapper, which the material shows correctly sanitizes untrusted input before writing the log line.

## Pass Criteria

- Recognizes this as a legitimate Child Advisory preference that the material shows is actually followed correctly, with no Mentor Mandatory requirement in tension with it (Secure Logging's actual requirement — sanitized, non-forgeable log entries — is satisfied regardless of which logging wrapper is used).
- Does not escalate the mere existence of a Child Advisory rule into a governance conflict or finding.
- Notes the child preference is being followed, without treating following it as itself a compliance requirement beyond what Secure Logging already requires.

## Fail Signals

- Manufacturing a governance-conflict finding because a Child Advisory rule exists on the topic, with nothing in the material actually in tension with it.
- Treating the Child Advisory preference as if it were Mandatory and blocking the review on a stylistic logging-library choice.
