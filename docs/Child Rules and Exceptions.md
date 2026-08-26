# Child Rules and Exceptions

## Status

Defined and validated this phase; **not enforced**. This document is the authoritative contract for `.mentor/rules/` and `.mentor/exceptions.yaml`. It does not redefine the governance model established in `docs/Child Repository Integration.md` (Sections 4–8, 17–19) — it makes that model's two child-declared artifacts concrete: their file format, required metadata, validation rules, and lifecycle semantics. Mentor Context Discovery (`docs/Context Discovery.md`) already discovers both artifacts structurally; this document is what a discovered rule or exception is now required to structurally look like.

**Defined now:** file formats, frontmatter/schema contracts, classification/status vocabularies, precedence documentation, validators, tests, examples.

**Implemented later (explicitly out of scope for this phase — see Section 15):** evaluating a rule against actual code, matching a rule's declared scope to a specific file/finding, executing precedence when a real conflict occurs, evaluating whether an exception has expired, and any Skill actually changing a finding's presence or severity because of a discovered rule or exception.

## 1. Purpose

Give `.mentor/rules/` and `.mentor/exceptions.yaml` — both already named in `docs/Child Repository Integration.md` Section 10 and already discovered (not interpreted) by `docs/Context Discovery.md` — a concrete, validated, testable contract, so a child repository has an unambiguous way to declare project-specific rules and documented deviations, and so a future enforcement phase has a stable, already-tested format to build on rather than inventing one under time pressure.

## 2. Scope

**In scope:** the `.mentor/rules/` directory's file format and required/optional metadata; the `.mentor/exceptions.yaml` file's schema and lifecycle vocabulary; validators and regression tests for both; realistic, clearly-labeled examples; documentation of how the two relate to the existing governance hierarchy and to Context Discovery.

**Out of scope (see Section 15):** actually enforcing a rule or exception against a finding; matching a rule's `scope` field against real files/code; resolving a live Mentor/child conflict; evaluating exception expiration against the current date; wiring this into every Mentor Skill.

## 3. Child Rules

`.mentor/rules/` holds **child project rules**: project-specific engineering requirements a child repository wants Mentor Skills to be aware of. A child rule never replaces Mentor governance — it exists entirely inside the space Mentor's own hierarchy leaves open to a child project (`docs/Child Repository Integration.md` Section 4's Level 2, and Section 6).

**Format:** one Markdown file per rule, with a small YAML frontmatter block, per `context/templates/` conventions and this repository's existing preference for Markdown as the primary human-readable medium. A large second YAML/JSON schema was deliberately not created for rules — see Section 5's reasoning.

**File naming:** `<id>.md`, where `<id>` is the rule's own kebab-case identifier and must exactly match the frontmatter `id` field — the same "frontmatter identity must match the filename" convention this repository already uses for `skills/<name>/SKILL.md`. A file whose `id` doesn't match its filename fails validation (`E_RULE_ID_FILENAME_MISMATCH`).

**Rule identification:** the frontmatter `id` field is the rule's identifier, referenced later by `.mentor/exceptions.yaml`'s `rule` field (Section 8) and, in a future enforcement phase, by review output. It must be unique across every file in `.mentor/rules/` (`E_DUPLICATE_RULE_ID` — checked directory-wide, not just per file, since two files can't literally share a filename but could still declare the same `id`).

## 4. Rule Classification

Every child rule must declare exactly one classification, using the same four-way vocabulary `docs/Child Repository Integration.md` Section 7 already defines for Mentor's own rules — not a new, competing vocabulary:

- **Mandatory** — the project treats this as non-negotiable for itself.
- **Configurable** — the project has picked a specific value within some bound (the bound itself may be documented in the rule's body).
- **Advisory** — the project prefers this, and a deviation is fine when justified, without needing the exception mechanism, as long as the deviation is visible.
- **Informational** — reference/preference only, never blocking, never something that needs an explicit override.

**Child Mandatory Does Not Outrank Mentor Mandatory.** This is the single most important thing this section establishes, restated from the task that commissioned this document: a child rule classified `mandatory` means **"mandatory for this child project,"** never **"more authoritative than a Mentor Mandatory rule."** A child rule can only ever *add* a requirement on top of Mentor's own baseline — it can never *remove or weaken* one.

```text
VALID   (child rule ADDS to a Mentor Mandatory requirement)
  Mentor:  Authentication is required (Mandatory).
  Child:   All admin APIs require MFA (Child Mandatory).

INVALID (child rule attempts to WEAKEN a Mentor Mandatory requirement)
  Mentor:  Authorization checks are mandatory (Mandatory).
  Child:   This project does not require authorization checks.
```

The second form is not a legitimate "Child Mandatory" rule at all — it is an attempted override, and `.mentor/rules/` is not a mechanism for expressing one (there is no field in the frontmatter contract that could express "disable X"; see Section 11 for why the analogous risk in `exceptions.yaml` is closed at the schema level, and why that specific structural guard doesn't have a direct equivalent need here). See `docs/examples/child-rules/01-api-conventions.md` and `02-database-conventions.md` for two worked Child Mandatory examples that add to, rather than weaken, a Mentor Mandatory baseline.

## 5. Rule Metadata

Frontmatter contract (validated by `scripts/validate_child_rule.py` — the single authoritative enforcement of this contract; there is no separate JSON Schema file for it):

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | **yes** | string | Kebab-case, must match the filename stem, unique within `.mentor/rules/`. |
| `title` | **yes** | string | Short, human-readable. |
| `classification` | **yes** | enum | `mandatory` \| `configurable` \| `advisory` \| `informational` — see Section 4. |
| `scope` | **yes** | string | Free text — see Section 6. Every rule must state its applicability explicitly; there is no implicit "applies everywhere" default. |
| `category` | no | string | Open, free text (e.g. `database`, `api`, `testing`) — not an enum, mirroring `project.yaml`'s open `stack.*` fields, since a fixed category list would be incomplete for some project. |
| `owner` | no | string | Team/person who owns this rule, if the project wants that recorded. |
| `status` | no | enum | `draft` \| `active` \| `deprecated`. Omitting this field means `active` — this default is documented here, not silently assumed by the validator (the validator simply treats the field as optional; nothing infers a value). |

An unrecognized frontmatter field produces a **warning** (`W_UNKNOWN_FRONTMATTER_FIELD`), not an error — forward-compatible, matching `project.yaml`'s own top-level-field policy, since nothing in this small frontmatter contract could structurally express an override of Mentor governance the way an unrestricted `exceptions.yaml` field could (see Section 11's contrasting, deliberately strict policy there).

**Description, rationale, applicability, and examples are not frontmatter fields.** They belong in the Markdown body, under `## Description`, `## Rationale`, `## Applicability`, and `## Examples` headings (see the worked examples in `docs/examples/child-rules/`) — this keeps the machine-checked contract to the six fields above ("a small frontmatter contract," per this phase's instructions) while still capturing everything Section 2 of the commissioning task asked a rule to be able to express, in the human-readable form that content actually wants.

## 6. Rule Scope

`scope` is a **free-text string**, not a structured matcher. It may describe a repository-wide rule, a directory, a file pattern, a language, a framework, an API, a database, a testing concern, a deployment target, or a specific domain/module — whatever best describes the rule's actual applicability in prose (see the varied `scope` values across `docs/examples/child-rules/`).

This is a deliberate, documented limitation, not an oversight: **exact scope-matching semantics (e.g. evaluating a glob against a changed file, or detecting "this diff touches the database layer") are deferred to a future phase.** Nothing in this phase parses or evaluates a `scope` value against real code — Context Discovery still only lists rule files and their sizes (`docs/Context Discovery.md`'s `childRules.files`), and this document does not change that.

## 7. Rule Precedence

The full, authoritative precedence order — including how Configurable and Advisory child rules relate to each other and to Mentor's own tiers, the six conflict-type categories, and expected future handling for each — now lives in one place: `docs/Governance Precedence Model.md`. This section does not restate it, to avoid a third copy of the same model drifting out of sync with the other two (`docs/Child Repository Integration.md` Section 8/18 being the second).

**The one sentence worth repeating here, because it's the sentence this whole document exists to protect:** a child rule can add a *stricter* requirement; it can never weaken or disable a Mentor Mandatory security/safety requirement — the same VALID/INVALID distinction shown in Section 4, and `docs/Governance Precedence Model.md` Section 5's worked examples.

**This document only documents rule content and format — it does not execute precedence.** No validator, Skill, or script in this phase evaluates two rules against each other and picks a winner. Executing precedence when an actual conflict is detected is future enforcement work (Section 15, and `docs/Governance Precedence Model.md` Section 16).

## 8. Exceptions

`.mentor/exceptions.yaml` records **explicit, documented deviations** from an applicable Mentor or child rule — never an implicit one. Format: a single YAML file whose top-level document is a **list** of exception entries (formalizing what `docs/Context Discovery.md`'s `exceptions.entryCount` already assumed as the primary shape). Unlike `project.yaml`, this schema **is** machine-validated end-to-end with a JSON Schema — `docs/schema/exceptions.schema.v1.json` — because the entry shape is fixed, closed, and small enough that a schema adds real value without the "second large schema" risk the task warned against for rules (see Section 5's contrasting choice there).

Each entry (see the full field reference and the schema itself for exact types):

| Field | Required | Notes |
|---|---|---|
| `id` | **yes** | Unique within the file. |
| `rule` | **yes** | The affected rule's identifier — see the ambiguity noted below. |
| `reason` | **yes** | The engineering justification. |
| `scope` | **yes** | Exactly what this covers — never a blanket exemption. |
| `owner` | **yes** | Who owns / accepted the risk. |
| `status` | **yes** | `requested` \| `approved` \| `rejected` \| `expired` — see Section 9. |
| `evidence` | no | Supporting detail beyond `reason` (a compensating control, a sign-off reference). |
| `approvedBy` | no | Recorded plain metadata, not connected to any external system this phase. |
| `approvedAt` | no | ISO 8601 date. |
| `createdAt` | no | ISO 8601 date. |
| `expiresAt` | no | ISO 8601 date — presence makes this a **temporary** exception; absence makes it **permanent** (Section 9). |

**Ambiguity, documented rather than invented around (No Invention Rule):** Mentor's own rules (Standards, SOPs, Skills) do not currently carry individual machine identifiers — `docs/Child Repository Integration.md` Section 22 explicitly lists "tag existing Standards/SOPs/checklists with the Mandatory/Configurable/Advisory/Informational classification" as still-undone future work, and the same gap means there's no formal ID scheme for an individual Mentor rule either. So `rule` is a free-text reference: either a child rule's own `id` (e.g. `02-database-conventions`, as in `docs/examples/exceptions.yaml`'s third entry) or a human-readable pointer into a Mentor Standard (e.g. `context/standards/Security Standards.md#rate-limiting`, as in the schema's own field description). This is the smallest safe contract available given that gap — inventing a formal Mentor rule ID registry here would be inventing behavior the task told this document not to invent.

## 9. Exception Lifecycle

Two independent axes, both present in the schema, deliberately not merged into one enum:

**Status** (approval lifecycle) — exactly the four values Section 8 of the commissioning task asked for:

- **`requested`** — proposed, awaiting a decision. This is also what the task's own language calls an **"under-review"** exception; rather than adding a fifth, redundant status value, this document maps "under review" to `requested` explicitly, here, so the term isn't left undefined.
- **`approved`** — granted. `approvedBy`/`approvedAt` are optional but recommended (a missing pair on an `approved` entry produces `W_APPROVED_WITHOUT_APPROVAL_METADATA`, a warning, not an error — recorded as encouraged practice, not a hard requirement, since this phase does not implement a real approval system, per Section 10).
- **`rejected`** — requested, but declined. A rejected entry is still recorded (see `docs/examples/exceptions.yaml`'s fourth entry) so the request and the reasoning for declining it stay visible, exactly as Section 17 of `docs/Child Repository Integration.md` already requires for every deviation ("never silent").
- **`expired`** — the exception's review window has passed and it is no longer active.

**Durability** (permanent vs. temporary) — not a separate field, but a direct consequence of whether `expiresAt` is set:

- **No `expiresAt`** → **permanent.** There is no automatic expiration; the exception stands until a human revisits it. This is exactly why `owner` and `reason` are still required even for a permanent entry — "permanent" is not the same as "unowned" or "unjustified."
- **`expiresAt` set** → **temporary.** The exception is expected to be re-reviewed by that date.

**What this phase does not do:** compare `expiresAt` to today's date and automatically flip a `status` from `approved` to `expired`, or emit a warning that an exception has silently lapsed. `docs/examples/exceptions.yaml`'s third entry (`old-migration-raw-sql`) shows an already-expired exception whose `status` was set to `expired` by a human after the fact — the schema supports recording that state; nothing in this phase computes it. Automatic expiration evaluation is explicitly future work (Section 15).

## 10. Exception Approval Metadata

`approvedBy` and `approvedAt` are **plain recorded metadata** — a string and a date, nothing more. This phase does **not** connect them to GitHub, Jira, Slack, a database, or any external approval system; there is no verification that the named approver actually approved anything, no workflow that produces these values, and no enforcement that they're present before a `status: approved` entry is treated as valid (their absence only produces the non-blocking `W_APPROVED_WITHOUT_APPROVAL_METADATA` warning). This is a deliberate scope limit, not an oversight — building a real approval system was never in scope for this phase, and documenting that plainly here is preferable to letting the field names imply more machinery than exists.

## 11. Security Boundaries

**This is non-negotiable, restated directly from the commissioning task:** an exception must never silently disable or downgrade a Mentor Mandatory security/safety requirement. If existing Mentor governance says something cannot be overridden, this contract preserves that — it does not, and structurally cannot, create a path around it.

Concretely: `docs/schema/exceptions.schema.v1.json` sets `additionalProperties: false` on every exception entry. This is a deliberate departure from `project.yaml`'s own philosophy (which stays open, with unknown fields only warning — see `docs/Project Profile Schema.md`), made specifically here because `exceptions.yaml` is the one artifact in this whole contract whose entire purpose is to reference and deviate from a rule — which makes it the one place a field like `disable: sql-injection-check` could plausibly be proposed. Closing the schema means that concept **cannot become a supported field** without an explicit, reviewed schema change — it cannot be silently smuggled in as an "extra" property the way it could under an open schema. `scripts/validate_exceptions_yaml.py` enforces this as a hard error (`E_UNKNOWN_FIELD`), verified by a dedicated regression fixture (`tests/schema-tests/exceptions/invalid-unknown-field.yaml`).

Beyond the schema-level guard: nothing in this phase gives an exception's `status: approved` any actual effect on a finding. No Skill in this repository reads `.mentor/exceptions.yaml` and changes what it reports because of it — Context Discovery still only counts and structurally validates entries (`docs/Context Discovery.md`'s `exceptions` field). Recording an exception here is documentation of an intended, human-reviewed deviation; it becomes operative only once a future enforcement phase is built to consult it, and that future phase will still be bound by everything stated in this section and in `docs/Child Repository Integration.md` Section 19, which remains the unmodified, authoritative security boundary.

If a future, legitimate need arises for a more formal security-exception process (e.g. one with real external approval integration), that is a **future governance capability** to design and document deliberately when it's actually needed — not something this phase implements speculatively.

## 12. Examples

All under `docs/examples/`, every file headed with an explicit "EXAMPLE FILE" label — **none of these are real child rules or exceptions in `engineering-mentor` itself**, which has no `.mentor/` directory (`docs/Child Repository Integration.md`'s Design Principles):

- `docs/examples/child-rules/01-api-conventions.md` — a **Child Mandatory** rule (MFA on admin APIs) that adds to, and cannot weaken, a Mentor Mandatory authentication requirement.
- `docs/examples/child-rules/02-database-conventions.md` — a second **Child Mandatory** rule (Prisma-only data access) with a documented, narrow scope carve-out.
- `docs/examples/child-rules/03-testing-requirements.md` — a **Child Advisory** rule (prefer integration over deep mocking), demonstrating a classification a reviewer can deviate from with visible justification, without the formal exception mechanism.
- `docs/examples/exceptions.yaml` — five entries covering a **temporary** (has `expiresAt`) approved exception, a **permanent** (no `expiresAt`) approved exception, an **expired**-status exception, and a **rejected** exception — deliberately including a rejected authorization-bypass request to show what Section 11's boundary looks like in a real (illustrative) entry.

Every example validates cleanly against its respective validator (`scripts/validate_child_rule.py --dir docs/examples/child-rules` and `scripts/validate_exceptions_yaml.py docs/examples/exceptions.yaml`).

## 13. Validation

**One authoritative validator per artifact, reusing the existing `Finding` class** (`scripts/validate_project_yaml.py`'s `Finding`) rather than redefining an equivalent shape twice more:

- `.mentor/rules/<id>.md` — `scripts/validate_child_rule.py`. `validate_file(path)` checks a single file (frontmatter presence/parse, required fields, `classification`/`status` enums, filename/id match); `validate_rules_dir(dir_path)` additionally checks cross-file `id` uniqueness. No separate JSON Schema file — see Section 5.
- `.mentor/exceptions.yaml` — `scripts/validate_exceptions_yaml.py`, backed by `docs/schema/exceptions.schema.v1.json`. `validate_file(path)` checks top-level list structure, required fields, `status` enum, date formats, unknown-field rejection, and cross-entry `id` uniqueness.

**Regression suite:** `python3 scripts/run_rules_and_exceptions_tests.py`, covering, at minimum, every scenario the commissioning task named:

*Exceptions (`tests/schema-tests/exceptions/`):* valid single entry; valid multiple entries; missing required identifier; missing affected rule; invalid status; invalid date; invalid scope; invalid structure (non-list top level); temporary exception with expiration; expired-status exception — plus two bonus fixtures: a rejected exception, a duplicate-id fixture, and the security-boundary regression (an unrecognized/`disable`-like field is rejected).

*Child rules (`tests/schema-tests/child-rules/`):* valid Mandatory, Configurable, Advisory, and Informational rules; missing rule identifier; invalid classification; invalid (unclosed) frontmatter; missing required metadata — plus a bonus filename/id-mismatch fixture and two directory-level fixtures (`dir-fixtures/valid-rules-dir/`, a clean three-rule directory; `dir-fixtures/duplicate-ids/`, two files declaring the same `id`).

All fixtures use the same `<name>.{yaml,md} + <name>.expected.json` sidecar convention already established by `tests/schema-tests/project-yaml/` — comparing the multiset of error/warning codes produced, not exact message text, so wording changes don't spuriously break the suite (see `tests/schema-tests/README.md`).

## 14. Context Discovery Relationship

Mentor Context Discovery (`docs/Context Discovery.md`, `scripts/discover_project_context.py`) already discovers `.mentor/rules/` (listing files and sizes) and `.mentor/exceptions.yaml` (parsing it and counting entries) — and it continues to do exactly that, unchanged, after this phase. This document finalizes what a *structurally valid* rule file or exceptions file looks like; it does not change discovery's behavior, and discovery still does not validate against these new contracts, parse rule frontmatter, or interpret exception entries. `docs/Context Discovery.md` was updated only to point its `childRules`/`exceptions` field descriptions at this document instead of describing the format as "deferred," since it no longer is — see that document's changelog note in its own Status section.

After this phase, "Context Discovery found `.mentor/rules/no-raw-sql.md`" still means exactly: **this file exists.** It does not mean: **this file is frontmatter-valid** (that requires running `scripts/validate_child_rule.py` separately, which discovery does not do), and it certainly does not mean: **this rule has already changed Mentor's behavior.** The distinction the commissioning task drew — "these rules exist and are structurally valid" vs. "these rules have already changed Mentor behavior" — is preserved exactly, and in fact sharpened: even "structurally valid" is not something discovery itself asserts today; it's something this phase's new validators can check, on request, separately.

## 15. Enforcement — Future Phase

Everything below is **explicitly deferred**, named directly from the commissioning task, so a later phase has a clear, unambiguous starting point rather than an implicit assumption about what "later" already covers:

- Evaluating a rule against actual code or a diff.
- Matching a rule's declared `scope` (Section 6) against real files, languages, or changes.
- Executing the precedence order (Section 7) when a real Mentor/child conflict is detected.
- Evaluating an exception against a specific finding (i.e. actually suppressing, downgrading, or annotating a finding because a matching, approved exception exists).
- Evaluating exception expiration (comparing `expiresAt` to the current date and reacting to it — Section 9).
- Resolving a live Mentor/child conflict end-to-end (`docs/Child Repository Integration.md` Sections 8 and 18 already define the model; nothing executes it).
- Skill-level enforcement — no Mentor Skill in this repository was modified this phase to consult `.mentor/rules/` or `.mentor/exceptions.yaml` when producing a finding. `skills/code-review/SKILL.md`'s existing context-discovery hook (added in the prior phase) already states plainly that discovered rules/exceptions are informational only, and that statement remains accurate and untouched.
- Automated governance decisions of any kind.

This phase's job was to make the *shape* of these two artifacts stable, documented, and testable, so that whenever enforcement is built, it's built against a contract that already has 24 passing regression checks behind it — not designed and validated for the first time under the pressure of also making it work end-to-end.
