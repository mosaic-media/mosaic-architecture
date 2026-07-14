<!--
File: docs/engineering/protocols/mip-001-event-protocol/01-event-model.md
Document: MIP-001
Status: Draft
Version: 0.1
-->

# 01 — Event Model

---

# Definition

An event is an immutable record of a fact that has already occurred.

An event answers:

> **What happened?**

It does not request work, describe intent or represent mutable state.

---

# Event Lifecycle

Events follow a simple lifecycle:

```text
State Changes
↓
Event Created
↓
Event Published
↓
Event Observed
↓
Event Retained
```

Each stage preserves history rather than rewriting it.

---

# Event Ownership

The publishing capability owns the business meaning of an event.

The Platform owns routing, delivery, tracing and compatibility metadata.

Subscribers should treat events as historical facts and publish new events when new facts occur.
