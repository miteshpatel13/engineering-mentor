#!/usr/bin/env python3
"""
Validate a .mentor/rules/<id>.md child rule file's frontmatter against the
Engineering Mentor Child Rule frontmatter contract.

Usage:
    python3 scripts/validate_child_rule.py <path-to-rule.md> [--json]
    python3 scripts/validate_child_rule.py --dir <path-to-rules-dir> [--json]

Exit codes:
    0 - valid (warnings may still be printed)
    1 - invalid (one or more errors)
    2 - usage / file error

Unlike .mentor/project.yaml and .mentor/exceptions.yaml, a child rule's
frontmatter contract is intentionally small (four required fields, three
optional) and is documented in prose in
docs/Child Rules and Exceptions.md rather than as a separate JSON Schema
file -- a JSON Schema doesn't apply cleanly to a frontmatter block
embedded inside a Markdown file (you would have to extract the block
before a schema could see it either way), and a second schema file for
a six-field contract would be exactly the "second large YAML schema"
this phase was told to avoid. This script IS the authoritative
enforcement of that contract; nothing else re-validates it.

This script only validates frontmatter structure and required metadata.
It does not interpret the Markdown body, and it does not evaluate,
match, or enforce the rule against any code -- that is out of scope for
this phase (see docs/Child Rules and Exceptions.md Section 15).

It reuses the Finding class from scripts/validate_project_yaml.py rather
than redefining an equivalent one.
"""
import sys
import json
import re
import argparse
from pathlib import Path as _Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required to run this validator (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_project_yaml import Finding  # noqa: E402 -- single canonical Finding shape, reused not redefined

ID_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)

CLASSIFICATION_ENUM = {"mandatory", "configurable", "advisory", "informational"}
STATUS_ENUM = {"draft", "active", "deprecated"}

REQUIRED_FIELDS = ("id", "title", "classification", "scope")
KNOWN_FIELDS = set(REQUIRED_FIELDS) | {"category", "owner", "status"}


def _error(findings, code, path, message):
    findings.append(Finding("error", code, path, message))


def _warning(findings, code, path, message):
    findings.append(Finding("warning", code, path, message))


def _is_nonempty_str(v):
    return isinstance(v, str) and len(v) > 0


def _extract_frontmatter(raw):
    """Returns (frontmatter_text_or_None, body_text). frontmatter_text is
    None if no valid '---'-delimited block opens the file."""
    m = FRONTMATTER_PATTERN.match(raw)
    if not m:
        return None, raw
    return m.group(1), raw[m.end():]


def validate_frontmatter(frontmatter, findings, expected_id=None):
    """`frontmatter` is the already-parsed dict from the YAML frontmatter
    block (or None if it failed to parse / wasn't a mapping). `expected_id`
    is the id implied by the filename (stem), if validating a real file on
    disk -- pass None to skip the filename/id cross-check (e.g. validating
    an in-memory fixture with no filename)."""
    if not isinstance(frontmatter, dict):
        _error(findings, "E_MALFORMED_FRONTMATTER", "", "frontmatter must be a YAML mapping/object, got {}".format(type(frontmatter).__name__))
        return

    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            _error(findings, "E_MISSING_REQUIRED_FIELD", field, "{} is required".format(field))

    if "id" in frontmatter:
        if not _is_nonempty_str(frontmatter["id"]):
            _error(findings, "E_INVALID_TYPE", "id", "expected a non-empty string, got {!r}".format(frontmatter["id"]))
        else:
            if not ID_PATTERN.match(frontmatter["id"]):
                _error(findings, "E_INVALID_VALUE", "id", "'{}' does not match the required kebab-case identifier pattern ({})".format(frontmatter["id"], ID_PATTERN.pattern))
            if expected_id is not None and frontmatter["id"] != expected_id:
                _error(
                    findings, "E_RULE_ID_FILENAME_MISMATCH", "id",
                    "frontmatter id '{}' does not match the filename '{}.md' -- a rule's id must equal its filename stem".format(frontmatter["id"], expected_id),
                )

    for field in ("title", "scope", "category", "owner"):
        if field in frontmatter and not _is_nonempty_str(frontmatter[field]):
            _error(findings, "E_INVALID_TYPE", field, "expected a non-empty string, got {!r}".format(frontmatter[field]))

    if "classification" in frontmatter:
        if not _is_nonempty_str(frontmatter["classification"]):
            _error(findings, "E_INVALID_TYPE", "classification", "expected a non-empty string, got {!r}".format(frontmatter["classification"]))
        elif frontmatter["classification"] not in CLASSIFICATION_ENUM:
            _error(findings, "E_INVALID_ENUM", "classification", "'{}' is not one of {}".format(frontmatter["classification"], sorted(CLASSIFICATION_ENUM)))

    if "status" in frontmatter:
        if not _is_nonempty_str(frontmatter["status"]):
            _error(findings, "E_INVALID_TYPE", "status", "expected a non-empty string, got {!r}".format(frontmatter["status"]))
        elif frontmatter["status"] not in STATUS_ENUM:
            _error(findings, "E_INVALID_ENUM", "status", "'{}' is not one of {} (omit this field to mean 'active')".format(frontmatter["status"], sorted(STATUS_ENUM)))

    for field in frontmatter.keys():
        if field not in KNOWN_FIELDS:
            _warning(findings, "W_UNKNOWN_FRONTMATTER_FIELD", field, "'{}' is not a recognized child-rule frontmatter field -- ignored, not an error".format(field))


def validate_file(path):
    """Validate a single rule file. Returns (frontmatter_dict_or_None, findings)."""
    findings = []
    p = _Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError as e:
        return None, [Finding("error", "E_FILE_ERROR", "", "could not read {}: {}".format(path, e))]

    frontmatter_text, _body = _extract_frontmatter(raw)
    if frontmatter_text is None:
        _error(findings, "E_MALFORMED_FRONTMATTER", "", "file does not open with a '---' ... '---' YAML frontmatter block")
        return None, findings

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return None, [Finding("error", "E_MALFORMED_FRONTMATTER", "", "frontmatter is not valid YAML: {}".format(e))]

    expected_id = p.stem
    validate_frontmatter(frontmatter, findings, expected_id=expected_id)
    return (frontmatter if isinstance(frontmatter, dict) else None), findings


def validate_rules_dir(dir_path):
    """Validate every *.md file directly inside `dir_path` (a .mentor/rules/
    directory), plus cross-file duplicate-id detection. Returns
    (per_file_results: {filename: (frontmatter, findings)}, dir_findings: [Finding])."""
    dir_path = _Path(dir_path)
    per_file = {}
    dir_findings = []
    seen_ids = {}

    for md_path in sorted(dir_path.glob("*.md")):
        frontmatter, findings = validate_file(md_path)
        per_file[md_path.name] = (frontmatter, findings)
        if frontmatter and _is_nonempty_str(frontmatter.get("id")):
            rule_id = frontmatter["id"]
            if rule_id in seen_ids:
                dir_findings.append(Finding(
                    "error", "E_DUPLICATE_RULE_ID", rule_id,
                    "id '{}' is used by both {} and {} -- rule ids must be unique within .mentor/rules/".format(rule_id, seen_ids[rule_id], md_path.name),
                ))
            else:
                seen_ids[rule_id] = md_path.name

    return per_file, dir_findings


def main():
    parser = argparse.ArgumentParser(description="Validate a .mentor/rules/ child rule file, or an entire rules directory")
    parser.add_argument("path", help="path to a rule .md file, or (with --dir) a rules directory")
    parser.add_argument("--dir", action="store_true", help="treat `path` as a .mentor/rules/ directory and validate every rule file plus cross-file duplicate ids")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON output")
    args = parser.parse_args()

    if args.dir:
        per_file, dir_findings = validate_rules_dir(args.path)
        all_errors = list(dir_findings)
        all_warnings = []
        for _fname, (_fm, findings) in per_file.items():
            all_errors.extend(f for f in findings if f.level == "error")
            all_warnings.extend(f for f in findings if f.level == "warning")

        if args.json:
            print(json.dumps({
                "valid": len(all_errors) == 0,
                "files": {
                    fname: {
                        "valid": len([f for f in findings if f.level == "error"]) == 0,
                        "frontmatter": fm if isinstance(fm, dict) else None,
                        "errors": [f.to_dict() for f in findings if f.level == "error"],
                        "warnings": [f.to_dict() for f in findings if f.level == "warning"],
                    }
                    for fname, (fm, findings) in per_file.items()
                },
                "directoryErrors": [f.to_dict() for f in dir_findings],
            }, indent=2))
        else:
            for fname, (_fm, findings) in per_file.items():
                for f in findings:
                    print("{}: {}".format(fname, f))
            for f in dir_findings:
                print(str(f))
            print()
            print("{} file(s), {} error(s), {} warning(s)".format(len(per_file), len(all_errors), len(all_warnings)))
        sys.exit(1 if all_errors else 0)

    _frontmatter, findings = validate_file(args.path)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(json.dumps({
            "valid": len(errors) == 0,
            "frontmatter": _frontmatter if isinstance(_frontmatter, dict) else None,
            "errors": [f.to_dict() for f in errors],
            "warnings": [f.to_dict() for f in warnings],
        }, indent=2))
    else:
        if not findings:
            print("OK: {} is a valid child rule file".format(args.path))
        else:
            for f in findings:
                print(str(f))
            print()
            print("{} error(s), {} warning(s)".format(len(errors), len(warnings)))

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
