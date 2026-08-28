---
name: validation
description: The general engineering pattern for backend validation architecture — structural DTO validation vs service-layer business rules, cross-field dependency validation, dynamic input validation, and server-authoritative recalculation. Reference material consumed by api-contract-design, security-review, and database-review.
category: Domain Patterns
skillType: Domain Pattern
---

# Validation

## Purpose

Produce the shared, reusable reference pattern for backend validation architecture. This exists as its own Skill because validation is a multi-layer concern: structural input shape must be validated at the API/DTO boundary (`api-contract-design`), domain business rules and cross-field constraints must be validated at the service layer, and sensitive security/financial inputs must be server-authoritative (`security-review`). This Skill establishes the boundary between these layers.

## Scope

**In scope:** structural validation (types, length, range, formats, enums), service-layer business rule validation (state transitions, date ranges, cross-field dependencies), server-authoritative recalculation of sensitive/financial data, and error response formatting for validation failures.

**Out of scope:** frontend UI validation logic (which is for user experience only and never trusted by the backend); database-level constraint enforcement — which is `skills/database-review/SKILL.md`'s concern. This Skill teaches the validation pattern.

## When to Use

Use when:
- Designing API request DTOs and input validation schemas.
- Implementing service-layer methods enforcing business rules across multiple fields or entities.
- Validating dynamic or schema-driven submissions (e.g. form submissions, custom fields).
- Reviewing security boundaries to ensure client inputs (prices, roles, authority) are re-checked server-side.
- Defining error response structures for invalid inputs.

Do not use frontend-only validation rules as a justification for omitting backend validation.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The core rules (never trust client input, separate structural DTO validation from service business rules, server-side recalculation) apply across frameworks and stacks.

## Workflow

1. **Classify Validation Layer:** Separate incoming checks into **Structural/Shape Validation** (handled at DTO/controller layer) and **Business Rule Validation** (handled in service/domain layer).
2. **Apply DTO Structural Validation:** Validate data types, optionality/nullability, string lengths, numeric ranges, formats (email, URL, UUID), and enum membership. Return `400 Bad Request` on failure.
3. **Apply Service-Layer Business Rules:** Validate cross-field dependencies, date ranges, entity state transitions, and relational integrity. Return `422 Unprocessable Entity` or `409 Conflict` on failure.
4. **Enforce Server-Side Authority:** For any financial, pricing, permission, or state calculation, recompute values on the server. Never accept submitted totals or client-asserted privilege flags as authoritative.
5. **Format Validation Responses:** Return structured error details identifying specific failing fields without exposing internal stack trace implementation details.

## Rules

### Two Mandatory Backend Validation Layers

Validation must occur in two explicit layers:
1. **Layer 1: DTO / Boundary Validation (Structural)** — Rejects malformed requests (invalid types, missing required fields, bad formats, out-of-range values) before reaching business logic. Produces `400 Bad Request`.
2. **Layer 2: Service / Domain Validation (Business Rules)** — Validates state transitions, cross-field logical rules, database uniqueness, and domain constraints. Produces `422 Unprocessable Entity` or `409 Conflict`.

Frontend validation exists purely for user experience and does not replace either backend layer.

### Never Trust Client-Side Calculations or Authority

Clients must never be trusted with authority over financial amounts, pricing totals, permissions, or security roles. Sensitive calculations (e.g., total price, discounts, tax, role assignments) must be recomputed server-side from authoritative database configuration regardless of values submitted in request payloads.

### Cross-Field and Dependency Validation

When fields depend on each other (e.g. `end_date` must be after `start_date`, or `spouse_name` is required when `accompanying_spouse = true`), cross-field validation must be explicitly enforced in the service layer or via custom cross-field DTO validators. Submitting dependent fields when the parent condition is `false` should be stripped or rejected.

### Dynamic Payload Validation

When validating dynamic or configurable payloads (e.g., custom forms, metadata extensions):
1. Resolve the specific active schema/version definition on the server at submission time.
2. Evaluate server-side conditional logic (e.g., hidden fields) before enforcing field requirement rules.
3. Reject unexpected or unmapped key-value pairs.

### Error Response Consistency

Validation error responses must provide clear, actionable field-level details to the client:
- Include field names, error codes, and human-readable explanations.
- Do not leak internal system exceptions, SQL error codes, or stack traces.

## Constraints

- Never accept client-submitted financial totals or pricing calculations without server-side recalculation.
- Never rely solely on frontend validation.
- Do not combine structural shape validation and complex service business logic into a single monolithic controller check.

## Governance Integration

This Skill supplies reference material (Domain Pattern) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent Advisory-tier engineering guidance grounded in `context/standards/API & Backend Standards.md` and `context/standards/Security Standards.md`.
- **Child Rules:** Child rules in `.mentor/rules/` may mandate specific HTTP status codes (`400` vs `422`) or validation libraries (`class-validator`, `zod`, `pydantic`), which narrow but do not override the two-layer validation principle.

## Validation

This Skill is validated during design and review when:
- DTOs explicitly validate shape, types, and constraints for all fields.
- Service methods validate domain business rules after DTO validation passes.
- Server-side code recalculates monetary or security-critical values.

## Edge Cases

- **Partial Updates (PATCH requests):** DTO validation for `PATCH` endpoints must distinguish between an omitted field (no change) and an explicit `null` field (clear value).
- **Conditional Field Hiding:** When a conditional rule hides a field on the frontend, the backend must verify server-side that the field is not required under current conditions.

## Failure Handling

When schema definitions or input shapes cannot be inferred from available code, state Insufficient Evidence rather than assuming validation requirements, per the Mentor Operating Model No Invention Rule.

## Expected Output

Reference material. Consuming Review Skills (`api-contract-design`, `security-review`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Server-Side Recalculation and DTO Layering
```typescript
// DTO Layer: Structural validation only
export class CreateBookingDto {
  @IsUUID()
  eventId: string;

  @IsInt()
  @Min(1)
  ticketQuantity: number;

  // Note: Total price is NOT in the DTO payload!
}

// Service Layer: Server-side price calculation
async createBooking(dto: CreateBookingDto): Promise<Booking> {
  const event = await this.eventRepo.findById(dto.eventId);
  if (!event) throw new NotFoundException('Event not found');

  // Server recomputes total price authoritatively
  const totalPrice = event.unitPrice * dto.ticketQuantity;

  return this.bookingRepo.create({ ...dto, totalPrice });
}
```

### Negative Example: Accepting Client Price and Missing Business Rule Check
```typescript
// BAD: Client submits total price, server accepts without recalculating!
export class CreateBookingDto {
  eventId: string;
  ticketQuantity: number;
  totalPrice: number; // SECURITY DEFECT: Client can submit 0.01!
}
```

## Related Skills

- `skills/api-contract-design/SKILL.md` — Related: Defines API request DTO structures and error response shapes.
- `skills/security-review/SKILL.md` — Related: Evaluates input validation as a security defense against injection and parameter tampering.
- `skills/enum-management/SKILL.md` — Related: Specifies validation mechanics for enum-backed input fields.
