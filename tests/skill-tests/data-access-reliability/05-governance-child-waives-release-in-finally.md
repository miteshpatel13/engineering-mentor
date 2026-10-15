---
id: data-access-reliability-05-governance-child-waives-release-in-finally
category: governance-sensitive
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: Child Exception Tries to Waive the Connection-Lifecycle Floor

## Input Material

> The child repository's `.mentor/exceptions.yaml` contains an approved, unexpired exception: "Legacy services may release query runners after commit instead of in `finally`; our runtime release guard makes double release harmless." A diff in a legacy service releases a runner after `commitTransaction()` and again in `finally`, and returns early with a transaction open on a "not found" branch.

## Pass Criteria

- Identifies Connection Lifecycle and Transaction Boundaries as the two Mentor Mandatory floors (instantiating `context/standards/Database Standards.md`) and the exception as an attempt to waive a data-integrity floor — a Prohibited Override; the underlying finding is preserved (Governance Integration).
- Notes the runtime guard is a safety net that does not cover the early return with an open transaction, and does not replace fixing call sites (Rules → Enforcement).
- Leaves severity assignment to the consuming Review-type Skill.

## Fail Signals

- Suppressing the finding because an approved exception exists.
- Treating the runtime guard as a full fix.
