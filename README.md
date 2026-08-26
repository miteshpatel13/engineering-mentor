# Engineering Mentor

A version-controlled, reusable Engineering Mentor for AI-assisted software development — distributed as a **Claude Code plugin**.

## What This Is

Engineering Mentor is a global engineering knowledge base and capability set that any number of independent child repositories can consume. It defines **how software should be engineered**: principles, standards, SOPs, reusable Skills, and Agents. It does not define what any particular application does — that stays with each child repository.

## Why It Exists

Engineering practices (code review rigor, security review, database standards, testing discipline, API design conventions) tend to drift and duplicate across repositories when each project reinvents its own guidance. Engineering Mentor centralizes that guidance once, versions it, and lets child repositories pull in a known, pinned version rather than silently diverging.

## Mentor vs. Child Architecture

| | Engineering Mentor (this repo) | Child Repository |
|---|---|---|
| Answers | *How* should this be engineered? | *What* does this system do? |
| Owns | Engineering principles, architecture guidance, standards, SOPs, reusable Skills, Agents, checklists, templates | Business/domain knowledge, project architecture, tech stack, database schema, API contracts, project-specific Skills/Agents/rules |
| Independence | Repository-independent — must not assume a specific stack, framework, or domain | Independently owned and deployable |

Conflict priority when Mentor guidance and a child's legitimate project-specific requirement disagree:

1. Explicit user request
2. Security and safety requirements
3. Child repository requirements and architecture
4. Engineering Mentor global standards
5. General engineering best practices

The Mentor must never invent facts about a child repository — it inspects the child before applying repository-sensitive guidance and adapts its principles to that repository's actual technology and architecture.

## Plugin Architecture

This repository is structured as a Claude Code plugin. The manifest lives at `.claude-plugin/plugin.json`; the plugin's executable components (`skills/`, `agents/`) sit at the repository root, not inside `.claude-plugin/`, per current Claude Code plugin conventions.

```text
engineering-mentor/
│
├── .claude-plugin/
│   └── plugin.json              # plugin manifest (name, version, description, author)
│
├── skills/                      # reusable, repository-independent Claude Skills
│   ├── skill-creator/SKILL.md
│   ├── skill-tester/SKILL.md
│   ├── skill-reviewer/SKILL.md
│   ├── architecture-review/SKILL.md
│   ├── code-review/SKILL.md
│   ├── security-review/SKILL.md
│   ├── performance-review/SKILL.md
│   ├── database-review/SKILL.md
│   ├── api-design/SKILL.md
│   └── testing-review/SKILL.md
│
├── agents/                      # specialized Mentor Agents
│   └── mentor-reviewer.md
│
├── context/                     # Mentor's knowledge base (reference material, not executable)
│   ├── core/                    # Engineering & Architecture Principles, Mentor Operating Model, Mentor Governance Rules
│   ├── standards/                # Code Review, Security, Performance, Database, API & Backend, Testing, Engineering, Git standards
│   ├── sop/                      # Feature dev, bug fixing, debugging, refactoring, API/DB change, release, security review SOPs
│   ├── skills/                   # standards governing how Skills should be built and tested
│   ├── agents/                   # standard governing how Agents should be built
│   ├── checklists/               # Feature, PR, Performance, Release, Security checklists
│   └── templates/                # Agent, Skill, SOP, Review templates
│
├── docs/                        # integration & versioning documentation
│   ├── Child Repository Integration.md
│   └── Versioning Strategy.md
│
├── tests/skill-tests/           # reserved for Skill test scenarios
├── scripts/                     # reserved for repository automation (validation, linting)
│
├── CLAUDE.md                    # operating instructions for Claude when acting as the Mentor
├── README.md
└── .gitignore
```

**Directory roles, precisely:**

- `skills/` — executable Claude Skills, exposed under the plugin namespace (see below). Repository-independent by design.
- `agents/` — specialized Mentor Agent definitions.
- `context/` — the Mentor's knowledge base. Standards, SOPs, checklists, and templates that Skills and Agents draw on. `context/skills/` and `context/agents/` hold the *standards that govern* how Skills and Agents should be built — they are not Skill or Agent instances themselves (those live in the top-level `skills/` and `agents/` directories).
- `docs/` — documentation about the Mentor repository and its integration/versioning approach — not part of the plugin's runtime surface.

## Global Skills

Once this plugin is installed, its Skills are invoked under the plugin namespace:

```text
/engineering-mentor:code-review
/engineering-mentor:architecture-review
/engineering-mentor:security-review
/engineering-mentor:performance-review
/engineering-mentor:database-review
/engineering-mentor:api-design
/engineering-mentor:testing-review
/engineering-mentor:skill-creator
/engineering-mentor:skill-tester
/engineering-mentor:skill-reviewer
```

Each `SKILL.md`'s `name` frontmatter field matches its directory name exactly, and each `description` states what the Skill does, when to use it, and what kind of engineering problem it addresses — so Claude can select the right Skill without an explicit slash command.

## Global Agents

- **`mentor-reviewer`** — reviews Mentor standards, Skills, SOPs, and Agents themselves for quality, ambiguity, conflicts, and maintainability. This is a meta-governance Agent for the Mentor's own content, not a per-domain reviewer (domain review — architecture, security, performance, database, API, testing — is handled by the corresponding Skills above).

The Agent roster is intentionally minimal in this first plugin version. Expanding it (e.g. dedicated Architect, Debugger, or Test Engineer Agents) is deferred until the Skill-based approach has been validated in practice.

## Context (Knowledge Base)

`context/` is not converted into Skills — it remains the Mentor's reference material, read by Skills, Agents, and by Claude directly when reasoning about engineering decisions. See the directory role notes above.

## Testing the Plugin Locally

This plugin has not yet been installed into a Claude Code session or validated with the official plugin tooling — that is the next step after this restructuring, done separately with your own Claude Code CLI. What has been verified so far in this repository:

- `.claude-plugin/plugin.json` is present at the required location and is valid JSON.
- Every Skill directory name matches its `SKILL.md` `name` frontmatter field exactly.
- No Skill name is duplicated between the old `.claude/skills/` location and the new `skills/` location (the old location no longer contains any Skills).

No plugin installation commands are documented here yet, since none have been run against this repository. Once you validate installation locally, this section should be updated with the exact verified steps.

## Distribution

Not yet available. This plugin is intended to eventually be distributed via a Claude Code plugin marketplace, but the marketplace repository has not been created — this repository must be validated as a correct, installable plugin on its own first.

## Versioning

Engineering Mentor uses semantic versioning for releases:

- **MAJOR** — breaking changes to the Mentor's contract or integration model.
- **MINOR** — backward-compatible new Skills, standards, SOPs, or capabilities.
- **PATCH** — clarifications, corrections, and non-breaking improvements.

Child repositories should pin or intentionally select a Mentor version rather than silently receiving uncontrolled breaking changes. See `docs/Versioning Strategy.md` for details. The current manifest version is `1.0.0`.
