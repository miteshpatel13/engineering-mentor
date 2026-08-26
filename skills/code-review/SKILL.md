---
name: code-review
description: Perform a production-grade review of a code change — a diff, pull request, or specific files — using the global Code Review Standard and canonical severity taxonomy, prioritizing correctness, security, and data integrity ahead of style. Use when reviewing a pull request, diff, or code change before merge. Refuses to fabricate a review when insufficient material is provided, and explicitly reconciles project constraints against security/correctness requirements rather than silently dropping either.
---

# Code Review

## Purpose

Review a code change for correctness, security, data integrity, compatibility, performance, reliability, maintainability, and test coverage, and report findings in a consistent, severity-tagged, blocking/non-blocking structure that a maintainer can act on directly.

## Scope

Applies to reviewing an actual code change: a diff, a pull request, a set of modified files, or an explicitly described API/contract change, in any language or stack, in a target repository whose own project-specific conventions and constraints take precedence over generic Mentor guidance per the Mentor Operating Model's conflict priority (explicit user request > security/safety > child repository requirements > Mentor standards > general best practices).

Does not cover: architecture review of a design that hasn't been implemented yet (use `architecture-review`), a standalone security audit not tied to a specific change (use `security-review`), or judging whether a test suite is adequate independent of a specific code change (use `testing-review`) — use those Skills instead of, or alongside, this one.

## Required Context

Before reviewing, confirm there is actual review material: the diff/patch, the specific files, the PR description and link, or an explicit before/after description of an API contract. General discussion of a change, a plan, or a vague description of what someone intends to build is not review material.

**If sufficient material has not been provided, do not invent a review.** Instead:

1. Identify specifically what is missing (e.g. "no diff or file contents were provided — only a description of the change").
2. Explain why it's required — a code review's findings must trace to actual code, not to an assumption about what the code probably does.
3. Ask for the minimum artifact needed to proceed (the diff, the changed files, or a link/paste of the PR).
4. Stop there. Do not produce Findings, severities, or a Blocking/Non-Blocking split against material that doesn't exist. It's fine to note general risk areas worth checking once material is available, but label these explicitly as *things to look for*, never as findings.

When material is partial (e.g. a single function without its callers, or a diff without full file context), review what's provided but say so in Verification (see Expected Output) — do not assume what the missing surrounding code does.

## Workflow

This Skill's methodology is defined once, upstream, and referenced here rather than duplicated:

0. If a child repository root is identifiable for this review, run `context-discovery` (`skills/context-discovery/SKILL.md`) first to obtain the Normalized Project Context. When `.mentor/` context is available and its `project.yaml` is valid, use the declared stack/architecture to adapt generic guidance to the child's actual technology (e.g. Prisma-specific vs. TypeORM-specific remediation) — exactly as this Skill's existing Constraint Handling rule already adapts to a single stated in-request constraint, now extended to structured, persistent child context per `docs/Child Repository Integration.md` Section 13. When no repository root is identifiable (e.g. reviewing a bare diff/snippet), or `.mentor/` isn't configured, or `project.yaml` is invalid, skip straight to step 1 exactly as this Skill already behaves today — do not block or degrade the review on missing/invalid child context, and do not invent stack facts that discovery didn't find. Context discovery never overrides this Skill's own findings or severities (Section 19 remains the unmodified security boundary); it only informs how a finding is phrased or remediated.
1. Follow `context/sop/Code Review SOP.md` for the review process: understand the requirement, inspect the complete change, review in the Standard's priority order, separate blocking from non-blocking, confirm no unrelated changes are included.
2. Apply `context/standards/Code Review Standard.md` for review priority order and finding structure, and `context/standards/Severity Taxonomy.md` for the canonical severity levels and blocking determination.
3. For security-relevant changes, consult `context/checklists/Security Checklist.md` as a verification aid, not a replacement for judgment. For performance-relevant changes, consult `context/checklists/Performance Checklist.md`. For test-adequacy questions, apply `context/standards/Testing Standards.md`.
4. Format the output using `context/templates/Review Template.md`'s structure.
5. Apply Constraint Handling (below) whenever a stated project/user constraint appears to conflict with a finding.

## Rules

### Constraint Handling

When an explicit user or project constraint conflicts with a generic recommendation, do not silently comply and do not silently ignore the constraint. Instead:

1. Respect the legitimate constraint — do not override it unilaterally.
2. Explain the engineering tension between the constraint and the recommendation.
3. Identify the underlying risk the recommendation was addressing.
4. Propose the least-disruptive change that satisfies the constraint while addressing the risk.
5. Never silently drop a security or correctness issue to satisfy a constraint.

Distinguish two categories of constraint:

- **Legitimate implementation constraints** — e.g. "do not change the API contract," "do not add a new dependency," "this must ship without a migration." These bound *how* a fix is implemented. Respect them and design the remediation to fit inside them (step 4 above).
- **Requests to bypass a security or correctness requirement** — e.g. "do not add authorization checks," "skip input validation for this endpoint," "don't worry about that SQL injection, ship it anyway." These are not implementation constraints; they are a request to accept a risk. Do not treat them as permission to omit the finding. Report the finding at its correct severity regardless, state plainly what residual risk the request would leave in place, and require an explicit, informed decision from the requester to accept that risk — do not make that decision on their behalf by staying silent.

### Severity

Every finding uses exactly one severity from `context/standards/Severity Taxonomy.md`: CRITICAL, HIGH, MEDIUM, LOW, or INFO. Never use any other label (no "Major," "Minor," "Blocker," "Required/Optional," or ad hoc terms).

### No Fabrication

Do not invent a file path, line number, or code detail that isn't present in the material provided. If the material doesn't pin down a location, say so explicitly in the finding (e.g. "location not determinable from the diff provided — appears in the request handler based on the described behavior") rather than fabricating a plausible-looking one.

### False-Positive Discipline

Do not report a finding against code that already handles the concern correctly (e.g. don't flag "missing authorization" on an endpoint that has an explicit ownership check, don't flag a query as N+1 when it's already batched, don't flag a parameterized query as injection). When genuinely uncertain whether something is a defect, say so and explain the uncertainty rather than asserting it as a confirmed finding.

### Severity Under Incomplete Surrounding Context

When a concern's real-world impact depends on surrounding behavior that is not visible in the material provided — whether global error-handling middleware exists, whether an upstream caller already validates input, whether a framework version handles a case automatically — classify it using this three-way distinction. Never assume the worst about code you cannot see, and never invent a production failure that hasn't been demonstrated.

- **Missing Evidence** — the material doesn't show the surrounding behavior either way (e.g. no error-handling middleware is visible, but none is shown to be *absent* either — it simply isn't in view). Do not assume the surrounding system has no safeguard. A missing visible `try/catch` alone, with nothing more, is Missing Evidence: if it's worth raising at all, cap it at MEDIUM — never HIGH or CRITICAL — and state explicitly, inside the finding, that the surrounding behavior could not be verified from the material given.
- **Real Defect** — the material itself demonstrates the defect regardless of surrounding context (a raw string-concatenated SQL query, a lookup with no ownership filter, a hardcoded secret, a missing authentication check on an endpoint). Classify these using the full severity range — the Missing Evidence MEDIUM cap does not apply, because there's nothing left to verify: the defect is confirmed by the code in front of you, not contingent on what's outside it.
- **Confirmed High-Impact Failure** — the material provides concrete evidence that a surrounding-context-dependent concern actually causes a production-impacting failure: the diff/PR states a framework/runtime version known to lack default async-error handling, a stack trace or incident description is included, or the surrounding file (also provided) shows no error-handling middleware anywhere in the app. Only then may a concern whose impact depends on surrounding context be classified HIGH or CRITICAL — and the finding must cite the specific evidence that justifies it, not just restate the absence of a visible `try/catch`.

### Severity for Availability / Resource-Exhaustion Findings

Availability and resource-exhaustion concerns — unbounded result sets, missing pagination, unbounded loops/fan-out, missing rate limiting, missing timeouts, and similar — are real findings and must not be dropped, but do not automatically classify one as CRITICAL merely because a query or loop has no limit. The defect itself (e.g. "this query has no `.limit()`") is typically a Real Defect visible in the code, but its severity depends on impact *magnitude*, which is a separate question from whether the defect exists — and magnitude usually depends on production traffic, data volume, and infrastructure-level protections (timeouts, connection-pool limits, existing rate limiting, deployment constraints) that are rarely visible in a diff. Classify using this evidence bar, applying the same "never assume the worst about what you cannot see, never invent an incident that hasn't been demonstrated" discipline as above:

- **Plausible but unquantified risk (MEDIUM — the default)** — the material shows an unbounded query, missing pagination, or similar, but does not establish real-world scale or exploitability: no documented row/request volume, no indication of how exposed or high-traffic the path is, and surrounding limits (timeouts, pool limits, rate limiting, pagination middleware) are unknown. This is the default classification for "found an unbounded query" absent further evidence — state explicitly that scale/exploitability could not be established from the material given.
- **Credible high risk (HIGH)** — the material provides concrete evidence that raises the risk above speculative: the diff/PR/comment documents a specific, realistic large scale (e.g. "can return tens of thousands of rows," a stated production data volume), the endpoint is unauthenticated or otherwise highly exposed rather than gated behind auth, or the material demonstrates substantial amplification (one request fanning out into many expensive downstream calls). Cite the specific evidence in the finding.
- **Confirmed critical availability impact (CRITICAL)** — the material provides concrete evidence of actual, severe, shared-resource impact: a documented production incident or postmortem, a reproducible outage described or demonstrated, explicit evidence that a single request can exhaust a shared critical dependency (e.g. a stated connection-pool collapse affecting all tenants), or an exploit path shown to reliably break core functionality service-wide rather than degrade a single request. A comment merely noting the query is unbounded, with no further evidence of actual outage-level impact, does not meet this bar on its own.

This does not weaken genuine denial-of-service findings: when the material itself demonstrates service-wide memory/CPU exhaustion, a reproducible outage, a shared connection-pool collapse, catastrophic amplification, or other concrete evidence of core-functionality failure, CRITICAL remains available and must be used — cite the evidence.

## Constraints

- Never lower a CRITICAL or HIGH finding's severity to make a review look more favorable, and never omit a finding because it's inconvenient.
- Do not present unrelated refactoring preferences as review findings — style preferences belong at INFO, not higher.
- Stay within the target repository's actual conventions and stack; do not import a generic recommendation that doesn't fit the repository without inspecting it first (per the Mentor Operating Model).

## Validation

A review produced by this Skill is complete when: every finding has a canonical severity, a category, a location (or an explicit statement that location isn't determinable), a problem/impact/remediation; Blocking and Non-Blocking findings are clearly separated per the Severity Taxonomy's default blocking rule; the Verification section states what was and wasn't checked; and no finding references code, a file, or a line that wasn't actually present in the reviewed material.

## Edge Cases

- **Insufficient material** — handled explicitly under Required Context: request the artifact, do not fabricate.
- **Constraint conflicts with a recommendation** — handled explicitly under Constraint Handling.
- **Constraint is actually a request to bypass security/correctness** — report the finding anyway; see Constraint Handling.
- **Clean code with no real defects** — say so plainly in the Summary and produce an empty or near-empty Findings section. Do not manufacture findings to appear thorough.
- **Large diff spanning unrelated concerns** — review what's provided, but flag in Verification if scope appears to mix unrelated changes (per the Code Review SOP's step 10).
- **A finding's severity depends on invisible surrounding context** (e.g. an async handler with no visible error handling and no visible middleware) — handled explicitly under Severity Under Incomplete Surrounding Context: cap at MEDIUM as Missing Evidence unless the material provides concrete evidence of Confirmed High-Impact Failure. Do not default to HIGH/CRITICAL on absence of evidence, and do not suppress the observation entirely — state the uncertainty.
- **An availability/resource-exhaustion finding (unbounded query, missing pagination, unbounded fan-out, etc.)** — handled explicitly under Severity for Availability / Resource-Exhaustion Findings: default to MEDIUM (plausible but unquantified) unless the material documents concrete scale/exposure evidence (HIGH) or concrete evidence of an actual outage/shared-resource collapse (CRITICAL). Do not classify as CRITICAL merely because the query or loop has no limit — cite the specific evidence that justifies going above MEDIUM.
- **No identifiable repository root, or `.mentor/` context missing/invalid** — proceed with the review exactly as this Skill already does without child context: apply generic Mentor standards, note in Verification that repository-specific adaptation wasn't available, and never invent declared stack/architecture facts that context discovery didn't actually find.

## Failure Handling

If the target repository's conventions or constraints are genuinely unknown and material to a finding's severity or remediation, say so explicitly rather than guessing — do not invent repository facts (per the Mentor Operating Model's No Invention Rule).

## Expected Output

A review formatted per `context/templates/Review Template.md`:

```text
## Summary
## Findings          (each: Severity, Category, Location, Problem, Impact, Recommended remediation)
## Blocking Findings
## Non-Blocking Recommendations
## Verification
```

## Examples

- A PR adds a new `/orders/:id` endpoint with no ownership check on `:id` → CRITICAL, Category: Security (BOLA/IDOR), blocking.
- A raw SQL query concatenates a user-supplied string directly into the statement → CRITICAL, Category: Security (Injection), blocking.
- A new N+1 query added on an admin-only, low-traffic report page → MEDIUM, Category: Performance, non-blocking by default.
- User says "don't touch the public API response shape" while a naive fix would change it → respect the constraint; propose an additive/optional field or a versioned endpoint instead (Constraint Handling).
- User says "skip the auth check, we're behind a VPN" on a CRITICAL authorization gap → still report it as CRITICAL and blocking; explain that VPN access is not per-user authorization, and require an explicit accept-risk decision rather than silently complying.
- An async route handler has no visible `try/catch` and no surrounding middleware is shown in the material → Missing Evidence: MEDIUM at most, non-blocking, with the uncertainty ("surrounding error-handling middleware not visible in the material provided") stated explicitly in the finding — never HIGH, and never silently omitted either.
- The same missing-`try/catch` pattern, but the material also includes the app's bootstrap file showing no global error-handling middleware is registered anywhere → Confirmed High-Impact Failure: HIGH is justified, and the finding must cite the bootstrap file as the evidence.
- An endpoint runs an unbounded query with no documented scale or exposure evidence (e.g. "no `.limit()`, no pagination," nothing more) → Plausible but unquantified risk: MEDIUM by default, non-blocking by default, with the uncertainty about real-world scale/exploitability stated explicitly — not CRITICAL merely because the query is unbounded.
- The same unbounded query, but a comment/PR description documents a concrete realistic scale (e.g. "can return tens of thousands of rows for a single user") → Credible high risk: HIGH is justified, citing the documented scale as the evidence — still not CRITICAL without evidence of an actual outage or shared-resource collapse.
- The same unbounded query, but the material also includes evidence of an actual production incident or a demonstrated shared connection-pool collapse caused by it → Confirmed critical availability impact: CRITICAL is justified, citing the incident/collapse evidence.
