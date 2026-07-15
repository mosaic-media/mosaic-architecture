<!--
File: docs/engineering/guides/meg-014-refraction-engine/03-surface-and-spatial-resolution.md
Document: MEG-014
Status: Draft
Version: 0.1
-->

# 03 — Surface And Spatial Resolution

---

# Surface Model

Each Acrylic receiver should expose:

| Value | Meaning |
|-------|---------|
| Stable identity | Cache and diagnostics key. |
| Projected bounds | Two-dimensional receiver extent. |
| Mask | Rounded rectangle, path or alpha mask. |
| Transform | Position, scale and orientation in Composition Space. |
| Z-order | Backdrop, occlusion and ordering relationship. |
| Material profile | Apparent thickness, diffusion and response limits. |
| Semantic priority | Hero, supporting or overlay importance. |

---

# Artwork Projection

The engine should derive a two-dimensional mapping from receiver coordinates to artwork UV coordinates using the artwork and receiver transforms.

The `UVLightFrame` remains anchored in normalised artwork UV space.

An Acrylic receiver acts as a moving sampling window over that stable field as its Composition transform changes.

Moving or scrolling Acrylic must not regenerate or reposition the source frame solely to preserve visual alignment.

The mapping may be affine for ordinary surfaces.

Perspective-aware renderers may use a projective mapping when Composition projection requires it.

The engine should sample a lower `UVLightFrame` mip when the projected receiver footprint or available budget does not justify the base level.

---

# Static Brand Field Projection

When meaningful artwork is absent, the engine should generate a procedural field from the active Brand Illumination Pair and Static Brand Emitter.

The field remains anchored to the Composition Space parent rather than to artwork UV space.

An Acrylic receiver acts as a moving sampling window over that stable field as the page scrolls, Focus changes or Composition elements move.

Receiver movement must not regenerate or reposition the field.

The engine should invalidate and rebuild the cached field only when one of these inputs changes:

- Brand Illumination Pair
- Static Brand Emitter position
- appearance mode
- Composition Space parent dimensions

The generated field is a client-internal runtime resource.

It does not become a `.mos` resource or a [MIP-003 — UVLightFrame Protocol](../../protocols/mip-003-uv-light-frame-protocol/index.md) interchange payload.

---

# Occlusion

Opaque surfaces should occlude hidden artwork transport according to projected bounds, masks and z-order.

An implementation may use:

- mask overlap tests
- clipped coverage maps
- coarse occlusion tiles
- renderer-native clipping information

It should avoid general-purpose mesh occlusion.

---

# Acrylic Proximity Transport

Projected overlap is not required for secondary Acrylic influence.

The engine should consider two Acrylic surfaces related when:

- their nearest projected boundaries fall within the governed influence radius
- their z separation remains within the governed depth range
- opaque masks do not block the transport path
- the contributing Acrylic retains meaningful energy

A practical bounded approximation is:

```text
proximity = clamp(1 - projectedGap / influenceRadius, 0, 1)
depth     = clamp(1 - abs(sourceZ - receiverZ) / depthRadius, 0, 1)
coupling  = proximity * depth * visibility * remainingEnergy
```

The Material profile owns the radii and maximum coupling strength.

The engine should discard contributions below its active energy threshold.

---

# Optical Parallax

The engine should derive internal parallax from Composition movement, scrolling and Focus transitions only.

It should consume a governed `ApparentThicknessProfile` supplied by the Material System.

MEG-014 does not hard-code a physical thickness, refractive index or universal thickness-to-pixel conversion.

A practical approximation is:

```text
internalOffset = clamp(
    projectedRelationshipDelta * apparentThicknessScale,
    maximumOpticalOffset
)
```

The renderer applies this offset inside a stable Acrylic mask.

It must constrain the offset to the available expanded sampling region so displacement cannot expose an empty or uncaptured area inside that mask.

Pointer position, device tilt and gyroscope input must not affect the result.
