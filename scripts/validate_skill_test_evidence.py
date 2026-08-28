#!/usr/bin/env python3
"""
Check whether a Skill has the on-disk test evidence docs/Skill Testing
Standard.md Section 3 requires before that Skill can be considered to
have reached the Tested lifecycle stage (docs/Skill Taxonomy.md Section 7,
stage 3).

This exists to close a real gap: scripts/validate_skill.py checks a
Skill's own file structure (frontmatter, required sections), but nothing
in the automated suite previously checked whether narrative test evidence
actually exists on disk for a given Skill, or whether that evidence is
happy-path-only -- the two conditions docs/Skill Testing Standard.md
Section 3 names as hard blockers to advancing past Tested ("Zero fixtures
of either tier", "Happy-path-only coverage... regardless of fixture
count").

Deliberately narrow, matching the precedent set by validate_skill.py and
validate_child_rule.py: this script checks EXISTENCE and CATEGORY
DIVERSITY only -- never fixture *quality*, *correctness*, or whether a
fixture's Pass Criteria are well-formed. Judging that remains
docs/skill-tester/SKILL.md's and docs/skill-reviewer/SKILL.md's job
(narrative, LLM-judged, no execution harness -- per
tests/skill-tests/code-review/README.md's own precedent). A Skill that
passes every check here has evidence that SOME testing was done; it does
not certify that the testing was good.

Evidence location convention (docs/Skill Testing Standard.md Section 5):
narrative/regression fixtures for a specific Skill's judgment layer live
at tests/skill-tests/<skill-name>/. A Skill with no directory there is
reported as a WARNING, not an ERROR -- some Skills are legitimately
deterministic-only (their judgment-layer test evidence lives in a
dedicated directory of their own, e.g. skills/context-discovery/SKILL.md
-> tests/context-discovery/) or are explicitly exempted meta-guidance
with no behavioral fixtures in this sense at all (docs/Skill Ecosystem
Inventory.md's note on skills/mentor-development/SKILL.md). This script
cannot distinguish "legitimately exempt" from "simply not yet tested"
on its own -- it surfaces the fact and lets a human/skill-reviewer
judgment call resolve which it is, rather than guessing either way.

Once a tests/skill-tests/<skill-name>/ directory exists, the stricter
checks (README present, at least one fixture, more than one distinct
`category:` value across fixtures) are ERRORs -- at that point the Skill
has committed to the narrative-fixture convention and the two named
hard blockers apply without qualification.

Usage:
    python3 scripts/validate_skill_test_evidence.py <skill-name> [--json]
    python3 scripts/validate_skill_test_evidence.py --dir skills/ [--json]

Exit codes:
    0 - no errors (warnings may still be printed)
    1 - one or more errors
    2 - usage / file error

Reuses the Finding class from scripts/validate_project_yaml.py rather
than redefining an equivalent one.
"""
import sys
import re
import json
import argparse
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent))
from validate_project_yaml import Finding  # noqa: E402 -- single canonical Finding shape, reused not redefined

REPO_ROOT = _Path(__file__).resolve().parent.parent
FIXTURE_FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
CATEGORY_LINE_PATTERN = re.compile(r"^category:\s*(.+?)\s*$", re.MULTILINE)


def _error(findings, code, path, message):
    findings.append(Finding("error", code, path, message))


def _warning(findings, code, path, message):
    findings.append(Finding("warning", code, path, message))


def _fixture_category(fixture_path):
    """Best-effort extraction of a narrative fixture's `category:`
    frontmatter value. Returns None if it can't be read/parsed -- this
    script does not need full YAML parsing for a single scalar field."""
    try:
        raw = fixture_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = FIXTURE_FRONTMATTER_PATTERN.match(raw)
    if not m:
        return None
    cm = CATEGORY_LINE_PATTERN.search(m.group(1))
    return cm.group(1) if cm else None


def validate_skill_test_evidence(skill_name, repo_root=REPO_ROOT):
    """Check test evidence for one Skill by name. Returns (findings list)."""
    findings = []
    evidence_dir = repo_root / "tests" / "skill-tests" / skill_name

    if not evidence_dir.is_dir():
        _warning(
            findings, "W_NO_NARRATIVE_EVIDENCE_DIR", "tests/skill-tests/{}/".format(skill_name),
            "no narrative fixture directory found. If this Skill's test evidence lives elsewhere "
            "(a deterministic-only Skill with its own dedicated test directory, or a Skill explicitly "
            "exempted per docs/Skill Ecosystem Inventory.md), confirm that separately; otherwise this "
            "Skill has not reached the Tested lifecycle stage (docs/Skill Taxonomy.md Section 7, stage 3) "
            "per docs/Skill Testing Standard.md Section 3.",
        )
        return findings

    readme = evidence_dir / "README.md"
    if not readme.is_file():
        _error(
            findings, "E_NO_EVIDENCE_README", "tests/skill-tests/{}/README.md".format(skill_name),
            "test evidence directory exists but has no README.md listing its fixtures and re-run triggers "
            "(docs/Skill Testing Standard.md Section 5, tests/skill-tests/code-review/README.md's reference shape).",
        )

    fixture_files = sorted(p for p in evidence_dir.glob("*.md") if p.name != "README.md")
    if not fixture_files:
        _error(
            findings, "E_ZERO_FIXTURES", "tests/skill-tests/{}/".format(skill_name),
            "test evidence directory exists but contains zero fixtures -- docs/Skill Testing Standard.md "
            "Section 3's exact hard blocker ('Zero fixtures of either tier... treated here as a hard "
            "blocker, not a scored-but-passable deduction'). This Skill has not reached Tested.",
        )
        return findings

    categories = set()
    uncategorized = []
    for fp in fixture_files:
        cat = _fixture_category(fp)
        if cat is None:
            uncategorized.append(fp.name)
        else:
            categories.add(cat)

    for name in uncategorized:
        _warning(
            findings, "W_FIXTURE_MISSING_CATEGORY", "tests/skill-tests/{}/{}".format(skill_name, name),
            "fixture has no readable `category:` frontmatter field -- cannot be counted toward category "
            "diversity below.",
        )

    if len(categories) <= 1:
        _error(
            findings, "E_HAPPY_PATH_ONLY", "tests/skill-tests/{}/".format(skill_name),
            "all {} fixture(s) share a single category ({}) -- docs/Skill Testing Standard.md Section 3's "
            "other exact hard blocker ('Happy-path-only coverage... regardless of fixture count'). This "
            "check is existence/diversity only: it does not evaluate whether the fixtures are individually "
            "well-formed, only whether more than one required scenario category has any fixture at all.".format(
                len(fixture_files), sorted(categories) or "none readable"
            ),
        )

    return findings


def validate_skills_dir(skills_dir, repo_root=REPO_ROOT):
    """Run validate_skill_test_evidence for every skills/*/SKILL.md under
    `skills_dir`. Returns {skill_name: findings}."""
    skills_dir = _Path(skills_dir)
    results = {}
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        name = skill_md.parent.name
        results[name] = validate_skill_test_evidence(name, repo_root=repo_root)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check on-disk test evidence for a Skill (or every Skill under a skills/ directory) "
                     "against docs/Skill Testing Standard.md Section 3's hard blockers."
    )
    parser.add_argument("target", help="a Skill name (e.g. 'skill-creator'), or (with --dir) a skills/ directory")
    parser.add_argument("--dir", action="store_true", help="treat `target` as a skills/ directory and check every Skill under it")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON output")
    args = parser.parse_args()

    if args.dir:
        results = validate_skills_dir(args.target)
        all_errors = []
        if args.json:
            print(json.dumps({
                "valid": all(not any(f.level == "error" for f in findings) for findings in results.values()),
                "skills": {
                    name: {
                        "valid": not any(f.level == "error" for f in findings),
                        "errors": [f.to_dict() for f in findings if f.level == "error"],
                        "warnings": [f.to_dict() for f in findings if f.level == "warning"],
                    }
                    for name, findings in results.items()
                },
            }, indent=2))
        else:
            for name, findings in results.items():
                errors = [f for f in findings if f.level == "error"]
                warnings = [f for f in findings if f.level == "warning"]
                all_errors.extend(errors)
                if errors:
                    status = "BLOCKED"
                elif warnings:
                    status = "NO-NARRATIVE-EVIDENCE"
                else:
                    status = "OK"
                print("{}  {}".format(status, name))
                for f in errors:
                    print("  ERROR    [{}] {}: {}".format(f.code, f.path, f.message))
                for f in warnings:
                    print("  WARNING  [{}] {}: {}".format(f.code, f.path, f.message))
        return 0 if not all_errors else 1

    findings = validate_skill_test_evidence(args.target)
    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]

    if args.json:
        print(json.dumps({
            "valid": len(errors) == 0,
            "errors": [f.to_dict() for f in errors],
            "warnings": [f.to_dict() for f in warnings],
        }, indent=2))
    else:
        print("VALID" if not errors else "BLOCKED")
        for f in errors:
            print("  ERROR    [{}] {}: {}".format(f.code, f.path, f.message))
        for f in warnings:
            print("  WARNING  [{}] {}: {}".format(f.code, f.path, f.message))

    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
