# Open Questions and Documentation Defects

A register of things found in the documentation that **cannot be fixed by editing prose**, because resolving them requires knowing what Mosaic actually does.

This file is deliberately outside `docs/`. MkDocs never publishes it and `scripts/validate_docs.py` never scans it, so it can name unresolved contradictions plainly without those contradictions appearing on the documentation site as though they were content.

## Why this exists

The documentation rewrite fixes how the documentation reads. It cannot fix whether the documentation is *true*. Three classes of problem surface during a rewrite and all three are recorded here rather than guessed at:

- **Contradictions** — two documents, or two sections of one document, state incompatible rules. Picking a side without knowing the architecture would silently invent it.
- **Underspecified** — a passage is vague, hedged, or defers to an owner it never names. Making it concrete requires facts that exist in someone's head or in the codebase, not in this repository.
- **Duplication** — the same concept is defined in several places. Deduplicating means deciding which document owns it, which is an authority decision.

An agent rewriting prose must never resolve these by inference. Fabricated architecture is worse than vague architecture, because it reads as settled.

## How to use this

Answer entries inline. Edit the **Resolution** line, set **Status** to `Answered`, and the next documentation pass will apply it and set the entry to `Resolved`.

| Status | Meaning |
|--------|---------|
| `Open` | Needs a decision from someone who knows the architecture. |
| `Answered` | Decision recorded here; not yet applied to the documentation. |
| `Resolved` | Applied. Kept for traceability. |
| `Won't fix` | Deliberately left as-is, with the reason recorded. |

Identifiers are permanent. A resolved entry keeps its number.

---

# Contradictions

## Q-001 — Which layer owns a Driving Port?

**Status:** `Open`
**Where:** [MEG-004 ch03](../docs/engineering/guides/meg-004-hexagonal-architecture/03-driving-ports.md), [ch02](../docs/engineering/guides/meg-004-hexagonal-architecture/02-ports.md), [ch04](../docs/engineering/guides/meg-004-hexagonal-architecture/04-driven-ports.md)

Chapter 03 states that Driving Ports "belong to the Application layer immediately surrounding the Domain". Chapter 02's guidelines state that Ports must belong to the Domain, and chapter 04 repeats that for Driven Ports.

Either Driving Ports are a deliberate exception, or one of these statements is wrong. This is load-bearing: it determines which package a Port interface is declared in.

**Resolution:**

## Q-002 — Does a Driving Port receive transport models or business models?

**Status:** `Open`
**Where:** [MEG-004 ch03](../docs/engineering/guides/meg-004-hexagonal-architecture/03-driving-ports.md), sections *Request Models* and *Validation*

*Request Models* says transport models should be translated before reaching the Port, which implies a Port never sees a transport model. *Validation* says Driving Ports "should receive already valid transport models", which implies it does.

Both statements were preserved verbatim during the rewrite rather than picking a side.

**Resolution:**

## Q-003 — "Define Ports Last" contradicts its own chapter

**Status:** `Open`
**Where:** [MEG-004 ch13](../docs/engineering/guides/meg-004-hexagonal-architecture/13-modelling-guidelines.md)

The section heading says "Define Ports Last". The chapter's own Philosophy makes defining Ports step 3 of 5, before implementing Adapters and assembling the Composition Root. The body text ("Ports should emerge naturally") is consistent with the Philosophy; only the heading conflicts.

Probably just a wrong heading, but changing it changes guidance, so it is not an editorial fix.

**Resolution:**

## Q-004 — Dependency arrows point the wrong way

**Status:** `Open`
**Where:** [MEG-004 ch11](../docs/engineering/guides/meg-004-hexagonal-architecture/11-runtime-boundary.md), *Relationship to MEG* diagram

The diagram renders `Domain → Ports → Adapters → Reactive Runtime → Infrastructure`, with arrows pointing outward from the Domain. The guide's central rule, stated in chapters 09 and 13, is that dependencies point inward.

If the arrows mean "layering" rather than "depends on", the diagram needs a different notation, because every other diagram in the guide uses arrows for dependency.

**Resolution:**

## Q-005 — Can one Adapter implement several Ports?

**Status:** `Open`
**Where:** [MEG-004 ch05](../docs/engineering/guides/meg-004-hexagonal-architecture/05-adapters.md), [ch07](../docs/engineering/guides/meg-004-hexagonal-architecture/07-driven-adapters.md)

Chapter 05 titles a section "One Adapter, One Technology" and lists "Shared Adapters: one Adapter implementing unrelated Ports" as prohibited. The guidelines in both 05 and 07 state that an Adapter "must implement one **or more** Ports".

These reconcile only if "unrelated" carries the whole distinction, which is never defined. What makes two Ports related enough to share an Adapter?

**Resolution:**

## Q-006 — Uppercase RFC 2119 keywords across the engineering guides

**Status:** `Open`
**Where:** MEG-001 through MEG-009, MIP-003 — roughly 1,800 occurrences across 162 files
**Also:** [MDG-001 ch10](../docs/engineering/documentation/mdg-001-documentation-authority-guide/10-standards-mapping.md)

MDG-001 chapter 10 adopts RFC 2119 *semantics* but explicitly rejects its uppercase typography. Most engineering guides are written in uppercase `MUST` / `SHOULD` / `MAY`, and MEG-001's own Document Control defines an uppercase normative table, which directly contradicts the ratified standard.

Either those guides are rewritten to sentence case, or MDG-001 chapter 10 records them as a standing exception. Vale reports these as warnings today, which drowns other signal.

MEG-004 has already been converted, so the pattern is proven.

**Resolution:**

---

# Duplication and Ownership

## Q-007 — MEG-004 chapters 02 and 04 are substantially the same chapter

**Status:** `Open`
**Where:** [ch02 Ports](../docs/engineering/guides/meg-004-hexagonal-architecture/02-ports.md), [ch04 Driven Ports](../docs/engineering/guides/meg-004-hexagonal-architecture/04-driven-ports.md)

*Why Ports Exist* and *Why Driven Ports Exist* use the same Playback and PostgreSQL example and the same diagrams. *Ports Describe Behaviour*, *Business Language*, *Ports Are Stable* and the "ports are small" material appear in both. Chapter 02's *Mosaic Examples* is a superset of chapter 04's *Examples Within Mosaic*.

If 02 owns the general Port rules, much of 04 could become a sentence and a cross-reference.

**Resolution:**

## Q-008 — MEG-004 chapters 05 and 07 overlap substantially

**Status:** `Open`
**Where:** [ch05 Adapters](../docs/engineering/guides/meg-004-hexagonal-architecture/05-adapters.md), [ch07 Driven Adapters](../docs/engineering/guides/meg-004-hexagonal-architecture/07-driven-adapters.md)

Error Translation, Mapping, Composition Root, Multiple Adapters and the Shared Adapters anti-pattern appear in near-identical form in both. The `Domain → PlaybackRepository → PostgreSQL Adapter → Database` argument appears in chapters 04, 05 **and** 07.

**Resolution:**

## Q-009 — Repeated sections within single chapters

**Status:** `Open`
**Where:** MEG-004 chapters 02, 08, 09, 12, 13

Several sections make the same argument twice:

- ch02: *Ports Are Stable* and *Port Evolution*; *Ports Are Small* and *One Responsibility*
- ch08: *Adapters*, *Ports* and *Infrastructure* restate chapters 02 and 05 with no cross-reference
- ch12 *Test Composition Root* duplicates ch09 *Testing*
- ch13 *Runtime Is Infrastructure* restates chapter 11 wholesale, and says so ("One subtle guideline deserves repeating")
- Three near-identical litmus tests: ch12 *Domain Isolation*, ch12 *Architecture Verification*, ch13 *Design For Testing*

Each survives the rewrite because deleting one is a content decision.

**Resolution:**

## Q-010 — MDL-005 and MDP-001 overlap chapter for chapter

**Status:** `Open`
**Where:** [MDL-005](../docs/design/language/mdl-005-composition-model/index.md), [MDP-001](../docs/engineering/architecture/mdp-001-adaptive-composition-runtime/index.md)

| MDP-001 | MDL-005 already owns |
|---------|----------------------|
| 03 Composition Solver | 09 Composition Solving |
| 05 Runtime Hierarchy | 02 Hierarchy, 03 Priority, 04 Hero |
| 06 Adaptive Layout | 06 Adaptive Composition, 07 Density, 08 Breathing Space, 05 Anchors |
| 10 Multi-Device Composition | 10 Device Independence |

MDL-005 is authoritative; MDP-001 is deferred. The overlap is therefore not harmful today, but it means two documents describe the same concepts at different levels of commitment.

**Resolution:**

## Q-011 — MAC-001 and MDP-001 both claim orchestration

**Status:** `Open`
**Where:** [MAC-001 ch02](../docs/engineering/architecture/mac-001-platform-architecture/02-runtime-boundary.md), [MDP-001 ch07](../docs/engineering/architecture/mdp-001-adaptive-composition-runtime/07-behaviour-orchestration.md), [ch08](../docs/engineering/architecture/mdp-001-adaptive-composition-runtime/08-runtime-pipelines.md)

MAC-001 states the Runtime owns dependency graph management and execution orchestration. MDP-001 chapter 07 defines a dependency graph and asserts that "Behavioural ordering remains architecturally defined by this specification".

A deferred proposal should not claim architectural authority over something the Canon owns.

**Resolution:**

## Q-012 — MDP-001 asserts definitions in the MDS namespace

**Status:** `Open`
**Where:** [MDP-001](../docs/engineering/architecture/mdp-001-adaptive-composition-runtime/index.md) chapters 02, 04, 05, 06, 07, 08, 09

Seven chapters open with "Within MDS, **X** is defined as…". MDP-001 is a deferred, non-authoritative proposal and cannot define terms in the Design System namespace. The phrasing is left over from when this material was an active MDS specification.

Fixing it means rewriting the definitional sentence in seven chapters, which changes what the document claims about itself.

**Resolution:**

---

# Underspecified — needs domain knowledge

These cannot be made concrete by rewriting. The facts are not in this repository.

## Q-013 — Where do transaction responsibilities live?

**Status:** `Open`
**Where:** [MEG-004 ch03](../docs/engineering/guides/meg-004-hexagonal-architecture/03-driving-ports.md), *Transactions*

"Those responsibilities belong elsewhere within the architecture" names no owner. Chapters 09 and 10 look like the likely home, but that could not be confirmed, so no cross-reference was invented.

Note that [MAD-001](../docs/engineering/architecture/mad-001-transactional-store-extensibility/index.md) records the Platform transaction boundary decision and may already answer this.

**Resolution:**

## Q-014 — The "Application layer" is never defined

**Status:** `Open`
**Where:** MEG-004, referenced in ch03, never defined

Chapter 03 places Driving Ports in "the Application layer immediately surrounding the Domain". No chapter defines that layer, and it does not appear in the guide's own modelling guidelines. Related to Q-001.

**Resolution:**

## Q-015 — Go examples carry no real signatures

**Status:** `Open`
**Where:** MEG-004, throughout

Every Go example is elided: `FindByID(...)`, `Metadata(...)`. Real parameter and return types appear nowhere in the guide.

This is the largest single contributor to the "too abstract" problem in this document. Filling it in requires the actual SDK contract, which is the province of [MEG-015](../docs/engineering/guides/meg-015-platform-foundation-implementation/03-platform-contracts.md) and [MIP-004](../docs/engineering/protocols/mip-004-platform-sdk-contract-protocol/index.md).

**Resolution:**

## Q-016 — Unexplained phrases that read as placeholders

**Status:** `Open`
**Where:** MEG-004 chapters 05, 06, 07

- ch05 *Multiple Adapters*: "This is the Platform foundation value proposition of Ports and Adapters" — the phrase denotes nothing defined anywhere.
- ch06 *Authorisation*: "Authorisation decisions should **generally** occur before entering the Domain" — the hedge implies exceptions, presumably data-scoped permissions the Domain must enforce, but none are named.
- ch07 *External Service Adapters*: "retries (where appropriate)" — no criterion. The chapter's *Retry Behaviour* section distinguishes infrastructure from runtime retries but never says when to use either.

**Resolution:**

## Q-017 — Diagrams that draw lists as dependency chains

**Status:** `Open`
**Where:** MEG-004 ch09, ch11, ch12

Several retained diagrams render enumerations as linear chains, implying dependencies that probably do not exist:

- ch09 *Infrastructure Assembly*: `Configuration → Logger → Database → Blob Storage → HTTP Client`
- ch09 *Adapter Assembly*: `Database → Playback Repository → Metadata Repository → Collection Repository` — the three repositories almost certainly each depend on the Database, not on one another
- ch11 *The Runtime Is Infrastructure*: `HTTP → Runtime → Database → Blob Storage → External APIs`
- ch12 *Testing Strategy*: `Domain → Application → Adapters → Integration → End-to-End`

Each should probably become a branching diagram or a plain list. Deciding which requires knowing the real structure.

**Resolution:**

## Q-018 — Runtime Assembly chain is ambiguous

**Status:** `Open`
**Where:** [MEG-004 ch09](../docs/engineering/guides/meg-004-hexagonal-architecture/09-composition-root.md), *Runtime Assembly*

`Event Publisher → Runtime Adapter → Playback Service` — whether this means the Service receives the Adapter, or something else, is not stated anywhere in the guide.

**Resolution:**

## Q-019 — MIP-004, MIP-005 and MIP-006 have no chapters

**Status:** `Open`
**Where:** [MIP-004](../docs/engineering/protocols/mip-004-platform-sdk-contract-protocol/index.md), [MIP-005](../docs/engineering/protocols/mip-005-module-adapter-contract-protocol/index.md), [MIP-006](../docs/engineering/protocols/mip-006-generation-composition-protocol/index.md)

Each states a real contract in three paragraphs on its landing page and has no chapters. Each now opens with an "Outline only" notice, and `validate_docs.py` reports all three as `book-stub`. These are the only three findings the validator still reports.

They need contract chapters written, which requires the actual contract.

**Resolution:**

---

# Factual and naming defects

Small, but each changes meaning, so none were fixed during the rewrite.

## Q-020 — `ArtworkProvider` or `ArtworkStore`?

**Status:** `Open`
**Where:** [MEG-004 ch02](../docs/engineering/guides/meg-004-hexagonal-architecture/02-ports.md), *Ports Are Small*

Used once as `ArtworkProvider`; every other mention across the guide is `ArtworkStore`. Likely a typo in a normative example, but the two names imply different Port responsibilities.

**Resolution:**

## Q-021 — MEG-004's repository tree describes a layout that no longer exists

**Status:** `Open`
**Where:** [MEG-004 index](../docs/engineering/guides/meg-004-hexagonal-architecture/index.md), *Repository Structure*

The tree names `README.md` as the folder's landing file; the real file is `index.md`. The folder path shown, `engineering/meg/MEG-004 Hexagonal Architecture/`, does not match the real `docs/engineering/guides/meg-004-hexagonal-architecture/`.

Preserved verbatim under the no-invention rule. Other specifications may carry the same stale tree.

**Resolution:**

## Q-022 — MDP-001 listed twice with an identical label

**Status:** `Open`
**Where:** [MEG-004 references](../docs/engineering/guides/meg-004-hexagonal-architecture/references.md)

Listed once pointing at `index.md` and once at `14-adaptive-tile-model.md`, both labelled "MDP-001 — Adaptive Composition Runtime". The second entry needs a distinguishing label.

**Resolution:**

## Q-023 — MEG-004 index diagram implies a false dependency

**Status:** `Open`
**Where:** [MEG-004 index](../docs/engineering/guides/meg-004-hexagonal-architecture/index.md), *Relationship to MEG*

The diagram renders as one linear chain alternating document identifiers and concept names — `MEG-001 → Engineering Standards → MEG-002 → Reactive Runtime → …` — which reads as "Engineering Standards depends on MEG-002".

Re-wiring it means asserting a dependency structure between the engineering guides that is not recorded anywhere.

**Resolution:**

## Q-024 — Conflicting ADR numbering in the deferred proposals

**Status:** `Open`
**Where:** [MDP-002 ch11](../docs/engineering/architecture/mdp-002-tile-framework/11-tile-governance.md), [ch12](../docs/engineering/architecture/mdp-002-tile-framework/12-tile-decision-history.md), [MDP-001 ch11](../docs/engineering/architecture/mdp-001-adaptive-composition-runtime/11-governance.md)

MDP-002 chapter 11 lists ADR-163 to ADR-167. Chapter 12 defines ADR-168 to ADR-176 covering substantially the same five decisions, with no cross-reference. One numbering scheme is stale.

Separately, MDP-001 chapter 11 lists ADR-149 to ADR-153 as bare table rows; those ADRs are defined nowhere in the repository.

**Resolution:**

## Q-025 — Four ADRs may survive the deferral

**Status:** `Open`
**Where:** [MDP-001 ch12](../docs/engineering/architecture/mdp-001-adaptive-composition-runtime/12-decision-history.md)

Most decision records in this chapter bind only the deferred runtime, but four appear to bind Mosaic regardless:

- **ADR-163** — the client resolves geometry; SDUI never sends coordinates. Chapter 10 says this boundary is still live.
- **ADR-164** — ClearLogo versus Mona Sans title treatment. A concrete v1 rule with no post-v1 gate.
- **ADR-165** — Acrylic Assembly is not material fusion. Cross-references MDS-003 as owner.
- **ADR-166** — Adaptive Composition and Authored Layout as peer client consumption modes. Half of this is v1 today.

Extracting them into a MAD would mean *accepting* decisions on the owner's behalf, so nothing was moved.

**Resolution:**

---

# Resolved

Entries move here once applied, with their original number.

*(none yet)*
