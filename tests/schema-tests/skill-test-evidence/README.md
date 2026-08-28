# validate_skill_test_evidence.py -- Regression Fixtures

Synthetic `repo_root`-shaped directories exercising `scripts/validate_skill_test_evidence.py`
against `docs/Skill Testing Standard.md` Section 3's two named hard blockers ("Zero fixtures
of either tier", "Happy-path-only coverage... regardless of fixture count"), plus the
existence/README/category-diversity checks that support them.

Each `dir-fixtures/<case>/` directory is a standalone `repo_root` (passed as
`repo_root=` to `validate_skill_test_evidence()`), always checked against the fixed
Skill name `sample-skill`, with its expected result recorded in the sibling
`<case>.expected.json`. Run with `python3 scripts/run_skill_test_evidence_tests.py`.

Comparison is by the SET (multiset) of error/warning codes, matching
`scripts/run_skill_standard_tests.py`'s convention -- not exact message text.
