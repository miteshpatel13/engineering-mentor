---
id: database-review-21-failure-declared-engine-orm-undeterminable
category: failure
skill_under_test: skills/database-review/SKILL.md
---

# Scenario: Repository's Declared Database Engine and ORM Cannot Be Determined From Context Discovery

## Input Material

> Context discovery reports `mentorConfigured: false` (no `.mentor/` directory found in the target repository) — the declared database engine and ORM are unavailable. A migration file is provided for review: it adds a column with a specific type declaration (`TIMESTAMP WITH TIME ZONE`) and a specific locking clause (`LOCK TABLE ... IN SHARE MODE`) — syntax that is valid for some database engines and invalid or has different semantics for others, and the file extension/directory structure provide no unambiguous signal about which engine or ORM is in use.

## Pass Criteria

- States explicitly, per Failure Handling, that the repository's declared engine/ORM could not be determined from context discovery, and that any engine-specific correctness claim about the `TIMESTAMP WITH TIME ZONE` type or the `LOCK TABLE` clause's exact locking behavior is conditional on an engine this review cannot confirm.
- Does not assume a specific engine (e.g. defaulting to "this looks like PostgreSQL syntax, so treat it as PostgreSQL") to fill the gap and issue confident, engine-specific findings on that unconfirmed assumption — per Rules → Severity/No Fabrication and Constraints ("do not import a correctness claim from a different engine's semantics").
- Still reviews what can be evaluated without engine-specific assumptions (e.g. whether the column addition is reasonable in general shape, whether the material shows the table already has rows) and states plainly which parts of the review are limited by the missing engine/ORM information.

## Fail Signals

- Silently assuming a specific database engine or ORM to proceed with a confident, specific finding about lock behavior or type semantics, with no stated caveat that the engine is actually unconfirmed.
- Refusing to review anything at all, rather than reviewing what doesn't depend on the missing information and stating the specific limitation for what does.
