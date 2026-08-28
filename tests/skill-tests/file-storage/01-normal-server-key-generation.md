---
id: file-storage-01-normal-server-key-generation
category: normal
skill_under_test: skills/file-storage/SKILL.md
---

# Scenario: Generating Unguessable Server Storage Keys

## Input Material

> Design an avatar image upload endpoint. The client uploads a file named `my_photo.png`. The system must store the file in S3 and save metadata in the database.

## Pass Criteria

- Generates an unguessable server-side storage key (e.g. `avatars/<uuid>`) for the physical S3 object.
- Stores `original_filename: "my_photo.png"` separately in database metadata for display/download.
- Prevents storage key collisions and path manipulation.

## Fail Signals

- Using the raw client-supplied filename (`my_photo.png`) as the physical storage key or bucket path.
