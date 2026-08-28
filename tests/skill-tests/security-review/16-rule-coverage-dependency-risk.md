---
id: security-review-16-rule-coverage-dependency-risk
category: rule-coverage
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: Dependency With a Known CVE, Reachability Established vs. Not Established

## Input Material

> The material lists two dependencies. Dependency A has a known CVE for unsafe deserialization, and the code under review directly calls that library's vulnerable deserialization function on data read from an untrusted, user-controlled request body. Dependency B has a known CVE in an admin-CLI feature of the same package, and the material shows the application only ever imports and uses that package's unrelated string-formatting utility, with no code path reaching the vulnerable CLI feature.

## Pass Criteria

- Flags Dependency A as a Dependency Risk finding at a severity reflecting real exposure, explicitly stating that the vulnerable path is reachable from untrusted input.
- Does not flag Dependency B as a Severity-tagged Dependency Risk finding — states explicitly, per Rules → Dependency Risk and Edge Cases, that having a CVE is not itself sufficient without evidence the vulnerable path is reachable in this codebase's actual usage.
- Keeps the two dependencies' treatment visibly distinct rather than applying the same conclusion to both because both "have a CVE."

## Fail Signals

- Flagging both dependencies identically merely because both have a known CVE, without distinguishing reachability.
- Failing to flag Dependency A despite the material directly showing the vulnerable path is reached from untrusted input.
