<!--
File: docs/engineering/architecture/mac-001-platform-architecture/02-runtime-boundary.md
Document: MAC-001
Status: Draft
Version: 0.1
-->

# 02 — Runtime Boundary

---

# Purpose

The Runtime is the execution environment of the Platform.

It coordinates work, lifecycle and resources without becoming responsible for business decisions.

---

# Runtime Responsibilities

The Runtime owns:

- startup
- shutdown
- Runtime Service lifecycle
- worker coordination
- scheduling admission
- dependency graph management
- execution orchestration
- Runtime State
- diagnostic visibility

These responsibilities describe how the Platform operates.

---

# Runtime Non-Responsibilities

The Runtime does not own:

- media semantics
- user decisions
- recommendation logic
- metadata interpretation
- presentation decisions
- business state

Those responsibilities belong to capabilities.

---

# Runtime State

Runtime State describes the execution environment.

Examples include:

- registered capabilities
- service lifecycle
- queue depth
- worker allocation
- dependency status
- health state

Runtime State must not become business state.

---

# Boundary Rule

> **The Runtime knows how Mosaic is operating. Capabilities know what Mosaic is doing.**

This separation keeps the Platform observable and replaceable without diluting business ownership.
