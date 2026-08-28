---
name: performance-review
description: Investigate and review application performance using evidence rather than assumption — define measurable targets, identify bottlenecks, and verify improvements after the fix. Use when diagnosing a slow endpoint, query, or workflow, or when reviewing a proposed performance optimization.
category: Performance
skillType: Review
---

# Performance Review

## Purpose

Produce an evidence-based diagnosis of a performance problem, or a structured review of a proposed performance optimization, that is grounded in measurement rather than assumption. This Skill exists separately from `skills/database-review/SKILL.md` and `skills/architecture-review/SKILL.md` because those Skills identify *structurally* risky patterns (an N+1 query shape, a scaling ceiling in a design) without measuring anything; this Skill's job starts where a structural risk becomes, or is claimed to become, an actual measured problem — and it insists on a measurable target and post-change verification precisely because "this should be faster" claims, made without measurement, are a common source of wasted optimization effort and regressions elsewhere.

## Scope

**In scope:** defining a measurable performance target for a specific endpoint, query, or workflow; diagnosing the actual bottleneck from evidence (profiling data, timing measurements, query plans) rather than assumption; reviewing a proposed optimization for whether it actually addresses the diagnosed bottleneck; and requiring verification that a change achieved its stated target after the fact.

**Out of scope:** structural performance risk with no measurement yet available (a query pattern that looks like it will scale badly, before any evidence of actual slowness) — that is `skills/database-review/SKILL.md`'s or `skills/architecture-review/SKILL.md`'s structural concern, which this Skill picks up once a concrete measurement exists; and general code correctness unrelated to performance (`skills/code-review/SKILL.md`).

## When to Use

Use when: diagnosing a reported slow endpoint, query, page, or background workflow; reviewing a proposed performance optimization before it's implemented or merged; or verifying whether a performance fix actually achieved its intended effect.

Do not use to speculate about performance with no evidence at all that a problem exists — if the request is "is this query pattern likely to be slow at scale," with no actual measurement, that is a structural question for `skills/database-review/SKILL.md`, not a performance investigation.

## Required Context

- A measurable definition of the problem: what is slow, compared to what target or expectation, and what evidence establishes the current behavior (a timing measurement, a profiling trace, a query execution plan, a monitoring dashboard reading). Without this, the investigation has no baseline to work from.
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack — a recommendation grounded in a different stack's tooling or behavior is not actionable.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context before recommending any stack-specific profiling tool or optimization technique.
2. Establish or confirm a measurable target: what specific metric (latency, throughput, resource usage), measured how, and against what acceptable threshold. If no target is stated and none can be reasonably inferred from the material (e.g. an explicit SLA), proceed to Failure Handling rather than inventing a threshold.
3. Identify the actual bottleneck from evidence provided — profiling data, timing breakdowns, query plans — rather than the most commonly-blamed cause. When the material provides no such evidence, state that the diagnosis is provisional and named explicitly as a hypothesis, not a finding.
4. If reviewing a proposed optimization: assess whether it plausibly addresses the diagnosed bottleneck specifically, not merely whether it is "faster" in general — an optimization that speeds up a part of the system that isn't actually the bottleneck doesn't solve the stated problem.
5. State the verification step required after the change ships: what to re-measure, and what result would confirm the fix worked.

## Rules

### Measurable Targets

A performance review or investigation without a measurable target is incomplete — state one explicitly (a specific latency/throughput/resource number, or an explicit statement that none exists yet and one must be established first) before proceeding to diagnosis.

### Evidence-Based Diagnosis

Diagnose the bottleneck from the evidence actually provided — a profiling trace, timing breakdown, or query plan. When no such evidence exists, say so and frame any bottleneck guess explicitly as an untested hypothesis requiring measurement before acting on it, never as a finding stated with the same confidence as a measured one.

### Optimization Relevance

An optimization must be checked against whether it addresses the *diagnosed* bottleneck, not just whether it's a generally-accepted performance technique — caching a value that isn't actually the slow path doesn't fix a slow endpoint whose actual bottleneck is elsewhere.

### Regression Risk of the Fix Itself

Flag when a proposed optimization introduces its own risk — a cache with no invalidation strategy, a denormalization that risks data drift, an async/background shift that changes the operation's failure semantics (`skills/database-review/SKILL.md`'s data-integrity concerns, or `skills/architecture-review/SKILL.md`'s failure-mode concerns, may also apply — point to them rather than re-deriving that analysis here).

### Post-Change Verification Required

Every accepted optimization requires a stated verification step: what to re-measure, against what target, after the change ships. A performance fix with no verification step is not actually confirmed to work — this Skill requires the step be stated, even when it can't itself execute the re-measurement.

### Child Governance

When context discovery obtained parsed child rules and/or exceptions relevant to performance (e.g. a declared SLA or a resource-usage constraint), apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines — applicability against the rule's own scope text, deterministic classification via `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`).

### Severity, No Fabrication, False-Positive Discipline

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`. Never state a specific percentage or magnitude of improvement that wasn't actually measured — an estimate must be labeled as an estimate, not presented as a measured result (this is the same discipline `skills/documentation/SKILL.md` applies to recording unmeasured performance numbers; this Skill is where that discipline is exercised at the source).

## Constraints

Never approve a performance claim (a reported improvement, a diagnosed bottleneck) that rests on no evidence at all, and never let the pressure to ship a fix quickly substitute for stating a measurable target and a verification step — this Skill's entire value is in refusing to skip that discipline.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and routes any declared performance-related child rule/exception through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) — following `skills/code-review/SKILL.md`'s Child Governance mechanism as the reference implementation. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. Governance classification and finding severity remain independent axes (`docs/Governance Precedence Model.md` Section 12).

## Validation

A review or investigation produced by this Skill is complete when: a measurable target is stated (or its absence is stated explicitly as the finding itself); the diagnosed bottleneck is grounded in stated evidence, with any unevidenced guess labeled as a hypothesis; a proposed optimization is assessed specifically against the diagnosed bottleneck, not performance in general; and a concrete post-change verification step is stated.

## Edge Cases

- **Report of slowness with no measurement at all ("the app feels slow").** State that a measurable baseline is required before diagnosis can proceed, and name what evidence would establish one (timing, profiling, monitoring data) — do not guess at a bottleneck from a subjective report alone.
- **Multiple plausible bottlenecks, evidence doesn't clearly isolate one.** State that the evidence is consistent with more than one cause and name what additional measurement would disambiguate them, rather than picking the most likely-sounding one and presenting it as confirmed.
- **Optimization proposed for a problem that hasn't been measured to actually exist yet (premature optimization).** Flag this directly — the Rules → Measurable Targets requirement applies before an optimization is evaluated, not after.
- **A fix that improves the measured target but degrades a different metric the material also reveals (e.g. lower latency, higher memory).** Report both — a target achieved at an unstated cost elsewhere is not a clean pass.

## Failure Handling

When no measurable target and no baseline evidence exists, and none can be reasonably inferred from the material, state that explicitly as the primary finding rather than proceeding to a diagnosis with no basis. Do not invent a plausible-sounding bottleneck to fill an evidence gap.

## Expected Output

A structured review: Summary, measurable Target (stated or flagged as missing), Findings (each with Severity, Category — Diagnosis/Optimization Relevance/Regression Risk/Governance Conflict —, Location, Problem, Impact, Recommended remediation), Blocking Findings, Non-Blocking Recommendations, and Verification (the specific post-change re-measurement required, and what result would confirm success) — mirroring `skills/code-review/SKILL.md`'s output shape while adding the Target/Verification framing this domain specifically requires.

## Examples

**Positive example.** A reported "checkout is slow" comes with a profiling trace showing 80% of request time in a single synchronous external payment-gateway call. Finding: Diagnosis, evidence-based — the bottleneck is the synchronous external call, not the database queries a first guess might have blamed; recommend either an async confirmation flow or a documented SLA with the gateway provider, and state the specific latency target and re-measurement step required to verify either fix.

**Negative example (correctly declines to flag).** A stakeholder claims a recent change "made things faster" with no before/after measurement provided. Not accepted as a finding or a confirmed improvement — Rules → Severity, No Fabrication requires this be stated as an unverified claim needing a measured baseline and re-measurement, not recorded as a performance win.

## Related Skills

- `skills/context-discovery/SKILL.md` — Dependency: invoked first, every time, to obtain the declared stack before any tool- or technique-specific recommendation.
- `skills/database-review/SKILL.md` — Related: that Skill flags structurally risky query patterns before any measurement exists; this Skill picks up once a concrete measured slowness exists and may hand a diagnosed query-level bottleneck back for a schema/index-level fix, but neither requires the other's output to begin its own review.
- `skills/architecture-review/SKILL.md` — Related: that Skill flags a design's inherent scaling ceiling structurally; this Skill measures actual behavior against a target. Neither depends on the other's output.
- `skills/documentation/SKILL.md` — Related: shares the same discipline against recording an unmeasured number as a measured result, applied in a different domain (documentation of results vs. diagnosis of causes); neither Skill requires the other's output to function.
