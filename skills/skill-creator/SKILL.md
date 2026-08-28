---
name: skill-creator
description: The authoritative workflow for creating a new Engineering Mentor Skill — deciding whether a capability deserves a Skill at all, classifying it correctly (category, skillType, governance tier), generalizing source material instead of copying it, and drafting every required section of docs/Skill Standard.md. Use when defining a new global Skill from scratch, splitting or merging an existing one, or evaluating whether a project-specific pattern is ready to become reusable Mentor content.
category: Mentor Core
skillType: Mentor Core
---

# Skill Creator

## Purpose

Produce a new Mentor Skill that is structurally complete (`docs/Skill Standard.md`), correctly classified (`docs/Skill Taxonomy.md`), free of project-specific leakage, and ready to enter the Draft stage of the Skill lifecycle with a real chance of reaching Certified. This Skill exists separately from `skill-tester` and `skill-reviewer` because creation, testing, and review are three distinct responsibilities that must not collapse into one undifferentiated "make a good Skill" instruction — this Skill owns **how to create**; it does not own how to test (`skills/skill-tester/SKILL.md`) or how to review (`skills/skill-reviewer/SKILL.md`), and does not repeat their content here beyond the minimum handoff each needs.

## Scope

**In scope:**

- Deciding whether a candidate capability should become a Skill at all, versus a Standard, SOP, checklist, or template.
- Checking the candidate against `docs/Skill Ecosystem Inventory.md` and `docs/Skill Taxonomy.md` Section 5 for overlap before drafting anything.
- Classifying the candidate: `category` (Taxonomy Section 3), `skillType` (Taxonomy Section 1), naming pattern (Taxonomy Section 4).
- Determining the Skill's governance posture (`docs/Skill Standard.md` Section 4) and Required Context posture (Section 3).
- Generalizing source material — an existing project-specific skill, a repository pattern, an audit finding — into reusable Mentor content, and rejecting or flagging source material that cannot be generalized responsibly.
- Drafting every required section of `docs/Skill Standard.md` Section 1's canonical structure.
- Handing the drafted Skill to `skill-tester` and `skill-reviewer` with what each needs to do its own job.
- Tracking the Skill through the Draft and Implemented lifecycle stages (`docs/Skill Taxonomy.md` Section 7); stopping at the Implemented → Tested boundary, which belongs to `skill-tester`.

**Out of scope — explicitly not this Skill's responsibility:**

- **Testing.** Designing fixtures, deciding whether test coverage is adequate, and the two-tier testing model belong to `skills/skill-tester/SKILL.md` and `docs/Skill Testing Standard.md`. This Skill states what testing the drafted Skill will need (so the draft doesn't foreclose it) but does not write the fixtures.
- **Reviewing and scoring.** Contradiction detection, quality scoring against the ten dimensions, and certification sign-off belong to `skills/skill-reviewer/SKILL.md` and `docs/Skill Quality Standard.md`. This Skill drafts; it does not grade its own work as final.
- **Standards, SOPs, checklists, templates.** If Section "Does This Deserve a Skill?" below concludes the candidate isn't a Skill, this Skill's job ends with that determination — authoring the resulting Standard/SOP/checklist/template follows `skills/mentor-development/SKILL.md`, not this one.
- **Enforcing or discovering child-repository context at runtime.** That is `skills/context-discovery/SKILL.md`'s job; this Skill only decides, at authoring time, which Required Context posture a new Skill should declare.

## When to Use

- A recurring engineering pattern, review discipline, or authoring workflow has shown up in more than one place (a child repository, an audit, a standards gap) and looks genuinely reusable.
- `docs/Skill Ecosystem Inventory.md` Section 3 (or a fresh gap analysis) identifies a category with no Skill and a concrete source of material to build one from.
- An existing Skill needs to be split (Taxonomy overlap class B resolution grown into a genuine second concern) or merged (class A/B resolution).
- A migration or expansion plan (e.g. `docs/Skill Migration & Expansion Plan.md`) has designated a specific candidate as `NEW`, `REWRITE`, `MERGE`, or `SPLIT` and authorized implementation.

Do not use this Skill to make a one-off change to an existing Skill's wording that doesn't affect its scope, structure, or classification — that's a normal edit, not a creation-workflow invocation.

## Required Context

**Context-independent** with respect to any child repository — this Skill does not discover or depend on a child repository's `.mentor/` configuration. It does require read access to Mentor's own repository state: `docs/Skill Ecosystem Inventory.md`, `docs/Skill Taxonomy.md`, `docs/Skill Standard.md`, the `skills/` directory, and, when generalizing from a source collection, the specific source material being generalized (e.g. a `mentor-skills-source`-shaped audit, or a named project skill). This is Mentor authoring context, not child-repository context in the `docs/Skill Standard.md` Section 3 sense — declaring "Context-independent" here follows Taxonomy Section 1's own classification of `skill-creator` as a Mentor Core meta-skill.

## Workflow

1. **Does this deserve a Skill?** Apply `skills/mentor-development/SKILL.md`'s leakage test in reverse: is this genuinely a *procedure* (a repeatable workflow, an evaluation discipline, a design pattern applied case by case) rather than a static fact, principle, or one-time decision? A static principle belongs in a Standard; a one-time process belongs in a SOP; a fixed reference list belongs in a checklist or template. If the candidate is really "information a Skill would need," it may belong in `context/` for an existing Skill to cite, not as a new Skill of its own. State the conclusion and the reason before proceeding.
2. **Check for overlap.** Read `docs/Skill Ecosystem Inventory.md`'s current table and `docs/Skill Taxonomy.md` Section 5's five-class table. Classify the candidate against every existing Skill whose category or subject is plausibly related — not just the closest match. Resolve per Section 5's table: class A (exact duplicate) stops here; class B (strong overlap) redirects into growing the existing Skill instead of drafting a new one; class C and D proceed, with the required boundary statement drafted now, not deferred to Related Skills at the end; class E proceeds and is a signal worth flagging back to whoever maintains `docs/Skill Ecosystem Inventory.md`'s gap analysis.
3. **Classify `skillType`.** Use Taxonomy Section 1's four definitions and Section 2's composition diagram, not the candidate's working title. A Skill that evaluates existing material and produces findings is Review, regardless of what its source material called itself; a Skill that produces a new artifact or decision is Authoring/Workflow; reusable pattern/reference material consumed by other Skills is Domain Pattern; anything governing how Mentor itself or its Skills are built/tested/reviewed/certified is Mentor Core.
4. **Classify `category`.** Pick the single primary category from Taxonomy Section 3's fixed list. A Skill spanning two categories states the primary one in frontmatter and the secondary relationship in its own `Scope` section (Taxonomy Section 3) — never invent a second frontmatter value and never force a category that doesn't fit rather than leaving it as a documented open question.
5. **Assign the naming pattern.** Taxonomy Section 4's per-type pattern (`<domain>-review`, `<domain>-<noun>`, pattern-named, `mentor-<noun>`/`skill-<verb>`). The directory name and frontmatter `name` must match exactly (`docs/Skill Standard.md` Section 6) — decide the final name before drafting, not after, since renaming later touches every `Related Skills` reference elsewhere.
6. **Determine the Required Context posture.** One of `docs/Skill Standard.md` Section 3's three postures. Posture 3 (requires repository context) applies to essentially every Review-type Skill; posture 2 applies to most Authoring/Workflow and Domain Pattern content used against a real repository; posture 1 applies to Mentor Core meta-skills and pure-reference Domain Pattern content. If posture 3, name the specific Normalized Project Context fields (`docs/Context Discovery.md`) the Skill will actually read — not a generic reference to "context discovery output."
7. **Determine the governance posture.** Per `docs/Skill Standard.md` Section 4: for every Rule that will bind child-repository behavior, decide now whether it states a Mentor Mandatory floor (and cite the specific `context/standards/*.md` it instantiates — never invent a new Mandatory rule at Skill-authoring time), states Configurable/Advisory/Informational guidance, or makes no claim on child behavior at all. If the Skill is Review-type or can surface a governance-classified finding, plan for Context Discovery + `scripts/evaluate_governance.py` integration now (Section 4's second paragraph) rather than retrofitting it after drafting.
8. **Identify source-of-truth material and generalize it.** See Rules → Generalization, Not Copying, below. This is the step most likely to be rushed; it isn't optional.
9. **Draft every section of `docs/Skill Standard.md` Section 1's canonical structure**, in order: `Purpose`, `Scope` (explicit In/Out), `When to Use`, `Required Context` (step 6's posture, stated), `Workflow` (numbered, or explicitly stated as reference-only if the content is genuinely non-sequential), `Rules` (step 7's governance classification applied per rule), `Constraints` (if a genuine hard boundary exists), `Governance Integration` (step 7's conclusion, restated per Section 4's required content), `Validation`, `Edge Cases`, `Failure Handling`, `Expected Output`, `Examples` (at least one; a negative example wherever the Scope/Edge Cases boundary isn't otherwise obvious), `Related Skills` (accurate dependency-vs-Related classification — see Rules).
10. **Cross-check Rules against grounding standards.** Before the draft can be considered ready to hand off as Implemented, check every Rule that names a specific engineering concern against the corresponding `context/standards/*.md` and, where one exists for the domain, `context/checklists/*.md` — every item the applicable standard/checklist names either has a corresponding Rule or the omission is a deliberate, stated Scope decision, not a silent gap. This does not create new Mandatory rules (step 7 already covers that) or restate `docs/Skill Standard.md`/`docs/Skill Testing Standard.md` policy — it exists specifically to catch the completeness gap a structural validator cannot: a named standard item with no Rule addressing it at all.
11. **Run `scripts/validate_skill.py skills/<name>/SKILL.md`.** Fix every error before moving on; a structural failure here means the draft isn't Implemented yet (Taxonomy Section 7, stage 2), regardless of how complete the prose reads.
12. **State the testing and quality expectations the draft creates**, explicitly, for the handoff: which Testing Standard Section 2 scenario categories apply, whether the governance-relationship set applies (Testing Standard Section 2's second paragraph), and any dimension of `docs/Skill Quality Standard.md`'s ten that looks likely to be `N/A` or contested given the Skill's type and content. This is a prediction handed to `skill-tester`/`skill-reviewer`, not a self-certification.
13. **Update `docs/Skill Ecosystem Inventory.md`'s draft/in-progress tracking** if the repository's convention calls for it at this stage (the Inventory itself is only formally updated as Production content at lifecycle stage 6 — see Taxonomy Section 7 — but a Skill in progress should not be invisible to the next person who runs overlap-checking in step 2 against a stale table).

## Rules

### Generalization, Not Copying

**The single most common failure mode this Skill exists to prevent: copying an existing project-specific Skill into Mentor and renaming it.** A project Skill (from a child repository, or an audited external collection like `mentor-skills-source`) encodes two things at once — a genuinely reusable principle, and project-specific facts (a database engine choice, a business domain, a client decision, a table or field name). Copying the file verbatim and swapping the title imports both. This Skill requires separating them, every time:

1. Read the source material fully. Identify every sentence that is a *principle* (would still be true verbatim in an unrelated repository on a different stack) versus a *fact* (specific to the originating project, client, or codebase).
2. Draft the new Skill from the principles only. Where a fact was load-bearing for illustrating the principle, replace it with a clearly-fictional or clearly-generic stand-in (a placeholder table name, a generic framework reference, or an abstract description) rather than the real one.
3. Never carry forward a specific business rule, schema decision, client requirement, credential, domain name, or company-specific naming convention. `skills/mentor-development/SKILL.md`'s leakage test (`would this guidance make sense verbatim in an unrelated repository on a different stack?`) is applied line by line during this step, not just once at the end.
4. If, after separating principle from fact, there isn't enough genuinely reusable principle left to justify a Skill, that is a valid outcome — recommend Deferred or Rejected (Taxonomy Section 7) rather than padding a thin principle out with the original project's specifics to make it look complete.

A generalized Skill that still reads as "obviously about one specific project" — a lingering example using the source project's actual entity names, a Rule phrased as if only one stack exists — has not passed this step, regardless of how polished its prose is.

### Distinguishing Confirmed, Recommended, and Assumed Source Material

When source material itself distinguishes confirmed requirements from recommendations from assumptions (as `srs-scope-rules`-shaped material does, and as `skills/requirements-discipline/SKILL.md` formalizes for child-repository use), preserve that distinction into the generalized Skill rather than flattening it into uniform prose:

- A confirmed, load-bearing principle from the source becomes a Rule or a Constraint.
- A recommendation from the source becomes Advisory guidance (`docs/Skill Standard.md` Section 4), stated as a suggested approach, not a floor.
- An assumption from the source is not carried into the new Skill as a stated fact at all — either the underlying principle is confirmed independently (by a second source, or by being self-evidently general engineering practice) and stated as such, or it is left out.

### Preventing Project-Specific Leakage, Beyond the Generalization Step

Even a fully generalized draft can leak indirectly: an Example that only makes sense for one kind of application, a Rule that assumes one specific authentication mechanism exists, a Required Context posture that silently assumes a field only some project types declare. Re-check the finished draft — not just the source material — against the leakage test before handing it to `skill-tester`.

### Dependency vs. Related Classification

A Skill's `Related Skills` section must classify every cross-reference as either a **Dependency** or **Related**, using the test `docs/Skill Migration & Expansion Plan.md` Section 10 establishes: a Dependency exists only where the downstream Skill's own Rules, Workflow, or governance-classified findings actually require the upstream Skill's established output, contract, or rule to function correctly. Topical proximity, shared originating audit cluster, conventional sequencing, or a Taxonomy Section 5 class D Complementary pairing are **Related**, not Dependency, even when the two Skills are frequently used together. Getting this wrong in either direction breaks the Skill Dependency Graph any migration or expansion plan relies on — do not default to calling something a Dependency because it "feels important."

### Lifecycle Ownership

This Skill owns Draft and Implemented (Taxonomy Section 7, stages 1–2). Handing a drafted Skill to `skill-tester` begins stage 3 (Tested); handing a tested Skill to `skill-reviewer` begins stage 4 (Reviewed) through stage 5 (Certified). This Skill does not advance a Skill past Implemented itself, and does not claim a Skill is "basically done" before stage 3 — an Implemented Skill with zero fixtures is not close to Certified regardless of how complete its prose is (`docs/Skill Quality Standard.md` Section 3's hard Test Coverage gate).

## Constraints

- Never invent a new Mentor Mandatory rule while drafting a Skill. A Mandatory floor must already exist in a `context/standards/*.md` file; if the candidate Skill seems to need one that doesn't exist, that is a Standard-level change proposal, escalated separately — not something this Skill authorizes by drafting a Rule that claims the tier.
- Never copy a project-specific Skill's file verbatim, with only the frontmatter or title changed, and represent it as Mentor content.
- Never mark a Skill's structural draft as "ready" while `scripts/validate_skill.py` reports any error.
- Never assign `category` or `skillType` values outside the enums `scripts/validate_skill.py` enforces (`docs/Skill Taxonomy.md` Sections 1 and 3) — if neither existing value fits, say so explicitly rather than picking the closest approximation silently.

## Governance Integration

Not applicable in the child-repository sense — this Skill produces draft Mentor Skill content, not findings against a specific child repository's compliance, and does not invoke Context Discovery or Governance Evaluation itself. It is, however, the point at which a *future* Skill's own governance posture (Mentor Mandatory / Configurable / Advisory / Informational, per `docs/Skill Standard.md` Section 4) is decided — step 7 of the Workflow above governs that decision; this section states that this Skill's own output is Mentor-internal authoring material, not a child-repository finding.

## Validation

A drafted Skill is ready to leave this Skill's responsibility when: `scripts/validate_skill.py skills/<name>/SKILL.md` reports `valid: true`; the overlap check (Workflow step 2) was performed and its outcome recorded in the change description, per `docs/Skill Standard.md` Section 5(3); every `Related Skills` entry resolves to a real file and is correctly classified Dependency vs. Related; the Generalization, Not Copying check (Rules, above) was applied and any source material used is named in the change description; the grounding-standards cross-check (Workflow step 10) was performed and any deliberate omission stated explicitly rather than left silent; and the testing/quality expectations handoff (Workflow step 12) is written down, not left implicit.

## Edge Cases

- **Source material with no clear reusable principle at all** — conclude the candidate should not become a Skill (Rules → Generalization, Not Copying, point 4); do not force a thin Skill into existence to have something to show.
- **A candidate that overlaps two existing Skills differently** (strong overlap with one, complementary with another) — resolve each relationship independently per Taxonomy Section 5; do not average them into one blended disposition.
- **A candidate whose correct `skillType` is genuinely ambiguous** (e.g. content that both evaluates and produces) — state the ambiguity explicitly rather than picking one silently; this is exactly the kind of case Taxonomy Section 3's own open question about `category: Review` vs. `skillType: Review` illustrates can happen, and it is preserved as an open item, not force-resolved.
- **Source material spans multiple original Skills that should become one Mentor Skill** (a MERGE-shaped migration) — generalize all sources together, checking each individually for leakage, before drafting one unified Skill; do not draft one section per source and staple them together unedited.
- **A Skill candidate that would require repository context to design responsibly, but no example repository is available to check against** — draft the Skill's Required Context posture and Rules based on general, established principle (per the No-Invention discipline), and flag the absence of a concrete worked example as a known gap for `skill-reviewer` to weigh, rather than fabricating a plausible-looking example repository.

## Failure Handling

If overlap checking (Workflow step 2) is inconclusive — the candidate plausibly fits more than one existing Skill's territory and the right resolution isn't clear from `docs/Skill Ecosystem Inventory.md` and Taxonomy Section 5 alone — stop and state the ambiguity rather than picking a classification to keep moving. If source material cannot be separated into principle versus fact with reasonable confidence, do not draft a Skill from it; report that the source material is too project-specific to generalize safely, per the Mentor Operating Model's No Invention Rule extended to Skill content (`docs/Skill Migration & Expansion Plan.md` Section 11). If a required governance-tier citation (Workflow step 7) can't be traced to an existing Standard, stop and say so rather than drafting the Rule as Mandatory anyway.

## Expected Output

A new or revised `skills/<name>/SKILL.md` file, structurally valid per `docs/Skill Standard.md`, classified per `docs/Skill Taxonomy.md`, with source material generalized per this Skill's Rules — at the Implemented lifecycle stage, explicitly not yet claimed as Tested, Reviewed, or Certified. Alongside it: a short handoff note (in the change description, not necessarily in the Skill file itself) stating the overlap-check outcome, the testing expectations for `skill-tester`, and any open classification questions for `skill-reviewer`.

## Examples

**Worked example.** A migration plan designates `idempotency` (from an audited source collection) as `NEW`, `skillType: Domain Pattern`, `category: Domain Patterns`, P0. Applying this Workflow: overlap check finds no existing Mentor Skill on this subject (class E); the source material's specific mechanics (a particular payment gateway's transaction-reference field, a particular project's table name) are separated out, leaving the general principle — constraint-backed idempotency via a unique constraint on a caller-supplied idempotency key, not check-then-insert — which is what gets drafted; Required Context posture 2 (benefits from repository context, degrades gracefully without it); Governance Integration states this Domain Pattern content is Advisory unless a specific consuming Review Skill's Rules elevate a violation to a Mandatory-adjacent finding, in which case that classification lives in the *consuming* Skill, not here.

**Negative example (correctly declined).** A request to "make a Skill out of our team's Slack notification format for deploy announcements." Applying step 1: this is a one-time, team-specific convention with no evaluation discipline, authoring workflow, or reusable engineering pattern behind it — it's a fact, not a procedure. Correct outcome: not a Skill; recommend it live as a project-local convention (a child repository's own `.claude/rules/` or a README note), not as Mentor content, and say so rather than drafting a thin Skill to satisfy the request literally.

## Related Skills

- `skills/skill-tester/SKILL.md` — Related, not Dependency: `skill-tester` needs *a* structurally-complete (Implemented-stage) Skill to test, but its own Required Context and Workflow operate on whatever Skill is handed to it — from this Skill's output or from any other source (an existing Production Skill being regression-tested, for instance) — without requiring any specific mechanism from this Skill's own Workflow. Not a true Dependency in either direction.
- `skills/skill-reviewer/SKILL.md` — Related: consumes this Skill's eventual output once Tested, but this Skill does not require anything `skill-reviewer` produces to do its own job.
- `skills/mentor-development/SKILL.md` — Related: supplies the Mentor-vs-child leakage test this Skill applies in Workflow step 1 and Rules → Generalization, Not Copying; this Skill does not restate `mentor-development`'s full content, only cites and applies it.
- `skills/requirements-discipline/SKILL.md` — Related: Rules → Distinguishing Confirmed, Recommended, and Assumed Source Material applies the same CONFIRMED/RECOMMENDATION/ASSUMPTION vocabulary `requirements-discipline` formalizes, narrowed to the specific question of how a source material's confidence label should map onto a drafted Skill's Rule/Constraint/Advisory-guidance/omission — a distinct application, not a restatement of that Skill's full discipline, and not itself a Dependency in either direction.
- `docs/Skill Standard.md`, `docs/Skill Taxonomy.md` — the structural and classification contracts this Skill's Workflow directly implements; not restated here beyond what each Workflow step needs.
