<!--
File: docs/engineering/guides/meg-014-refraction-engine/02-source-and-inputs.md
Document: MEG-014
Status: Draft
Version: 0.1
-->

# 02 — Source And Inputs

---

# Primary Source Selection

The engine should select exactly one logical primary artwork source.

```text
if Focus references artwork:
    source = focused artwork
else:
    source = Hero artwork
```

When neither source exists, the engine should resolve neutral Acrylic without an artwork-light contribution.

A Focus transition should blend from the previous stable field to the new field rather than clear Acrylic state immediately.

The blend remains a transition between sources, not a permanent multi-source lighting model.

---

# Engine Inputs

| Input | Responsibility |
|-------|----------------|
| Material identity | Selects the governed Acrylic profile. |
| Focus and Hero state | Selects the primary artwork source. |
| `UVLightField` | Supplies temporally reconstructed relative radiance. |
| Surface transform | Supplies `x`, `y`, `z`, scale and orientation. |
| Surface bounds and mask | Defines the two-dimensional Acrylic region. |
| Z-order and opaque masks | Defines local backdrop and occlusion relationships. |
| Apparent thickness | Governs diffusion, displacement, edge response and optical parallax. |
| Runtime Atmosphere | Constrains source influence. |
| Accessibility | Constrains motion, translucency, contrast and distortion. |
| Renderer Capability Profile | Describes available techniques and measured cost. |
| Dynamic Material Budget | Limits work safe for the current frame. |

---

# Backdrop Input

The engine should treat visible Presentation behind Acrylic as a receiver-local input.

Backdrop sampling provides:

- local colour continuity
- translucency
- diffusion
- bounded displacement
- internal parallax

It does not replace or modify `UVLightField`.

A renderer that cannot sample the actual backdrop should preserve Acrylic identity using a stable tint, diffusion approximation and artwork-derived edge response.

---

# Source Transition State

A source transition should retain:

- previous field identity
- next field identity
- transition progress
- last stable resolved state

The engine should cancel obsolete intermediate analysis when Focus moves again and transition toward the latest useful source.
