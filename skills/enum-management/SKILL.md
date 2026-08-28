---
name: enum-management
description: The general engineering pattern for managing enumerated types — integer-backed persistence, centralized enum registries, API serialization, boundary validation, and schema evolution without breaking persisted data. Reference material consumed by database-review and api-contract-design.
category: Domain Patterns
skillType: Domain Pattern
---

# Enum Management

## Purpose

Produce the shared, reusable reference pattern for managing enums (enumerated domain types) across database storage, application logic, and external API contracts. This exists as its own Skill because enum management spans schema design (`database-review`), input validation (`validation`), and API serialization (`api-contract-design`) — requiring consistent rules for value assignment, immutability of persisted values, and boundary conversions.

## Scope

**In scope:** centralized enum definition practices, integer-backed vs string-backed database storage choices, explicit numeric assignment and value stability, DTO validation at the API boundary, string-to-integer translation, and rules for extending or deprecating enum members safely.

**Out of scope:** master data tables managed dynamically by application admins (which should be database lookup tables with active flags rather than code-compiled enums); framework-specific DTO libraries — this Skill teaches the general design pattern.

## When to Use

Use when:
- Adding a new enumerated status, category, or type to a system schema.
- Deciding whether a concept belongs as a code-defined enum versus a dynamic lookup table.
- Designing API DTO validation for enum-backed fields.
- Updating an existing enum with new members or deprecating legacy values.
- Reviewing schema changes for enum persistence safety.

Do not use for entity relationships where options are dynamically managed via administrative interfaces at runtime.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). The core rules (explicit values, immutability of persisted integers, single-source definition) apply universally across programming languages and relational database engines.

## Workflow

1. **Distinguish Enum from Master Data:** Verify that the set of values is fixed, small, and controlled exclusively by code releases (e.g. `PaymentStatus`, `OrderStatus`). If values must be added at runtime by users without code deployment, use a lookup table instead.
2. **Centralize Definitions:** Declare enums in a single, shared domain module per language/service, avoiding duplicate inline enum definitions across modules.
3. **Assign Explicit Ordinals/Values:** Assign explicit numeric (or fixed string) values to every member (e.g., `PENDING = 1`, `APPROVED = 2`). Never rely on implicit position-based auto-increment.
4. **Choose Storage Type:** Use fixed small integer columns (e.g. `TINYINT UNSIGNED` or `SMALLINT`) or standard text codes, documenting the mapping clearly in schema comments.
5. **Validate at Boundary:** Validate incoming requests against the exact enum value set at the API boundary before passing values to internal business logic or storage.
6. **Evolve Additively:** Only append new members with unused integers/codes. Never renumber or reuse retired member values.

## Rules

### Explicit Value Assignment and Freeze Principle

Every member of a code enum must be explicitly assigned a permanent value. Once any environment has persisted an enum value, that specific value-to-meaning mapping is frozen permanently.
- **Never renumber:** Never change the numeric value of an existing enum member.
- **Never re-order:** Changing declaration order must not alter underlying values.
- **Append-only:** Add new members by assigning fresh, previously unused values.

### Centralized Source of Truth

Enum definitions must live in a centralized, shared code location within the domain/application layer. Do not define parallel or duplicate enum declarations for the same domain concept across different files or microservices.

### Integer Storage over Native SQL ENUM Types

Prefer standard integer columns (`TINYINT UNSIGNED`, `SMALLINT`, or `INT`) for database persistence rather than native database `ENUM(...)` types. Native SQL enums introduce database DDL migration complexity when adding new values (requiring `ALTER TABLE`), whereas integer columns allow instant code-side extension without lock-heavy table alterations.

### API Boundary Validation

API endpoints accepting enum values must strictly validate incoming input against valid enum members at the controller/DTO layer. Rejections must produce clear client errors (`400 Bad Request` or `422 Unprocessable Entity`) before invalid integer values reach data access or database layers.

### Business Logic Comparison

Application code must perform logic checks against the typed enum constant (e.g. `order.status === OrderStatus.COMPLETED`), never against magic numbers (`order.status === 2`) or arbitrary string literals.

### Enum vs Master Data Decision

If a value set requires runtime additions, localized titles, or user permissions managed via admin UI, it is **Master Data**, not an Enum. Master data must be modeled as a relational table (`id`, `code`, `name`, `is_active`) rather than a hardcoded code enum.

## Constraints

- Never reassign an existing enum member's integer or string value.
- Do not use native SQL `ENUM` types where frequent addition of new members is expected.
- Do not hardcode magic numbers in application business logic.

## Governance Integration

This Skill supplies reference material (Domain Pattern) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Guidance in this Skill represents Advisory-tier engineering standards for data integrity and API safety grounded in `context/standards/Database Standards.md` and `context/standards/API & Backend Standards.md`.
- **Child Rules:** A repository may declare specific enum naming conventions (e.g. `UPPER_SNAKE_CASE` for members) in `.mentor/rules/`.

## Validation

This Skill is validated during design and review when:
- Enum members have explicit integer assignments.
- DTOs enforce enum validation.
- Schema definitions use standard integer types with mapping comments.
- Code comparisons use typed enum constants exclusively.

## Edge Cases

- **Deprecating Members:** When an enum value is no longer used for new records, mark it as `@deprecated` in code. Do not remove the enum constant if historical database rows still reference it.
- **Shared vs Context-Specific Enums:** If two domains initially share identical values (e.g., `Status`) but diverge in business logic, split them into distinct, domain-specific enums (`InvoiceStatus`, `FulfillmentStatus`) to avoid tight coupling.

## Failure Handling

If historical schema or code displays inconsistent enum values or unmapped integers, report Insufficient Evidence regarding data integrity and recommend a schema audit before extending the enum.

## Expected Output

Reference material. Consuming Review Skills (`database-review`, `api-contract-design`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Explicitly Assigned Enum and DTO Validation
```typescript
// Centralized enum definition with explicit integer values
export enum OrderStatus {
  DRAFT = 1,
  SUBMITTED = 2,
  PROCESSING = 3,
  COMPLETED = 4,
  CANCELLED = 5,
}

// DTO validation using explicit enum type
export class UpdateOrderStatusDto {
  @IsEnum(OrderStatus, { message: 'Invalid order status value' })
  status: OrderStatus;
}
```

### Negative Example: Implicit Ordinals and String Magic Literals
```typescript
// BAD: Reliance on implicit auto-increment values (adding a member in middle shifts values!)
export enum OrderStatus {
  DRAFT,       // 0
  PENDING,     // 1 - inserted later!
  SUBMITTED,   // was 1, now 2!
}

// BAD: Comparing against magic numbers in business logic
if (order.status === 2) {
  // Hard to read, fragile
}
```

## Related Skills

- `skills/database-review/SKILL.md` — Related: Reviews database columns for appropriate data type selection and index strategy for enum columns.
- `skills/api-contract-design/SKILL.md` — Related: Reviews API DTOs and serialization formats for enum fields.
- `skills/validation/SKILL.md` — Related: Defines boundary validation mechanics for incoming API request payloads.
