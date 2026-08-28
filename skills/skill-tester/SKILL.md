---
name: skill-tester
description: The authoritative workflow for testing an Engineering Mentor Skill against docs/Skill Testing Standard.md — designing fixtures across both testing tiers, covering realistic and adversarial scenarios, distinguishing a Skill defect from a fixture defect, and clearing the minimum fixture bar before a Skill can advance to Reviewed. Use when a Skill has completed drafting (skill-creator) and needs test evidence, or when regression-testing a Production Skill after a change.
category: Mentor Core
skillType: Mentor Core
---

# Skill Tester

## Purpose

Produce test evidence for a Skill that is honest about what it does and doesn't prove, sufficient to satisfy `docs/Skill Testing Standard.md`'s minimum fixture bar, and organized so `skills/skill-reviewer/SKILL.md` can score the Test Coverage dimension against real fixtures rather than a claim. This Skill owns **how to test**; it does not own how to create a Skill's content (`skills/skill-creator/SKILL.md`) or how to score/certify it (`skills/skill-reviewer/SKILL.md`).

## Scope

**In scope:**

- Determining which testing tier — deterministic or narrative/regression (`docs/Skill Testing Standard.md` Section 1) — applies to a given Skill or a given claim within it.
- Designing fixtures covering every required scenario category (`docs/Skill Testing Standard.md` Section 2), including the governance-relationship set where applicable.
- Writing fixtures in the repository's existing formats: `tests/schema-tests/skill/<name>.md` + `.expected.json` for deterministic structural checks, `tests/skill-tests/<skill-name>/NN-description.md` for narrative/regression scenarios.
- Executing narrative fixtures (loading the Skill's material into an agent and checking output against pass criteria) and deterministic fixtures (running the relevant `scripts/run_*.py` suite).
- Diagnosing a test failure: distinguishing a genuine Skill defect from a badly-specified fixture.
- Regression discipline when an existing Skill's behavior is found wrong (`docs/Skill Testing Standard.md` Section 4).
- Confirming the minimum fixture bar (`docs/Skill Testing Standard.md` Section 3) is cleared before handing the Skill to `skill-reviewer`.

**Out of scope — explicitly not this Skill's responsibility:**

- **Drafting the Skill's content.** Belongs to `skills/skill-creator/SKILL.md`. This Skill tests what was drafted; it does not rewrite Purpose/Scope/Rules to make testing easier — a Skill that's hard to test because its Rules are vague is a defect reported back to creation/review, not silently patched around here.
- **Quality scoring and certification.** Belongs to `skills/skill-reviewer/SKILL.md` and `docs/Skill Quality Standard.md`. This Skill produces the *evidence* the Test Coverage dimension is scored against; it does not assign that score itself.
- **Building a new automated execution harness.** `tests/skill-tests/code-review/README.md` is explicit that no such harness currently exists in this repository for narrative fixtures — this Skill uses the repository's existing two-tier convention as-is, honestly, rather than inventing a third tier or pretending narrative fixtures are automated assertions.
- **Discovering child-repository context at runtime.** `skills/context-discovery/SKILL.md`'s job; this Skill's fixtures may *describe* discovered context as fixture input (exactly as the code-review governance fixtures do), but this Skill does not run discovery live against a real repository as part of testing a Skill's text.

## When to Use

- A Skill has just been drafted or substantively revised (`skill-creator`'s output) and needs test evidence before entering Review.
- A Production Skill changed and needs regression testing per `docs/Skill Testing Standard.md` Section 4.
- A Skill's behavior was found wrong during real use or audit, and a fixture is needed to pin down and prevent recurrence.
- `skill-reviewer` returns a Skill for more test coverage after finding a gap during Review.

## Required Context

**Context-independent** with respect to any live child repository. This Skill requires the Skill under test (`skills/<name>/SKILL.md`) and its cited material (Standards, SOPs, other Skills it depends on), plus, when adapting the governance-fixture reference set, `tests/skill-tests/code-review/`'s existing fixtures as the shape to follow. Narrative fixtures may themselves *contain*, as fixture input, a described child-repository scenario (a snippet of code, a described `.mentor/` configuration) — that content is fixture material, not live Required Context this Skill discovers itself.

## Workflow

1. **Determine the testing tier(s) that apply.** Per `docs/Skill Testing Standard.md` Section 1: does the Skill wrap a deterministic script or a machine-checkable structural contract (deterministic tier, in addition to any narrative coverage its judgment layer still needs)? Does it require judgment about correctness, severity, or contract satisfaction (narrative/regression tier)? Most Skills beyond pure-reference Domain Pattern content need narrative coverage; a Skill wrapping a script needs both.
2. **Enumerate required scenario categories.** Pull the list directly from the Skill's own `Edge Cases` and `Failure Handling` sections (an edge case or failure mode named in the Skill but not exercised in a fixture is a fixture gap, per `docs/Skill Testing Standard.md` Section 2) plus the fixed category list: happy path, edge cases, invalid input, missing required context, ambiguous requests, conflicting requirements, existing-code/existing-repository scenarios, large inputs, failure scenarios, security-sensitive scenarios where the Skill's category or content touches trust boundaries.
3. **If the Skill is Review-type, or Authoring/Workflow-type and can surface a governance-classified finding:** additionally enumerate the governance-relationship categories `tests/skill-tests/code-review/README.md`'s fixtures 11–26 establish as the reference set (Compatible, Additive, Prohibited Override, scoped-inapplicable, insufficient-evidence, applicable exception, expired/inapplicable exception, Mandatory-downgrade exception attempt, classification-independent-of-severity, and the remaining categories that table names). Adapt them to the new Skill's subject matter — do not invent a different governance category set, and do not skip this step because "the Skill isn't code-review."
4. **Write deterministic fixtures**, where applicable, as `tests/schema-tests/skill/<name>.md` + `<name>.expected.json` (following `tests/schema-tests/skill/valid-full.md`'s exact shape) for the Skill's own structural validity, and confirm `scripts/run_skill_standard_tests.py` picks them up. For a Skill wrapping another deterministic script, confirm that script's own suite (e.g. `scripts/run_context_discovery_tests.py`) still passes — this Skill does not duplicate that suite, only confirms it.
5. **Write narrative/regression fixtures** as `tests/skill-tests/<skill-name>/NN-description.md`, following `tests/skill-tests/code-review/`'s file shape exactly: frontmatter (`id`, `category`, `skill_under_test`), `## Input Material`, `## Pass Criteria`, `## Fail Signals`. Write Pass Criteria and Fail Signals as falsifiable statements about the Skill's expected output — not vague aspirations ("the Skill should be helpful") that no evaluator could actually fail the Skill against.
6. **Execute each fixture.** Deterministic: run the suite script, confirm exit code and reported codes match `.expected.json`. Narrative: load the Skill's material (and everything it cites) as the acting agent's instructions, feed the fixture's Input Material verbatim, check the output against Pass Criteria, specifically watch for Fail Signals — exactly as `tests/skill-tests/code-review/README.md` documents, and with the same honesty about this not being an automated assertion.
7. **On any failure, diagnose before touching anything.** See Rules → Skill Defect vs. Fixture Defect, below.
8. **Confirm the minimum fixture bar** (`docs/Skill Testing Standard.md` Section 3) is cleared: no tier has zero fixtures where a tier is claimed applicable; coverage isn't happy-path-only; a Review-type Skill has the governance-relationship categories if its Governance Integration section claims that posture.
9. **Update the relevant `tests/.../README.md`** (or create one, following `tests/skill-tests/code-review/README.md`'s shape) listing every fixture, its category, and re-run triggers (which source files, when changed, require re-running this fixture set).
10. **Hand off to `skill-reviewer`** with the fixture set complete and passing, and an explicit statement of any category from step 2/3 that was judged not applicable to this specific Skill, and why — never a silent gap.

## Rules

### Skill Defect vs. Fixture Defect

When a fixture fails, determine which of these it is before changing anything — conflating them produces either a weakened Skill or a fixture that no longer tests anything real:

- **Skill defect**: the Skill's actual Rules/Workflow/Constraints, correctly applied, produce the wrong outcome — a missed finding, a false positive, an ambiguous instruction that a careful reader could reasonably follow into the wrong behavior. Fix the Skill; keep the fixture exactly as it was (it caught something real).
- **Fixture defect**: the fixture's Input Material doesn't actually exercise the scenario it claims to, its Pass Criteria are unfalsifiable or contradict the Skill's stated (correct) behavior, or its Fail Signals are testing for something the Skill was never supposed to guarantee. Fix the fixture; do not touch the Skill.
- **Genuinely unclear which**: this is itself a finding — report it rather than guessing. A Skill whose correct behavior is ambiguous enough that a reviewer can't tell whether the Skill or the fixture is wrong has a Clarity problem (`docs/Skill Quality Standard.md`), which belongs in front of `skill-reviewer` explicitly, not resolved unilaterally here.

### Regression Discipline

Follow `docs/Skill Testing Standard.md` Section 4 exactly: when a Skill's behavior is found wrong, write the fixture first, confirm it demonstrates the failure against the *current* Skill text, then fix the Skill, then confirm the fixture now passes. Never fix a Skill's behavior without a fixture that would have caught the regression. A Production Skill's fixture count only grows over time — a fixture is never deleted merely because the Skill was subsequently fixed to pass it.

### Preventing False-Positive Tests

A fixture that always passes regardless of what the Skill actually does is worse than no fixture — it creates false confidence. Before accepting a fixture as complete: could a materially wrong Skill still pass this fixture's Pass Criteria? If yes, tighten the criteria or add a Fail Signal that would catch the specific wrong behavior, the way `tests/skill-tests/code-review/01-clean-authenticated-endpoint.md` explicitly tightens its criteria around a previously-observed miscalibration rather than leaving a vague "looks fine" bar.

### Preventing Prose-Existence Tests

Never write a fixture whose Pass Criteria amounts to "the Skill's output contains section X" or "the Skill's output mentions concept Y" when what actually matters is whether the Skill reached the *correct conclusion*. A fixture tests decision quality and behavior, not the presence of keywords or headings — `scripts/validate_skill.py`'s structural checks already own presence-of-sections; this Skill's fixtures own whether the Skill's judgment was right.

### Not Inventing a New Testing Framework

Use `tests/schema-tests/README.md`'s deterministic format and `tests/skill-tests/code-review/README.md`'s narrative format exactly as they exist. If neither fits a genuinely new kind of claim a Skill makes, report that gap rather than silently building a third, parallel convention — a testing-format decision is a repository-wide one (`docs/Skill Testing Standard.md` Section 1), not a per-Skill one.

## Constraints

- Never mark a Skill's testing as complete while any Section 2/3 required category (per Workflow steps 2–3) is uncovered without an explicit, stated reason it doesn't apply.
- Never claim narrative fixtures are automated, machine-verified assertions — state plainly, in every narrative test suite's README, that they are LLM-judged scenario specifications, per `tests/skill-tests/code-review/README.md`'s own precedent.
- Never delete or weaken an existing regression fixture to make a change pass, without the deliberate, stated Fixture Defect determination above.
- Never test a Skill's live behavior against a real, uninvolved child repository as a substitute for a written fixture — every scenario this Skill certifies as covered must be reproducible from a stored fixture file.

## Governance Integration

Not applicable — this Skill tests other Skills' text and evidence; it does not itself evaluate a child repository's compliance or produce governance-classified findings. Where a fixture under test *is itself* a governance-relationship scenario (step 3), this Skill's job is to confirm the Skill-under-test's Governance Integration behavior matches `docs/Governance Precedence Model.md` and `docs/Governance Evaluation.md` correctly within that fixture — it does not separately classify anything on its own account.

## Validation

Testing is complete when: every category from Workflow steps 2–3 that applies to the Skill under test has at least one fixture; every fixture's Pass Criteria/Fail Signals are falsifiable, per Rules → Preventing False-Positive Tests; deterministic suites (where applicable) pass via their `scripts/run_*.py` runner with exit code 0; the fixture directory has a README listing every fixture and re-run triggers; and `docs/Skill Testing Standard.md` Section 3's minimum bar is met without a stated exception.

## Edge Cases

- **A Skill with no findings and no judgment calls at all** (rare pure-reference Domain Pattern content) — narrative coverage may be minimal; state explicitly which categories were judged not applicable and why, rather than manufacturing fixtures for scenarios the Skill genuinely has none of.
- **A Skill whose correct behavior depends on a live script** (wraps `context-discovery`-shaped tooling) — deterministic coverage of the script is necessary but not sufficient; the Skill's judgment layer (when to invoke it, how to interpret its output, what it does on a reported gap) still needs narrative fixtures, per `docs/Skill Testing Standard.md` Section 1's `context-discovery` worked example.
- **Conflicting Pass Criteria across two fixtures for the same Skill** — this usually indicates the Skill's Rules are themselves ambiguous or contradictory; report it as a Skill defect (likely a Clarity or Correctness gap) rather than editing one fixture to make the conflict disappear.
- **A fixture that only fails intermittently depending on how it's phrased to the evaluating agent** — this is evidence the Skill's instruction is under-specified for that scenario; tighten the Skill's Rules/Workflow rather than tuning fixture wording until it happens to pass.

## Failure Handling

If a Skill under test lacks a `Required Context` or `Failure Handling` section clear enough to derive fixtures from, stop and report that as a defect in the drafted Skill (send back toward `skill-creator`) rather than inventing plausible-sounding scenarios to fill the gap. If it is genuinely unclear whether a failing fixture reveals a Skill defect or a fixture defect after applying Rules → Skill Defect vs. Fixture Defect, report the ambiguity explicitly rather than resolving it by guessing which is more convenient.

## Expected Output

A complete fixture set for the Skill under test: deterministic fixtures under `tests/schema-tests/skill/` where applicable, narrative fixtures under `tests/skill-tests/<skill-name>/` with a README, all passing, covering every required category with an explicit statement of any category ruled not applicable. Where testing surfaced a Skill defect, a specific, actionable description of it (not a vague "something's off") handed back for correction before proceeding.

## Examples

**Worked example.** Testing a newly-drafted Review-type Skill: Workflow step 1 concludes both tiers apply (a deterministic structural check via `scripts/validate_skill.py`, plus narrative coverage of its judgment). Step 3 adapts `tests/skill-tests/code-review/`'s governance fixtures 11–20's categories to the new Skill's domain — e.g. a Prohibited Override fixture where a child rule attempts to downgrade a Mandatory finding this Skill's domain also protects. Step 7: a fixture fails because the Skill correctly flagged the issue, but the fixture's Pass Criteria expected it to stay silent — Rule → Skill Defect vs. Fixture Defect concludes this is a Fixture Defect (the criteria were wrong, not the Skill), and the fixture is corrected, not the Skill.

**Negative example (correctly declined).** A request to "just run the Skill against our actual production repository and see if it looks right" as the entire test plan. Declined: this produces no reusable, stored fixture, doesn't distinguish tiers, and can't be re-run for regression per `docs/Skill Testing Standard.md` Section 4 — the same scenario is instead captured as a written fixture (with the real repository's relevant details generalized into fixture Input Material) so it becomes permanent, reusable test evidence rather than a one-off manual check.

## Related Skills

- `skills/skill-creator/SKILL.md` — Related (not Dependency in the technical sense; this Skill needs *a* drafted Skill to exist to have anything to test, but does not require any specific mechanism from `skill-creator`'s own Workflow to function against a Skill drafted some other way).
- `skills/skill-reviewer/SKILL.md` — **Dependency in reverse**: `skill-reviewer`'s Reviewed stage scores the Test Coverage dimension against this Skill's fixture output (`docs/Skill Taxonomy.md` Section 7's Tested-before-Reviewed ordering) — `skill-reviewer` depends on this Skill's output; this Skill does not depend on anything `skill-reviewer` produces.
- `docs/Skill Testing Standard.md` — the contract this Skill's Workflow directly implements; not restated here beyond what each step needs.
- `tests/skill-tests/code-review/README.md` — the reference example this Skill's narrative fixtures follow the shape of.
