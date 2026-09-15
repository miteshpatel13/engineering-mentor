# Engineering Mentor

A version-controlled, reusable Engineering Mentor for AI-assisted software development — compatible with **Google Antigravity** and **Claude Code**.

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
| **`skills/`** | **Shared** | 27 reusable, platform-independent engineering skills (`skills/<name>/SKILL.md`) using standard YAML frontmatter. |
| **`context/`** | **Shared** | Comprehensive reference knowledge: core principles, standards, SOPs, checklists, and templates. |
| **`docs/`** | **Shared** | Integration contract, governance precedence model, taxonomy, schemas, and certification records. |
| **`tests/` & `scripts/`** | **Shared** | Narrative test scenarios, evaluation suites, and deterministic validation runners. |
| **`.claude-plugin/`** | **Claude Code** | Claude plugin manifest (`plugin.json`) for Claude Code CLI and marketplace distribution. |
| **`agents/`** | **Claude Code** | Specialized subagent definition (`mentor-reviewer.md`). |
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
├── skills/                      # 27 shared, repository-independent Skills
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
│   └── ... (27 total)
│
├── agents/                      # specialized Mentor Agents
│   └── mentor-reviewer.md
│
├── context/                     # Mentor's knowledge base (reference material, not executable)
│   ├── core/                    # Engineering & Architecture Principles, Mentor Operating Model, Governance Rules
│   ├── standards/                # Code Review, Security, Performance, Database, API, Testing, Engineering standards
│   ├── sop/                      # Feature dev, bug fixing, debugging, refactoring, API/DB change, release SOPs
│   ├── checklists/               # Feature, PR, Performance, Release, Security checklists
│   └── templates/                # Agent, Skill, SOP, Review templates
│
├── docs/                        # integration & versioning documentation
│   ├── Child Repository Integration.md
│   ├── Governance Precedence Model.md
│   ├── Skill Taxonomy.md
│   └── Versioning Strategy.md
│
├── tests/skill-tests/           # Skill test scenarios and evaluation evidence
├── scripts/                     # Deterministic automation and validation runners
│   ├── validate_skill.py
│   ├── validate_antigravity.py
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

When Antigravity starts, it automatically detects `plugin.json`, exposes all 27 skills, and applies the governance rules from `rules/AGENTS.md`.

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

#### Option A: Local Plugin
From your Claude Code session or project, add the plugin by referencing this repository:

```bash
claude plugin add /path/to/engineering-mentor
```

#### Option B: Claude Marketplace (When Published)
Once published to a team or public marketplace catalog:

```bash
claude plugin add engineering-mentor
```

## Local Development & Testing

### Working on the Repository in Google Antigravity
When you open `engineering-mentor` in Antigravity (IDE, CLI, or Desktop):
- `.agents/skills.json` automatically registers the canonical `skills/` directory.
- All 27 skills are immediately available in chat via `/<skill_name>`.
- `.agents/rules/AGENTS.md` automatically activates workspace development guidelines.

### Working on the Repository in Claude Code
When developing locally with Claude Code:
- Test skill execution via the plugin namespace: `/engineering-mentor:<skill_name>`.
- Validate plugin structure with:
  ```bash
  claude plugin validate .
  ```

### Automated Validation Suite
Run the full deterministic validation suite before committing:

```bash
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

All 27 skills are repository-independent and available across both platforms:

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
| `swagger-openapi` | Documentation | Author and review OpenAPI / Swagger specifications and documentation. |
| `documentation` | Documentation | Generate and maintain engineering documentation, READMEs, and runbooks. |
| `requirements-discipline` | Process | Clarify ambiguous specifications, resolve open points, and structure user stories. |
| `context-discovery` | Governance | Discover and evaluate child repository `.mentor/` configuration and conventions. |
| `jmeter-performance-testing`| Testing | Author and validate JMeter performance test scripts and load testing plans. |
| `skill-creator` | Meta | Author new production-grade Mentor skills conforming to standard taxonomy. |
| `skill-tester` | Meta | Create adversarial and edge-case test fixtures for skill evaluation. |
| `skill-reviewer` | Meta | Review existing skills against quality, ambiguity, and taxonomy standards. |
| `mentor-development` | Meta | Operational and governance guide for developing the Engineering Mentor itself. |

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
4. Include required sections: `## Purpose`, `## Scope`, `## When to Use`, `## Required Context`, `## Workflow`, `## Expected Output`, `## Verification`.
5. Run the validation suite:
   ```bash
   python3 scripts/validate_skill.py skills/<skill-name>/SKILL.md
   python3 scripts/validate_antigravity.py
   ```
6. Commit the file — no duplicate files, symlinks, or platform-specific registrations required.

## Platform-Specific Notes

- **Slash Commands**:
  - In **Claude Code**, skills are namespaced under the plugin prefix: `/engineering-mentor:<skill-name>`.
  - In **Google Antigravity**, skills are invoked directly as root slash commands: `/<skill-name>`, or automatically activated by the agent via semantic matching on the skill description.
- **Rules**:
  - In **Claude Code**, rules in child repositories live in `.claude/rules/`.
  - In **Google Antigravity**, active plugin rules are provided via `rules/AGENTS.md`, and project rules via `AGENTS.md` or `.agents/rules/*.md`.
- **Agents**:
  - In **Claude Code**, `agents/mentor-reviewer.md` is exposed as an agent persona.
  - In **Google Antigravity**, `mentor-reviewer` can be invoked as a subagent or referenced for governance reviews.

## Versioning

Engineering Mentor uses semantic versioning for releases:

- **MAJOR** — breaking changes to the Mentor's contract, governance precedence, or integration model.
- **MINOR** — backward-compatible new Skills, standards, SOPs, or capabilities.
- **PATCH** — clarifications, corrections, and non-breaking improvements.

Child repositories should pin or intentionally select a Mentor version rather than silently receiving uncontrolled breaking changes. See `docs/Versioning Strategy.md` for details. The current manifest version is `1.0.0`.
