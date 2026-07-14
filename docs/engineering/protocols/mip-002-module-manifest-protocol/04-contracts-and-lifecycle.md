<!--
File: docs/engineering/protocols/mip-002-module-manifest-protocol/04-contracts-and-lifecycle.md
Document: MIP-002
Status: Draft
Version: 0.1
-->

# 04 — Contracts And Lifecycle

---

# Provided Contracts

A module should declare the contracts it provides to the Platform or to other capabilities.

Examples include:

- capability contracts
- provider contracts
- event families
- diagnostic surfaces
- health surfaces

---

# Consumed Contracts

A module should declare the contracts it consumes.

This allows the Platform to validate whether required providers exist before activation.

---

# Lifecycle

The manifest should identify lifecycle expectations such as:

- discovery requirements
- activation requirements
- readiness conditions
- shutdown requirements
- health reporting

Lifecycle declarations help the Runtime coordinate modules consistently.
