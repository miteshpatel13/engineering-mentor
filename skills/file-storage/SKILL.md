---
name: file-storage
description: The general engineering pattern for secure file storage architecture — generic file registry, storage provider adapter isolation, server-side key generation, content-based MIME validation, and authorization-gated access control. Reference material consumed by security-review and architecture-review.
category: Domain Patterns
skillType: Domain Pattern
---

# File Storage

## Purpose

Produce the shared, reusable reference pattern for file storage and asset management backend architectures. This exists as its own Skill because file storage spans security (`security-review`), architecture provider abstraction (`architecture-review`), and data integrity — requiring server-side key generation, content-sniffed MIME validation, size caps, and strict public vs private access control.

## Scope

**In scope:** unified generic file registry modeling, storage provider adapter abstraction (local disk, AWS S3, Google Cloud Storage), content-based magic-byte MIME validation, server-side storage path/key generation (preventing path traversal), public vs private authorization access gating, and presigned URL access mechanisms.

**Out of scope:** configuring specific cloud bucket permissions or IAM roles; client-side image cropping or canvas rendering libraries. This Skill teaches the backend file storage pattern.

## When to Use

Use when:
- Designing file upload or document management endpoints.
- Integrating or swapping underlying cloud object storage providers.
- Defining file validation rules (MIME types, size limits, allowed extensions).
- Implementing access control for sensitive or private uploaded files.
- Reviewing file upload handling for path traversal or remote code execution vulnerabilities.

Do not use for database BLOB storage of structured application data.

## Required Context

**Posture 2 — benefits from repository context but degrades gracefully without it** (`docs/Skill Standard.md` Section 3). Core principles (server-generated storage keys, byte-sniffed MIME validation, provider abstraction, authorization checks on private files) apply across all storage drivers and backend frameworks.

## Workflow

1. **Model Generic File Registry:** Maintain a single, generic `File` entity (carrying `id`, `uuid`, `purpose`, `storage_key`, `original_filename`, `mime_type`, `byte_size`) referenced via foreign keys from domain entities, avoiding separate file tables per domain.
2. **Abstract Storage Provider:** Encapsulate storage drivers (local disk, S3, GCS) behind a generic `StorageService` adapter interface.
3. **Validate File Uploads Server-Side:** Validate file size caps and verify MIME types by inspecting initial byte magic numbers rather than trusting client-provided `Content-Type` headers or file extensions.
4. **Generate Storage Keys Server-Side:** Assign unguessable, server-generated storage keys (e.g. using `FileUUID`) for object paths. Never use raw client-supplied filenames directly in filesystem or bucket object keys.
5. **Enforce Access Control by Purpose:** Differentiate public assets (served via public CDN/URLs) from private files (served via authenticated endpoints or short-lived presigned URLs after authorization checks).
6. **Apply Soft Deletion for Metadata:** Soft-delete file metadata records to preserve referential integrity for historical views. Physical object deletion occurs via decoupled, asynchronous cleanup processes.

## Rules

### Unified Generic File Registry

Avoid creating entity-specific file storage tables (e.g. `UserAvatars`, `EventBanners`). Model a unified `File` metadata table with a `file_purpose` discriminator (e.g. `AVATAR`, `DOCUMENT`, `BANNER`, `SIGNATURE`). Domain entities store a foreign key referencing the `File` record.

### Storage Provider Adapter Abstraction

All object storage operations (upload, stream, delete, generate presigned URL) must pass through a generic `StorageService` interface. Application logic must never make direct calls to provider-specific SDKs (e.g. AWS S3 SDK, Google Cloud Storage SDK) outside dedicated adapter classes (`S3StorageAdapter`, `LocalStorageAdapter`).

### Server-Side Content-Based MIME Validation

Client-submitted `Content-Type` headers and file extensions are untrusted user input. The backend must inspect the initial file byte sequence (magic numbers) to verify the genuine file type before accepting or storing an upload. Disallow executable file types (e.g. `.php`, `.exe`, `.sh`, `.jsp`) outright.

### Server-Generated Storage Keys (No Path Traversal)

Storage object keys and file paths must be generated server-side using opaque identifiers (e.g. `files/avatars/<uuid>`). Never use the client-supplied `original_name` as a path component, as this exposes the system to path traversal attacks (e.g. `../../etc/passwd`) and filename collisions. Store the original filename in metadata for display or `Content-Disposition` header generation during download.

### Strict Access Control Gating (Opacity $\neq$ Authorization)

Access to uploaded files must match their intended privacy level:
- **Public Files:** (e.g. public banners, marketing assets) May be served directly via public bucket URLs or CDNs.
- **Private / Sensitive Files:** (e.g. ID documents, signatures, tax invoices, medical records) Must be served through authenticated, authorization-checked API endpoints or short-lived, signed URLs. An unguessable UUID storage path is a defense-in-depth mitigation, **not a substitute** for an explicit authorization check (`skills/security-review/SKILL.md`).

### Soft-Delete & Deferred Cleanup

Soft-deleting a domain entity or file record must not trigger an immediate, synchronous hard-deletion of the underlying physical cloud object. Retain physical storage objects until asynchronous, verified purge processes confirm no historical data references remain (`skills/soft-delete/SKILL.md`).

## Constraints

- Never use client-supplied filenames or paths as physical storage object keys.
- Do not trust client-asserted `Content-Type` headers or file extensions for file type validation.
- Never serve private, sensitive, or regulatory files via unauthenticated public URLs.
- Do not couple business logic directly to cloud vendor storage SDKs.

## Governance Integration

This Skill supplies reference material (Domain Pattern) per `docs/Skill Taxonomy.md` Section 2.

- **Mentor Advisory:** Rules in this Skill represent strongly recommended Advisory-tier standards for system security and storage architecture grounded in `context/standards/Security Standards.md` and `context/standards/Architecture Standards.md`.
- **Child Rules:** Child rules in `.mentor/rules/` may specify allowed file extensions, maximum file size limits, or primary cloud storage providers.

## Validation

This Skill is validated during design and review when:
- Upload endpoints inspect file byte magic numbers for MIME verification.
- Storage keys are generated using UUIDs rather than client filenames.
- Storage operations use generic `StorageService` interfaces.
- Private assets enforce authorization checks prior to streaming or presigning URLs.

## Edge Cases

- **Presigned Upload URLs:** Direct client-to-cloud bucket uploads using presigned URLs require the backend to issue the presigned URL with pre-validated file size caps and expected MIME conditions.
- **Serving Download Filenames:** When serving files with original names, set `Content-Disposition: attachment; filename="<original_name>"` with proper header encoding to prevent HTTP header injection.

## Failure Handling

When storage provider credentials or file validation rules cannot be established from provided code, report Insufficient Evidence regarding file security, per the Mentor Operating Model No Invention Rule.

## Expected Output

Reference material. Consuming Review Skills (`security-review`, `architecture-review`) format review findings using `context/templates/Review Template.md`.

## Examples

### Positive Example: Server Key Generation and Byte Validation
```typescript
// Secure file upload handler
async uploadFile(fileBuffer: Buffer, rawFilename: string, purpose: FilePurpose, user: User): Promise<FileRecord> {
  // 1. Content-based MIME validation via magic bytes
  const mimeType = await detectMimeTypeFromBytes(fileBuffer);
  if (!ALLOWED_MIME_TYPES[purpose].includes(mimeType)) {
    throw new BadRequestException('Invalid or unallowed file content format');
  }

  // 2. Server-generated unguessable storage key (no path traversal)
  const fileUuid = crypto.randomUUID();
  const storageKey = `storage/${purpose.toLowerCase()}/${fileUuid}`;

  // 3. Save via abstracted storage adapter
  await this.storageService.putObject(storageKey, fileBuffer, mimeType);

  // 4. Record metadata
  return this.fileRepo.create({
    uuid: fileUuid,
    purpose,
    storageKey,
    originalName: sanitizeFilename(rawFilename),
    mimeType,
    ownerId: user.id
  });
}
```

### Negative Example: Path Traversal and Untrusted MIME Header
```typescript
// BAD: Trusting client filename and Content-Type header directly!
app.post('/upload', async (req, res) => {
  const clientFilename = req.files.file.name; // DEFECT: Path traversal risk! e.g. "../../sh"
  const clientMime = req.headers['content-type']; // DEFECT: Easily spoofed!
  
  // Directly writing file to disk using client name
  fs.writeFileSync(`/var/www/uploads/${clientFilename}`, req.files.file.data);
  res.send({ status: 'uploaded' });
});
```

## Related Skills

- `skills/security-review/SKILL.md` — Related: Evaluates file upload security defenses, path traversal, RCE prevention, and authorization checks.
- `skills/architecture-review/SKILL.md` — Related: Evaluates storage provider abstraction and decoupled storage architecture.
- `skills/soft-delete/SKILL.md` — Related: Governs soft-delete retention and object cleanup behavior.
