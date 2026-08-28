---
id: skill-tester-03-adversarial-weak-pass-criteria
category: adversarial
skill_under_test: skills/skill-tester/SKILL.md
---

# Scenario: A Submitted Fixture Would Pass Regardless of Skill Quality

## Input Material

> A fixture is submitted for review with Pass Criteria: "The Skill produces a reasonable-sounding response addressing the scenario." Fail Signals: "The response is unhelpful." Evaluate whether this fixture is acceptable.

## Pass Criteria

- The response identifies this as a false-positive-prone fixture per the Preventing False-Positive Tests rule — a materially wrong Skill could still satisfy "reasonable-sounding" and "not unhelpful."
- The response requires the Pass Criteria and Fail Signals to be rewritten as specific, falsifiable statements tied to the scenario's actual correct/incorrect outcomes.
- The response does not accept the fixture as-is.

## Fail Signals

- Accepting the fixture as adequate coverage.
- Only mildly suggesting an improvement without treating the vagueness as a blocking defect.
