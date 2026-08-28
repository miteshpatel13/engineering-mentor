---
name: testing-review
description: Review whether a test suite meaningfully protects behavior and regressions — coverage of edge cases, failure paths, authorization, and concurrency — rather than only measuring line coverage. Use when reviewing new or existing tests for a change, or assessing whether test coverage is adequate before release.
category: Testing
skillType: Review
---

# Testing Review

## Purpose

Produce a structured review of whether a test suite actually protects the behavior it claims to, rather than merely achieving a line-coverage number. This Skill exists separately from `skills/code-review/SKILL.md` because a test suite can be extensive, pass consistently, and still fail to protect against the regressions that matter — a suite testing only the happy path, over-coupled to implementation detail, or silent on authorization and concurrency has a coverage number that overstates its actual protection.

## Scope

**In scope:** whether tests exercise meaningful behavior (not just line coverage); coverage of edge cases, boundary conditions, and failure/error paths; coverage of authorization and access-control scenarios where the code under test is security-sensitive; coverage of concurrency-relevant scenarios where the code under test has concurrent-access risk; test flakiness; and excessive coupling to implementation detail (tests that break on any refactor even when behavior is unchanged).

**Out of scope:** whether the underlying code itself is correct — this Skill reviews whether the *tests* would catch a regression, not whether the code currently has a defect (`skills/code-review/SKILL.md`, `skills/security-review/SKILL.md`, `skills/database-review/SKILL.md` own that); and test infrastructure/tooling choices unrelated to what's actually covered.

## When to Use

Use when: reviewing new or modified tests accompanying a change; assessing whether existing test coverage is adequate before a release; or evaluating whether a reported regression should have been, but wasn't, caught by the existing test suite (and what gap that reveals).

Do not use to write the tests themselves in place of `skills/skill-tester/SKILL.md`'s Skill-fixture-authoring process — that Skill's scope is specifically Mentor Skill test evidence; this Skill reviews application test suites.

## Required Context

- The test suite (or the specific tests) under review, and the code they exercise — a test reviewed with no visibility into what it actually asserts, or what code path it exercises, cannot be assessed for whether it's meaningful.
- The target repository's Normalized Project Context (`skills/context-discovery/SKILL.md`), including its declared stack and testing conventions where stated.

## Workflow

1. Invoke `skills/context-discovery/SKILL.md` to obtain the Normalized Project Context before reasoning about any stack-specific testing convention.
2. Confirm the material provided includes both the tests and enough of the code under test to determine what each test actually exercises and asserts — a test's name or description is not sufficient evidence of what it covers.
3. For each test (or the suite as a whole, when reviewing broadly), evaluate against each Rules category below — what behavior it actually protects, not what its name claims.
4. Identify categories of required coverage (edge cases, failure paths, authorization, concurrency where applicable) that have no corresponding test at all, distinct from categories that have a test but a weak one.
5. When step 1 obtained declared child rules and/or exceptions relevant to required test coverage (e.g. a declared minimum-coverage policy), apply the Child Governance discipline (Rules, below).
6. Produce the review per Expected Output.

## Rules

### Behavioral Coverage, Not Line Coverage

A test that executes a line without asserting anything meaningful about its behavior (a call with no assertion, or an assertion so weak it would pass under most incorrect implementations too) does not actually protect that line, regardless of what a coverage tool reports. Flag tests that inflate line coverage without behavioral protection.

### Edge Cases and Boundary Conditions

Flag missing coverage for boundary values (empty input, maximum size, zero, off-by-one boundaries) and other edge cases the code under test's own logic implies matter (a conditional branch with no test exercising the less common side).

### Failure and Error Paths

Flag a suite that tests only the success path for an operation that has a defined failure mode (an external call that can fail, a validation that can reject, a resource that can be missing) with no test exercising that failure mode's actual handling.

### Authorization Coverage

For security-sensitive code (endpoints, access-control logic), flag missing tests for authorization failure scenarios specifically — a suite that tests successful authorized access but never tests that an unauthorized caller is correctly rejected has not actually protected the authorization boundary. This is a Testing-domain finding about test coverage, distinct from `skills/security-review/SKILL.md`'s finding about whether the authorization logic itself is correct.

### Concurrency Coverage

Where the code under test has a plausible concurrent-access risk (shared mutable state, a read-then-write sequence, a resource with contention), flag the absence of any test exercising concurrent or interleaved access, when the material indicates this risk exists.

### Flakiness

Flag a test whose material shows it depends on timing, unseeded randomness, or external service availability with no isolation — a flaky test that sometimes fails for reasons unrelated to the code under test erodes trust in the whole suite and functionally provides less protection than its presence suggests.

### Implementation Coupling

Flag a test so tightly coupled to internal implementation detail (private method calls, exact internal call counts unrelated to the actual contract) that it would fail on a behavior-preserving refactor — this is a maintainability and false-signal risk distinct from insufficient coverage; a suite can have both problems at once, in different tests.

### Child Governance

When context discovery obtained a declared child rule or exception relevant to required test coverage or a minimum-coverage policy, apply the same discipline `skills/code-review/SKILL.md`'s Child Governance section defines.

### Severity, No Fabrication, False-Positive Discipline

Every finding carries exactly one severity from `context/standards/Severity Taxonomy.md`. Do not claim a test is inadequate without evidence — a test whose assertions aren't visible in the material provided is Insufficient Evidence, not an assumed gap.

## Constraints

Never recommend removing or weakening an existing test merely because it's inconvenient to a change, and never accept "the coverage percentage is high" as a substitute for the behavioral-coverage evaluation this Skill actually performs.

## Governance Integration

Review-type Skill: invokes `skills/context-discovery/SKILL.md` first and routes any declared coverage-policy child rule/exception through `scripts/evaluate_governance.py` (`docs/Governance Evaluation.md`) — following `skills/code-review/SKILL.md`'s Child Governance mechanism as the reference implementation. Every finding is tagged with exactly one level from `context/standards/Severity Taxonomy.md`. Governance classification and finding severity remain independent axes (`docs/Governance Precedence Model.md` Section 12).

## Validation

A review produced by this Skill is complete when: every finding has a severity, a category (Behavioral Coverage, Edge Cases, Failure Paths, Authorization Coverage, Concurrency Coverage, Flakiness, Implementation Coupling, or Governance Conflict), a location, and a stated impact/recommendation; each finding is grounded in what the material actually shows a test asserts (or fails to assert), not in the test's name alone; and coverage claims the material doesn't establish are stated as Insufficient Evidence.

## Edge Cases

- **High line-coverage percentage, but review reveals weak assertions.** Flag this explicitly and directly — Rules → Behavioral Coverage exists precisely for this case; do not let the reported percentage substitute for the actual evaluation.
- **Code with no plausible failure mode (a pure, total function with no external dependency or invalid-input path).** Do not manufacture a failure-path finding where none genuinely applies — state that failure-path coverage isn't applicable for this specific unit.
- **A test suite reviewed with no access to the actual test code, only a coverage report.** State plainly that behavioral adequacy cannot be assessed from a coverage number alone, and that reviewing the actual test code is required — this is the Required Context gap, not a finding about the tests themselves.
- **Tests that are thorough for the happy path of a security-sensitive endpoint but silent on authorization failure.** Flag under Authorization Coverage even though overall coverage may look strong — one dimension being well-covered does not offset another being absent.

## Failure Handling

When the material provides no visibility into what a test actually asserts (only its name, or only a coverage percentage), state that behavioral adequacy cannot be determined and name what's needed (the test code itself) rather than inferring quality from the test's name or from an aggregate coverage number.

## Expected Output

A structured review: Summary, Findings (each with Severity, Category, Location, Problem, Impact, Recommended remediation), a Governance Conflicts subsection when applicable, Blocking Findings, Non-Blocking Recommendations, and Verification (what was checked, what coverage claims couldn't be verified from the material) — mirroring `skills/code-review/SKILL.md`'s output shape.

## Examples

**Positive example.** A password-reset endpoint's test suite covers the successful reset flow in three variations but has no test for an expired or already-used reset token. Finding: Failure Paths, MEDIUM-to-HIGH depending on the endpoint's sensitivity — the suite doesn't protect against a regression that re-enables an expired token; recommend adding a test asserting rejection for both expired and already-used tokens.

**Negative example (correctly declines to flag).** A suite for a pure utility function (no I/O, no external dependency, total over its input domain) has no test for "the network is unavailable." Not flagged — Edge Cases explicitly excludes manufacturing a failure-path finding for a unit with no plausible failure mode.

## Related Skills

- `skills/context-discovery/SKILL.md` — Dependency: invoked first, every time, to obtain declared testing conventions before any stack-specific recommendation.
- `skills/code-review/SKILL.md` — Related: shares the Child Governance mechanism and Expected Output shape; a code review may note thin test coverage as a general observation, but the dedicated behavioral-adequacy evaluation is this Skill's job. Neither requires the other's output.
- `skills/security-review/SKILL.md` — Related: this Skill's Authorization Coverage finding is about whether a test exists proving unauthorized access is rejected; whether the authorization logic itself is actually correct is `security-review`'s finding. The two frequently appear together on the same endpoint but neither depends on the other's output.
- `skills/skill-creator/SKILL.md`, `skills/skill-tester/SKILL.md` — Related, not Dependency: those Skills apply an analogous coverage-category discipline (normal/edge/adversarial/failure/governance-sensitive) to Mentor Skill fixtures specifically, not to application test suites; the underlying discipline rhymes but each operates in its own domain with its own artifacts.
