<!--
File: docs/engineering/guides/meg-004-hexagonal-architecture/glossary.md
Document: MEG-004
Status: Draft
-->

# Glossary

> *Architecture succeeds when every engineer means the same thing by the same word.*

---

# Purpose

This glossary defines the terminology used throughout the Mosaic Hexagonal Architecture specification. These definitions establish the canonical architectural vocabulary for Architecture Specifications, ADRs, Source Code, Documentation, Module SDKs and Engineering Discussions.

Where a term has a specific meaning within the Mosaic Architecture, that definition takes precedence over informal usage.

---

# A

## Adapter

An infrastructure component that translates between the Domain and an external technology. Adapters implement Ports and own translation, protocol conversion and infrastructure integration. They do **not** own business behaviour.

---

## Application Layer

The layer immediately outside the Domain, responsible for coordinating business use cases. Application Services belong to this layer. The Application Layer orchestrates; the Domain decides.

---

## Application Service

A component responsible for coordinating a business use case. Application Services load Aggregates, invoke business behaviour and persist changes, but they do not implement business rules.

---

# C

## Composition Root

The single location where infrastructure, adapters, application services and runtime are assembled into a running application, typically:

```text
cmd/server/main.go
```

The Composition Root owns dependency construction.

---

# D

## Dependency Direction

The architectural rule stating that every dependency points towards the Domain. Infrastructure depends upon the Domain; the Domain depends upon nothing external.

---

## Domain

The business core of the application. The Domain owns Entities, Aggregates, Value Objects, Domain Services and Domain Events, and remains completely independent of infrastructure.

---

## Driven Adapter

An Adapter implementing a Driven Port — for example a PostgreSQL Repository, a TMDB Metadata Provider or a Blob Storage Adapter. Driven Adapters fulfil Domain requests.

---

## Driven Port

A Port describing a capability required by the Domain, such as a Repository, a Metadata Provider or an Artwork Store. The Domain owns these contracts; infrastructure implements them.

---

## Driving Adapter

An Adapter translating external requests into Domain behaviour — for example HTTP Controllers, CLI Commands, Runtime Subscribers or Scheduler Tasks. Driving Adapters invoke Driving Ports.

---

## Driving Port

A contract describing business behaviour exposed by the Application, such as Resume Playback, Import Media or Create Collection. Driving Ports define use cases, not transport protocols.

---

# H

## Hexagon

The conceptual boundary surrounding the Domain and Application. Everything inside the Hexagon represents business behaviour and everything outside represents infrastructure. The hexagon is a visual metaphor rather than a structural requirement.  [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture)

---

## Hexagonal Architecture

An architectural style introduced by Alistair Cockburn, also known as Ports and Adapters. Its central principle is:

> Dependencies point inward.

Business behaviour remains isolated from external technology.

 [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture)

---

# I

## Infrastructure

Everything outside the Domain, including HTTP, PostgreSQL, Blob Storage, Docker, Runtime and External APIs. Infrastructure adapts itself to the Domain, never the reverse.

---

# P

## Port

A business contract owned by the Domain or Application Layer. Ports define required capabilities and exposed behaviour, but never implementation.

---

# R

## Replaceability

The architectural property whereby one technology may be exchanged for another without modifying business behaviour. Replaceability is achieved through Ports, Adapters and Dependency Inversion.

---

## Runtime Boundary

The architectural separation between the Domain Model and the Reactive Runtime. The Runtime coordinates execution; the Domain models business behaviour.

---

# T

## Technology Leakage

The accidental introduction of infrastructure concepts — such as SQL, HTTP, JSON, Docker or Runtime APIs — into the Domain. Technology leakage violates Hexagonal Architecture.

---

## Translation

The process performed by Adapters to convert between infrastructure models and business models. Translation always occurs at the architectural boundary, never inside the Domain.

---

# U

## Use Case

A business operation exposed through a Driving Port, such as Import Media, Resume Playback or Archive Collection. Application Services coordinate use cases; Aggregates implement business behaviour.

---

# Common Acronyms

| Acronym | Meaning |
|----------|---------|
| ACL | Anti-Corruption Layer |
| ADR | Architectural Decision Record |
| API | Application Programming Interface |
| DTO | Data Transfer Object |
| HTTP | Hypertext Transfer Protocol |
| MEG | Mosaic Engineering Guidelines |
| SDK | Software Development Kit |
| SQL | Structured Query Language |
| UI | User Interface |

---

# Relationship to MEG-004

This glossary supports every document within the Hexagonal Architecture specification. Definitions should remain consistent across Architecture Specifications, Runtime Documentation, Domain Documentation, Module SDKs and Contributor Guidance.

Whenever architectural terminology evolves, this glossary should be updated before introducing new terminology elsewhere.
