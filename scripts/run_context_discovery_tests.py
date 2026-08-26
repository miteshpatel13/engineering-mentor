#!/usr/bin/env python3
"""
Run the Mentor Context Discovery regression suite.

Exercises scripts/discover_project_context.py's discover() function against
the fixtures in tests/context-discovery/fixtures/ and asserts specific,
named behavioral properties -- not full-dict equality against a golden
file (see tests/context-discovery/README.md for why).

Covers the 15 named scenarios required for this phase (some scenarios
share a fixture where that's the natural way to exercise the behavior;
each is asserted independently and named in the output below):

 1. Fully configured child
 2. No .mentor directory
 3. Missing project.yaml
 4. Invalid project.yaml
 5. Valid project.yaml + missing architecture.md
 6. Valid project.yaml + rules directory
 7. Valid project.yaml + exceptions.yaml
 8. Malformed architecture.md handling
 9. Empty rules directory
10. Empty exceptions file
11. Unsupported schemaVersion
12. Invalid Mentor version range
13. Progressive repository artifact discovery
14. No repository-wide blind loading
15. Read-only behavior (cross-cutting, checked against every fixture)

Usage:
    python3 scripts/run_context_discovery_tests.py

Exit code 0 if every scenario passes, 1 otherwise.
"""
import sys
import hashlib
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from discover_project_context import discover  # noqa: E402

FIXTURE_DIR = _Path(__file__).resolve().parent.parent / "tests" / "context-discovery" / "fixtures"

results = []  # list of (scenario_no, name, passed: bool, detail: str)


def check(scenario_no, name, condition, detail_on_fail):
    results.append((scenario_no, name, bool(condition), "" if condition else detail_on_fail))


def fixture(name):
    p = FIXTURE_DIR / name
    assert p.is_dir(), "fixture directory missing: {}".format(p)
    return p


def snapshot(root):
    """Hash + list every file under `root` for read-only verification."""
    files = sorted(p for p in root.rglob("*"))
    listing = tuple(str(p.relative_to(root)) + ("/" if p.is_dir() else "") for p in files)
    hashes = {}
    for p in files:
        if p.is_file():
            hashes[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return listing, hashes


def run():
    # --- Scenario 1: fully configured child ---
    ctx = discover(fixture("fully-configured-child"))
    check(1, "fully-configured-child: mentorConfigured=True",
          ctx["mentorConfigured"] is True, ctx)
    check(1, "fully-configured-child: projectProfile declared+valid",
          ctx["projectProfile"] == {"declared": True, "valid": True}, ctx["projectProfile"])
    check(1, "fully-configured-child: identity populated",
          ctx["identity"]["name"] == "fixture-child" and ctx["identity"]["schemaVersion"] == 1,
          ctx["identity"])
    check(1, "fully-configured-child: architecture doc available",
          ctx["architecture"]["architectureDocAvailable"] is True, ctx["architecture"])
    check(1, "fully-configured-child: childRules declared with 1 file",
          ctx["childRules"]["declared"] is True and len(ctx["childRules"]["files"]) == 1,
          ctx["childRules"])
    check(1, "fully-configured-child: exceptions declared, parsed, 1 entry",
          ctx["exceptions"] == {
              "declared": True, "path": ".mentor/exceptions.yaml", "parsed": True,
              "entryCount": 1,
              "note": ctx["exceptions"]["note"],
          }, ctx["exceptions"])
    check(1, "fully-configured-child: mentorCompatibility not_determined (valid range)",
          ctx["mentorCompatibility"] == {
              "declaredRange": ">=1.0.0 <2.0.0", "rangeValid": True,
              "compatibilityStatus": "not_determined",
          }, ctx["mentorCompatibility"])
    check(1, "fully-configured-child: no filesInvalid",
          ctx["discovery"]["filesInvalid"] == [], ctx["discovery"]["filesInvalid"])

    # --- Scenario 2: no .mentor directory ---
    ctx = discover(fixture("no-mentor-directory"))
    check(2, "no-mentor-directory: mentorConfigured=False",
          ctx["mentorConfigured"] is False, ctx)
    check(2, "no-mentor-directory: .mentor/ reported missing",
          ".mentor/" in ctx["discovery"]["filesMissing"], ctx["discovery"]["filesMissing"])
    check(2, "no-mentor-directory: warns child context not configured",
          any("not configured" in w for w in ctx["discovery"]["warnings"]),
          ctx["discovery"]["warnings"])
    check(2, "no-mentor-directory: no stack/architecture invented",
          ctx["identity"]["name"] is None and ctx["stack"]["language"] is None,
          (ctx["identity"], ctx["stack"]))

    # --- Scenario 3: missing project.yaml ---
    ctx = discover(fixture("missing-project-yaml"))
    check(3, "missing-project-yaml: mentorConfigured=True (dir exists)",
          ctx["mentorConfigured"] is True, ctx)
    check(3, "missing-project-yaml: projectProfile not declared",
          ctx["projectProfile"] == {"declared": False, "valid": None}, ctx["projectProfile"])
    check(3, "missing-project-yaml: .mentor/project.yaml reported missing",
          ".mentor/project.yaml" in ctx["discovery"]["filesMissing"], ctx["discovery"]["filesMissing"])
    check(3, "missing-project-yaml: no stack information invented",
          ctx["stack"]["language"] is None, ctx["stack"])
    check(3, "missing-project-yaml: architecture.md still discovered independently",
          ctx["architecture"]["architectureDocAvailable"] is True, ctx["architecture"])

    # --- Scenario 4: invalid project.yaml (generic -- missing required fields) ---
    ctx = discover(fixture("invalid-project-yaml"))
    check(4, "invalid-project-yaml: projectProfile declared but invalid",
          ctx["projectProfile"] == {"declared": True, "valid": False}, ctx["projectProfile"])
    check(4, "invalid-project-yaml: filesInvalid carries E_MISSING_REQUIRED_FIELD",
          any(e["code"] == "E_MISSING_REQUIRED_FIELD"
              for entry in ctx["discovery"]["filesInvalid"] for e in entry["errors"]),
          ctx["discovery"]["filesInvalid"])
    check(4, "invalid-project-yaml: does not silently report valid=None/True",
          ctx["projectProfile"]["valid"] is False, ctx["projectProfile"])

    # --- Scenario 5: valid project.yaml + missing architecture.md ---
    ctx = discover(fixture("missing-architecture-md"))
    check(5, "missing-architecture-md: projectProfile valid",
          ctx["projectProfile"]["valid"] is True, ctx["projectProfile"])
    check(5, "missing-architecture-md: architectureDocAvailable=False",
          ctx["architecture"]["architectureDocAvailable"] is False, ctx["architecture"])
    check(5, "missing-architecture-md: warns architecture narrative unavailable",
          any("architecture narrative unavailable" in w for w in ctx["discovery"]["warnings"]),
          ctx["discovery"]["warnings"])

    # --- Scenario 6: valid project.yaml + rules directory ---
    ctx = discover(fixture("with-rules-dir"))
    check(6, "with-rules-dir: childRules declared with 2 files",
          ctx["childRules"]["declared"] is True and len(ctx["childRules"]["files"]) == 2,
          ctx["childRules"])
    check(6, "with-rules-dir: rules discovered only, not enforced (note present)",
          "not enforced" in ctx["childRules"]["note"], ctx["childRules"]["note"])

    # --- Scenario 7: valid project.yaml + exceptions.yaml ---
    ctx = discover(fixture("with-exceptions"))
    check(7, "with-exceptions: exceptions declared, parsed, 2 entries",
          ctx["exceptions"]["declared"] is True and ctx["exceptions"]["parsed"] is True
          and ctx["exceptions"]["entryCount"] == 2, ctx["exceptions"])
    check(7, "with-exceptions: does not change finding/severity behavior (note present)",
          "does not change finding" in ctx["exceptions"]["note"], ctx["exceptions"]["note"])

    # --- Scenario 8: malformed architecture.md (a directory, not a file) ---
    ctx = discover(fixture("malformed-architecture-md"))
    check(8, "malformed-architecture-md: architectureDocAvailable=False",
          ctx["architecture"]["architectureDocAvailable"] is False, ctx["architecture"])
    check(8, "malformed-architecture-md: reported invalid with E_NOT_A_FILE",
          any(e["code"] == "E_NOT_A_FILE"
              for entry in ctx["discovery"]["filesInvalid"] for e in entry["errors"]),
          ctx["discovery"]["filesInvalid"])

    # --- Scenario 9: empty rules directory ---
    ctx = discover(fixture("empty-rules-dir"))
    check(9, "empty-rules-dir: childRules declared with 0 files",
          ctx["childRules"]["declared"] is True and ctx["childRules"]["files"] == [],
          ctx["childRules"])
    check(9, "empty-rules-dir: warns rules directory is empty",
          any("empty" in w and "rules" in w for w in ctx["discovery"]["warnings"]),
          ctx["discovery"]["warnings"])

    # --- Scenario 10: empty exceptions file ---
    ctx = discover(fixture("empty-exceptions-file"))
    check(10, "empty-exceptions-file: declared, parsed, 0 entries",
          ctx["exceptions"]["declared"] is True and ctx["exceptions"]["parsed"] is True
          and ctx["exceptions"]["entryCount"] == 0, ctx["exceptions"])
    check(10, "empty-exceptions-file: warns no exceptions declared",
          any("declares no exceptions" in w for w in ctx["discovery"]["warnings"]),
          ctx["discovery"]["warnings"])

    # --- Scenario 11: unsupported schemaVersion ---
    ctx = discover(fixture("unsupported-schema-version"))
    check(11, "unsupported-schema-version: projectProfile invalid",
          ctx["projectProfile"]["valid"] is False, ctx["projectProfile"])
    check(11, "unsupported-schema-version: E_SCHEMA_VERSION_UNSUPPORTED reported",
          any(e["code"] == "E_SCHEMA_VERSION_UNSUPPORTED"
              for entry in ctx["discovery"]["filesInvalid"] for e in entry["errors"]),
          ctx["discovery"]["filesInvalid"])
    check(11, "unsupported-schema-version: schemaVersion still surfaced (not nulled)",
          ctx["identity"]["schemaVersion"] == 99, ctx["identity"])

    # --- Scenario 12: invalid Mentor version range (contradictory) ---
    ctx = discover(fixture("invalid-mentor-version-range"))
    check(12, "invalid-mentor-version-range: rangeValid=False",
          ctx["mentorCompatibility"]["rangeValid"] is False, ctx["mentorCompatibility"])
    check(12, "invalid-mentor-version-range: compatibilityStatus=range_invalid",
          ctx["mentorCompatibility"]["compatibilityStatus"] == "range_invalid",
          ctx["mentorCompatibility"])
    check(12, "invalid-mentor-version-range: declaredRange still surfaced",
          ctx["mentorCompatibility"]["declaredRange"] == ">=2.0.0 <1.0.0", ctx["mentorCompatibility"])

    # --- Scenario 13: progressive repository artifact discovery ---
    ctx = discover(fixture("progressive-artifacts"))
    artifacts = {a["path"]: a["exists"] for a in ctx["discovery"]["repositoryArtifactsInspected"]}
    check(13, "progressive-artifacts: package.json found",
          artifacts.get("package.json") is True, artifacts)
    check(13, "progressive-artifacts: Dockerfile found",
          artifacts.get("Dockerfile") is True, artifacts)
    check(13, "progressive-artifacts: tsconfig.json correctly reported absent",
          artifacts.get("tsconfig.json") is False, artifacts)

    # --- Scenario 14: no repository-wide blind loading ---
    import json as _json
    dumped = _json.dumps(ctx)
    check(14, "progressive-artifacts: deep sentinel file never appears in output",
          "SENTINEL" not in dumped and "secret-sentinel.txt" not in dumped, "sentinel leaked into discovery output")
    check(14, "progressive-artifacts: artifact list stays bounded (fixed candidate set)",
          len(ctx["discovery"]["repositoryArtifactsInspected"]) == 13,
          ctx["discovery"]["repositoryArtifactsInspected"])

    # --- Scenario 15: read-only behavior (cross-cutting, all fixtures) ---
    all_fixtures = sorted(p for p in FIXTURE_DIR.iterdir() if p.is_dir())
    before = {f.name: snapshot(f) for f in all_fixtures}
    for f in all_fixtures:
        discover(f)
    after = {f.name: snapshot(f) for f in all_fixtures}
    mutated = [name for name in before if before[name] != after[name]]
    check(15, "read-only: no fixture mutated across all {} fixtures".format(len(all_fixtures)),
          mutated == [], "mutated fixtures: {}".format(mutated))

    # --- report ---
    print()
    failures = [r for r in results if not r[2]]
    for scenario_no, name, passed, detail in results:
        status = "PASS" if passed else "FAIL"
        print("{}  [{:2d}] {}".format(status, scenario_no, name))
        if not passed:
            print("      -> {}".format(detail))
    print()
    print("{}/{} checks passed across scenarios 1-15".format(len(results) - len(failures), len(results)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
