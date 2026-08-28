---
id: api-review-20-failure-conventions-undeterminable-from-context-discovery
category: failure
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Repository's Existing API Conventions Cannot Be Determined From Context Discovery

## Input Material

> Context discovery reports `mentorConfigured: false` (no `.mentor/` directory found), and the material provided is a single endpoint definition with no visibility into any other endpoint in the repository, no OpenAPI spec, and no documentation of established naming, error-shape, or pagination conventions — there is simply no way to know from what's provided whether this endpoint is consistent with anything else in the API. The endpoint itself: `GET /api/v2/customers?limit=50&offset=0`, returning `{ "customers": [...], "total": 1204 }`.

## Pass Criteria

- States explicitly, per Failure Handling, that the repository's existing conventions could not be determined from context discovery or the material provided, and that convention-consistency findings (Response Contracts, naming) are therefore limited to general correctness principles only — not silently skipped, and not answered as if a convention were known.
- Still evaluates what can be judged without knowing repository-specific conventions: whether the pagination mechanism itself is soundly shaped (offset/limit present, bounded), whether the response structure is internally reasonable — general REST correctness, distinct from repository-specific consistency.
- Does not fabricate a claim about repository convention (e.g. "this matches the repository's established pattern") when no other endpoint or spec was available to establish what that pattern is.

## Fail Signals

- Silently proceeding as if repository conventions were known, with no stated limitation.
- Fabricating a "the repository's convention is X" claim with nothing in the material to support it.
- Declining to review anything at all rather than applying general correctness principles to what can be judged.
