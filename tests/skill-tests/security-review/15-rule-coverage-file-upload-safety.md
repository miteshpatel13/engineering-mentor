---
id: security-review-15-rule-coverage-file-upload-safety
category: rule-coverage
skill_under_test: skills/security-review/SKILL.md
---

# Scenario: File-Upload Endpoint Trusts Client-Supplied Filename and Content-Type

## Input Material

> An avatar-upload endpoint accepts a multipart file upload, reads the client-supplied `filename` and `Content-Type` header, and writes the file directly to `/var/www/uploads/<filename>` using the client-supplied name verbatim, with no server-side check of the file's actual content, no filename sanitization, no allow-list of extensions, and no maximum file size enforced. `/var/www/uploads/` is served directly by the web server as static content.

## Pass Criteria

- Flags the missing server-side content verification (trusting client-declared `Content-Type`/filename extension alone) per Rules → File-Upload Safety.
- Flags the use of the client-supplied filename directly in a file-system path with no path-traversal sanitization.
- Flags storage inside the web-served root with no configuration preventing execution of an uploaded file.
- Flags the absence of an enforced maximum file size.
- Names the category as File-Upload Safety in the finding.

## Fail Signals

- Treating the endpoint as safe because it "checks Content-Type" without noting that a client-declared header is not verification of actual content.
- Missing the path-traversal risk from using the raw client filename in a file-system path.
