---
name: api-contract-design
description: Design a new production API contract from requirements — resource shape, endpoints, request/response schemas, validation rules, versioning approach, and error semantics — before implementation begins. Use when designing new API endpoints from scratch or deciding the contract shape for a new capability, before any code exists to review.
category: API
skillType: Authoring/Workflow
---

# API Contract Design

## Purpose

Produce a concrete, well-reasoned API contract design — resource shape, endpoint set, request/response schemas, validation rules, versioning approach, and error semantics — from a stated requirement, before implementation begins. This Skill exists separately from `skills/api-review/SKILL.md` because designing a contract from an open requirement is a generative, decision-making task with genuine trade-offs to weigh (resource modeling choices, versioning strategy, pagination approach), not an evaluation of something that already exists; collapsing the two under one name previously produced a Skill that mixed authoring and critique in a way neither did well (`docs/Skill Ecosystem Inventory.md`'s recorded finding on the original combined `api-design` Skill).

## Scope

**In scope:** deciding resource modeling and naming for a new capability; designing the endpoint set and its request/response schemas; choosing a validation approach; deciding a versioning strategy appropriate to the contract's expected consumers; and designing error response semantics — all before implementation, working from a stated requirement rather than existing code.

**Out of scope:** reviewing a contract that already exists or is already concretely drafted (`skills/api-review/SKILL.md` — hand a completed draft there once concrete); implementing the endpoint in code; and the deep authorization-logic correctness of whatever access-control approach the design specifies (`skills/security-review/SKILL.md`, once implemented).

## When to Use

Use when: a new capability needs an API contract designed from requirements, with no existing contract to extend; deciding how to shape a new endpoint or set of endpoints before writing any implementation; or resolving a specific open design question (pagination approach, versioning strategy, error schema) for a contract still being drafted.

Do not use once a concrete contract already exists or has already been drafted — that is `skills/api-review/SKILL.md`'s evaluation scope, not this Skill's authoring scope.

## Required Context

- The requirement or capability the new contract needs to serve — what a consumer needs to do, with enough detail to model resources and operations. A requirement stated only as "we need an API for X" with no further detail about the actual operations needed is insufficient to design a concrete contract from (see Failure Handling).
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack and any existing API conventions the new contract should stay consistent with — a new contract designed with no regard for the repository's existing patterns creates unnecessary inconsistency even when each individual decision is independently reasonable.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context, in particular any existing API conventions (naming, versioning scheme, error shape, pagination approach) the new contract should follow for consistency, absent a specific reason to diverge.
2. Confirm the requirement is concrete enough to model — what operations a consumer needs, on what resources, with what access pattern. If not, proceed to Failure Handling rather than inventing operations the requirement didn't actually ask for.
3. Model the resource(s) and the operation set needed to serve the requirement — prefer the smallest contract that actually serves the stated need over speculative completeness (an endpoint added "in case it's needed later" with no current requirement is scope creep, not thoroughness).
4. Design request/response schemas, validation rules, and error semantics for each operation, following the repository's existing conventions where one exists (step 1) and general REST/GraphQL correctness principles where it doesn't.
5. Decide a versioning approach appropriate to the contract's expected consumer stability needs — an internal-only contract with a single consumer under the same team's control can reasonably tolerate a lighter versioning approach than a public contract with third-party consumers; state which applies and why.
6. Present the design with its trade-offs stated explicitly — where more than one reasonable shape exists, name the alternative(s) considered and why the recommended one was chosen, rather than presenting a single option as though no other was possible.

## Rules

### Model From the Actual Requirement

Design only the operations the stated requirement actually calls for. An operation added because it seems likely to be useful later, with no current requirement, is out of scope for this pass — note it as a possible future extension rather than including it in the contract now.

### Consistency With Existing Conventions First

Where the target repository has an established API convention (naming, versioning, error shape, pagination), the new contract should follow it unless there's a stated reason to diverge — divergence should be a deliberate, named decision, not an accidental inconsistency from designing in isolation.

### State Trade-offs, Don't Hide Them

Where a genuine design choice exists with more than one reasonable answer (resource-per-endpoint vs. a single flexible endpoint, offset vs. cursor pagination, embedding vs. linking related resources), name the alternatives considered and the reasoning for the chosen one. Presenting only the chosen option, with no visibility into what was weighed, denies the requester the ability to disagree with a specific trade-off.

### Validation Rules Stated Explicitly

Every field in a designed request schema states its validation rule (required/optional, type, format, bounds) at design time — a schema with unstated validation is not actually a complete contract design, it's a shape with the hard part deferred to implementation.

### Versioning Decided, Not Deferred

A new contract's versioning approach is decided at design time, not left for the first breaking change to force a decision under pressure — state the approach even when the immediate contract has no known future breaking change yet.

### Error Semantics Designed Up Front

Design the error response shape and the status-code mapping for the operation's actual failure modes (validation failure, not-found, authorization failure, conflict) as part of the contract, not left as an implementation afterthought — an incomplete error design is a common source of the exact HTTP-status-code inconsistency `skills/api-review/SKILL.md`'s Validation and Error Semantics rule exists to catch after the fact.

### Child Governance

When context discovery obtained a declared child rule or exception relevant to API design conventions (e.g. a mandated versioning scheme), apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines — a Mentor Mandatory API-design requirement is never silently overridden by a child preference; the conflict is surfaced, not resolved unilaterally by this Skill.

## Constraints

Never design a contract's authorization model in place of `skills/security-review/SKILL.md`'s deeper review once implemented — this Skill designs the contract's *shape* (which operations require which access level, at a design level), it does not itself perform the security-correctness review of the eventual implementation. Never present a single design option as though it were the only reasonable one when a genuine, namable alternative exists.

## Governance Integration

Authoring/Workflow-type Skill, not itself evaluative: invokes `skills/context-discovery/SKILL.md` first for existing convention and any declared child governance context relevant to API design. It does not itself produce Severity-tagged findings against an existing repository's compliance — that is `skills/api-review/SKILL.md`'s role once a contract exists. Where context discovery surfaces a Mentor Mandatory requirement relevant to contract design (e.g. a mandated error-response shape), this Skill follows it directly in the design rather than routing a finding through `scripts/evaluate_governance.py` — there is no existing contract yet to classify a conflict against. A child rule that conflicts with a Mentor Mandatory design requirement is surfaced to the requester as a stated tension in the design output, not silently resolved by picking one side.

## Validation

A design produced by this Skill is complete when: every operation maps to an actual stated requirement, not speculative future need; every request/response schema states its validation rules explicitly; a versioning approach is stated with its reasoning; error semantics are designed for the operation's actual failure modes; and every genuine design trade-off considered is named, with the reasoning for the chosen option stated rather than presented as the only option.

## Edge Cases

- **Requirement specifies operations but not who consumes them (internal-only vs. public).** State this as an open question affecting the versioning-strategy decision (Workflow step 5) rather than guessing; recommend the more conservative (stricter versioning) approach when it can't be determined, since loosening a strict-but-unnecessary approach later is easier than tightening a too-loose one after consumers already depend on it.
- **A requirement that would naturally fit an existing endpoint's extension rather than a new one.** Say so explicitly and recommend extending the existing contract (handing it to `skills/api-review/SKILL.md` for the compatibility check that entails) rather than designing a redundant new endpoint.
- **GraphQL vs. REST not specified by the requirement or the repository's existing convention.** State this as an open decision with its own trade-offs (schema flexibility vs. REST's simpler caching/tooling story) rather than defaulting silently to one without surfacing the choice.

## Failure Handling

When the stated requirement doesn't specify enough about the actual operations needed (what a consumer needs to do, on what resource) to model concretely, state that the requirement needs to be more specific before a contract can be designed, and name what's missing — do not invent plausible-sounding operations to fill the gap, per the Mentor Operating Model's No Invention Rule.

## Expected Output

A design artifact, not a Findings-style review: the proposed resource model, endpoint set with request/response schemas and validation rules, the chosen versioning approach with its reasoning, designed error semantics, and a named list of trade-offs considered with the reasoning for each choice made. State explicitly which parts of the requirement remain open questions the requester needs to resolve before implementation.

## Examples

**Positive example.** Requirement: "consumers need to submit and later check the status of a long-running export job." Design: `POST /exports` (create, returns `202` with a job resource including `id` and `status`), `GET /exports/{id}` (poll status), status enum `queued | running | completed | failed` with a `resultUrl` field populated only when `completed`. Versioning: URL-path versioned (`/v1/exports`) given the requirement implies external consumers. Trade-off named: polling vs. webhook notification considered; polling chosen as the initial design given no requirement yet for push notification, with webhook support noted as a reasonable future extension once a concrete need for it exists.

**Negative example (correctly declines to over-design).** Requirement: "an endpoint to fetch a user's profile." Design does not add speculative endpoints for profile history, profile comparison, or bulk profile export — Rules → Model From the Actual Requirement excludes operations the stated requirement didn't ask for; these are noted as possible future extensions only if the requester raises them.

## Related Skills

- `skills/api-review/SKILL.md` — Related: the two Skills split what was originally one Skill along the design/review boundary — this Skill produces a contract design from requirements; `api-review` evaluates a contract that already exists or is already concretely drafted, including a draft this Skill produces. Neither requires the other's output to function independently.
- `skills/context-discovery/SKILL.md` — Dependency: invoked first, every time, to obtain existing API conventions the new design should stay consistent with absent a stated reason to diverge.
- `skills/architecture-review/SKILL.md` — Related: a new API contract with significant service-boundary implications (a new external-facing service, a major new data-ownership boundary) may warrant that Skill's structural review in addition to this Skill's contract-shape design; neither requires the other's output, and most contract designs have no such implication.
