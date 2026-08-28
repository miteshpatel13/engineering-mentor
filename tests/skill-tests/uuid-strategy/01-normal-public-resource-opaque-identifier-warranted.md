---
id: uuid-strategy-01-normal-public-resource-opaque-identifier-warranted
category: normal
skill_under_test: skills/uuid-strategy/SKILL.md
---

# Scenario: Designing Identifiers for a Public-Facing Order Resource

## Input Material

> Design the identifier strategy for an `order` resource exposed via `GET /api/orders/:id`, reachable by any authenticated customer for their own orders. The current design uses the database's auto-increment integer primary key directly in the URL.

## Pass Criteria

- Identifies the sequential integer-in-URL exposure as an enumeration/business-information leak (Rules → When an Opaque Identifier Is Warranted) — a caller could increment the value to infer total order volume.
- Recommends a separate opaque public identifier for the URL/response, while retaining the sequential integer as the internal storage/join key (Rules → Storage, Indexing, and Ordering).
- States the resolution boundary explicitly — the public identifier resolves to the internal one once, early in the request path (Rules → Resolution Boundary).
- Notes separately that an authorization/ownership check is still required regardless of the identifier change (Rules → Exposure and Security Considerations) — opacity alone doesn't secure the endpoint.

## Fail Signals

- Recommending the opaque identifier as sufficient on its own without separately noting the authorization requirement.
- Recommending the internal sequential key be dropped entirely rather than retained for storage/joins.
