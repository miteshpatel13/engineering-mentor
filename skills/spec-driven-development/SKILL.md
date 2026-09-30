---
name: spec-driven-development
description: Decide how much process an engineering request needs and route it — no ceremony for a trivial change, a bug assess/fix/test flow for a defect, GitHub Spec Kit's spec-driven workflow (constitution, specify, clarify, plan, tasks, implement, converge) for a substantial feature, architecture analysis first for a structural change — and place Engineering Mentor's review gates around those phases. Use when a user asks to build a feature, fix a bug, make an architectural or database change, or asks how to run spec-driven development with Spec Kit.
category: Core Engineering
skillType: Authoring/Workflow
---

# Spec-Driven Development

> **Resource paths:** Mentor file paths in this Skill (`context/…`, `docs/…`, `scripts/…`, `skills/…`, `tests/…`) are relative to the Engineering Mentor root, not the repository being worked on; `.mentor/…` paths refer to the target repository. In Claude Code the Mentor root is `${CLAUDE_PLUGIN_ROOT}` — read and run Mentor files from there.

## Purpose

Choose the lightest workflow that is still safe for a given engineering request, and make Engineering Mentor's quality gates land at the right points of that workflow. GitHub Spec Kit (`docs/integrations/spec-kit.md`) owns *what* is built and how the work is structured — constitution, specification, plan, tasks, implementation, convergence. Graft (`docs/integrations/graft.md`) owns *understanding the existing codebase*. Engineering Mentor owns *how well* it is engineered. This Skill is the routing layer between them; it exists because no other Mentor Skill decides whether a request warrants a specification at all, and forcing every request through full spec-driven development is as harmful as skipping it for a production feature.

## Scope

**In scope:** classifying a request (question, trivial change, bug, feature, architectural change, database/API change); choosing the workflow and naming its steps; detecting whether Spec Kit and Graft are set up in the project; placing Mentor gates (plan review, code/security/database/performance/testing review) around Spec Kit phases; telling the user which Spec Kit skills to run next and what to review before continuing.

**Out of scope:** the Spec Kit phases themselves — writing `spec.md`, `plan.md`, `tasks.md`, running implementation or convergence is done by Spec Kit's own `/speckit-*` skills, which this Skill never re-implements, renames, or edits; codebase exploration (`skills/codebase-orientation/SKILL.md`); reviewing a plan's engineering quality (`skills/implementation-plan-review/SKILL.md`); reviewing code (`skills/code-review/SKILL.md` and the other Review-type Skills); installing or upgrading Spec Kit or Graft (the user does that — `docs/integrations/`).

## When to Use

Use when a user asks to build or add a feature, fix a bug, change architecture, change a database schema or public API, or asks how to apply spec-driven development or Spec Kit in their project — and the right amount of process is not already obvious. Also use when a Spec Kit phase has just finished and the next step (continue, review, or stop) is unclear.

Do not use for a pure question about existing code ("what does this function do?") — answer it, using `skills/codebase-orientation/SKILL.md` if orientation is needed. Do not use when the user has explicitly chosen a workflow and only wants it executed.

## Required Context

Benefits from repository context but degrades gracefully without it (`docs/Skill Standard.md` Section 3, posture 2):

- The request itself.
- Whether Spec Kit is initialized in the project: a `.specify/` directory, `.specify/memory/constitution.md`, and Spec Kit skills such as `speckit-specify` installed for the agent (in Claude Code, under the project's `.claude/skills/`). Bug fixing and idea assessment are opt-in Spec Kit extensions (`bug`, `assess`); check for their skills before recommending them.
- Whether Graft context is available: a `graft/` directory at the project root, the `graft` CLI, or `graft_*` MCP tools.
- The project's Normalized Project Context from `skills/context-discovery/SKILL.md` when the request is repository-sensitive.

Missing Spec Kit or Graft is not an error: say what is missing and route to the equivalent Mentor-only workflow.

## Workflow

1. **Classify the request** into exactly one primary type, using the Rules → Routing table. When it spans types (a feature that needs a migration), take the heaviest type and note the others.
2. **Check tooling** (Required Context). Record: Spec Kit initialized yes/no (and which of `bug`/`assess` are installed), constitution present yes/no, Graft context available yes/no. Never install, initialize, or upgrade either tool yourself; if one would help, give the user the command from `docs/integrations/` and let them run it.
3. **Choose the workflow** from the Routing table, scaled down where the Rules allow. State it to the user as an ordered list, marking each step's owner: Spec Kit, Graft, or Mentor.
4. **Before planning a change to existing code**, route through `skills/codebase-orientation/SKILL.md` (Graft-backed when available) so the plan is grounded in affected modules, dependencies, and consumers rather than assumptions.
5. **Run or hand off the current step.** For a Spec Kit phase, tell the user which `/speckit-*` skill to invoke next and what input it needs; Spec Kit phases are run one at a time and reviewed before continuing. For a Mentor gate, invoke the named Mentor Skill.
6. **Apply the Mentor gates** (Rules → Mentor Gates) at the points the chosen workflow reaches them. A blocking (CRITICAL/HIGH) finding at a gate stops forward progress until it is resolved or explicitly accepted by the user.
7. **Report** per Expected Output.

## Rules

### Routing

| Request type | Signals | Workflow |
|---|---|---|
| Question / exploration | "what does…", "where is…", "how does… work" | Answer directly; `codebase-orientation` if orientation is needed. No Spec Kit. |
| Trivial change | typo, copy, config value, rename with no behavior change | Make the change; `code-review` only if it touches production behavior. No Spec Kit. |
| Bug | observed wrong behavior, error, crash, regression | Assess → Fix → Test → Review. With Spec Kit's `bug` extension: `/speckit-bug-assess` → `/speckit-bug-fix` → `/speckit-bug-test`, then Mentor review. Without it: reproduce and state the cause before changing code, add a failing test first where feasible, fix, then `testing-review` and `code-review`. Full SDD is not required. |
| Feature | new user-facing capability, new endpoint, new workflow | Spec Kit SDD: constitution (once per project) → `/speckit-specify` → `/speckit-clarify` when the spec has open questions → `codebase-orientation` → `/speckit-plan` → **plan gate** → `/speckit-tasks` → `/speckit-implement` → `/speckit-converge` (repeat implement → converge until Converged) → **review gates** → test/verify → production readiness. |
| Architectural change | new service/boundary, data-ownership change, cross-cutting refactor | `codebase-orientation` → `architecture-review` of the proposed direction → Spec Kit specify/plan → **plan gate** → tasks → implement → converge → **review gates**. |
| Database or API change | migration, schema change, public/partner API change | `codebase-orientation` (consumers and dependents first) → `database-review` / `api-review` or `api-contract-design` → Spec Kit SDD if the change is substantial (multiple tables/endpoints, data backfill, a breaking change) → **review gates** with migration-safety and backward-compatibility emphasis. |
| Idea not yet committed to | "should we build…", unclear value | Spec Kit `assess` extension if installed (`/speckit-assess-intake` … `/speckit-assess-decide`); a `go` decision feeds `/speckit-specify`. Otherwise `requirements-discipline`. |

Scale down, never up without reason: a small, low-risk feature confined to one module may skip `/speckit-clarify` and `/speckit-analyze`; a feature touching security, money, personal data, or persisted data never skips the plan gate or the relevant review gate. Mentor Advisory guidance — the project and user decide the process; this Skill recommends it and says why.

### Mentor Gates

- **Plan gate — after `/speckit-plan`, before `/speckit-tasks`:** `skills/implementation-plan-review/SKILL.md` reviews `plan.md` (and its design artifacts) for architecture, security, performance, database design, API design, maintainability, observability, testing, backward compatibility, migration safety, and deployment risk. Fixing a plan is far cheaper than fixing generated tasks or code.
- **Review gates — after `/speckit-converge` reports Converged:** `skills/code-review/SKILL.md` on the resulting change, plus `security-review`, `database-review`, `api-review`, and `performance-review` wherever the change touches their domains, and `testing-review` on the tests. Convergence confirms the code matches the spec; it does not confirm the code is safe or well engineered.
- **Production readiness:** `context/checklists/Release Checklist.md` and `context/sop/Production Release SOP.md`.

### Authority Boundaries

- Engineering Mentor governs engineering quality; Spec Kit governs the feature's requirements and task structure. A spec or plan never overrides a Mentor Mandatory requirement (`docs/Governance Precedence Model.md`): if a plan conflicts with one, the plan changes. Conversely this Skill never rewrites a spec's requirements to suit an engineering preference — it raises the conflict with the user.
- The project owns its artifacts. Spec Kit writes `.specify/` and `specs/<feature>/` in the project; nothing is written into the Engineering Mentor plugin, and this Skill never moves or duplicates those artifacts.
- The project constitution (`.specify/memory/constitution.md`) is project-owned. Recommend Mentor-aligned principles (`docs/integrations/spec-kit.md` → Constitution) but never overwrite a constitution the user already has.

## Constraints

- Never install, initialize, upgrade, or uninstall Spec Kit or Graft, and never run commands that make network calls on the user's behalf (for example Graft's `--deep` build or Trail commands) without explicit user instruction.
- Never edit Spec Kit's installed skills, templates, or `.specify/extensions.yml`, and never edit Graft's `.claude/` wiring.
- Never skip a gate the Routing table marks mandatory for security-, money-, personal-data-, or persisted-data-touching work because the user asked to go faster; say what is being skipped and let the user decide explicitly.

## Governance Integration

Not applicable in the findings sense: this Skill routes work and produces a workflow recommendation, not a compliance evaluation. Every finding in the workflow it recommends is produced by the Review-type Skill at that gate, which applies context discovery, `scripts/evaluate_governance.py`, and `context/standards/Severity Taxonomy.md` itself. The routing recommendations in Rules are Mentor Advisory; the requirement that a plan never overrides a Mentor Mandatory requirement restates `docs/Governance Precedence Model.md` rather than creating a new rule.

## Validation

The output is correct when: the request has exactly one primary type with the signals that justified it; the chosen workflow matches the Routing table or states why it was scaled; every step names its owner (Spec Kit, Graft, Mentor); tooling status was checked rather than assumed; no Spec Kit phase was recommended for a question or trivial change; and every security-, money-, personal-data-, or persisted-data-touching workflow includes the plan gate and the matching review gate.

## Edge Cases

- **Spec Kit not initialized, user wants SDD.** Give the initialization command from `docs/integrations/spec-kit.md` and stop; offer to proceed Mentor-only if they prefer not to install it.
- **Spec Kit initialized but no constitution.** Recommend `/speckit-constitution` first, with Mentor-aligned principles, before `/speckit-specify`.
- **Bug that turns out to be a missing feature or a design flaw.** Stop the bug flow, say so, and re-route (feature or architectural change).
- **Existing `specs/` feature being extended.** Route to Spec Kit's guidance for evolving existing specs rather than creating a parallel feature directory.
- **Request type genuinely ambiguous.** Ask one clarifying question rather than guessing the heavier or lighter workflow.

## Failure Handling

If the request can't be classified from what was given, ask the one question that would classify it. If a gate's Review Skill reports blocking findings, stop and report them; do not advance to the next Spec Kit phase. If Spec Kit or Graft behaves differently from `docs/integrations/` (a renamed skill, a moved artifact), say so, follow the tool's current behavior, and recommend updating the integration doc — never invent a skill or command name.

## Expected Output

A routing decision: request type and the signals behind it; tooling status (Spec Kit, constitution, `bug`/`assess` extensions, Graft); the ordered workflow with each step's owner and which steps were scaled out and why; the immediate next step (the exact `/speckit-*` skill or Mentor Skill to run); and the gates still ahead.

## Examples

**Feature.** "Add customer-level pricing so enterprise customers get negotiated prices." Type: Feature, with persisted-data and money signals. Tooling: Spec Kit initialized, constitution present, Graft available. Workflow: `/speckit-specify` → `/speckit-clarify` (currency, precedence over promotions, effective dates are unstated) → `codebase-orientation` (pricing calculation, order totals, invoice snapshots, their consumers) → `/speckit-plan` → plan gate (`implementation-plan-review`, with `database-review` for the new price table and `payment-integration` guidance on server-side amount calculation) → `/speckit-tasks` → `/speckit-implement` ⇄ `/speckit-converge` → `code-review`, `security-review`, `database-review`, `testing-review` → release checklist. Next step: `/speckit-specify` with the business description, no technology choices.

**Bug.** "Fix this null pointer when the cart is empty." Type: Bug. Workflow: reproduce, state the cause, add a failing test, fix, `testing-review`, `code-review` — or the `/speckit-bug-*` skills if the `bug` extension is installed. No specification.

**Negative example (correctly declines).** "Fix the typo in the README heading." Type: Trivial change. Workflow: make the change. No Spec Kit phase, no review gate — routing a typo through specify/plan/tasks is the failure this Skill exists to prevent.

## Related Skills

- `skills/codebase-orientation/SKILL.md` — Consumed: the understand-before-planning step of every workflow that changes existing code.
- `skills/implementation-plan-review/SKILL.md` — Consumed: the plan gate after `/speckit-plan`.
- `skills/code-review/SKILL.md`, `skills/security-review/SKILL.md`, `skills/database-review/SKILL.md`, `skills/api-review/SKILL.md`, `skills/performance-review/SKILL.md`, `skills/testing-review/SKILL.md` — Consumed: the review gates after convergence.
- `skills/architecture-review/SKILL.md` — Consumed: the first step of an architectural change.
- `skills/requirements-discipline/SKILL.md` — Shares a boundary: labels requirements as CONFIRMED/RECOMMENDATION/ASSUMPTION inside a spec; this Skill decides whether a spec is needed at all.
- `skills/context-discovery/SKILL.md` — Consumed when the request is repository-sensitive.
