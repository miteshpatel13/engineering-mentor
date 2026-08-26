# Skill Testing & Evaluation Standard

A Skill is not production-ready merely because its instructions look correct.

Test:
- Happy path
- Edge cases
- Invalid input
- Missing context
- Ambiguous requests
- Conflicting requirements
- Existing-code scenarios
- Large inputs
- Failure scenarios
- Security-sensitive scenarios

Evaluation should check:
- Correctness
- Consistency
- False positives
- False negatives
- Unintended side effects
- Compatibility with repository conventions
- Clarity of output

When a failure is discovered:
1. Record the scenario.
2. Identify the root cause.
3. Update the Skill.
4. Add a regression test.
5. Re-run the evaluation.
