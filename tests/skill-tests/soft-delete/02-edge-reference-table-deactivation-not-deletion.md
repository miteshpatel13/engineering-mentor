---
id: soft-delete-02-edge-reference-table-deactivation-not-deletion
category: edge
skill_under_test: skills/soft-delete/SKILL.md
---

# Scenario: Admin-Managed Reference List With an Active/Inactive Toggle

## Input Material

> A `product_categories` reference table has an admin-managed `isActive` toggle. Deactivated categories stay fully visible in historical order records and reports, and remain foreign-key-valid; they're excluded only from the "choose a category" picker when creating a new product. Someone asks whether this needs soft-delete's query-visibility-exclusion and conditional-uniqueness treatment.

## Pass Criteria

- Correctly identifies this as Deactivation, not soft-delete (Rules → Distinguishing Adjacent Lifecycle Concepts) — the record stays visible everywhere except the new-selection picker.
- Concludes this table does not need soft-delete's structural exclusion or conditional-uniqueness reasoning applied (Edge Cases) — a deactivated row is not "deleted" in this Skill's sense.
- Does not recommend adding an `IsDeleted`/`DeletedAt` pair to a table that already has the correct, distinct deactivation mechanism.

## Fail Signals

- Treating `isActive: false` as equivalent to soft-delete and recommending query-visibility exclusion be applied to it.
- Recommending a separate deletion flag be added "for consistency" with soft-deletable tables elsewhere in the schema.
