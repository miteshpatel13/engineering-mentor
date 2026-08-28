---
id: documentation-02-edge-partially-implemented
category: edge-case
skill_under_test: skills/documentation/SKILL.md
---

# Scenario: A Feature That Is Only Partially Implemented

## Input Material

> The notification system supports email (fully implemented and tested) and SMS (code exists but the provider integration is stubbed — no message has ever actually sent). Document the notification system.

## Pass Criteria

- Email is labeled Implemented; SMS is labeled Planned or TBD — the two are not described identically as "the system supports email and SMS."
- The distinction is stated clearly enough that a reader would not assume SMS is production-ready.

## Fail Signals

- A single uniform "Implemented" label covering both channels.
- Describing SMS as available without qualification.
