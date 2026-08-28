---
id: api-review-04-failure-vague-intent-no-concrete-contract
category: failure-handling
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Request Describes Intent, No Concrete Contract Exists

## Input Material

> "Can you review our plan for an API for managing user notifications?" No endpoint definitions, schemas, or concrete draft are provided — only the stated intent.

## Pass Criteria

- States that the material isn't concrete enough to review (Required Context / Failure Handling), rather than inventing a plausible contract to review against.
- Recommends the appropriate next step: `skills/api-contract-design/SKILL.md` for designing a concrete draft first.

## Fail Signals

- Producing a scored review (findings, severities) against a contract that doesn't actually exist in the material.
- Silently designing a contract itself rather than naming the correct Skill/step for that.
