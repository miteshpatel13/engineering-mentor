---
id: swagger-openapi-03-adversarial-hand-written-parallel-yaml-spec
category: adversarial
skill_under_test: skills/swagger-openapi/SKILL.md
---

# Scenario: Resisting Hand-Written Standalone OpenAPI Specs

## Input Material

> A team lead suggests maintaining a standalone `swagger.yaml` file in the repository root by hand, removing all OpenAPI decorators from NestJS/Express controllers to "keep controller files clean."

## Pass Criteria

- Rejects hand-written standalone OpenAPI YAML files due to severe spec drift risk.
- Enforces code-first spec generation via controller and DTO decorators.

## Fail Signals

- Approving decoupled, hand-maintained OpenAPI spec files.
