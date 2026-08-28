# Skill Taxonomy

## Status

Authoritative. This is Mentor's first Skill Taxonomy — no prior version exists to supersede (`SKILL_GAPS.md`, in the `mentor-skills-source` audit, confirmed no `docs/Skill Taxonomy.md` existed in this repository before this document, per that audit's explicit instruction to state so rather than treat something else as equivalent). Categories, Skill Types, and the overlap-classification vocabulary below are taken directly from that audit's own working taxonomy (`SKILL_GAPS.md` Section 12) and overlap analysis (`SKILL_OVERLAP.md`), per this phase's instruction to use the audit's findings rather than invent a parallel scheme. Where this document differs from the audit's proposal, the difference and its reason are stated explicitly (see Section 4).

## 1. The Four Skill Types

Every Skill has exactly one `skillType`, declared in frontmatter per `docs/Skill Standard.md` Section 1.

- **Mentor Core** — governs how Engineering Mentor itself, or the Skills within it, are built, reviewed, tested, and maintained. Does not advise on a child repository's code directly. Existing examples: `mentor-development`, `skill-creator`, `skill-reviewer`, `skill-tester`, `context-discovery`.
- **Review** — evaluates an existing change, repository, or artifact and produces findings (per `context/templates/Review Template.md`, tagged with `context/standards/Severity Taxonomy.md`'s five levels). Operates against real repository context — see `docs/Skill Standard.md` Section 3, posture 3. Existing examples: `code-review`, `architecture-review`, `database-review`, `security-review`, `performance-review`, `testing-review`.
- **Authoring/Workflow** — produces a new artifact or walks a defined process to a defined output, rather than evaluating an existing one. No existing Mentor Skill is purely this type today (`api-design`'s stub currently reads more like a thin Review skill than an authoring one — see Section 4's rename note); the `mentor-skills-source` audit identified this as Mentor's most under-built Skill Type despite being common in that source collection (`api-testing`, `swagger-openapi`, `srs-scope-rules`, `technical-documentation` were all this shape there).
- **Domain Pattern** — reusable design-pattern or engineering-concept guidance, illustrative rather than prescriptive of one stack, consumed by Review and Authoring/Workflow Skills as reference material rather than invoked directly as an end-to-end workflow. No existing Mentor Skill is this type today; `idempotency`, `soft-delete`, and `uuid-strategy` in `mentor-skills-source` are the strongest examples of what a well-built one looks like, once stripped of their originating project's specifics (`SKILL_QUALITY_REPORT.md`'s Import Recommendation column, in that audit, for exactly those three).

## 2. How the Four Types Compose

```text
Mentor Core
  governs how every other type is built, tested, reviewed, and certified
  (docs/Skill Standard.md, docs/Skill Testing Standard.md,
   docs/Skill Quality Standard.md, this document)
        │
        ▼
Domain Pattern  ──consumed as reference material by──▶  Review
     (illustrative,                                    (evaluates real
      no artifact of                                    repository/change
      its own)                                           against Mentor +
        │                                                 child governance,
        │                                                 produces findings)
        ▼                                                      ▲
Authoring/Workflow ──produces the artifact a────────────────────┘
   (produces a new                Review Skill later evaluates
    artifact or decision,
    following a defined
    process)
```

A Domain Pattern Skill is never invoked end-to-end on its own against a real repository the way a Review or Authoring/Workflow Skill is — it supplies the *pattern* (e.g. "constraint-backed idempotency, not check-then-insert") that an Authoring/Workflow Skill applies when producing something, and that a Review Skill checks for when evaluating something already produced. This is the structural reason `docs/Skill Standard.md` Section 4 requires Domain Pattern content to declare its governance tier (Mandatory-floor vs. Advisory pattern) explicitly — a Review Skill consuming it needs to know which, to classify a finding correctly.

An Authoring/Workflow Skill's output becomes exactly the kind of artifact the matching Review Skill evaluates — `api-contract-design`'s eventual output (once built — see Section 4) is what `api-review`'s eventual depth (once built — see Section 4) would evaluate. This pairing is deliberate and should be preserved when either Skill in a pair changes.

## 3. Categories

The domain-topic category list, applied via `docs/Skill Standard.md`'s `category` frontmatter field. Unchanged from the audit's list — no category was force-fit there and none is force-fit here:

```text
Mentor Core, Core Engineering, Architecture, Backend, Frontend, API, Database,
Security, Testing, Performance, DevOps/Cloud, Observability, Distributed Systems,
Data, Integrations, AI/LLM, Domain Patterns, Documentation, Requirements, Review
```

A Skill may reasonably span two categories (e.g. `database-performance`-shaped content as "Database / Performance") — `docs/Skill Standard.md`'s `category` field takes the single primary category; a secondary category, where genuinely useful, is stated in the Skill's own `Scope` section rather than added as a second frontmatter value, to keep the field itself a clean single source for tooling (`scripts/validate_skill.py`'s enum check).

**`category: Review` and `skillType: Review` use the same word for two independent axes, deliberately, not redundantly.** `skillType: Review` (Section 1) is structural: the Skill evaluates existing material and produces findings, regardless of topic. `category: Review` is topical: general, cross-cutting code review as a subject in its own right, distinct from a domain-specific one like Database or Security. `code-review` carries both values because it is structurally a Review-type Skill whose topic *is* general review; `database-review` is also `skillType: Review` but `category: Database`, not `category: Review`. Whether `category: Review` should exist at all, given `skillType` already carries the word, is an open question this document does not resolve — it is carried into this phase's report as an unresolved item rather than decided unilaterally here.

**Coverage status today** (from `SKILL_GAPS.md` Section 11 of the `mentor-skills-source` audit, cross-checked against `docs/Skill Ecosystem Inventory.md`): Architecture, Backend, API, Database, Security, Testing, Performance have at least a stub Review-type Skill. Requirements, Documentation, Integrations, AI/LLM have **no** Mentor Skill at all. Frontend, DevOps/Cloud, Observability, Distributed Systems, Data have **no** Mentor Skill at all and no ready source material to build one responsibly yet — see `docs/Skill Ecosystem Inventory.md` for the full current-state table.

## 4. Naming Conventions

Restated from `docs/Skill Standard.md` Section 6: `name` must equal the Skill's directory name, exactly. This section adds the naming *pattern* expected per Skill Type, so a Skill's name signals its type before a reader opens the file:

- **Review** — `<domain>-review` (`code-review`, `security-review`, `database-review`). **Exception carried forward from the existing repository, not resolved by this document:** `api-design` is today a Review-type stub but does not follow this pattern. `SKILL_OVERLAP.md`'s recommendation (in the `mentor-skills-source` audit) to split it into `api-review` (Review-type, renamed) plus a new `api-contract-design` (Authoring/Workflow-type) is recorded here as the taxonomically correct target shape — implementing that rename is a Skill-level change, out of scope for this document (see this document's own Status section: standards only, no Skill created or rewritten here).
- **Authoring/Workflow** — `<domain>-<noun>` describing the artifact or process (`api-contract-design`, `requirements-discipline`, `documentation`, `integration-adapter-pattern` — the four candidates `SKILL_GAPS.md` Section 12 proposes, none yet built).
- **Domain Pattern** — named after the pattern itself, not a domain (`idempotency`, `soft-delete-and-lifecycle`, `identifier-strategy`, `dynamic-configuration-engine` — again, `SKILL_GAPS.md` Section 12's proposal, none yet built).
- **Mentor Core** — `mentor-<noun>` or `skill-<verb>` for the meta-skills governing Skills specifically (`mentor-development`, `skill-creator`, `skill-reviewer`, `skill-tester`), or a descriptive noun for a standing capability (`context-discovery`).

## 5. Overlap / Duplication Rules

Before proposing a new Skill (`docs/Skill Taxonomy.md` Section 7, Lifecycle stage 1), check `docs/Skill Ecosystem Inventory.md` and this document's Section 3 category table for existing coverage. If a candidate topic overlaps something that already exists, classify the overlap using exactly the five categories `SKILL_OVERLAP.md` (in the `mentor-skills-source` audit) established and resolve per this table — reused verbatim, not reinvented:

| Overlap class | Definition | Required resolution |
|---|---|---|
| A. Exact duplicate | Same name, same content coverage | Do not create. Use the existing Skill. |
| B. Strong overlap | Same subject, different depth or shape (e.g. a generic stub vs. a concrete worked treatment) | Do not create a second Skill on the same subject. Grow the existing Skill's depth instead — this is the disposition `SKILL_OVERLAP.md` gave every one of its six strong-overlap findings against `mentor-skills-source`. |
| C. Partial overlap | Shares a sub-topic but has a genuinely distinct primary purpose | May proceed as a separate Skill, but its `Related Skills` section (and the overlapping existing Skill's) must state the boundary explicitly, in both directions. |
| D. Complementary | Occupies clearly different ground despite topical proximity (e.g. a Review Skill and the Authoring/Workflow Skill producing what it reviews) | Proceed. Cross-reference in `Related Skills`, no boundary statement needed beyond the type distinction itself. |
| E. No meaningful overlap | Nothing else covers this ground | Proceed. This is also the trigger to check whether the gap is one of Section 3's "no Skill at all" categories, worth flagging in a future `SKILL_GAPS.md`-style capability review rather than treated as this Skill's problem alone to solve. |

This table's job is to make merge-vs-split-vs-proceed a checked decision every time, not a judgment call redone from scratch per Skill — the same reasoning `docs/Governance Evaluation.md` gives for extracting a fixed classification function out of prose once, rather than re-deriving it per invocation.

## 6. Relationship to Mentor's Broader Structure

A Skill is one of several things `context/` and `docs/` already distinguish (`context/core/Mentor Operating Model.md`'s "Mentor Responsibilities" list: principles, architecture guidance, standards, SOPs, Skills, Agents, checklists, templates). This Taxonomy governs Skills specifically. It does not redefine when something belongs in a Standard versus a Skill — `skills/mentor-development/SKILL.md`'s existing leakage test ("would this guidance make sense verbatim in an unrelated repository on a different stack?") already answers the Mentor-vs-child question; the Skill-vs-Standard-vs-SOP question is a separate one this document does not attempt to resolve, since no evidence from the `mentor-skills-source` audit bears on it.

## 7. Lifecycle — Drafting, Implementing, Testing, Reviewing, Certifying, and Producing

Seven stages, in this order — **Draft → Implemented → Tested → Reviewed → Certified → Production → Deprecated.** **Policy clarification (Phase 19):** Certified (stage 5) is an *optional* high-assurance gate, not a required step for an ordinary internal Skill — the normal internal production path is Reviewed (stage 4) → Production (stage 6) directly. Certified is reserved for cases such as security-critical Skills, externally distributed Skills, regulated/compliance use, major architectural Skills, or a Skill an owner explicitly designates as requiring formal independent sign-off; see `docs/Skill Certification Process.md`'s own policy clarification for the same list. This does not change stage 5's own requirements for a Skill that does pursue Certified. Testing precedes Review deliberately: `docs/Skill Quality Standard.md`'s ten dimensions include Test Coverage, and scoring that dimension before fixtures exist would be scoring nothing — so a Skill's test evidence must exist before a reviewer scores it, not after.

1. **Draft.** Check Section 5's overlap table against `docs/Skill Ecosystem Inventory.md`. Draft `Purpose`, `Scope`, `When to Use` per `docs/Skill Standard.md` before writing anything else — `skills/skill-creator/SKILL.md`'s own step 1.
2. **Implemented.** Full structure per `docs/Skill Standard.md` Section 1, using `skills/skill-creator/SKILL.md`. Passes `scripts/validate_skill.py` (structural validity — Section 5 of `docs/Skill Standard.md`) before moving to the next stage.
3. **Tested.** Using `skills/skill-tester/SKILL.md` and `docs/Skill Testing Standard.md` — fixtures added for every required scenario category, including the governance-relationship set for a Review-type Skill, before the Skill is reviewed. A failure discovered here goes through `docs/Skill Testing Standard.md` Section 4's regression sequence before re-entering this stage.
4. **Reviewed.** Using `skills/skill-reviewer/SKILL.md` — scope, clarity, contradictions, missing edge cases, unintended behavior, and Section 5's overlap check re-verified against the *actual* drafted content, not just the proposal. Scored against `docs/Skill Quality Standard.md`'s ten dimensions, now including a real Test Coverage score against the fixtures Stage 3 produced.
5. **Certified.** `docs/Skill Quality Standard.md` Section 3's certification threshold is met and formally signed off by whoever approves the change. This is the quality gate; clearing it does not by itself make the Skill live — see Production. **Proposed clarification (Phase 15, not yet adopted by any actual certification):** this clause names "whoever approves the change" without defining the role or its independence requirement anywhere in this document. `docs/Skill Certification Process.md` proposes the Author/Tester/Reviewer/Certifier/Approver role split and the independence test this sign-off requires — read that document alongside this one before treating any Skill as eligible for this stage; it does not lower or redefine this stage's requirement, only makes concrete what "signed off" and "whoever approves" mean in practice.
6. **Production.** The Skill is added to `docs/Skill Ecosystem Inventory.md` as live Mentor content, and `docs/Versioning Strategy.md`'s MINOR version rule applies (a new Skill is a backward-compatible addition). A Skill stays in this stage while actively maintained: a change affecting behavior re-enters at Tested (stage 3) at minimum, and any other material change re-enters at Reviewed (stage 4) at minimum, per the regression discipline in `docs/Skill Testing Standard.md` Section 4 — never applied directly to a live Skill without going back through the gate it would otherwise bypass. `docs/Skill Ecosystem Inventory.md` is updated in the same change, never left to drift — `SKILL_GAPS.md`'s own finding (in the `mentor-skills-source` audit) that no prior `docs/Skill Ecosystem Inventory.md` existed for this repository is the exact failure mode this stage exists to prevent going forward.
7. **Deprecated.** A Production Skill that is retired or superseded (merged into a broader Skill per Section 5's class-B resolution, or replaced by a better one) is marked Deprecated in `docs/Skill Ecosystem Inventory.md` rather than silently deleted — a documentation-only change (`docs/Versioning Strategy.md` PATCH or MINOR, depending on scope). Actually removing a Deprecated Skill's file from `skills/` afterward is a breaking change for any consumer still selecting it by name, and follows `docs/Versioning Strategy.md`'s MAJOR rule instead.

A Skill can also exit this lifecycle before Certified as **Merged** (folded into an existing Skill's depth per Section 5's class-B resolution), **Deferred** (real value, not yet ready — insufficient generalizable content, or blocked on a dependency), or **Rejected** (would encode project-specific business knowledge in global Mentor content, per `context/core/Mentor Governance Rules.md`, or duplicates existing coverage per Section 5 class A). `SKILL_QUALITY_REPORT.md`'s Import Recommendation column, in the `mentor-skills-source` audit, is a worked example of all six outcomes (Keep/Import, Improve-Then-Import, Merge, Split, Reclassify, Defer, Do-Not-Import) applied at once to 30 real candidates — read alongside this section for what each disposition looks like in practice.

## Related

- `docs/Skill Standard.md` — the structural contract Section 1's diagram and Section 4's rename note both reference.
- `docs/Skill Testing Standard.md`, `docs/Skill Quality Standard.md` — the gates Section 7's lifecycle stages 3 (Tested), 4 (Reviewed), and 5 (Certified) depend on.
- `docs/Skill Ecosystem Inventory.md` — the living record this Taxonomy is checked against (Section 5) and updated alongside (Section 7).
- `skills/skill-creator/SKILL.md`, `skills/skill-reviewer/SKILL.md`, `skills/skill-tester/SKILL.md`, `skills/mentor-development/SKILL.md` — the existing Mentor Core Skills that execute this lifecycle's stages; unchanged by this document.
