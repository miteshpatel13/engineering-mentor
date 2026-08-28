---
name: architecture-review
description: Review a system or component design against global architecture principles — boundaries, coupling, cohesion, data ownership, and failure modes — while respecting the target repository's existing stack and constraints. Use when evaluating a proposed architecture, reviewing a design document, or assessing whether a change introduces structural risk.
category: Architecture
skillType: Review
---

# Architecture Review

## Purpose

Produce a structured, evidence-based review of a system or component design — a proposed change, an existing subsystem, or a design document (ADR, RFC, diagram) — against durable architecture principles that hold regardless of stack: boundaries, coupling, cohesion, data ownership, and failure modes. This Skill exists separately from `skills/code-review/SKILL.md` because architecture review evaluates structural decisions above the level of an individual diff — a change can be free of code-level defects and still introduce a structural risk (a new circular dependency, a shared-write data-ownership violation, a single point of failure) that only becomes visible when the design is considered as a whole.

## Scope

**In scope:** component/service boundaries, coupling and cohesion, data ownership and consistency boundaries, failure modes and blast radius, scalability implications of the proposed structure, and whether the design is testable in isolation. Applies to a proposed design (before implementation), a design document, or an existing subsystem being assessed for structural risk.

**Out of scope:** line-level code defects, security-specific vulnerability classes (`skills/security-review/SKILL.md`), database schema/query/migration correctness (`skills/database-review/SKILL.md`), measured performance bottlenecks (`skills/performance-review/SKILL.md`), and test-suite adequacy (`skills/testing-review/SKILL.md`) — this Skill notes when a structural decision has implications in one of those domains (e.g. "this boundary places security-sensitive validation in two places") but does not perform that domain's own review.

## When to Use

Use when: evaluating a proposed system or component design before implementation; reviewing an architecture decision record, RFC, or design document; assessing whether a code change introduces a structural risk (new circular dependency, ownership violation, broadened blast radius) beyond what a line-level code review would catch; or deciding between two or more structural approaches to the same problem.

Do not use for a routine code change with no structural implications — that is `skills/code-review/SKILL.md`'s scope.

## Required Context

- The design or change under review: a design document, ADR/RFC text, a diagram, or a description of the proposed or existing structure sufficient to reason about boundaries and data flow. If none of these is available, state that in Failure Handling rather than inferring structure from a partial code excerpt.
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack, existing architecture narrative (`architecture.md`, when present), and any declared child rules/exceptions — an architecture review that ignores what the repository already does risks recommending a pattern the repository has already deliberately rejected.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context before reasoning about any repository-specific structural claim.
2. Identify what is actually under review — a net-new design, a proposed change to an existing structure, or an existing subsystem being assessed — and confirm the material provided is sufficient to reason about boundaries and data flow (Required Context). If not, proceed to Failure Handling rather than inventing missing structure.
3. Evaluate the design against each Rules category below, grounded in what the material actually shows — never against a generic reference architecture that ignores the repository's declared stack and constraints.
4. When step 1 obtained declared child rules and/or exceptions, apply the Child Governance discipline (Rules, below) to any that plausibly bear on architectural boundaries or data ownership.
5. Produce the review per Expected Output, separating structural findings from domain-specific concerns that belong to a sibling Skill (Scope → Out of scope).

## Rules

### Boundaries and Coupling

A boundary (service, module, package) should have a narrow, explicit interface; flag a boundary whose consumers reach past its interface into internal state or implementation detail, and flag coupling that would force two components to change together for unrelated reasons. Prefer the repository's existing boundary conventions over a generic ideal — a monolith with clean internal module boundaries is not automatically wrong for being a monolith.

### Cohesion and Data Ownership

A component should own a coherent set of responsibilities and, for any given piece of data, there should be one component that owns writes to it. Flag a design where two components write the same data through different paths with no reconciliation mechanism, or where a component's responsibilities span unrelated concerns with no shared reason to change together.

### Failure Modes and Blast Radius

Identify what happens when each dependency in the design is unavailable, slow, or returns bad data — a design with no stated failure mode for a critical dependency has not actually addressed failure, whatever its happy-path description says. Flag a design that turns a single component's failure into a wider outage than the component's actual importance justifies (an unbounded blast radius), and flag a design with no isolation between failure domains that should be isolated.

### Scalability Implications

Evaluate whether the proposed structure has an inherent scaling ceiling (a single writer, a synchronous chain with no backpressure, a shared resource with no partitioning strategy) — this is a structural assessment of the design's shape, not a measured performance verdict (`skills/performance-review/SKILL.md` owns measurement).

### Testability

A design whose components cannot be exercised in isolation (hidden global state, an untestable hard dependency with no seam) is a structural finding here, distinct from `skills/testing-review/SKILL.md`'s review of an actual test suite's coverage.

### Child Governance

When context discovery (step 1) obtained parsed child rules and/or exceptions, apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines — determine applicability against the rule's own scope text, classify the relationship deterministically via `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`), and never let a child rule's classification suppress, downgrade, or silently resolve a Mentor Mandatory architectural constraint (a Prohibited Override is preserved and reported, exactly as `skills/code-review/SKILL.md` handles it). This Skill applies that same mechanism to architecture-relevant rules; it does not define a second version of it.

### Severity, No Fabrication, False-Positive Discipline

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`. Never claim a structural risk the material doesn't actually support — an ambiguous diagram that could plausibly represent either a clean or a coupled boundary is Insufficient Evidence (Failure Handling), not a finding either way. Do not report a stylistic architectural preference (e.g. "I would have named this layer differently") as a finding; that is not a structural risk.

## Constraints

Never lower a CRITICAL or HIGH structural finding to make a review look more favorable, and never omit a finding because implementing the fix would be disruptive — this Skill reports risk, it does not weigh delivery cost. Stay within the target repository's actual declared stack and constraints; do not recommend a pattern the repository's own architecture.md or child rules have already deliberately addressed differently, without first checking why.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and, wherever a finding is checked against a discovered child rule or exception, routes tier/relationship classification through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) rather than re-deriving `docs/Governance Precedence Model.md` Section 10's conflict-type table from prose — following `skills/code-review/SKILL.md`'s Child Governance mechanism as the reference implementation, not a parallel one. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. Governance classification and finding severity are independent axes (`docs/Governance Precedence Model.md` Section 12) — a Prohibited Override classification never implies CRITICAL severity by itself, and a Compatible classification never implies INFO by itself.

## Validation

A review produced by this Skill is complete when: every finding has a severity, a category (Boundaries/Coupling, Cohesion/Data Ownership, Failure Modes, Scalability, Testability, or Governance Conflict), a location or explicit statement that location isn't determinable from the material provided, and a stated impact/recommendation; findings that belong to a sibling Skill's domain (security, database, performance, testing specifics) are noted as out-of-scope pointers, not evaluated in depth; and any rule-applicability or relationship classification that couldn't be determined is stated as Insufficient Evidence rather than silently resolved.

## Edge Cases

- **Design document with no diagram, prose only.** Reason from the prose; if the prose doesn't establish clear boundaries or data ownership, state that as Insufficient Evidence rather than inferring a diagram that doesn't exist.
- **Existing subsystem with no original design document.** Reconstruct the boundary/ownership picture from what context discovery and the provided material actually show; do not claim knowledge of intent that was never stated (no invention).
- **A single, small change to an otherwise large existing system.** Scope the review to the actual structural implications of the change — do not perform a full-system architecture review unprompted when only a narrow change was submitted.
- **Two structurally valid approaches, no clearly worse option.** Present both with their trade-offs rather than asserting a single "correct" answer that isn't actually supported by the material.

## Failure Handling

When the material provided is insufficient to determine a boundary, an ownership relationship, or a failure mode (Required Context not met, or the design's actual structure is genuinely ambiguous from what's given), state the gap explicitly and do not proceed to score that aspect — this mirrors the Mentor Operating Model's No Invention Rule. Do not guess at a repository's existing conventions when context discovery reports them undeclared; state that context is missing and evaluate only against durable, stack-agnostic architecture principles.

## Expected Output

A structured review: Summary, Findings (each with Severity, Category, Location or explicit "not determinable," Problem, Impact, Recommended remediation), a Governance Conflicts subsection when Child Governance surfaced a Prohibited Override, Conflict, or rule-applicability Insufficient-Evidence case, Blocking Findings, Non-Blocking Recommendations, and Verification (what was and wasn't checked, including any out-of-scope pointer to a sibling Skill's domain) — mirroring `skills/code-review/SKILL.md`'s output shape for consistency across Review-type Skills.

## Examples

**Positive example.** A design document proposes two services both writing to the same `orders` table directly, with no defined owner. Finding: Cohesion/Data Ownership, HIGH — two independent write paths to the same data with no reconciliation mechanism risks lost updates and inconsistent state; recommend a single owning service with the other consuming via its API or an event.

**Negative example (correctly declines to flag).** A monolithic codebase with clearly separated internal modules, each with a narrow public interface, is not flagged for "not being microservices" — that is a stylistic/architectural-preference judgment this Skill's Rules explicitly exclude (Rules → Severity, No Fabrication), not a structural finding, absent an actual coupling or ownership problem in the material.

## Related Skills

- `skills/context-discovery/SKILL.md` — Dependency: this Skill invokes it first, every time, to obtain the Normalized Project Context before reasoning about any repository-specific structural claim.
- `skills/code-review/SKILL.md` — Related: shares the Child Governance mechanism (this Skill applies the same evaluate_governance.py-routed discipline rather than inventing a parallel one) and the same Expected Output shape, but neither Skill requires the other's specific findings to function — a code review can proceed with no architecture review having occurred, and vice versa.
- `skills/security-review/SKILL.md`, `skills/database-review/SKILL.md`, `skills/performance-review/SKILL.md`, `skills/testing-review/SKILL.md` — Related: each owns a domain this Skill explicitly excludes (Scope → Out of scope) and this Skill points to them rather than evaluating that domain itself; none of these Skills requires this one's output to function.
