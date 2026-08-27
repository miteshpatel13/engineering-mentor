# Governance Evaluation Tests

Deterministic regression fixtures for `scripts/evaluate_governance.py`, run by `scripts/run_governance_evaluation_tests.py`.

Each `<name>.input.json` supplies the four composed-mode arguments to `evaluate_governance.evaluate()` directly: `{"context", "rules", "exceptions", "assertions"}` (any key may be omitted). `rules`/`exceptions` are hand-built in the same shape `validate_child_rule.py --dir --json` / `validate_exceptions_yaml.py --json` produce — these fixtures test the classification step, not discovery or validation, which already have their own suites (`run_context_discovery_tests.py`, `run_rules_and_exceptions_tests.py`).

Each `<name>.expected.json` is a **partial** match against the returned `GovernanceEvaluationResult` — only the keys present are checked (see `run_governance_evaluation_tests.py`'s module docstring for the full field reference), so a fixture states only what the phase instructions actually assert, not the entire result shape.

The 15 fixtures correspond one-to-one with this phase's 15 named deterministic scenarios:

| Fixture | Scenario |
|---|---|
| `01-compatible-rule` | Compatible Mentor + Child rule |
| `02-additive-child-mandatory` | Additive Child Mandatory (`docs/Governance Precedence Model.md` Section 7's SQL-parameterized/Prisma example) |
| `03-prohibited-child-override` | Prohibited Child override (Section 5's `/admin` INVALID example) |
| `04-child-advisory-vs-mentor-advisory` | Child Advisory legitimately overriding Mentor Advisory (Section 8 — the one documented Override case) |
| `05-child-mandatory-vs-mentor-advisory` | Child Mandatory vs. Mentor Advisory — child structurally outranks, but this is *not* the documented Override shape, so it classifies as Conflict, not Override |
| `06-applicable-exception` | An applicable, approved, non-floor exception |
| `07-expired-exception` | An expired exception (inactive, regardless of applicability) |
| `08-prohibited-security-exception` | An approved exception targeting a Mentor Mandatory requirement — still Prohibited Override (Section 9: an exception's own status does not exempt it) |
| `09-insufficient-applicability-evidence` | `applicability`/`relationship` both `unknown` |
| `10-missing-child-context` | No `.mentor/` discovered at all |
| `11-invalid-child-context` | `project.yaml` declared but failed validation |
| `12-multiple-applicable-rules` | Two rules asserted in one evaluation |
| `13-multiple-applicable-exceptions` | Two exceptions asserted in one evaluation |
| `14-conflicting-child-rules` | Two same-tier requirements genuinely disagreeing (tied rank, no invented tie-break) |
| `15-classification-independent-of-severity` | No `severity` key exists anywhere in the result, at any nesting level |

Run the suite:

```bash
python3 scripts/run_governance_evaluation_tests.py
```

Add a new fixture by dropping a `<name>.input.json` plus a `<name>.expected.json` sidecar into this directory; the runner picks up new fixtures automatically.

See `docs/Governance Evaluation.md` for the full input/output contract, and `docs/Governance Precedence Model.md` for the precedence rules this classification implements.
