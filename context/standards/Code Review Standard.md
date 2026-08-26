# Code Review Standard

Review in priority order:

1. Correctness
2. Security
3. Data integrity
4. Compatibility
5. Performance
6. Reliability
7. Maintainability
8. Testing
9. Readability

For every finding, identify:
- Severity — one of CRITICAL, HIGH, MEDIUM, LOW, or INFO, per `context/standards/Severity Taxonomy.md`. This is the Mentor's canonical severity vocabulary; do not use any other severity label.
- Location
- Problem
- Impact
- Recommended fix

Separate blocking findings (CRITICAL/HIGH by default) from non-blocking recommendations (MEDIUM/LOW/INFO by default) — see `context/standards/Severity Taxonomy.md` for the full blocking rule. Do not demand unrelated refactoring.
