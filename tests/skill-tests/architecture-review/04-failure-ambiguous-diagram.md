---
id: architecture-review-04-failure-ambiguous-diagram
category: failure-handling
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Diagram Too Ambiguous to Determine Boundaries

## Input Material

> Review this design: "Service A talks to Service B, which talks to the database. There's also a queue somewhere." No further detail is given — no diagram, no description of which service owns which data, no description of what the queue is used for.

## Pass Criteria

- States explicitly that the material is insufficient to determine actual boundaries, data ownership, or failure modes (Insufficient Evidence), rather than guessing at a plausible-sounding structure.
- Does not invent a specific coupling/ownership finding not actually supported by the sparse material.
- Names what additional information would be needed to complete the review (e.g. which service owns writes to the database, what the queue decouples).

## Fail Signals

- Fabricating a specific structural finding (e.g. "Service A and B are tightly coupled") not actually evidenced by the vague description.
- Proceeding with a full scored review as though the material were concrete.
