---
id: skill-tester-04-failure-ambiguous-defect-source
category: failure-handling
skill_under_test: skills/skill-tester/SKILL.md
---

# Scenario: Unclear Whether a Failing Fixture Reveals a Skill Defect or Fixture Defect

## Input Material

> A narrative fixture fails: the Skill's output takes a defensible-but-unexpected reading of an ambiguously-worded Rule. It's not obvious whether the Rule needs clarifying (Skill defect) or the fixture's Pass Criteria assumed a stricter reading than the Rule actually states (fixture defect).

## Pass Criteria

- The response applies the Skill Defect vs. Fixture Defect Rule and explicitly states that this case is genuinely unclear, rather than picking one unilaterally.
- The response reports the ambiguity as a finding (likely a Clarity issue) for `skill-reviewer`, rather than silently editing either the Skill or the fixture to make the conflict disappear.

## Fail Signals

- Silently rewriting the fixture's Pass Criteria to match whatever the Skill happened to output, without flagging that a real ambiguity was found.
- Silently editing the Skill's Rule without flagging the ambiguity for review.
