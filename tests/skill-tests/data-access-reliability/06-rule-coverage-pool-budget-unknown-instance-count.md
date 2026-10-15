---
id: data-access-reliability-06-rule-coverage-pool-budget-unknown-instance-count
category: rule-coverage
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: Sizing a Pool Without Knowing the Instance Count

## Input Material

> An application creates two database pools per process — one through the web framework's ORM module and one legacy data source initialized at startup — each with a limit of 30. The database allows 305 connections. The team asks: "What should the pool size be?" The material does not say how many instances run at peak or during deploys.

## Pass Criteria

- Flags the two pools per process as doubling demand and recommends one shared pool with a startup assertion (Rules → Pool Budget and Fail-Fast).
- States the budget as a formula — pools per process × processes per instance × peak instances including deploy surge ≤ ~80% of (305 minus an admin reserve) — and that the instance count is unknown, so no final number can be given (Constraints: never invent).
- Recommends a configuration-driven, validated pool size, a bounded wait queue that fails fast with a retryable response, and pool metrics to measure real usage.

## Fail Signals

- Stating a definitive pool size or instance count as fact.
- Ignoring the second pool.
