---
name: api-review
description: Review an existing or proposed API contract for correctness, consistency, and backward compatibility — validation, authorization, response contracts, error semantics, idempotency, versioning, and observability. Use when reviewing an API endpoint or contract before or after implementation for consistency with existing conventions and safe evolution.
category: API
skillType: Review
---

# API Review

## Purpose

Produce a structured, evidence-based review of an existing or already-drafted API contract — endpoint behavior, request/response schemas, validation, error semantics, versioning, and backward compatibility — against the target repository's own established conventions. This Skill exists separately from `skills/api-contract-design/SKILL.md` because reviewing a contract that already exists (or already has a concrete draft) is evaluation against evidence, not the open-ended structural decision-making `api-contract-design` owns; splitting the two keeps this Skill's output a scored, evidence-based review rather than a mix of critique and fresh design recommendation. (This split follows `docs/Skill Ecosystem Inventory.md`'s own recorded finding that the original combined `api-design` Skill mixed two distinct responsibilities under one name.)

## Scope

**In scope:** whether an existing or drafted endpoint's validation, authorization, response contract, error semantics, HTTP method semantics, pagination for collection-returning endpoints, idempotency behavior, versioning approach, and observability are correct and consistent with the target repository's own established API conventions; and whether a proposed change to an existing contract preserves backward compatibility for existing consumers.

**Out of scope:** designing a new API contract's shape from requirements — that is `skills/api-contract-design/SKILL.md`'s authoring workflow, invoked before a contract exists to review; the authorization logic's actual correctness against IDOR/BOLA risk in depth (`skills/security-review/SKILL.md` owns that, though this Skill flags an obviously missing authorization check as a contract-consistency concern); measured endpoint latency (`skills/performance-review/SKILL.md`); whether outbound calls to external dependencies have an appropriate timeout configured — an implementation-level reliability concern owned by `skills/code-review/SKILL.md`'s general reliability review, not a contract-shape concern this Skill evaluates; and confirming a collection endpoint's actual query implementation avoids N+1 database access — owned by `skills/database-review/SKILL.md`'s N+1 Query Risk Rule (this Skill's own Pagination Rule addresses the related but distinct contract-shape question of whether a growing collection is exposed safely at all).

## When to Use

Use when: reviewing an existing API endpoint or contract for correctness and consistency; reviewing a proposed change to an existing contract for backward-compatibility risk; or evaluating a just-drafted new endpoint (produced by `skills/api-contract-design/SKILL.md` or otherwise) against the repository's established conventions before implementation proceeds.

Do not use when no contract exists yet and the actual need is to decide its shape — start with `skills/api-contract-design/SKILL.md`, which may hand its draft to this Skill for review once concrete.

## Required Context

- The API contract under review: endpoint definitions, request/response schemas, or a description of proposed behavior concrete enough to evaluate — a one-line description of "an endpoint that returns users" is not sufficient to review request/response contract details.
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack and, critically, its existing API conventions (naming, versioning scheme, error shape) — an API review that ignores the repository's own established conventions and imposes a generic preference instead is not useful.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context, in particular any existing API conventions the repository has already established.
2. Confirm the material provided is concrete enough to review (Required Context). If it describes intent without a concrete contract, note that a design step (`skills/api-contract-design/SKILL.md`) is the appropriate next step rather than attempting to review something not yet drafted.
3. Evaluate the contract against each Rules category below, checked against the repository's own existing conventions first, and general REST/GraphQL correctness principles second where the repository has no established convention of its own. `context/standards/API & Backend Standards.md` is the grounding checklist the Rules below instantiate.
4. For a change to an existing contract, specifically assess backward compatibility for consumers on the previous contract version.
5. When step 1 obtained declared child rules and/or exceptions, apply the Child Governance discipline (Rules, below).
6. Produce the review per Expected Output.

## Rules

### Validation and Error Semantics

Flag missing or inconsistent request validation, and flag error responses that don't map to the correct HTTP status code for the actual failure (a validation failure returning `200`, or an authorization failure returning `404` when `403` is the repository's established convention, or vice versa — `401` for authentication failures must be distinguished from `403` for authorization failures). Error response structure should be consistent across the API's own existing endpoints; flag a new endpoint that invents a new error shape without justification.

### HTTP Method Semantics

Flag a request that uses an HTTP method inconsistent with the operation it performs, where the repository follows REST conventions: a state-changing operation exposed via `GET` (a safe method, expected to have no side effects and to be safely cacheable/prefetchable); a fully idempotent replace-or-create operation implemented as `POST` where the repository's own convention uses `PUT` for that shape elsewhere; or a partial-update operation that silently overwrites unspecified fields when the repository's established convention for partial updates is `PATCH` with merge semantics. This is distinct from Validation and Error Semantics (above), which governs the *response* side (status codes for outcomes); this Rule governs the *request* side (whether the chosen method matches the operation's actual safety/idempotency/side-effect semantics). Check the repository's own established method conventions first; where none exists, apply general REST method-semantics correctness (`GET`/`HEAD`/`OPTIONS` safe and side-effect-free, `PUT` idempotent full replacement, `PATCH` partial update, `DELETE` idempotent removal, `POST` for non-idempotent creation or an action with no natural HTTP-method mapping).

### Authorization Contract

Flag an endpoint whose contract exposes an operation with no visible authorization check on the specific resource being acted on — this is a contract-consistency finding (the endpoint's shape implies an authorization boundary that isn't evidently enforced); the depth of whether existing authorization logic is itself correct against IDOR/BOLA belongs to `skills/security-review/SKILL.md`.

### Response Contracts and Consistency

Flag a response shape inconsistent with the repository's own established conventions for similar endpoints (naming, pagination shape, nesting depth) without a stated reason for the deviation.

### Pagination

Flag a collection-returning endpoint (a list or search operation) with no pagination mechanism (cursor- or offset-based) where the material shows or implies the collection can grow unbounded — returning an entire unbounded collection in one response risks slow, memory-heavy, or timed-out requests as the underlying data grows. Do not flag a collection endpoint the material shows is inherently small and bounded (e.g. a fixed enumeration) with no pagination — matching the same evidence-based restraint Response Contracts and Consistency (above) already applies; a small, bounded list needs no pagination scaffolding.

### Idempotency

For an operation that should be safely retryable (most `PUT`/`DELETE`, and any `POST` representing a create-if-not-exists intent), flag the absence of an idempotency mechanism (an idempotency key, or a naturally idempotent operation shape) where retries are plausible (e.g. over an unreliable network) and the material shows none exists.

### Versioning and Backward Compatibility

Flag a change to an existing contract that breaks an existing consumer without a versioning strategy to accommodate it (a new required field with no default, a removed field, a changed response type) — evaluated against the repository's own declared versioning approach (`docs/Versioning Strategy.md`'s MAJOR/MINOR/PATCH framing is the general pattern this maps to structurally, applied here to API contracts specifically rather than to Mentor content).

### Documentation and Observability

Flag a contract with no discoverable documentation of its request/response shape (whether that's a schema file, OpenAPI spec, or equivalent the repository actually uses), and flag an endpoint with no observability hook (logging, metrics, tracing) consistent with the repository's existing pattern for comparable endpoints, where the material shows the repository has an established pattern to be consistent with.

### Child Governance

When context discovery obtained parsed child rules and/or exceptions, apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines.

### Severity, No Fabrication, False-Positive Discipline

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`. Do not flag a deviation from a generic REST convention the repository has already deliberately established differently and consistently — check the repository's own pattern first (Rules → Response Contracts).

## Constraints

Never approve a breaking change to an existing contract with no versioning accommodation, and never let convenience (skipping validation, skipping an idempotency mechanism) pass review for an operation where the material shows the risk is real.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and routes child-rule/exception tier and relationship classification through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) — following `skills/code-review/SKILL.md`'s Child Governance mechanism as the reference implementation. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. Governance classification and finding severity remain independent axes (`docs/Governance Precedence Model.md` Section 12).

## Validation

A review produced by this Skill is complete when: every finding has a severity, a category (Validation/Errors, HTTP Method Semantics, Authorization Contract, Response Consistency, Pagination, Idempotency, Versioning/Compatibility, Documentation/Observability, or Governance Conflict), a location, and a stated impact/recommendation; every convention-consistency finding is checked against the repository's own established pattern first; and any claim the material doesn't establish (existing convention, existing consumer's dependency on current shape) is stated as Insufficient Evidence.

## Edge Cases

- **Brand-new API with no existing conventions to be consistent with.** Evaluate against general REST/GraphQL correctness principles instead, and note explicitly that no repository-specific convention exists yet to check against — do not invent one and treat a deviation from it as a finding.
- **A breaking change proposed for an internal-only API with no external consumers.** State this distinction explicitly — the backward-compatibility bar for a genuinely internal-only contract is lower, but only when the material actually establishes there are no external consumers, not assumed.
- **GraphQL contract reviewed with REST-shaped expectations.** Apply GraphQL's own correctness principles (schema evolution via additive fields, deprecation directives) rather than REST-specific versioning expectations that don't map cleanly.

## Failure Handling

When the material describes intent without a concrete contract to evaluate, state that a design step is the appropriate next action rather than attempting a review with nothing concrete to check. When the repository's existing conventions can't be determined from context discovery, state that convention-consistency findings are limited to general correctness principles only.

## Expected Output

A structured review: Summary, Findings (each with Severity, Category, Location, Problem, Impact, Recommended remediation), a Governance Conflicts subsection when applicable, Blocking Findings, Non-Blocking Recommendations, and Verification (what was checked, what existing conventions were or weren't determinable) — mirroring `skills/code-review/SKILL.md`'s output shape.

## Examples

**Positive example.** A proposed change removes a field from an existing, versioned public API response with no deprecation period. Finding: Versioning/Compatibility, HIGH — this breaks existing consumers reading that field with no migration path; recommend deprecating the field for a stated period (or introducing a new API version) before removal.

**Negative example (correctly declines to flag).** A new internal-only endpoint's error responses use a different shape than the repository's public-facing API, but the material shows the repository already maintains two distinct, documented error conventions (internal vs. public). Not flagged — Rules → Response Contracts checks against the repository's own established pattern, and this material shows the "deviation" is itself the established pattern for internal endpoints.

**HTTP Method Semantics example.** A `POST /orders/:id/cancel` endpoint performs a fully idempotent state transition (cancel an order — calling it twice leaves the order in the same cancelled state, no side effect accumulates) but the repository has an established convention of using `PUT` for idempotent state-transition endpoints elsewhere (`PUT /orders/:id/ship`, `PUT /orders/:id/confirm`). Finding: HTTP Method Semantics, LOW — the endpoint's actual behavior is idempotent and safe to retry, but `POST` signals non-idempotent semantics to clients and diverges from this repository's own established `PUT` convention for the same operation shape; recommend `PUT /orders/:id/cancel` for consistency, or explicit documentation of the deviation if `POST` is intentional.

## Related Skills

- `skills/api-contract-design/SKILL.md` — Related: the two Skills split what was originally one Skill along the design/review boundary — this Skill reviews a contract that already exists or is already concretely drafted; `api-contract-design` produces the draft. `api-contract-design` may hand its output to this Skill for review, but neither requires the other's output to function independently (an existing, undocumented API can be reviewed here with no prior design step, and a design can be produced without ever being formally reviewed).
- `skills/context-discovery/SKILL.md` — Dependency: invoked first, every time, to obtain the repository's existing API conventions before any consistency judgment.
- `skills/code-review/SKILL.md` — Related: shares the Child Governance mechanism and Expected Output shape; neither requires the other's output.
- `skills/security-review/SKILL.md` — Related: this Skill flags a contract-level authorization gap (the endpoint's shape implies a check that isn't evidently present); whether existing authorization logic is itself correct in depth, including IDOR/BOLA, is that Skill's concern.
- `skills/database-review/SKILL.md` — Related: this Skill flags a collection endpoint's *contract shape* (e.g. a nested per-item sub-resource with no batching/expansion parameter) as a design concern that makes an N+1 pattern likely; whether the actual query implementation behind it exercises N+1 database access is that Skill's Rules → N+1 Query Risk concern. Neither depends on the other's output.
