---
id: 03-testing-requirements
title: Prefer integration tests over deep mocking for service-layer code
classification: advisory
scope: "src/services/** test coverage"
category: testing
owner: qa-guild
status: active
---

> **EXAMPLE FILE — for documentation purposes only.** This is not a real
> child rule in this repository. It illustrates the `.mentor/rules/`
> frontmatter contract defined in `docs/Child Rules and Exceptions.md`,
> including a non-Mandatory (Advisory) classification.

# Prefer Integration Tests Over Deep Mocking for Service-Layer Code

## Description

For code under `src/services/`, prefer a real (test-database-backed)
integration test over a unit test that mocks the Prisma client to a
significant depth. A small number of pure-logic unit tests are fine;
avoid tests that mostly assert "the mock was called with X."

## Rationale

This project has found deeply-mocked service tests tend to pass even
when the real query is wrong, and to churn heavily whenever the query
shape changes — integration tests against a real (containerized) test
database catch more real defects here.

This is a **Child Advisory** rule: a reviewer can deviate from it when
justified (e.g. a genuinely pure function with no I/O), without needing
the formal exception mechanism — but per `docs/Child Rules and
Exceptions.md` Section 4, the deviation should be visible (stated in the
review), not silent. This contrasts with the Child Mandatory examples in
`01-api-conventions.md` and `02-database-conventions.md`, which cannot be
silently or informally deviated from.

## Applicability

Applies to new or materially-changed tests under `src/services/`. Does
not apply to `src/utils/` pure-function tests, where mocking concerns
don't arise.

## Examples

**Preferred:** a test that spins up the test database, seeds a fixture
order, calls `orderService.cancel(id)`, and asserts the resulting row
state.

**Discouraged (not forbidden — Advisory):** a test that mocks
`prisma.order.update` and asserts it was called with a particular
argument shape, without ever touching a real database.
