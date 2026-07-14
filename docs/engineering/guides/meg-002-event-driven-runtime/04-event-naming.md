<!--
File: docs/engineering/guides/meg-002-event-driven-runtime/04-event-naming.md
Document: MEG-002
Status: Draft
Version: 0.2
-->

# Event Naming

> *Event names are part of the protocol. Engineering practice should protect their meaning.*

---

# Purpose

MIP-001 defines the event naming protocol.

This chapter explains how engineers should apply that protocol while building capabilities.

---

# Engineering Guidance

Event names should describe completed business facts in the language of the publishing capability.

Preferred examples include:

```text
MediaImported
PlaybackStarted
MetadataUpdated
ModuleInstalled
```

Avoid names that describe handlers, transports, queues or implementation mechanics.

---

# Review Criteria

A new event name should be accepted only when it:

- describes a completed fact
- uses stable domain language
- avoids transport details
- remains meaningful to subscribers
- has a clear publisher owner

---

# Reference

Protocol authority is provided by:

- MIP-001 — Event Protocol
