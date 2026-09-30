# Google Antigravity Integration

This directory documents how the `engineering-mentor` repository integrates with **Google Antigravity**.

## Overview

Engineering Mentor is configured to operate natively with Google Antigravity as both an installable **Plugin** and a standalone **Workspace**, without duplicating any skill content or modifying Claude Code functionality.

```text
                             Engineering Mentor
                                      │
              ┌───────────────────────┴───────────────────────┐
              │                                               │
      Claude Code Adapter                            Antigravity Adapter
              │                                               │
   .claude-plugin/plugin.json                        plugin.json (root)
   skills/<name>/SKILL.md                            rules/AGENTS.md
   agents/mentor-reviewer.md                         .agents/skills.json
                                                     .agents/rules/AGENTS.md
                                                     antigravity/README.md
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      │
                       Shared Core Knowledge Base
                                      │
                           ├── skills/ (31 Skills)
                           ├── context/ (Standards, SOPs, Principles)
                           ├── docs/ (Governance, Taxonomy, Architecture)
                           └── tests/ (Fixtures, Evidence)
```

## How Antigravity Discovers Engineering Mentor

Antigravity supports three primary ways to consume this repository:

### 1. Global Plugin Installation (Available to All Projects)

Clone the repository into your user's global Antigravity plugins directory:

```bash
git clone https://github.com/miteshpatel13/engineering-mentor.git ~/.gemini/config/plugins/engineering-mentor
```

When Antigravity starts, it automatically detects:
- `plugin.json`: Plugin manifest and metadata
- `skills/`: All 31 skills under `skills/<skill_name>/SKILL.md`
- `rules/AGENTS.md`: Active plugin rules establishing the Mentor Operating Model and Governance Precedence

### 2. Project-Level Plugin Installation (VCS-Tracked per Project)

For teams wanting to pin Engineering Mentor to a specific project:

```bash
git clone https://github.com/miteshpatel13/engineering-mentor.git <project-root>/.agents/plugins/engineering-mentor
```

Or configure `<project-root>/.agents/plugins.json`:

```json
{
  "entries": [
    {
      "path": "path/to/engineering-mentor"
    }
  ]
}
```

### 3. Direct Workspace Development (Working on the Mentor Itself)

When opening `engineering-mentor` directly as a workspace in the Antigravity IDE or CLI (`agy`):
- `.agents/skills.json` points directly to the `skills` directory.
- All 31 skills become instantly available without requiring installation.
- `.agents/rules/AGENTS.md` provides development rules for maintaining technology-agnostic standards.

## Skills Invocation in Antigravity

Once loaded, all skills are discoverable by Antigravity's semantic reasoning and can also be triggered directly in chat:

- `/code-review`
- `/architecture-review`
- `/security-review`
- `/database-review`
- `/api-contract-design`
- `/api-review`
- `/idempotency`
- `/uuid-strategy`
- `/soft-delete`
- `/testing-review`
- `/performance-review`
- `/requirements-discipline`
- `/context-discovery`
- *(and all remaining skills)*

## Spec Kit and Graft in Antigravity

Engineering Mentor's workflow skills (`spec-driven-development`, `implementation-plan-review`, `codebase-orientation`) are ordinary shared skills and load in Antigravity like every other Mentor skill. The external tools are installed per project, using each tool's own Antigravity support:

- **Spec Kit** has an official Antigravity integration: `specify init . --integration agy` installs its skills into the project's `.agents/skills/`, invoked as `/speckit-<command>`. See `docs/integrations/spec-kit.md`.
- **Graft** has no Antigravity-specific integration. Its `agents` target writes a Graft section into the project's `AGENTS.md` (`graft init --agents agents --no-global`), and its MCP server can be registered by hand. This route is not yet verified end to end in Antigravity. See `docs/integrations/graft.md`.

Nothing from either tool is copied into this repository, so no Antigravity adapter code is needed for them.

## Verification

To verify that the Antigravity integration is intact:

```bash
python3 scripts/validate_antigravity.py
```
