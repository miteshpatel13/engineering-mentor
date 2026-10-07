# Engineering Mentor

A version-controlled, reusable Engineering Mentor for AI-assisted software development — compatible with **Google Antigravity** and **Claude Code**, and designed to compose with **[GitHub Spec Kit](https://github.com/github/spec-kit)** for spec-driven development and **[Graft](https://github.com/trailhq/Graft)** for codebase intelligence.

## What This Is

Engineering Mentor is a global engineering knowledge base and capability set that any number of independent child repositories can consume. It defines **how software should be engineered**: principles, standards, SOPs, reusable Skills, and Agents. It does not define what any particular application does — that stays with each child repository.

## Why It Exists

Engineering practices (code review rigor, security review, database standards, testing discipline, API design conventions) tend to drift and duplicate across repositories when each project reinvents its own guidance. Engineering Mentor centralizes that guidance once, versions it, and lets child repositories pull in a known, pinned version rather than silently diverging.

## Multi-Platform Architecture

Engineering Mentor functions as a unified multi-agent framework. The core engineering knowledge, standards, and skills are maintained as a **single source of truth** and exposed to different AI environments through dedicated platform adapters:

```text
                  ┌─────────────────────────────────────┐
                  │          Engineering Mentor         │
                  │        Shared Knowledge Base        │
                  │   (skills/, context/, docs/, tests/)│
                  └──────────────────┬──────────────────┘
                                     │
                 ┌───────────────────┴───────────────────┐
                 │                                       │
         ┌───────▼────────┐                      ┌───────▼────────┐
         │  Claude Code   │                      │  Antigravity   │
         │    Adapter     │                      │    Adapter     │
         └───────┬────────┘                      └───────┬────────┘
                 │                                       │
     .claude-plugin/plugin.json                  plugin.json (root)
     skills/<name>/SKILL.md                      rules/AGENTS.md
     agents/mentor-reviewer.md                   .agents/skills.json
                                                 .agents/rules/AGENTS.md
                                                 antigravity/
```

### Shared Core vs. Platform Adapters

| Component | Scope | Role |
|---|---|---|
| **`skills/`** | **Shared** | 31 reusable, platform-independent engineering skills (`skills/<name>/SKILL.md`) using standard YAML frontmatter. |
| **`context/`** | **Shared** | Comprehensive reference knowledge: core principles, standards, SOPs, checklists, and templates. |
| **`docs/`** | **Shared** | Integration contract, governance precedence model, taxonomy, schemas, and certification records. |
| **`tests/` & `scripts/`** | **Shared** | Narrative test scenarios, evaluation suites, and deterministic validation runners. |
| **`.claude-plugin/`** | **Claude Code** | Claude plugin manifest (`plugin.json`) for Claude Code CLI and marketplace distribution. Only `plugin.json` belongs here. |
| **`agents/`** | **Claude Code** | Specialized subagent definition (`mentor-reviewer.md`). |
| **`evals/`** | **Claude Code** | Behavioral eval suite for `claude plugin eval` — checks that the right Skill fires and that its output follows Mentor standards. |
| **`plugin.json`** | **Antigravity** | Root Antigravity plugin manifest (`https://antigravity.google/schemas/v1/plugin.json`). |
| **`rules/AGENTS.md`** | **Antigravity** | Active plugin rules loaded automatically when the plugin is enabled in Antigravity. |
| **`.agents/`** | **Antigravity** | Workspace configuration (`skills.json`, `rules/AGENTS.md`) for zero-install discovery when opening the repository. |
| **`antigravity/`** | **Antigravity** | Platform adapter documentation and integration guides. |

## Mentor vs. Child Architecture

| | Engineering Mentor (this repo) | Child Repository |
|---|---|---|
| Answers | *How* should this be engineered? | *What* does this system do? |
| Owns | Engineering principles, architecture guidance, standards, SOPs, reusable Skills, Agents, checklists, templates | Business/domain knowledge, project architecture, tech stack, database schema, API contracts, project-specific Skills/Agents/rules |
| Independence | Repository-independent — must not assume a specific stack, framework, or domain | Independently owned and deployable |

Conflict priority when Mentor guidance and a child's legitimate project-specific requirement disagree:

1. Explicit user request (live in-session instruction)
2. Security and safety requirements (Mentor Mandatory rules)
3. Child repository requirements and architecture (`.mentor/project.yaml`, child rules)
4. Engineering Mentor global standards (`context/standards/`)
5. General engineering best practices

The Mentor must never invent facts about a child repository — it inspects the child before applying repository-sensitive guidance and adapts its principles to that repository's actual technology and architecture.

## Core Capabilities

| Capability | Provided by |
|---|---|
| **Engineering Governance** | Mentor standards, SOPs, governance precedence (`context/`, `docs/`), severity taxonomy |
| **Spec-Driven Development** | [GitHub Spec Kit](docs/integrations/spec-kit.md), routed and gated by `spec-driven-development` and `implementation-plan-review` |
| **Codebase Intelligence** | [Graft](docs/integrations/graft.md), consumed through `codebase-orientation` |
| **Architecture Review** | `architecture-review`, `implementation-plan-review` |
| **Security** | `security-review`, Security Standards and Checklist |
| **Performance** | `performance-review`, `jmeter-performance-testing`, `algorithm-complexity` |
| **Testing** | `testing-review`, Testing Standards |
| **Database** | `database-review`, `database-indexing`, `soft-delete`, `uuid-strategy`, `idempotency` |
| **API Design** | `api-contract-design`, `api-review`, `swagger-openapi` |
| **Git Governance** | Git & Change Management Standard, applied through `code-review` |

Each system keeps one responsibility: **Engineering Mentor governs *how* engineering is done. Spec Kit structures *what* is built and how the work is planned. Graft helps the agent *understand the existing codebase* before changing it.** None contains the others' source; see [`docs/architecture/engineering-workflow.md`](docs/architecture/engineering-workflow.md).

## Spec-Driven Development with Spec Kit

- **When to use it:** substantial features, architectural changes, and substantial database or API changes. Not for questions, typos, or small bugs — `spec-driven-development` routes those to lighter workflows (a bug gets assess → fix → test → review).
- **How it integrates:** Spec Kit's official Claude Code integration installs `/speckit-*` skills into your project's `.claude/skills/`; Mentor does not wrap or rename them. Mentor routes to them, reviews `plan.md` with `implementation-plan-review` after `/speckit-plan` (the **plan gate**), and runs its Review skills after `/speckit-converge` reports Converged (the **review gates**). Add the Engineering Governance principle from [`docs/integrations/spec-kit.md`](docs/integrations/spec-kit.md#constitution-make-spec-kit-enforce-the-mentor-gates) to your constitution and Spec Kit's own Constitution Check enforces the plan gate.
- **Where artifacts live:** in your project — `.specify/` (constitution, feature pointer, bug and assessment reports) and `specs/<NNN-feature>/` (spec, plan, tasks). Never in this plugin.
- **Install** (Python 3.11+ and `uv`), per project:

  ```bash
  uv tool install specify-cli
  specify init . --integration claude
  ```

  Optional processes: `specify extension add bug` and `specify extension add assess`. Antigravity: `--integration agy`.
- **Upgrade:** follow Spec Kit's [Upgrade guide](https://github.github.io/spec-kit/upgrade.html). Mentor is verified against Spec Kit 1.0.13 (supported `>=1.0.13 <2.0.0`).

## Codebase Intelligence with Graft

- **What it provides:** a local graph of your repository (symbols, callers, dependencies, repo map, blast radius of a diff), kept fresh automatically, plus a Claude Code skill, hooks, statusline, and MCP server.
- **How it integrates:** `codebase-orientation` uses Graft — when your project has it — to answer what a change touches before planning it: affected modules, dependencies, APIs, database relationships, downstream consumers, and boundaries. Graft output is treated as evidence to verify, not authority. Without Graft, orientation falls back to direct repository inspection. Mentor ships no Graft hooks or configuration.
- **Initialize** (Node.js 20+), per project:

  ```bash
  npm install -g @nanonets/graft
  graft init --agents claude
  ```

- **Why `graft/` is not committed:** it is a regenerable local cache (like `node_modules`); `graft build` adds `/graft/` to `.gitignore` itself and each teammate builds their own. Also keep `.graft/` out of git — it can hold a Trail read token.
- **What `.claude/` contains after `graft init`:** `skills/graft/SKILL.md`, `helpers/graft-hooks.cjs` and `graft-statusline.cjs`, and Graft's hook, statusline, and permission blocks merged into `settings.json`; plus a `graft` server in `.mcp.json`. Commit these so the team shares the wiring. Review the data-sharing notes in [`docs/integrations/graft.md`](docs/integrations/graft.md) before using `--deep` builds or Trail on proprietary code.

Mentor is verified against Graft 0.21.1.

## Recommended Workflow

```text
Request → Mentor (classify) → Spec (/speckit-specify, /speckit-clarify) → Graft context (codebase-orientation)
        → Plan (/speckit-plan) → Plan gate (implementation-plan-review) → Tasks (/speckit-tasks)
        → Implement (/speckit-implement) ⇄ Converge (/speckit-converge)
        → Review (code-review + security / database / API / performance as relevant) → Test (testing-review, verify)
        → Production readiness (Release Checklist)
```

That is the path for a production feature. Smaller work gets less: a question is answered directly, a typo is just fixed, a bug goes assess → fix → test → review. Ask Claude to build, fix, or change something and `engineering-mentor:spec-driven-development` picks the route — for features, invoke it explicitly (`/engineering-mentor:spec-driven-development <request>`) when other broad project skills such as Graft's are installed, since they can win automatic selection; the full set of routes and diagrams is in [`docs/architecture/engineering-workflow.md`](docs/architecture/engineering-workflow.md).

## Directory Structure

```text
engineering-mentor/
│
├── .claude-plugin/
│   └── plugin.json              # Claude Code plugin manifest
│
├── plugin.json                  # Antigravity plugin manifest
│
├── rules/
│   └── AGENTS.md                # Antigravity active plugin rules (Operating Model, Precedence)
│
├── .agents/                     # Antigravity workspace configuration
│   ├── skills.json              # Workspace skill registration pointing to skills/
│   └── rules/
│       └── AGENTS.md            # Workspace rules for developing the Mentor repository
│
├── antigravity/
│   └── README.md                # Antigravity adapter documentation
│
├── skills/                      # 31 shared, repository-independent Skills
│   ├── code-review/SKILL.md
│   ├── architecture-review/SKILL.md
│   ├── security-review/SKILL.md
│   ├── database-review/SKILL.md
│   ├── api-contract-design/SKILL.md
│   ├── testing-review/SKILL.md
│   ├── idempotency/SKILL.md
│   ├── uuid-strategy/SKILL.md
│   ├── soft-delete/SKILL.md
│   ├── validation/SKILL.md
│   ├── dynamic-form-engine/SKILL.md
│   ├── requirements-discipline/SKILL.md
│   ├── context-discovery/SKILL.md
│   ├── mentor-development/SKILL.md
│   └── ... (31 total)
│
├── agents/                      # specialized Mentor Agents
│   └── mentor-reviewer.md
│
├── evals/                       # Claude Code behavioral evals (claude plugin eval)
│   └── <case>/prompt.md + graders/
│
├── context/                     # Mentor's knowledge base (reference material, not executable)
│   ├── core/                    # Engineering & Architecture Principles, Mentor Operating Model, Governance Rules
│   ├── standards/                # Code Review, Security, Performance, Database, API, Testing, Engineering standards
│   ├── sop/                      # Feature dev, bug fixing, debugging, refactoring, API/DB change, release SOPs
│   ├── checklists/               # Feature, PR, Performance, Release, Security checklists
│   └── templates/                # Agent, Skill, SOP, Review templates
│
├── docs/                        # integration & versioning documentation
│   ├── architecture/engineering-workflow.md   # Mentor + Spec Kit + Graft architecture
│   ├── integrations/spec-kit.md               # Spec Kit: versions, install, artifacts, upgrades
│   ├── integrations/graft.md                  # Graft: versions, install, what to commit, upgrades
│   ├── Child Repository Integration.md
│   ├── Governance Precedence Model.md
│   ├── Skill Taxonomy.md
│   └── Versioning Strategy.md
│
├── tests/skill-tests/           # Skill test scenarios and evaluation evidence
├── scripts/                     # Deterministic automation and validation runners
│   ├── validate_skill.py
│   ├── validate_antigravity.py
│   ├── validate_claude_plugin.py
│   └── ...
│
├── README.md
└── .gitignore
```

## Installation

### Google Antigravity Installation

#### Option A: Global Plugin (Recommended for Individual Developers)
Clone the repository into your global Antigravity plugins directory:

```bash
git clone https://github.com/miteshpatel13/engineering-mentor.git ~/.gemini/config/plugins/engineering-mentor
```

When Antigravity starts, it automatically detects `plugin.json`, exposes all 31 skills, and applies the governance rules from `rules/AGENTS.md`.

#### Option B: Project-Level Plugin (Recommended for Teams)
Clone directly into the project's `.agents/plugins/` directory:

```bash
git clone https://github.com/miteshpatel13/engineering-mentor.git <your-project>/.agents/plugins/engineering-mentor
```

Or reference it in `<your-project>/.agents/plugins.json`:

```json
{
  "entries": [
    {
      "path": "path/to/engineering-mentor"
    }
  ]
}
```

### Claude Code Installation

Engineering Mentor is distributed through the [`mentors-marketplace`](https://github.com/miteshpatel13/mentors-marketplace) catalog. The marketplace only lists the plugin; the plugin itself is fetched from this repository.

#### Option A: Install from the marketplace (recommended)

Inside a Claude Code session:

```text
/plugin marketplace add miteshpatel13/mentors-marketplace
/plugin install engineering-mentor@mentors-marketplace
```

Or from your shell:

```bash
claude plugin marketplace add miteshpatel13/mentors-marketplace
claude plugin install engineering-mentor@mentors-marketplace
```

Machines without a GitHub SSH key can set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` so the clone uses HTTPS. To pick up a new release later:

```bash
claude plugin marketplace update mentors-marketplace
claude plugin update engineering-mentor@mentors-marketplace
```

To share the marketplace with everyone working in a project, run `claude plugin marketplace add miteshpatel13/mentors-marketplace --scope project` in that project once and commit the `.claude/settings.json` it writes.

#### Option B: Load a local checkout for one session

No install step — useful for trying a branch or developing the Mentor itself:

```bash
claude --plugin-dir /absolute/path/to/engineering-mentor
```

#### How Claude Code finds Mentor files

Skills refer to Mentor standards, SOPs, and scripts with repository-relative paths such as `context/standards/Severity Taxonomy.md` and `scripts/discover_project_context.py`. Each Skill carries a **Resource paths** note that resolves those against `${CLAUDE_PLUGIN_ROOT}` — Claude Code substitutes the plugin's installed directory there — so a Skill used inside a child repository reads the Mentor's own files rather than looking for them in the child. Skills that run Mentor scripts (for example `context-discovery`) need Python 3 with PyYAML available on the machine.

## Local Development & Testing

### Working on the Repository in Google Antigravity
When you open `engineering-mentor` in Antigravity (IDE, CLI, or Desktop):
- `.agents/skills.json` automatically registers the canonical `skills/` directory.
- All 31 skills are immediately available in chat via `/<skill_name>`.
- `.agents/rules/AGENTS.md` automatically activates workspace development guidelines.

### Working on the Repository in Claude Code

1. **Validate the plugin** (manifest plus the frontmatter of every skill and agent). `--strict` also fails on warnings:

   ```bash
   claude plugin validate /absolute/path/to/engineering-mentor --strict
   ```

2. **Load your working copy** for one session. If the marketplace copy is also installed, disable it first (`claude plugin disable engineering-mentor@mentors-marketplace`) so you know which copy you are testing:

   ```bash
   claude --plugin-dir /absolute/path/to/engineering-mentor
   ```

3. **Invoke skills** through the plugin namespace, or describe a task and let Claude pick the skill from its description:

   ```text
   /engineering-mentor:code-review
   /engineering-mentor:security-review
   /engineering-mentor:database-review
   /engineering-mentor:architecture-review
   /engineering-mentor:api-contract-design
   ```

   The agent is available as `engineering-mentor:mentor-reviewer`.

4. **Reload after editing** skills, agents, or the manifest — no restart needed:

   ```text
   /reload-plugins
   ```

   `/plugin` shows the loaded components under **Installed** and any load failures under **Errors**.

5. **Check behavior with evals.** `claude plugin eval` runs each case in `evals/` in an isolated session with and without the plugin and scores the difference (requires Claude Code v2.1.269+). Every run is a real model call billed to your account, so iterate on one case at a time:

   ```bash
   claude plugin eval . --case code-review-sql-injection --runs 1 --ablation none
   ```

   Run the full suite, with the no-plugin baseline, before a release:

   ```bash
   claude plugin eval . --scaffold --threshold 0.8 --no-publish --max-cost-usd 20
   ```

   Results go to `evals/results/`, which is git-ignored. See `evals/README.md` for what each case checks.

### Automated Validation Suite
Run the full deterministic validation suite before committing:

```bash
# Claude Code plugin packaging validation (add --with-cli to also run `claude plugin validate --strict`)
python3 scripts/validate_claude_plugin.py
python3 scripts/run_claude_plugin_tests.py

# Antigravity integration validation
python3 scripts/validate_antigravity.py

# Skill standard & taxonomy validation
python3 scripts/run_skill_standard_tests.py

# Governance & context discovery suites
python3 scripts/run_project_yaml_tests.py
python3 scripts/run_context_discovery_tests.py
python3 scripts/run_rules_and_exceptions_tests.py
python3 scripts/run_governance_evaluation_tests.py
python3 scripts/run_skill_test_evidence_tests.py
```

## Skills Catalog

All 32 skills are repository-independent and available across both platforms (in Claude Code, prefix each with `engineering-mentor:`):

| Skill | Category | Description |
|---|---|---|
| `code-review` | Review | Production-grade review of code changes prioritizing correctness, security, and data integrity. |
| `architecture-review` | Review | Architectural evaluation of system designs, boundaries, scalability, and patterns. |
| `security-review` | Review | Deep security audit for OWASP Top 10, auth, injection, and authorization vulnerabilities. |
| `database-review` | Review | Review database migrations, schema alterations, index plans, and transaction boundaries. |
| `api-review` | Review | Review API contracts, REST conventions, backward compatibility, and error shapes. |
| `testing-review` | Review | Evaluate test suites for coverage quality, mock boundaries, and flaky failure modes. |
| `performance-review` | Review | Analyze resource bottlenecks, N+1 query patterns, indexing, and latency risks. |
| `api-contract-design` | Implementation | Design backwards-compatible, robust API contracts and specifications. |
| `idempotency` | Implementation | Design and review idempotent operations, deduplication keys, and retry safety. |
| `uuid-strategy` | Implementation | Select and apply primary key / identifier strategies (UUIDv4, UUIDv7, ULID, BigInt). |
| `soft-delete` | Implementation | Implement safe soft-delete patterns, uniqueness handling, and cascade strategies. |
| `validation` | Implementation | Implement multi-layer input validation, sanitization, and invariant protection. |
| `dynamic-form-engine` | Architecture | Design and evaluate schema-driven dynamic form engines and submission versioning. |
| `database-indexing` | Database | Design indexes for query patterns, composite indexes, and index maintenance. |
| `enum-management` | Architecture | Manage lifecycle, migration, and serialization of state machine enums. |
| `file-storage` | Integration | Architect object storage, pre-signed upload URLs, virus scanning, and metadata storage. |
| `notification-integration` | Integration | Design resilient notification systems (SMS, email, push) with retry and rate-limiting. |
| `payment-integration` | Integration | Integrate payment gateways with webhook verification, ledgering, and idempotency. |
| `third-party-integration` | Integration | Analyze, design, implement, review, secure, and operate third-party integrations (APIs, webhooks, events, files, SDKs). |
| `swagger-openapi` | Documentation | Author and review OpenAPI / Swagger specifications and documentation. |
| `documentation` | Documentation | Generate and maintain engineering documentation, READMEs, and runbooks. |
| `requirements-discipline` | Process | Clarify ambiguous specifications, resolve open points, and structure user stories. |
| `context-discovery` | Governance | Discover and evaluate child repository `.mentor/` configuration and conventions. |
| `jmeter-performance-testing`| Testing | Author and validate JMeter performance test scripts and load testing plans. |
| `algorithm-complexity` | Performance | Analyze, review, and optimize time and space complexity, loops, recursion, and Big-O trade-offs. |
| `skill-creator` | Meta | Author new production-grade Mentor skills conforming to standard taxonomy. |
| `skill-tester` | Meta | Create adversarial and edge-case test fixtures for skill evaluation. |
| `skill-reviewer` | Meta | Review existing skills against quality, ambiguity, and taxonomy standards. |
| `mentor-development` | Meta | Operational and governance guide for developing the Engineering Mentor itself. |
| `spec-driven-development` | Workflow | Route a request to the lightest safe workflow — none, bug flow, Spec Kit SDD, or architecture-first — and place Mentor gates around Spec Kit phases. |
| `implementation-plan-review` | Review | Review a Spec Kit `plan.md` (or any plan) across architecture, security, performance, database, API, observability, testing, compatibility, migration, and deployment risk before tasks are generated. |
| `codebase-orientation` | Workflow | Establish a change footprint — modules, dependencies, APIs, data, consumers, boundaries — using Graft when available, direct inspection otherwise. |

## Adding a New Skill

Because skills are platform-independent, adding a new skill makes it immediately available on both Claude Code and Antigravity:

1. Create a directory: `skills/<skill-name>/`
2. Create the main instruction file: `skills/<skill-name>/SKILL.md`
3. Add required frontmatter:
   ```yaml
   ---
   name: <skill-name>
   description: <Actionable description stating what it does and when to use it>
   category: <Taxonomy Category per docs/Skill Taxonomy.md>
   skillType: <Taxonomy Type per docs/Skill Taxonomy.md>
   ---
   ```
   `category` and `skillType` are Mentor taxonomy fields read by `scripts/validate_skill.py`; Claude Code ignores them. Keep `description` under 1,536 characters (Claude Code's listing cap) and lead with the primary use case.
4. Start from `context/templates/Skill Template.md`, which includes the **Resource paths** note under the title — keep it whenever the Skill references `context/`, `docs/`, or `scripts/` files. Include every required section from `docs/Skill Standard.md`.
5. Run the validation suite:
   ```bash
   python3 scripts/validate_skill.py skills/<skill-name>/SKILL.md
   python3 scripts/validate_claude_plugin.py --with-cli
   python3 scripts/validate_antigravity.py
   ```
6. Commit the file — no duplicate files, symlinks, or platform-specific registrations required.

## Platform-Specific Notes

- **Slash Commands**:
  - In **Claude Code**, skills are namespaced under the plugin prefix: `/engineering-mentor:<skill-name>`.
  - In **Google Antigravity**, skills are invoked directly as root slash commands: `/<skill-name>`, or automatically activated by the agent via semantic matching on the skill description.
- **Rules**:
  - In **Claude Code**, rules in child repositories live in `.claude/rules/`. Claude Code plugins have no always-on rules component (a plugin-root `CLAUDE.md` is not loaded), so `rules/AGENTS.md` is Antigravity-only; in Claude Code the same governance reaches Claude through the Skills that apply it.
  - In **Google Antigravity**, active plugin rules are provided via `rules/AGENTS.md`, and project rules via `AGENTS.md` or `.agents/rules/*.md`.
- **Agents**:
  - In **Claude Code**, `agents/mentor-reviewer.md` is exposed as the subagent `engineering-mentor:mentor-reviewer`.
  - In **Google Antigravity**, `mentor-reviewer` can be invoked as a subagent or referenced for governance reviews.

## Versioning

Engineering Mentor uses semantic versioning for releases:

- **MAJOR** — breaking changes to the Mentor's contract, governance precedence, or integration model.
- **MINOR** — backward-compatible new Skills, standards, SOPs, or capabilities.
- **PATCH** — clarifications, corrections, and non-breaking improvements.

Child repositories should pin or intentionally select a Mentor version rather than silently receiving uncontrolled breaking changes. See `docs/Versioning Strategy.md` for details. The current manifest version is `2.1.0`; `.claude-plugin/plugin.json` and the Antigravity `plugin.json` must always carry the same version (enforced by `scripts/validate_claude_plugin.py`). Claude Code users receive a release only when this version changes, so bump it on every release.
