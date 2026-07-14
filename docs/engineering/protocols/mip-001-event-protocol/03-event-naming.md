<!--
File: docs/engineering/protocols/mip-001-event-protocol/03-event-naming.md
Document: MIP-001
Status: Draft
Version: 0.1
-->

# 03 — Event Naming

---

# Naming Rule

Event names should describe completed business facts.

Preferred structure:

```text
<Noun><PastTenseVerb>
```

Examples:

```text
MediaImported
PlaybackStarted
MetadataUpdated
ModuleInstalled
```

---

# Stability

An event name identifies what happened.

It should remain stable across compatible payload versions.

If the meaning changes, define a new event name rather than overloading the old one.

---

# Vocabulary

Event names should use the ubiquitous language of the publishing capability.

Avoid names that expose infrastructure, transport or handler implementation details.
