---
id: api-contract-design-01-normal-design-from-clear-requirement
category: normal
skill_under_test: skills/api-contract-design/SKILL.md
---

# Scenario: Designing a Contract From a Clear Requirement

## Input Material

> "Consumers need to submit a long-running export job and later check its status." No existing contract for this exists yet.

## Pass Criteria

- Produces a concrete design: endpoint(s), request/response schemas, validation rules for each field, a stated versioning approach with reasoning, and designed error semantics for the operation's actual failure modes.
- States at least one genuine trade-off considered (e.g. polling vs. webhook notification) with reasoning for the chosen option, per Rules → State Trade-offs, Don't Hide Them.
- Does not add operations beyond what the stated requirement calls for.

## Fail Signals

- Producing only a vague description with no concrete schema/validation detail.
- Presenting the design with no acknowledgment of any alternative considered.
