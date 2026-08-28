---
id: architecture-review-08-governance-advisory-no-conflict-module-layout
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Child Advisory Module-Layout Preference Diverges From Generic Guidance Without a Mandatory Conflict

## Input Material

> Context discovery reports a declared Child Advisory rule: "Prefer a feature-based module layout (one directory per business capability) over a layer-based layout (controllers/services/models directories) for this project." The design under review organizes new code by feature directory, consistent with the child's stated preference, with clean boundaries and no cross-feature coupling issues.

## Pass Criteria

- Recognizes the feature-based layout as the project's stated, legitimate Advisory-level convention rather than a defect — no Mentor Mandatory requirement concerns this specific organizational style.
- Does not report a layout finding or governance conflict merely because a generic (unstated) preference for layer-based organization might otherwise exist.
- Does not manufacture a governance-conflict callout when the rule and the material fully agree.

## Fail Signals

- Flagging the feature-based layout as inconsistent with "standard" practice, ignoring the project's own stated convention.
- Treating agreement between the rule and the material as itself needing a conflict note.
