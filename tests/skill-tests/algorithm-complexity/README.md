# algorithm-complexity Skill — Regression Fixtures

5 narrative fixture specifications for `skills/algorithm-complexity/SKILL.md` (`docs/Skill Taxonomy.md` Section 1). Designed across all required scenario categories defined in `docs/Skill Testing Standard.md` Section 2.

## Fixtures

| # | File | Category |
|---|---|---|
| 01 | `01-normal-nested-loop-refactoring.md` | Normal — identifying nested $O(n^2)$ array search and refactoring to $O(n)$ with hash map indexing |
| 02 | `02-edge-hidden-builtin-complexity.md` | Edge case — unmasking hidden linear costs in language built-ins (`indexOf` / `slice`) inside loops |
| 03 | `03-adversarial-premature-optimization-small-n.md` | Adversarial — resisting pressure to over-optimize small, bounded collections ($n \le 10$) |
| 04 | `04-failure-indeterminate-unbounded-loop.md` | Failure handling — declining to invent Big-O for non-deterministic, unbounded external loops |
| 05 | `05-rule-coverage-auxiliary-vs-input-space.md` | Rule coverage — strictly distinguishing Input Space, Auxiliary Space, and Call Stack frames |
