---
name: implementation-plan-review
description: Review a technical implementation plan before tasks are generated or code is written — a Spec Kit plan.md with its design artifacts, an RFC, or any written plan — across architecture, security, performance, database design, API design, maintainability, observability, testing, backward compatibility, migration safety, and deployment risk, and report blocking gaps with canonical severities. Use after /speckit-plan and before /speckit-tasks, or whenever a plan must be approved before implementation starts.
category: Architecture
skillType: Review
---

# Implementation Plan Review

> **Resource paths:** Mentor file paths in this Skill (`context/…`, `docs/…`, `scripts/…`, `skills/…`, `tests/…`) are relative to the Engineering Mentor root, not the repository being worked on; `.mentor/…` paths refer to the target repository. In Claude Code the Mentor root is `${CLAUDE_PLUGIN_ROOT}` — read and run Mentor files from there.

## Purpose

Catch engineering defects in a plan while they are still cheap to fix — before a task list is derived from it and before code exists. A Spec Kit plan is checked by Spec Kit for consistency with its own spec and constitution (`/speckit-analyze`); nothing in that loop checks whether the plan is *well engineered*: whether its migration can run on a live table, whether its API change breaks existing consumers, whether it has an authorization model at all. This Skill is that gate. It is separate from `skills/architecture-review/SKILL.md` because a plan spans every engineering dimension at once, not only structure, and separate from the code-level Review Skills because there is no code yet — findings concern decisions and omissions, not lines.

## Scope

**In scope:** a written implementation plan and its supporting design artifacts — for Spec Kit, `specs/<feature>/plan.md` plus any `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` it produced — evaluated against the feature's spec and the project constitution for these dimensions: architecture, security, performance, database design, API design, maintainability, observability, testing strategy, backward compatibility, migration safety, and deployment/rollback risk.

**Out of scope:** whether the spec's requirements are right (the user and Spec Kit's `/speckit-clarify` own that; `skills/requirements-discipline/SKILL.md` labels them); consistency between spec, plan, and tasks (`/speckit-analyze`); reviewing code (`skills/code-review/SKILL.md` and the domain Review Skills after implementation); designing the API or schema from scratch (`skills/api-contract-design/SKILL.md`); editing the plan — this Skill reports; the plan's author (the user, via `/speckit-plan`) revises.

## When to Use

Use after `/speckit-plan` completes and before `/speckit-tasks`; when a user asks whether a plan, RFC, or design-plus-rollout document is ready to implement; or when `skills/spec-driven-development/SKILL.md` reaches its plan gate.

Do not use for a plan that is a single trivial step, or once code already exists — review the code instead.

## Required Context

Requires repository context to operate correctly (`docs/Skill Standard.md` Section 3, posture 3):

- The plan and its design artifacts. For Spec Kit, locate the active feature from `.specify/feature.json` (or `SPECIFY_FEATURE_DIRECTORY`) and read `plan.md` and its siblings in that `specs/<feature>/` directory.
- The feature's `spec.md`, to check the plan covers its requirements — and nothing is planned that the spec doesn't ask for.
- The project constitution, `.specify/memory/constitution.md`, when present.
- The Normalized Project Context from `skills/context-discovery/SKILL.md`: `stack` and `architecture` to judge the plan against what the repository actually uses, and `childRules` / `exceptions` for Child Governance.
- Codebase context for the areas the plan changes, from `skills/codebase-orientation/SKILL.md` (Graft-backed when available): which modules, APIs, tables, and consumers the plan affects. A plan claim such as "no existing callers" is verified against this, not accepted.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` for the Normalized Project Context.
2. Locate and read the plan, its design artifacts, the spec, and the constitution (Required Context). If there is no plan, stop (Failure Handling).
3. Establish the change's footprint with `skills/codebase-orientation/SKILL.md`: affected modules, public APIs, persisted data, and downstream consumers. Note every plan assertion that the footprint contradicts.
4. Evaluate each dimension in Rules → Review Dimensions. For a dimension the plan doesn't touch, record "not applicable" with the reason rather than silently skipping it.
5. Where a dimension needs depth beyond plan level, apply the owning Review Skill's Rules to the planned design (for example `skills/database-review/SKILL.md` for a planned migration) and cite it; do not restate that Skill's rules here.
6. Apply Child Governance to any discovered child rules or exceptions that bear on the plan, exactly as `skills/code-review/SKILL.md` defines it.
7. Report per Expected Output, with a verdict: **Ready for tasks**, **Ready with non-blocking recommendations**, or **Revise before tasks** (any CRITICAL or HIGH finding).

## Rules

### Review Dimensions

- **Architecture** — boundaries, data ownership, coupling, and failure modes of the planned structure (`skills/architecture-review/SKILL.md`, `context/core/Architecture Principles.md`). Flag a plan that introduces a new service, queue, or data store without stating why the existing structure is insufficient.
- **Security** — trust boundaries, authentication, authorization per operation, input validation, secrets handling, and sensitive-data exposure (`context/standards/Security Standards.md`, `skills/security-review/SKILL.md`). A plan that adds an operation on user-owned data with no stated authorization rule has a gap, not an omission to fill during implementation.
- **Performance** — expected data volumes and request rates, query patterns, N+1 risk, and a measurable target where the spec implies one (`context/standards/Performance Standards.md`, `skills/performance-review/SKILL.md`).
- **Database design** — schema, constraints, indexes for the planned queries, transactions, and concurrency (`context/standards/Database Standards.md`, `skills/database-review/SKILL.md`).
- **API design** — contract shape, error semantics, idempotency for retried or money-moving operations, versioning, and pagination (`context/standards/API & Backend Standards.md`, `skills/api-review/SKILL.md`).
- **Maintainability** — fits existing conventions and module structure; no speculative abstraction the spec doesn't need (`context/core/Engineering Principles.md`).
- **Observability** — logs, metrics, and traces sufficient to tell whether the feature works in production and to diagnose failure, without logging secrets or personal data.
- **Testing** — the plan states how each requirement will be verified, including failure paths, authorization, and concurrency where relevant (`context/standards/Testing Standards.md`, `skills/testing-review/SKILL.md`).
- **Backward compatibility** — effect on existing API consumers, persisted data, events, and configuration; a breaking change states its migration path for consumers.
- **Migration safety** — schema and data migrations are safe on the production data size under live traffic (locking, backfill, `NOT NULL` without default, index builds), reversible or explicitly forward-only, and ordered correctly with the code that depends on them (`context/sop/Database Change SOP.md`).
- **Deployment risk** — rollout order, feature flags where risk warrants them, rollback plan, and dependencies on other deployments (`context/sop/Production Release SOP.md`).

### Plan-Level Evidence

A finding cites the plan section (or the absence of one) and, where codebase context contradicts the plan, the file or module that shows it. Codebase context from Graft or any other tool is evidence to verify, not an authority: when it matters to a finding's severity, confirm it against the source. Never report a risk the plan and codebase context don't support; an under-specified plan section is reported as a gap to specify, not as an invented defect.

### Spec and Constitution Alignment

Flag planned work with no requirement behind it in `spec.md`, and requirements the plan leaves unaddressed. Flag a plan decision that violates a constitution principle — but defer consistency-only checks to `/speckit-analyze` rather than duplicating it. A constitution principle never lowers a Mentor Mandatory requirement (`docs/Governance Precedence Model.md`); where they conflict, report the conflict.

### Child Governance

Apply `skills/code-review/SKILL.md`'s Child Governance discipline unchanged: determine applicability from the rule's own scope text, classify the relationship via `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`), and preserve and report any Prohibited Override of a Mentor Mandatory requirement.

### Severity

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`: CRITICAL, HIGH, MEDIUM, LOW, or INFO. A plan-level gap is rated by the harm it would cause if implemented as written — a planned migration that locks a large live table is HIGH or CRITICAL even though no code exists yet.

## Constraints

Read-only: never edit `plan.md`, `spec.md`, `tasks.md`, the constitution, or any Spec Kit file, and never run Spec Kit phases. Never downgrade a blocking finding because the plan is otherwise good or because revising it delays delivery.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and, wherever a finding is checked against a discovered child rule or exception, routes tier/relationship classification through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) following `skills/code-review/SKILL.md`'s Child Governance mechanism rather than a parallel one. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. Governance classification and finding severity are independent axes (`docs/Governance Precedence Model.md` Section 12). Security and data-integrity requirements it checks are Mentor Mandatory where the cited Standard makes them so; it does not create new Mandatory rules.

## Validation

A review is complete when every Review Dimension is either evaluated or marked not applicable with a reason; every finding has a severity, a dimension, the plan section (or "absent from plan") it concerns, the problem, the impact, and a recommendation; plan assertions that codebase context contradicts are reported; blocking findings (CRITICAL/HIGH) are listed separately; and the verdict follows from the findings.

## Edge Cases

- **Plan with no spec (not Spec Kit).** Review against the stated goal; note that requirement coverage could not be checked.
- **Plan references code that doesn't exist, or ignores code that does.** Report the mismatch as a finding with the codebase evidence; a plan built on a wrong picture of the system is a HIGH risk to everything derived from it.
- **Plan defers a decision ("TBD: auth approach").** An open decision on a security, data-integrity, or migration question is a blocking gap; an open decision on a cosmetic question is not.
- **Very large plan.** Review the dimensions the change actually touches in depth and state which areas received a lighter pass.
- **No Graft context.** Use direct repository inspection via `skills/codebase-orientation/SKILL.md`'s fallback and state the reduced confidence.

## Failure Handling

If no plan exists, say so and point to `/speckit-plan` (or ask for the plan) — do not review a plan inferred from a spec. If the active feature can't be determined, ask which feature directory to review. If context discovery reports `.mentor/` missing or invalid, proceed against durable Mentor standards and say repository-specific conventions were not available; never invent them.

## Expected Output

A structured review following `context/templates/Review Template.md`: Summary with the verdict; Findings (Severity, Dimension, Location — plan section, artifact, or "absent from plan", Problem, Impact, Recommended remediation); a Governance Conflicts subsection when applicable; Blocking Findings; Non-Blocking Recommendations; and Verification — which artifacts were read, which dimensions were not applicable and why, what codebase context was used and whether it was verified, and what could not be checked.

## Examples

**Positive example.** A `plan.md` for customer-level pricing adds `customer_prices(customer_id, sku, price)` and an `ALTER TABLE orders ADD COLUMN price_source TEXT NOT NULL`, lets the client submit `unit_price` on order creation "to support negotiated prices", and has no rollback section. Findings: HIGH, Security — client-supplied price must be recalculated server-side (`skills/payment-integration/SKILL.md`, `context/standards/Security Standards.md`); HIGH, Migration Safety — `NOT NULL` without default or backfill fails on existing orders; MEDIUM, Database Design — no unique constraint on `(customer_id, sku)`; MEDIUM, Deployment Risk — no rollback plan. Verdict: Revise before tasks.

**Negative example (correctly declines to flag).** A plan for an internal admin report reads from existing tables, adds no schema, API, or permission change, and states its test approach. Performance and Migration Safety are marked not applicable with reasons; no finding is manufactured to make the review look thorough. Verdict: Ready for tasks.

## Related Skills

- `skills/spec-driven-development/SKILL.md` — Consumer: invokes this Skill at its plan gate.
- `skills/codebase-orientation/SKILL.md` — Dependency: supplies the change footprint the plan is checked against.
- `skills/context-discovery/SKILL.md` — Dependency: invoked first for the Normalized Project Context.
- `skills/architecture-review/SKILL.md`, `skills/security-review/SKILL.md`, `skills/database-review/SKILL.md`, `skills/api-review/SKILL.md`, `skills/performance-review/SKILL.md`, `skills/testing-review/SKILL.md` — Related: own the depth of each dimension; this Skill applies their Rules at plan level and points to them rather than restating them.
- `skills/code-review/SKILL.md` — Related: shares the Child Governance mechanism and output shape; reviews the code this plan later produces.
- `skills/requirements-discipline/SKILL.md` — Shares a boundary: owns requirement labeling in the spec; this Skill checks the plan against those requirements.
