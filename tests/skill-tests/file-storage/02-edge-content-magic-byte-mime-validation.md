---
id: file-storage-02-edge-content-magic-byte-mime-validation
category: edge
skill_under_test: skills/file-storage/SKILL.md
---

# Scenario: Validating File MIME Type via Magic Byte Inspection

## Input Material

> An application accepts profile image uploads (`.png`, `.jpg`). A user uploads a malicious PHP script renamed to `avatar.png` with a `Content-Type: image/png` header.

## Pass Criteria

- Inspects the initial byte sequence (magic numbers) of the file content buffer.
- Detects that the byte content is not a valid PNG image and rejects the upload with `400 Bad Request`.
- Explicitly ignores untrusted client `Content-Type` headers and file extensions.

## Fail Signals

- Trusting the client `Content-Type` header or filename extension for file type verification.
