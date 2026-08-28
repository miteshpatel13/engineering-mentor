---
id: api-review-19-edge-graphql-contract-reviewed-with-rest-expectations
category: edge
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: GraphQL Contract Reviewed — Do Not Apply REST-Specific Versioning Expectations

## Input Material

> Context discovery confirms the repository's API layer is GraphQL. The change under review adds a new optional field `preferredLocale` to the existing `User` type in the schema, with no changes to any existing field's name, type, or nullability, and no field removed. The material includes no `@deprecated` directive usage anywhere in this change (none is needed — nothing is being deprecated).

## Pass Criteria

- Applies GraphQL's own schema-evolution correctness principles — additive, optional fields are a normal, non-breaking way to evolve a GraphQL schema, per the Skill's own named Edge Case — rather than REST-specific versioning expectations (a new API version, a URL path change, a deprecation *period* in the REST sense) that don't map cleanly to GraphQL's schema-evolution model.
- Does not flag the absence of a versioning strategy (in the REST/`docs/Versioning Strategy.md` MAJOR/MINOR/PATCH sense) as a defect — an additive, optional GraphQL field is the correct, idiomatic way to evolve the schema and needs no such accommodation.
- Would still flag a genuinely breaking GraphQL change correctly (e.g. removing a field, changing a field from nullable to non-nullable, changing a field's type) using GraphQL's own breaking-change vocabulary (schema evolution via additive fields, `@deprecated` directives for planned removal) — this fixture's material doesn't contain such a change, but the Pass Criteria for a reviewer applying this Skill correctly is that it would recognize one if present, not that GraphQL is exempt from compatibility review entirely.

## Fail Signals

- Flagging the new field for lacking a REST-style version bump or deprecation period — a category error, applying REST expectations to a GraphQL contract.
- Treating GraphQL contracts as exempt from backward-compatibility review altogether, rather than applying GraphQL's own correctness principles.
