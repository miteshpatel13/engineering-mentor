---
id: api-review-14-rule-coverage-pagination
category: rule-coverage
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Unbounded Collection Endpoint With No Pagination Mechanism

## Input Material

> `GET /search/products` accepts a free-text query and returns every matching product in a single JSON array response, with no `limit`/`offset`/`cursor` parameter accepted anywhere in the endpoint's contract, and the material states the product catalog currently holds over 2 million items and grows continuously.

## Pass Criteria

- Flags the endpoint for the absence of any pagination mechanism per Rules → Pagination, citing the unbounded, continuously-growing collection size as the evidence that this isn't a small, inherently-bounded case.
- States the concrete risk (slow/memory-heavy/timed-out responses as the catalog grows) rather than a generic "should paginate" statement with no grounding.
- Recommends a cursor- or offset-based mechanism consistent with Rules → Pagination, without inventing a specific implementation the material doesn't call for.

## Fail Signals

- Not flagging the endpoint because "search" endpoints are assumed exempt with no evidence-based reason.
- Flagging pagination as missing on a materially different, small/bounded endpoint elsewhere not shown in this scenario (i.e. over-generalizing the finding).
