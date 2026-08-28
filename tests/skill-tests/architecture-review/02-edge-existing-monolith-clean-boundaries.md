---
id: architecture-review-02-edge-existing-monolith-clean-boundaries
category: edge
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Monolith With Clean Internal Boundaries

## Input Material

> Review the architecture of a monolithic Node.js application. Internally it is organized into clearly separated modules (`billing`, `users`, `notifications`), each with a narrow, documented internal interface and no reach-through into another module's internals. The requester asks whether this should be split into microservices.

## Pass Criteria

- Does not flag the monolith itself as a structural defect merely for not being microservices.
- Evaluates actual boundaries/coupling/cohesion within the material given and finds them sound, or names a specific concrete issue if one is genuinely present in the described structure.
- If addressing the microservices question at all, frames it as a trade-off discussion, not a mandate — this Skill's Rules explicitly treat "not being microservices" as a stylistic preference, not a finding.

## Fail Signals

- Recommending a microservices split as a "finding" with a severity, absent a concrete structural defect in the material.
- Failing to evaluate the monolith's actual internal boundary quality at all.
