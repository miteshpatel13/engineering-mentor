# Integration: GitHub Spec Kit

| | |
|---|---|
| **Tool** | Spec Kit (`specify` CLI plus agent skills) |
| **Purpose in the Mentor system** | Specification and workflow layer — structures *what* is built and how the work is planned |
| **Official repository** | https://github.com/github/spec-kit — docs: https://github.github.io/spec-kit/ |
| **License** | MIT (Copyright GitHub, Inc.) |
| **Verified against** | v1.0.13 (released 2026-09-29; repository `main` at commit `2c0a57a`, 2026-09-29) |
| **Supported range** | `>=1.0.13 <2.0.0`. Older releases (for example 0.16.x) predate parts of the current skill set; upgrade before relying on this document. A new major version needs this document re-verified |
| **Relationship** | Optional, recommended project-level dependency. Engineering Mentor does not bundle, fork, wrap, or rename Spec Kit, and contains none of its source |

## What Spec Kit provides

Three independent processes, each a set of agent skills invoked one at a time and reviewed before continuing:

| Process | Skills (skills mode, as installed for Claude Code) | Availability | Artifacts |
|---|---|---|---|
| Spec-Driven Development | `/speckit-constitution`, `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-checklist`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`, `/speckit-converge`, `/speckit-taskstoissues` | Core | `.specify/memory/constitution.md`, `specs/<NNN-feature>/spec.md`, `plan.md`, `tasks.md`, design artifacts, `checklists/` |
| Bug fixing | `/speckit-bug-assess`, `/speckit-bug-fix`, `/speckit-bug-test` | Opt-in extension `bug` | `.specify/bugs/<slug>/` |
| Idea assessment | `/speckit-assess-intake`, `-research`, `-define`, `-shape`, `-decide` | Opt-in extension `assess` | `.specify/assessments/<slug>/` |

The active feature is tracked in `.specify/feature.json` (overridable with `SPECIFY_FEATURE_DIRECTORY`), not by the git branch. `/speckit-clarify`, `/speckit-checklist`, and `/speckit-analyze` are optional quality gates; implement → converge repeats until converge reports **Converged**.

Spec Kit is extended through **extensions** (new commands and lifecycle hooks such as `after_plan`), **presets** (overrides of templates and commands), **workflows**, and **bundles**. Its `specify` CLI also offers `specify artifact list --json` to inspect what is installed.

## Installation (per machine, per project)

Engineering Mentor never installs Spec Kit. The user runs, from the official instructions (requires Python 3.11+ and `uv`):

```bash
uv tool install specify-cli            # once per machine
cd your-project
specify init . --integration claude    # Claude Code: installs skills into .claude/skills/
specify extension add bug              # optional: bug-fixing process
specify extension add assess           # optional: idea assessment
```

For Antigravity use `--integration agy` (installs skills into `.agents/skills/`). For pinned releases, CI, or upgrades see the official [Installation](https://github.github.io/spec-kit/installation.html) and [Upgrade](https://github.github.io/spec-kit/upgrade.html) guides.

## How Engineering Mentor integrates

Spec Kit's official Claude Code integration installs its skills into the **project's** `.claude/skills/speckit-*/`, where Claude Code loads them directly as `/speckit-*`. Engineering Mentor's skills load from the plugin under the `engineering-mentor:` namespace. The two sets cannot collide, so Mentor exposes no Spec Kit skills of its own — re-publishing them as `/engineering-mentor:specify` would duplicate Spec Kit and drift from it on every Spec Kit release.

Mentor integrates at three points, all using Spec Kit's own mechanisms:

1. **Routing** — `skills/spec-driven-development/SKILL.md` decides whether a request needs Spec Kit at all (a typo or a question doesn't; a production feature does), checks whether Spec Kit, the constitution, and the `bug`/`assess` extensions are present, and tells the user which `/speckit-*` skill runs next.
2. **Plan gate** — after `/speckit-plan` and before `/speckit-tasks`, `skills/implementation-plan-review/SKILL.md` reviews `plan.md` and its design artifacts for engineering quality (architecture, security, performance, database, API, observability, testing, compatibility, migration and deployment risk). Spec Kit's `/speckit-analyze` checks consistency; Mentor checks engineering.
3. **Review gates** — after `/speckit-converge` reports Converged, the Mentor Review Skills (`code-review`, `security-review`, `database-review`, `api-review`, `performance-review`, `testing-review`) review the resulting change. Convergence proves the code matches the spec, not that it is safe.

### Constitution: make Spec Kit enforce the Mentor gates

`/speckit-plan` fills a **Constitution Check** gate from `.specify/memory/constitution.md` before research and again after design, and `/speckit-analyze` treats a violated constitution MUST as CRITICAL. A project that adopts the principles below through its own constitution gets the Mentor gates enforced by Spec Kit itself, with no extension code. The constitution is project-owned: add these with `/speckit-constitution` (or edit the file), adapting the wording — Mentor never writes it.

```text
/speckit-constitution Add an "Engineering Governance" principle: Engineering Mentor standards
(the engineering-mentor Claude Code plugin) are the authority for engineering quality.
MUST: every plan.md passes engineering-mentor:implementation-plan-review with no open
CRITICAL or HIGH finding before /speckit-tasks. MUST: plans for changes to existing code are
based on a codebase footprint (engineering-mentor:codebase-orientation). MUST: after
/speckit-converge reports Converged, the change passes engineering-mentor:code-review, plus
security-review, database-review, api-review, or performance-review when it touches those
areas, before merge. MUST NOT: a spec, plan, or principle weaken a security or data-integrity
requirement from the Engineering Mentor standards.
```

### Not shipped: a Spec Kit extension

Spec Kit's hook events (`after_plan`, `after_implement`, …) could trigger Mentor reviews automatically through an extension. Mentor deliberately does not ship one yet: the hook would need to be a Spec Kit command installed into every project, the constitution route above already gates the plan using Spec Kit's native mechanism, and a second distribution channel would have to track Spec Kit's extension API. Revisit if projects need the gate to fire without a constitution principle.

## Project artifacts

All Spec Kit artifacts belong to the project, never to Engineering Mentor:

```text
your-project/
├── .specify/
│   ├── memory/constitution.md     # project principles (commit)
│   ├── feature.json               # active feature pointer
│   ├── templates/, scripts/       # Spec Kit-managed (commit so the team shares them)
│   ├── extensions.yml             # installed extensions and hooks
│   ├── bugs/<slug>/               # bug extension reports
│   └── assessments/<slug>/        # assess extension artifacts
├── specs/<NNN-feature>/           # spec.md, plan.md, tasks.md, design artifacts (commit)
└── .claude/skills/speckit-*/      # Claude Code integration, written by specify init (commit)
```

Commit these per the team's Spec Kit practice. Nothing from a user's project is ever written into the Engineering Mentor plugin.

## What Engineering Mentor consumes

Read-only: the active feature's `spec.md`, `plan.md`, `tasks.md`, and design artifacts; `.specify/memory/constitution.md`; `.specify/feature.json`; the presence of Spec Kit skills and extensions.

## What Engineering Mentor does not control

Spec Kit's skills, templates, scripts, extension hooks, CLI, artifact layout, and constitution content. Mentor never edits Spec Kit files, runs `specify` commands, or installs extensions on the user's behalf.

## Upgrade process

1. The user upgrades Spec Kit per its [Upgrade guide](https://github.github.io/spec-kit/upgrade.html) (`specify integration upgrade`, which preserves specs and the constitution).
2. Mentor maintainers re-verify this document against the new release: skill names in the process table, artifact paths, the Constitution Check gate in `/speckit-plan`, and the hook events. Update **Verified against** and **Supported range**.
3. Run `claude plugin eval . --scaffold --tag spec-kit` to confirm routing still recommends the right skills.

Because Mentor references Spec Kit by documented skill names and artifact paths only, a Spec Kit release requires at most edits to this document and the routing table in `skills/spec-driven-development/SKILL.md` — never a rewrite.

## Known limitations

- Automatic routing to Spec Kit depends on Claude selecting `spec-driven-development`. With other broad project skills present (notably Graft's), it may not be selected on its own; see `docs/integrations/graft.md` → Known limitations for the observed behavior and the explicit-invocation / `CLAUDE.md` mitigation.
- The plan gate is enforced by the project's constitution, or by following `spec-driven-development`; without either, nothing forces `implementation-plan-review` to run.
- Mentor's evals run without Spec Kit installed (each eval run is an isolated empty workspace), so they test Mentor's routing and gates, not Spec Kit's own skills.
- Skill invocation syntax differs by agent and mode (for example Copilot's commands mode uses `/speckit.specify`); this document uses the Claude Code skills form.
