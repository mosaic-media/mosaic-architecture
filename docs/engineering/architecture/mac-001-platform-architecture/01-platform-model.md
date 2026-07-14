<!--
File: docs/engineering/architecture/mac-001-platform-architecture/01-platform-model.md
Document: MAC-001
Status: Draft
Version: 0.1
-->

# 01 — Platform Model

---

# Purpose

The Platform is the stable architectural foundation on which Mosaic capabilities execute.

It provides the environment in which independently evolving capabilities can be discovered, composed, executed, observed and governed.

---

# Definition

Within Mosaic, the Platform is the combination of:

- Runtime
- capability registry
- module admission
- execution services
- scheduling services
- resource ownership
- observability surfaces
- security and permission enforcement

The Platform does not own product behaviour.

---

# Platform Responsibilities

The Platform owns responsibilities that must remain consistent across all capabilities.

These include:

- execution
- lifecycle
- dependency composition
- scheduling
- capability discovery
- module admission
- operational visibility
- fault isolation
- permission enforcement

These responsibilities are architectural infrastructure.

They allow capabilities to focus on behaviour rather than hosting themselves.

---

# Product Responsibilities

Product behaviour belongs outside the Platform.

Examples include:

- playback
- libraries
- metadata
- recommendations
- user workflows
- media-specific behaviour

These behaviours may be delivered by first-party modules, third-party modules or built-in capabilities.

They should still execute through the same Platform model.

---

# Architectural Rule

> **The Platform becomes stronger by standardising how capabilities run, not by absorbing what capabilities do.**

This rule prevents Mosaic from becoming a monolith as new product areas are added.
