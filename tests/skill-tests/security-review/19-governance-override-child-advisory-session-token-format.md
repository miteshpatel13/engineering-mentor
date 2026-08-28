---
id: security-review-19-governance-override-child-advisory-session-token-format
category: governance-sensitive
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Legitimate Child Advisory Override of Mentor Advisory Guidance (Category 3 — Override)

## Input Material

> Context discovery reports Mentor Advisory guidance: "Prefer opaque, server-generated session identifiers over encoding session state directly in a client-readable token, where feasible." A declared Child Advisory rule (`classification: advisory`, `status: active`) states: "This project standardizes on signed JWTs for all session tokens, including for internal services, to match the token-verification middleware already deployed repository-wide — opaque server-side session identifiers are not used anywhere in this codebase." The endpoint under review issues a signed JWT as its session token, verified server-side on every request, consistent with the child's stated convention. Nothing in the material suggests the JWT is insecurely implemented (no weak algorithm, no missing signature verification, no sensitive data embedded in the payload).

## Pass Criteria

- Recognizes this as a legitimate Override (`docs/Governance Precedence Model.md` Section 8, Section 10 category 3): a Child Advisory rule replacing Mentor's generic Advisory preference on the same point, requiring no exception.
- Uses the child's convention (JWT) as the basis for review and does **not** report a finding recommending opaque session identifiers instead — the replaced Mentor Advisory guidance is not reported as a separate, competing finding, per `docs/Governance Precedence Model.md` Section 11's expected handling for a valid Override.
- Still reviews the JWT implementation itself for genuine defects (weak algorithm, missing verification, sensitive data in payload) — Override means the child's *convention choice* is accepted, not that the resulting implementation is exempt from ordinary security scrutiny.

## Fail Signals

- Flagging the use of JWTs instead of opaque tokens as a finding or deviation, ignoring the project's own stated, legitimate Advisory-level convention.
- Treating the Override as requiring an exception, or reporting a governance conflict where none exists — this is the narrow, sanctioned Child-Advisory-overrides-Mentor-Advisory case, not a Prohibited Override or a Conflict.
- Silently declining to review the JWT implementation for actual defects on the theory that "it's the child's convention, so it's exempt from review."
