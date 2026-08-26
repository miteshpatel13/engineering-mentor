---
id: 01-api-conventions
title: All admin APIs require MFA-backed authentication
classification: mandatory
scope: "All routes under /admin/**"
category: api
owner: platform-team
status: active
---

> **EXAMPLE FILE — for documentation purposes only.** This is not a real
> child rule in this repository. It illustrates the `.mentor/rules/`
> frontmatter contract defined in `docs/Child Rules and Exceptions.md`.
> `engineering-mentor` itself has no `.mentor/` directory (see
> `docs/Child Repository Integration.md`'s Design Principles).

# All Admin APIs Require MFA-Backed Authentication

## Description

Every route under `/admin/**` must require a session established via
multi-factor authentication, in addition to standard authentication.

## Rationale

Admin routes carry elevated privileges (user impersonation, billing
overrides, feature-flag control). Standard password/session
authentication alone is judged insufficient for this blast radius.

This is a **Child Mandatory** rule: it is mandatory for this project,
not a claim of authority over Mentor Mandatory rules. It **adds** a
requirement on top of Mentor's own Mandatory authentication/authorization
baseline (`context/standards/Security Standards.md`) — it does not, and
structurally cannot, weaken or replace it. See
`docs/Child Rules and Exceptions.md` Section 4 ("Child Mandatory
Does Not Outrank Mentor Mandatory") for the general principle this
example demonstrates.

## Applicability

Applies to every route registered under the `/admin` path prefix,
regardless of HTTP method. Does not apply to `/api/v1/**` customer-facing
routes, which follow the repository's standard (non-MFA) authentication
rule instead.

## Examples

**Compliant:** an admin route handler that checks `req.session.mfaVerifiedAt`
is set and recent, in addition to the existing `requireAuth` middleware.

**Non-compliant:** an admin route protected only by `requireAuth`, with no
MFA check — this would be flagged against this rule during review, in
addition to (not instead of) any Mentor-level authorization findings that
already apply.
