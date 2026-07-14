<!--
File: docs/engineering/guides/meg-002-event-driven-runtime/03-event-model.md
Document: MEG-002
Status: Draft
Version: 0.2
-->

# Event Model

> *Engineering should implement events as protocol contracts, not local message shapes.*

---

# Purpose

MEG-002 explains how engineers build an event-driven Runtime.

The authoritative event model is defined by **MIP-001 — Event Protocol**.

This chapter describes the engineering implications of that protocol.

---

# Engineering Guidance

Every published event should be implemented as an immutable fact that has already occurred.

Engineers should avoid using events as:

- commands
- mutable state snapshots
- transport-specific messages
- implementation callbacks

When a component needs to request work, model that request explicitly rather than disguising it as an event.

---

# Runtime Responsibility

The Runtime should preserve the event lifecycle described by MIP-001.

It should provide routing, delivery, tracing, replay and diagnostics without owning business meaning.

---

# Capability Responsibility

Capabilities own the business facts they publish.

They should use event names and payloads that reflect domain language rather than implementation details.

---

# Reference

Protocol authority is provided by:

- MIP-001 — Event Protocol
