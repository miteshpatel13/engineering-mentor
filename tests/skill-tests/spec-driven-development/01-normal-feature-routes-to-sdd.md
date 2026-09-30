---
id: spec-driven-development-01-normal-feature-routes-to-sdd
category: normal
skill_under_test: skills/spec-driven-development/SKILL.md
---

# Scenario: Production feature routes to Spec Kit SDD with Mentor gates

## Input Material

> "Add customer-level pricing so enterprise customers get negotiated per-SKU prices at checkout." The project has `.specify/memory/constitution.md` and Spec Kit skills under `.claude/skills/speckit-*`; a `graft/` directory exists.

## Pass Criteria

- Classifies the request as a Feature with money and persisted-data signals.
- Reports tooling status: Spec Kit initialized, constitution present, Graft context available.
- Recommends specify → clarify → codebase-orientation → plan → implementation-plan-review → tasks → implement ⇄ converge → review gates, naming each step's owner (Spec Kit, Graft, Mentor).
- Includes the plan gate and database/security review gates, and names `/speckit-specify` as the next step.

## Fail Signals

- Skipping the plan gate or review gates.
- Writing the spec or plan itself instead of routing to Spec Kit.
- Inventing a Spec Kit skill name not in `docs/integrations/spec-kit.md`.
