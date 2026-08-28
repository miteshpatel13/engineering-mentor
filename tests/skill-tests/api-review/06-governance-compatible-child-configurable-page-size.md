---
id: api-review-06-governance-compatible-child-configurable-page-size
category: governance-sensitive
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Child Configurable Default Page Size Compatible With Mentor Mandatory Pagination Requirement

## Input Material

> Context discovery reports a Mentor Mandatory requirement that collection-returning endpoints be paginated, with the default page size left to the child project (Mentor Configurable boundary). A declared Child Configurable rule sets the default page size to 50. The `GET /orders` endpoint under review implements cursor-based pagination with a default page size of 50, matching the child's configured value.

## Pass Criteria

- Recognizes the Mentor Mandatory "must be paginated" requirement and the Child Configurable specific default (50) as Compatible — both satisfied simultaneously.
- Does not flag the specific default value as a finding; Mentor's boundary is only that pagination exists, the child owns the default size.
- States the classification explicitly rather than saying nothing because there's no defect.

## Fail Signals

- Treating the child-selected default page size as itself requiring justification.
- Failing to recognize the endpoint as satisfying the pagination requirement at all.
