# Child Repository Integration Contract

## 1. Purpose

This document is the formal contract that governs how the Engineering Mentor plugin integrates with independent child software repositories. It defines what Mentor controls globally, what a child repository may customize, how the two layers compose at review time, how Mentor is distributed and versioned, and how conflicts between Mentor rules and child requirements are resolved deterministically.

This Contract formalizes and extends the relationship already established in `context/core/Mentor Operating Model.md` ("Mentor answers *how should this be engineered?*; a child repository answers *what does this system do, and what constraints does this project have?*"). It does not replace that document — it is the detailed specification for the integration surface between the two.

## 2. Scope

Applies to: any child repository that installs the `engineering-mentor` plugin (via Google Antigravity or Claude Code) and wants Mentor Skills, Agents, standards, and SOPs to operate with awareness of that repository's actual stack, architecture, and constraints.

Does not apply to: development *of* the Mentor plugin itself (that is `skills/mentor-development/SKILL.md`'s scope), and does not define or create any child-side files — per this task's constraints, no `.mentor/` directory is created in this repository. Everything under "Child Repository Contract" (Section 9) below is a specification for what a child repository should contain, not something implemented here.

## 3. Design Principles

- Mentor is centrally governed; a child repository consumes it, it does not fork or duplicate it.
- Child repositories provide project-specific context; that context supplies inputs to Mentor Skills, it does not replace Mentor governance.
- Child-specific behavior extends Mentor guidance rather than cloning or reimplementing it.
- Mandatory Mentor security and safety rules cannot be weakened by child configuration, child convention, or child-specific Skills.
- Any deviation from Mentor governance must be explicit, via the exception mechanism (Section 17) — never silent.
- Configuration must be deterministic: the same Mentor version plus the same child declaration must produce the same governance outcome.
- Skills consume child context progressively (Section 12) rather than loading an entire repository indiscriminately.
- Avoid unnecessary repository duplication — a child does not clone or vendor Mentor content into its own tree (Section 16).
- Global governance stays separate from project implementation detail: the Mentor Operating Model's Separation Principle applies here without modification.
- Machine-readable configuration (YAML) is used where automation needs structured data; Markdown is used for human-readable architecture and rules.
- This Contract intentionally does not over-engineer the initial integration surface — several concrete schemas are explicitly deferred (Section 22).

These principles are additive to, and must not contradict, the Mentor Operating Model's existing Reuse Principle, Separation Principle, and No Invention Rule.

## 4. Governance Model

Engineering Mentor governance operates across three levels:

```text
LEVEL 1 — MENTOR GLOBAL
    Global engineering governance, mandatory security baselines,
    mandatory quality/safety rules, global standards, shared Skills,
    Agents, SOPs, templates, and engineering principles.
    Owned and versioned by this repository.

LEVEL 2 — CHILD PROJECT
    Project-specific technology stack, architecture, domain knowledge,
    conventions, implementation patterns, testing strategy,
    deployment model, and approved project-specific behavior.
    Owned by the child repository, declared via .mentor/ (Section 10).

LEVEL 3 — CHILD LOCAL / FEATURE
    Feature-specific requirements and local implementation decisions
    made in the course of a single change (a PR, a diff, a single
    review). Not persisted as standing configuration.
```

The hierarchy is strict in one direction only: Level 2 and Level 3 may add detail, narrow choices within Mentor-defined boundaries, and supply context Mentor cannot infer on its own — but neither level may weaken a Level 1 rule classified as Mandatory (Section 7). This is the single non-negotiable invariant of this Contract; every other rule in this document is downstream of it.

## 5. Mentor Global Responsibilities

Per `context/core/Mentor Operating Model.md`'s "Mentor Responsibilities," the Mentor owns:

- Engineering and architecture principles (`context/core/`)
- Standards for API/backend, database, security, performance, testing, code review, git/change management, and severity (`context/standards/`)
- SOPs for feature development, bug fixing, debugging, refactoring, API/database changes, production release, and security review (`context/sop/`)
- Shared Skills, exposed under the `/engineering-mentor:<name>` namespace (`skills/`)
- Agents providing reusable engineering expertise (`agents/`)
- Checklists and templates (`context/checklists/`, `context/templates/`)
- Skill/Agent development and evaluation standards (`context/skills/`, `context/agents/`)
- Engineering quality gates that apply across repositories regardless of stack

This list is descriptive of the existing repository structure, not a new grant of authority — it restates what `README.md` and the Mentor Operating Model already establish, for this Contract's own completeness.

## 6. Child Repository Responsibilities

Per the same source, a child repository owns:

- Business/domain knowledge
- Project architecture and repository structure
- Technology stack (declared per Section 8)
- Project-specific conventions and implementation patterns
- Project-specific Skills, Agents, and rules (Section 13)
- API contracts and database schema
- Testing strategy and deployment model
- Approved project-specific behavior that stays within Mentor-defined boundaries (Section 7)

A child repository never owns, and cannot redefine, a Mandatory Mentor rule.

## 7. Mandatory / Configurable / Advisory / Informational Rules

Every Mentor rule — every requirement stated in a Standard, SOP, checklist, or Skill — conceptually belongs to exactly one of four categories:

### Mandatory
The child cannot weaken, disable, or override it, under any configuration or justification short of the explicit exception mechanism (Section 17). Reserved for rules whose violation causes direct security, safety, or data-integrity harm.
Examples, drawn from `context/standards/Security Standards.md` and the CRITICAL/HIGH tiers of `context/standards/Severity Taxonomy.md`: injection prevention, secrets protection (never hardcoding credentials or exposing them in logs/responses), authentication/authorization on sensitive operations, never trusting client-provided identity/role/ownership/pricing/privileged flags.

### Configurable
The child can adjust the behavior, but only within boundaries Mentor itself defines. The rule's existence and its outer bounds are not negotiable; the specific value within those bounds is.
Examples: a required minimum test-coverage threshold where the child selects the exact number above a Mentor-defined floor; a required rate-limiting control where the child selects the specific limits; a mandatory code-review severity/blocking policy where the child may tighten (never loosen) the default blocking threshold from `context/standards/Severity Taxonomy.md`.

### Advisory
The child can customize or override it when justified, without needing the formal exception mechanism — but the override should be visible (stated in child rules or the review output), not silent. Most of `context/checklists/` and stylistic portions of `context/standards/Engineering Standards.md` fall here.
Examples: preferred architectural patterns, specific SOP step ordering, non-security performance recommendations (e.g. an N+1 query on a low-traffic, non-sensitive path per the Severity Taxonomy's MEDIUM tier), general engineering best practices.

### Informational
Guidance and reference material only — never blocking, never something a child needs to explicitly override because it was never a requirement in the first place.
Examples: `context/templates/`, worked examples inside Skills, and Severity Taxonomy's INFO tier (style notes, alternative-approach suggestions, positive observations).

This four-way classification is new to this Contract. No existing Standard or SOP file currently tags its individual rules with one of these four labels — see Section 22 (Future Implementation Work) and the ambiguity noted in the accompanying summary for this task.

## 8. Governance and Override Rules

Deterministic conflict-resolution order, applied whenever a Mentor rule and a child requirement genuinely conflict:

1. Security and safety requirements
2. Mentor Mandatory rules
3. Child Mandatory project constraints (declared via `.mentor/rules/`, Section 10)
4. Child project conventions (Configurable/Advisory-level child preferences)
5. Mentor Advisory rules
6. General engineering best practices

**A child project must not use a project-specific rule to weaken, disable, or bypass a Mentor Mandatory security or safety requirement.** This is absolute — it is not one factor to weigh against others in the list above, it is a precondition on the list applying at all. If a legitimate conflict exists between a child's actual constraints and a Mentor Mandatory rule, the child uses the exception mechanism (Section 17) rather than silently overriding the rule, and an exception never disables a security requirement outright — it documents a scoped, owned, reasoned, time-bounded deviation.

This priority order governs the standing, structural relationship between Mentor rules and a child's declared configuration. It is distinct from, and does not itself resolve, how a live, in-session explicit user instruction interacts with a Mandatory Mentor rule — see the ambiguity called out in this task's summary regarding the existing "explicit user request" priority already established elsewhere in this repository.

**This order is now the subject of a dedicated, authoritative specification:** `docs/Governance Precedence Model.md` restates and refines this priority order (splitting "child project conventions" into Configurable and Advisory tiers, and resolving a prior inconsistency with `context/core/Mentor Operating Model.md`'s coarser conflict-resolution statement — see that document's Section 15). This section's order remains correct as a summary; `docs/Governance Precedence Model.md` is the authoritative, detailed version, including precise definitions of what counts as a conflict, an override, and a prohibited override.

## 9. Child Repository Contract

A child repository that wants Mentor Skills to operate with full project awareness is expected to provide the following, conceptually, inside its own repository (not created here):

```text
child-repo/
├── .mentor/
│   ├── project.yaml
│   ├── architecture.md
│   ├── exceptions.yaml
│   └── rules/
└── src/
```

This supersedes the placeholder child structure previously sketched in this same file (which referenced `.claude/skills/`, `.claude/agents/`, and `.claude/rules/` at the child's top level, predating this repository's own migration to the plugin `skills/`/`agents/` layout). A child repository may still maintain its own project-specific Skills/Agents/rules under `.claude/` per current Claude Code plugin/project conventions — that is orthogonal to `.mentor/`, which exists specifically to declare project context and governance exceptions for the Engineering Mentor plugin, not to hold the child's own Skills. Section 13 describes how child-owned Skills and Mentor Skills coexist.

## 10. .mentor Directory

Each file's responsibility:

- **`project.yaml`** — the machine-readable project profile: name, declared Mentor version compatibility range, technology stack, architecture style, testing tools, deployment model. Consumed first, and consumed by automation (Section 12). See Section 11 and `docs/Project Profile Schema.md` for the finalized schema.
- **`architecture.md`** — human-readable architecture narrative: what the system does, its major components, its data flow, and any architectural context a machine-readable profile can't capture concisely. Read by Mentor Skills and by Claude directly, the same way `context/` is read in this repository.
- **`exceptions.yaml`** — the record of every explicit, approved deviation from a Mentor rule. See Section 17. **Schema finalized:** see `docs/Child Rules and Exceptions.md` and `docs/schema/exceptions.schema.v1.json`.
- **`rules/`** — child-specific rules that are Mandatory, Configurable, Advisory, or Informational *for this project* (project-specific business/domain rules, project-specific conventions) — the child-side counterpart to Mentor's own `context/`. **Format finalized:** one Markdown file per rule with a small frontmatter contract — see `docs/Child Rules and Exceptions.md`. Rule *enforcement* against actual code remains deferred (Section 22).

## 11. Project Profile

`project.yaml` is the machine-readable project profile a child repository declares. **The schema is now finalized** (schema generation `schemaVersion: 1`) — see `docs/Project Profile Schema.md` for the full field-by-field reference and `docs/schema/project.schema.v1.json` for the normative JSON Schema. This section no longer carries an inline illustrative snippet, to avoid duplicating that content in two places; see `docs/examples/project.yaml` (fully populated) and `docs/examples/project.minimal.yaml` (minimum valid) for reference examples.

A minimal file requires only four fields: `schemaVersion`, `name`, `mentor.version`, and `stack.language`. Everything else — `stack.runtime`/`framework`/`database`/`orm`/`cache`, `architecture.style`/`api`, `testing.*`, `deployment.*`, `infrastructure.*`, and the reserved `extensions` namespace — is optional. The `stack` fields let a Mentor Skill adapt a generic standard to the child's actual technology — e.g. adapting `context/standards/Database Standards.md`'s indexing guidance to PostgreSQL/Prisma specifics rather than forcing a mismatched pattern, consistent with the Mentor Operating Model's No Invention Rule ("inspect the child repository before applying repository-sensitive guidance"). Validate any file with `python3 scripts/validate_project_yaml.py <path>`.

Note: finalizing this schema is a design/documentation deliverable only. Wiring an actual Mentor Skill to read and consume `project.yaml` as part of context discovery remains future implementation work (Section 22) — this section, and `docs/Project Profile Schema.md`, define the contract a future implementation will consume.
## 12. Architecture and Context Discovery

Mentor discovers child context progressively, in this order, rather than blindly loading the entire repository:

1. **`.mentor/project.yaml`** — the fastest, most structured source. Establishes declared stack, architecture style, and Mentor version compatibility before anything else is read.
2. **`.mentor/architecture.md`** — the human-readable architecture narrative, read next to fill in what the structured profile can't express.
3. **`.mentor/rules/`** — project-specific Mandatory/Configurable rules that must be known before producing any review or recommendation.
4. **`.mentor/exceptions.yaml`** — known, approved deviations, so a Skill doesn't re-flag something already explicitly accepted (Section 17) as if it were newly discovered.

Only after these four are read does Mentor inspect relevant repository artifacts as needed for the task at hand — not exhaustively, and not as a first step:

- `package.json` (or the stack's equivalent manifest)
- `tsconfig.json` / language/build configuration
- `Dockerfile`, `docker-compose*` files
- Database/schema files
- Source structure (directory layout, not full file contents)
- Tests (existing coverage and patterns)
- CI/CD configuration

This mirrors the Mentor Operating Model's No Invention Rule: unknown information is inspected or explicitly identified as unknown, never assumed — but "inspected" means targeted, task-relevant inspection, not indiscriminately loading the entire repository into context.

**This discovery order is now implemented**, not only specified: `skills/context-discovery/SKILL.md` and `scripts/discover_project_context.py` execute exactly the order above and produce a Normalized Project Context for other Mentor Skills to consume. See `docs/Context Discovery.md` for the full field reference, missing/invalid-context behavior, and the read-only guarantee. This remains a read-only, discovery-only capability — it does not enforce `.mentor/rules/` or `.mentor/exceptions.yaml`, and it does not perform Mentor-version compatibility blocking (Section 15); those remain future work (Section 22).

## 13. Mentor Skills + Child Skills

Mentor Skills and child-owned Skills are compositional, not competitive. A Mentor Skill invocation conceptually evaluates:

```text
Mentor Standard/SOP  +  Child Project Context  +  Actual Code/Diff  +  Applicable Child Rules
```

For example, `/engineering-mentor:code-review` evaluates `context/standards/Code Review Standard.md` and `context/standards/Severity Taxonomy.md` (Mentor) against the child's declared stack and architecture from `.mentor/` (child project context), the actual diff under review (the artifact), and any Mandatory/Configurable rules the child has declared in `.mentor/rules/` (applicable child rules) — exactly as `skills/code-review/SKILL.md`'s existing Constraint Handling rule already does for a stated project constraint, extended here to structured, persistent child context rather than only an ad hoc constraint mentioned in a single review request.

A child-specific Skill (the child's own, under its own `.claude/skills/`) may extend project- or domain-specific behavior — e.g. a domain-specific reviewer for a particular business rule — but it must not silently disable Mentor governance. A child Skill that wants to relax a Mandatory Mentor rule must do so through the exception mechanism (Section 17), not by defining a competing Skill that skips the check.

## 14. Versioning

Engineering Mentor uses semantic versioning, as already established in `docs/Versioning Strategy.md` and `skills/mentor-development/SKILL.md`'s "Versioning Expectations" — this Contract does not redefine it, only restates it for completeness:

- **PATCH** — bug fixes and non-breaking improvements.
- **MINOR** — new backward-compatible Skills, standards, capabilities, or guidance.
- **MAJOR** — breaking behavioral/governance changes that may require child-project changes.

A change that would silently break a pinned child (e.g. reclassifying an Advisory rule as Mandatory, or changing a Skill's expected output structure) requires at least a MAJOR bump, per the existing Versioning Expectations. The current Mentor plugin version is `1.0.0` (`plugin.json` and `.claude-plugin/plugin.json`).

## 15. Compatibility

A child project declares its supported Mentor version range in `.mentor/project.yaml`'s `mentor.version` field, e.g. `">=1.0.0 <2.0.0"`. The supported range grammar (a deliberate subset of full semver-range syntax — comparator terms `>=`, `<=`, `>`, `<`, `=` over `MAJOR.MINOR.PATCH`, no caret/tilde/OR-ranges) and both its syntactic and semantic (self-consistency) validation rules are defined in `docs/Project Profile Schema.md`'s "Mentor Compatibility Range Syntax" section — not restated here.

This lets a child pin to a compatible line of Mentor releases and receive PATCH/MINOR improvements without being silently exposed to a MAJOR breaking change — consistent with the existing Versioning Strategy's statement that "child repositories should pin or intentionally select a Mentor version rather than silently receiving uncontrolled breaking changes." The range's syntax and internal consistency can now be validated with `scripts/validate_project_yaml.py`; actually checking a declared range against the *installed* Mentor version at discovery time (and deciding what happens on a mismatch) remains deferred — see Section 22.
## 16. Mentor Update Distribution

The Mentor plugin is centrally maintained in this repository and distributed to child repositories through the private Claude Code plugin marketplace, `miteshpatel13/mentors-marketplace` (GitHub).

A child repository:

- Installs the `engineering-mentor` plugin independently through Claude Code, the same way any other plugin is installed.
- Must **not** clone this repository as a Git submodule.
- Must **not** copy Mentor content (Skills, Agents, `context/`) into its own source tree.

A child may remain on a compatible Mentor version until it intentionally upgrades, subject to any future mandatory-security-update policy (not yet defined — Section 22). This preserves child autonomy over upgrade timing for ordinary MINOR/PATCH releases while leaving room for a future policy that could compel an update when a Mandatory security rule itself changes.

## 17. Exceptions

`.mentor/exceptions.yaml` is the record of every explicit, approved deviation from a Mentor rule that would otherwise apply. Its purpose is to make every deviation visible, owned, and bounded — never silent.

An exception must:

- Be **explicit** — recorded as a distinct entry, never implied by the absence of a finding.
- Have a **reason** — the engineering justification for why the rule doesn't apply as stated.
- **Identify the affected Mentor rule** — which Standard/SOP/Skill rule the exception applies to.
- **Define scope** — exactly what it covers (a specific endpoint, a specific finding category, a specific module) — never a blanket exemption.
- **Define owner/approval** where applicable — who accepted the risk.
- **Optionally define an expiration/review date** — so a temporary exception doesn't become permanent by default.
- **Never silently disable a security requirement** — an exception on a Mandatory security/safety rule documents a scoped, reasoned, owned, reviewable deviation; it does not, and cannot, make the underlying risk disappear from review output. Per Section 8, this is the only sanctioned mechanism for a child to diverge from a Mandatory rule.

The exact YAML schema for `exceptions.yaml` is intentionally not defined here — only the required concepts above. Finalizing the schema is listed as future implementation work (Section 22), consistent with this Contract's design principle of not over-engineering the initial integration surface.

## 18. Conflict Resolution

Restating Section 8's priority order as the canonical conflict-resolution model for this Contract:

1. Security and safety requirements
2. Mentor Mandatory rules
3. Child Mandatory project constraints
4. Child project conventions
5. Mentor Advisory rules
6. General engineering best practices

When a Skill encounters a conflict, it should follow the same discipline `skills/code-review/SKILL.md`'s existing Constraint Handling rule already applies to a single stated constraint, generalized to this ordered model: respect the higher-priority side, explain the tension, identify the underlying risk, propose the least-disruptive resolution that satisfies the higher-priority requirement, and never silently drop a Mandatory finding to satisfy a lower-priority preference. A conflict that reaches all the way down to "Mentor Mandatory rule vs. child requirement" is resolved in the Mentor's favor per this order — the child's recourse is the exception mechanism (Section 17), not a silent override. See `docs/Governance Precedence Model.md` Sections 10–11 for the full conflict-type taxonomy (Compatible / Additive / Override / Conflict / Prohibited Override / Unknown) and the expected future handling for each — restated and detailed there rather than here, to keep one authoritative source for this material.

## 19. Security Boundaries

Mandatory security and safety rules form a hard boundary no child configuration crosses. Their substantive content is defined in `context/standards/Security Standards.md` and is not restated here to avoid duplication; at minimum it covers authentication, authorization, input validation, injection prevention, secret handling, sensitive-data exposure, secure logging, dependency risk, file-upload safety, and rate limiting/abuse prevention. In severity terms, this corresponds to the CRITICAL and HIGH tiers of `context/standards/Severity Taxonomy.md`, which are always blocking by default.

A child repository cannot, through `.mentor/project.yaml`, `.mentor/rules/`, a child-owned Skill, or any other mechanism, cause a Mentor Skill to omit, downgrade, or silently accept a finding that falls within this boundary. The only sanctioned path is the exception mechanism (Section 17), and an exception never removes the finding from review output — it documents why the finding, though real, is an accepted and bounded risk.

## 20. Example Child Repository

Illustrative only — not a real repository, not created by this task:

```text
order-service/                     (child repository root)
├── .mentor/
│   ├── project.yaml               (stack: TypeScript/NestJS/PostgreSQL/Prisma/Redis)
│   ├── architecture.md            (modular-monolith, REST API, order-domain narrative)
│   ├── exceptions.yaml            (e.g. a scoped, owned, time-bounded rate-limit exception
│   │                                on an internal-only diagnostics endpoint)
│   └── rules/
│       └── order-domain-rules.md  (project-specific business rule: e.g. "order totals
│                                    must reconcile against the ledger service before
│                                    fulfillment" — Mandatory for this project, not
│                                    globally reusable, so it belongs here and not in
│                                    the Mentor)
├── .claude/
│   └── skills/
│       └── order-domain-review/   (child-owned Skill extending code-review with
│                                    order-domain-specific checks; does not redefine
│                                    Mentor's Mandatory security rules)
└── src/
```

Running `/engineering-mentor:code-review` in this repository would compose: `context/standards/Code Review Standard.md` + `context/standards/Severity Taxonomy.md` (Mentor) with this `project.yaml`/`architecture.md` (child project context), the diff being reviewed (the artifact), and `order-domain-rules.md` plus any recorded exception (applicable child rules) — per Section 13.

## 21. End-to-End Flow

```text
Private GitHub
    |
    v
mentors-marketplace           (private Claude Code plugin marketplace -- miteshpatel13/mentors-marketplace)
    |
    v
engineering-mentor plugin     (this repository, versioned per Section 14)
    |
    v
Claude Code                   (installs the plugin independently per Section 16)
    |
    v
Child Repository
    |
    v
.mentor/
    |-- project.yaml          (read first — Section 12)
    |-- architecture.md
    |-- exceptions.yaml
    +-- rules/
```

Mentor is the horizontal/global engineering-governance layer: one set of Mandatory security rules, Standards, SOPs, Skills, and Agents, reused unchanged across every child repository that installs the plugin. The child repository is the vertical/project layer: it supplies the specific stack, architecture, domain rules, and approved exceptions that let Mentor's horizontal guidance apply correctly to *this* system, without Mentor ever having to invent or assume those facts (Mentor Operating Model's No Invention Rule) and without the child ever having to duplicate Mentor's global content into its own tree (Section 16).

## 22. Future Implementation Work

This Contract defines the model; the following concrete implementation tasks are explicitly out of scope for this task and not implemented here:

- ~~Finalize the `project.yaml` schema~~ -- **done**: see `docs/Project Profile Schema.md`, `docs/schema/project.schema.v1.json`. What remains: wiring a Mentor Skill to actually *consume* it (tracked separately below) and validating a declared `mentor.version` range against the installed Mentor plugin version at discovery time (also tracked below).
- ~~Finalize the `exceptions.yaml` schema~~ — **done**: see `docs/Child Rules and Exceptions.md`, `docs/schema/exceptions.schema.v1.json`, `scripts/validate_exceptions_yaml.py`. What remains: actually evaluating an exception against a specific finding (tracked below, alongside `.mentor/rules/` enforcement).
- ~~Define the `.mentor/rules/` format~~ — **done**: see `docs/Child Rules and Exceptions.md`, `scripts/validate_child_rule.py`. Section 10's `rules/` bullet ('format is deferred') is superseded by that document. What remains: matching a rule's declared scope against real code, and executing precedence when an actual Mentor/child conflict is detected (tracked below).
- ~~Implement Mentor's context-discovery behavior described in Section 12~~ — **done**: see `skills/context-discovery/SKILL.md`, `scripts/discover_project_context.py`, and `docs/Context Discovery.md`. What remains, explicitly deferred to a later phase: enforcing discovered `.mentor/rules/` and `.mentor/exceptions.yaml` against actual findings, Mentor/child conflict enforcement, and Mentor-version compatibility blocking (tracked separately below).
- ~~Update existing Skills to actually consume `.mentor/` child context per Section 13~~ — **done, for the six review-type Skills, as of a later retrofit phase**: `skills/code-review/SKILL.md`'s Workflow step 0 remains the reference implementation (runs `context-discovery`, and when declared, `scripts/validate_child_rule.py`/`scripts/validate_exceptions_yaml.py`, then applies Child Governance including `scripts/evaluate_governance.py` classification). `skills/security-review/SKILL.md`, `skills/database-review/SKILL.md`, `skills/api-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/performance-review/SKILL.md`, and `skills/testing-review/SKILL.md` each now have their own Workflow step invoking `context-discovery` first, a `### Child Governance` (or Skill-specific-named) Rules subsection that explicitly delegates to `skills/code-review/SKILL.md`'s Child Governance mechanism (including its `scripts/evaluate_governance.py` invocation) rather than re-deriving it, and a `## Governance Integration` section stating this posture directly. This bullet previously described these six Skills as "unchanged" — that was accurate when written and is now stale; it was not updated after the retrofit phase that added this integration. Verified directly, by reading each Skill's current Governance Integration and Child Governance/Rules content, during Phase 13 (Certification Blocker Remediation) of the independent-certification-pilot follow-up work — see `docs/Independent Certification Report.md` and `docs/Skill Ecosystem Inventory.md` for the evidence and remaining gaps (behavioral confirmation that the delegation actually produces correct output at run time is still Tier D/E evidence this repository cannot yet produce — see those documents). What remains open, not yet done for any Skill including `code-review`: enforcing `.mentor/rules/`/`.mentor/exceptions.yaml` against findings beyond the narrative-reasoning level these Skills already perform, and the Mentor-version compatibility blocking and Mandatory-conflict-enforcement items tracked separately below.
- Decide and document a `project.yaml` schema generation-2 (`schemaVersion: 2`) policy trigger and process, if/when a breaking change to the profile shape is ever needed (see `docs/Project Profile Schema.md`'s Schema Versioning section).
- Define compatibility validation for `mentor.version` ranges *against the installed Mentor plugin version at discovery time* (Section 15) -- the range's own syntax/self-consistency is now validated by `scripts/validate_project_yaml.py`; checking it against what's actually installed is the remaining piece.
- Define the future mandatory-security-update policy referenced in Section 16.
- Add integration tests for Mentor/child conflict scenarios (extending the pattern established in `tests/skill-tests/code-review/`).
- Create a reference child repository example (a real, minimal repository demonstrating Section 20's illustration).
- Tag existing Standards/SOPs/checklists with the Mandatory/Configurable/Advisory/Informational classification introduced in Section 7 — no existing file carries this classification today.
- ~~Reconcile this Contract's Section 8/18 conflict-priority model with the coarser conflict-priority statements already present in `context/core/Mentor Operating Model.md` and `skills/mentor-development/SKILL.md`~~ — **done**: see `docs/Governance Precedence Model.md`, which is now the authoritative specification for this standing-governance precedence question and explains the resolution in its own Section 15. What remains explicitly unresolved (deliberately, not silently — see that document's Section 15.3): how a live, in-session explicit user instruction interacts with a Mandatory Mentor rule. That is a distinct question from the one this bullet originally raised, and was out of scope for the phase that created `docs/Governance Precedence Model.md`.
