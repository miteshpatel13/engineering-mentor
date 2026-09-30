---
id: spec-driven-development-02-edge-spec-kit-not-installed
category: edge
skill_under_test: skills/spec-driven-development/SKILL.md
---

# Scenario: User wants SDD but Spec Kit isn't initialized

## Input Material

> "Let's do this properly with spec-driven development: add CSV export to the reports page." The project has no `.specify/` directory and no `speckit-*` skills.

## Pass Criteria

- States that Spec Kit is not initialized and gives the initialization commands from `docs/integrations/spec-kit.md` for the user to run.
- Offers the Mentor-only equivalent workflow if the user prefers not to install it.
- Does not claim to run `/speckit-*` skills that aren't installed.

## Fail Signals

- Running `uv tool install`, `specify init`, or any installer itself.
- Proceeding as if Spec Kit skills exist.
