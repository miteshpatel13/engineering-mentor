#!/usr/bin/env python3
"""
Validate a .mentor/project.yaml file against the Engineering Mentor
Project Profile Schema (schemaVersion 1).

Usage:
    python3 scripts/validate_project_yaml.py <path-to-project.yaml> [--json]

Exit codes:
    0 - valid (warnings may still be printed)
    1 - invalid (one or more errors)
    2 - usage / file error (file not found, not parseable YAML, etc.)

This script performs the same structural checks encoded in
docs/schema/project.schema.v1.json, plus semantic checks (Mentor
version range syntax and self-consistency) that plain JSON Schema
cannot express. It has no dependency beyond the Python standard
library and PyYAML (assumed available -- see docs/schema/README.md).

Reference: docs/Project Profile Schema.md is the authoritative,
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

SUPPORTED_SCHEMA_VERSIONS = {1}

ARCHITECTURE_STYLE_ENUM = {"monolith", "modular-monolith", "microservices", "serverless", "event-driven", "other"}
API_STYLE_ENUM = {"REST", "GraphQL", "gRPC", "WebSocket", "other"}

NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
COMPARATOR_PATTERN = re.compile(r"^(>=|<=|>|<|=)?(\d+\.\d+\.\d+)$")

KNOWN_TOP_LEVEL_FIELDS = {
    "schemaVersion", "name", "mentor", "stack", "architecture",
    "testing", "deployment", "infrastructure", "extensions",
}


class Finding:
    def __init__(self, level, code, path, message):
        self.level = level  # "error" | "warning"
        self.code = code
        self.path = path
        self.message = message

    def to_dict(self):
        return {"level": self.level, "code": self.code, "path": self.path, "message": self.message}

    def __str__(self):
        return "[{}] {} at {}: {}".format(self.level.upper(), self.code, self.path or "<root>", self.message)


def _error(findings, code, path, message):
    findings.append(Finding("error", code, path, message))


def _warning(findings, code, path, message):
    findings.append(Finding("warning", code, path, message))


def _is_nonempty_str(v):
    return isinstance(v, str) and len(v) > 0


def _check_string_array(findings, value, path, required_nonempty=False):
    if not isinstance(value, list):
        _error(findings, "E_INVALID_TYPE", path, "expected an array of strings, got {}".format(type(value).__name__))
        return
    if required_nonempty and len(value) == 0:
        _error(findings, "E_INVALID_VALUE", path, "must contain at least one entry")
        return
    for i, item in enumerate(value):
        if not _is_nonempty_str(item):
            _error(findings, "E_INVALID_TYPE", "{}[{}]".format(path, i), "expected a non-empty string, got {!r}".format(item))


def _parse_mentor_version_range(findings, raw, path):
    """Validate the Mentor compatibility range grammar and basic self-consistency.

    Supported grammar (a deliberate, documented subset of full semver-range
    syntax -- see docs/Project Profile Schema.md):
        <comparator>? MAJOR.MINOR.PATCH (' ' <comparator>? MAJOR.MINOR.PATCH)*
    where <comparator> is one of >=, <=, >, <, = (a bare version means exact '=').
    Caret/tilde/OR ranges are not supported in schemaVersion 1.
    """
    if not _is_nonempty_str(raw):
        _error(findings, "E_INVALID_TYPE", path, "mentor.version must be a non-empty string")
        return

    tokens = raw.strip().split()
    if not tokens:
        _error(findings, "E_INVALID_MENTOR_VERSION_RANGE_SYNTAX", path, "mentor.version must not be empty")
        return

    comparators = []
    for tok in tokens:
        m = COMPARATOR_PATTERN.match(tok)
        if not m:
            _error(
                findings,
                "E_INVALID_MENTOR_VERSION_RANGE_SYNTAX",
                path,
                "'{}' is not a valid comparator/version term (expected e.g. '>=1.0.0', '<2.0.0', or a bare '1.2.3')".format(tok),
            )
            return
        op = m.group(1) or "="
        version = tuple(int(p) for p in m.group(2).split("."))
        comparators.append((op, version))

    lower_bound = None  # most restrictive >= / >
    upper_bound = None  # most restrictive <= / <
    for op, version in comparators:
        if op in (">=", ">"):
            if lower_bound is None or version > lower_bound[1]:
                lower_bound = (op, version)
        elif op in ("<=", "<"):
            if upper_bound is None or version < upper_bound[1]:
                upper_bound = (op, version)

    if lower_bound and upper_bound:
        lo_op, lo_ver = lower_bound
        hi_op, hi_ver = upper_bound
        contradictory = lo_ver > hi_ver or (lo_ver == hi_ver and (lo_op == ">" or hi_op == "<"))
        if contradictory:
            _error(
                findings,
                "E_MENTOR_VERSION_RANGE_CONTRADICTORY",
                path,
                "lower bound {}{} is not satisfiable together with upper bound {}{}".format(
                    lo_op, ".".join(map(str, lo_ver)), hi_op, ".".join(map(str, hi_ver))
                ),
            )


def validate(doc, findings):
    if not isinstance(doc, dict):
        _error(findings, "E_INVALID_TYPE", "", "top-level document must be a mapping/object")
        return

    if "schemaVersion" not in doc:
        _error(findings, "E_MISSING_REQUIRED_FIELD", "schemaVersion", "schemaVersion is required")
    else:
        sv = doc["schemaVersion"]
        if not isinstance(sv, int) or isinstance(sv, bool):
            _error(findings, "E_INVALID_TYPE", "schemaVersion", "expected an integer, got {!r}".format(sv))
        elif sv not in SUPPORTED_SCHEMA_VERSIONS:
            _error(
                findings, "E_SCHEMA_VERSION_UNSUPPORTED", "schemaVersion",
                "schemaVersion {} is not supported by this validator (supported: {})".format(sv, sorted(SUPPORTED_SCHEMA_VERSIONS)),
            )

    if "name" not in doc:
        _error(findings, "E_MISSING_REQUIRED_FIELD", "name", "name is required")
    else:
        name = doc["name"]
        if not _is_nonempty_str(name):
            _error(findings, "E_INVALID_TYPE", "name", "expected a non-empty string, got {!r}".format(name))
        elif not NAME_PATTERN.match(name):
            _warning(
                findings, "W_NAME_NOT_KEBAB_CASE", "name",
                "'{}' does not match the recommended kebab-case identifier pattern ({}) -- not an error, but recommended for consistency".format(name, NAME_PATTERN.pattern),
            )

    if "mentor" not in doc:
        _error(findings, "E_MISSING_REQUIRED_FIELD", "mentor", "mentor is required")
    else:
        mentor = doc["mentor"]
        if not isinstance(mentor, dict):
            _error(findings, "E_INVALID_TYPE", "mentor", "expected a mapping/object, got {}".format(type(mentor).__name__))
        elif "version" not in mentor:
            _error(findings, "E_MISSING_REQUIRED_FIELD", "mentor.version", "mentor.version is required")
        else:
            _parse_mentor_version_range(findings, mentor["version"], "mentor.version")

    if "stack" not in doc:
        _error(findings, "E_MISSING_REQUIRED_FIELD", "stack", "stack is required")
    else:
        stack = doc["stack"]
        if not isinstance(stack, dict):
            _error(findings, "E_INVALID_TYPE", "stack", "expected a mapping/object, got {}".format(type(stack).__name__))
        else:
            if "language" not in stack:
                _error(findings, "E_MISSING_REQUIRED_FIELD", "stack.language", "stack.language is required")
            else:
                _check_string_array(findings, stack["language"], "stack.language", required_nonempty=True)
            for optional_list_field in ("runtime", "framework", "database", "orm", "cache"):
                if optional_list_field in stack:
                    _check_string_array(findings, stack[optional_list_field], "stack.{}".format(optional_list_field))

    if "architecture" in doc:
        arch = doc["architecture"]
        if not isinstance(arch, dict):
            _error(findings, "E_INVALID_TYPE", "architecture", "expected a mapping/object, got {}".format(type(arch).__name__))
        else:
            if "style" in arch and arch["style"] not in ARCHITECTURE_STYLE_ENUM:
                _error(findings, "E_INVALID_ENUM", "architecture.style", "'{}' is not one of {}".format(arch["style"], sorted(ARCHITECTURE_STYLE_ENUM)))
            if "api" in arch and arch["api"] not in API_STYLE_ENUM:
                _error(findings, "E_INVALID_ENUM", "architecture.api", "'{}' is not one of {}".format(arch["api"], sorted(API_STYLE_ENUM)))

    if "testing" in doc:
        testing = doc["testing"]
        if not isinstance(testing, dict):
            _error(findings, "E_INVALID_TYPE", "testing", "expected a mapping/object, got {}".format(type(testing).__name__))
        else:
            for k, v in testing.items():
                if not _is_nonempty_str(v):
                    _error(findings, "E_INVALID_TYPE", "testing.{}".format(k), "expected a non-empty string, got {!r}".format(v))

    if "deployment" in doc:
        deployment = doc["deployment"]
        if not isinstance(deployment, dict):
            _error(findings, "E_INVALID_TYPE", "deployment", "expected a mapping/object, got {}".format(type(deployment).__name__))
        else:
            if "platform" in deployment and not _is_nonempty_str(deployment["platform"]):
                _error(findings, "E_INVALID_TYPE", "deployment.platform", "expected a non-empty string, got {!r}".format(deployment["platform"]))
            if "containerized" in deployment and not isinstance(deployment["containerized"], bool):
                _error(findings, "E_INVALID_TYPE", "deployment.containerized", "expected a boolean, got {!r}".format(deployment["containerized"]))
            for k in ("orchestration", "region"):
                if k in deployment and not _is_nonempty_str(deployment[k]):
                    _error(findings, "E_INVALID_TYPE", "deployment.{}".format(k), "expected a non-empty string, got {!r}".format(deployment[k]))

    if "infrastructure" in doc:
        infra = doc["infrastructure"]
        if not isinstance(infra, dict):
            _error(findings, "E_INVALID_TYPE", "infrastructure", "expected a mapping/object, got {}".format(type(infra).__name__))
        else:
            for k, v in infra.items():
                _check_string_array(findings, v, "infrastructure.{}".format(k))

    if "extensions" in doc and not isinstance(doc["extensions"], dict):
        _error(findings, "E_INVALID_TYPE", "extensions", "expected a mapping/object, got {}".format(type(doc["extensions"]).__name__))

    for k in doc.keys():
        if k not in KNOWN_TOP_LEVEL_FIELDS:
            _warning(findings, "W_UNKNOWN_TOP_LEVEL_FIELD", k, "'{}' is not a recognized field in schemaVersion 1 -- ignored, not an error".format(k))


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

    validate(doc if doc is not None else {}, findings)
    return doc, findings


def main():
    parser = argparse.ArgumentParser(description="Validate a .mentor/project.yaml file")
    parser.add_argument("path", help="path to the project.yaml file to validate")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON output")
    args = parser.parse_args()

    doc, findings = validate_file(args.path)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(json.dumps({
            "valid": len(errors) == 0,
            "errors": [f.to_dict() for f in errors],
            "warnings": [f.to_dict() for f in warnings],
        }, indent=2))
    else:
        if not findings:
            print("OK: {} is a valid project.yaml (schemaVersion 1)".format(args.path))
        else:
            for f in findings:
                print(str(f))
            print()
            print("{} error(s), {} warning(s)".format(len(errors), len(warnings)))

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
