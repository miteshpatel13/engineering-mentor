---
id: 02-database-conventions
title: All database access must use Prisma services
classification: mandatory
scope: "All backend database access code (excludes one-time, reviewed migration scripts)"
category: database
owner: platform-team
status: active
---

> **EXAMPLE FILE — for documentation purposes only.** This is not a real
> child rule in this repository. It illustrates the `.mentor/rules/`
> frontmatter contract defined in `docs/Child Rules and Exceptions.md`.

# All Database Access Must Use Prisma Services

## Description

Application code must read and write the database exclusively through
the project's generated Prisma client, wrapped in a `services/` layer.
Raw SQL strings, manually-built query strings, or a second ORM are not
permitted in application code.

## Rationale

Centralizing data access through one client and one service layer keeps
query construction consistent, reviewable, and type-checked, and avoids
splitting query-building conventions across two different tools.

This example is written as **Child Mandatory** because the project in
this illustration has chosen to disallow raw SQL outright, with no
carve-out — a **Child Configurable** variant would instead be used if the
project wanted to allow some parameterization (e.g. "raw SQL is
permitted only in `scripts/reporting/`, subject to review"). Either way,
this rule does not affect, and cannot weaken, Mentor's own
injection-prevention Mandatory rule (`context/standards/Security
Standards.md`) — a raw SQL string that concatenates user input remains a
Mentor CRITICAL finding regardless of what this rule says; this rule
only adds an additional, project-specific "don't use raw SQL at all"
requirement on top.

## Scope

Applies to all backend service code under `src/`. Does **not** apply to
`scripts/one-time-migrations/`, which is reviewed and approved on a
per-script basis outside this rule (exact directory/glob matching
semantics are deferred — see `docs/Child Rules and Exceptions.md`
Section 6).

## Examples

**Compliant:** `await orderService.findById(id)`, where `orderService`
wraps the generated Prisma client.

**Non-compliant:** `db.query('SELECT * FROM orders WHERE id = ?', [id])`
inside an application route handler — flagged against this rule (Child
Mandatory: use the service layer) independently of whatever a Mentor
security review already says about the query itself.
