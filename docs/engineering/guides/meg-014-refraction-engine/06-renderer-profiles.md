<!--
File: docs/engineering/guides/meg-014-refraction-engine/06-renderer-profiles.md
Document: MEG-014
Status: Draft
Version: 0.1
-->

# 06 — Renderer Profiles

---

# Selection Principle

Renderer paths should be selected from measured cost and available frame headroom.

They must not be assigned permanently by browser, television, mobile or device category.

---

# Web Profiles

| Profile | Techniques | Intended role |
|---------|------------|---------------|
| Basic CSS | Tint, gradients, borders, opacity and transforms. | Minimum stable Acrylic identity. |
| CSS Composite | Pseudo-elements, masks, blend modes and limited backdrop filters. | Default web path. |
| Two-Dimensional Shader | WebGL2 or equivalent fragment processing over rectangular surfaces. | Consolidated or enhanced dynamic response. |
| WebGPU | Optional two-dimensional compute or fragment path. | Use only when measured benefit justifies it. |

TypeScript should decode source data, resolve spatial state and set renderer inputs.

CSS may remain responsible for all visible painting in Basic CSS and CSS Composite profiles.

Example adapter output:

```css
--acrylic-light-r: 0.72;
--acrylic-light-g: 0.31;
--acrylic-light-b: 0.18;
--acrylic-light-strength: 0.64;
--acrylic-parallax-x: -1.2px;
--acrylic-parallax-y: 0.8px;
--acrylic-edge-top: 0.18;
--acrylic-edge-right: 0.73;
```

---

# Flutter Profiles

| Profile | Techniques | Intended role |
|---------|------------|---------------|
| Flutter Composite | `Stack`, `Transform`, clipping, gradients, backdrop filters and `CustomPainter`. | Default native path. |
| Flutter Fragment | `FragmentProgram` over two-dimensional surfaces. | Enhanced fidelity or pass consolidation. |

Flutter adapters may unpack canonical RGBA source data into renderer-friendly textures when necessary.

Peak luminance must not accidentally become visual transparency.

---

# Profile Switching

The engine should preserve `ResolvedAcrylicState` semantics when switching profiles.

It should avoid switching repeatedly near a performance threshold.

Quality should reduce quickly under pressure and recover only after sustained headroom.

---

# Unsupported Features

When a technique is unavailable or too expensive, the renderer should omit it explicitly rather than emulate it with unbounded main-thread work.

Fallback order should preserve:

1. Material presence and readability
2. direct artwork-derived colour
3. directional edge response
4. bounded optical parallax
5. backdrop refinement
6. secondary transport
