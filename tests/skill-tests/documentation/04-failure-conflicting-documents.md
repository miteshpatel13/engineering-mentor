---
id: documentation-04-failure-conflicting-documents
category: failure-handling
skill_under_test: skills/documentation/SKILL.md
---

# Scenario: Two Existing Documents Disagree

## Input Material

> An existing architecture document states the system uses a message queue for order processing. A separate, more recent API document describes order processing as fully synchronous, with no queue. Update the documentation for order processing.

## Pass Criteria

- The response does not silently merge or pick one description without investigation.
- The response states the conflict explicitly and recommends verifying against actual current code before writing anything as Implemented.
- If verification is performed (per the scenario as given, code should be checked), the document is updated to match reality and the stale document is flagged/corrected, not left standing unaddressed.

## Fail Signals

- Silently choosing one existing document's description without checking actual code.
- Leaving both conflicting documents in place with no flag.
