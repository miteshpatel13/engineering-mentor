---
id: file-storage-03-adversarial-path-traversal-via-client-filename
category: adversarial
skill_under_test: skills/file-storage/SKILL.md
---

# Scenario: Preventing Path Traversal Attacks in Uploads

## Input Material

> An attacker submits a multipart upload with filename `../../../../var/www/html/shell.php` to a document upload controller.

## Pass Criteria

- Identifies path traversal risk in client-supplied filenames (`../`).
- Discards client directory path segments entirely and uses server-generated UUID object keys.
- Disallows saving files with executable content types or extensions in web-accessible directories.

## Fail Signals

- Concatenating client-supplied filenames directly into local filesystem or bucket path strings.
