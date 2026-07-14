<!--
File: docs/engineering/architecture/mac-001-platform-architecture/04-module-model.md
Document: MAC-001
Status: Draft
Version: 0.1
-->

# 04 — Module Model

---

# Purpose

Modules are the delivery mechanism through which Mosaic can add or replace capabilities without modifying the Runtime.

Modules are not a separate execution model.

They participate in the same Platform architecture as every other capability.

---

# Definition

A module is a package of capability contribution.

It may provide:

- one capability
- multiple related capabilities
- adapters
- providers
- configuration
- contracts
- operational metadata

The Platform admits modules through manifest-driven discovery and validation.

---

# Module Responsibilities

Modules own the implementation they contribute.

They must declare:

- identity
- version
- dependencies
- permissions
- provided contracts
- consumed contracts
- lifecycle expectations

These declarations belong to MIP-002.

---

# Platform Responsibilities

The Platform owns module admission.

It decides whether a module can participate by validating:

- manifest structure
- dependency availability
- permission requests
- compatibility
- lifecycle requirements

A module is not trusted merely because it exists on disk.

---

# Module Rule

> **Modules extend Mosaic by declaring capability, not by modifying the Platform.**

This rule protects Platform stability while allowing the ecosystem to grow.
