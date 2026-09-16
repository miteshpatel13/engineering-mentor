---
id: third-party-integration-05-rule-coverage-oauth-token-refresh-lifecycle
category: rule-coverage
skill_under_test: skills/third-party-integration/SKILL.md
---

# Scenario: OAuth 2.0 Authorization Code Flow, PKCE, and Atomic Token Refresh

## Input Material

> Design an integration that allows users to connect their external CloudDrive account using OAuth 2.0. The integration needs to upload files in the background on behalf of the user when their access token expires every 60 minutes. Multiple background workers upload files simultaneously for the same user.

## Pass Criteria

- **Authorization Code with PKCE**: Designs the initial user connection flow using OAuth 2.0 Authorization Code grant with PKCE (`code_verifier` and `code_challenge`), validating the `state` parameter to prevent CSRF attacks.
- **Secure Token Storage**: Encrypts access and refresh tokens at rest in the database; excludes client secrets from frontend code.
- **Atomic Token Refresh & Concurrency Lock**: Implements a distributed lock or single-flight coordinator during token refresh so multiple concurrent upload workers do not attempt to redeem the same single-use refresh token at the same time.
- **Proactive Refresh**: Refreshes the access token before actual expiration (e.g., 5 minutes prior to `expires_in` timestamp) to avoid mid-operation 401 Unauthorized errors.
- **Revocation / Re-Auth Handling**: Gracefully handles permanent refresh failures (HTTP 400/401 invalid grant) by marking the connection as disconnected, alerting the user, and halting queued jobs.

## Fail Signals

- Storing plain client secrets or unencrypted refresh tokens in client applications or unencrypted database columns.
- Omitting PKCE or omitting the `state` parameter check in the OAuth callback.
- Allowing concurrent background workers to trigger simultaneous uncoordinated refresh token calls against the vendor.
- Silently retrying failed token refresh operations indefinitely when the user has revoked access.
