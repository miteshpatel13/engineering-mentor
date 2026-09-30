# Integration: Graft

| | |
|---|---|
| **Tool** | Graft (`graft` CLI, npm package `@nanonets/graft`) |
| **Purpose in the Mentor system** | Codebase intelligence layer — helps the agent *understand the existing codebase* before changing it |
| **Official repository** | https://github.com/trailhq/Graft |
| **License** | MIT (Copyright (c) 2026 Context Graph Engine contributors) |
| **Verified against** | `@nanonets/graft` 0.21.1 (npm `latest` dist-tag; repository `main` at commit `fe30ead`, 2026-09-30). The repository publishes no GitHub releases; npm is the version source |
| **Supported range** | `0.21.x`. Graft is pre-1.0, so treat each new minor version as needing re-verification of this document. Older installs (for example 0.16.x) differ; upgrade before relying on this document |
| **Relationship** | Optional, recommended per-project development dependency. Engineering Mentor does not bundle, fork, wrap, or install Graft, and contains none of its source or wiring |

## What Graft provides

A codebase graph built from the repository: a deterministic, tree-sitter per-symbol wiring graph (no model, no key, no network) and, optionally, a language-model layer of concept nodes and summaries (`graft build --deep`, using the user's own provider key). Queries refresh the graph first when the working tree has moved.

CLI (as of 0.21.1): `graft init`, `build`, `ask`, `skeleton`, `callers`, `grep`, `map`, `blast`, `check`, `viz`, `uninstall`, `version`/`upgrade`, and `trail` commands for Graft's hosted Trail service. MCP tools: `graft_find_code`, `graft_file_api`, `graft_trace_calls`, `graft_find_all`, `graft_repo_map`, `graft_check_freshness`.

## Installation (per machine, per project)

Engineering Mentor never installs Graft or runs `graft init`. The user runs, from the official README (requires Node.js 20+):

```bash
npm install -g @nanonets/graft        # once per machine (or use npx @nanonets/graft …)
cd your-project
graft init --dry-run                  # optional: list every file init would touch
graft init --agents claude            # wire Claude Code only and build the graph
```

`graft init` on a terminal prompts for which agents to wire (Claude Code is preselected); with no TTY it writes nothing unless `--agents` or `--yes` is passed. Graft checks npm for new versions daily; `graft upgrade` updates the global install.

## What `graft init` writes, and what to commit

For Claude Code, all repo-local:

| Path | What | Commit? |
|---|---|---|
| `.claude/skills/graft/SKILL.md` | Graft's own skill: how Claude should query the graph | Yes |
| `.claude/helpers/graft-hooks.cjs`, `.claude/helpers/graft-statusline.cjs` | Hook and statusline shims | Yes |
| `.claude/settings.json` | Merged blocks: `SessionStart`/`UserPromptSubmit`/`PostToolUse`/`Stop` hooks, a `statusLine`, and `Bash(graft:*)`-style permission allow rules. Commands use `${CLAUDE_PROJECT_DIR:-.}`, so they carry no machine paths | Yes — review the merged permissions first: the allow list includes `Bash(graft:*)`, `Bash(npx graft:*)`, `Bash(graft-dev:*)`, and `Bash(node dist/cli.js:*)`; the last lets *any* `node dist/cli.js …` in the project run without a prompt, so remove it unless the project is Graft itself |
| `.mcp.json` | `mcpServers.graft`. Observed form: `"command": "graft", "args": ["mcp"]`, which needs Graft installed globally on every teammate's machine; the README's portable alternative is `npx -y @nanonets/graft mcp` | Yes |
| `.ignore` | Re-admits `graft/` to ripgrep-based search (ripgrep reads `.ignore` before `.gitignore`) while excluding `graft/.cache/` and `graft/.graph/` | Yes |
| `graft/` | The generated graph — a local, regenerable cache | **No.** `graft build` adds `/graft/` to `.gitignore` itself |
| `.graft/` | Local build config and, once a Trail is linked, a read token (`trail-push.log` also lands here) | **No.** Graft ignores it when a Trail link is created; add `/.graft/` to `.gitignore` yourself so it is ignored before that |

Each teammate runs `graft build` to generate their own graph. This matches Graft's README: share the `.claude/` wiring, not the graph. `graft init` merges into an existing `.claude/settings.json` and leaves other content, including a non-Graft `statusLine`, untouched; pass `--no-statusline` to skip its statusline, `--no-hooks` or `--no-mcp` to skip those.

Selecting Graft's `agents` target (for `AGENTS.md`-reading agents) also writes to the user-level `~/.codex/` when it exists; `--no-global` prevents writes outside the repository.

## How Engineering Mentor integrates

Engineering Mentor **consumes** Graft context; it doesn't become Graft or wrap it:

```text
Engineering Mentor ──consumes──▶ Graft context ──▶ Claude Code
```

- `skills/codebase-orientation/SKILL.md` defines what must be understood before a significant change — affected modules, dependencies, related APIs, database relationships, downstream consumers, architectural boundaries, tests — and uses Graft to answer it when available, falling back to direct repository inspection when not. How to call Graft's tools is left to Graft's own project skill, so Graft CLI changes don't require Mentor changes.
- `skills/implementation-plan-review/SKILL.md` checks a plan's assertions ("no other callers") against that footprint.
- `skills/spec-driven-development/SKILL.md` routes every change to existing code through orientation before planning, which matters most for architecture, database, API, refactoring, performance, and security-sensitive work.

Graft output is **contextual evidence**, not authority: facts that change a plan or a finding's severity are confirmed against source, and Graft context never overrides explicit project requirements, a spec, or a `.mentor/` rule.

Engineering Mentor ships **no hooks, statusline, or MCP configuration** for Graft. Graft's hooks live in the project and are maintained by Graft; duplicating them in the plugin would run them twice.

## Governance notes for teams

- **Code leaving the machine.** Plain `graft build` and all queries are local. `graft build --deep` and `graft blast --name` send code to the model provider configured in `GRAFT_PROVIDER`/`GRAFT_API_KEY`/`GRAFT_MODEL`. `graft trail push` sends repository history to Graft's hosted Trail service and, once a Trail is linked, Graft's session hook may run it in the background (disable with `GRAFT_TRAIL_AUTOPUSH=0`). Treat these as data-sharing decisions under the project's security policy.
- **Telemetry.** Graft sends an anonymous daily usage ping (documented in its `TELEMETRY.md`); disable with `graft telemetry disable` or `DO_NOT_TRACK=1`.
- **Secrets.** Never commit `.graft/` or provider keys; keep `GRAFT_API_KEY` in the environment, not in `.claude/settings.json`.

## What Engineering Mentor consumes

Graft query results (through its CLI or MCP tools, as the agent's permissions allow), graph freshness status, and the presence of `graft/` and Graft's wiring — all read-only.

## What Engineering Mentor does not control

Graft's CLI, MCP tools, graph format, hooks, statusline, skill file, telemetry, and Trail service. Mentor never runs `graft init`, `build --deep`, `trail`, `upgrade`, or `uninstall`, and never edits Graft's wiring.

## Upgrade process

1. The user runs `graft upgrade` (or `npm install -g @nanonets/graft@latest`); the next session refreshes the project's wiring itself.
2. Mentor maintainers re-verify this document: package name, `graft init` outputs and what to commit, the gitignore behavior, and the governance notes. Update **Verified against** and **Supported range**.
3. Run `claude plugin eval . --scaffold --tag graft` to confirm orientation behavior.

Because `codebase-orientation` defers command usage to Graft's own skill, a Graft release normally requires edits to this document only.

## Antigravity

Graft has no Antigravity-specific integration (its agent ids: `agents`, `cursor`, `gemini`, `grok`, `copilot`, `kiro`, `windsurf`, `adal`, `claude`). Its `agents` target writes a marker-fenced section into the project's `AGENTS.md`, which this repository's Antigravity adapter documents as a project-rules file Antigravity reads — use `graft init --agents agents --no-global`. Its MCP server can also be registered by hand (`npx -y @nanonets/graft mcp`) in an agent that supports MCP. This route has not been verified end to end in Antigravity.

## Known limitations

- **Skill selection with Graft installed.** Graft's project skill describes itself as applying to *any* task in the repository. In an end-to-end test (Graft 0.16.0, Spec Kit 0.16.3, this plugin, one feature request) Claude chose Graft's skill, oriented well — it found a consumer the request didn't mention — but did not engage `spec-driven-development`, so Spec Kit and the plan gate were never suggested. Invoked explicitly (`/engineering-mentor:spec-driven-development …`), the full flow worked: Spec Kit and Graft were detected and the gated workflow was produced. Mitigation, project-owned and optional: invoke the routing skill explicitly for features, or add a line to the project's `CLAUDE.md` such as "For new features and architectural, database, or API changes, start with /engineering-mentor:spec-driven-development." Mentor does not edit Graft's skill.
- Static analysis misses dynamic dispatch, reflection, string-built routes, and cross-service network calls; `codebase-orientation` searches for these explicitly.
- Mentor's evals run in isolated workspaces without Graft, so they test the fallback path and the discipline around Graft, not Graft's own retrieval quality.
