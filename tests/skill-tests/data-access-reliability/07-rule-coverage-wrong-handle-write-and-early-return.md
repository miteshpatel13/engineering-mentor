---
id: data-access-reliability-07-rule-coverage-wrong-handle-write-and-early-return
category: rule-coverage
skill_under_test: skills/data-access-reliability/SKILL.md
---

# Scenario: A Transaction With a Write on the Wrong Handle and an Unrolled-Back Early Return

## Input Material

> `updateCart` starts a transaction on a manual runner, loads the cart through `runner.manager`; if the cart is missing it `return { error: 'cart not found' }`; the `finally` block releases the runner. Later in the happy path it saves items through `runner.manager` and updates the cart total through `this.cartRepository.update(...)`, then commits.

## Pass Criteria

- Flags the early return that releases the runner with the transaction still open (Rules → Transaction Boundaries) and its consequence (open transaction or held locks returned to the pool).
- Flags the cart-total update as running on a different connection, outside the transaction and not atomic with the item saves.
- Recommends rollback before the early return (or a managed transaction helper) and routing the update through the transaction's handle.

## Fail Signals

- Accepting the `finally` release as sufficient.
- Missing that the two handles are different connections.
