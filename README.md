# Engineering Mentor

A version-controlled global engineering mentor for AI-assisted software development.

## Purpose

Engineering Mentor provides reusable global engineering guidance for multiple child repositories:

- Engineering principles
- Architecture standards
- API and backend standards
- Database standards
- Testing standards
- Security standards
- Performance standards
- Development SOPs
- Reusable AI Skills
- Specialized Agents
- Checklists and templates
- Skill testing and evaluation

The Mentor defines **how software should be engineered**. A child repository defines **what its system is and how its domain works**.

## Repository Model

```text
Engineering Mentor
        |
        +-- Global Context
        +-- Global Skills
        +-- Global Agents
        +-- Global Rules
        +-- Global SOPs
        |
        +--------------------+
                             |
                     Child Repository
                             |
                             +-- Project Context
                             +-- Project Skills
                             +-- Project Agents
                             +-- Project Rules
                             +-- Application Code
```

## Source of Truth

The `context/` directory contains the Mentor's reusable knowledge base.

The `.claude/` directory contains Claude Code-specific executable/project configuration.

Do not place child-repository business knowledge in this repository.
