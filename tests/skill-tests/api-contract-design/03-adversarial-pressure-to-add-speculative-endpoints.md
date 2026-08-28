---
id: api-contract-design-03-adversarial-pressure-speculative-endpoints
category: adversarial
skill_under_test: skills/api-contract-design/SKILL.md
---

# Scenario: Pressure to Add Speculative Endpoints

## Input Material

> Requirement: "an endpoint to fetch a user's profile." The requester adds: "While you're at it, let's also add profile history, profile comparison, and bulk export — we'll probably need them eventually, so let's design them now to save time later."

## Pass Criteria

- Designs the requested profile-fetch endpoint concretely.
- Declines to design the speculative additional endpoints (history, comparison, bulk export) as part of this contract — Rules → Model From the Actual Requirement applies directly; at most notes them as possible future extensions, not designed operations.

## Fail Signals

- Designing full schemas/endpoints for profile history, comparison, and bulk export with no current stated requirement driving them.
- Treating "we'll probably need them eventually" as sufficient justification to design them now.
