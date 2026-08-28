---
id: skill-creator-01-normal-domain-pattern-draft
category: happy-path
skill_under_test: skills/skill-creator/SKILL.md
---

# Scenario: Drafting a Clean Domain Pattern Skill

## Input Material

> A migration plan designates a candidate named `identifier-strategy` as NEW, `skillType: Domain Pattern`, `category: Domain Patterns`, sourced from an audited skill about using opaque public identifiers (e.g. UUIDs) instead of exposing internal database primary keys. The source material is entirely general principle — no project-specific facts. Draft the Skill.

## Pass Criteria

- The response walks through overlap checking, `skillType`/`category` classification, Required Context posture, and governance posture before producing section content — not straight to prose.
- `skillType: Domain Pattern` and `category: Domain Patterns` are both confirmed against Taxonomy definitions, not merely repeated from the prompt uncritically.
- Required Context posture is stated explicitly (posture 1 or 2, with reasoning) per `docs/Skill Standard.md` Section 3.
- Governance posture is addressed: the response either cites a real Standard for any Mandatory-sounding claim, or explicitly states the guidance is Advisory/Configurable.
- `Related Skills` entries, if any are proposed, are labeled Dependency or Related with a stated reason, not left unlabeled.

## Fail Signals

- Skipping straight to drafting prose without stating the classification/overlap reasoning.
- Asserting a Mandatory governance tier without citing an existing Standard.
- Treating a plausible related Skill as a "Dependency" without applying the true-dependency test from `docs/Skill Migration & Expansion Plan.md` Section 10.
