<!--
File: docs/engineering/guides/meg-014-refraction-engine/09-testing-and-benchmarking.md
Document: MEG-014
Status: Draft
Version: 0.1
-->

# 09 — Testing And Benchmarking

---

# Conformance Testing

Engine tests should verify:

- focused artwork overrides Hero artwork
- Hero artwork is used when Focus has no artwork
- an approved Brand Illumination Pair is used when focused and Hero artwork are absent
- the default Mosaic pair is used when no approved pair exists
- source transitions do not flash or reset Acrylic
- backdrop pixels remain receiver-local
- non-overlapping nearby Acrylic may couple
- distant or occluded Acrylic does not couple
- energy decreases through secondary transport
- parallax reacts to Composition movement, scrolling and Focus transitions
- pointer, gyro and device tilt do not drive parallax
- highlight rotation follows the canonical quadrant and angle convention
- receiver motion changes its artwork-UV sampling window without invalidating the source frame
- optical displacement never reveals an empty or uncaptured area inside the Acrylic mask
- Essential fidelity retains cached artwork-derived colour when source data is available
- user fidelity preference acts as a maximum and never forces work above safe budget
- nested Acrylic does not create unbounded backdrop-filter stacking
- invalid frames preserve the last stable state
- video presentation never waits for Refraction work

---

# Visual Fixtures

The test set should include:

- bright point against dark artwork
- broad low-contrast artwork
- saturated artwork beside neutral Acrylic
- transparent artwork regions
- rounded and irregular Acrylic masks
- overlapping opaque and Acrylic surfaces
- nearby non-overlapping Acrylic
- Focus transitions between artworks
- static and moving artwork
- reduced-motion and high-contrast states

Golden images should validate perceptual invariants rather than exact equality across rendering backends.

---

# Performance Benchmarks

Benchmarks should measure:

- [MIP-003](../../protocols/mip-003-uv-light-frame-protocol/index.md) decode and validation
- 32-, 64- and 128-texel analysis candidates
- binary16 and alternative runtime precision
- unsupercompressed and Zstandard cache payloads
- CSS layer and backdrop-filter cost
- filtered pixel area and backdrop nesting depth
- Flutter composite and fragment cost
- two-dimensional shader crossover points
- Acrylic receiver and proximity-relationship scaling
- static and video update cadence
- profile-switch hysteresis
- Enhanced, Balanced and Essential fidelity residency
- memory and upload pressure

---

# Playback Gate

A benchmark run is not acceptable when Refraction causes a presentation deadline miss, even if average frame rate remains high.

Tests should report:

- presented video frames
- dropped video frames
- Refraction-attributable drops
- worst and percentile frame time
- skipped Material updates
- stable-state reuse

---

# Technical Review Inputs

Prototype evidence should determine whether to retain or revise:

- the [MIP-003](../../protocols/mip-003-uv-light-frame-protocol/index.md) 64-texel longest edge
- `RGBA16F` canonical payload
- complete mip-chain requirement
- optional Zstandard compression
- default video polling ranges
- CSS Composite as the default web path

Documentation should remain Draft until those decisions receive technical review.
