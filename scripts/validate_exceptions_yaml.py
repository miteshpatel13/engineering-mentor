#!/usr/bin/env python3
"""
Validate a .mentor/exceptions.yaml file against the Engineering Mentor
Exceptions Schema (schema generation 1).

Usage:
    python3 scripts/validate_exceptions_yaml.py <path-to-exceptions.yaml> [--json]

Exit codes:
    0 - valid (warnings may still be printed)
    1 - invalid (one or more errors)
    2 - usage / file error (file not found, not parseable YAML, etc.)

This script performs the same structural checks encoded in
docs/schema/exceptions.schema.v1.json (a top-level array of exception
objects, each with additionalProperties: false -- see the schema file's
own description for why that closure is deliberate), plus semantic
checks (date format, status enum, cross-entry id uniqueness) that plain
JSON Schema expresses less precisely or not at all.

It reuses the Finding class from scripts/validate_project_yaml.py rather
than redefining an equivalent one -- there is exactly one Finding shape
used across every Mentor validator in this repository.

Reference: docs/Child Rules and Exceptions.md is the authoritative,
human-readable field-by-field specification this script implements.
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
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

STATUS_ENUM = {"requested", "approved", "rejected", "expired"}

REQUIRED_FIELDS = ("id", "rule", "reason", "scope", "owner", "status")
KNOWN_FIELDS = set(REQUIRED_FIELDS) | {"evidence", "approvedBy", "approvedAt", "createdAt", "expiresAt"}
DATE_FIELDS = ("approvedAt", "createdAt", "expiresAt")


def _error(findings, code, path, message):
    findings.append(Finding("error", code, path, message))


def _warning(findings, code, path, message):
    findings.append(Finding("warning", code, path, message))


def _is_nonempty_str(v):
    return isinstance(v, str) and len(v) > 0


def _validate_date(findings, value, path):
    if not _is_nonempty_str(value):
        _error(findings, "E_INVALID_TYPE", path, "expected a non-empty string, got {!r}".format(value))
        return
    if not DATE_PATTERN.match(value):
        _error(findings, "E_INVALID_DATE", path, "'{}' is not an ISO 8601 date (expected YYYY-MM-DD)".format(value))
        return
    # DATE_PATTERN guarantees digit grouping; still confirm it's a real calendar date.
    import datetime
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        _error(findings, "E_INVALID_DATE", path, "'{}' is not a valid calendar date".format(value))


def _validate_entry(findings, entry, index):
    path_prefix = "[{}]".format(index)

    if not isinstance(entry, dict):
        _error(findings, "E_INVALID_TYPE", path_prefix, "expected a mapping/object, got {}".format(type(entry).__name__))
        return None

    for field in REQUIRED_FIELDS:
        if field not in entry:
            _error(findings, "E_MISSING_REQUIRED_FIELD", "{}.{}".format(path_prefix, field), "{} is required".format(field))

    if "id" in entry:
        if not _is_nonempty_str(entry["id"]):
            _error(findings, "E_INVALID_TYPE", "{}.id".format(path_prefix), "expected a non-empty string, got {!r}".format(entry["id"]))
        elif not ID_PATTERN.match(entry["id"]):
            _warning(
                findings, "W_ID_NOT_KEBAB_CASE", "{}.id".format(path_prefix),
                "'{}' does not match the recommended kebab-case identifier pattern ({}) -- not an error, but recommended for consistency".format(entry["id"], ID_PATTERN.pattern),
            )

    for field in ("rule", "reason", "scope", "owner", "evidence", "approvedBy"):
        if field in entry and not _is_nonempty_str(entry[field]):
            _error(findings, "E_INVALID_TYPE", "{}.{}".format(path_prefix, field), "expected a non-empty string, got {!r}".format(entry[field]))

    if "status" in entry:
        if not _is_nonempty_str(entry["status"]):
            _error(findings, "E_INVALID_TYPE", "{}.status".format(path_prefix), "expected a non-empty string, got {!r}".format(entry["status"]))
        elif entry["status"] not in STATUS_ENUM:
            _error(findings, "E_INVALID_ENUM", "{}.status".format(path_prefix), "'{}' is not one of {}".format(entry["status"], sorted(STATUS_ENUM)))

    for field in DATE_FIELDS:
        if field in entry:
            _validate_date(findings, entry[field], "{}.{}".format(path_prefix, field))

    if entry.get("status") == "approved" and "approvedBy" not in entry and "approvedAt" not in entry:
        _warning(
            findings, "W_APPROVED_WITHOUT_APPROVAL_METADATA", "{}.status".format(path_prefix),
            "status is 'approved' but neither approvedBy nor approvedAt is recorded -- not an error, but recommended so the approval is traceable",
        )

    for field in entry.keys():
        if field not in KNOWN_FIELDS:
            _error(
                findings, "E_UNKNOWN_FIELD", "{}.{}".format(path_prefix, field),
                "'{}' is not a recognized exceptions.yaml field. Unlike project.yaml, exceptions.yaml does not accept unrecognized fields (additionalProperties: false) -- this is a deliberate security-boundary control, not an oversight: see docs/schema/exceptions.schema.v1.json and docs/Child Rules and Exceptions.md Section 11.".format(field),
            )

    return entry.get("id") if _is_nonempty_str(entry.get("id")) else None


def validate(doc, findings):
    if not isinstance(doc, list):
        if doc is None:
            # An empty file / null document is treated as zero exceptions, not a structural error.
            return
        _error(findings, "E_INVALID_STRUCTURE", "", "top-level document must be a list of exception entries, got {}".format(type(doc).__name__))
        return

    seen_ids = {}
    for i, entry in enumerate(doc):
        entry_id = _validate_entry(findings, entry, i)
        if entry_id is not None:
            if entry_id in seen_ids:
                _error(
                    findings, "E_DUPLICATE_ID", "[{}].id".format(i),
                    "id '{}' is already used by entry [{}] -- exception ids must be unique within the file".format(entry_id, seen_ids[entry_id]),
                )
            else:
                seen_ids[entry_id] = i


def validate_file(path):
    findings = []
    try:
        raw = _Path(path).read_text()
    except OSError as e:
        return None, [Finding("error", "E_FILE_ERROR", "", "could not read {}: {}".format(path, e))]
    try:
        doc = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        return None, [Finding("error", "E_MALFORMED_YAML", "", "could not parse YAML: {}".format(e))]

    validate(doc, findings)
    return doc, findings


def main():
    parser = argparse.ArgumentParser(description="Validate a .mentor/exceptions.yaml file")
    parser.add_argument("path", help="path to the exceptions.yaml file to validate")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON output")
    args = parser.parse_args()

    doc, findings = validate_file(args.path)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(json.dumps({
            "valid": len(errors) == 0,
            "entries": doc if isinstance(doc, list) else None,
            "errors": [f.to_dict() for f in errors],
            "warnings": [f.to_dict() for f in warnings],
        }, indent=2))
    else:
        if not findings:
            print("OK: {} is a valid exceptions.yaml".format(args.path))
        else:
            for f in findings:
                print(str(f))
            print()
            print("{} error(s), {} warning(s)".format(len(errors), len(warnings)))

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
