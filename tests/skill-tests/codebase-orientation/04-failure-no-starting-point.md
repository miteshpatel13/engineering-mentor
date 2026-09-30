---
id: codebase-orientation-04-failure-no-starting-point
category: failure-handling
skill_under_test: skills/codebase-orientation/SKILL.md
---

# Scenario: No starting point can be identified

## Input Material

> "Orient yourself in the codebase before we start." No change, feature area, or question is given, in a repository with 4,000 files.

## Pass Criteria

- Offers a brief repository map at most and asks what change or area to orient around.
- Does not produce a detailed footprint for an unspecified change.

## Fail Signals

- Producing an exhaustive whole-repository footprint.
- Inventing a change to analyze.
