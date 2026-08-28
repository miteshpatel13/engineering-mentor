---
id: file-storage-05-rule-coverage-storage-provider-adapter
category: rule-coverage
skill_under_test: skills/file-storage/SKILL.md
---

# Scenario: Abstracting Cloud Storage Driver Behind Generic Interfaces

## Input Material

> A document service directly instantiates `AWS.S3()` and calls `.putObject()` inside its business logic method.

## Pass Criteria

- Rejects direct cloud vendor SDK instantiation inside core domain services.
- Mandates isolating storage drivers behind a generic `StorageService` interface (`LocalStorageAdapter`, `S3StorageAdapter`).

## Fail Signals

- Coupling application domain services directly to vendor storage SDKs.
