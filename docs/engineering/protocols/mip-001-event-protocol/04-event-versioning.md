<!--
File: docs/engineering/protocols/mip-001-event-protocol/04-event-versioning.md
Document: MIP-001
Status: Draft
Version: 0.1
-->

# 04 — Event Versioning

---

# Purpose

Event versions communicate payload compatibility.

They do not describe implementation progress.

---

# Version Ownership

Publishers own event versioning.

Subscribers own defensive consumption.

The Platform coordinates compatibility by preserving envelope metadata and making version information visible to routing, diagnostics and tooling.

---

# Compatibility

Compatible changes may evolve the payload without breaking existing subscribers.

Breaking semantic changes should use a new version and a deliberate migration path.

The event name describes the fact.

The event version describes how to interpret the payload contract.
