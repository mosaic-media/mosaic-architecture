<!--
File: docs/engineering/protocols/mip-002-module-manifest-protocol/01-manifest-model.md
Document: MIP-002
Status: Draft
Version: 0.1
-->

# 01 — Manifest Model

---

# Definition

A Module Manifest is a machine-readable declaration of what a module contributes to Mosaic.

It describes the module before the Platform loads executable code.

---

# Manifest Responsibilities

A manifest declares:

- identity
- metadata
- module version
- dependencies
- permissions
- configuration expectations
- provided contracts
- consumed contracts
- lifecycle requirements

These declarations allow the Platform to decide whether the module can participate safely.

---

# Manifest Rule

> **Discovery reads manifests. Activation executes code. The two steps must remain separate.**
