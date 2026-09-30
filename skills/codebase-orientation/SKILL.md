---
name: codebase-orientation
description: Build an evidence-based picture of the existing code a change will touch before planning or making it — affected modules, dependencies, related APIs, database relationships, downstream consumers, and architectural boundaries — using Graft's codebase graph when the project has it and direct repository inspection when it doesn't. Use before a significant change, refactor, database or API change, performance optimization, or security-sensitive change, when orienting in an unfamiliar repository, or when asked what a change could break.
category: Core Engineering
skillType: Authoring/Workflow
---

# Codebase Orientation

> **Resource paths:** Mentor file paths in this Skill (`context/…`, `docs/…`, `scripts/…`, `skills/…`, `tests/…`) are relative to the Engineering Mentor root, not the repository being worked on; `.mentor/…` paths refer to the target repository. In Claude Code the Mentor root is `${CLAUDE_PLUGIN_ROOT}` — read and run Mentor files from there.

## Purpose

Make sure a change is planned against the code as it actually is. Most damaging changes are not wrong in themselves; they are made without knowing who else depends on what they touch. This Skill produces a change footprint — the modules, APIs, data, consumers, and boundaries in play — before a plan is written or code is edited. When the project uses Graft (`docs/integrations/graft.md`), Graft supplies the codebase graph and this Skill consumes it; Graft's own project skill defines how to call its tools. This Skill adds what Graft doesn't: which questions must be answered before a significant change, how to treat tool output as evidence, and what to do when no graph exists. It is separate from `skills/context-discovery/SKILL.md`, which discovers a repository's declared Mentor governance (`.mentor/`), not its code structure.

## Scope

**In scope:** establishing the footprint of a proposed change in existing code; repository orientation for an unfamiliar codebase; blast-radius questions ("what does changing X affect?"); choosing between Graft and direct inspection; checking graph freshness; stating confidence and gaps.

**Out of scope:** installing, initializing, building, or configuring Graft (`docs/integrations/graft.md`; the user runs those commands); how to invoke each Graft command or MCP tool (Graft's own `graft` project skill and documentation are authoritative); judging whether the change is a good idea (the Review-type Skills); discovering `.mentor/` governance context (`skills/context-discovery/SKILL.md`); writing the plan (Spec Kit's `/speckit-plan` or the user).

## When to Use

Use before: a change that touches more than one module; a refactor; a database schema or migration change; a public or internal API change; a performance optimization; a security-sensitive change (authentication, authorization, input handling, secrets, personal data). Also use when a user asks where something lives, how a subsystem fits together, or what a change could break, in a repository that isn't already understood in this session.

Do not use for a one-line change whose effects are fully visible in the file being edited, or when the footprint was already established earlier in the session and the code hasn't moved.

## Required Context

Requires the repository itself (read access); degrades gracefully without Graft (`docs/Skill Standard.md` Section 3, posture 2):

- The proposed change or question, specific enough to name a starting point (a feature area, file, symbol, table, or endpoint).
- Graft availability, checked rather than assumed: a `graft/` directory at the project root, the `graft` CLI on the PATH, or `graft_*` MCP tools. If Graft is wired into the project, its `graft` skill describes its current commands and tools.
- Otherwise, direct inspection with the agent's read and search tools.

## Workflow

1. **State the starting point** — the symbols, files, endpoints, or tables the change is expected to touch. If none can be named, ask.
2. **Choose the source.** If Graft context is available, use it first, following Graft's own skill for command choice. If Graft reports a stale graph (a freshness check, or its statusline warning), prefer a refreshed query or confirm against source; never plan on a graph known to be stale. If Graft is unavailable, use direct inspection (search for definitions, references, imports, routes, and schema files) and say that the footprint was built without a graph.
3. **Answer the orientation questions** in Rules → Orientation Questions, as far as the change warrants. For each, record the evidence: file and line, symbol, or query result.
4. **Verify what matters.** Any footprint fact that would change a plan or a finding's severity — "no other callers", "only used internally", "this table has no other writers" — is confirmed against source, not taken from a summary alone.
5. **Report** the footprint per Expected Output, including what could not be determined.

## Rules

### Orientation Questions

1. **Affected modules** — which modules, packages, or services the change edits directly.
2. **Dependencies** — what those modules call or import that the change relies on.
3. **Related APIs** — public, internal, and event interfaces the change adds, alters, or relies on.
4. **Database relationships** — tables, columns, constraints, and migrations involved, and every other component that reads or writes the same data.
5. **Downstream consumers** — callers, importers, API clients, event subscribers, jobs, and reports that depend on what changes (the blast radius).
6. **Architectural boundaries** — which boundaries the change crosses or leans on, and whether it reaches past a module's public interface.
7. **Tests** — existing tests that cover the affected behavior, and gaps.
8. **Then plan** — only after 1–7 does planning begin; the footprint is an input to the plan (`skills/implementation-plan-review/SKILL.md` checks the plan against it).

Scale to the change: a single-module refactor needs 1, 5, and 7; a migration needs 4 and 5 in depth; a security-sensitive change needs 3, 5, and 6.

### Evidence Discipline

Graft output is contextual evidence, not authority. A node summary or ranked result can be outdated, incomplete, or wrong about intent; exact references (callers, imports, file:line spans) are stronger than prose summaries. Codebase context never overrides explicit project requirements, a spec, or a `.mentor/` rule — it informs them. Never invent a dependency or consumer that no source shows (Mentor Operating Model's No Invention Rule, `context/core/Mentor Operating Model.md`); when evidence is incomplete, say what is unknown.

### Tool Hygiene

Queries that only read the existing graph or the repository are fine to run. Commands that write project files, rebuild with a language model, or contact an external service — initializing Graft, `--deep` builds that send code to a model provider, Trail commands that push repository history to Graft's hosted service — are the user's decision; recommend them, don't run them. Mentor Advisory.

## Constraints

Read-only with respect to the repository and its Graft wiring: never edit `.claude/` Graft files, `.mcp.json`, `graft/`, or `.graft/`, and never commit graph output. Never send repository content to an external service without the user's explicit instruction.

## Governance Integration

Not applicable in the findings sense: this Skill produces a factual footprint, not a compliance evaluation. Review-type Skills that consume the footprint (`skills/implementation-plan-review/SKILL.md`, `skills/architecture-review/SKILL.md`, `skills/database-review/SKILL.md`, and others) apply context discovery, `scripts/evaluate_governance.py`, and `context/standards/Severity Taxonomy.md` themselves. Its Rules are Mentor Advisory process guidance and make no claim on child-repository behavior.

## Validation

A footprint is complete when each orientation question relevant to the change is answered with evidence or marked unknown; the source (Graft or direct inspection) and graph freshness are stated; every fact that could change a plan or severity was verified against source; and nothing is listed that no evidence supports.

## Edge Cases

- **Graft installed but graph never built** (no `graft/`). Treat as unavailable; mention that the user can build it (`docs/integrations/graft.md`), and proceed with direct inspection.
- **Monorepo or multi-repo folder.** Scope queries to the relevant sub-project and say which one.
- **Dynamic dispatch, reflection, string-built routes, or cross-service calls over the network.** Static graphs and text search both miss these; say so and search for the dynamic patterns explicitly (route tables, configuration, message topics).
- **Generated or vendored code.** Exclude it from the footprint unless the change touches its generator.
- **Graft and source disagree.** Source wins; note the disagreement so the graph can be refreshed.

## Failure Handling

If no starting point can be identified, ask for one. If the repository can't be read, stop and say so. If the footprint can't be established to the confidence the change needs (for example, consumers live in repositories not available here), report the gap as an explicit risk for the plan and the reviewers rather than assuming there are no consumers.

## Expected Output

A change footprint: starting point; source used (Graft with freshness status, or direct inspection); answers to the relevant orientation questions, each with evidence; verified versus unverified facts; unknowns and the risk they carry; and the next step (typically planning, or `skills/implementation-plan-review/SKILL.md` if a plan already exists).

## Examples

**Positive example.** Before planning "add customer-level pricing": with Graft available and fresh, a query for the pricing calculation and a caller trace on the price function show three consumers — checkout totals, invoice generation, and a nightly revenue report. The report reads `order_items.unit_price` directly from the database, bypassing the pricing module. Footprint: modules `pricing`, `checkout`, `invoicing`; data `order_items.unit_price`, new `customer_prices`; consumers include the revenue report (verified at its SQL file). Risk: the report would ignore customer pricing unless it switches to the stored snapshot. Next: `/speckit-plan`.

**Negative example (correctly declines).** "Rename the local variable `tmp` to `total` in this function." The effect is fully visible in the function; no footprint is built and no graph is queried.

## Related Skills

- `skills/spec-driven-development/SKILL.md` — Consumer: runs this Skill before planning any change to existing code.
- `skills/implementation-plan-review/SKILL.md` — Consumer: checks a plan's assertions against this footprint.
- `skills/architecture-review/SKILL.md`, `skills/database-review/SKILL.md`, `skills/api-review/SKILL.md`, `skills/performance-review/SKILL.md`, `skills/security-review/SKILL.md` — Consumers: use the footprint as context for their reviews.
- `skills/context-discovery/SKILL.md` — Shares a boundary: discovers declared `.mentor/` governance context; this Skill discovers code structure.
