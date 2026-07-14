<!--
File: docs/engineering/protocols/mip-001-event-protocol/05-compatibility.md
Document: MIP-001
Status: Draft
Version: 0.1
-->

# 05 — Compatibility

---

# Compatibility Goal

The Event Protocol exists so independently evolving capabilities can communicate safely.

A capability should be able to publish or consume events without knowing another capability's implementation.

---

# Compatibility Responsibilities

Publishers should:

- preserve event meaning
- version payload contracts deliberately
- document compatibility expectations
- avoid removing fields without migration

Subscribers should:

- tolerate unknown compatible fields
- validate required fields
- fail explicitly on unsupported versions
- avoid relying on Platform envelope internals beyond the published contract

---

# Protocol Rule

> **Events are contracts. Contracts evolve deliberately, never accidentally.**
