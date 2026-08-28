---
id: api-review-18-edge-breaking-change-internal-only-no-external-consumers
category: edge
skill_under_test: skills/api-review/SKILL.md
---

# Scenario: Breaking Change Proposed for a Genuinely Internal-Only API With No External Consumers

## Input Material

> A proposed change removes a field from an endpoint's response with no deprecation period or versioning accommodation. Context discovery and the material both confirm this endpoint is served only on an internal-only network segment, is called exclusively by two other services in the same monorepo (both call sites are shown in the material, and both are being updated in the same change to stop reading the removed field), and the repository's own architecture documentation states this endpoint has never been exposed externally.

## Pass Criteria

- States explicitly that the backward-compatibility bar is lower for this genuinely internal-only contract, per the Skill's own named Edge Case — because the material actually establishes there are no external consumers (both internal call sites are shown and are being updated in the same change), not merely asserted.
- Does not apply the same HIGH-severity, blocking Versioning/Compatibility treatment this Skill would correctly apply to a public API breaking change (contrast with the Skill's own positive Example) — the risk profile is genuinely different when all consumers are visible and are being updated together.
- Still checks that the material's claim is actually substantiated (both call sites shown, both being updated) rather than accepting an unverified assertion of "internal only" at face value — if the material asserted internal-only status without showing the call sites, that would not meet this Edge Case's evidence bar (see Fail Signals).

## Fail Signals

- Treating this identically to a public API breaking change (HIGH severity, blocking, requires a deprecation period) when the material actually establishes there are no external consumers and both are being updated together.
- Applying the lower bar merely because the material *claims* "internal only" with no supporting evidence (e.g. no call sites shown) — the Skill's own Edge Case requires this to be established by the material, not assumed from an unverified claim.
