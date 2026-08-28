---
id: swagger-openapi-05-rule-coverage-atomic-spec-code-updates
category: rule-coverage
skill_under_test: skills/swagger-openapi/SKILL.md
---

# Scenario: Atomic Synchronization of API Changes and OpenAPI Metadata

## Input Material

> A Pull Request adds a new query parameter `category_id` to an API endpoint implementation, but does not add `@ApiQuery()` or update DTO property metadata, promising to "add Swagger docs in a follow-up ticket."

## Pass Criteria

- Rejects deferring Swagger documentation to a separate task.
- Enforces that API code changes and OpenAPI metadata updates occur atomically within the exact same commit.

## Fail Signals

- Allowing API code changes to be merged without updating corresponding OpenAPI documentation in the same commit.
