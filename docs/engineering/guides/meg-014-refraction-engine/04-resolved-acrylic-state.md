<!--
File: docs/engineering/guides/meg-014-refraction-engine/04-resolved-acrylic-state.md
Document: MEG-014
Status: Draft
Version: 0.1
-->

# 04 — Resolved Acrylic State

---

# Purpose

The engine should produce one immutable `ResolvedAcrylicState` for each active Acrylic receiver and resolution cycle.

This is a logical client-internal contract rather than a network protocol.

---

# Logical Fields

| Group | Values |
|-------|--------|
| Identity | Receiver identity, Material profile and semantic priority. |
| Source | `sourceId`, `sourceRevision`, epoch and sequence. |
| Projection | Artwork UV transform and selected mip level. |
| Direct response | Relative colour, intensity, absorption and diffusion. |
| Backdrop | Sampling availability, blur, tint, displacement and opacity. |
| Parallax | Whole-surface depth response and internal optical offset. |
| Edge response | Per-boundary colour, strength, position and spread. |
| Secondary response | Bounded aggregate colour and intensity from related Acrylic. |
| Accessibility | Applied contrast, motion and translucency constraints. |
| Quality | Active techniques, update cadence and omitted refinements. |
| Timing | Source timestamp, transition progress and stable-state age. |

---

# Renderer Independence

Resolved state should describe behaviour rather than CSS properties, Dart objects or shader uniforms.

Renderer adapters may translate the same logical state into:

- CSS custom properties
- Flutter widget and paint values
- fragment-shader uniforms
- native compositor parameters

Renderer-specific state must not leak back into Runtime SDUI or `UVLightFrame`.

---

# Immutability

The renderer should receive a complete state snapshot.

It should not observe a partially updated combination of source, edge or parallax values.

When a resolution cycle is cancelled, the previous stable snapshot remains active.

---

# Minimum Acrylic Invariants

Every accepted state should preserve:

- visible material presence
- readable foreground content
- coherent artwork-derived colour
- restrained edge response
- bounded motion
- no invented energy

Backdrop distortion, secondary transport and fine parallax may be absent when capability or budget requires simplification.
