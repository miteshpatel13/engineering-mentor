#!/usr/bin/env python3
"""
Run the Skill Standard structural regression suite.

Two fixture sets, both under tests/schema-tests/skill/:

  *.md + *.expected.json
      -- each fixture is a single, standalone SKILL.md-shaped file,
         validated with validate_skill.validate_file(). Not located
         under a real skills/<name>/ directory, so the directory/name
         cross-check and the Related Skills existence check are not
         exercised by these -- see the dir-fixtures set for that.

  dir-fixtures/<name>/skills/ + skill/<name>.expected.json
      -- each fixture is a small skills/-shaped directory (one or more
         <skill-name>/SKILL.md files), validated with
         validate_skill.validate_skills_dir(); findings from every file
         are pooled together before comparing against the expected
         codes. This is what exercises E_NAME_DIRECTORY_MISMATCH and
         W_RELATED_SKILL_NOT_FOUND, both of which only apply when a
         Skill file sits under a real-looking skills/<name>/ tree.

Comparison is by the SET (multiset) of error/warning codes produced,
exactly like scripts/run_rules_and_exceptions_tests.py -- not exact
message text, so wording tweaks don't spuriously break this suite.

Usage:
    python3 scripts/run_skill_standard_tests.py

Exit code 0 if every fixture matches its expectation, 1 otherwise.
"""
import sys
import json
from collections import Counter
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_skill import validate_file as validate_skill_file  # noqa: E402
from validate_skill import validate_skills_dir  # noqa: E402

TESTS_DIR = _Path(__file__).resolve().parent.parent / "tests" / "schema-tests" / "skill"
DIR_FIXTURES_DIR = TESTS_DIR / "dir-fixtures"


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


def run_single_file(failures):
    fixture_files = sorted(TESTS_DIR.glob("*.md"))
    if not fixture_files:
        failures.append(("skill/*.md", "no fixtures found under {}".format(TESTS_DIR)))
        return
    for md_path in fixture_files:
        expected_path = md_path.with_suffix("").with_suffix(".expected.json")
        if not expected_path.exists():
            failures.append((md_path.name, "no matching .expected.json sidecar"))
            continue
        expected = json.loads(expected_path.read_text())
        _fm, findings = validate_skill_file(str(md_path))
        errors = [f for f in findings if f.level == "error"]
        warnings = [f for f in findings if f.level == "warning"]
        _compare("skill/{}".format(md_path.name), expected, errors, warnings, failures)


def run_dirs(failures):
    if not DIR_FIXTURES_DIR.is_dir():
        failures.append(("skill/dir-fixtures/*", "no directory found at {}".format(DIR_FIXTURES_DIR)))
        return
    fixture_dirs = sorted(p for p in DIR_FIXTURES_DIR.iterdir() if p.is_dir())
    if not fixture_dirs:
        failures.append(("skill/dir-fixtures/*", "no fixture directories found under {}".format(DIR_FIXTURES_DIR)))
        return
    for fixture_dir in fixture_dirs:
        skills_root = fixture_dir / "skills"
        expected_path = TESTS_DIR / "{}.expected.json".format(fixture_dir.name)
        if not expected_path.exists():
            failures.append(("dir-fixtures/{}".format(fixture_dir.name), "no matching .expected.json sidecar at {}".format(expected_path)))
            continue
        expected = json.loads(expected_path.read_text())
        results = validate_skills_dir(skills_root)
        errors = []
        warnings = []
        for _name, (_fm, findings) in results.items():
            errors.extend(f for f in findings if f.level == "error")
            warnings.extend(f for f in findings if f.level == "warning")
        _compare("skill/dir-fixtures/{}/".format(fixture_dir.name), expected, errors, warnings, failures)


def run():
    failures = []
    run_single_file(failures)
    run_dirs(failures)

    dir_fixture_count = len([p for p in DIR_FIXTURES_DIR.iterdir() if p.is_dir()]) if DIR_FIXTURES_DIR.is_dir() else 0
    total = len(list(TESTS_DIR.glob("*.md"))) + dir_fixture_count

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
