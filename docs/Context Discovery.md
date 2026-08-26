# Mentor Context Discovery

## Status

Implemented (this phase). This document is the field-by-field reference for the **Normalized Project Context** produced by `scripts/discover_project_context.py` and consumed via `skills/context-discovery/SKILL.md`. It does not redefine the discovery model — that's `docs/Child Repository Integration.md` Section 12 — it documents the executable implementation of it.

Explicitly not covered by this phase (tracked in `docs/Child Repository Integration.md` Section 22): enforcing discovered `.mentor/rules/`, enforcing discovered `.mentor/exceptions.yaml`, resolving Mentor/child conflicts, blocking on Mentor-version compatibility, or automatically upgrading a child's Mentor version.

**Update:** the `.mentor/rules/` and `.mentor/exceptions.yaml` formats referenced below as "deferred" are now finalized — see `docs/Child Rules and Exceptions.md`. Discovery's own behavior is unchanged by that: it still only lists rule files and parses/counts exception entries structurally, exactly as described below; it does not validate against the new contracts, and finding a rule/exception file still means only "this file exists," never "this content has been applied." See `docs/Child Rules and Exceptions.md` Section 14 for the full relationship.

**Update:** `skills/code-review/SKILL.md` is now the first Mentor Skill that reasons about discovered `childRules`/`exceptions` (its "Child Governance" rules), as a scoped reference implementation of `docs/Governance Precedence Model.md`. It does so as a distinct, explicit step *after* discovery — invoking `scripts/validate_child_rule.py`/`scripts/validate_exceptions_yaml.py` itself to get field-level rule/exception data — never by discovery parsing rule frontmatter or exception fields on its own. This capability's own scope, guarantees, and "discovery, never enforcement" boundary (this section and Security / Governance Boundary, below) are unchanged by that; no other Mentor Skill has been updated to do the same yet.

## What Context Discovery Owns

- Locating a child repository's `.mentor/` directory and reading its four well-known files, in the fixed order defined by `docs/Child Repository Integration.md` Section 12.
- Validating `.mentor/project.yaml` against the finalized schema (`docs/schema/project.schema.v1.json`) by reusing `scripts/validate_project_yaml.py` — never re-implementing that validation.
- A bounded, existence-only check of a fixed list of well-known repository artifacts (Section 12's second discovery list).
- Producing one normalized, consistently-shaped context object that every Mentor Skill can read the same way.
- Explicitly reporting every gap (missing file, invalid file, empty directory) rather than silently omitting it.

## What Context Discovery Does Not Own

- **Enforcement.** Discovered `.mentor/rules/` and `.mentor/exceptions.yaml` are surfaced as data, never applied to suppress, downgrade, or alter a finding. That is future work (Section 22).
- **Conflict resolution.** `docs/Governance Precedence Model.md` (which restates and refines `docs/Child Repository Integration.md` Sections 8 and 18) governs Mentor/child conflicts; this capability supplies facts to that process, it doesn't run it.
- **Compatibility enforcement.** See Mentor Compatibility below — discovery reports facts about the declared range, never a pass/fail compatibility verdict, and never blocks anything on that basis.
- **Governance.** A child cannot use anything discovery surfaces to weaken a Mentor Mandatory rule, downgrade a security severity, or disable a security check — see Security / Governance Boundary below and `docs/Child Repository Integration.md` Section 19, which remains the authoritative, unmodified boundary.
- **Reading the whole repository.** Discovery never performs a full or recursive scan; artifact discovery is a short, fixed candidate list, existence-only.
- **Writing anything.** Discovery is strictly read-only — see Read-Only Guarantee below.

## Discovery Order

Exactly `docs/Child Repository Integration.md` Section 12, restated here only as the field-level walkthrough below follows it:

1. `.mentor/project.yaml`
2. `.mentor/architecture.md`
3. `.mentor/rules/`
4. `.mentor/exceptions.yaml`
5. Relevant repository artifacts (bounded, existence-only, only as needed)

## Files

| Path | Purpose |
|---|---|
| `scripts/discover_project_context.py` | The deterministic discovery engine. `discover(root) -> dict` is importable directly (used by the test runner); the CLI (`python3 scripts/discover_project_context.py <root>`) prints the same structure as JSON. |
| `skills/context-discovery/SKILL.md` | The Skill interface: instructs an agent to invoke the script and treat its output as the Normalized Project Context, rather than reimplementing discovery logic inline. |
| `scripts/run_context_discovery_tests.py` | Automated regression suite — see Testing below. |
| `tests/context-discovery/fixtures/*` | Synthetic child-repository fixtures exercising every discovery scenario. **Test fixtures only** — none of this creates a real `.mentor/` directory in `engineering-mentor` itself. |

## The Normalized Project Context

A plain JSON object with these top-level sections. Field names match `scripts/discover_project_context.py`'s output exactly.

### `projectRoot` (string)

Absolute path discovery was run against.

### `mentorConfigured` (boolean)

Whether `.mentor/` exists as a directory at all. This is the single fastest signal for "is this repository integrated with Mentor."

### `identity`

| Field | Source | Notes |
|---|---|---|
| `name` | `project.yaml`'s `name` | `null` if not declared or `project.yaml` missing. |
| `schemaVersion` | `project.yaml`'s `schemaVersion` | Surfaced even when the value is unsupported (e.g. `99`) — the *raw declared value* is never nulled out just because it failed validation; `projectProfile.valid` is what signals untrustworthiness, not a silently blanked field. |

### `mentorCompatibility`

| Field | Meaning |
|---|---|
| `declaredRange` | The raw `mentor.version` string as declared, or `null` if not declared. |
| `rangeValid` | Whether the range is syntactically valid and internally self-consistent (via `scripts/validate_project_yaml.py`) — `null` if nothing was declared. |
| `compatibilityStatus` | One of `not_declared`, `range_invalid`, or `not_determined`. **Never** a computed "compatible"/"incompatible" verdict against the installed Mentor plugin version — see Mentor Compatibility below. |

### `stack`, `architecture`, `testing`, `deployment`, `infrastructure`, `extensions`

Populated directly from `project.yaml`'s corresponding sections when the file is present and structurally parseable (even if overall validation failed — see Missing or Invalid Context). `architecture` additionally carries three discovery-derived fields not sourced from `project.yaml`: `architectureDocAvailable` (bool), `architectureDocPath` (string or `null`), `architectureDocLineCount` (int or `null`) — these describe `.mentor/architecture.md`, not the declared `architecture.style`/`architecture.api` fields.

### `projectProfile`

| Field | Meaning |
|---|---|
| `declared` | Whether `.mentor/project.yaml` exists. |
| `valid` | `true`/`false` once the file exists and was checked; `null` if it doesn't exist (there's nothing to validate). |

### `childRules`

| Field | Meaning |
|---|---|
| `declared` | Whether `.mentor/rules/` exists. |
| `files` | `[{path, sizeBytes}, ...]` for every file directly inside `rules/`. Content is not parsed or interpreted — the frontmatter/format of an individual rule file is now defined in `docs/Child Rules and Exceptions.md`, but discovery still does not validate against it; running `scripts/validate_child_rule.py` is a separate, explicit step. |
| `note` | A fixed string reiterating that these are discovered, not enforced, in this phase. |

### `exceptions`

| Field | Meaning |
|---|---|
| `declared` | Whether `.mentor/exceptions.yaml` exists. |
| `path` | Its relative path, or `null`. |
| `parsed` | Whether the file parsed as valid YAML — `null` if the file doesn't exist. |
| `entryCount` | Number of entries if the parsed document is a list or mapping; `0` for an empty/null document; `null` if it didn't parse or parsed to something else. `docs/Child Rules and Exceptions.md` now formalizes the top-level shape as a list of exception objects — discovery's own `entryCount` logic (list-or-mapping, generic) is unchanged and does not itself enforce that shape; running `scripts/validate_exceptions_yaml.py` is a separate, explicit step. |
| `note` | A fixed string reiterating that discovery does not change finding/severity behavior in this phase. |

### `discovery`

| Field | Meaning |
|---|---|
| `filesFound` | Every `.mentor/`-relative path (or `.mentor/` itself) that was found, in discovery order. |
| `filesMissing` | Every expected path that wasn't found. |
| `filesInvalid` | `[{path, errors: [{level, code, path, message}, ...]}, ...]` — `errors` uses the exact `Finding.to_dict()` shape from `scripts/validate_project_yaml.py` for `project.yaml` entries, and the same shape (hand-constructed) for non-schema structural problems (a directory where a file was expected, malformed YAML). |
| `repositoryArtifactsInspected` | `[{path, exists}, ...]` for the fixed candidate list below — always present, always the same length, regardless of what was found. |
| `warnings` | Human-readable strings describing every gap or anomaly encountered. Every "missing" or "invalid" condition produces at least one warning — nothing is silently swallowed. |

**Fixed repository-artifact candidate list** (existence-only, no content read): `package.json`, `tsconfig.json`, `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `requirements.txt`, `pyproject.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `composer.json`, `.github/workflows`. This list may grow over time (a Mentor MINOR change), but it stays a fixed, reviewed list — never a dynamic directory walk.

## Missing or Invalid Context

| Condition | Behavior |
|---|---|
| No `.mentor/` | `mentorConfigured: false`; every `.mentor/`-derived field stays `null`/empty; a warning states child context is not configured; nothing is invented. |
| `.mentor/` exists, `project.yaml` missing | `projectProfile: {declared: false, valid: null}`; no stack/architecture information invented. |
| `project.yaml` invalid | `projectProfile: {declared: true, valid: false}`; `discovery.filesInvalid` carries the specific error codes; individual fields are still surfaced from whatever structurally parsed, but must be treated as **unverified**, not authoritative, until fixed. |
| `architecture.md` missing | `architectureDocAvailable: false`; a warning states the narrative is unavailable. A consuming Skill that needs architecture understanding falls back to repository-artifact inspection rather than guessing. |
| `rules/` missing | `childRules: {declared: false, files: []}`; this is a normal, valid state. |
| `exceptions.yaml` missing | `exceptions: {declared: false, ...}`; this is a normal, valid state. |

This table is the executable form of `docs/Child Repository Integration.md` Section 12 combined with the Mentor Operating Model's No Invention Rule — nothing here introduces new policy beyond making that existing policy deterministic and testable.

## Validation Reuse

`.mentor/project.yaml` is validated exactly once, by calling `validate_project_yaml.validate_file()` directly from `scripts/discover_project_context.py`. The schema itself (`docs/schema/project.schema.v1.json`) and its field-by-field reference (`docs/Project Profile Schema.md`) are not duplicated here or anywhere in this discovery layer — this document describes the *discovery-time behavior around* that validation (what happens to the surrounding context when validation fails), not the validation rules themselves.

## Mentor Compatibility

Discovery validates only whether a declared `mentor.version` range is itself syntactically valid and internally self-consistent (e.g. rejecting `>=2.0.0 <1.0.0` as contradictory) — exactly what `scripts/validate_project_yaml.py` already checks for `docs/Project Profile Schema.md`'s purposes.

It deliberately does **not** compare that range against the Mentor plugin version actually installed in the current session. There is no documented mechanism, in the current plugin architecture, for a Skill to introspect which Mentor version is active — inventing a comparison against, say, `.claude-plugin/plugin.json`'s own version would mean guessing at an installed-version signal this discovery layer cannot actually verify, which is exactly the kind of invented fact the No Invention Rule prohibits. So: when the declared range is itself valid, `compatibilityStatus` is always `"not_determined"` — not a placeholder for an unfinished feature, a deliberate, explicit statement that this question cannot be reliably answered yet. Actually checking compatibility against the installed version is tracked separately in `docs/Child Repository Integration.md` Section 22, as its own future task, not implied or half-implemented here.

Discovery never blocks a task because compatibility is undetermined. `compatibilityStatus: "not_determined"` is not an error state.

## Security / Governance Boundary

Context Discovery collects and normalizes facts; it never adjudicates them. Concretely, discovery must never (and does not) let:

- A discovered `.mentor/rules/` entry override a Mentor Mandatory rule.
- A discovered `.mentor/exceptions.yaml` entry downgrade a security finding's severity on its own — an exception is surfaced as *data about an existing, owned, scoped deviation* (`docs/Child Repository Integration.md` Section 17); applying that judgment to an actual finding is a consuming Skill's responsibility, later, if and when exception *enforcement* is implemented (not this phase).
- A child Skill definition replace Mentor governance.
- An invalid or unverified `project.yaml` field be treated as authoritative by a consuming Skill.

`docs/Child Repository Integration.md` Sections 8, 18, and 19 remain the unmodified, authoritative governance hierarchy. This capability sits entirely upstream of it.

## Read-Only Guarantee

`scripts/discover_project_context.py` only ever calls read operations against the target repository (`Path.is_dir`, `Path.is_file`, `Path.exists`, `Path.read_text`, `Path.iterdir`, `Path.stat`) — it contains no write, create, move, or delete call against any path under the target root. `scripts/run_context_discovery_tests.py`'s scenario 15 verifies this mechanically: it hashes every file under every fixture before running discovery against all of them, and asserts an exact match afterward.

## Testing

```bash
python3 scripts/run_context_discovery_tests.py
```

See `tests/context-discovery/README.md` for the fixture/scenario convention. As with `tests/schema-tests/`, this is fully automated (deterministic logic), unlike `tests/skill-tests/`'s narrative convention for LLM-judged Skill behavior.
