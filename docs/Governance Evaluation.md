# Governance Evaluation

## Status

Authoritative for the scope defined below. This document specifies `scripts/evaluate_governance.py`: a reusable, deterministic capability that classifies the relationship between a child requirement (a `.mentor/rules/` entry or a `.mentor/exceptions.yaml` entry) and a Mentor governance requirement, per `docs/Governance Precedence Model.md` Sections 3–11. It is the first executable implementation of that document's Section 10 (Conflict Types) and Section 11 (Conflict Resolution — Future Behavior), which until this phase were documentation-only.

This document does not restate `docs/Governance Precedence Model.md`'s precedence order, its worked examples, or its rationale — that document remains the single specification for *what the rules of precedence are*. This document specifies *what the script that applies those rules mechanically consumes, returns, and deliberately leaves alone*.

## Purpose

`skills/code-review/SKILL.md`'s Child Governance rules (added when Code Review became this repository's first reference implementation of child governance) determine, by LLM judgment against the actual diff under review, whether a child rule applies and how it relates to a Mentor requirement — then classify that relationship into one of Section 10's six categories, entirely through narrative reasoning re-derived from `docs/Governance Precedence Model.md`'s prose on every review.

The classification step is not, in fact, a judgment call. Given a Mentor-side tier, a child-side tier, and an already-determined relationship (does the child rule narrow the Mentor requirement, replace it, disagree with it, assert it's exempt, or is it unrelated), the resulting conflict type and expected handling are a fixed function of the Governance Precedence Model — the same two tiers and the same relationship always produce the same classification. Re-deriving that function from prose, per review, per Skill, is unnecessary and drift-prone: two Skills (or two runs of the same Skill) could reach different classifications for the same inputs, and there is no way to unit-test prose-based reasoning deterministically.

`evaluate_governance.py` extracts exactly that fixed function into code, once, so every Skill that adopts it gets identical, testable classification behavior — while leaving every judgment call that genuinely requires reading the actual code or rule text where it already lives: in the Skill.

## What Governance Evaluation Owns

- Deterministic classification of a rule-vs-Mentor-requirement relationship into one of Section 10's categories (Compatible, Additive, Override, Conflict, Prohibited Override, Unknown) plus the corresponding Section 11 expected handling, given tiers and a relationship as input.
- The exception-specific counterpart (an exception is not a governance tier — Section 9 — so it is evaluated separately): whether a specific exception is a legitimate, bounded deviation; inactive (`status` is `rejected`/`expired` — checked first, before tier, since an inactive exception is not a live override attempt regardless of what it targets); a Prohibited Override (an *active* exception — `status: requested` or `approved` — that targets a Mentor Mandatory/security-safety/Mentor-Configurable-boundary requirement, regardless of which of those two active statuses it has); or of unknown applicability.
- Assembling the discovered/validated child rules and exceptions for a repository into a small catalog (id, tier, scope, status, validity), by calling `discover_project_context.discover()`, `validate_child_rule.validate_rules_dir()`, and `validate_exceptions_yaml.validate_file()` directly — never re-parsing `.mentor/` content itself.
- A single normalized result shape (`GovernanceEvaluationResult` — see below) a calling Skill can consume without re-deriving classification logic.
- Read-only evaluation. No file writes (aside from stdout), no modification of a child repository, `.mentor/`, or Mentor's own governance; no exception creation or approval.

## What Governance Evaluation Does Not Own

- **Whether a child rule's declared `scope` actually covers the specific diff/file under review.** Free-text scope-to-code matching requires reading the actual code under review, which this script never receives. `docs/Child Rules and Exceptions.md` Section 6 explicitly defers "exact scope-matching semantics" as future work; this script does not invent that matching now. That determination (**applicability**) is supplied by the caller as input.
- **What relationship a specific child rule bears to a specific Mentor requirement** — narrows it, replaces it, disagrees with it, asserts it's exempt, or is unrelated to it. Determining this requires reading the rule's text and the Mentor requirement's text together and forming a judgment; it is exactly the kind of narrative determination `skills/code-review/SKILL.md`'s Child Governance rules already make. This script takes that judgment as input (via `--assertions`) and classifies its *consequence* — it does not form the judgment itself.
- **Finding severity.** Severity is, and remains, entirely the calling Skill's responsibility, governed solely by `context/standards/Severity Taxonomy.md` (see `docs/Governance Precedence Model.md` Section 12, unchanged by this phase). No key in this script's output is named `severity`, and none should be added.
- **Whether a finding is suppressed, downgraded, or omitted because an applicable exception exists.** Per `docs/Governance Precedence Model.md` Section 13, that decision (annotate vs. suppress) is deferred, unimplemented, and — when it is implemented — remains a Skill/finding-output concern, not a governance-evaluation concern. `evaluate_exception_relationship()` reports `exception_applicable`; it never suppresses anything.
- **Parsing `.mentor/project.yaml`, `.mentor/rules/`, or `.mentor/exceptions.yaml`.** Those artifacts have exactly one authoritative parser/validator each, already built (`discover_project_context.py`, `validate_child_rule.py`, `validate_exceptions_yaml.py`). This script consumes their output; it does not duplicate their parsing.
- **A second precedence hierarchy.** `TIER_RANKS` in `evaluate_governance.py` is a literal, code-form restatement of `docs/Governance Precedence Model.md` Section 4's ordering, referenced by section number in the script's own comments — not an independently-derived ranking. If the Governance Precedence Model's order ever changes, this constant is what must change to match it; there is no second copy of the order anywhere else in code.

## Relationship with Context Discovery

Governance Evaluation is a consumer of Context Discovery, never a second discovery mechanism. `docs/Context Discovery.md` already establishes that Context Discovery "does not parse rule *content*... does not evaluate exceptions... [and] does not implement governance precedence" (Context Discovery.md, "What Context Discovery Does Not Own") — Governance Evaluation is the layer that picks up exactly where that boundary was left: it takes the *structural* catalog Context Discovery and the two validators already produce (which rules/exceptions exist, whether each is well-formed, its declared tier and scope) and applies precedence classification on top, without re-parsing anything.

In convenience mode (`python3 scripts/evaluate_governance.py <repo-root> --assertions <file> --json`), `evaluate_governance.py` calls `discover_project_context.discover()`, `validate_child_rule.validate_rules_dir()`, and `validate_exceptions_yaml.validate_file()` as direct Python function calls — the same functions Context Discovery and the two validators already expose, imported rather than reimplemented. Composed mode (`--context/--rules/--exceptions/--assertions`) accepts their JSON output directly, for testing or when that output is already on hand.

## Relationship with Skills

`skills/code-review/SKILL.md`'s Child Governance rules retain full ownership of: determining whether a discovered child rule's scope covers the material under review (**applicability**); determining what relationship a specific rule bears to a specific Mentor requirement (**relationship**) by reading the rule and the code together; gathering evidence; writing findings; and assigning severity. Code Review supplies those two judgments to `evaluate_governance.py` as `--assertions` input and consumes the returned classification/handling instead of re-deriving Section 10's category table from prose. See `skills/code-review/SKILL.md`'s Child Governance rules for exactly how the two responsibilities divide in that Skill.

No other Skill was integrated with Governance Evaluation in this phase (`security-review`, `architecture-review`, `database-review`, `testing-review`, `performance-review`, `api-design` are unchanged) — this phase's scope is establishing the reusable layer and proving it against the one existing reference implementation, not a repository-wide rollout.

**Update (later retrofit phase, reconciled in Phase 13 of the independent-certification-pilot follow-up work):** the paragraph above is an accurate historical record of *this document's own originating phase* and is left unchanged as that record. It no longer describes the current state. In a later phase, `security-review`, `database-review`, `api-review`, `architecture-review`, `performance-review`, and `testing-review` (the successor to `api-design`, per `docs/Skill Ecosystem Inventory.md`'s recorded design/review split) were each given a Workflow step invoking `context-discovery`, a Child Governance Rules subsection delegating to `skills/code-review/SKILL.md`'s Child Governance mechanism (the same mechanism this document specifies), and a `## Governance Integration` section stating that posture. `docs/Child Repository Integration.md` Section 22 carried the same now-corrected staleness and was updated in the same Phase 13 pass. This means the `evaluate_governance.py` classification function this document specifies is, as of that later phase, invoked (by delegation, via the reference implementation) from seven Skills' worth of narrative Workflow instructions, not one — though whether each Skill's delegation actually produces correct classification at run time remains unconfirmed Tier D/E evidence (no execution harness exists in this repository as of Phase 13 either) — see `docs/Independent Certification Report.md`.

## Relationship with Severity Taxonomy

None, by design. `context/standards/Severity Taxonomy.md` is untouched by this phase and is not consulted by `evaluate_governance.py`. Governance classification (this document) and finding severity (Severity Taxonomy) are, per `docs/Governance Precedence Model.md` Section 12, two independent dimensions; a Prohibited Override classification does not imply CRITICAL, and a Compatible classification does not imply INFO. The calling Skill computes severity the normal, evidence-based way regardless of what this script returns.

## Inputs

**`--assertions` (always required)** — the caller-supplied judgment layer, JSON:

```json
{
  "requirements": [
    {
      "ruleId": "<a discovered child rule's id>",
      "mentorRequirementTier": "security_safety | mentor_mandatory | mentor_configurable_boundary | mentor_advisory | informational",
      "mentorRequirementDescription": "<free text, carried through for reporting only>",
      "applicability": "applies | not_applicable | unknown",
      "relationship": "unrelated | narrows | replaces | disagrees | asserts_exempt | unknown"
    }
  ],
  "exceptions": [
    {
      "exceptionId": "<a discovered exception's id>",
      "targetRuleTier": "<same vocabulary as mentorRequirementTier, or a child tier (e.g. child_configurable) if the exception targets a child rule rather than a Mentor requirement>",
      "targetRuleDescription": "<free text, for reporting only>",
      "applicability": "applies | not_applicable | unknown"
    }
  ]
}
```

An entry whose `ruleId`/`exceptionId` does not match anything in the discovered/validated catalog, or whose `applicability`/`relationship` value is outside the enumerated vocabulary, is reported as its own warning and otherwise ignored — this script never evaluates a rule/exception that discovery/validation didn't actually find, and never guesses at a malformed assertion.

**Convenience mode**: `<repo-root>` — a child repository root; discovery and validation run internally.

**Composed mode**: `--context` (Context Discovery's own output shape, or any subset with `mentorConfigured`/`projectProfile`/`childRules`/`exceptions`), `--rules` (`validate_child_rule.py --dir <dir> --json` output), `--exceptions` (`validate_exceptions_yaml.py <path> --json` output) — any of the latter two may be omitted when nothing was declared for that artifact.

## Output: `GovernanceEvaluationResult`

```json
{
  "mentorConfigured": true,
  "childContextValid": true,
  "childRules": [ { "id", "file", "valid", "classification", "tier", "scope", "status", "errors" } ],
  "exceptions": [ { "id", "rule", "scope", "status", "expiresAt", "valid", "errors" } ],
  "applicableRequirements": [ { "ruleId", "childTier", "scope", "status", "mentorRequirementTier", "mentorRequirementDescription", "applicability", "relationship", "classification", "handling" } ],
  "exceptionEvaluations": [ { "exceptionId", "rule", "scope", "status", "expiresAt", "targetRuleTier", "targetRuleDescription", "applicability", "classification", "handling" } ],
  "conflicts": [ "...entries from applicableRequirements where classification == conflict" ],
  "prohibitedOverrides": [ "...entries from applicableRequirements and exceptionEvaluations where classification == prohibited_override" ],
  "advisoryOverrides": [ "...entries from applicableRequirements where classification == override" ],
  "insufficientEvidence": [ "...entries from applicableRequirements and exceptionEvaluations where classification == unknown" ],
  "warnings": [ "string, string, ..." ]
}
```

This is a superset of the shape sketched in this phase's brief (`applicableRequirements, childRules, exceptions, conflicts, prohibitedOverrides, advisoryOverrides, insufficientEvidence, warnings`), with three additions, each necessary rather than decorative:

- **`mentorConfigured` / `childContextValid`** — a caller must be able to distinguish "no `.mentor/` exists" from "`.mentor/` exists but `project.yaml` is invalid" from "everything is valid but nothing applies to this review" (Scenarios 10 and 11 of the deterministic test suite below). `warnings` alone cannot be branched on programmatically; these two booleans (the second is `null`, not `false`, when `project.yaml` was never declared at all) can be.
- **`exceptionEvaluations`** — exceptions are evaluated by a separate function with a separate, non-tier-based outcome vocabulary (`evaluate_exception_relationship()`, not `classify_relationship()` — Section 9: "an exception is not a governance tier"). Folding them into `applicableRequirements` would force a false shared shape between two structurally different evaluations.

`classification` values: `compatible`, `additive`, `override`, `conflict`, `prohibited_override`, `unknown`, `not_applicable` — the last two are bookkeeping outcomes (an assertion said the rule/exception is not applicable, or a rule's own status is `deprecated`) rather than Section 10 categories, and are excluded from every bucket list.

`classification` values for exceptions: `exception_applicable`, `inactive` (`status` is `rejected`/`expired`), `prohibited_override`, `unknown`, `not_applicable`.

## Deterministic Test Coverage

`tests/schema-tests/governance-evaluation/` and `scripts/run_governance_evaluation_tests.py` cover, as fixed input/expected-output pairs, the 15 named scenarios this phase specified: compatible Mentor+Child rule; additive Child Mandatory; prohibited Child override; Child Advisory vs. Mentor Advisory (legitimate Override); Child Mandatory vs. Mentor Advisory (Conflict, not Override — the documented Override case is narrow); applicable exception; expired exception; prohibited security exception; insufficient applicability evidence; missing child context; invalid child context; multiple applicable rules; multiple applicable exceptions; conflicting child rules (tied tiers); and governance classification independent of severity (no `severity` key anywhere in the result, at any nesting level). See that directory's `README.md` for the fixture format and how each scenario maps to a fixture.

Where a decision genuinely requires LLM judgment — determining applicability or relationship from actual code and rule text — this script does not attempt to test that deterministically, and neither does `skills/code-review/SKILL.md`'s own test suite (`tests/skill-tests/code-review/`), which retains its existing narrative Skill tests (11 through 26) for exactly that reason. This script's deterministic suite tests only the classification step that follows those judgments, which is the part that actually is a pure function of its inputs.

## Read-Only Guarantee

`evaluate_governance.py` performs no file writes at all, aside from stdout when run as a CLI. It does not create, modify, or delete anything in a child repository, in `.mentor/`, or in this repository's own governance documents. It does not create or approve exceptions. This mirrors `docs/Context Discovery.md`'s own Read-Only Guarantee, extended to the evaluation step built on top of it.
