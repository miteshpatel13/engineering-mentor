#!/usr/bin/env python3
"""
Run the .mentor/rules/ and .mentor/exceptions.yaml regression suite.

Three fixture sets, all under tests/schema-tests/:

  exceptions/*.yaml + *.expected.json
      -- each fixture IS a full exceptions.yaml (a top-level list),
         validated with validate_exceptions_yaml.validate_file().

  child-rules/*.md + *.expected.json
      -- each fixture is a single rule file, validated with
         validate_child_rule.validate_file().

  child-rules/dir-fixtures/<name>/ + child-rules/<name>.expected.json
      -- each fixture is a small .mentor/rules/-shaped directory,
         validated with validate_child_rule.validate_rules_dir();
         findings from every file in the directory plus any
         directory-level findings (e.g. duplicate ids) are pooled
         together before comparing against the expected codes.

Comparison is by the SET (multiset) of error/warning codes produced,
exactly like scripts/run_project_yaml_tests.py -- not exact message
text, so wording tweaks don't spuriously break this suite.

Usage:
    python3 scripts/run_rules_and_exceptions_tests.py

Exit code 0 if every fixture matches its expectation, 1 otherwise.
"""
import sys
import json
from collections import Counter
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_exceptions_yaml import validate_file as validate_exceptions_file  # noqa: E402
from validate_child_rule import validate_file as validate_rule_file  # noqa: E402
from validate_child_rule import validate_rules_dir  # noqa: E402

TESTS_DIR = _Path(__file__).resolve().parent.parent / "tests" / "schema-tests"
EXCEPTIONS_DIR = TESTS_DIR / "exceptions"
CHILD_RULES_DIR = TESTS_DIR / "child-rules"
DIR_FIXTURES_DIR = CHILD_RULES_DIR / "dir-fixtures"


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


def run_exceptions(failures):
    fixture_files = sorted(EXCEPTIONS_DIR.glob("*.yaml"))
    if not fixture_files:
        failures.append(("exceptions/*", "no fixtures found under {}".format(EXCEPTIONS_DIR)))
        return
    for yaml_path in fixture_files:
        expected_path = yaml_path.with_suffix("").with_suffix(".expected.json")
        if not expected_path.exists():
            failures.append((yaml_path.name, "no matching .expected.json sidecar"))
            continue
        expected = json.loads(expected_path.read_text())
        _doc, findings = validate_exceptions_file(str(yaml_path))
        errors = [f for f in findings if f.level == "error"]
        warnings = [f for f in findings if f.level == "warning"]
        _compare("exceptions/{}".format(yaml_path.name), expected, errors, warnings, failures)


def run_child_rules_single_file(failures):
    fixture_files = sorted(CHILD_RULES_DIR.glob("*.md"))
    if not fixture_files:
        failures.append(("child-rules/*.md", "no fixtures found under {}".format(CHILD_RULES_DIR)))
        return
    for md_path in fixture_files:
        expected_path = md_path.with_suffix("").with_suffix(".expected.json")
        if not expected_path.exists():
            failures.append((md_path.name, "no matching .expected.json sidecar"))
            continue
        expected = json.loads(expected_path.read_text())
        _fm, findings = validate_rule_file(str(md_path))
        errors = [f for f in findings if f.level == "error"]
        warnings = [f for f in findings if f.level == "warning"]
        _compare("child-rules/{}".format(md_path.name), expected, errors, warnings, failures)


def run_child_rules_dirs(failures):
    if not DIR_FIXTURES_DIR.is_dir():
        failures.append(("child-rules/dir-fixtures/*", "no directory found at {}".format(DIR_FIXTURES_DIR)))
        return
    fixture_dirs = sorted(p for p in DIR_FIXTURES_DIR.iterdir() if p.is_dir())
    if not fixture_dirs:
        failures.append(("child-rules/dir-fixtures/*", "no fixture directories found under {}".format(DIR_FIXTURES_DIR)))
        return
    for fixture_dir in fixture_dirs:
        expected_path = CHILD_RULES_DIR / "{}.expected.json".format(fixture_dir.name)
        if not expected_path.exists():
            failures.append(("dir-fixtures/{}".format(fixture_dir.name), "no matching .expected.json sidecar at {}".format(expected_path)))
            continue
        expected = json.loads(expected_path.read_text())
        per_file, dir_findings = validate_rules_dir(fixture_dir)
        errors = list(dir_findings)
        warnings = []
        for _fname, (_fm, findings) in per_file.items():
            errors.extend(f for f in findings if f.level == "error")
            warnings.extend(f for f in findings if f.level == "warning")
        _compare("child-rules/dir-fixtures/{}/".format(fixture_dir.name), expected, errors, warnings, failures)


def run():
    failures = []
    run_exceptions(failures)
    run_child_rules_single_file(failures)
    run_child_rules_dirs(failures)

    dir_fixture_count = len([p for p in DIR_FIXTURES_DIR.iterdir() if p.is_dir()]) if DIR_FIXTURES_DIR.is_dir() else 0
    total = (
        len(list(EXCEPTIONS_DIR.glob("*.yaml")))
        + len(list(CHILD_RULES_DIR.glob("*.md")))
        + dir_fixture_count
    )

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
