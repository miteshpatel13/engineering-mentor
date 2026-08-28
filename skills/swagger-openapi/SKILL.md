---
name: swagger-openapi
description: The general engineering workflow for OpenAPI/Swagger API documentation — code-first spec generation, complete status code schemas, DTO property metadata, enum value mapping, and atomic spec synchronization with API changes. Workflow guidance for building and maintaining API specifications.
category: Documentation
skillType: Authoring/Workflow
---

# Swagger / OpenAPI Documentation

## Purpose

Produce the shared, reusable workflow guidance for authoring, maintaining, and validating OpenAPI/Swagger documentation for RESTful web APIs. This exists as an Authoring/Workflow Skill because API documentation is an integral part of API contract design (`api-contract-design`) — requiring code-first spec generation, explicit HTTP status code schemas, enum value documentation, and atomic synchronization between application code and published specs.

## Scope

**In scope:** code-first OpenAPI/Swagger spec annotation conventions, DTO property metadata, path/query parameter documentation, authentication/authorization scheme definitions, enum value mapping, request/response schema examples, and atomic spec-code synchronization workflows.

**Out of scope:** configuring specific API gateway UI hosting servers (e.g., Swagger UI server deployment pipelines); designing the core HTTP response payload formats — which is `skills/api-contract-design/SKILL.md`'s concern. This Skill teaches the documentation workflow.

## When to Use

Use when:
- Authoring a new API endpoint or controller method.
- Modifying request DTOs, response bodies, or validation rules on existing endpoints.
- Annotating controllers or DTO classes with OpenAPI/Swagger decorators.
- Reviewing Pull Requests that touch API endpoints to ensure spec synchronization.
- Documenting authentication schemes, path parameters, or error response formats.

Do not use hand-maintained standalone YAML specs that are decoupled from application code and prone to drift.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). Core documentation requirements (documenting all return status codes, DTO property descriptions, code-first generation, atomic commits) apply across programming languages and framework OpenAPI tooling.

## Workflow

1. **Annotate Request DTOs:** Decorate DTO fields with property descriptions, data types, format constraints, optionality, and realistic example values.
2. **Document Enums Dynamically:** Map enum-backed fields to their typed enum declarations, documenting both integer/code values and human-readable names.
3. **Annotate Controller Endpoints:** Add summary and detailed business context descriptions to endpoint route handlers.
4. **Specify Security Schemes:** Declare required authentication (e.g., Bearer JWT) and role authorization requirements per endpoint.
5. **Declare All Response Status Codes:** Explicitly document every HTTP status code the endpoint can return (`200`, `201`, `400`, `401`, `403`, `404`, `409`, `422`), linking each to its specific response schema and example payload.
6. **Synchronize Spec with Code Changes:** Update OpenAPI decorators in the exact same commit whenever endpoint logic or DTO shapes change.

## Rules

### Code-First Generation over Hand-Written Parallel Specs

OpenAPI specs must be generated directly from application source code and DTO annotations (e.g. framework OpenAPI decorators or schema reflection). Maintaining a separate, hand-written OpenAPI YAML file decoupled from application code leads to specification drift and is unacceptable.

### Atomic Synchronization with Code Changes

OpenAPI documentation is part of the definition of done for an API task. Any change to a controller, route, request DTO, response shape, validation rule, or error condition must include corresponding OpenAPI decorator updates within the same commit. A published spec that disagrees with runtime endpoint behavior is treated as a bug.

### Complete Status Code and Error Schema Coverage

Endpoints must document *every* HTTP status code they can return, not just success responses (`200`/`201`).
- **Success Responses:** Include response body DTO schemas and realistic success payload examples.
- **Error Responses:** Document error status codes (`400`, `401`, `403`, `404`, `409`, `422`) using standardized error payload schemas (`skills/api-contract-design/SKILL.md`). Include distinct examples for different error conditions.

### Comprehensive Parameter Documentation

All endpoint parameters must be documented:
- **Path Parameters:** Specify parameter name, data type (e.g. UUID format per `skills/uuid-strategy/SKILL.md`), and description.
- **Query Parameters:** Document pagination parameters (`page`, `limit` or cursor), filters, and sort orders, including default values and allowed bounds.
- **Header Parameters:** Document custom headers (e.g. `Idempotency-Key` per `skills/idempotency/SKILL.md`).

### Dynamic Enum Documentation

Enum-backed fields in request payloads or response bodies must document all allowed values dynamically from code enums (`skills/enum-management/SKILL.md`). Include both numeric/string code values and member names in description metadata to avoid manual comment drift.

### Alignment Between Validation and Spec Optionality

A field's optionality in OpenAPI documentation must match its DTO validation rules. Marking a field as optional in OpenAPI while enforcing `@IsDefined()` in validation is an inconsistency defect.

## Constraints

- Never commit an API change without updating its corresponding OpenAPI/Swagger annotations in the same change.
- Do not document happy-path `200 OK` status codes only while omitting error status codes.
- Do not hand-type enum value lists in static string comments; reference central enum definitions.

## Governance Integration

This Skill provides workflow guidance for API documentation per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent strongly recommended Advisory-tier workflow practices grounded in `context/standards/API & Backend Standards.md` and `context/standards/Documentation Standards.md`.
- **Child Rules:** Projects may define specific OpenAPI route paths (e.g. `/api/docs`), title metadata, or decorator libraries in `.mentor/rules/`.

## Validation

This Skill is validated during pull request review and automated checks when:
- Controller routes and DTO classes contain OpenAPI decorators.
- All returned HTTP status codes have documented response schemas.
- OpenAPI specs generate without syntax or reflection errors.
- DTO optionality matches OpenAPI property metadata.

## Edge Cases

- **Polymorphic Responses:** Endpoints returning different object schemas based on type discriminators must use OpenAPI `oneOf` or `anyOf` schema compositions with explicit discriminator mappings.
- **File Upload Endpoints:** Multipart form upload endpoints must document binary request schemas (`format: binary`) and acceptable MIME types.

## Failure Handling

When endpoint routes or DTO decorators are missing, report Insufficient Evidence regarding API documentation and mark the endpoint specification as incomplete.

## Expected Output

Updated, fully annotated controller and DTO source code producing an accurate, complete OpenAPI specification.

## Examples

### Positive Example: Complete Endpoint OpenAPI Annotation
```typescript
@ApiTags('Orders')
@Controller('orders')
@ApiBearerAuth()
export class OrderController {

  @Post()
  @ApiOperation({ 
    summary: 'Create a new order',
    description: 'Submits a new customer order. Prices are recomputed server-side.' 
  })
  @ApiHeader({ name: 'Idempotency-Key', required: true, description: 'Unique retry key' })
  @ApiResponse({ status: 201, description: 'Order created successfully', type: OrderResponseDto })
  @ApiResponse({ status: 400, description: 'Validation failed or missing header', type: ApiErrorResponseDto })
  @ApiResponse({ status: 409, description: 'Duplicate idempotency key conflict', type: ApiErrorResponseDto })
  async createOrder(
    @Headers('Idempotency-Key') idempotencyKey: string,
    @Body() dto: CreateOrderDto
  ): Promise<OrderResponseDto> {
    return this.orderService.create(idempotencyKey, dto);
  }
}
```

### Negative Example: Hand-Written YAML and Missing Status Codes
```typescript
// BAD: Controller has zero decorators; team maintains a separate swagger.yaml manually!
@Controller('orders')
export class OrderController {
  @Post()
  async createOrder(@Body() dto: any) {
    // DEFECT: Spec drifts immediately when dto changes!
  }
}
```

## Related Skills

- `skills/api-contract-design/SKILL.md` — Related: Defines core API response shapes, error structures, and URL path conventions.
- `skills/validation/SKILL.md` — Related: Provides DTO validation decorators that generate OpenAPI request schemas.
- `skills/enum-management/SKILL.md` — Related: Sourcing enum values for OpenAPI property schemas.
- `skills/uuid-strategy/SKILL.md` — Related: Documenting UUID path parameter formats.
- `skills/idempotency/SKILL.md` — Related: Documenting idempotency request headers in OpenAPI specs.
