---
id: api-contract-design-02-edge-fits-existing-endpoint-extension
category: edge
skill_under_test: skills/api-contract-design/SKILL.md
---

# Scenario: Requirement Naturally Extends an Existing Endpoint

## Input Material

> "We need to let consumers filter the existing `GET /orders` list by status." Context discovery / the material shows `GET /orders` already exists and supports other query parameters.

## Pass Criteria

- Recognizes this as an extension of the existing endpoint (a new query parameter) rather than designing a redundant new endpoint.
- Recommends handing the concrete change to `skills/api-review/SKILL.md` for the backward-compatibility check that an existing-contract change entails, per Edge Cases guidance.

## Fail Signals

- Designing a brand-new endpoint (e.g. `GET /orders/by-status`) when extending the existing one is the natural fit and nothing in the material rules it out.
- Failing to note that a change to an existing contract should go through the review step.
