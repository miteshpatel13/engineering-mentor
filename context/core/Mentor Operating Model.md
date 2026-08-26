# Mentor Operating Model

## Purpose

Define the relationship between the Engineering Mentor and child repositories.

## Mentor Responsibilities

The Mentor owns reusable global engineering knowledge:

- Engineering principles
- Architecture principles
- Standards
- SOPs
- Skills
- Agents
- Checklists
- Templates
- Skill evaluation
- Engineering quality gates

## Child Responsibilities

A child repository owns:

- Business/domain knowledge
- Project architecture
- Technology stack
- Repository structure
- Project-specific conventions
- Project-specific Skills
- Project-specific Agents
- Project-specific SOPs
- API contracts
- Database schema
- Deployment specifics

## Separation Principle

Mentor answers:

> How should this be engineered?

Child answers:

> What does this system do and what constraints does this project have?

## Conflict Resolution

Project-specific requirements can override generic Mentor guidance when justified. Security requirements and explicit user requirements remain highest priority.

**For the standing, structural question of how a child repository's own declared rules (`.mentor/rules/`) relate to Mentor's own Mandatory/Configurable/Advisory/Informational rules** — as opposed to a single, live, in-session instruction — `docs/Governance Precedence Model.md` is the authoritative, detailed specification. It refines "generic Mentor guidance" into Mentor's own four classification tiers and establishes, without exception, that no child rule (however classified) can weaken a Mentor Mandatory rule. This paragraph's statement about live, in-session explicit user requests is unaffected and unresolved by that document — see its Section 15.3.

## No Invention Rule

The Mentor must never invent repository facts. Unknown information must be inspected or explicitly identified as unknown.

## Reuse Principle

A global capability should be added to the Mentor only when it is broadly reusable across projects.
