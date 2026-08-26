#!/usr/bin/env python3
"""
Mentor Context Discovery -- deterministic, read-only child-repository
context discovery.

Implements the discovery responsibility and ordering defined in
docs/Child Repository Integration.md Section 12, and produces a
Normalized Project Context object per docs/Context Discovery.md.

This script NEVER writes to, creates in, or deletes from the target
(child) repository. It only reads. See docs/Context Discovery.md's
"Read-Only Guarantee" section.

It reuses docs/schema/project.schema.v1.json's validation logic via
scripts/validate_project_yaml.py -- it does not redefine or duplicate
that schema.

Usage:
    python3 scripts/discover_project_context.py <child-repo-root>

Exit codes:
    0 - discovery completed (this is true even when .mentor/ is missing,
        or project.yaml is missing/invalid -- discovery reporting a gap
        is a successful discovery run, not a failure)
    2 - usage error (the given root does not exist or is not a directory)
"""
import sys
import json
import argparse
from pathlib import Path as _Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required to run context discovery (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_project_yaml import validate_file as _validate_project_yaml_file  # noqa: E402

SCHEMA_DOC_REFERENCE = "docs/schema/project.schema.v1.json"

# Discovery order per docs/Child Repository Integration.md Section 12.
MENTOR_DIR = ".mentor"
PROJECT_YAML = "project.yaml"
ARCHITECTURE_MD = "architecture.md"
RULES_DIR = "rules"
EXCEPTIONS_YAML = "exceptions.yaml"

# Fixed, bounded set of well-known root-level repository artifacts.
# Existence-only check (per Section 12: "targeted, task-relevant inspection,
# not indiscriminately loading the entire repository"). Content of these
# files is deliberately NOT parsed for stack/framework inference in this
# phase -- see docs/Context Discovery.md's "No Content Inference" note,
# which follows the Mentor No Invention Rule.
CANDIDATE_ARTIFACTS = [
    "package.json",
    "tsconfig.json",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "requirements.txt",
    "pyproject.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "Gemfile",
    "composer.json",
    ".github/workflows",
]


def _rel(root, path):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def discover(root):
    """Run context discovery against `root` (a child repository path).

    Returns a plain-dict Normalized Project Context. Never raises for
    ordinary missing/invalid context -- those are reported in the
    returned structure, not as exceptions. Only truly unexpected I/O
    errors on files that DO exist propagate (surfaced as warnings, not
    raised, per the read-only/never-fail-on-a-child's-mess design).
    """
    root = _Path(root).resolve()
    mentor_dir = root / MENTOR_DIR

    files_found = []
    files_missing = []
    files_invalid = []  # [{path, errors: [{code, path, message}]}]
    warnings = []

    context = {
        "projectRoot": str(root),
        "mentorConfigured": mentor_dir.is_dir(),
        "identity": {"name": None, "schemaVersion": None},
        "mentorCompatibility": {
            "declaredRange": None,
            "rangeValid": None,
            "compatibilityStatus": "unknown",
        },
        "stack": {
            "language": None, "runtime": None, "framework": None,
            "database": None, "orm": None, "cache": None,
        },
        "architecture": {
            "style": None, "api": None,
            "architectureDocAvailable": False,
            "architectureDocPath": None,
            "architectureDocLineCount": None,
        },
        "testing": {},
        "deployment": {},
        "infrastructure": {},
        "extensions": {},
        "projectProfile": {
            "declared": False,
            "valid": None,
        },
        "childRules": {
            "declared": False,
            "files": [],
            "note": "discovered only -- not enforced in this phase (see docs/Child Repository Integration.md Section 22)",
        },
        "exceptions": {
            "declared": False,
            "path": None,
            "parsed": None,
            "entryCount": None,
            "note": "discovered only -- does not change finding/severity behavior in this phase",
        },
        "discovery": {
            "filesFound": files_found,
            "filesMissing": files_missing,
            "filesInvalid": files_invalid,
            "repositoryArtifactsInspected": [],
            "warnings": warnings,
        },
    }

    if not mentor_dir.is_dir():
        warnings.append("no .mentor/ directory found -- child context is not configured; continuing with repository-evidence-only discovery")
        files_missing.append(f"{MENTOR_DIR}/")
    else:
        files_found.append(f"{MENTOR_DIR}/")

        # --- 1. project.yaml ---
        project_yaml_path = mentor_dir / PROJECT_YAML
        if not project_yaml_path.is_file():
            files_missing.append(_rel(root, project_yaml_path))
            warnings.append("no .mentor/project.yaml found -- project profile not declared; not inventing stack/architecture information")
        else:
            files_found.append(_rel(root, project_yaml_path))
            context["projectProfile"]["declared"] = True
            doc, findings = _validate_project_yaml_file(str(project_yaml_path))
            errors = [f for f in findings if f.level == "error"]
            profile_warnings = [f for f in findings if f.level == "warning"]
            for w in profile_warnings:
                warnings.append(f"project.yaml: {w}")

            if errors:
                context["projectProfile"]["valid"] = False
                files_invalid.append({
                    "path": _rel(root, project_yaml_path),
                    "errors": [e.to_dict() for e in errors],
                })
                warnings.append(
                    "project.yaml failed schema validation (see discovery.filesInvalid) -- "
                    "treat its declared fields as UNVERIFIED, not as a trustworthy declaration"
                )
            else:
                context["projectProfile"]["valid"] = True

            # Populate whatever is structurally present, regardless of
            # overall validity -- validity is exposed via
            # projectProfile.valid / discovery.filesInvalid so a
            # consuming Skill can decide how much to trust it. This
            # script never asserts an invalid file's fields as fact.
            if isinstance(doc, dict):
                context["identity"]["name"] = doc.get("name")
                context["identity"]["schemaVersion"] = doc.get("schemaVersion")

                mentor_block = doc.get("mentor")
                if isinstance(mentor_block, dict) and "version" in mentor_block:
                    declared_range = mentor_block["version"]
                    context["mentorCompatibility"]["declaredRange"] = declared_range
                    range_errors = {"E_INVALID_MENTOR_VERSION_RANGE_SYNTAX", "E_MENTOR_VERSION_RANGE_CONTRADICTORY"}
                    range_has_error = any(e.code in range_errors for e in errors)
                    if range_has_error:
                        context["mentorCompatibility"]["rangeValid"] = False
                        context["mentorCompatibility"]["compatibilityStatus"] = "range_invalid"
                    else:
                        context["mentorCompatibility"]["rangeValid"] = True
                        # Per Section 6: this script does NOT invent a
                        # compatibility algorithm. There is no reliable,
                        # documented mechanism for a Skill to introspect
                        # which Mentor plugin version is actually
                        # installed/active in the current session, so
                        # compatibility is always reported as not
                        # determined once the declared range itself is
                        # valid -- see docs/Context Discovery.md.
                        context["mentorCompatibility"]["compatibilityStatus"] = "not_determined"
                else:
                    context["mentorCompatibility"]["compatibilityStatus"] = "not_declared"

                stack = doc.get("stack")
                if isinstance(stack, dict):
                    for key in ("language", "runtime", "framework", "database", "orm", "cache"):
                        if key in stack:
                            context["stack"][key] = stack[key]

                arch = doc.get("architecture")
                if isinstance(arch, dict):
                    context["architecture"]["style"] = arch.get("style")
                    context["architecture"]["api"] = arch.get("api")

                if isinstance(doc.get("testing"), dict):
                    context["testing"] = doc["testing"]
                if isinstance(doc.get("deployment"), dict):
                    context["deployment"] = doc["deployment"]
                if isinstance(doc.get("infrastructure"), dict):
                    context["infrastructure"] = doc["infrastructure"]
                if isinstance(doc.get("extensions"), dict):
                    context["extensions"] = doc["extensions"]

        # --- 2. architecture.md ---
        arch_md_path = mentor_dir / ARCHITECTURE_MD
        if not arch_md_path.exists():
            files_missing.append(_rel(root, arch_md_path))
            warnings.append("no .mentor/architecture.md found -- architecture narrative unavailable")
        elif arch_md_path.is_dir():
            files_invalid.append({
                "path": _rel(root, arch_md_path),
                "errors": [{"level": "error", "code": "E_NOT_A_FILE", "path": "", "message": "architecture.md exists but is a directory, not a file"}],
            })
            warnings.append("architecture.md is a directory, not a file -- treating architecture narrative as unavailable")
        else:
            try:
                text = arch_md_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as e:
                files_invalid.append({
                    "path": _rel(root, arch_md_path),
                    "errors": [{"level": "error", "code": "E_FILE_UNREADABLE", "path": "", "message": str(e)}],
                })
                warnings.append(f"architecture.md could not be read: {e}")
            else:
                files_found.append(_rel(root, arch_md_path))
                context["architecture"]["architectureDocAvailable"] = True
                context["architecture"]["architectureDocPath"] = _rel(root, arch_md_path)
                context["architecture"]["architectureDocLineCount"] = len(text.splitlines())
                if not text.strip():
                    warnings.append("architecture.md exists but is empty")

        # --- 3. rules/ ---
        rules_dir_path = mentor_dir / RULES_DIR
        if not rules_dir_path.is_dir():
            files_missing.append(_rel(root, rules_dir_path) + "/")
            warnings.append("no .mentor/rules/ found -- no child rules declared")
        else:
            files_found.append(_rel(root, rules_dir_path) + "/")
            context["childRules"]["declared"] = True
            rule_files = sorted(p for p in rules_dir_path.iterdir() if p.is_file())
            context["childRules"]["files"] = [
                {"path": _rel(root, p), "sizeBytes": p.stat().st_size} for p in rule_files
            ]
            if not rule_files:
                warnings.append("rules/ directory exists but is empty")

        # --- 4. exceptions.yaml ---
        exceptions_path = mentor_dir / EXCEPTIONS_YAML
        if not exceptions_path.is_file():
            files_missing.append(_rel(root, exceptions_path))
            warnings.append("no .mentor/exceptions.yaml found -- no child exceptions declared")
        else:
            files_found.append(_rel(root, exceptions_path))
            context["exceptions"]["declared"] = True
            context["exceptions"]["path"] = _rel(root, exceptions_path)
            try:
                raw = exceptions_path.read_text(encoding="utf-8")
                parsed = yaml.safe_load(raw) if raw.strip() else None
            except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
                context["exceptions"]["parsed"] = False
                files_invalid.append({
                    "path": _rel(root, exceptions_path),
                    "errors": [{"level": "error", "code": "E_MALFORMED_YAML", "path": "", "message": str(e)}],
                })
                warnings.append(f"exceptions.yaml could not be parsed: {e}")
            else:
                context["exceptions"]["parsed"] = True
                if parsed is None:
                    context["exceptions"]["entryCount"] = 0
                    warnings.append("exceptions.yaml exists but declares no exceptions")
                elif isinstance(parsed, list):
                    context["exceptions"]["entryCount"] = len(parsed)
                elif isinstance(parsed, dict):
                    context["exceptions"]["entryCount"] = len(parsed)
                else:
                    context["exceptions"]["entryCount"] = None
                    warnings.append("exceptions.yaml did not parse to a list or mapping -- entry count not determinable")

    # --- 5. relevant repository artifacts (bounded, existence-only) ---
    artifacts_inspected = []
    for candidate in CANDIDATE_ARTIFACTS:
        candidate_path = root / candidate
        artifacts_inspected.append({"path": candidate, "exists": candidate_path.exists()})
    context["discovery"]["repositoryArtifactsInspected"] = artifacts_inspected

    return context


def main():
    parser = argparse.ArgumentParser(
        description="Run Mentor Context Discovery against a child repository root. "
                     "Always emits the Normalized Project Context as JSON on stdout."
    )
    parser.add_argument("root", help="path to the child repository root")
    args = parser.parse_args()

    root_path = _Path(args.root)
    if not root_path.is_dir():
        print(f"error: {args.root} is not a directory", file=sys.stderr)
        sys.exit(2)

    context = discover(root_path)
    print(json.dumps(context, indent=2, sort_keys=False))
    sys.exit(0)


if __name__ == "__main__":
    main()
