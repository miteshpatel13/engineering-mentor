---
id: file-storage-04-failure-unguessable-url-as-only-authorization
category: failure
skill_under_test: skills/file-storage/SKILL.md
---

# Scenario: Relying on Unguessable URLs for Sensitive Document Security

## Input Material

> A developer serves private medical diagnostic reports at `https://cdn.example.com/reports/3f9a12b4-89c0-4d5e-a123-9876543210ab.pdf` via an unauthenticated public CDN, stating: "The 128-bit UUID in the URL is unguessable, so no authorization check is needed."

## Pass Criteria

- Rejects unguessable URLs as a substitute for explicit authorization checks on sensitive files.
- Mandates that private/sensitive documents be served through authenticated endpoints or short-lived presigned URLs after verifying user authorization (`skills/security-review/SKILL.md`).

## Fail Signals

- Serving private, sensitive, or regulatory documents via unauthenticated public URLs.
