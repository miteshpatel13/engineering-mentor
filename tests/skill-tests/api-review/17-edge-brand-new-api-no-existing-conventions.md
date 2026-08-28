---
id: api-review-17-edge-brand-new-api-no-existing-conventions
category: edge
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Brand-New API With No Existing Conventions to Be Consistent With

## Input Material

> Context discovery reports this is the very first API endpoint being added to a brand-new service repository — no existing endpoints, no established error shape, no established pagination pattern, no established naming convention anywhere in the repository. The endpoint under review is `POST /widgets`, returning `{ "id": "...", "name": "...", "createdAt": "..." }` on success and `{ "error": "validation_failed", "details": [...] }` on a `422` validation failure.

## Pass Criteria

- Evaluates the endpoint against general REST/GraphQL correctness principles instead of a repository-specific convention, per the Skill's own named Edge Case ("Brand-new API with no existing conventions to be consistent with").
- States explicitly that no repository-specific convention exists yet to check consistency against — does not invent one (e.g. claiming "the repository's convention is X" with no basis) and does not treat this endpoint's own shape as automatically "the convention" other endpoints must now match.
- Does not manufacture a Response Contracts or naming-convention finding merely because there is nothing yet to be consistent *with* — the endpoint is evaluated on general correctness (is the shape itself reasonable, is the status code correct for the outcome), not flagged for "inconsistency" against a convention that doesn't exist.

## Fail Signals

- Fabricating an existing repository convention to compare the endpoint against when the material states none exists.
- Flagging the endpoint as "inconsistent" with unstated, invented conventions.
- Declining to review the endpoint at all on the theory that consistency review requires an existing pattern — general REST/GraphQL correctness principles still apply and should still be checked.
