# Governance Tests

Deterministic governance test cases for `docs/Governance Precedence Model.md`, under `precedence-model-test-matrix.md`.

Unlike `tests/schema-tests/` (fully deterministic, mechanical, and automated — real code validates real files) and like `tests/skill-tests/` (narrative behavioral specs with no execution harness), this suite is **documentation, not executable tests**. There is no rule-matching engine, exception-matching engine, or conflict-resolution engine to run these cases against — `docs/Child Rules and Exceptions.md` Section 15 and `docs/Governance Precedence Model.md` Section 16 both explicitly defer that work. Building an automated harness here now would mean building the very enforcement engine this phase was told not to build.

Each test case states: the setup (which requirements are involved and at which governance tiers), the conflict-type classification (`docs/Governance Precedence Model.md` Section 10), the reasoning, and the expected future handling (Section 11) — a specification a future enforcement phase should validate its actual behavior against, and a reference a reviewer can reason from today.

When enforcement is eventually built, this matrix is the natural seed for a real automated regression suite (mirroring `tests/schema-tests/`'s fixture + expected-result convention) — at that point, each case here should become a real, executable fixture, not before.
