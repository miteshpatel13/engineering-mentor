---
id: codebase-orientation-01-normal-footprint-with-graft
category: normal
skill_under_test: skills/codebase-orientation/SKILL.md
---

# Scenario: Footprint for a schema change with Graft available

## Input Material

> "Before we plan it: we want to split `users.name` into `first_name` and `last_name`." `graft/` exists and Graft reports the graph fresh. Graft caller/grep results show `users.name` read by `accounts/serializers.py`, `billing/invoice_pdf.py`, and a SQL view `reporting.v_customers`.

## Pass Criteria

- Lists affected modules, the column's readers and writers (including the SQL view), related APIs that expose `name`, and existing tests.
- States Graft as the source and its freshness, and verifies the view dependency against source before relying on it.
- Names unknowns (for example external API clients reading `name`) as risks for the plan.

## Fail Signals

- Omitting the SQL view or other non-code consumers.
- Presenting Graft summaries as verified fact without checking source.
