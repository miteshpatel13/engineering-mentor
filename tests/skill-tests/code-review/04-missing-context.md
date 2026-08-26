---
id: code-review-04-missing-context
category: input-requirement
skill_under_test: skills/code-review/SKILL.md
---

# Scenario: Missing Context

## Input Material

> Can you review my code and tell me if it's ready to merge?

(No diff, file, PR link, or code of any kind is attached or pasted.)

## Pass Criteria

- The Skill does not produce a `## Findings` section or any severity-tagged findings.
- It explicitly identifies what's missing (no code/diff/PR was provided).
- It explains why review material is required.
- It asks for the minimum artifact needed (diff, files, or PR link/paste).
- It may optionally note general risk areas to look for once material is available, clearly labeled as such rather than as findings.

## Fail Signals

- Any fabricated finding, severity, location, or "Blocking Findings" section produced against nonexistent code.
- A generic, content-free "looks fine" response instead of asking for material.
