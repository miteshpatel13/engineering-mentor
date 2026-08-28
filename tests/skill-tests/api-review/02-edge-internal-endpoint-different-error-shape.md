---
id: api-review-02-edge-internal-endpoint-different-error-shape
category: edge
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Internal Endpoint's Error Shape Differs From Public API, By Established Convention

## Input Material

> Review a new internal-only endpoint whose error responses use a different shape (`{ errorCode, message }`) than the repository's public-facing API (`{ error: { type, detail } }`). Context discovery confirms the repository already maintains two distinct, documented error conventions — one for public endpoints, one for internal-only endpoints — and this is consistent with the internal convention.

## Pass Criteria

- Does not flag the differing error shape as an inconsistency finding — Rules → Response Contracts checks against the repository's own established pattern, and the material shows this is the established pattern for internal endpoints, not a deviation.

## Fail Signals

- Flagging the internal endpoint's error shape as inconsistent with the public API's shape, ignoring the repository's own documented two-convention pattern.
