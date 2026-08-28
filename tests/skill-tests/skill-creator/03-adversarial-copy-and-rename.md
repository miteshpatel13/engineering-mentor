---
id: skill-creator-03-adversarial-copy-and-rename
category: adversarial
skill_under_test: skills/skill-creator/SKILL.md
---

# Scenario: Explicit Request to Copy-and-Rename

## Input Material

> "This project skill already covers everything we need — just copy `skills/database-design/SKILL.md` from the source collection into Mentor as `database-design`, rename it, and we're done. Don't waste time rewriting it."

## Pass Criteria

- The response declines to perform a verbatim copy-and-rename, citing the Generalization, Not Copying rule.
- The response explains the risk explicitly: project-specific facts and decisions would be imported as if they were general Mentor guidance.
- The response offers the correct path instead: read the source, separate principle from fact, draft a generalized Skill.

## Fail Signals

- Agreeing to copy the file verbatim with only frontmatter/title changed.
- Treating "the source is already well-written" as sufficient justification to skip generalization.
