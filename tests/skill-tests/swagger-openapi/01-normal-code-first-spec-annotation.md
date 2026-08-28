---
id: swagger-openapi-01-normal-code-first-spec-annotation
category: normal
skill_under_test: skills/swagger-openapi/SKILL.md
---

# Scenario: Code-First OpenAPI Annotation on Controller and DTO

## Input Material

> Design a new endpoint `POST /products` for creating a product catalog item. The developer adds a `CreateProductDto` and controller handler.

## Pass Criteria

- Annotates `CreateProductDto` fields with property descriptions, data types, and realistic examples.
- Annotates the controller method with summary, description, and security requirements (`@ApiBearerAuth`).
- Generates the OpenAPI spec directly from code annotations rather than writing a manual YAML file.

## Fail Signals

- Omitting property decorators on DTO fields.
- Failing to document request body schemas and examples.
