<!--
File: docs/engineering/architecture/mac-001-platform-architecture/03-capability-model.md
Document: MAC-001
Status: Draft
Version: 0.1
-->

# 03 — Capability Model

---

# Purpose

Capabilities are the units of product behaviour that run on the Mosaic Platform.

The Platform discovers, hosts and governs capabilities. It does not need to understand their internal behaviour.

---

# Definition

A capability is a self-contained unit of Mosaic behaviour.

A capability may be:

- built into the initial Platform distribution
- delivered as a first-party module
- delivered as a third-party module
- enabled
- disabled
- upgraded
- removed

The delivery mechanism does not change how the capability participates in the Platform.

---

# Capability Responsibilities

Capabilities own:

- business behaviour
- domain rules
- product workflows
- emitted business events
- consumed business events
- user-facing outcomes

Capabilities should express their needs through Platform contracts rather than direct implementation dependencies.

---

# Platform Responsibilities

The Platform owns the common services capabilities depend upon:

- registration
- dependency validation
- execution
- scheduling
- permissions
- lifecycle
- diagnostics

The Platform should treat built-in and module-delivered capabilities consistently.

---

# Capability Rule

> **A capability is defined by the behaviour it contributes, not by where it is delivered from.**

This keeps first-party and third-party evolution aligned with the same architectural model.
