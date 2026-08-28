#!/usr/bin/env python3
"""
Run the on-disk test-evidence regression suite for
scripts/validate_skill_test_evidence.py.

Fixture shape: tests/schema-tests/skill-test-evidence/dir-fixtures/<case>/
is a standalone repo_root-shaped directory, always checked against the
fixed Skill name "sample-skill" (i.e.
validate_skill_test_evidence("sample-skill", repo_root=<that dir>)).
Its expected result lives in the sibling
tests/schema-tests/skill-test-evidence/<case>.expected.json.

This mirrors scripts/run_skill_standard_tests.py's dir-fixtures pattern
and its SET-of-codes (not exact message text) comparison.

Usage:
    python3 scripts/run_skill_test_evidence_tests.py

Exit code 0 if every fixture matches its expectation, 1 otherwise.
"""
import sys
import json
from collections import Counter
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_skill_test_evidence import validate_skill_test_evidence  # noqa: E402

TESTS_DIR = _Path(__file__).resolve().parent.parent / "tests" / "schema-tests" / "skill-test-evidence"
DIR_FIXTURES_DIR = TESTS_DIR / "dir-fixtures"
FIXED_SKILL_NAME = "sample-skill"


def _compare(name, expected, errors, warnings, failures):
    problems = []
    actual_valid = len(errors) == 0
    if actual_valid != expected["valid"]:
        problems.append("expected valid={}, got valid={}".format(expected["valid"], actual_valid))

    expected_error_counter = Counter(expected.get("error_codes", []))
    actual_error_counter = Counter(f.code for f in errors)
    if expected_error_counter != actual_error_counter:
        problems.append("expected error codes {}, got {}".format(dict(expected_error_counter), dict(actual_error_counter)))

    expected_warning_counter = Counter(expected.get("warning_codes", []))
    actual_warning_counter = Counter(f.code for f in warnings)
    if expected_warning_counter != actual_warning_counter:
        problems.append("expected warning codes {}, got {}".format(dict(expected_warning_counter), dict(actual_warning_counter)))

    if problems:
        failures.append((name, "; ".join(problems)))
        return False
    print("PASS  {}".format(name))
    return True


def run():
    failures = []
    if not DIR_FIXTURES_DIR.is_dir():
        print("no fixtures found under {}".format(DIR_FIXTURES_DIR))
        return 1

    fixture_dirs = sorted(p for p in DIR_FIXTURES_DIR.iterdir() if p.is_dir())
    if not fixture_dirs:
        print("no fixture directories found under {}".format(DIR_FIXTURES_DIR))
        return 1

    for fixture_dir in fixture_dirs:
        expected_path = TESTS_DIR / "{}.expected.json".format(fixture_dir.name)
        if not expected_path.exists():
            failures.append((fixture_dir.name, "no matching .expected.json sidecar at {}".format(expected_path)))
            continue
        expected = json.loads(expected_path.read_text())
        findings = validate_skill_test_evidence(FIXED_SKILL_NAME, repo_root=fixture_dir)
        errors = [f for f in findings if f.level == "error"]
        warnings = [f for f in findings if f.level == "warning"]
        _compare("skill-test-evidence/{}/".format(fixture_dir.name), expected, errors, warnings, failures)

    total = len(fixture_dirs)
    print()
    if failures:
        for name, reason in failures:
            print("FAIL  {} -- {}".format(name, reason))
        print()
        print("{}/{} fixtures passed".format(total - len(failures), total))
        return 1

    print("{}/{} fixtures passed".format(total, total))
    return 0


if __name__ == "__main__":
    sys.exit(run())
