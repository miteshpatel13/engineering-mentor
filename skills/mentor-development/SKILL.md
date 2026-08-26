---
name: mentor-development
description: Guidance for developing, maintaining, reviewing, and extending the Engineering Mentor repository itself — how to create and test Mentor Skills, develop Mentor Agents, maintain global context, avoid project-specific leakage, review changes, and follow versioning and governance rules. Use when creating or modifying a Skill, Agent, or standard in this repository, reviewing a proposed change to it, or deciding whether a piece of guidance belongs in the Mentor versus a child repository.
---

# Mentor Development

## Purpose

The Engineering Mentor is a version-controlled, reusable engineering knowledge base and capability set, distributed as a Claude Code plugin, that provides senior-level, production-grade engineering guidance — principles, standards, SOPs, Skills, Agents, checklists, and templates — to any number of independent child repositories. This Skill governs how the Mentor itself should be built, changed, and kept trustworthy over time. It applies to work *on* this repository, not work performed *by* it inside a child repository.

## Scope

Applies when: creating or editing a Skill or Agent under `skills/` or `agents/`; adding or changing a standard, SOP, checklist, or template under `context/`; reviewing a change to this repository; deciding whether a piece of guidance is globally reusable or belongs in a specific child repository instead; or making a versioning/release decision for the Mentor.

Does not apply to work inside a child repository's own `.claude/skills/`, `.claude/agents/`, or `.claude/rules/` — those are project-specific and out of scope for this Skill.

## Mentor vs Child Architecture

- Mentor = global engineering knowledge: reusable principles, standards, SOPs, Skills, Agents, checklists, templates, and the meta-process for creating, testing, and versioning them.
- Child = project/domain-specific knowledge: business rules, project architecture, technology stack, repository structure, database schema, API contracts, and project-specific Skills/Agents/rules.
- Mentor answers "how should this be engineered?"; a child repository answers "what does this system do, and what constraints does this project have?"
- Never invent child-repository facts. Inspect the child repository before applying repository-sensitive guidance, and adapt global principles to that child's actual technology and architecture rather than forcing a mismatched pattern — e.g. adapt the underlying principle behind a database standard to MongoDB rather than forcing a PostgreSQL-shaped rule onto it.
- A child's legitimate project-specific requirement can override generic Mentor guidance when justified. Conflict priority: (1) explicit user request, (2) security and safety requirements, (3) child repository requirements and architecture, (4) Engineering Mentor global standards, (5) general engineering best practices.

## Global vs Project-Specific Responsibilities

Belongs in the Mentor only when genuinely reusable across multiple repositories: engineering and architecture principles; standards for API, database, security, performance, testing, code review, and git/change management; SOPs; Skill and Agent development/testing standards; checklists; templates.

Never belongs in the Mentor: business logic for a specific application, project-specific database schemas, project-specific API contracts, project-specific domain rules, child repository source code, or a technology assumption that isn't globally applicable.

## How Mentor Skills Should Be Created

1. Define the Skill's purpose and scope before writing anything.
2. Define its triggers/use cases and required context.
3. Define its workflow, rules, and constraints.
4. Define how its output is validated.
5. Define edge cases and failure handling.
6. Create realistic test scenarios before considering it done (see Testing, below).
7. Ensure no project-specific assumptions leak into a global Skill (see Avoiding Leakage, below).
8. Give it valid frontmatter: `name` must exactly match its directory name under `skills/<name>/SKILL.md` — this is what makes `/engineering-mentor:<name>` resolve — and `description` must state what the Skill does, when to use it, and what kind of engineering problem it addresses. A vague description ("perform a review") prevents Claude from selecting the right Skill.
9. Follow `context/skills/Skill Development Standard.md` and `context/templates/Skill Template.md` for the full structure a production Skill should have.

## How Mentor Skills Should Be Tested

A Skill is not production-ready merely because its instructions read well. Per `context/skills/Skill Testing & Evaluation Standard.md`, test it against: the happy path, edge cases, invalid input, missing context, ambiguous requests, conflicting requirements, existing-code scenarios, large inputs, failure scenarios, and security-sensitive scenarios where applicable. When a failure is found: record the scenario, identify the root cause, update the Skill, add a regression test, and re-run the evaluation. Store reproducible scenarios under `tests/skill-tests/`.

## How Mentor Agents Should Be Developed

Follow `context/agents/Agent Development Standard.md`: a Mentor Agent needs a clear, narrow responsibility, a defined scope, the Skills it should use, defined inputs and expected outputs, explicit boundaries (what it must not do), and validation expectations. Mentor Agents provide reusable engineering expertise — they are not a place to re-implement what a Skill already does. Do not add an Agent when a Skill already covers the same ground; only add one when the responsibility is genuinely a distinct, standing role rather than an on-demand capability.

## How Global Context Should Be Maintained

`context/` is the Mentor's knowledge base — standards, SOPs, checklists, and templates — and is not converted into Skills. Read the relevant files under `context/` before changing a Mentor standard or creating a new reusable capability; do not invent or duplicate a standard that already exists. `context/skills/` and `context/agents/` hold the standards that govern how Skills and Agents should be built, not Skill or Agent instances themselves — those live in the top-level `skills/` and `agents/` directories. Preserve this distinction when adding new files.

## How to Avoid Project-Specific Leakage

Before adding or changing anything in `context/`, `skills/`, or `agents/`, ask: would this guidance make sense verbatim in an unrelated repository on a different stack? If the answer depends on a specific framework, database, cloud provider, or business domain, either generalize it to the underlying principle or leave it out of the Mentor entirely — it belongs in a child repository's own `.claude/skills/`, `.claude/agents/`, or `.claude/rules/` instead.

## How to Review Changes to the Mentor

Review every change to a standard, SOP, Skill, or Agent for: scope, clarity, contradictions with existing guidance, missing edge cases, testability, reusability across repositories, project-specific leakage, unnecessary complexity, and compatibility with the Mentor Operating Model (`context/core/Mentor Operating Model.md`). Do not simply agree with a proposed change — challenge weak assumptions, and separate blocking issues from optional improvements.

## Quality Expectations

Optimize for correctness, security, reliability, maintainability, scalability, performance, testability, and observability. Avoid unnecessary abstractions, dependencies, rewrites, and unrelated changes. Do not rewrite something simply because a different implementation would look cleaner — preserve working behavior unless a change is explicitly required.

## Versioning Expectations

The Mentor uses semantic versioning (`docs/Versioning Strategy.md`): MAJOR for breaking changes to the Mentor's contract or integration model, MINOR for backward-compatible new Skills, standards, SOPs, or capabilities, PATCH for clarifications and non-breaking corrections. Child repositories pin or intentionally select a Mentor version rather than silently receiving breaking changes — do not ship a change that would silently break a pinned child without an appropriate version bump.

## Repository Governance

Keep global guidance reusable and technology-aware. Do not add project-specific business rules to global standards. When changing a global Skill, Standard, or SOP, consider backward compatibility and add regression coverage when practical. When a recurring engineering problem is discovered in a child repository, determine whether it is project-specific or globally applicable — globally applicable improvements belong in the Mentor and should include regression coverage when practical.

## Validation

A change to this repository is ready when: the Skill, Agent, or standard follows the relevant Development Standard and Template; project-specific leakage has been checked and ruled out; for a Skill, realistic test scenarios exist or are planned under `tests/skill-tests/`; the change doesn't silently break the Mentor's contract with pinned child repositories without an appropriate version bump; and the plugin still validates cleanly (`claude plugin validate .` and `claude plugin validate . --strict`).

## Edge Cases

- A proposed Skill or standard is *almost* globally reusable but has one project-specific assumption baked in — generalize the assumption rather than accepting the leakage, or scope it explicitly and keep it out of the Mentor's global surface.
- A child's legitimate project-specific requirement conflicts with a Mentor standard — the child's requirement wins per the priority order above, but this Skill's job is to make sure that's a deliberate, visible decision rather than a silent one.
- Two Skills, or an Agent and a Skill, appear to cover the same ground (e.g. a review-type Agent and a review-type Skill) — resolve the overlap explicitly rather than leaving both in place with an undefined relationship.

## Failure Handling

If it's unclear whether a piece of guidance belongs in the Mentor or a child repository, or whether a change breaks compatibility for existing child repositories, say so explicitly rather than guessing — this mirrors the Mentor Operating Model's No Invention Rule: unknown information must be inspected or explicitly identified as unknown, never assumed.

## Expected Output

Depending on the request: a new or modified file under `skills/`, `agents/`, or `context/` that follows the standards above, or a structured review (scope, findings ranked by severity, and a recommendation) of a proposed change to this repository.
