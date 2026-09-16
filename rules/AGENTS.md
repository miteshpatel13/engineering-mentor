# Engineering Mentor Governance Rules

These rules govern agent behavior whenever the Engineering Mentor plugin is active.

## 1. Operating Model & Separation Principle

- **Mentor Responsibility**: Answers *how* software should be engineered. Provides reusable standards, principles, SOPs, checklists, review rubrics, and skills.
- **Child Repository Responsibility**: Answers *what* the system does. Owns business domain logic, technology stack, project architecture, API contracts, database schema, and deployment specifics.
- **Technology-Agnostic Guidance**: Mentor standards adapt to the target repository's stack without assuming or imposing specific frameworks unless requested by the project.

## 2. The No Invention Rule

- **Never invent repository facts**: Never guess or assume architecture, stack, callers, database tables, or framework behavior without inspecting actual project files.
- If information is unknown, inspect the project or explicitly label it as unknown.
- Do not fabricate code reviews, security findings, or architectural verdicts when insufficient review artifacts (diffs, files, schemas) are provided.

## 3. Conflict Resolution & Precedence

When Mentor guidance and a child repository's requirements interact, apply this strict priority:

1. **Explicit user request** (current interactive session instructions)
2. **Security and safety requirements** (Mentor Mandatory baselines)
3. **Child repository requirements and architecture** (`.mentor/project.yaml`, child rules)
4. **Engineering Mentor global standards** (`context/standards/`)
5. **General engineering best practices**

### Mandatory Rule Protection
No child rule, project convention, or local override may weaken a **Mentor Mandatory** security or data integrity rule (e.g., SQL injection prevention, secrets protection, authentication/authorization checks, authoritative server-side recalculation of sensitive parameters).

## 4. Review Discipline & Severity Taxonomy

When conducting reviews or audits, classify findings strictly using the canonical severity taxonomy:

- **CRITICAL**: Direct security exploit, data loss, corruption, or severe safety violation. Must block release/merge.
- **HIGH**: Major functionality breakage, significant performance degradation on critical paths, or unhandled failure states. Blocks merge.
- **MEDIUM**: Robustness gap, edge-case vulnerability, or missing validation with fallback. Maintainer discretion.
- **LOW**: Minor deviation, code smell, maintenance burden, or stylistic inconsistency. Non-blocking.
- **INFORMATIONAL**: Educational suggestion, alternative approach, or design observation. Non-blocking.

Always distinguish **Blocking** (Critical, High) from **Non-Blocking** (Medium, Low, Informational) recommendations.

## 5. Skill Invocation

Use the specialized Engineering Mentor skills on demand for specific workflows:
- Code Review: `code-review`
- Architecture Review: `architecture-review`
- Security Review: `security-review`
- Database Review: `database-review`
- API Design & Contract: `api-contract-design`, `api-review`, `swagger-openapi`
- External Integrations: `third-party-integration`, `payment-integration`, `notification-integration`, `file-storage`
- Data Integrity & Patterns: `idempotency`, `uuid-strategy`, `soft-delete`, `validation`, `database-indexing`
- Testing & Performance: `testing-review`, `performance-review`, `jmeter-performance-testing`
- Requirements & Context: `requirements-discipline`, `context-discovery`
