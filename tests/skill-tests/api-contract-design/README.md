# api-contract-design Skill — Regression Fixtures

Five permanent behavioral test scenarios for `skills/api-contract-design/SKILL.md`, covering the normal/edge/adversarial/failure/governance-sensitive categories required for a retrofitted Skill per `docs/Skill Testing Standard.md` Section 3. This is the ecosystem's first Authoring/Workflow-type Skill — fixtures are framed around design-decision quality (Pass Criteria evaluate the produced design artifact and stated trade-offs), not Findings/Severity output, matching this Skill's own Expected Output shape.

## What this is, and isn't

Fixture specifications, not automated assertions — same convention as `tests/skill-tests/code-review/README.md`. Each fixture is run by loading `skills/api-contract-design/SKILL.md` as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

Re-run all fixtures whenever `skills/api-contract-design/SKILL.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-design-from-clear-requirement.md` | Happy path — designing a contract from a clear, concrete requirement |
| 2 | `02-edge-fits-existing-endpoint-extension.md` | Edge case — a requirement that should extend an existing endpoint, not create a new one |
| 3 | `03-adversarial-pressure-to-add-speculative-endpoints.md` | Adversarial — pressure to add endpoints "while we're at it" with no current requirement |
| 4 | `04-failure-underspecified-requirement.md` | Failure handling — a requirement too vague to model concrete operations from |
| 5 | `05-governance-child-preference-conflicts-mandatory-error-shape.md` | Governance-sensitive — a child preference conflicts with a Mentor Mandatory design requirement |
