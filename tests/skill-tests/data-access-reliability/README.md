# data-access-reliability Skill — Regression Fixtures

7 narrative fixture specifications for `skills/data-access-reliability/SKILL.md` (Domain Pattern). Authored with the Skill, generalized from a real child-repository performance & security remediation (sanitized: no child names, paths, identifiers, or data) per `skills/mentor-development/SKILL.md` → Evolving the Mentor from Child-Repository Learnings.

## What this is, and isn't

Fixture specifications, not automated assertions — the same convention as every other Skill's fixture set. Each fixture is run by loading the Skill as the acting agent's instructions, feeding the Input Material verbatim, and checking output against Pass Criteria while watching for Fail Signals.

**Structurally complete, not confirmed-passing behavioral evidence.** No live model execution (Tier D) or independent human review (Tier E) has occurred; evidence stands at Tier A/B/C (`docs/Skill Testing Standard.md` Section 1).

Re-run all fixtures whenever the Skill changes; re-run fixture 05 whenever `docs/Governance Precedence Model.md` or `docs/Governance Evaluation.md` changes.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-scheduled-job-pool-self-deadlock.md` | Normal — hold-and-wait pool self-deadlock from an unbounded in-process job |
| 02 | `02-edge-single-orm-lookup-no-guidance.md` | Edge case — nothing held; correctly declines to add ceremony |
| 03 | `03-adversarial-retry-non-atomic-post.md` | Adversarial — pressure to retry a non-atomic multi-step post |
| 04 | `04-failure-release-helper-not-visible.md` | Failure handling — lifecycle depends on helpers not in the material |
| 05 | `05-governance-child-waives-release-in-finally.md` | Governance-sensitive — Prohibited Override of the Mandatory lifecycle floor |
| 06 | `06-rule-coverage-pool-budget-unknown-instance-count.md` | Rule coverage — Pool Budget and Fail-Fast with unknown inputs |
| 07 | `07-rule-coverage-wrong-handle-write-and-early-return.md` | Rule coverage — Transaction Boundaries |

## Rule Coverage

Connection Lifecycle (05), Transaction Boundaries (05, 07), Hold-and-Wait (01), Bounded Concurrency (01), Pool Budget and Fail-Fast (06), Lock Contention and Derived Data (03), Deadlock Retry Requires Atomicity (03), Once-Per-Period Execution (01), Enforcement (05), Observability (03). Failure Handling (04); declining edge (02). Known limitation: migration-lock-on-one-connection under Once-Per-Period Execution has no dedicated fixture.
