<!--
File: docs/engineering/protocols/mip-001-event-protocol/index.md
Document: MIP-001
Status: Draft
Version: 0.1
-->

# MIP-001 — Event Protocol

> *Events are the shared language of Mosaic. The Protocol keeps that language stable as capabilities evolve independently.*

---

# Purpose

MIP-001 defines the canonical event contract used by Mosaic capabilities, modules, Runtime Services and observability tooling.

MEG-002 explains how engineers build event-driven behaviour.

MIP-001 defines the protocol those implementations must preserve.

---

# Protocol Statement

Within Mosaic:

> **Every event consists of an immutable Platform envelope surrounding an immutable business payload.**

The Platform owns the envelope.

Capabilities own the payload.

---

# Scope

This protocol defines:

- event model
- event envelope
- naming rules
- versioning rules
- compatibility expectations

It does not define:

- subscriber implementation
- event bus internals
- retry strategy
- storage implementation
- business payload schemas for individual domains
