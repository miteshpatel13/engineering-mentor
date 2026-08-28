---
name: documentation
description: A general-purpose discipline for writing and maintaining technical documentation that represents actual implementation rather than plan or invention — labeling every claim Implemented, Planned, Recommended, or TBD, verifying claims against real code, and keeping documentation synchronized with the system it describes. Use when writing or updating any architecture, API, database, testing, performance, security, or operational document.
category: Documentation
skillType: Authoring/Workflow
---

# Documentation

## Purpose

Documentation that describes the original plan instead of what was actually built is worse than no documentation — it actively misleads a reader who trusts it. This Skill generalizes a project's documentation-labeling discipline (`technical-documentation`, in the audited `mentor-skills-source` collection) into reusable Mentor content: every project-specific area list and domain reference has been stripped out, keeping the labeling scheme, the verify-against-code rule, and the update-in-the-same-change discipline that made the source material trustworthy. This Skill is deliberately broad — general documentation discipline, not an API-only or OpenAPI-specific one; OpenAPI/Swagger-specific contract depth belongs to a future `api-contract-design` Skill, not here.

## Scope

**In scope:**

- Labeling every non-obvious documented claim as Implemented, Planned, Recommended, or TBD.
- Verifying documented claims against the actual current implementation before writing them, not against the original ticket, design doc, or memory.
- Documenting decisions, constraints, and assumptions in a way a later reader can act on without guessing.
- Choosing to update an existing document over forking a new one on the same subject.
- Keeping documentation and implementation synchronized — updated in the same change, not as separate follow-up work that may never happen.
- Recording only actually-measured results for anything empirical (a performance number, a test result, a security-scan finding) — never a projection presented as a measurement.

**Out of scope — explicitly not this Skill's responsibility:**

- **Deciding what the requirements are**, or classifying requirement confidence (CONFIRMED/RECOMMENDATION/ASSUMPTION) — that discipline belongs to `skills/requirements-discipline/SKILL.md`; this Skill documents outcomes and states, informed by that classification where it exists, but doesn't perform it.
- **OpenAPI/Swagger-specific contract depth** — per-endpoint schema, validation-rule documentation generated from DTO decorators, and API-contract authoring belong to a future `api-contract-design` Skill (`docs/Skill Migration & Expansion Plan.md` row 14). This Skill's API-related guidance stays at the level of "document why an endpoint exists and what business flow it serves" — the prose context a contract-generation tool can't produce on its own.
- **Producing the artifact being documented.** This Skill documents architecture, code, tests, or infrastructure that exists or is planned; it does not design that architecture or write that code itself.
- **Evaluating whether documented code is itself correct.** That's a Review-type Skill's job (`code-review`, `security-review`, etc.); this Skill's job is accurate representation of what exists, not judgment of whether what exists is good.

## When to Use

- Writing or updating any architecture, API, database, testing, performance, security, or operational document.
- Recording the results of an executed test run, benchmark, or security assessment.
- Deciding whether to update an existing document or start a new one for a given subject.
- A prior document is discovered to no longer match the implementation it describes.

## Required Context

**Benefits from repository/project context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3, posture 2). Richer with access to the actual codebase, test results, and any existing documentation and decision log for the project being documented (`skills/requirements-discipline/SKILL.md`'s output, where it exists). Still applicable in the abstract — the labeling and verification discipline holds regardless of what's being documented.

## Workflow

1. **Check for an existing document or Skill covering the same subject.** Extend it rather than producing a second, potentially-drifting source on the same subject — this mirrors the don't-duplicate discipline `docs/Skill Taxonomy.md` Section 5 applies to Skills themselves, applied here to project documentation.
2. **Verify every factual claim against the actual current implementation** — read the real code, run the real test, check the real configuration — not the ticket that requested it, the original design doc, or memory of how it was supposed to work. A documented behavior that only matches the original spec, and not what actually shipped (including any deviation), is a documentation bug, not an acceptable simplification.
3. **Label every non-obvious claim explicitly:**
   - **Implemented** — exists in the codebase right now, verified by reading the actual code or running the actual test, not assumed from a plan.
   - **Planned** — scoped and intended, not yet built. State this plainly rather than describing it as if it already exists.
   - **Recommended** — a suggested approach or decision not yet confirmed by whoever owns the decision (mirrors `skills/requirements-discipline/SKILL.md`'s RECOMMENDATION label).
   - **TBD** — genuinely undecided, blocked on a decision or further information (mirrors `skills/requirements-discipline/SKILL.md`'s ASSUMPTION and open-point handling).
4. **For empirical claims specifically** (performance numbers, security findings, load-test results), record only what was actually measured or found by an actually-executed run — never a projected or estimated number presented without that caveat. If no measurement exists yet, label the claim Planned or TBD rather than inventing a plausible-sounding number.
5. **Document decisions, constraints, and assumptions explicitly**, cross-referencing `skills/requirements-discipline/SKILL.md`'s decision log where one exists for the project, rather than re-deriving or restating requirement-confidence classification independently inside the documentation itself.
6. **Include concrete examples** wherever a described behavior isn't self-evident from a one-line description — an example grounded in the actual implementation, not a hypothetical that doesn't match what the code does.
7. **Update the document in the same change that changes the implementation it describes.** Documentation updated as separate, later, optional follow-up work is documentation that will drift — treat the update as part of the definition of done for the implementation change, not an afterthought.
8. **Before finishing, re-scan for stale claims**: does anything in the document describe the pre-change state, a status that's since changed (Planned → Implemented, TBD → confirmed), or a number from before the most recent measurement? Update or explicitly supersede it.

## Rules

### Never Invent

Never document an API, table, field, relationship, performance number, or security result that doesn't exist or wasn't measured. If something isn't built yet, label it Planned or TBD explicitly — never described as if it exists because that's what was originally scoped. This is the Mentor Operating Model's No Invention Rule applied specifically to documentation content.

### Labeling Is Not Optional for Non-Obvious Claims

A document that doesn't distinguish Implemented from Planned from Recommended from TBD is not acceptable documentation under this Skill's discipline — a reader must never have to guess whether a described feature actually exists. Self-evident claims (documenting that a function named `calculateTotal` calculates a total) don't need a label; anything a reader could reasonably mistake for settled fact when it isn't does.

### Verify Against Code, Not Against the Plan

The plan and the implementation diverge over time, in every real project. Documentation that was accurate when written and never re-verified against the current code is documentation that silently becomes wrong. This Skill's verification step (Workflow step 2) is not a one-time act performed only when a document is first written — it is repeated every time the document is revisited.

### Prefer Extending Over Forking

Before creating a new document, actively look for an existing one on the same subject — a project's existing architecture doc, a Skill's own material, a prior technical document. Two documents that could drift apart on the same subject are strictly worse than one that's occasionally out of date, because a reader has no way to know which of the two to trust.

### Documentation Ships With the Change, Not After It

A documentation update that's deferred to "a follow-up ticket" after the implementation ships is, in practice, often never written — this Skill treats the documentation update as part of the same change as the implementation it describes, the same discipline `swagger-openapi`-shaped source material states for API contracts specifically ("Swagger is not a nice-to-have generated afterward — it's part of the definition of done"), generalized here to documentation of any kind.

## Constraints

- Never document a feature, field, endpoint, or capability that doesn't exist in the current implementation as if it does.
- Never record a performance, load, or security-testing number that wasn't actually produced by an executed run.
- Never let a document silently continue describing pre-change behavior after the change ships.
- Never fork a new document covering the same subject as an existing one without first checking for and considering extending the existing one.

## Governance Integration

Not applicable in the Mentor-Mandatory sense — this Skill is a documentation-writing discipline; it does not itself state or enforce a Mentor Mandatory/Configurable/Advisory/Informational rule against child-repository code, and does not invoke `scripts/evaluate_governance.py`. Where this Skill is used to document a security- or compliance-sensitive area, the underlying facts being documented (e.g. what authentication mechanism is actually implemented) still carry whatever governance tier the relevant Standard assigns them — this Skill's Implemented/Planned/Recommended/TBD label is a factual-status classification, not a substitute for that tier, and never overrides or downgrades it.

## Validation

Documentation produced under this Skill is complete and correct when: every non-obvious claim carries an explicit status label; every Implemented claim was verified against actual current code, configuration, or test results, not assumed; every empirical claim (performance, security, load) traces to an actually-executed run; the document was checked against — and updates — any existing document on the same subject rather than forking a duplicate; and the document was updated in the same change as the implementation it describes, not deferred.

## Edge Cases

- **A feature that's partially implemented** (some cases handled, others not) — do not label the whole feature Implemented; document exactly what's covered and what isn't, or split the claim into per-case labels.
- **A number that was measured once, a while ago, and the system has changed since** — treat it as stale, not current; re-measure before restating it as current Implemented fact, or explicitly date it and note it may no longer reflect the current system.
- **Documentation requested for a system with no existing documentation or decision log at all** — start one; this Skill applies from a blank slate exactly as it does when extending an existing document, using the same labeling discipline from the first entry.
- **A stakeholder asks for documentation of a "planned" feature written as if it were already available**, for external-facing purposes — decline to misrepresent it; if external communication genuinely needs to describe planned capability, that's a distinct product/marketing artifact, not this Skill's technical documentation output, and the two should not be conflated into one document.
- **Conflicting documentation exists** (two documents describe the same subject differently) — this is itself a finding to surface, not something to silently resolve by picking one; determine which (if either) matches actual current implementation, and consolidate or flag the discrepancy explicitly.

## Failure Handling

If a claim can't be verified against actual code, configuration, or a real test result — access to the implementation isn't available, or the behavior is genuinely ambiguous even after reading the code — do not document it as Implemented. Label it TBD, state what verification is missing, and stop rather than writing a plausible-sounding but unverified claim. If two existing documents on the same subject conflict and it's unclear which (if either) is current, report the conflict explicitly rather than silently merging or picking one.

## Expected Output

A new or updated technical document (architecture, API-context, database, testing, performance, security, or operational) with every non-obvious claim labeled Implemented/Planned/Recommended/TBD, verified against actual current implementation, cross-referencing the relevant decision log where one exists, and updated in the same change as the implementation it describes.

## Examples

**Worked example.** Documenting a newly-built notification feature: the email channel is fully implemented and tested; the SMS channel's code exists but its provider credentials are still pending, so no message has ever actually sent. Applying this Skill: email is labeled Implemented (verified by an actually-executed test); SMS is labeled Planned or TBD (code exists but nothing verifiably works end-to-end yet) — not both described identically as "the system supports email and SMS notifications," which would misrepresent the SMS channel's actual current state.

**Negative example (correctly declined).** Asked to document a performance benchmark "based on what we'd expect given the architecture" because no load test has actually been run yet. Declined: this Skill never records a performance number that wasn't measured by an actually-executed run — the document instead states plainly that no load test has been performed yet (TBD), rather than presenting an estimate as if it were a measured result.

## Related Skills

- `skills/requirements-discipline/SKILL.md` — Related: this Skill's Implemented/Planned/Recommended/TBD labels mirror `requirements-discipline`'s CONFIRMED/RECOMMENDATION/ASSUMPTION labels and this Skill cross-references its decision log where one exists, but neither Skill requires the other's specific output to function on its own — a project may have documentation with no formal decision log, or vice versa.
