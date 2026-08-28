---
name: context-discovery
description: "Discover and normalize a child repository's declared Mentor context — .mentor/project.yaml, architecture.md, rules/, exceptions.yaml, plus a bounded, targeted check of well-known repository artifacts — into a Normalized Project Context that other Mentor Skills (code-review, security-review, architecture-review, database-review, testing-review, performance-review, api-review, api-contract-design) can consume consistently. Use at the start of any Mentor Skill invocation against a real repository, before applying repository-sensitive guidance. Read-only: never creates, modifies, or deletes anything in the child repository. Does not enforce child rules or exceptions — discovery only."
category: Mentor Core
skillType: Mentor Core
---

# Context Discovery

## Purpose

Locate a child repository's `.mentor/` directory (if any), discover and validate its contents in a fixed order, and produce a single **Normalized Project Context** — a plain structured object — that downstream Mentor Skills read instead of each reimplementing their own repository-inspection logic.

This Skill implements the discovery responsibility and ordering already specified in `docs/Child Repository Integration.md` Section 12 ("Architecture and Context Discovery"). It does not redefine that model; it is the executable implementation of it.

## Scope

**In scope:**

- Locating the child repository root (the path given for the task).
- Detecting whether `.mentor/` exists.
- Discovering and validating `.mentor/project.yaml` (reusing the existing schema validator — see Rules).
- Discovering `.mentor/architecture.md`.
- Discovering `.mentor/rules/`.
- Discovering `.mentor/exceptions.yaml`.
- Identifying missing or invalid context and reporting it explicitly.
- A bounded, existence-only check of well-known repository artifacts (Section 12's second list) when the task at hand needs them.
- Producing the Normalized Project Context for another Skill (or for direct reporting to the user) to consume.

**Out of scope — explicitly not this Skill's responsibility:**

- **Enforcement.** This Skill does not decide whether a finding should be suppressed, downgraded, or accepted because of a discovered rule or exception. It surfaces `.mentor/rules/` and `.mentor/exceptions.yaml` as discovered data only. A consuming Skill (or a future enforcement capability) decides what to do with that data.
- **Mentor/child conflict resolution.** Governed by `docs/Child Repository Integration.md` Sections 8 and 18 — unaffected by this Skill.
- **Compatibility blocking.** This Skill reports whether a declared `mentor.version` range is itself syntactically/semantically valid, and always reports `compatibilityStatus: "not_determined"` when it is — it never blocks a project or claims compatibility/incompatibility with the installed Mentor version. See Rules.
- **Reading the entire repository.** This Skill never performs a full or recursive repository load. Repository-artifact inspection (the fifth discovery step) is a fixed, bounded, existence-only check of a short, well-known candidate list — never a directory walk of arbitrary depth, and never file-content inference of stack/framework facts.
- **Writing to the child repository.** This Skill is strictly read-only (see Constraints).

## When to Use

At the start of any Mentor Skill invocation (`code-review`, `security-review`, `architecture-review`, `database-review`, `testing-review`, `performance-review`, or a future Mentor Skill) that is operating against a real, identifiable repository, so the Skill can adapt generic Mentor guidance to the child's actual declared stack, architecture, and constraints — per the Mentor Operating Model's No Invention Rule ("inspect the child repository before applying repository-sensitive guidance").

Do not use this Skill when there is no identifiable repository root to inspect (e.g. a review of a bare code snippet or diff pasted without repository context) — there is nothing to discover, and the consuming Skill should proceed exactly as it does today in that situation.

## Required Context

The path to the child repository's root directory. Nothing else is required — this Skill does not need the user to already know whether `.mentor/` exists, what it contains, or whether it's valid; discovering that is the Skill's job.

## Workflow

1. Run `python3 scripts/discover_project_context.py <child-repo-root>` (the Mentor plugin's own `scripts/` directory — an absolute path to it is safe to use regardless of the child repository's location). This script implements the discovery order below and reuses `scripts/validate_project_yaml.py` for schema validation — do not reimplement either in this Skill or in any consuming Skill.
2. Parse the resulting JSON as the Normalized Project Context (see Expected Output for its shape).
3. If `mentorConfigured` is `false`, or `projectProfile.valid` is not `true`, follow Rules → Missing or Invalid Context below rather than treating any field as a reliable declaration.
4. Hand the resulting context to the consuming Skill/task, or, when this Skill is invoked directly, report it per Expected Output.
5. Never re-run discovery mid-task against a repository that hasn't changed — one discovery pass per task is sufficient; this is deterministic, not conversational, so repeating it wastes effort without changing the result.

### Discovery Order

Exactly the order defined in `docs/Child Repository Integration.md` Section 12 — restated here only as an implementation checklist, not redefined:

1. `.mentor/project.yaml`
2. `.mentor/architecture.md`
3. `.mentor/rules/`
4. `.mentor/exceptions.yaml`
5. Relevant repository artifacts (bounded, existence-only, only as needed for the task)

## Rules

### Reuse, Never Duplicate, the project.yaml Schema

`.mentor/project.yaml` validation always goes through `scripts/validate_project_yaml.py`'s `validate_file()` (called internally by `scripts/discover_project_context.py`), which itself implements `docs/schema/project.schema.v1.json`. Never hand-parse or re-validate `project.yaml` fields directly in this Skill, in a consuming Skill, or in a one-off script. If the schema needs to change, that happens in `docs/schema/project.schema.v1.json` and its validator — not here.

### Missing or Invalid Context

Behavior is deterministic and follows `docs/Child Repository Integration.md` Section 12 and the Mentor Operating Model's No Invention Rule — never invent what discovery didn't find:

| Condition | Required behavior |
|---|---|
| No `.mentor/` directory | Report: child context is not configured. Do not invent stack, architecture, or convention facts. A consuming Skill may continue using only direct repository evidence it inspects itself (e.g. an existing `package.json`), exactly as it would for a repository with no Mentor integration at all. |
| `.mentor/` exists but `project.yaml` is missing | Report: project profile missing. Do not invent stack/architecture information. |
| `project.yaml` exists but fails schema validation | Report the validation errors (`discovery.filesInvalid`). Do not silently proceed as though the declaration were valid — `projectProfile.valid` is `false`, and any individual field values surfaced in the context are UNVERIFIED, not authoritative, until the file is fixed. |
| `architecture.md` missing | Report: architecture narrative unavailable. If the task requires an architecture understanding, fall back to inspecting relevant repository artifacts (discovery step 5) rather than guessing. |
| `rules/` missing | Report: no child rules declared. This is a normal, valid state — not an error. |
| `exceptions.yaml` missing | Report: no child exceptions declared. This is a normal, valid state — not an error. |

### Mentor Version Compatibility

- Validate only the declared range's own syntax and internal self-consistency (via the existing validator) — e.g. reject `>=2.0.0 <1.0.0` as self-contradictory, exactly as `scripts/validate_project_yaml.py` already does.
- Expose the declared range and whether it is itself valid.
- **Never** compare the declared range against the installed Mentor plugin version to compute an "installed-vs-declared" compatibility verdict — there is no documented mechanism for a Skill to introspect which Mentor plugin version is actually active in the current session, and inventing one here would be inventing a new compatibility algorithm, which this phase explicitly does not do. When the range itself is valid, `compatibilityStatus` is always `"not_determined"`. This is a deliberate, permanent-for-this-phase behavior, not a placeholder bug — see `docs/Context Discovery.md`'s "Mentor Compatibility" section for the full reasoning.
- **Never** block a task, refuse to proceed, or treat a project as unsupported because compatibility can't be determined. Compatibility enforcement is explicitly out of scope for this phase (`docs/Child Repository Integration.md` Section 22).

### Security / Governance Boundary

This Skill collects and normalizes context; it does not adjudicate it. It must never cause, and a consuming Skill must never let it cause:

- A discovered child rule or exception overriding a Mentor Mandatory rule.
- A discovered exception downgrading a security finding's severity on its own — an exception documents a scoped, reasoned, owned deviation (`docs/Child Repository Integration.md` Section 17); it doesn't silently remove the finding, and this Skill doesn't apply that judgment itself.
- Invalid or unverified `project.yaml` content being treated as an authoritative declaration.
- Any discovered child data disabling or bypassing a security check.

`docs/Child Repository Integration.md` Sections 8, 18, and 19 remain the authoritative, unmodified governance hierarchy. This Skill sits entirely upstream of that hierarchy — it supplies facts; it does not adjudicate them.

### No Content Inference

Repository-artifact discovery (step 5) is existence-only. Do not open `package.json`, `Dockerfile`, or any other candidate artifact to infer framework, database, or architecture facts from its contents in this Skill — that would be exactly the kind of invented inference the Mentor Operating Model's No Invention Rule prohibits when reliable evidence (a declared `project.yaml` field, or an explicit read the consuming Skill performs and documents) isn't in view. A consuming Skill that genuinely needs to read one of these files' contents for its own task does so itself, explicitly, and says so — this Skill's job stops at "this file exists" or "this file does not exist."

## Constraints

- **Read-only, absolutely.** This Skill must never create, modify, move, or delete any file or directory inside the child repository, under any circumstance, including when context is missing or invalid. `scripts/discover_project_context.py` is implemented to guarantee this; do not work around it with a different mechanism that writes.
- Never invoke this Skill's logic by hand-parsing `.mentor/` files directly — always go through `scripts/discover_project_context.py` so validation and discovery-order logic stay in one place.
- Never treat an unvalidated or invalid `project.yaml` field as trustworthy in a downstream recommendation.

## Governance Integration

Not applicable in the findings sense — this Skill supplies context to governance-consuming Skills; it does not itself evaluate a child repository's compliance, classify a rule/exception relationship, or produce a governance-classified finding. `discovery.childRules`/`discovery.exceptions` are surfaced as parsed data only (per Workflow); the tier/relationship classification a consuming Review-type Skill performs against that data is `scripts/evaluate_governance.py`'s job (`docs/Governance Evaluation.md`), not this Skill's.

## Validation

Discovery is complete and correct when: every one of the four `.mentor/` files has been explicitly reported as found, missing, or invalid (never silently skipped); `project.yaml` validation was performed via the shared validator, not reimplemented; the Normalized Project Context was produced even when `.mentor/` is entirely absent; no repository content outside the fixed artifact candidate list and the four `.mentor/` files was read; and nothing in the child repository was modified. `scripts/run_context_discovery_tests.py` exercises all of this mechanically — see `tests/context-discovery/README.md`.

## Edge Cases

- **No identifiable repository root** — nothing to discover; skip this Skill entirely for that invocation (see When to Use).
- **`.mentor/` exists but is empty** (no files inside at all) — every one of the four files is reported missing; this is equivalent to no `.mentor/` directory for practical purposes, but `mentorConfigured` is still `true` since the directory itself exists.
- **`project.yaml` parses as YAML but isn't a mapping** (e.g. a bare list or scalar at the document root) — the validator reports this as a validation error; `projectProfile.valid` is `false`, and no fields are populated from it.
- **`architecture.md` exists but is a directory, not a file** — reported as invalid (a structural anomaly), and treated as architecture-narrative-unavailable, not as a crash.
- **`rules/` exists but is empty** — reported as declared, with zero files; not an error.
- **`exceptions.yaml` exists but is empty or contains only a YAML null document** — reported as declared, parsed, with zero entries; not an error.
- **`exceptions.yaml` exists but is malformed YAML** — reported as invalid (`E_MALFORMED_YAML`), `parsed: false`; never silently treated as "no exceptions."
- **A repository large enough that a full scan would be expensive** — never a concern, because repository-artifact discovery is a fixed, bounded, existence-only candidate list, not a scan.

## Failure Handling

If `scripts/discover_project_context.py` cannot run at all (e.g. the given root doesn't exist), report that plainly and stop — do not fabricate a Normalized Project Context. If the script runs but reports `.mentor/` missing or `project.yaml` invalid, that is a **successful discovery run with a reported gap**, not a failure — proceed per Missing or Invalid Context above, never treat a reported gap as a reason to halt the consuming Skill's task entirely (the consuming Skill decides how much repository-evidence-only inspection to do instead; this Skill has already told it exactly what is and isn't available).

## Expected Output

The Normalized Project Context, as emitted by `scripts/discover_project_context.py`, is a JSON object with these top-level sections (see `docs/Context Discovery.md` for the full field-by-field reference — not duplicated here):

```text
projectRoot            -- absolute path discovery was run against
mentorConfigured        -- whether .mentor/ exists at all
identity                -- name, schemaVersion (from project.yaml, if declared)
mentorCompatibility     -- declaredRange, rangeValid, compatibilityStatus
stack                   -- language, runtime, framework, database, orm, cache
architecture            -- style, api, architectureDocAvailable/Path/LineCount
testing                 -- as declared in project.yaml (open map)
deployment              -- as declared in project.yaml (open map)
infrastructure          -- as declared in project.yaml (open map)
extensions              -- as declared in project.yaml (open map, forward-compat)
projectProfile          -- { declared, valid } summary for project.yaml
childRules              -- { declared, files[], note: discovery-only }
exceptions              -- { declared, path, parsed, entryCount, note: discovery-only }
discovery               -- filesFound[], filesMissing[], filesInvalid[], repositoryArtifactsInspected[], warnings[]
```

When reporting discovery results directly to a user (rather than handing the context to another Skill), summarize: whether `.mentor/` is configured, whether `project.yaml` is valid (and its errors if not), what architecture/rules/exceptions were found, and any warnings — do not dump the raw JSON as the entire response unless asked for it.

## Examples

- A repository with a fully populated `.mentor/` directory → `mentorConfigured: true`, `projectProfile.valid: true`, stack/architecture fields populated from `project.yaml`, `childRules.declared: true`, `exceptions.declared: true` — a consuming `code-review` invocation can now adapt generic guidance to the declared TypeScript/NestJS/PostgreSQL/Prisma stack.
- A repository with no `.mentor/` directory at all → `mentorConfigured: false`, every `.mentor/`-derived field `null`/empty, a warning stating child context is not configured — a consuming Skill proceeds exactly as it does today, using only what it inspects directly.
- A repository with a `project.yaml` that fails schema validation (e.g. `schemaVersion: 99`) → `projectProfile.valid: false`, `discovery.filesInvalid` carries the specific error codes (e.g. `E_SCHEMA_VERSION_UNSUPPORTED`) — a consuming Skill must not treat any declared field from this file as trustworthy until it's fixed, and should say so if it surfaces any of those fields at all.
- A repository declaring `mentor.version: ">=1.0.0 <2.0.0"` → `mentorCompatibility.rangeValid: true`, `mentorCompatibility.compatibilityStatus: "not_determined"` — never a computed "compatible"/"incompatible" verdict.

## Related Skills

- `skills/code-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/database-review/SKILL.md`, `skills/performance-review/SKILL.md`, `skills/security-review/SKILL.md`, `skills/testing-review/SKILL.md`, `skills/api-review/SKILL.md`, `skills/api-contract-design/SKILL.md` — Dependents: each of these Skills has a true Dependency on this Skill (invokes it first, every time, before reasoning about any repository-specific claim), not the reverse — this Skill has no dependency on any of them and functions identically regardless of which, if any, consumes its output.
