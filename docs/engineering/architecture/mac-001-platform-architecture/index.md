<!--
File: docs/engineering/architecture/mac-001-platform-architecture/index.md
Document: MAC-001
Status: Draft
Version: 0.1
-->

# MAC-001 — Platform Architecture

> *Mosaic is a platform before it is an application. The Platform provides stable execution, composition and governance so product capabilities can evolve independently.*

---

# Purpose

This canon defines the accepted architecture of the Mosaic Platform.

It establishes the architectural home for concepts that appear throughout the engineering guides:

- the Platform
- the Runtime
- capabilities
- modules
- contracts
- operational boundaries

Engineering guides explain how to realise this architecture. MAC-001 defines what the architecture is.

---

# Platform Statement

Within Mosaic:

> **The Platform owns execution, composition and governance. Capabilities own product behaviour.**

The Platform exists to keep Mosaic stable while allowing the product surface to grow.

It should not accumulate business behaviour simply because the behaviour is important. Important behaviour still belongs in capabilities or modules unless it is required for the Platform itself to operate.

---

# Scope

This canon defines durable architectural responsibilities.

It covers:

- Platform responsibility
- Runtime responsibility
- capability responsibility
- module participation
- architectural boundaries
- cross-document ownership

It does not define:

- implementation patterns
- Go package structure
- event schemas
- manifest schemas
- operational runbooks
- deployment procedures

Those concerns belong to MEG, MIP and MOP specifications.

---

# Relationship To Other Documents

MAC-001 is the authoritative home for Mosaic's platform architecture.

Related implementation and protocol documents include:

- MEG-002 — Event-Driven Runtime
- MEG-005 — Runtime Architecture
- MEG-006 — Module Platform
- MIP-001 — Event Protocol
- MIP-002 — Module Manifest Protocol
- MOP-001 — Observability Operations

When these documents need to explain platform ownership, they should reference MAC-001 rather than redefining it.
