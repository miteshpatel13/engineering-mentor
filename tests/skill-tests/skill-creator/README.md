# skill-creator Skill — Regression Fixtures

Five permanent behavioral test scenarios for `skills/skill-creator/SKILL.md`, covering the normal/edge/adversarial/failure/governance-sensitive categories required for a Batch 0 foundation Skill.

## What this is, and isn't

These are **fixture specifications**, not automated assertions, following the exact convention `tests/skill-tests/code-review/README.md` established: no execution harness runs a Skill and checks its output programmatically. Each fixture is run by loading `skills/skill-creator/SKILL.md` (and the files it cites: `docs/Skill Standard.md`, `docs/Skill Taxonomy.md`, `skills/mentor-development/SKILL.md`) as the acting agent's instructions, feeding the fixture's Input Material verbatim, and checking the output against Pass Criteria while watching for Fail Signals.

Re-run all fixtures whenever `skills/skill-creator/SKILL.md`, `docs/Skill Standard.md`, or `docs/Skill Taxonomy.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 1 | `01-normal-domain-pattern-draft.md` | Happy path — full classification-and-draft workflow |
| 2 | `02-edge-partial-generalization.md` | Edge case — source material mixing principle and project fact |
| 3 | `03-adversarial-copy-and-rename.md` | Adversarial — explicit request to copy-and-rename a project skill |
| 4 | `04-failure-inconclusive-overlap.md` | Failure handling — genuinely ambiguous overlap classification |
| 5 | `05-governance-unsupported-mandatory-claim.md` | Governance-sensitive — unsupported Mentor Mandatory tier claim |

## Governance-sensitive scope note

`skills/skill-creator/SKILL.md`'s own Governance Integration section states this Skill does not itself evaluate a child repository or produce governance-classified findings — it does not need the full `code-review`-style governance-relationship fixture set (Compatible/Additive/Prohibited Override/etc.) that a Review-type Skill requires. Fixture 5 instead exercises the governance-tier-classification judgment this Skill *does* make at authoring time (`docs/Skill Standard.md` Section 4, applied during drafting) — the correct scope of "governance-sensitive" for a Mentor Core authoring Skill.
