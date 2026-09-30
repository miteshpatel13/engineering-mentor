---
id: codebase-orientation-02-edge-no-graft-fallback
category: edge
skill_under_test: skills/codebase-orientation/SKILL.md
---

# Scenario: No Graft in the project

## Input Material

> "What would changing the `Order.total` calculation affect?" The project has no `graft/` directory and no `graft` CLI.

## Pass Criteria

- States that Graft context is unavailable and proceeds with direct inspection (definitions, references, imports, routes, schema).
- Produces the footprint with evidence and states the reduced confidence.

## Fail Signals

- Refusing to proceed without Graft.
- Running `graft init` or installing Graft.
