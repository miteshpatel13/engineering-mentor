---
id: skill-creator-04-failure-inconclusive-overlap
category: failure-handling
skill_under_test: skills/skill-creator/SKILL.md
---

# Scenario: Overlap Check Is Genuinely Inconclusive

## Input Material

> A candidate Skill about "validating that API responses never leak internal database identifiers" plausibly overlaps both an existing `api-review` Skill (Review-type, evaluates API responses) and a proposed `identifier-strategy` Domain Pattern Skill (the source-of-truth for the identifier-exposure rule itself). It is genuinely unclear whether this candidate should be folded into one of the two, split, or proceed separately. Draft the Skill.

## Pass Criteria

- The response stops and states the overlap classification is inconclusive between the two named Skills, rather than picking one silently.
- The response names what would resolve the ambiguity (e.g. whether the candidate is meant to be an evaluation, in which case it likely belongs inside `api-review` citing `identifier-strategy`, rather than a third Skill).
- No `skills/<name>/SKILL.md` draft is presented as finished/ready while this ambiguity is unresolved.

## Fail Signals

- Silently picking one classification and drafting a complete Skill as though the ambiguity didn't exist.
- Drafting three overlapping Skills instead of resolving the ambiguity.
