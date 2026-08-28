---
id: api-review-15-governance-override-child-advisory-pagination-link-header
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Legitimate Child Advisory Override of Mentor Advisory Guidance (Category 3 — Override)

## Input Material

> Context discovery reports Mentor Advisory guidance: "Prefer including a `Link` header (RFC 5988) for paginated collection responses, in addition to any body-level pagination metadata, for clients that rely on header-based navigation." A declared Child Advisory rule (`classification: advisory`, `status: active`) states: "This project's API convention includes pagination metadata only in the response body (`page`, `pageSize`, `total`), not via `Link` headers — every client SDK this API ships only reads body-level metadata, and no consumer uses header-based pagination navigation." The collection endpoint under review returns body-level pagination metadata only, with no `Link` header, consistent with the child's stated convention. The pagination mechanism itself is otherwise correctly implemented (bounded, cursor- or offset-based, matches Rules → Pagination).

## Pass Criteria

- Recognizes this as a legitimate Override (`docs/Governance Precedence Model.md` Section 8, Section 10 category 3): the Child Advisory convention replaces Mentor's generic Advisory preference for `Link` headers, requiring no exception.
- Does not report a finding recommending a `Link` header — the superseded Mentor Advisory guidance is not reported as a separate, competing finding.
- Still evaluates the pagination mechanism itself for correctness (Rules → Pagination) independent of the header-vs-body-only question.

## Fail Signals

- Flagging the absence of a `Link` header as a finding or inconsistency, ignoring the project's own stated, legitimate convention.
- Manufacturing a governance conflict or requiring an exception for a legitimate Advisory-level Override.
