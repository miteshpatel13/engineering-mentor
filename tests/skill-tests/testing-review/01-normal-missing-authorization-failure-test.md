---
id: testing-review-01-normal-missing-authorization-failure-test
category: normal
skill_under_test: skills/testing-review/SKILL.md
---

# Scenario: Security-Sensitive Endpoint Missing an Authorization-Failure Test

## Input Material

> The test suite for `DELETE /accounts/:id` includes three tests: successful deletion by the account owner, a 404 for a non-existent account, and a validation test for a malformed ID. There is no test asserting that a caller who does not own the account is rejected.

## Pass Criteria

- Flags this under Authorization Coverage: the suite has no test proving an unauthorized caller is rejected, despite otherwise-thorough coverage.
- States this explicitly as a gap distinct from the code's actual authorization correctness — this Skill reviews whether a test would catch a regression, not whether the endpoint is currently vulnerable.
- Does not let the otherwise-strong coverage on other dimensions offset this specific gap.

## Fail Signals

- Treating the three existing tests as sufficient coverage overall and not flagging the authorization gap.
- Conflating this finding with a claim about the endpoint's actual current security correctness (that's `security-review`'s domain).
