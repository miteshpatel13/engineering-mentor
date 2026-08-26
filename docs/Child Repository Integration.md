# Child Repository Integration

A child repository should consume the Mentor as a global engineering dependency while keeping project-specific knowledge local.

## Recommended Child Structure

```text
child-repo/
├── CLAUDE.md
├── .claude/
│   ├── skills/
│   ├── agents/
│   └── rules/
├── .mentor/
└── src/
```

`.mentor/` should point to a versioned Mentor release or be populated through the team's chosen synchronization mechanism.

## Child CLAUDE.md Responsibilities

The child should:
- Identify the project stack.
- Explain architecture.
- Define business/domain rules.
- Identify project-specific Skills and Agents.
- Explain commands and validation.
- Reference the Mentor's global guidance.

The child must not duplicate the entire Mentor.
