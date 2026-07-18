<!--
File: docs/engineering/documentation/index.md
Document: Documentation
Status: Draft
-->

# Documentation

Documentation guides define how Mosaic architecture documentation is created, reviewed, organised, and maintained.

## Documentation Guides in Brief

| Specification | In one sentence |
|---------------|-----------------|
| [MDG-001 — Documentation Authority Guide](mdg-001-documentation-authority-guide/index.md) | Governs document types, lifecycle, writing, decisions, references, organisation, review and maintenance. |

Read [MDG-001 — Documentation Authority Guide](mdg-001-documentation-authority-guide/index.md) before creating, splitting, renaming, reorganising or materially editing specifications. Its rules take precedence over convenience or local convention.

Its rules are enforced rather than trusted. `scripts/validate_docs.py` checks metadata, chapter ordering, cross-references and generated artefacts against [MDG-001 — Documentation Authority Guide](mdg-001-documentation-authority-guide/index.md) on every pull request, and `validate_docs.py --rules` lists each rule with the requirement it enforces.

New specifications are scaffolded from the templates in `templates/`, which are the machine-readable form of the standard, using `scripts/new_doc.py`. Each template's chapters correspond one-to-one with its type definition in [02 — Document Types](mdg-001-documentation-authority-guide/02-document-types.md).

Each Mosaic document type is a branded profile of an established open standard, recorded in [10 — Standards Mapping](mdg-001-documentation-authority-guide/10-standards-mapping.md): decisions follow ADR, proposals follow the RFC and PEP process, normative language follows RFC 2119, and revision histories follow Keep a Changelog.

The linked MDG specification is authoritative; this page is an entry point only.
