# Roadmap

Derived from the real state of `mosaic-platform`, not from a plan written ahead of it.

---

## Where the build actually is

Thirteen slices are complete. The Platform boots against real PostgreSQL, serves a GraphQL schema, runs an outbox worker with retry and dead-lettering, resolves secrets, reports component health, shuts down gracefully with a final outbox drain, and holds a content-agnostic object graph. Every slice passes `go build`, `go vet` and `go test -race` against a real database.

Two further slices — uniform store resolution and its PostgreSQL follow-up — were built and then reverted under [ADR 0012](adr/0012-capabilities-do-not-own-stores.md), which found they solved a case the architecture had already ruled out.

The content model was the last thing blocking the critical path. What remains is the thesis test itself.

---

## The critical path

Everything below is one thread. Nothing else should start until it lands, because it is the test of Mosaic's central thesis: **that a developer who is not you can extend Mosaic through the SDK.**

### 1 — The content-agnostic object model — **done**

The node tree and relation graph, designed in [ADR 0013](adr/0013-object-graph.md), with authority and media linking settled in [ADR 0014](adr/0014-storage-authority-and-transaction-scope.md).

`nodes`, `parts`, `relations` and `source_bindings` shipped with domain types, store contracts, PostgreSQL implementations, the four stores added to `Tx`, and adapter-agnostic contract tests against real PostgreSQL. Identifiers are UUIDv7 in native `uuid` columns; the twenty-five infrastructure tables keep their `text`/UUIDv4 ids and were not migrated. ADR 0013's four deliberate non-uniformities each have a contract test, since each is cheap to normalise away by accident.

This was the real blocker, and it had been mistaken for something else. The reference capability was recorded as blocked on an empty `contracts/platform/v1` and a closed `Tx`; both were symptoms of building the extension mechanism before the thing it extends. A capability now has somewhere to put an anime.

**Deliberately not in the slice, and still unbuilt:** export formats, the filesystem projection, streaming, the job queue, `LISTEN/NOTIFY`, and IPTV listings. None blocks the reference capability.

### 2 — Content commands and queries — **done**

The stores existed and were proven, but nothing above them did. No application service touched the graph, so the only way in was `Tx`, which the composition root holds — and a capability reaching for `Tx` directly would bypass the policy engine entirely.

This slice put the command order over the content model. Nine application services now exist, each validating, authenticating, authorising and — for writes — committing state and an outbox event in one transaction:

- **Reads:** `SearchContent` (title substring, media type, kind), `FindContentByExternalID` (provider id against the GIN index), `GetContentNode` (one node, optionally its direct children). Before this, `FindBySource` answered only *"have I bound this exact provider reference?"*; "do I already have this anime?" by title or external id was unanswerable, and the `nodes_external_ids_gin` and `nodes (media_type, title)` indexes had no query reaching them.
- **Writes:** `AddContentWork`, `AddContentChild`, `AttachContentPart` build the containment tree; `RelateContent`, `BindContentSource`, `ResolveContentBinding` write the association graph and resolve identity.

Two shapes were decided in the building. A child inherits its work id and media type from its parent, so a season cannot declare a different media type than its series. A binding is created confirmed or pending-review, never rejected — rejection is a resolution of an existing binding, not a state to create one in.

It was scheduled ahead of the reference capability because it is needed under every resolution of the boundary problem below, so none of it could be wasted. It did **not** resolve either blocker: every content command still authorises on a user session, and the contracts still reference `domain` types under `internal/`.

### 3 — Reference capability path

Attempted twice and correctly reported as blocked rather than forced. **It is blocked a third time, on something new**, and the block is recorded here rather than discovered mid-slice.

#### Blocked: contracts cannot be promoted as they stand

Step 3's exit criteria require promoting the proven contracts into `contracts/platform/v1` first. That is not a move. Every contract signature references `domain.Node`, `domain.User`, `domain.Session` — and those live in `internal/platform/domain`, which Go forbids an external module from importing. Verified by compiling a separate module against this one:

```
main.go:8:2: use of internal package
  github.com/mosaic-media/mosaic-platform/internal/platform/domain not allowed
```

So promotion needs a decision before it needs work: does the domain package leave `internal/`, does `contracts/platform/v1` carry a curated parallel type set with conversion at the boundary, or do contracts stop taking domain types at all? Each has a different blast radius, and every contract added before the decision is more surface to move afterwards. This is step 4's subject matter arriving early because step 3 depends on it.

#### Blocked: a capability has no way to act

`policy.Subject` carries a `UserID` and an `AuthStrength`. There is no module, capability or system principal anywhere in the policy engine, so a capability today must borrow a human's session id to do anything at all. This may resolve cheaply — *capabilities always act on behalf of an invoking user* is a legitimate answer that needs no new machinery — but it is currently undecided, and "undecided" is not the same as "cheap".

#### The slice itself

Its purpose changed under [ADR 0012](adr/0012-capabilities-do-not-own-stores.md). It was to prove a capability could own a store and join a transaction. Since capabilities own no schema, it should now prove what a capability actually does, shaped like the anime module the platform exists to support:

- source metadata from an external provider
- search existing content
- create nodes and relations in the generic model
- publish an event

Sourcing metadata needs no Platform HTTP contract, which is worth stating because it looks like a gap and is not one. Capabilities compile into the binary with trust established before the build ([ADR 0007](adr/0007-static-go-module-composition.md)), so a capability imports `net/http` itself. A Platform-provided client is worth having eventually for rate limiting and secret handling; it is not a prerequisite.

**It also carries the `media_types` registry** ([ADR 0015](adr/0015-open-and-closed-vocabularies.md)). Media types are an open vocabulary, and normalisation already collapses spelling variants, but nothing yet catches a value that was never a real type. The fix is a Platform-owned table a module contributes to through its manifest — which is precisely the "declare through the manifest, Platform acts on it" shape this slice exists to prove, so the consumer and the mechanism should land together rather than one retrofitting the other.

**Exit criteria.** The boundary decision above is made and applied, the proven contracts are promoted into `contracts/platform/v1`, and then one capability does all four using only those packages, owning no schema and touching no Platform code.

### 4 — SDK extraction readiness

Whether the contracts proven across the completed slices can leave the Platform repository as a standalone SDK a third party can build against.

**Exit criteria.** Import boundaries are enforced, and the promoted `contracts/platform/v1` surface is confirmed to expose no private Platform internals. This slice *verifies* isolation; it does not populate the surface for the first time — that happens in step 3.

A cheap standing check falls out of the block found above: compiling a throwaway module against this one catches an `internal/` leak immediately, and it should become a test rather than something rediscovered by hand.

### The stop point

> **The Platform is ready for SDK work when the reference capability uses only published contract packages and no private Platform internals.**
>
> **If the reference capability requires a private import, the contracts are not ready to publish.**

This is the rule to hold the line on. A private import that gets waved through is the moment the ecosystem becomes second-class — the community developer hits a wall the built-in modules never hit, and the extension model quietly stops being real.

**Steps 3 and 4 together are the thesis test.** If a capability can be built entirely against the published contract surface, the module ecosystem works. If it cannot, the extension model needs rethinking — and better to learn that now than after building media formats on top of it.

### Acceptance baseline

Before the foundation is considered ready for SDK extraction:

- `go test ./...` passes
- adapter contract tests pass against real PostgreSQL
- migration tests run from an empty database
- import boundary checks pass
- GraphQL resolver tests prove service routing
- Supervisor health probes pass against a running process

---

## After the thesis holds

Deliberately unplanned in detail. These follow only once the extension mechanism is proven, and each should be scoped when it starts rather than now.

- **First real module** — one media format end to end, built the way a community developer would build it. The first honest test of the SDK's ergonomics.
- **Module permissions** — what a module declares, who grants it, what enforcement means given modules compile into the binary. See the isolation tradeoff in [the overview](index.md); this is a declaration and audit mechanism, not containment.
- **Module distribution** — how the Supervisor discovers, selects and pulls a community module. Manifest shape, signing, trust tiers.
- **Export formats** — NFO for other systems, `.mos` for Mosaic-to-Mosaic portability. Generated on demand from authoritative state ([ADR 0014](adr/0014-storage-authority-and-transaction-scope.md)).
- **Job queue** — the `jobs` tables exist with no service on them. `SELECT ... FOR UPDATE SKIP LOCKED` is the intended pattern, for import, provider sync and enrichment.
- **`LISTEN`/`NOTIFY`** — an accelerator over the outbox worker's existing poll, not a replacement for it. Notifications are dropped when no listener is connected, so the poll stays as the floor.
- **Shell and SDUI** — the server-driven interface.
- **Mosaic Design Language** — acrylic with weight, artwork as the light source.

---

## Working rules

- **One slice at a time**, in order, each passing its gate before the next begins.
- **Report blockers, do not force past them.** The reference capability slice was stopped twice and reported instead of bodged. That was correct both times, and it is why the fix was a design decision rather than a workaround buried in code.
- **Code is authoritative where code exists.** Documentation describes what is built; it does not specify what is not.
- **When implementation contradicts a specification, the specification is wrong.** Fix it there, in the same session, rather than carrying a correction in a repository-local note.
