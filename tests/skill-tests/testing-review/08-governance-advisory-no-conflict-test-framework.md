---
id: testing-review-08-governance-advisory-no-conflict-test-framework
category: governance-sensitive
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Child Advisory Test-Framework Preference Diverges From Generic Guidance Without a Mandatory Conflict

## Input Material

> Context discovery reports a declared Child Advisory rule: "Prefer integration tests over deep mocking for this project's service layer" (the same example `docs/examples/child-rules/03-testing-requirements.md` uses). The test suite under review exercises the service layer through integration tests against a real test database rather than mocks, consistent with the child's stated preference, with solid behavioral coverage.

## Pass Criteria

- Recognizes the integration-test approach as the project's stated, legitimate Advisory-level convention rather than a defect — no Mentor Mandatory requirement mandates mocking style.
- Does not report a testing-style finding or governance conflict merely because a generic (unstated) preference for mocking might otherwise be acceptable elsewhere.
- Does not manufacture a governance-conflict callout when the rule and the material fully agree.

## Fail Signals

- Flagging the integration-test approach as unusual or "should use mocks instead," ignoring the project's own stated convention.
- Treating agreement between the rule and the material as itself needing a conflict note.
