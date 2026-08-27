#!/usr/bin/env python3
"""
Run the Governance Evaluation deterministic regression suite.

Fixtures live under tests/schema-tests/governance-evaluation/ as
`<name>.input.json` / `<name>.expected.json` pairs. Each `<name>.input.json`
supplies the four composed-mode arguments to evaluate_governance.evaluate()
directly: {"context", "rules", "exceptions", "assertions"} (any may be
omitted/null -- e.g. a fixture testing "missing child context" supplies no
rules/exceptions at all). This calls evaluate() directly (composed mode,
in-process) rather than the discover_project_context.discover() ->
validate_*() -> evaluate_from_repo_root() chain, because these fixtures
exist to pin down the one deterministic function this suite is about
(classify_relationship() / evaluate_exception_relationship(), exercised
through evaluate()) -- not to re-test discovery or the two validators,
which already have their own regression suites
(run_context_discovery_tests.py, run_rules_and_exceptions_tests.py).

Each `<name>.expected.json` is a PARTIAL match against the actual
GovernanceEvaluationResult: only the keys present in the expected file are
checked, so fixtures stay small (per this phase's "small stable result
contract... do not over-engineer" instruction) instead of pinning the
entire result shape. Supported expected keys:

  mentorConfigured, childContextValid   -- exact value match
  applicableRequirements, exceptionEvaluations
      -- list of partial-match dicts, compared positionally against the
         actual list of the same name; each expected dict's keys are
         checked against the corresponding actual entry (extra actual
         keys are ignored)
  conflictCount, prohibitedOverrideCount, advisoryOverrideCount,
  insufficientEvidenceCount
      -- exact length match against conflicts/prohibitedOverrides/
         advisoryOverrides/insufficientEvidence
  warningSubstrings
      -- list of strings; each must appear as a substring of at least one
         entry in the actual warnings list
  noSeverityKeyAnywhere
      -- if true, asserts no "severity" key exists anywhere in the actual
         result, at any nesting level (Scenario 15: governance
         classification is independent of finding severity)

Usage:
    python3 scripts/run_governance_evaluation_tests.py

Exit code 0 if every fixture matches its expectation, 1 otherwise.
"""
import sys
import json
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from evaluate_governance import evaluate  # noqa: E402

FIXTURES_DIR = _Path(__file__).resolve().parent.parent / "tests" / "schema-tests" / "governance-evaluation"

COUNT_FIELDS = {
    "conflictCount": "conflicts",
    "prohibitedOverrideCount": "prohibitedOverrides",
    "advisoryOverrideCount": "advisoryOverrides",
    "insufficientEvidenceCount": "insufficientEvidence",
}


def _no_severity_key(obj):
    if isinstance(obj, dict):
        if "severity" in obj:
            return False
        return all(_no_severity_key(v) for v in obj.values())
    if isinstance(obj, list):
        return all(_no_severity_key(v) for v in obj)
    return True


def _partial_list_match(expected_list, actual_list, problems, label):
    if len(expected_list) > len(actual_list):
        problems.append("{}: expected at least {} entries, got {}".format(label, len(expected_list), len(actual_list)))
        return
    for i, expected_entry in enumerate(expected_list):
        actual_entry = actual_list[i]
        for key, expected_value in expected_entry.items():
            actual_value = actual_entry.get(key)
            if actual_value != expected_value:
                problems.append(
                    "{}[{}].{}: expected {!r}, got {!r}".format(label, i, key, expected_value, actual_value)
                )


def _check(name, expected, actual):
    problems = []

    if "mentorConfigured" in expected and actual.get("mentorConfigured") != expected["mentorConfigured"]:
        problems.append("mentorConfigured: expected {!r}, got {!r}".format(expected["mentorConfigured"], actual.get("mentorConfigured")))

    if "childContextValid" in expected and actual.get("childContextValid") != expected["childContextValid"]:
        problems.append("childContextValid: expected {!r}, got {!r}".format(expected["childContextValid"], actual.get("childContextValid")))

    if "applicableRequirements" in expected:
        _partial_list_match(expected["applicableRequirements"], actual.get("applicableRequirements", []), problems, "applicableRequirements")

    if "exceptionEvaluations" in expected:
        _partial_list_match(expected["exceptionEvaluations"], actual.get("exceptionEvaluations", []), problems, "exceptionEvaluations")

    for count_key, result_key in COUNT_FIELDS.items():
        if count_key in expected:
            actual_len = len(actual.get(result_key, []))
            if actual_len != expected[count_key]:
                problems.append("{}: expected {}, got {}".format(count_key, expected[count_key], actual_len))

    if "warningSubstrings" in expected:
        actual_warnings = actual.get("warnings", [])
        for substr in expected["warningSubstrings"]:
            if not any(substr in w for w in actual_warnings):
                problems.append("warningSubstrings: expected a warning containing {!r}, got {}".format(substr, actual_warnings))

    if expected.get("noSeverityKeyAnywhere") and not _no_severity_key(actual):
        problems.append("noSeverityKeyAnywhere: found a 'severity' key somewhere in the result")

    return problems


def main():
    if not FIXTURES_DIR.is_dir():
        print("no fixtures directory at {}".format(FIXTURES_DIR), file=sys.stderr)
        sys.exit(1)

    input_files = sorted(FIXTURES_DIR.glob("*.input.json"))
    if not input_files:
        print("no fixtures found under {}".format(FIXTURES_DIR), file=sys.stderr)
        sys.exit(1)

    total = 0
    failures = []
    for input_path in input_files:
        name = input_path.name[: -len(".input.json")]
        expected_path = FIXTURES_DIR / "{}.expected.json".format(name)
        if not expected_path.is_file():
            failures.append((name, ["missing {}.expected.json".format(name)]))
            continue

        fixture = json.loads(input_path.read_text(encoding="utf-8"))
        expected = json.loads(expected_path.read_text(encoding="utf-8"))

        actual = evaluate(
            fixture.get("context"),
            fixture.get("rules"),
            fixture.get("exceptions"),
            fixture.get("assertions"),
        )

        total += 1
        problems = _check(name, expected, actual)
        if problems:
            failures.append((name, problems))
            print("FAIL  {}".format(name))
            for p in problems:
                print("      {}".format(p))
        else:
            print("PASS  {}".format(name))

    print()
    print("{}/{} fixtures passed".format(total - len(failures), total))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
