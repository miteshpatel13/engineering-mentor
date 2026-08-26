# Project Profile Schema (.mentor/project.yaml)

## Status

This is the finalized, versioned schema for `.mentor/project.yaml`, superseding the "EXAMPLE ONLY -- not yet the final schema" placeholder previously shown in `docs/Child Repository Integration.md`. It defines schema generation **1** (field `schemaVersion: 1`).

This document does **not** implement `.mentor` context discovery, does not wire any Mentor Skill to consume `project.yaml`, and does not redefine the Mandatory/Configurable/Advisory/Informational Mentor-rule classification from `docs/Child Repository Integration.md` Section 7 -- those remain future implementation work (see `docs/Child Repository Integration.md` Section 22).

**Important distinction:** "required / optional / extensible" below classifies *fields of this schema*. It is a different axis from the Mandatory/Configurable/Advisory/Informational classification of *Mentor governance rules* defined in `docs/Child Repository Integration.md` Section 7. A field being "required" in `project.yaml` says nothing about whether a Mentor rule is Mandatory -- do not conflate the two.

## Files

- `docs/schema/project.schema.v1.json` -- the normative, machine-readable JSON Schema (draft 2020-12) for structural validation.
- `scripts/validate_project_yaml.py` -- a dependency-light (Python stdlib + PyYAML) reference validator implementing the same structure plus semantic checks JSON Schema cannot express (Mentor version range self-consistency).
- `scripts/run_project_yaml_tests.py` -- the regression suite runner for `tests/schema-tests/project-yaml/`.
- `docs/examples/project.yaml` -- a fully populated reference example.
- `docs/examples/project.minimal.yaml` -- the minimum valid example.

## Schema Versioning

The schema has its own semantic version, independent of the Mentor plugin's own version (`docs/Versioning Strategy.md`, currently plugin `1.0.0`):

- The `schemaVersion` field inside a `project.yaml` file is an integer identifying the schema's **MAJOR generation** -- currently only `1`.
- Within generation 1, the schema itself may receive MINOR additions (new optional fields, new enum values) and PATCH clarifications (documentation, error-message wording) without requiring any child repository to change its `schemaVersion` or its existing file -- these are purely additive and backward-compatible by construction (see Compatibility Expectations below).
- A breaking change (removing a required field, repurposing an existing field's meaning, tightening a previously-open type) requires a new MAJOR schema generation: a new `project.schema.v2.json`, a new set of docs, and `schemaVersion: 2` for files that opt into it. `project.schema.v1.json` and its validator remain in place and continue to validate existing `schemaVersion: 1` files -- generations coexist rather than replacing each other in place.
- This mirrors the same generation-marker pattern used by Kubernetes `apiVersion` and GitHub Actions workflow schemas: a small integer marks which generation's rules apply, while richer SemVer tracks the schema *document's* own revision history for change-log purposes.

## Required Fields

| Field | Type | Description |
|---|---|---|
| `schemaVersion` | integer, `const: 1` | The schema generation this file conforms to. Only `1` is defined today. |
| `name` | string, non-empty | Project identifier. Recommended kebab-case (`^[a-z0-9]([a-z0-9-]*[a-z0-9])?$`) -- a validator SHOULD warn, not error, on a non-matching name; see Validation Expectations. |
| `mentor.version` | string | The Mentor compatibility range this project declares -- see Mentor Compatibility Range Syntax below. |
| `stack.language` | array of non-empty strings, `minItems: 1` | At least one programming language. Open vocabulary -- no fixed enum, since the set of languages is unbounded and Mentor Skills should adapt to whatever the child actually declares (Mentor Operating Model's No Invention Rule) rather than reject an uncommon-but-real language. |

A file missing any of these four produces `E_MISSING_REQUIRED_FIELD`.

## Optional Fields

| Field | Type | Allowed values | Notes |
|---|---|---|---|
| `stack.runtime` | array of strings | open | e.g. `Node.js`, `JVM`, `CPython`. |
| `stack.framework` | array of strings | open | e.g. `NestJS`, `Django`, `Spring Boot`. |
| `stack.database` | array of strings | open | e.g. `PostgreSQL`, `MongoDB`. |
| `stack.orm` | array of strings | open | The data-access layer -- e.g. `Prisma`, `TypeORM`, `SQLAlchemy`, or `none` for raw queries. |
| `stack.cache` | array of strings | open | e.g. `Redis`, `Memcached`. |
| `architecture.style` | string, enum | `monolith`, `modular-monolith`, `microservices`, `serverless`, `event-driven`, `other` | Bounded vocabulary (unlike `stack.*`) because Mentor Skills reason about a small number of structurally distinct architecture shapes. Use `other` plus `architecture.styleNote` (free text) for anything that doesn't fit -- this is the schema's designed escape hatch, not a gap. |
| `architecture.styleNote` | string | free text | Only meaningful alongside `style: other`, but not type-restricted to that case. |
| `architecture.api` | string, enum | `REST`, `GraphQL`, `gRPC`, `WebSocket`, `other` | Same escape-hatch pattern as `architecture.style`. |
| `architecture.apiNote` | string | free text | Same pattern as `styleNote`. |
| `testing.<category>` | string (open map) | free-form keys | e.g. `testing.unit: Jest`, `testing.integration: Supertest`, `testing.e2e: Playwright`. Deliberately an open map rather than a fixed set of named fields, since testing taxonomies vary by project. |
| `deployment.platform` | string | open | e.g. `AWS`, `GCP`, `Azure`, `on-prem`. |
| `deployment.containerized` | boolean | `true` / `false` | |
| `deployment.orchestration` | string | open | e.g. `ECS`, `Kubernetes`, `none`. |
| `deployment.region` | string | open | e.g. `us-east-1`. |
| `infrastructure.<category>` | array of strings (open map) | free-form keys | Covers "relevant infrastructure/runtime metadata" not otherwise modeled -- e.g. `infrastructure.messageQueue: [SQS]`, `infrastructure.cdn: [CloudFront]`, `infrastructure.objectStorage: [S3]`, `infrastructure.secretsManager: [...]`. |

## Extensible Fields

| Field | Type | Purpose |
|---|---|---|
| `extensions` | object, freeform | Reserved namespace for forward-compatible custom metadata the current schema generation doesn't formally model. Never deeply validated -- only checked to be an object. A future MINOR schema revision may formally "promote" a commonly used `extensions.*` key into a first-class field without breaking files that used it informally. |

Beyond `extensions`, the schema is deliberately **open at every object level** (`additionalProperties: true` on the top-level document, `stack`, `architecture`, `testing`, `deployment`, and `infrastructure`): an unrecognized field does not fail validation. The reference validator (`scripts/validate_project_yaml.py`) instead emits a non-blocking `W_UNKNOWN_TOP_LEVEL_FIELD` warning for unrecognized *top-level* keys (not nested ones, to avoid warning noise on every open map above), so authors get visibility without a newer Mentor schema silently breaking an older child file, or an older Mentor validator hard-failing a file that used a slightly newer field -- this is the concrete mechanism behind Design Principle 6 (forward/backward compatibility) from `docs/Child Repository Integration.md`.

## Mentor Compatibility Range Syntax

`mentor.version` uses a deliberately small, documented subset of semantic-versioning range syntax -- not the full `node-semver` grammar (no `^`, `~`, `||`, pre-release tags), to keep validation dependency-free and match exactly what `docs/Child Repository Integration.md` and `docs/Versioning Strategy.md` already illustrate:

```text
<comparator>? MAJOR.MINOR.PATCH (' ' <comparator>? MAJOR.MINOR.PATCH)*
```

where `<comparator>` is one of `>=`, `<=`, `>`, `<`, `=` (a bare version with no comparator means exact `=`). Examples: `>=1.0.0 <2.0.0`, `1.2.3`, `>=1.4.0`.

Two independent checks apply:

1. **Syntax** -- every space-separated term must match the grammar above. A malformed term (e.g. `whatever`, `^1.0.0`, `1.0`) produces `E_INVALID_MENTOR_VERSION_RANGE_SYNTAX`. This check is also encoded directly in `docs/schema/project.schema.v1.json` via a regex `pattern`.
2. **Self-consistency** -- if both a lower bound (`>=`/`>`) and an upper bound (`<=`/`<`) are present, the lower bound must not exceed the upper bound (e.g. `>=2.0.0 <1.0.0` is contradictory and unsatisfiable). This produces `E_MENTOR_VERSION_RANGE_CONTRADICTORY`. **This check cannot be expressed in plain JSON Schema** and is only performed by `scripts/validate_project_yaml.py` -- a consumer relying on JSON Schema alone (e.g. an editor's YAML language server) will accept a syntactically valid but contradictory range; use the reference validator (or an equivalent semantic check) wherever that matters.

Caret/tilde/OR-range support and pre-release tags are explicitly out of scope for schema generation 1 (see `docs/Child Repository Integration.md` Section 22, "Future Implementation Work").

## Validation Expectations

| Condition | Result | Code |
|---|---|---|
| A required field is absent | Error | `E_MISSING_REQUIRED_FIELD` |
| A field has the wrong type (e.g. `stack.language` is a string, not an array) | Error | `E_INVALID_TYPE` |
| A required array is present but empty (e.g. `stack.language: []`) | Error | `E_INVALID_VALUE` |
| An enum field (`architecture.style`, `architecture.api`) holds a value outside its allowed set | Error | `E_INVALID_ENUM` |
| `schemaVersion` is not an integer, or is an integer this validator generation doesn't support | Error | `E_SCHEMA_VERSION_UNSUPPORTED` (unsupported value) or `E_INVALID_TYPE` (wrong type) |
| `mentor.version` doesn't match the supported grammar | Error | `E_INVALID_MENTOR_VERSION_RANGE_SYNTAX` |
| `mentor.version`'s bounds are mutually unsatisfiable | Error | `E_MENTOR_VERSION_RANGE_CONTRADICTORY` |
| The file isn't valid YAML at all | Error | `E_MALFORMED_YAML` |
| `name` doesn't match the recommended kebab-case pattern | Warning (non-blocking) | `W_NAME_NOT_KEBAB_CASE` |
| An unrecognized top-level field is present | Warning (non-blocking) | `W_UNKNOWN_TOP_LEVEL_FIELD` |

Errors make the file invalid (validator exit code `1`); warnings do not (exit code `0`). This split is deliberate: strict, deterministic rejection for anything that would cause a Mentor Skill to misinterpret the file (missing/mistyped/out-of-range data), and non-blocking visibility for anything that's merely unusual (an unrecognized field a newer schema might define, a name that doesn't follow the recommended convention).

## How Mentor Consumes This Information

Not implemented in this task (see `docs/Child Repository Integration.md` Sections 12-13 and Section 22). Conceptually, once context discovery is implemented, a Mentor Skill would read `project.yaml` first (before `architecture.md`, `rules/`, or `exceptions.yaml`, per Section 12's discovery order) to establish the child's declared stack, architecture style, and Mentor version compatibility before reasoning about anything else -- e.g. `stack.orm: Prisma` would let `/engineering-mentor:database-review` phrase indexing guidance in Prisma-specific terms rather than generic ORM language, per the Mentor Operating Model's No Invention Rule.

## Backward / Forward Compatibility Expectations

- **A well-formed generation-1 file remains valid under every future MINOR/PATCH revision of the generation-1 schema.** Only a new MAJOR generation (`schemaVersion: 2`) may invalidate it, and only if the child opts in by changing `schemaVersion`.
- **A file using a field a given validator doesn't yet recognize does not fail validation.** Unknown top-level fields warn; unknown nested fields inside the already-open maps (`stack`, `testing`, `deployment`, `infrastructure`, `extensions`) don't even warn. This lets a child repository or a newer Mentor version introduce a field ahead of formal schema documentation without breaking older tooling.
- **A validator must reject an unsupported `schemaVersion` explicitly** (`E_SCHEMA_VERSION_UNSUPPORTED`) rather than attempting to interpret an unknown generation's file under generation-1 rules -- silently misinterpreting a future generation's file would be worse than a clear rejection.
- **`mentor.version` range validity is independent of `schemaVersion`.** A child can be compatible with a wide range of Mentor plugin versions while still declaring `schemaVersion: 1` for its own file shape; the two version axes (Mentor plugin version, project.yaml schema generation) are intentionally decoupled so one can evolve without forcing the other.
