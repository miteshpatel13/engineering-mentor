# Severity Taxonomy

## Purpose

This is the canonical severity vocabulary for every Engineering Mentor review-type Skill, Standard, SOP, and Template. Every review-type Skill (`code-review`, `security-review`, `performance-review`, `database-review`, `api-review`, `architecture-review`, `testing-review`) tags findings using these five levels and no others. Do not introduce a different severity vocabulary (e.g. "Major/Minor", "Blocker", "P0/P1/P2", "Required/Optional") into Mentor-level guidance — a child repository may keep its own convention internally, but the Mentor's own output is always expressed in these terms.

## Levels

### CRITICAL
Causes data loss or corruption, is an exploitable security vulnerability (missing authentication/authorization on a sensitive operation, injection, secret exposure, and similar), or is a correctness defect that breaks core functionality or violates an explicit compatibility contract. Always blocking. Must be fixed, or explicitly and knowingly accepted as risk by the requester, before merge or release — never silently downgraded or dropped.

### HIGH
A significant security weakness, data-integrity risk, or correctness defect with real but narrower impact than CRITICAL — an authorization gap on a lower-sensitivity resource, a race condition under realistic concurrency, a validation gap that lets bad data through a non-destructive path. Blocking by default. May be deferred only with an explicit, recorded justification from the requester or reviewer.

### MEDIUM
A real defect or risk that degrades reliability, maintainability, or performance without directly threatening data integrity, security, or core correctness — an N+1 query on a low-traffic path, missing error handling on a non-critical branch, a maintainability problem likely to cause future bugs. Non-blocking by default. A reviewer may still mark a MEDIUM finding as blocking when it compounds with other findings or context makes it more urgent — state that reasoning explicitly when doing so.

### LOW
A minor issue, edge case with limited real-world impact, or small maintainability/readability concern. Non-blocking. Worth recording so it isn't lost, not worth holding up the change.

### INFO
An observation, style note, alternative-approach suggestion, or acknowledgment of something done well. Not a defect. Never blocking.

## Blocking Determination

- CRITICAL and HIGH findings are blocking by default.
- MEDIUM, LOW, and INFO findings are non-blocking by default.
- Any default may be overridden, but the override and its reasoning must be stated explicitly in the review output — never silently.

## Usage

Every Engineering Mentor review-type Skill must tag each finding with exactly one of these five levels and must not invent, rename, or substitute a different vocabulary. `context/standards/Code Review Standard.md`, `context/templates/Review Template.md`, and `skills/code-review/SKILL.md` all reference this file as their sole source of severity definitions — none of them redefines severity independently.
