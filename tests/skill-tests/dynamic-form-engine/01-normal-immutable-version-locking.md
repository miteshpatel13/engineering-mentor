---
id: dynamic-form-engine-01-normal-immutable-version-locking
category: normal
skill_under_test: skills/dynamic-form-engine/SKILL.md
---

# Scenario: Form Version Locking on First Submission

## Input Material

> An administrator creates a custom feedback form (Version 1). User A submits a response against Version 1. The administrator then attempts to add a mandatory rating field to the form.

## Pass Criteria

- Marks Version 1 as immutable (`IsLocked = true`) upon receiving User A's submission.
- Mandates that modifying the form creates a new `FormVersionNumber = 2`.
- Ensures User A's historical submission remains pinned to Version 1 so field meanings do not drift.

## Fail Signals

- Editing Version 1 in-place after submissions exist.
- Failing to pin submissions to their exact rendering version ID.
