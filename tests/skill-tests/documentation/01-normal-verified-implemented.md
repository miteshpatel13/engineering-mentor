---
id: documentation-01-normal-verified-implemented
category: happy-path
skill_under_test: skills/documentation/SKILL.md
---

# Scenario: Documenting a Fully Implemented, Verified Feature

## Input Material

> Document the password-reset flow. The engineer confirms they read the actual controller and service code, and ran the existing test suite for it, which passes.

## Pass Criteria

- The documented behavior is labeled Implemented.
- The response states (or asks for confirmation of) how the claim was verified — reading the actual code / running the actual test — not assumed from the ticket.
- The documentation describes what the code actually does, not what the original ticket requested, if the two could differ.

## Fail Signals

- Documenting the flow based on the ticket description without any verification step against actual code.
- Omitting the Implemented label as if unlabeled prose were sufficient.
