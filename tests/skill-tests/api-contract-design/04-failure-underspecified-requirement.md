---
id: api-contract-design-04-failure-underspecified-requirement
category: failure-handling
skill_under_test: skills/api-contract-design/SKILL.md
---

# Scenario: Requirement Too Vague to Model

## Input Material

> "We need an API for reports." No detail is given about what a report contains, who consumes it, what operations are needed (generate, fetch, list, schedule), or on what resource.

## Pass Criteria

- States that the requirement doesn't specify enough about the actual operations needed to design a concrete contract (Failure Handling), and names what's missing (what a report contains, what operations are needed, who consumes it).
- Does not invent a plausible-sounding reports API (endpoints, schemas) to fill the gap.

## Fail Signals

- Producing a concrete designed contract (specific endpoints/schemas) from this vague a requirement, inventing the missing detail.
