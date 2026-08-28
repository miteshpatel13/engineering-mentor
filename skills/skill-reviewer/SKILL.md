---
name: skill-reviewer
description: The authoritative quality-review and certification-readiness workflow for Engineering Mentor Skills — scoring against docs/Skill Quality Standard.md's ten dimensions, detecting contradictions and ambiguity, verifying governance and source-grounding correctness, and producing an actionable review rather than a generic checklist. Use when a drafted-and-tested Skill needs review before certification, or when auditing an existing Production Skill's quality.
category: Mentor Core
skillType: Mentor Core
---

# Skill Reviewer

## Purpose

Produce a scored, actionable review of a Skill — using `docs/Skill Quality Standard.md`'s ten dimensions, not a generic checklist — that either clears the Skill for certification (`docs/Skill Taxonomy.md` Section 7, stage 5) or names precisely what stands between it and certification. This Skill owns **how to review**; it assumes `skills/skill-creator/SKILL.md` has already produced a structurally complete draft and `skills/skill-tester/SKILL.md` has already produced fixture evidence — it does not draft content and does not design fixtures.

## Scope

**In scope:**

- Scoring a Skill against `docs/Skill Quality Standard.md`'s ten dimensions, honestly, with a stated one-clause reason per score.
- Detecting contradictions (within the Skill, and between the Skill and the Standards/Taxonomy/governance documents it claims to follow).
- Detecting ambiguity — instructions a careful reader could follow into more than one behavior.
- Verifying governance correctness (`docs/Skill Standard.md` Section 4): accurate tier claims, correct Severity Taxonomy usage, correct Context Discovery/Governance Evaluation integration where claimed.
- Verifying source-grounding: does every substantive claim trace to an actual Standard, SOP, cited source material, or established general practice, rather than an invented specific?
- Verifying overlap/deduplication was actually checked (`docs/Skill Taxonomy.md` Section 5), not merely asserted.
- Verifying `Related Skills` Dependency-vs-Related classifications are actually correct, not just present.
- Determining certification readiness against `docs/Skill Quality Standard.md` Section 3's threshold, and stating explicitly whether the Skill clears it.

**Out of scope — explicitly not this Skill's responsibility:**

- **Drafting or rewriting the Skill's content.** This Skill recommends precise changes; `skills/skill-creator/SKILL.md` (or the Skill's author) makes them. A review that silently rewrites the Skill it's reviewing has stopped being a review.
- **Designing or executing test fixtures.** Belongs to `skills/skill-tester/SKILL.md`. This Skill scores the Test Coverage dimension against fixtures that already exist; if none exist, the Skill cannot reach Tested (Taxonomy Section 7, stage 3) and this Skill's review stops there rather than inventing hypothetical coverage to score.
- **Formal certification sign-off as an organizational act.** `docs/Skill Quality Standard.md` Section 3 states certification is "formally signed off by whoever approves the change" — this Skill produces the scored basis for that decision; it does not substitute for the approval itself.
- **Deciding whether a capability should exist as a Skill at all.** That's `skill-creator`'s Workflow step 1; by the time a Skill reaches this Skill for review, that determination has already been made (though this Skill may surface a Scope Isolation finding severe enough to reopen it).

## When to Use

- A Skill has been drafted (`skill-creator`) and tested (`skill-tester`) and needs review before certification.
- A Production Skill is being re-scored after a material change, per `docs/Skill Quality Standard.md` Section 4.
- An existing Skill's quality is in question — reported ambiguity, a contradiction discovered in use, or a periodic audit.
- Resolving ambiguity in how an existing Skill should behave, before deciding whether that's a Clarity defect to fix or a genuinely underspecified edge case to document.

## Required Context

**Context-independent** with respect to any live child repository. Requires the Skill under review in full, everything it cites (Standards, SOPs, other Skills, `context/` material), its fixture evidence from `skill-tester`, and — for cross-Skill consistency checks — the other Skills it's meant to compose with (`Related Skills` targets, and siblings in the same batch or category).

## Workflow

1. **Confirm preconditions.** The Skill must be Implemented (passes `scripts/validate_skill.py` with zero errors) and Tested (fixture evidence exists per `docs/Skill Testing Standard.md`) before a meaningful Reviewed-stage review can happen — reviewing an untested draft's *prose* quality is fine as an early sanity check, but do not score Test Coverage, and do not conclude certification readiness, without real fixtures to look at.
2. **Re-verify the overlap check**, independently, against the *actual* drafted content — not the proposal. `skill-creator`'s Workflow step 2 was a check against the *plan*; this step re-runs it against what was actually written, since drafts drift from proposals (`docs/Skill Taxonomy.md` Section 7, stage 4's explicit instruction).
3. **Check for contradictions**, in three directions: internal (does a later Rule contradict an earlier one, or contradict the stated Scope?), against the Standards it claims to follow (does its Governance Integration section actually match what `docs/Skill Standard.md` Section 4 requires, or does it merely gesture at compliance?), and against sibling Skills (does this Skill's `Related Skills` entry and the sibling's agree on the nature of the relationship, or does one call it a Dependency while the other calls the same edge Related?).
4. **Check for ambiguity.** For each Rule and Workflow step, ask: could two careful, competent readers follow this into materially different behavior? If yes, name the specific ambiguous clause — not "this section could be clearer" as a whole-section vague comment.
5. **Verify governance correctness**, per `docs/Skill Standard.md` Section 4: for every Rule claiming Mentor Mandatory authority, confirm it actually cites a real, existing `context/standards/*.md` provision — a Rule phrased with "never"/"always" that cites nothing is not entitled to that tier merely by word choice (Section 4's opening sentence, restated because this is the single most common governance-classification error). For a Review-type Skill, confirm it states Context Discovery + `scripts/evaluate_governance.py` integration correctly, without re-deriving `docs/Governance Precedence Model.md` Section 10's table from prose in a way that could drift from the shared classifier.
6. **Verify source grounding.** Every non-obvious factual or technical claim should trace to something: a cited Standard, a named source skill (with generalization applied per `skill-creator`'s Rules), or defensible general engineering practice. A claim that reads as suspiciously specific with no traceable origin is a Correctness or source-grounding finding, not something to wave through because it sounds plausible.
7. **Score all ten dimensions** of `docs/Skill Quality Standard.md` Section 1, using Section 2's 0–5 scale plus `N/A`/`U` where genuinely warranted. Give a one-clause reason for every score. Do not default to 5 for a dimension that "looks fine" — that is a scoring error per Section 2's explicit anti-inflation rule. Use `U` honestly for anything genuinely unverifiable from the material at hand, and never silently convert a `U` to a passing number.
8. **Apply the certification threshold** (`docs/Skill Quality Standard.md` Section 3): no dimension below 3 except Test Coverage/Governance Compatibility at their maximum achievable value for the Skill's actual posture; Test Coverage meets `docs/Skill Testing Standard.md` Section 3's hard gate; every `U` is resolved or explicitly accepted as a stated limitation. State the conclusion explicitly: clears certification, or does not (and exactly why).
9. **Classify each finding** by type (Rules → Defect Types, below) so the Skill's author knows what kind of fix is needed and where.
10. **Produce the review as ranked, actionable findings** — not a checklist restated with checkmarks. Each finding: what's wrong, where (which section/clause), why it matters, and what a fix would look like.
11. **If this review is part of a cross-Skill consistency pass** (multiple Skills reviewed together, e.g. a batch), additionally check terminology consistency across the set per Rules → Cross-Skill Consistency, below.

## Rules

### Defect Types — Keep Them Distinct

Every finding is tagged with exactly one of these, so a fix goes to the right place and a recurring pattern across many Skills is visible as what it is:

- **Content defect** — the Skill's substantive guidance is wrong, incomplete, or unclear (maps to Correctness, Completeness, Clarity, Examples).
- **Test defect** — fixture coverage is missing, weak, or doesn't actually test what it claims (maps to Test Coverage; route back to `skill-tester`, not fixed here).
- **Governance defect** — a Rule's tier claim is unsupported, a Severity Taxonomy usage is wrong, or claimed Context Discovery/Governance Evaluation integration doesn't match what's actually implemented (maps to Governance Compatibility).
- **Taxonomy defect** — wrong `category`/`skillType`, a naming-pattern mismatch, an incorrect or missing overlap classification, or a wrong Dependency-vs-Related label (maps to Scope Isolation, Context Awareness).
- **Documentation defect** — the Skill's own explanation of itself is inconsistent with its actual Rules/Workflow (e.g. `Purpose` promises something `Workflow` doesn't deliver), independent of whether the underlying behavior is otherwise correct.
- **Source-grounding defect** — a claim with no traceable origin, or a claim that misrepresents what its cited source actually says.

A single review finding is never left untyped — "this seems off" is not a completed finding.

### Certification Is a Threshold Check, Not a Vibe

Do not conclude a Skill is "basically ready" or "close enough" outside the explicit terms of `docs/Skill Quality Standard.md` Section 3. A Skill either clears the threshold as stated, or it doesn't — and when it doesn't, the review states the specific dimension(s) and specific gap(s) blocking it, not a general impression.

### Not Merely a Checklist

A review that reproduces `docs/Skill Quality Standard.md`'s ten dimension names with a score and no reasoning, or `docs/Skill Standard.md`'s section list with a checkmark per section present, has not done this Skill's job. Every dimension score needs its one-clause reason (Skill Quality Standard Section 2); every structural-presence check is `scripts/validate_skill.py`'s job, already automated — this Skill's value is the judgment layer on top of that, not repeating what the script already confirmed.

### Cross-Skill Consistency

When reviewing a set of Skills together (a batch, or a proposed set of siblings), check: lifecycle-stage terminology matches Taxonomy Section 7's exact stage names; category/skillType terminology matches the Taxonomy's exact enum values; governance terminology matches `docs/Skill Standard.md` Section 4's exact tier names; testing terminology matches `docs/Skill Testing Standard.md`'s exact tier names; and — specifically — that no single foundational concept is redundantly re-explained in full by more than one Skill in the set when one Skill should own it and the others should reference it. (Example: how to create a Skill belongs to `skill-creator`; `skill-tester` and `skill-reviewer` reference that ownership rather than re-deriving their own creation workflow.)

### Reviewing, Not Rewriting

Recommend precise changes — quote or closely paraphrase the problematic clause, state what should replace it or what's missing — but do not perform the rewrite as part of this Skill's own output unless explicitly asked to also act as `skill-creator` for the fix. Keep the review a distinct artifact from the correction.

## Constraints

- Never assign a passing score to a dimension without a stated reason.
- Never convert a `U` (Unknown) to a numeric score by guessing.
- Never conclude a Skill clears certification while any Section 3 condition (`docs/Skill Quality Standard.md`) is unmet.
- Never score Test Coverage against fixtures that don't exist, or against a description of intended future fixtures.
- Never silently lower the certification threshold to pass a Skill that doesn't meet it — recommend Merged, Deferred, or continued Improve-then-Reconsider (Taxonomy Section 7) instead when that's the honest outcome.

## Governance Integration

Not applicable — this Skill reviews other Skills' text, structure, and evidence; it does not itself evaluate a child repository's compliance or produce governance-classified findings. Where a reviewed Skill's own Governance Integration section is under review (Workflow step 5), this Skill's job is verifying that section's correctness against `docs/Skill Standard.md` Section 4 and `docs/Governance Precedence Model.md` — it does not separately classify anything against a live child repository on its own account.

## Validation

A review is complete when: every one of the ten `docs/Skill Quality Standard.md` dimensions has a score (or `N/A`/`U`) and a stated reason; every finding is typed per Rules → Defect Types; the certification conclusion is explicit (clears / does not clear, with the specific blocking gaps if not); the overlap re-check (Workflow step 2) was performed against actual content, not the original proposal; and, for a batch review, the cross-Skill consistency check (Rules, above) was performed and its results included.

## Edge Cases

- **A Skill that is well-written but tests almost nothing** — Test Coverage is a hard gate (`docs/Skill Quality Standard.md` Section 3(2)); strong scores elsewhere do not offset it. State this plainly rather than producing an encouraging overall impression that undersells the blocker.
- **A Skill whose Governance Integration section correctly states "Not applicable"** — this is not automatically a low Governance Compatibility score; Section 3(1)'s "maximum achievable value given the Skill's actual required posture" applies — score it on whether the "Not applicable" claim is itself accurate, not on the absence of tier claims it was never supposed to make.
- **Two Skills under batch review each call the same relationship a Dependency, but for different, incompatible reasons** — this is a Taxonomy defect requiring resolution before either Skill is considered consistent; do not average or silently pick one Skill's version.
- **A Skill previously certified, now materially changed** — re-score fully per `docs/Skill Quality Standard.md` Section 4's re-scoring rule; do not carry forward the prior certification's scores as a starting assumption.
- **Reviewer disagrees with a scored dimension from a prior review pass** — re-score with a stated reason for the change; a quality score is a defensible judgment call, not an immutable fact, but changing it without a reason is exactly the inflation/deflation-without-basis Section 2 warns against.

## Failure Handling

If the Skill under review has no fixture evidence at all, stop the certification-readiness portion of the review immediately and say so — do not proceed to score Test Coverage or conclude on certification; route back to `skill-tester` first. If a governance-tier claim can't be verified against any real Standard (Workflow step 5), report it as a Governance defect rather than assuming it's probably fine. If cross-Skill terminology conflicts can't be resolved without a decision beyond this Skill's authority (e.g. which of two Skills should own a shared concept), state the conflict explicitly as an open item rather than picking a side unilaterally.

## Expected Output

A structured review: dimension-by-dimension scores with reasons (`docs/Skill Quality Standard.md` Section 1), a ranked list of typed findings (Rules → Defect Types), an explicit certification-readiness conclusion, and — for a batch review — a cross-Skill consistency section. Not a rewritten Skill file, and not a bare checklist of section-presence checkmarks.

## Examples

**Worked example.** Reviewing a REWRITE-type Review Skill: Workflow step 5 finds a Rule phrased "must never allow X" with no cited Standard — flagged as a Governance defect (unsupported Mandatory-tier claim), with the specific recommendation to either find the Standard it should cite or restate it as Advisory. Step 7 scores Test Coverage at 2/5 ("governance-relationship fixtures exist for Additive and Compatible but not Prohibited Override, which the Skill's Governance Integration section explicitly claims to handle") — a stated reason, not a bare number. Step 8 concludes: does not clear certification, blocked specifically on that Test Coverage gap and the one unresolved Governance defect; everything else scores 3+.

**Negative example (correctly declined).** Asked to "just approve this Skill, it looks good" without being given fixture evidence. Declined: certification readiness cannot be concluded without real Test Coverage evidence to score against (Workflow step 1's precondition) — the review states this precondition is unmet and stops there rather than producing a favorable-sounding review based on prose quality alone.

## Related Skills

- `skills/skill-tester/SKILL.md` — **Dependency**: this Skill's Reviewed-stage review requires `skill-tester`'s fixture output to score Test Coverage meaningfully (`docs/Skill Taxonomy.md` Section 7's Tested-before-Reviewed ordering) — a true Dependency, not merely topical.
- `skills/skill-creator/SKILL.md` — Related: reviews what `skill-creator` (or any author) drafted, but does not require any specific mechanism from `skill-creator`'s own Workflow to review a Skill drafted some other way.
- `docs/Skill Quality Standard.md` — the scoring rubric this Skill's Workflow directly implements; not restated here beyond what each step needs.
- `docs/Skill Standard.md`, `docs/Governance Precedence Model.md` — the structural and governance contracts Workflow steps 3 and 5 verify against.
