#!/usr/bin/env python3
"""
Validate the Claude Code plugin packaging of engineering-mentor.

This is the Claude Code counterpart of scripts/validate_antigravity.py. It
checks only what Claude Code plugin loading depends on, plus distribution
hygiene; it deliberately does NOT re-check the Skill Standard (required
sections, category/skillType enums) -- that stays with
scripts/validate_skill.py -- and it is not a substitute for the official
`claude plugin validate` command, which remains the authoritative manifest
check (pass --with-cli to run it as part of this script).

Checks:
 1. .claude-plugin/plugin.json exists, is valid JSON, and has a valid name,
    a semantic version, description, author.name, license, and an HTTPS
    repository URL (no SSH host aliases).
 2. .claude-plugin/ holds only plugin.json -- skills/, agents/, hooks/ etc.
    must be siblings of .claude-plugin/, never inside it.
 3. Manifest component paths (skills, agents, commands, hooks, mcpServers,
    ...) start with ./, stay inside the plugin root, and exist.
 4. Antigravity parity: root plugin.json, when present, agrees with the
    Claude manifest on name, version, description, license, repository.
 5. skills/<name>/SKILL.md: exists, frontmatter parses, name matches the
    directory and Claude's naming rules, description present and within
    Claude Code's 1,536-character listing cap; no duplicate skill names.
 6. agents/*.md: frontmatter parses with name and description; no duplicate
    agent names.
 7. hooks/hooks.json and .mcp.json, when present, are valid JSON of the
    documented shape (hooks.json needs a top-level "hooks" object; .mcp.json
    needs a top-level "mcpServers" object).
 8. Skills and agents that reference Mentor files (context/, docs/,
    scripts/, ...) carry the Resource paths note that resolves them against
    ${CLAUDE_PLUGIN_ROOT}, and every concrete referenced path exists.
 9. No machine-specific absolute paths (/Users/<name>/, /home/<name>/,
    C:\\Users\\<name>\\) in distributed text files.
10. No committed secrets (cloud keys, GitHub/Anthropic/Slack tokens,
    private keys) and no tracked .env files.

Usage:
    python3 scripts/validate_claude_plugin.py [plugin-root] [--json] [--with-cli]

Exit codes:
    0 - valid (warnings may still be printed)
    1 - invalid (one or more errors)
    2 - usage error
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("error: PyYAML is required to run this validator (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_project_yaml import Finding  # noqa: E402 -- single canonical Finding shape, reused not redefined

REPO_ROOT = Path(__file__).resolve().parent.parent

FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
# Plugin, skill, and agent names: kebab-case, which also satisfies Claude
# Code's rule of no spaces, '@', ':', or path separators.
NAME_PATTERN = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SKILL_LISTING_CAP = 1536  # combined description + when_to_use, per the Claude Code skills reference
MAX_SKILL_NAME = 64

COMPONENT_PATH_KEYS = ("skills", "agents", "commands", "hooks", "mcpServers", "lspServers", "outputStyles", "workflows")
PARITY_FIELDS = ("name", "version", "description", "license", "repository")

RESOURCE_NOTE_MARKER = "${CLAUDE_PLUGIN_ROOT}"
MENTOR_PREFIXES = ("context", "docs", "scripts", "skills", "tests", "agents", "rules")
REFERENCE_PATTERN = re.compile(r"`((?:%s)/[^`\n]+?)`" % "|".join(MENTOR_PREFIXES))
# Placeholders and globs are illustrative, not concrete references.
PLACEHOLDER_PATTERN = re.compile(r"[<>*{}…]|\.\.\.|\bNN\b|XX")
# Paths a Skill names deliberately as hypothetical examples (e.g. a
# not-yet-created Skill's test directory). Keep this list short and explicit.
HYPOTHETICAL_REFERENCES = {
    "tests/skill-tests/rate-limiting/",  # skills/mentor-development/SKILL.md worked example of a proposed Skill
}

MACHINE_PATH_PATTERN = re.compile(r"(/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|[A-Za-z]:\\\\?Users\\\\?[A-Za-z0-9._-]+)")
SECRET_PATTERNS = (
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("aws-secret-access-key", re.compile(r"aws_secret_access_key\s*[=:]\s*['\"]?[A-Za-z0-9/+=]{40}")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{22,})\b")),
    ("anthropic-api-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
)
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ".txt", ".sh", ".toml", ".cfg", ".ini", ""}
SKIP_DIRS = {".git", "__pycache__", "node_modules", "results"}


def _error(findings, code, path, message):
    findings.append(Finding("error", code, path, message))


def _warning(findings, code, path, message):
    findings.append(Finding("warning", code, path, message))


def _rel(root, path):
    return str(path.relative_to(root))


def _parse_frontmatter(path):
    """Returns (dict_or_None, body, error_message_or_None)."""
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_PATTERN.match(text)
    if not m:
        return None, text, "missing YAML frontmatter (the opening --- must be the first line)"
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as err:
        return None, text[m.end():], "frontmatter YAML error: {}".format(err)
    if not isinstance(fm, dict):
        return None, text[m.end():], "frontmatter is not a mapping"
    return fm, text[m.end():], None


def _load_json(root, rel_path, findings, code):
    path = root / rel_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        _error(findings, code, rel_path, "invalid JSON: {}".format(err))
        return None


def check_manifest(root, findings):
    manifest_path = root / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        _error(findings, "E_MANIFEST_MISSING", ".claude-plugin/plugin.json", "Claude Code plugin manifest not found")
        return None
    manifest = _load_json(root, ".claude-plugin/plugin.json", findings, "E_MANIFEST_INVALID_JSON")
    if not isinstance(manifest, dict):
        return None

    rel = ".claude-plugin/plugin.json"
    name = manifest.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.match(name):
        _error(findings, "E_MANIFEST_NAME", rel, "name must be a non-empty kebab-case string, got {!r}".format(name))
    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_PATTERN.match(version):
        _error(findings, "E_MANIFEST_VERSION", rel, "version must be a semantic version (MAJOR.MINOR.PATCH), got {!r}".format(version))
    if not manifest.get("description"):
        _error(findings, "E_MANIFEST_DESCRIPTION", rel, "description is required for marketplace listing")
    author = manifest.get("author")
    if not isinstance(author, dict) or not author.get("name"):
        _error(findings, "E_MANIFEST_AUTHOR", rel, "author.name is required")
    if not manifest.get("license"):
        _warning(findings, "W_MANIFEST_LICENSE", rel, "license is not declared")
    repository = manifest.get("repository")
    if repository is not None and not (isinstance(repository, str) and repository.startswith("https://")):
        _error(findings, "E_MANIFEST_REPOSITORY", rel, "repository must be a public https:// URL, not an SSH host alias or other form: {!r}".format(repository))

    for key in COMPONENT_PATH_KEYS:
        if key not in manifest:
            continue
        value = manifest[key]
        entries = value if isinstance(value, list) else [value]
        for entry in entries:
            if not isinstance(entry, str):
                continue  # inline hook/MCP configuration objects
            if entry in (".", "./") and key == "skills":
                continue
            if entry.startswith("https://") and key == "mcpServers":
                continue
            if not entry.startswith("./"):
                _error(findings, "E_COMPONENT_PATH", rel, "{} path {!r} must start with ./".format(key, entry))
                continue
            target = (root / entry).resolve()
            if ".." in Path(entry).parts or not str(target).startswith(str(root.resolve())):
                _error(findings, "E_COMPONENT_PATH", rel, "{} path {!r} escapes the plugin root".format(key, entry))
            elif not target.exists():
                _error(findings, "E_COMPONENT_PATH", rel, "{} path {!r} does not exist".format(key, entry))
    return manifest


def check_manifest_dir_contents(root, findings):
    manifest_dir = root / ".claude-plugin"
    if not manifest_dir.is_dir():
        return
    for child in sorted(manifest_dir.iterdir()):
        if child.name in ("plugin.json", ".DS_Store"):
            continue
        _error(findings, "E_COMPONENT_IN_MANIFEST_DIR", _rel(root, child),
               "only plugin.json belongs in .claude-plugin/; components placed there do not load -- move it to the plugin root")


def check_antigravity_parity(root, manifest, findings):
    ag_path = root / "plugin.json"
    if manifest is None or not ag_path.is_file():
        return
    ag = _load_json(root, "plugin.json", findings, "E_PARITY_INVALID_JSON")
    if not isinstance(ag, dict):
        return
    for field in PARITY_FIELDS:
        if manifest.get(field) != ag.get(field):
            _error(findings, "E_MANIFEST_PARITY", "plugin.json",
                   "{!r} differs between .claude-plugin/plugin.json ({!r}) and the Antigravity plugin.json ({!r})".format(field, manifest.get(field), ag.get(field)))


def _check_resource_references(root, rel, body, findings):
    refs = REFERENCE_PATTERN.findall(body)
    if not refs:
        return
    if RESOURCE_NOTE_MARKER not in body:
        _error(findings, "E_RESOURCE_NOTE_MISSING", rel,
               "references Mentor files ({}) but has no Resource paths note resolving them against ${{CLAUDE_PLUGIN_ROOT}}; they would resolve against the user's project instead".format(refs[0]))
    seen = set()
    for ref in refs:
        ref = ref.strip().rstrip(".,;:")
        if ref in seen or ref in HYPOTHETICAL_REFERENCES or PLACEHOLDER_PATTERN.search(ref):
            continue
        seen.add(ref)
        # A trailing section qualifier such as "docs/X.md Section 3" is prose, not path.
        candidate = re.split(r"\s+(?:Section|§)", ref)[0].strip()
        if not (root / candidate).exists():
            _error(findings, "E_BROKEN_REFERENCE", rel, "referenced path `{}` does not exist in the plugin".format(candidate))


def check_skills(root, findings):
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        _warning(findings, "W_NO_SKILLS", "skills/", "no skills/ directory at the plugin root")
        return 0
    names = {}
    count = 0
    for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        rel = "skills/{}/SKILL.md".format(child.name)
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            _error(findings, "E_SKILL_MD_MISSING", rel, "skill directory has no SKILL.md, so Claude Code will not load it")
            continue
        count += 1
        fm, body, err = _parse_frontmatter(skill_md)
        if err:
            _error(findings, "E_SKILL_FRONTMATTER", rel, err)
            continue
        name = fm.get("name", child.name)
        if not isinstance(name, str) or not NAME_PATTERN.match(name) or len(name) > MAX_SKILL_NAME:
            _error(findings, "E_SKILL_NAME", rel, "name must be kebab-case and at most {} characters, got {!r}".format(MAX_SKILL_NAME, name))
        elif name != child.name:
            _error(findings, "E_SKILL_NAME", rel, "name {!r} does not match its directory {!r}".format(name, child.name))
        description = fm.get("description")
        if not isinstance(description, str) or not description.strip():
            _error(findings, "E_SKILL_DESCRIPTION", rel, "description is required -- Claude uses it to decide when to invoke the skill")
        else:
            listing = len(description) + len(str(fm.get("when_to_use", "") or ""))
            if listing > SKILL_LISTING_CAP:
                _warning(findings, "W_SKILL_DESCRIPTION_TRUNCATED", rel,
                         "description + when_to_use is {} characters; Claude Code truncates the listing at {}".format(listing, SKILL_LISTING_CAP))
        if isinstance(name, str):
            if name in names:
                _error(findings, "E_DUPLICATE_SKILL", rel, "skill name {!r} is also declared by {}".format(name, names[name]))
            names.setdefault(name, rel)
        _check_resource_references(root, rel, body, findings)
    return count


def check_agents(root, findings):
    agents_dir = root / "agents"
    if not agents_dir.is_dir():
        return 0
    names = {}
    count = 0
    for agent_md in sorted(agents_dir.rglob("*.md")):
        rel = _rel(root, agent_md)
        count += 1
        fm, body, err = _parse_frontmatter(agent_md)
        if err:
            _error(findings, "E_AGENT_FRONTMATTER", rel, err)
            continue
        name = fm.get("name")
        if not isinstance(name, str) or not NAME_PATTERN.match(name):
            _error(findings, "E_AGENT_NAME", rel, "name must be a kebab-case string, got {!r}".format(name))
        if not isinstance(fm.get("description"), str) or not fm["description"].strip():
            _error(findings, "E_AGENT_DESCRIPTION", rel, "description is required -- Claude uses it to decide when to delegate")
        if isinstance(name, str):
            if name in names:
                _error(findings, "E_DUPLICATE_AGENT", rel, "agent name {!r} is also declared by {}".format(name, names[name]))
            names.setdefault(name, rel)
        _check_resource_references(root, rel, body, findings)
    return count


def check_hooks_and_mcp(root, findings):
    if (root / "hooks" / "hooks.json").is_file():
        data = _load_json(root, "hooks/hooks.json", findings, "E_HOOKS_INVALID")
        if data is not None and not isinstance(data.get("hooks") if isinstance(data, dict) else None, dict):
            _error(findings, "E_HOOKS_INVALID", "hooks/hooks.json", "must contain a top-level \"hooks\" object")
    if (root / ".mcp.json").is_file():
        data = _load_json(root, ".mcp.json", findings, "E_MCP_INVALID")
        if data is not None and not isinstance(data.get("mcpServers") if isinstance(data, dict) else None, dict):
            _error(findings, "E_MCP_INVALID", ".mcp.json", "must contain a top-level \"mcpServers\" object")


def _distributed_files(root):
    """Files that ship with the plugin: git-tracked files when root is a git
    work tree root (so ignored local files are not flagged), else every file."""
    if (root / ".git").exists() and shutil.which("git"):
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=False)
        if out.returncode == 0:
            return [root / p for p in out.stdout.decode("utf-8").split("\0") if p]
    return [p for p in root.rglob("*") if p.is_file() and not (set(p.relative_to(root).parts) & SKIP_DIRS)]


def check_hygiene(root, findings):
    for path in _distributed_files(root):
        if not path.is_file():
            continue
        rel = _rel(root, path)
        if path.name == ".env" or (path.name.startswith(".env.") and path.name not in (".env.example", ".env.sample", ".env.template")):
            _error(findings, "E_ENV_FILE", rel, "environment files must not be distributed with the plugin")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if MACHINE_PATH_PATTERN.search(line):
                _error(findings, "E_MACHINE_PATH", "{}:{}".format(rel, lineno),
                       "machine-specific absolute path; use a relative path, $HOME, or ${CLAUDE_PLUGIN_ROOT}")
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    # Never echo the matched value itself.
                    _error(findings, "E_SECRET", "{}:{}".format(rel, lineno), "possible committed secret ({})".format(label))


def check_with_cli(root, findings):
    claude = shutil.which("claude")
    if not claude:
        _warning(findings, "W_CLI_UNAVAILABLE", "", "claude CLI not on PATH; skipped `claude plugin validate --strict`")
        return
    result = subprocess.run([claude, "plugin", "validate", str(root), "--strict"], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        _error(findings, "E_CLI_VALIDATE", "", "`claude plugin validate --strict` failed:\n{}".format((result.stdout + result.stderr).strip()))


def validate(root, with_cli=False):
    root = Path(root).resolve()
    findings = []
    manifest = check_manifest(root, findings)
    check_manifest_dir_contents(root, findings)
    check_antigravity_parity(root, manifest, findings)
    skills = check_skills(root, findings)
    agents = check_agents(root, findings)
    check_hooks_and_mcp(root, findings)
    check_hygiene(root, findings)
    if with_cli:
        check_with_cli(root, findings)
    return findings, {"skills": skills, "agents": agents}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", nargs="?", default=str(REPO_ROOT), help="plugin root (default: this repository)")
    parser.add_argument("--json", action="store_true", help="emit findings as JSON")
    parser.add_argument("--with-cli", action="store_true", help="also run `claude plugin validate --strict`")
    args = parser.parse_args()
    if not Path(args.root).is_dir():
        print("error: {} is not a directory".format(args.root), file=sys.stderr)
        return 2

    findings, counts = validate(args.root, with_cli=args.with_cli)
    errors = [f for f in findings if f.level == "error"]
    if args.json:
        print(json.dumps({"valid": not errors, "counts": counts, "findings": [f.to_dict() for f in findings]}, indent=2))
    else:
        for f in findings:
            print(f, file=sys.stderr if f.level == "error" else sys.stdout)
        if errors:
            print("FAIL: Claude Code plugin validation failed with {} error(s)".format(len(errors)), file=sys.stderr)
        else:
            print("PASS: Claude Code plugin validation succeeded ({} skills, {} agents)".format(counts["skills"], counts["agents"]))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
