---
id: swagger-openapi-02-edge-documenting-all-error-status-codes
category: edge
skill_under_test: skills/swagger-openapi/SKILL.md
---

# Scenario: Documenting All Return HTTP Status Codes

## Input Material

> An endpoint `POST /orders` can return `201 Created`, `400 Bad Request` (validation failure), `401 Unauthorized` (missing token), `409 Conflict` (duplicate order key), and `422 Unprocessable Entity` (insufficient stock). The developer only documents `201 Created` in Swagger.

## Pass Criteria

- Flags documenting happy-path status codes only as an incomplete specification.
- Mandates documenting all status codes (`201`, `400`, `401`, `409`, `422`) with their respective error response schemas.

## Fail Signals

- Documenting only success status codes while omitting realistic error status codes.
