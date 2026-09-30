#!/usr/bin/env python3
"""
Run the Claude Code plugin packaging regression suite against
scripts/validate_claude_plugin.py.

Unlike the other runners, fixtures are declared inline below and written
to a temporary directory at run time rather than committed under tests/.
Several fixtures must contain things the validator forbids in a
distributed plugin -- a fake secret, a machine-specific path, a component
inside .claude-plugin/ -- and committing them would make the repository's
own validation fail.

Comparison is by the multiset of error/warning codes, exactly like
scripts/run_skill_standard_tests.py -- not message text.

Usage:
    python3 scripts/run_claude_plugin_tests.py

Exit code 0 if every fixture matches its expectation, 1 otherwise.
"""
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_claude_plugin import validate  # noqa: E402

MANIFEST = {
    "name": "sample-plugin",
    "description": "Sample plugin",
    "version": "1.0.0",
    "author": {"name": "Sample Author"},
    "repository": "https://github.com/example/sample-plugin",
    "license": "Apache-2.0",
}
NOTE = "> Resource paths resolve against `${CLAUDE_PLUGIN_ROOT}`.\n"


def skill(name, description="Review sample code for defects.", body=""):
    return "---\nname: {}\ndescription: {}\n---\n\n# {}\n\n{}".format(name, description, name, body)


def agent(name, description="Review sample artifacts."):
    return "---\nname: {}\ndescription: {}\n---\n\nReview the artifact.\n".format(name, description)


def base(**overrides):
    files = {
        ".claude-plugin/plugin.json": json.dumps(MANIFEST),
        "skills/sample-review/SKILL.md": skill("sample-review"),
        "agents/sample-reviewer.md": agent("sample-reviewer"),
    }
    files.update(overrides)
    return files


def manifest(**changes):
    data = dict(MANIFEST)
    for key, value in changes.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value
    return json.dumps(data)


# (name, files, expected error codes, expected warning codes). A value of
# None in `files` removes that path from the base fixture.
FIXTURES = [
    ("valid-minimal", base(), [], []),
    ("valid-with-resource-note", base(**{
        "skills/sample-review/SKILL.md": skill("sample-review", body=NOTE + "Follow `context/sop/Review SOP.md`.\n"),
        "context/sop/Review SOP.md": "# Review SOP\n",
    }), [], []),
    ("valid-hooks-and-mcp", base(**{
        "hooks/hooks.json": json.dumps({"hooks": {"PostToolUse": []}}),
        ".mcp.json": json.dumps({"mcpServers": {"sample": {"command": "sample-server"}}}),
    }), [], []),
    ("missing-manifest", base(**{".claude-plugin/plugin.json": None}), ["E_MANIFEST_MISSING"], []),
    ("invalid-manifest-json", base(**{".claude-plugin/plugin.json": "{not json"}), ["E_MANIFEST_INVALID_JSON"], []),
    ("invalid-manifest-name", base(**{".claude-plugin/plugin.json": manifest(name="Sample Plugin")}), ["E_MANIFEST_NAME"], []),
    ("missing-version", base(**{".claude-plugin/plugin.json": manifest(version=None)}), ["E_MANIFEST_VERSION"], []),
    ("missing-license", base(**{".claude-plugin/plugin.json": manifest(license=None)}), [], ["W_MANIFEST_LICENSE"]),
    ("ssh-alias-repository", base(**{".claude-plugin/plugin.json": manifest(repository="git@github-alias:example/sample-plugin.git")}), ["E_MANIFEST_REPOSITORY"], []),
    ("component-path-escapes-root", base(**{".claude-plugin/plugin.json": manifest(skills="./../outside")}), ["E_COMPONENT_PATH"], []),
    ("component-path-missing", base(**{".claude-plugin/plugin.json": manifest(agents=["./agents/missing.md"])}), ["E_COMPONENT_PATH"], []),
    ("skills-inside-manifest-dir", base(**{".claude-plugin/skills/misplaced/SKILL.md": skill("misplaced")}), ["E_COMPONENT_IN_MANIFEST_DIR"], []),
    ("antigravity-version-drift", base(**{"plugin.json": manifest(version="0.9.0")}), ["E_MANIFEST_PARITY"], []),
    ("skill-dir-without-skill-md", base(**{"skills/empty-skill/README.md": "not a skill\n"}), ["E_SKILL_MD_MISSING"], []),
    ("skill-no-frontmatter", base(**{"skills/sample-review/SKILL.md": "# Sample\n\nNo frontmatter.\n"}), ["E_SKILL_FRONTMATTER"], []),
    ("skill-name-dir-mismatch", base(**{"skills/sample-review/SKILL.md": skill("other-name")}), ["E_SKILL_NAME"], []),
    ("skill-missing-description", base(**{"skills/sample-review/SKILL.md": "---\nname: sample-review\n---\n\nBody.\n"}), ["E_SKILL_DESCRIPTION"], []),
    ("skill-description-truncated", base(**{"skills/sample-review/SKILL.md": skill("sample-review", description="x" * 1600)}), [], ["W_SKILL_DESCRIPTION_TRUNCATED"]),
    ("duplicate-agent-names", base(**{"agents/copy.md": agent("sample-reviewer")}), ["E_DUPLICATE_AGENT"], []),
    ("agent-missing-description", base(**{"agents/sample-reviewer.md": "---\nname: sample-reviewer\n---\n\nBody.\n"}), ["E_AGENT_DESCRIPTION"], []),
    ("resource-note-missing", base(**{
        "skills/sample-review/SKILL.md": skill("sample-review", body="Follow `context/sop/Review SOP.md`.\n"),
        "context/sop/Review SOP.md": "# Review SOP\n",
    }), ["E_RESOURCE_NOTE_MISSING"], []),
    ("broken-reference", base(**{
        "skills/sample-review/SKILL.md": skill("sample-review", body=NOTE + "Apply `docs/Missing Standard.md`.\n"),
    }), ["E_BROKEN_REFERENCE"], []),
    ("placeholder-reference-ignored", base(**{
        "skills/sample-review/SKILL.md": skill("sample-review", body=NOTE + "Create `skills/<name>/SKILL.md`.\n"),
    }), [], []),
    ("hooks-wrong-shape", base(**{"hooks/hooks.json": json.dumps({"PostToolUse": []})}), ["E_HOOKS_INVALID"], []),
    ("mcp-invalid-json", base(**{".mcp.json": "{"}), ["E_MCP_INVALID"], []),
    ("machine-specific-path", base(**{"docs/setup.md": "Run /" + "Users/alice/projects/sample/setup.sh\n"}), ["E_MACHINE_PATH"], []),
    # Built by concatenation so this source file never contains a token-shaped string.
    ("committed-secret", base(**{"docs/config.md": "token = " + "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8" + "\n"}), ["E_SECRET"], []),
    ("committed-env-file", base(**{".env": "API_URL=https://example.com\n"}), ["E_ENV_FILE"], []),
]


def write_fixture(root, files):
    for rel, content in files.items():
        if content is None:
            continue
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def run():
    failures = []
    for name, files, expected_errors, expected_warnings in FIXTURES:
        with tempfile.TemporaryDirectory(prefix="claude-plugin-fixture-") as tmp:
            root = Path(tmp) / name
            root.mkdir()
            write_fixture(root, files)
            findings, _counts = validate(root)
        errors = Counter(f.code for f in findings if f.level == "error")
        warnings = Counter(f.code for f in findings if f.level == "warning")
        problems = []
        if errors != Counter(expected_errors):
            problems.append("expected error codes {}, got {}".format(dict(Counter(expected_errors)), dict(errors)))
        if warnings != Counter(expected_warnings):
            problems.append("expected warning codes {}, got {}".format(dict(Counter(expected_warnings)), dict(warnings)))
        if problems:
            failures.append((name, "; ".join(problems)))
        else:
            print("PASS  {}".format(name))

    print()
    total = len(FIXTURES)
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
