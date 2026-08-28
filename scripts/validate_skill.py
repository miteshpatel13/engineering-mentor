#!/usr/bin/env python3
"""
Validate a skills/<name>/SKILL.md file's frontmatter and required-section
structure against docs/Skill Standard.md.

Usage:
    python3 scripts/validate_skill.py <path-to-SKILL.md> [--json]
    python3 scripts/validate_skill.py --dir <path-to-skills-root> [--json]

Exit codes:
    0 - valid (warnings may still be printed)
    1 - invalid (one or more errors)
    2 - usage / file error

Scope, deliberately narrow, matching the precedent set by
scripts/validate_child_rule.py: this script checks structure only --
frontmatter fields (name, description, category, skillType) and the
presence of every required "## <Section>" heading from
docs/Skill Standard.md Section 1. It does not evaluate whether a
Skill's content is good (docs/Skill Quality Standard.md, a human/review
judgment), and it does not run a Skill's own test fixtures
(docs/Skill Testing Standard.md, scripts/run_skill_standard_tests.py
only replays fixtures against THIS script, it doesn't invoke a Skill's
own narrative fixtures -- those have no execution harness, per
tests/skill-tests/code-review/README.md).

Like scripts/validate_child_rule.py, this follows docs/Skill Standard.md's
own precedent for why there is no separate JSON Schema file here: the
frontmatter contract is small (four fields today) and lives embedded in
a Markdown file, so a prose contract plus this script is the sole
authoritative enforcement -- not a second schema file to keep in sync.

Reuses the Finding class from scripts/validate_project_yaml.py rather
than redefining an equivalent one.
"""
import sys
import re
import json
import argparse
from pathlib import Path as _Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required to run this validator (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_project_yaml import Finding  # noqa: E402 -- single canonical Finding shape, reused not redefined

NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
SECTION_HEADER_PATTERN_TEMPLATE = r"^##\s+{}\s*$"

REQUIRED_FIELDS = ("name", "description", "category", "skillType")
KNOWN_FIELDS = set(REQUIRED_FIELDS)

# docs/Skill Taxonomy.md Section 3 -- the single source of truth for this
# enum. If that document's category list changes, this constant is what
# must change to match it; there is no second copy of the list in code.
CATEGORY_ENUM = {
    "Mentor Core", "Core Engineering", "Architecture", "Backend", "Frontend",
    "API", "Database", "Security", "Testing", "Performance", "DevOps/Cloud",
    "Observability", "Distributed Systems", "Data", "Integrations", "AI/LLM",
    "Domain Patterns", "Documentation", "Requirements", "Review",
}

# docs/Skill Taxonomy.md Section 1 -- the four Skill Types.
SKILL_TYPE_ENUM = {"Mentor Core", "Review", "Authoring/Workflow", "Domain Pattern"}

# docs/Skill Standard.md Section 1 -- the canonical section order. Presence
# is checked, not order (order is a Standard recommendation, not machine-
# enforced here, to avoid false positives on an otherwise-complete Skill
# that lists two sections in a different but reasonable sequence).
REQUIRED_SECTIONS = (
    "Purpose", "Scope", "When to Use", "Required Context", "Workflow",
    "Rules", "Governance Integration", "Validation", "Edge Cases",
    "Failure Handling", "Expected Output", "Examples",
)
RECOMMENDED_SECTIONS = ("Constraints", "Related Skills")

RELATED_SKILL_REF_PATTERN = re.compile(r"skills/([a-z0-9-]+)/SKILL\.md")


def _error(findings, code, path, message):
    findings.append(Finding("error", code, path, message))


def _warning(findings, code, path, message):
    findings.append(Finding("warning", code, path, message))


def _is_nonempty_str(v):
    return isinstance(v, str) and len(v) > 0


def _extract_frontmatter(raw):
    """Returns (frontmatter_text_or_None, body_text)."""
    m = FRONTMATTER_PATTERN.match(raw)
    if not m:
        return None, raw
    return m.group(1), raw[m.end():]


def validate_frontmatter(frontmatter, findings, expected_name=None):
    """`frontmatter` is the already-parsed dict from the YAML frontmatter
    block (or None/non-dict if it failed to parse). `expected_name` is the
    name implied by the skill's directory (skills/<name>/), if validating a
    real file on disk -- pass None to skip the directory/name cross-check
    (e.g. a fixture with no real skills/<name>/ location)."""
    if not isinstance(frontmatter, dict):
        _error(findings, "E_MALFORMED_FRONTMATTER", "", "frontmatter must be a YAML mapping/object, got {}".format(type(frontmatter).__name__))
        return

    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            _error(findings, "E_MISSING_REQUIRED_FIELD", field, "{} is required".format(field))

    if "name" in frontmatter:
        if not _is_nonempty_str(frontmatter["name"]):
            _error(findings, "E_INVALID_TYPE", "name", "expected a non-empty string, got {!r}".format(frontmatter["name"]))
        else:
            if not NAME_PATTERN.match(frontmatter["name"]):
                _error(findings, "E_INVALID_VALUE", "name", "'{}' does not match the required kebab-case identifier pattern ({})".format(frontmatter["name"], NAME_PATTERN.pattern))
            if expected_name is not None and frontmatter["name"] != expected_name:
                _error(
                    findings, "E_NAME_DIRECTORY_MISMATCH", "name",
                    "frontmatter name '{}' does not match the directory 'skills/{}/' -- docs/Skill Standard.md Section 6 requires an exact match".format(frontmatter["name"], expected_name),
                )

    if "description" in frontmatter and not _is_nonempty_str(frontmatter["description"]):
        _error(findings, "E_INVALID_TYPE", "description", "expected a non-empty string, got {!r}".format(frontmatter["description"]))

    if "category" in frontmatter:
        if not _is_nonempty_str(frontmatter["category"]):
            _error(findings, "E_INVALID_TYPE", "category", "expected a non-empty string, got {!r}".format(frontmatter["category"]))
        elif frontmatter["category"] not in CATEGORY_ENUM:
            _error(findings, "E_INVALID_ENUM", "category", "'{}' is not one of {} (docs/Skill Taxonomy.md Section 3)".format(frontmatter["category"], sorted(CATEGORY_ENUM)))

    if "skillType" in frontmatter:
        if not _is_nonempty_str(frontmatter["skillType"]):
            _error(findings, "E_INVALID_TYPE", "skillType", "expected a non-empty string, got {!r}".format(frontmatter["skillType"]))
        elif frontmatter["skillType"] not in SKILL_TYPE_ENUM:
            _error(findings, "E_INVALID_ENUM", "skillType", "'{}' is not one of {} (docs/Skill Taxonomy.md Section 1)".format(frontmatter["skillType"], sorted(SKILL_TYPE_ENUM)))

    for field in frontmatter.keys():
        if field not in KNOWN_FIELDS:
            _warning(findings, "W_UNKNOWN_FRONTMATTER_FIELD", field, "'{}' is not a recognized Skill frontmatter field -- ignored, not an error".format(field))


def validate_sections(body, findings):
    for section in REQUIRED_SECTIONS:
        pattern = re.compile(SECTION_HEADER_PATTERN_TEMPLATE.format(re.escape(section)), re.MULTILINE)
        if not pattern.search(body):
            _error(findings, "E_MISSING_REQUIRED_SECTION", section, "required section '## {}' not found (docs/Skill Standard.md Section 1)".format(section))
    for section in RECOMMENDED_SECTIONS:
        pattern = re.compile(SECTION_HEADER_PATTERN_TEMPLATE.format(re.escape(section)), re.MULTILINE)
        if not pattern.search(body):
            _warning(findings, "W_MISSING_RECOMMENDED_SECTION", section, "recommended section '## {}' not found -- required only when the content genuinely calls for it (docs/Skill Standard.md Section 1)".format(section))


def validate_related_skill_refs(body, path, findings):
    """Best-effort: only checked when `path` sits at skills/<name>/SKILL.md
    inside a real repository checkout (grandparent directory named
    'skills') -- skipped for standalone fixtures with no such tree, since
    there is nothing meaningful to resolve a reference against."""
    p = _Path(path)
    if p.parent.parent.name != "skills":
        return
    repo_root = p.parent.parent.parent
    for match in RELATED_SKILL_REF_PATTERN.finditer(body):
        referenced_name = match.group(1)
        candidate = repo_root / "skills" / referenced_name / "SKILL.md"
        if not candidate.is_file():
            _warning(findings, "W_RELATED_SKILL_NOT_FOUND", referenced_name, "referenced 'skills/{}/SKILL.md' does not exist in this repository".format(referenced_name))


def validate_file(path):
    """Validate a single Skill file. Returns (frontmatter_dict_or_None, findings)."""
    findings = []
    p = _Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except OSError as e:
        return None, [Finding("error", "E_FILE_ERROR", "", "could not read {}: {}".format(path, e))]

    frontmatter_text, body = _extract_frontmatter(raw)
    if frontmatter_text is None:
        _error(findings, "E_MALFORMED_FRONTMATTER", "", "file does not open with a '---' ... '---' YAML frontmatter block")
        return None, findings

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return None, [Finding("error", "E_MALFORMED_FRONTMATTER", "", "frontmatter is not valid YAML: {}".format(e))]

    # A real skill lives at skills/<name>/SKILL.md -- the parent directory
    # name is the expected `name` value. A fixture not shaped that way
    # (e.g. tests/schema-tests/skill/<fixture>.md) has no such expectation.
    expected_name = p.parent.name if p.parent.name != "skill" and p.parent.parent.name == "skills" else None

    validate_frontmatter(frontmatter, findings, expected_name=expected_name)
    validate_sections(body, findings)
    validate_related_skill_refs(body, path, findings)
    return (frontmatter if isinstance(frontmatter, dict) else None), findings


def validate_skills_dir(dir_path):
    """Validate every skills/*/SKILL.md under `dir_path`. Returns
    {relative_path: (frontmatter, findings)}."""
    dir_path = _Path(dir_path)
    results = {}
    for skill_md in sorted(dir_path.glob("*/SKILL.md")):
        frontmatter, findings = validate_file(skill_md)
        results[str(skill_md.relative_to(dir_path.parent))] = (frontmatter, findings)
    return results


def main():
    parser = argparse.ArgumentParser(description="Validate a Skill file, or every Skill under a skills/ directory, against docs/Skill Standard.md")
    parser.add_argument("path", help="path to a SKILL.md file, or (with --dir) a skills/ directory")
    parser.add_argument("--dir", action="store_true", help="treat `path` as a skills/ directory and validate every skills/*/SKILL.md under it")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON output")
    args = parser.parse_args()

    if args.dir:
        results = validate_skills_dir(args.path)
        all_errors = []
        all_warnings = []
        for _name, (_fm, findings) in results.items():
            all_errors.extend(f for f in findings if f.level == "error")
            all_warnings.extend(f for f in findings if f.level == "warning")

        if args.json:
            print(json.dumps({
                "valid": len(all_errors) == 0,
                "files": {
                    name: {
                        "valid": len([f for f in findings if f.level == "error"]) == 0,
                        "errors": [f.to_dict() for f in findings if f.level == "error"],
                        "warnings": [f.to_dict() for f in findings if f.level == "warning"],
                    }
                    for name, (_fm, findings) in results.items()
                },
            }, indent=2))
        else:
            for name, (_fm, findings) in results.items():
                errors = [f for f in findings if f.level == "error"]
                warnings = [f for f in findings if f.level == "warning"]
                status = "VALID" if not errors else "INVALID"
                print("{}  {}".format(status, name))
                for f in errors:
                    print("  ERROR    [{}] {}: {}".format(f.code, f.path, f.message))
                for f in warnings:
                    print("  WARNING  [{}] {}: {}".format(f.code, f.path, f.message))
        return 0 if not all_errors else 1

    frontmatter, findings = validate_file(args.path)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(json.dumps({
            "valid": len(errors) == 0,
            "frontmatter": frontmatter,
            "errors": [f.to_dict() for f in errors],
            "warnings": [f.to_dict() for f in warnings],
        }, indent=2))
    else:
        print("VALID" if not errors else "INVALID")
        for f in errors:
            print("  ERROR    [{}] {}: {}".format(f.code, f.path, f.message))
        for f in warnings:
            print("  WARNING  [{}] {}: {}".format(f.code, f.path, f.message))

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
