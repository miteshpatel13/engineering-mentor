---
category: failure
id: validation-04-failure-relying-on-frontend-validation-only
skill_under_test: skills/validation/SKILL.md
---

# Scenario: Omitting Backend Validation Due to Frontend UI Checks

## Input Material

> A developer omits backend email and password strength validation on a sign-up controller, stating: "The React frontend form already validates email format and password strength before enabling the Submit button."

## Pass Criteria

- Rejects omitting backend validation as a violation of backend safety.
- Re-asserts the core principle: "Never trust client-side validation."
- Mandates full structural and business-rule validation on the backend regardless of UI checks.

## Fail Signals

- Accepting frontend validation as a substitute for backend DTO/service validation.
