<!--
File: docs/engineering/protocols/mip-002-module-manifest-protocol/02-identity-and-metadata.md
Document: MIP-002
Status: Draft
Version: 0.1
-->

# 02 — Identity And Metadata

---

# Identity

Every module must declare stable identity information.

At minimum, identity should include:

- module identifier
- display name
- module version
- manifest version
- provider or author

The identifier is the stable Platform reference.

The display name is presentation metadata.

---

# Metadata

Metadata should help humans and tooling understand the module without executing it.

Useful metadata includes:

- description
- supported Mosaic versions
- documentation references
- ownership information
- support contact

Metadata should not be used as an authority mechanism.

Permissions and contracts define authority.
