#!/usr/bin/env python3
"""
Run the project.yaml schema-validation regression suite.

Reads every *.yaml fixture in tests/schema-tests/project-yaml/, validates
it with scripts/validate_project_yaml.py's validate_file(), and compares
the outcome against the matching *.expected.json sidecar:
    { "valid": bool, "error_codes": [...], "warning_codes": [...] }

Comparison is by the SET of error/warning codes produced (order-independent,
duplicates preserved via multiset comparison) -- not exact message text, so
wording tweaks to the validator don't spuriously break this suite.

Usage:
    python3 scripts/run_project_yaml_tests.py

Exit code 0 if every fixture matches its expectation, 1 otherwise.
"""
import sys
import json
from collections import Counter
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_project_yaml import validate_file  # noqa: E402

FIXTURE_DIR = _Path(__file__).resolve().parent.parent / "tests" / "schema-tests" / "project-yaml"


def run():
    fixture_files = sorted(FIXTURE_DIR.glob("*.yaml"))
    if not fixture_files:
        print("no fixtures found under {}".format(FIXTURE_DIR))
        return 1

    failures = []
    for yaml_path in fixture_files:
        expected_path = yaml_path.with_suffix("").with_suffix(".expected.json")
        if not expected_path.exists():
            failures.append((yaml_path.name, "no matching .expected.json sidecar"))
            continue

        expected = json.loads(expected_path.read_text())
        _, findings = validate_file(str(yaml_path))
        errors = [f for f in findings if f.level == "error"]
        warnings = [f for f in findings if f.level == "warning"]
        actual_valid = len(errors) == 0

        problems = []
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
            failures.append((yaml_path.name, "; ".join(problems)))
        else:
            print("PASS  {}".format(yaml_path.name))

    print()
    if failures:
        for name, reason in failures:
            print("FAIL  {} -- {}".format(name, reason))
        print()
        print("{}/{} fixtures passed".format(len(fixture_files) - len(failures), len(fixture_files)))
        return 1

    print("{}/{} fixtures passed".format(len(fixture_files), len(fixture_files)))
    return 0


if __name__ == "__main__":
    sys.exit(run())
