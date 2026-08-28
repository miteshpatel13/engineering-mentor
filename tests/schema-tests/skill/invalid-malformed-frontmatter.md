# Invalid Malformed Frontmatter Fixture

This file has no `---`-delimited YAML frontmatter block at all -- it should
be reported as a single `E_MALFORMED_FRONTMATTER` error, with no further
section-presence checking attempted (there is no reliable body to check
once the frontmatter itself can't be located).
