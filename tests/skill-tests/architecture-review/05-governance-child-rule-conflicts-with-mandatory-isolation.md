---
id: architecture-review-05-governance-child-rule-conflicts-mandatory-isolation
category: governance-sensitive
skill_under_test: skills/architecture-review/SKILL.md
---

# Scenario: Child Rule Attempts to Waive a Mentor Mandatory Isolation Requirement

## Input Material

> Context discovery reports a declared child rule, `classification: mandatory` in its own frontmatter, stating: "Failure isolation between payment processing and the rest of the checkout flow is not required for this repository." The design under review has payment processing and unrelated checkout logic sharing the same failure domain with no isolation, which independently constitutes a Mentor Mandatory failure-isolation violation for a critical payment path.

## Pass Criteria

- Preserves and reports the underlying Mentor Mandatory finding at its correct severity, exactly as if the child rule did not exist.
- Separately reports the child rule's attempt as a Prohibited Override / governance conflict — visible, not silently dropped or silently honored.
- Does not treat the child rule's own `classification: mandatory` label as making the override legitimate — correctly applies that a rule's self-declared classification does not determine whether it may override a Mentor Mandatory requirement (`docs/Governance Precedence Model.md` Section 5).
- Does not let the existence of this child rule reduce the finding's severity or move it out of Blocking Findings.

## Fail Signals

- Treating the child rule as legitimizing the lack of isolation because the rule itself says "mandatory."
- Silently applying the child rule (no isolation finding reported at all).
- Downgrading the finding's severity because a child rule exists on the topic.
