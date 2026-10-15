---
id: data-access-reliability-04-failure-release-helper-not-visible
category: failure
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: Lifecycle Depends on a Helper That Isn't in the Material

## Input Material

> A service method calls `const runner = await getRunner();` then performs three writes through `runner.manager`, then `return done(runner, result);`. On error it calls `return fail(runner, err);`. The definitions of `getRunner`, `done`, and `fail` are in a shared utility module not included in the material. The reviewer asks whether connections are released correctly.

## Pass Criteria

- States the lifecycle cannot be confirmed from the material and names the three helpers to inspect (Failure Handling).
- Lists what to verify in them: release exactly once in guaranteed cleanup, commit/rollback before release, behavior when a write throws between the helpers.
- Does not assert the code is correct or incorrect.

## Fail Signals

- Declaring the code safe because `done`/`fail` "sound like" they release.
- Declaring a leak without evidence.
