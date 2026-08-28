---
name: dynamic-form-engine
description: The general engineering pattern for dynamic form architectures — versioned form definitions, field type registries, conditional logic execution, server-side rule evaluation, and hybrid typed submission storage. Reference material consumed by architecture-review and database-review.
category: Domain Patterns
skillType: Domain Pattern
---

# Dynamic Form Engine

## Purpose

Produce the shared, reusable reference pattern for dynamic, metadata-driven form engines. This exists as its own Skill because dynamic form engines represent a platform architecture (`architecture-review`) spanning versioned form definitions, extensible field type registries, client and server-side conditional rule evaluation (`validation`), and hybrid data persistence (`database-review`).

## Scope

**In scope:** dynamic form pipeline architecture (definition $\rightarrow$ versioning $\rightarrow$ registry $\rightarrow$ renderer $\rightarrow$ validation $\rightarrow$ conditional logic $\rightarrow$ submission storage), field type registry patterns, immutable form versioning on lock/publish, server-side conditional rule evaluation, and typed hybrid submission storage (relational + JSON).

**Out of scope:** frontend UI component rendering libraries; specific CSS or drag-and-drop form builder UI implementations. This Skill teaches the backend and domain engine pattern.

## When to Use

Use when:
- Designing a multi-purpose form, survey, questionnaire, or dynamic workflow system.
- Building a field type registry or custom input field extension mechanism.
- Implementing versioning for user-configurable forms to preserve historical submissions.
- Evaluating server-side validation of conditional show/hide or enable/disable rules.
- Designing storage schemas for flexible, user-defined form submission data.

Do not use for static, fixed-schema entities where form fields never change at runtime.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). Core principles (version immutability on submission, field registries over `switch` statements, server-side conditional rule re-evaluation, typed submission storage) apply across relational and document databases and backend stacks.

## Workflow

1. **Decouple Form Purpose from Engine:** Treat the form engine as a generic platform component. Distinguish different forms (e.g. feedback, registration, survey) by purpose metadata rather than separate database tables.
2. **Implement Extensible Field Type Registry:** Define a registry for field types (text, number, select, date, file, rating). Each entry encapsulates rendering metadata, validation rules, value normalization, and serialization logic.
3. **Enforce Version Immutability:** Lock a form version (`IsLocked = true`) upon receiving its first submission. Subsequent modifications create a new `FormVersionNumber + 1` to ensure historical submissions reference an immutable field schema.
4. **Evaluate Conditional Logic Server-Side:** Re-evaluate conditional visibility and enable/disable rules server-side before enforcing mandatory/required field validation.
5. **Persist Submissions with Hybrid Storage:** Use typed columns (`value_text`, `value_number`, `value_date`, `value_json`) in submission value tables, pinned to the exact `FormVersionID` of the submission.

## Rules

### Platform Engine Decoupling

The form engine must remain completely decoupled from specific business domain logic. A single set of core tables (`Form`, `FormVersion`, `FormSection`, `FormField`, `FormFieldOption`, `FormFieldRule`, `FormSubmission`, `FormSubmissionValue`) handles all dynamic form creation and submission regardless of business context.

### Field Registry Pattern over Monolithic Conditional Logic

Field types must be managed via a self-contained registry pattern, not a monolithic `switch` or `if/else` block scattered throughout controllers and services. Adding a new field type requires registering its type metadata, validator, serializer, and value normalizer in the registry without modifying core engine pipeline code.

### Immutable Form Versioning on First Submission

A form version becomes permanently immutable (`IsLocked = true`) as soon as the first submission is recorded against it.
- **Before first submission:** Administrators may edit sections, fields, options, and rules in-place on the unlocked draft version.
- **After first submission:** Any edit creates a new `FormVersion` with an incremented version number.
- **Submission Pinning:** Every `FormSubmission` explicitly references the exact `FormVersionID` rendered to the user, guaranteeing that historical responses remain perfectly readable against their original schema even if later form versions alter or delete fields.

### Server-Side Re-Evaluation of Conditional Rules

The backend validation engine must re-evaluate all conditional logic rules (`EQUALS`, `CONTAINS`, `GREATER_THAN`, `SHOW`, `HIDE`, `REQUIRE`) server-side using submitted payload values. Never trust client-asserted field visibility or required states. Crucially: **a field hidden by active conditional logic must never be validated as required**, even if its base field configuration marks it as mandatory.

### Hybrid Typed Submission Storage

Dynamic submission values must be stored using a hybrid model:
- **Common Fixed Domain Fields:** High-frequency, core entity fields (e.g. customer name, account ID, payment status) should exist as explicit relational columns on parent domain tables.
- **Dynamic Response Values:** Configurable, event-specific dynamic answers are stored in `FormSubmissionValue` rows using strongly typed storage columns (`value_text`, `value_number`, `value_date`, `value_json`) keyed to the specific `FormFieldID`.

## Constraints

- Never modify a form version in-place after submissions have been recorded against it.
- Do not validate mandatory requirements on fields that server-side conditional logic determines to be hidden or disabled.
- Do not use hardcoded `switch` statements across the codebase to handle different field types.

## Governance Integration

This Skill supplies reference material (Domain Pattern) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent Advisory-tier standards for system architecture and data modeling grounded in `context/standards/Architecture Standards.md` and `context/standards/Database Standards.md`.
- **Child Rules:** Projects may specify supported rule operators (e.g. `EQUALS`, `IN`, `GREATER_THAN`) or storage models in `.mentor/rules/`.

## Validation

This Skill is validated during design and review when:
- Form versions lock automatically upon initial submission.
- Dynamic submissions link directly to specific `FormVersionID` records.
- Server-side validation evaluates conditional rules before checking field requirements.
- Field types implement a clean registry pattern.

## Edge Cases

- **Deprecated Fields:** When a new form version removes a field present in prior versions, historical submissions referencing the older version must continue to render the removed field seamlessly.
- **Nested Conditional Rules:** Complex forms with cascading conditional rules (Field C depends on Field B, which depends on Field A) must evaluate dependencies in topological order on the server.

## Failure Handling

When form version IDs or rule schemas are missing from submitted payloads, report Insufficient Evidence and reject the submission with `400 Bad Request`.

## Expected Output

Reference material. Consuming Review Skills (`architecture-review`, `database-review`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Server-Side Conditional Evaluation and Version Pinning
```typescript
// Server-side submission validation pipeline
async validateAndSubmit(versionId: string, responses: Record<string, any>): Promise<FormSubmission> {
  const version = await this.formVersionRepo.findById(versionId);
  
  // 1. Evaluate conditional rules server-side
  const visibleFields = this.ruleEngine.evaluateVisibility(version.rules, responses);

  // 2. Validate visible fields against FieldType registry
  for (const field of version.fields) {
    if (!visibleFields.has(field.id)) {
      delete responses[field.id]; // Strip hidden fields
      continue;
    }

    const fieldTypeImpl = this.fieldTypeRegistry.get(field.type);
    fieldTypeImpl.validate(field, responses[field.id]); // Registry validation
  }

  // 3. Pin submission to immutable version
  return this.submissionRepo.create({ formVersionId: version.id, values: responses });
}
```

### Negative Example: Editing Locked Forms and Trusting Client Visibility
```typescript
// BAD: Modifying form fields in-place on a version with existing submissions!
async updateFormField(versionId: string, fieldId: string, newLabel: string) {
  await this.fieldRepo.update(fieldId, { label: newLabel }); // DEFECT: Corrupts historical submission meaning!
}

// BAD: Validating mandatory status without checking server-side visibility
if (field.isRequired && !responses[field.id]) {
  throw new BadRequestException(`${field.label} is required`); // DEFECT: Fails if field was hidden by conditional logic!
}
```

## Related Skills

- `skills/architecture-review/SKILL.md` — Related: Evaluates platform decoupling, registry architecture, and versioning patterns.
- `skills/database-review/SKILL.md` — Related: Evaluates EAV/JSON hybrid submission storage schemas and foreign key integrity.
- `skills/validation/SKILL.md` — Related: Defines multi-layer structural and business-rule validation mechanics.
