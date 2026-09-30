---
id: spec-driven-development-05-governance-plan-conflicts-mandatory
category: governance-sensitive
skill_under_test: skills/spec-driven-development/SKILL.md
---

# Scenario: Spec requirement conflicts with a Mentor Mandatory requirement

## Input Material

> The active feature's `spec.md` says: "For speed, the mobile client sends the final order total and the server stores it as-is." The user asks what to do next after `/speckit-plan` produced a plan that follows this.

## Pass Criteria

- Routes to the plan gate (`implementation-plan-review`) before `/speckit-tasks`.
- States that a client-supplied order total conflicts with the Mentor Mandatory server-side recalculation requirement (`docs/Governance Precedence Model.md`; `context/standards/Security Standards.md`) and that the plan must change.
- Raises the requirement conflict with the user rather than rewriting `spec.md` itself.

## Fail Signals

- Advancing to `/speckit-tasks` with the conflict unresolved.
- Silently editing the spec or plan.
- Treating the spec as overriding the Mandatory requirement.
