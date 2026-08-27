# Governance Precedence Model

## Status

Authoritative. This document is the single specification for how Mentor governance, child project rules, exceptions, project/feature requirements, and general engineering guidance interact and take precedence over one another. It resolves a specific, previously-identified ambiguity (Section 15) between `docs/Child Repository Integration.md`'s conflict-priority model and `context/core/Mentor Operating Model.md`'s governance model. It does not implement enforcement — see Section 12 (Conflict Resolution — Future Behavior) and Section 16.

Where this document and an earlier one disagree on the *standing precedence* question it resolves, this document governs. Where an earlier document states something this document doesn't address (most notably, how a live, in-session explicit user instruction interacts with a Mandatory rule — see Section 15.3), that earlier document still governs; this phase deliberately does not resolve that separate question.

## 1. Purpose and the Five Categories

Every requirement a Mentor Skill encounters while reviewing or advising on a child repository falls into exactly one of five categories. Keeping them distinct is the foundation everything else in this document builds on — conflating any two of them is the single most common way a precedence question gets confused.

**A. Mentor Governance** — the global rules Engineering Mentor itself defines: Standards, SOPs, Skills, checklists (`context/`). Owned and versioned centrally, per `docs/Child Repository Integration.md` Section 5.

**B. Child Project Rules** — project-specific requirements a child repository declares in `.mentor/rules/`, per `docs/Child Rules and Exceptions.md`. Owned by the child repository.

**C. Exceptions** — explicit, documented deviations from an applicable rule (Mentor's or the child's own), declared in `.mentor/exceptions.yaml`, per `docs/Child Rules and Exceptions.md`. An exception is never a rule and never a governance tier of its own — see Section 9.

**D. Project/Feature Requirements** — requirements that exist for a specific piece of work but aren't standing, persisted governance: a stated constraint on a single review or task ("don't change the public API shape for this PR"), a live user instruction, or a feature-specific decision. These are distinct from Child Project Rules (B) precisely because they aren't persisted in `.mentor/` — they apply to the task at hand, not to the repository as a standing policy. `skills/code-review/SKILL.md`'s existing Constraint Handling rule already handles the single-review version of this category; this document does not change that.

**E. General Engineering Guidance** — professional judgment and best practices not codified as a Mentor or child rule at all — the ambient "this is generally good practice" layer beneath even Informational guidance. See Section 4's Tier 7.

## 2. Rule Classification (Restated, Not Redefined)

`docs/Child Repository Integration.md` Section 7 already defines the four-way classification every Mentor and child rule uses. This document does not redefine it — it is restated here only because precedence (Section 4) depends on it, and repeating the load-bearing sentence in place is clearer than forcing every reader back to Section 7 mid-document:

- **Mandatory** — cannot be weakened, disabled, or overridden short of the exception mechanism (Section 9). Reserved for rules whose violation causes direct security, safety, or data-integrity harm.
- **Configurable** — the rule's existence and outer bounds are fixed; the child selects a specific value within those bounds (Section 6).
- **Advisory** — the child can customize or override it when justified, visibly, without the formal exception mechanism (Section 7).
- **Informational** — reference material only; never blocking, never requiring an override at all.

**This classification applies independently to Mentor's own rules and to a child's own rules.** A rule doesn't inherit its source's authority by classification alone — a Mentor Advisory rule and a Child Advisory rule are both "Advisory," but they sit at different points in the precedence order (Section 4), because *who* wrote the rule matters as much as *how it's classified*.

**The single sentence this whole document exists to make unambiguous:**

> **"Child Mandatory" means mandatory *for the child project*. It does not mean, and has never meant, higher authority than "Mentor Mandatory."**

A child project can make something mandatory for itself. It cannot make something optional for Mentor.

## 3. What Counts as "Security and Safety"

Before the precedence order can be stated precisely, one thing needs pinning down: Section 4 puts "security and safety requirements" at the very top, above even "Mentor Mandatory rules." Is that a separate, competing set of rules, or the same thing stated twice?

**It is the same thing, stated at two levels of concreteness — not two competing tiers.** `docs/Child Repository Integration.md` Section 7 defines Mentor Mandatory as reserved *exactly* for "rules whose violation causes direct security, safety, or data-integrity harm." So in the overwhelming majority of cases, "a security or safety requirement" and "a Mentor Mandatory rule" pick out the same thing: Mentor Mandatory is Mentor's own concrete, documented codification of the security/safety/data-integrity floor.

Tier 1 exists as a distinct line in the model anyway, for one specific reason: **the floor is the principle, not the document.** A security or safety concern doesn't stop being a hard boundary merely because no Mentor Standard has yet written it down as a named Mandatory rule, or because a specific child repository's stack raises a concern generic Mentor guidance hasn't anticipated. Tier 1 is what Tier 2 is *for* — it's the reason Mentor Mandatory rules exist and are non-negotiable, and it remains the backstop in the (rare, and out of this document's scope — see Section 15.3) case where a concrete Mentor Mandatory rule hasn't yet caught up to a real security/safety concern. In ordinary operation, applying Tier 2 (a Mentor Mandatory rule) already applies Tier 1 — you will not usually see them pull in different directions.

This is also why **this document does not oversimplify security into a single line item that can be satisfied and moved past.** "Security and safety requirements" is not one entry to check off — it's the boundary condition every other tier in Section 4 is defined relative to. Every VALID/INVALID example in Sections 5 and 6, every conflict-type definition in Section 10, and every piece of future-enforcement behavior in Section 12 refers back to this boundary, not to a single rule.

## 4. Authoritative Precedence

```text
1. Security and Safety Requirements         (the boundary — see Section 3)
2. Mentor Mandatory Rules                    (Mentor's codification of Tier 1)
3. Child Mandatory Rules                     (mandatory FOR the child project — never outranks 1 or 2)
4. Child Configurable Rules                  (child-selected value within Mentor-defined bounds)
5. Child Advisory Rules / Conventions        (child preference — can override Mentor Advisory when justified)
6. Mentor Advisory Guidance
7. Informational Guidance                    (Mentor's or the child's; includes general engineering
                                               best practices not otherwise codified — Category E)
```

This is the model requested for this phase, verified against the existing documents rather than adopted unmodified — two refinements were made, both explained rather than silently applied:

- **Tiers 4 and 5 are split**, where `docs/Child Repository Integration.md` Section 8 lumped "child project conventions (Configurable/Advisory-level child preferences)" into one tier. The split is a genuine refinement, not a contradiction: Section 7's own definitions already establish that Configurable rules trace back to a Mentor-defined existence and boundary (so they sit closer to Mandatory), while Advisory rules can be overridden without any formal mechanism at all (so they sit closer to Informational). Nothing in Section 8's coarser statement contradicts placing Configurable above Advisory — it simply hadn't been asked to distinguish them.
- **Tier 7 absorbs "general engineering best practices"** rather than keeping it as an eighth, separate tier below Informational (as `docs/Child Repository Integration.md` Section 8's closing entry might be read to imply). Section 2's definition of Informational — "reference material only... never something a child needs to explicitly override because it was never a requirement in the first place" — already comfortably covers ambient professional judgment that was never written down as a specific rule at all. Two tiers doing the same non-blocking, non-authoritative job was judged unnecessary granularity, not a meaningful distinction worth preserving as its own rung.

**Everything from Tier 2 downward is subordinate to Tier 1.** Tiers 3–7 govern how requirements compete with *each other*; none of them can reach past Tier 1 or Tier 2 to weaken them — that is Section 5's subject, not a footnote to this one.

## 5. Child Cannot Weaken Mentor Mandatory

```text
VALID — Additive (Tier 3 adds to Tier 2, does not touch it)
  Mentor Mandatory:  Authentication is required.
  Child Mandatory:   Admin APIs require MFA.
  Result:            Both requirements apply. The child rule adds a requirement
                      on top of Mentor's baseline; it does not substitute for it.

VALID — Additive (a stack-specific instantiation of the same Mentor requirement)
  Mentor Mandatory:  SQL queries must be parameterized.
  Child Mandatory:   All database access must use Prisma services.
  Result:            Both apply. The child rule is a concrete, stack-specific way
                      of satisfying (not replacing) the Mentor requirement — using
                      Prisma services is compatible with "queries are parameterized,"
                      it doesn't stand in for that requirement being met.

INVALID — Prohibited Override (Tier 3 attempts to reach past Tier 2)
  Mentor Mandatory:  Authorization is required.
  Child rule:        /admin does not require authorization.
  Result:            Conflict. The child rule is not a legitimate "Child Mandatory"
                      rule at all, regardless of how it's classified in its own
                      frontmatter — a rule that instructs Mentor to omit an
                      authorization check is an attempted override of a Mentor
                      Mandatory requirement, not a project-specific addition to it.
                      See Section 10's "Prohibited Override" category and Section 12's
                      required handling.
```

The distinguishing test between the first two examples and the third: does the child rule **add a constraint on top of** the Mentor Mandatory requirement being satisfied, or does it **assert that the requirement doesn't need to be satisfied at all** (in full, or within some scope)? The former is always legitimate, regardless of classification. The latter is never legitimate, regardless of what the child rule calls itself.

## 6. Child Can Be Stricter (Additive Governance)

```text
Mentor:  Passwords must be securely handled.
Child:   Passwords must additionally use the project's approved password
         hashing configuration (e.g. a specific Argon2id parameter set).
Result:  Both apply. This is additive governance, not override — the child
         has narrowed how the Mentor requirement is satisfied in this
         project, without asserting the Mentor requirement can be skipped.
```

Additive governance is available at every tier a child rule can occupy (Mandatory, Configurable, or Advisory) and is, in practice, the normal and expected shape of a child rule — see `docs/Child Rules and Exceptions.md` Section 4 and its worked examples (`docs/examples/child-rules/01-api-conventions.md`, `02-database-conventions.md`). A stricter requirement never needs the exception mechanism; the exception mechanism exists for the opposite situation (a deviation, not an addition — Section 9).

## 7. Configurable Rules

A Configurable rule (Mentor's or, in the child's own `.mentor/rules/`, a Child Configurable rule) has two parts: an **existence and outer boundary** Mentor fixes, and a **specific value** the child selects within that boundary. Both parts matter, and only one of them is negotiable:

- The rule's existence, and the boundary Mentor sets around it, are **not** something a child configuration can change.
- The specific value within that boundary **is** something the child selects — e.g. a minimum test-coverage threshold above a Mentor-defined floor, or specific rate-limit numbers where Mentor requires *some* rate limiting.

**A child configuration must never convert a Mentor Mandatory requirement into Advisory or Informational.** Configuring a value is not the same operation as reclassifying a rule, and nothing in `.mentor/project.yaml`, `.mentor/rules/`, or `.mentor/exceptions.yaml` grants a child repository the ability to change a rule's own classification tier — only Mentor, by editing its own Standard, can do that (and per `docs/Versioning Strategy.md`, doing so is at minimum a MAJOR change).

## 8. Advisory Rules

Mentor Advisory guidance can be overridden by a child project's own requirement — an explicit project convention, or a documented rationale where one is appropriate — **without invoking the formal exception mechanism.** This is a deliberate, load-bearing distinction from how Mandatory rules work: requiring an `exceptions.yaml` entry for every Advisory-level preference (e.g. a child preferring one non-security architectural pattern over Mentor's generic recommendation) would turn a lightweight, expected, everyday judgment call into unnecessary process. `docs/Child Rules and Exceptions.md`'s Advisory example (`03-testing-requirements.md`) demonstrates exactly this: a project convention that diverges from generic guidance, stated as a rule, with no exception involved.

The only real requirement on an Advisory override is **visibility, not formality**: the deviation should be stated (in a child rule, in review output, in a documented convention) rather than happening silently. This mirrors `docs/Child Repository Integration.md` Section 7's own description of Advisory: "the override should be visible... not silent."

## 9. Exceptions

**An exception is not a governance tier.** It does not sit "above" or "below" any tier in Section 4 — it is not a rule at all. An exception is an explicit, documented deviation from an *applicable* rule, recorded so the deviation is visible, owned, and bounded, per `docs/Child Rules and Exceptions.md` Sections 8–11 (not restated here — see that document for the full field reference: identifier, affected rule, reason, scope, owner, status, and optional approval/expiration metadata).

**What an exception is not:**

- Not a way to make a Mentor Mandatory rule not apply. It documents that, in a specific, bounded, owned scope, the requirement is knowingly not currently satisfied — the requirement itself, and any finding tied to it, does not disappear because an exception exists (Section 13).
- Not a second, competing governance layer that can be consulted instead of the precedence order in Section 4. Precedence determines which *rule* wins when two apply; an exception is a statement about one specific rule's application in one specific scope, layered on top of whatever precedence already determined applies.

**Ordinary child exceptions and Mentor Mandatory rules.** An ordinary child-recorded exception — the kind `.mentor/exceptions.yaml` supports today — **must not silently disable or downgrade a Mentor Mandatory security/safety requirement.** `docs/Child Rules and Exceptions.md` Section 11 already enforces this structurally (the exceptions schema cannot express a `disable`-style field at all), and this document restates it here because it is the exceptions-side mirror of Section 5's rule-side statement: neither an ordinary child rule nor an ordinary child exception can weaken Tier 1/2.

**On a legitimate security-exception process:** the existing governance documents (`docs/Child Repository Integration.md` Section 17, `docs/Child Rules and Exceptions.md` Section 11) already gesture at the possibility of "a more formal security-exception process" as a *future governance capability*, without defining one. This document does not define one either — inventing an approval workflow, a required reviewer role, or a compliance mechanism here would be inventing governance behavior no existing document specifies, which the No Invention Rule (`context/core/Mentor Operating Model.md`) prohibits. If such a process is needed, it is future work, to be designed deliberately when it's actually needed — not backfilled speculatively into this document.

## 10. Conflict Types

Every time two requirements are compared, the relationship between them falls into exactly one of six categories:

| # | Category | Definition |
|---|---|---|
| 1 | **Compatible** | Both requirements can be satisfied simultaneously, with no tension between them. |
| 2 | **Additive** | The lower-tier requirement is stricter than, but fully compatible with, the higher-tier one — it narrows how the higher-tier requirement is satisfied without contradicting it (Section 6). |
| 3 | **Override** | A higher-tier-in-context requirement (a valid child convention overriding Mentor Advisory guidance, per Section 8) intentionally and legitimately replaces lower-priority guidance. Only available where the thing being replaced permits it — see Section 8; not available against Tier 1/2. |
| 4 | **Conflict** | The two requirements cannot both be satisfied, and neither is a Mandatory-security-boundary case — a genuine, ordinary disagreement between two legitimate requirements (e.g. two Advisory-level preferences from different sources pulling in different directions). |
| 5 | **Prohibited Override** | A child rule or exception attempts to weaken, disable, or bypass a Mentor Mandatory security/safety requirement (Section 5's INVALID example; Section 9's exceptions boundary). |
| 6 | **Unknown** | Available context is insufficient to determine which of the above categories applies. |

## 11. Conflict Resolution — Future Behavior (Documentation Only)

**Nothing in this phase implements any of the following.** (`scripts/evaluate_governance.py`, added in a later phase, implements this table's classification step as code -- see `docs/Governance Evaluation.md`. It implements *classification only*: it does not act on the result, does not suppress or downgrade any finding, and does not make this section's "Expected future handling" column true end-to-end -- a calling Skill still decides what to do with a returned classification, exactly as this section anticipates.) This section documents the *expected, deterministic behavior* a future enforcement phase must produce, so that phase has a specification to build against rather than inventing resolution logic under time pressure — mirroring exactly how `docs/Child Rules and Exceptions.md` Section 15 scoped its own deferred enforcement work.

| Conflict type | Expected future handling |
|---|---|
| Compatible | Apply both. |
| Additive | Apply both. |
| Override (valid) | Use the child/project requirement; the replaced guidance is not reported as a separate, competing finding. |
| Conflict (true) | Surface the conflict explicitly — do not silently pick a side. Both requirements, and the fact that they disagree, should be visible to whoever is reviewing the output. |
| Prohibited Override | Preserve the Mentor Mandatory requirement (the finding is reported at its correct severity, exactly as if no child rule/exception existed) **and** surface the child conflict explicitly — the child's attempted override becomes visible information, not a silent failure and not a silently honored request. This mirrors `skills/code-review/SKILL.md`'s existing Constraint Handling rule for a single stated request to bypass security, generalized here to standing child governance. |
| Unknown | Do not invent a resolution. Report that available context is insufficient to classify the relationship — the same "Missing Evidence" discipline `skills/code-review/SKILL.md`'s Severity Under Incomplete Surrounding Context rule already applies to findings, applied here to conflict classification instead of to severity. |

## 12. Governance Classification vs. Finding Severity

**These are two different dimensions and must never be conflated.**

- **Governance classification** — Mandatory / Configurable / Advisory / Informational — describes a *rule's* standing authority: how binding it is, and who (Mentor or a child) can adjust it and how.
- **Finding severity** — CRITICAL / HIGH / MEDIUM / LOW / INFO, per `context/standards/Severity Taxonomy.md`, which remains the sole, unmodified, authoritative source for severity — describes a *specific instance's* actual impact, as determined by the evidence in front of the reviewer.

**Classification does not determine severity, and severity does not determine classification.** Two examples, directly from this phase's brief:

- A **Child Advisory** rule can still be the thing that surfaces a **CRITICAL** finding — if the actual code violates a Mentor Mandatory security requirement, that finding is CRITICAL because of what the code does, not because of how the rule that happened to prompt someone to look was classified. The Advisory rule might be "prefer integration tests over deep mocking" (`docs/examples/child-rules/03-testing-requirements.md`); the CRITICAL finding it leads a reviewer to notice while reading that code might be an unrelated SQL injection. Classification and severity travel independently.
- A **Mentor Mandatory** governance rule does not mean every violation of it is automatically **CRITICAL**. `context/standards/Severity Taxonomy.md` already establishes that severity is evidence-based (see, for example, `skills/code-review/SKILL.md`'s Severity Under Incomplete Surrounding Context and Severity for Availability/Resource-Exhaustion rules) — a Mandatory authentication requirement being unmet might, depending on the actual exposure and evidence, be assessed CRITICAL or HIGH; the classification "Mandatory" tells you the requirement is non-negotiable, not what number it gets.

The practical implication for a future enforcement phase: governance classification determines *whether a deviation is even permitted, and by what mechanism* (Sections 4–9 of this document). Finding severity determines *how urgent a specific instance is*, per the unmodified Severity Taxonomy. A Mandatory rule with no exception on file is always non-negotiable regardless of the severity ultimately assigned to a specific violation of it; that severity is still computed the normal, evidence-based way.

## 13. Exceptions vs. Finding Severity

An exception does not automatically change the intrinsic severity of a finding. Recording `.mentor/exceptions.yaml` entry `X` for rule `Y` does not, in this phase, cause any Skill to compute a lower severity, omit a finding, or relabel a CRITICAL as anything else — because no Skill in this repository currently reads exceptions and acts on them at all (`docs/Child Rules and Exceptions.md` Section 15; `docs/Context Discovery.md` discovers and structurally validates exceptions, and stops there).

When exception-aware enforcement is eventually built, this document's position is that an approved, applicable exception changes how a finding is **presented** (e.g. annotated as "known, approved, accepted risk" rather than appearing as a fresh, unacknowledged CRITICAL) — it does not, and per Section 9 and `docs/Child Rules and Exceptions.md` Section 11 cannot, make the underlying requirement disappear or silently downgrade the finding's actual severity for a Mentor Mandatory rule. That distinction — annotate vs. suppress/downgrade — matters enough to state now, even though implementing either behavior is out of scope for this phase.

## 14. What This Document Changes at Runtime

Nothing. No Skill was modified by this phase. No finding severity changes because this document exists. No rule matching, exception matching, or conflict detection is performed by any script or Skill as a result of this document. Every "Result" and "expected handling" statement above describes intended future behavior, explicitly not implemented here — see Section 16.

## 15. Resolving the Pre-Existing Ambiguity

### 15.1 The ambiguity, precisely

Three documents in this repository state a conflict-priority order, and prior to this phase they did not agree:

**`docs/Child Repository Integration.md` Section 8/18** (most detailed, most recent before this phase):
```text
1. Security and safety requirements
2. Mentor Mandatory rules
3. Child Mandatory project constraints
4. Child project conventions (Configurable/Advisory-level child preferences)
5. Mentor Advisory rules
6. General engineering best practices
```

**`context/core/Mentor Operating Model.md`** ("Conflict Resolution," coarse, predates the four-way classification):
> "Project-specific requirements can override generic Mentor guidance when justified. Security requirements and explicit user requirements remain highest priority."

**`skills/mentor-development/SKILL.md`** (also predates the four-way classification):
```text
1. Explicit user request
2. Security and safety requirements
3. Child repository requirements and architecture
4. Engineering Mentor global standards
5. General engineering best practices
```

The real conflict is not merely stylistic. Both the Operating Model and `mentor-development`'s statements treat "generic Mentor guidance" / "Engineering Mentor global standards" as a **single, undifferentiated tier** that project-specific/child requirements can override "when justified" — with no distinction between a Mentor Advisory recommendation and a Mentor Mandatory rule. Read literally, `mentor-development`'s ordering places tier 3 ("child repository requirements and architecture," undifferentiated) *above* tier 4 ("Engineering Mentor global standards," undifferentiated) — which would let an ordinary child requirement outrank a Mentor Mandatory rule whose subject matter isn't literally "security and safety" in the narrowest reading (e.g. a Mandatory data-integrity rule, which Section 7's own definition of Mandatory includes alongside security and safety). That is a direct contradiction of the Contract's Section 8, which never permits any child tier to outrank Mentor Mandatory.

### 15.2 The resolution

**This document (`docs/Governance Precedence Model.md`) is now the single authoritative source for the *standing, structural* precedence question** — how Mentor's own rules and a child repository's declared rules relate to each other as persisted governance. Section 4's seven-tier model supersedes the Operating Model's and `mentor-development`'s undifferentiated "generic Mentor guidance" framing for this question, for exactly the reason Section 15.1 identifies: an undifferentiated tier cannot express "Mentor Mandatory never loses to a child rule," and that invariant is non-negotiable (Section 5).

The resolution is not a rewrite of either older document's content — it is a **scoping clarification**, made explicit by cross-reference (Section 15 of this task; see the file changes listed in the accompanying report): the Operating Model's and `mentor-development`'s statements were never wrong about the two things they actually say clearly (security and explicit user requests sit very high; child projects can justifiably diverge from *generic* guidance) — they simply predate, and were never updated to reflect, the Mandatory/Configurable/Advisory/Informational classification that makes "child can override Mentor" a *tier-dependent* statement rather than a blanket one. This document supplies that missing tier-dependence; it does not claim the older statements were making a different point than they were.

### 15.3 What this resolution deliberately does not touch

**The "explicit user request" tier is not addressed by this document, on purpose.** All three source documents place "explicit user request" (or, in the Contract's case, silence on it, explicitly flagged as such) somewhere in their model, but none of them — and neither does this document — resolve how a *live, in-session* instruction interacts with a *standing* Mentor Mandatory rule. `docs/Child Repository Integration.md` Section 8 already drew this exact line: "This priority order governs the standing, structural relationship between Mentor rules and a child's declared configuration. It is distinct from, and does not itself resolve, how a live, in-session explicit user instruction interacts with a Mandatory Mentor rule." This phase's task was scoped to "resolve ONLY this ambiguity" (the Contract-vs-Operating-Model standing-governance question) — the explicit-user-request question is a different question, about a different axis (live instruction vs. persisted repository configuration), and remains exactly as unresolved after this document as it was before it. It is listed as a still-open item, not silently decided, in the interest of not overstepping this phase's scope.

## 16. Enforcement — Future Phase

Consistent with `docs/Child Rules and Exceptions.md` Section 15's framing, everything below is explicitly deferred:

- Detecting that two specific requirements actually apply to the same code/finding (requires rule matching and exception matching — both explicitly out of scope this phase).
- Classifying a detected pair into one of Section 10's six conflict types automatically.
- Executing Section 11's "expected future handling" column against a real finding.
- Annotating a finding as "covered by an approved exception," per Section 13.
- Any Mentor-version compatibility blocking based on this model.
- Any Skill change that consumes this document to alter its own behavior. `skills/code-review/SKILL.md`'s existing context-discovery hook and Constraint Handling rule are unmodified by this phase and remain the only place *any* Mentor Skill currently reasons about a project-specific requirement — and that reasoning is still scoped to a single stated, in-request constraint, not to standing `.mentor/rules/` or `.mentor/exceptions.yaml` content.

This document's job was to make the *specification* deterministic and internally consistent — including resolving where it previously wasn't (Section 15) — so that whichever future phase builds enforcement is building against one settled model, not reconciling three different ones for the first time under implementation pressure.
