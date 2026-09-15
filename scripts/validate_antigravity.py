#!/usr/bin/env python3
"""
Validate Antigravity plugin and workspace configuration for engineering-mentor.

Checks:
1. Root plugin.json manifest exists, is valid JSON, and contains required metadata.
2. rules/AGENTS.md exists and contains core governance and operating model sections.
3. .agents/skills.json exists, is valid JSON, and points to the skills directory.
4. .agents/rules/AGENTS.md exists and is non-empty.
5. All skills in skills/ meet Antigravity skill requirements (SKILL.md exists,
   name matches directory, description is present).
6. Claude Code configuration (.claude-plugin/plugin.json) remains valid and intact.

Usage:
    python3 scripts/validate_antigravity.py

Exit codes:
    0 - all checks passed
    1 - validation failure
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required to run this validator (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


def check_plugin_json(errors: list[str]) -> None:
    plugin_path = REPO_ROOT / "plugin.json"
    if not plugin_path.is_file():
        errors.append("plugin.json is missing from repository root")
        return

    try:
        data = json.loads(plugin_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        errors.append(f"plugin.json is invalid JSON: {err}")
        return

    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"plugin.json missing required field: {field}")

    if data.get("name") != "engineering-mentor":
        errors.append(f"plugin.json 'name' expected 'engineering-mentor', got {data.get('name')!r}")


def check_rules_agents_md(errors: list[str]) -> None:
    rules_path = REPO_ROOT / "rules" / "AGENTS.md"
    if not rules_path.is_file():
        errors.append("rules/AGENTS.md is missing")
        return

    content = rules_path.read_text(encoding="utf-8")
    if not content.strip():
        errors.append("rules/AGENTS.md is empty")
        return

    required_snippets = [
        "Operating Model",
        "No Invention Rule",
        "Conflict Resolution",
        "Severity Taxonomy",
    ]
    for snippet in required_snippets:
        if snippet.lower() not in content.lower():
            errors.append(f"rules/AGENTS.md missing key section: '{snippet}'")


def check_agents_config(errors: list[str]) -> None:
    skills_json_path = REPO_ROOT / ".agents" / "skills.json"
    if not skills_json_path.is_file():
        errors.append(".agents/skills.json is missing")
        return

    try:
        data = json.loads(skills_json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        errors.append(f".agents/skills.json is invalid JSON: {err}")
        return

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append(".agents/skills.json 'entries' must be a non-empty array")
        return

    found_skills = False
    for entry in entries:
        p = entry.get("path")
        if p and (REPO_ROOT / p).is_dir():
            found_skills = True
            break
    if not found_skills:
        errors.append(".agents/skills.json entries do not resolve to an existing skills directory")

    rules_path = REPO_ROOT / ".agents" / "rules" / "AGENTS.md"
    if not rules_path.is_file():
        errors.append(".agents/rules/AGENTS.md is missing")


def check_skills_compatibility(errors: list[str]) -> int:
    skills_dir = REPO_ROOT / "skills"
    if not skills_dir.is_dir():
        errors.append("skills/ directory not found")
        return 0

    checked_count = 0
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        skill_name = child.name
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"Skill '{skill_name}' is missing SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8")
        match = FRONTMATTER_PATTERN.match(text)
        if not match:
            errors.append(f"Skill '{skill_name}/SKILL.md' is missing YAML frontmatter")
            continue

        try:
            fm = yaml.safe_load(match.group(1))
        except yaml.YAMLError as err:
            errors.append(f"Skill '{skill_name}/SKILL.md' frontmatter YAML error: {err}")
            continue

        if not isinstance(fm, dict):
            errors.append(f"Skill '{skill_name}/SKILL.md' frontmatter is not a mapping")
            continue

        if fm.get("name") != skill_name:
            errors.append(f"Skill '{skill_name}/SKILL.md' name '{fm.get('name')}' != dir '{skill_name}'")

        if not fm.get("description") or not str(fm.get("description")).strip():
            errors.append(f"Skill '{skill_name}/SKILL.md' missing description in frontmatter")

        checked_count += 1

    return checked_count


def check_claude_preservation(errors: list[str]) -> None:
    claude_plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if not claude_plugin_path.is_file():
        errors.append(".claude-plugin/plugin.json is missing (Claude Code compatibility broken!)")
        return

    try:
        data = json.loads(claude_plugin_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        errors.append(f".claude-plugin/plugin.json is invalid JSON: {err}")
        return

    for field in ["name", "version", "description"]:
        if field not in data or not data[field]:
            errors.append(f".claude-plugin/plugin.json missing required field: {field}")


def main() -> int:
    errors: list[str] = []

    check_plugin_json(errors)
    check_rules_agents_md(errors)
    check_agents_config(errors)
    skills_count = check_skills_compatibility(errors)
    check_claude_preservation(errors)

    if errors:
        print("FAIL: Antigravity validation failed with errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"PASS: Antigravity validation succeeded ({skills_count} skills verified, Claude Code intact)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
