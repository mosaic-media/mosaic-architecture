## What changes

<!-- One or two sentences. What is different after this merges? -->

## Kind of change

<!-- Tick one. If you cannot tell, treat it as architectural and open a proposal first. -->

- [ ] **Editorial** — wording, formatting, links, typos. Meaning is unchanged.
- [ ] **Additive** — new chapter or section within an existing specification's remit.
- [ ] **Structural** — renaming, renumbering, moving or splitting. No meaning changed.
- [ ] **Architectural** — changes what Mosaic accepts. Requires an accepted proposal and a decision record.
- [ ] **Tooling** — scripts, CI, linters, templates.

## Lifecycle

<!--
Architecture changes only through MDP -> MAD -> MAC. See CONTRIBUTING.md.
Leave this section as-is if the change is editorial, structural or tooling.
-->

- Proposal (MDP):
- Decision (MAD):
- Specifications updated:

## Document type

<!-- If this adds or moves content, say why it belongs to that type rather than another. -->

## Status changes

<!--
List any Status transitions, e.g. "MEG-016 Draft -> Review".
Do not promote a document to Active in the same pull request that writes it.
-->

## Checks

- [ ] `python3 scripts/validate_docs.py` passes
- [ ] `python3 -m mkdocs build --strict` passes
- [ ] Guidance comments from the template are removed
- [ ] `Owner` is a real Git username
- [ ] Cross-references are relative hyperlinks using the catalogued `ID — Canonical Title` form
- [ ] One specification folder per commit

## Notes for reviewers

<!-- Anything you are unsure about, or a rule you think is wrong. Say so here rather than working around it. -->
