# Skill Standard

## Status

Authoritative. This document is the single specification for what a production Engineering Mentor Skill must contain, how it declares the context it depends on, and how it participates in Mentor's governance model. It elaborates, and does not redefine, `context/skills/Skill Development Standard.md` (the short required-elements list) and `context/templates/Skill Template.md` (the section-header template) — where this document adds detail those two don't, it governs; where they already state something plainly, it is restated here only where needed for a rule elsewhere in this document to make sense, not duplicated wholesale. `docs/Skill Taxonomy.md` covers categories, naming, overlap resolution, and the draft→implement→test→review→certify→production lifecycle. `docs/Skill Testing Standard.md` covers what counts as adequate test coverage. `docs/Skill Quality Standard.md` covers how a finished Skill is scored. This document does not cover any of those three.

**Applies going forward.** Engineering Mentor's 12 existing Skills predate this Standard and are not retrofitted by it — see `docs/Skill Ecosystem Inventory.md` for their current, honestly-marked non-compliance. Migrating an existing Skill to this Standard is a deliberate, separate change to that Skill, reviewed like any other Skill change per `skills/mentor-development/SKILL.md`, not a side effect of this document's adoption.

## 1. Canonical Skill Structure

A Skill is one file, `skills/<name>/SKILL.md`, consisting of a YAML frontmatter block followed by a Markdown body with a fixed set of `##` sections in this order. This is `Skill Template.md`'s section list, with two additions this document introduces: **Governance Integration** (new — see Section 4) and **Related Skills** (already common practice across existing Skills; formalized here as the standard place for it).

```text
---
name: <kebab-case, must equal the skills/<name>/ directory name>
description: <what it does, when to use it, what kind of engineering problem it addresses>
category: <one value from docs/Skill Taxonomy.md's category list>
skillType: <Mentor Core | Review | Authoring/Workflow | Domain Pattern>
---

# <Title>

## Purpose
## Scope
## When to Use
## Required Context
## Workflow
## Rules
## Constraints
## Governance Integration
## Validation
## Edge Cases
## Failure Handling
## Expected Output
## Examples
## Related Skills
```

`Constraints` and `Related Skills` are recommended in every Skill but only structurally required (flagged by `scripts/validate_skill.py` as an error, not a warning, if absent) when the content genuinely calls for them — a Skill with no hard boundary beyond its own scope, or no genuine sibling dependency, should say so in one line rather than force an empty section. Every other section is required, present or not applicable stated explicitly — never silently omitted.

## 2. Required Sections, Precisely

- **Purpose** — the outcome the Skill produces and why it exists as its own Skill rather than folded into another. One paragraph is usually enough; if it takes more, the Skill's `Scope` is probably too wide (see `docs/Skill Taxonomy.md` Section 5, Overlap/Duplication Rules).
- **Scope** — explicit **In scope** and **Out of scope** lists, matching the pattern `skills/context-discovery/SKILL.md` already uses. "Out of scope" must name what a reader might reasonably expect this Skill to cover but doesn't, and say where that responsibility actually lives (another Skill, a Standard, explicitly nowhere yet).
- **When to Use** — concrete trigger conditions, phrased so a reader (human or Claude selecting among Skills) can match a real request against them without needing to read the rest of the file first.
- **Required Context** — see Section 3.
- **Workflow** — numbered steps. A Skill whose actual behavior can't be described as an ordered sequence (pure reference material, e.g. a taxonomy or a data map) states that plainly here rather than forcing artificial numbering.
- **Rules** — the Skill's substantive guidance. See Section 4 for how a Rule's authority (Mentor Mandatory / Configurable / Advisory / Informational, or none of those) must be handled.
- **Constraints** — hard boundaries the Skill must never cross regardless of instruction (e.g. `context-discovery`'s "read-only, absolutely"). Required whenever such a boundary exists; may be omitted only when the Skill genuinely has none beyond its stated Scope.
- **Governance Integration** — see Section 4. Required in every Skill, even a one-line "Not applicable" for a Mentor Core meta-skill that never touches a child repository or produces a governance-classified finding.
- **Validation** — how a reader (or a future execution harness) determines the Skill's output was actually correct, not just superficially well-formed. Mirrors `context-discovery`'s own Validation section.
- **Edge Cases** — situations that are valid inputs but not the common case, named explicitly rather than left for a reader to discover by trial. A Skill whose Testing scenarios (per `docs/Skill Testing Standard.md`) turn up an edge case not listed here has an incomplete Skill, not just an incomplete test suite — update both together.
- **Failure Handling** — what the Skill does when it cannot safely or correctly proceed (missing required context, an unresolvable ambiguity, a request that would violate a Constraint). Never silently guesses; states the gap and stops, mirroring the Mentor Operating Model's No Invention Rule (`context/core/Mentor Operating Model.md`).
- **Expected Output** — the shape of what the Skill produces: a structured review (per `context/templates/Review Template.md`, for Review-type Skills — see `docs/Skill Taxonomy.md`), a new artifact, a decision, or reference material with no artifact at all. State which.
- **Examples** — at least one worked example showing the Skill applied to a realistic input. A negative example (input that looks like it should trigger the Skill but doesn't, or a case the Skill correctly declines) is encouraged wherever the boundary in Scope or Edge Cases isn't otherwise obvious — this is the one concrete gap the `mentor-skills-source` audit found across an otherwise strong 30-skill collection (`SKILL_GAPS.md` Section 13, in that source repository): confident "Do/Don't" pairs, but no worked negative example walked through end to end.
- **Related Skills** — the Skill's real dependencies and neighbors, by file path (`skills/<name>/SKILL.md`), each with one clause on the nature of the relationship (consumes, is consumed by, shares a boundary with). This is the mechanism `docs/Skill Taxonomy.md` Section 5 relies on for overlap prevention — keep it accurate, not decorative.

## 3. Skill Input / Context Contract

Every Skill must state, in its **Required Context** section, one of three postures:

1. **Context-independent.** The Skill needs nothing about the repository it's invoked in or invoked against — true for most Mentor Core meta-skills (`skill-creator`, `mentor-development`) and pure-reference Domain Pattern content. State this explicitly rather than leaving Required Context blank.
2. **Benefits from repository context but degrades gracefully without it.** The common case for a Domain Pattern or Authoring/Workflow-type Skill: richer with a declared stack/architecture, still useful in the abstract without one.
3. **Requires repository context to operate correctly.** The case for every Review-type Skill operating against a real repository — per the Mentor Operating Model's No Invention Rule, a Skill in this posture MUST invoke `skills/context-discovery/SKILL.md` before applying repository-sensitive guidance, exactly as `skills/code-review/SKILL.md` already does, and MUST state in Failure Handling what it does when Context Discovery reports `.mentor/` missing or invalid (never invent the missing facts; fall back to direct repository inspection where the Skill itself performs and documents that inspection, per `skills/context-discovery/SKILL.md`'s own "No Content Inference" rule).

A Skill claiming posture 3 must name which specific fields of the Normalized Project Context (`docs/Context Discovery.md`'s field reference) it actually reads — `stack`, `architecture`, `childRules`, `exceptions`, etc. — not just "context discovery output" generically. This is what lets a future consuming Skill or reviewer verify the dependency is real, not decorative.

## 4. Governance Integration Contract

**A Rule inside a Skill does not acquire Mentor Mandatory authority merely by being phrased with "never," "always," or "non-negotiable."** `docs/Governance Precedence Model.md` Section 2 reserves Mentor Mandatory for rules "whose violation causes direct security, safety, or data-integrity harm" — a Skill author does not get to self-assign that tier by word choice. Every Rule in a Skill's `Rules` section that is meant to bind a child repository's behavior (as opposed to describing this Skill's own internal process) must fall into exactly one of:

- **States a Mentor Mandatory floor.** Cite the specific `context/standards/*.md` (or, once it exists, a future rule-identifier scheme per `docs/Child Repository Integration.md` Section 22) the Rule instantiates. A Skill does not invent a new Mandatory rule that isn't already grounded in an existing Standard — that's a Standard-level change, not a Skill-level one, and goes through the same review `docs/Governance Precedence Model.md` itself went through.
- **States Mentor Configurable, Advisory, or Informational guidance.** Say which. This is the default posture for most Domain Pattern and Authoring/Workflow content — a recommended pattern, not a floor.
- **Makes no claim on child-repository behavior at all.** Pure reference material (a taxonomy, a worked example) states this plainly; Section 2's authority question doesn't arise.

**Every Skill whose Skill Type is Review, or that is invoked against a real child repository and can surface a finding, must additionally state in Governance Integration:**

- That it invokes `skills/context-discovery/SKILL.md` first (per Section 3, posture 3), and, wherever a finding is checked against a discovered child rule or exception, that it routes the tier/relationship classification through `scripts/evaluate_governance.py` per `docs/Governance Evaluation.md`, rather than re-deriving `docs/Governance Precedence Model.md` Section 10's conflict-type table from prose on every invocation. `skills/code-review/SKILL.md`'s Child Governance rules are the reference implementation of this — a new Review-type Skill should follow that shape, not invent a parallel one.
- That every finding it produces is tagged with exactly one level from `context/standards/Severity Taxonomy.md` and no other vocabulary — restated here because it is the single most load-bearing cross-Skill consistency rule Mentor has, not because `Severity Taxonomy.md` is being redefined.
- That governance classification and finding severity are independent axes (`docs/Governance Precedence Model.md` Section 12) — a Skill must never imply that a Prohibited Override classification automatically means CRITICAL severity, or that a Compatible classification automatically means INFO.

A Skill that makes no findings and touches no child repository (most Mentor Core and Domain Pattern skills) states "Not applicable" here, with one sentence on why (e.g. "this Skill produces reference material only and does not evaluate a specific repository's compliance").

## 5. Validation Requirements — the Skill File Itself

Before a Skill is considered structurally complete (separate from whether its *content* is good — see `docs/Skill Quality Standard.md` — and separate from whether it's *tested* — see `docs/Skill Testing Standard.md`):

1. `scripts/validate_skill.py skills/<name>/SKILL.md` reports `valid: true`: frontmatter parses, `name` matches the directory, `description` is non-empty, `category` is one of `docs/Skill Taxonomy.md`'s defined categories, `skillType` is one of the four types in Section 6 of `docs/Skill Taxonomy.md`, and every required `##` section from Section 1 above is present (by header text, not by content quality — this is a structural check, not a review).
2. Every path referenced under `Related Skills` resolves to a real `skills/<name>/SKILL.md` in this repository at the time of the check.
3. The Skill was checked against `docs/Skill Taxonomy.md` Section 5 (Overlap/Duplication Rules) before being proposed — record the outcome of that check in the pull request or change description, not in the Skill file itself.

Passing (1)–(3) makes a Skill structurally valid. It does not make it production-ready — that additionally requires meeting `docs/Skill Testing Standard.md`'s minimum bar and `docs/Skill Quality Standard.md`'s certification threshold before it is added to `docs/Skill Ecosystem Inventory.md` as a Production Skill (see `docs/Skill Taxonomy.md` Section 7, Lifecycle).

## 6. Naming

Restated from `skills/mentor-development/SKILL.md` point 8, not redefined: `name` in frontmatter must exactly match the Skill's directory name under `skills/<name>/SKILL.md` — this is what makes `/engineering-mentor:<name>` resolve. `docs/Skill Taxonomy.md` Section 4 adds the naming *pattern* expected per Skill Type (e.g. Review-type Skills as `<domain>-review`); this document only restates the exact-match mechanical rule.

## Related

- `context/templates/Skill Template.md`, `context/skills/Skill Development Standard.md` — the shorter documents this one elaborates.
- `docs/Skill Testing Standard.md`, `docs/Skill Quality Standard.md`, `docs/Skill Taxonomy.md` — the three companion documents; see their own Status sections for exactly what each owns.
- `docs/Governance Precedence Model.md`, `docs/Governance Evaluation.md`, `docs/Context Discovery.md` — the governance and context mechanisms Section 3 and Section 4 require a Skill to integrate with correctly rather than reimplement.
- `skills/context-discovery/SKILL.md`, `skills/code-review/SKILL.md` — the two existing reference implementations this document asks a new Skill to follow the shape of, not duplicate.
