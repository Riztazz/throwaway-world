---
paths:
  - "authoring/references/**"
---

<!-- Generated from the reference rules and CARD-TEMPLATE.md by the bootstrapper; do not edit. Loaded when a matching file is read or edited. -->

# Reference cards and research

Cards describe transferable techniques in your own words. Quote at most a few words from a source, never passages, and do not summarize plot. For every card record the source and its type (the work itself, an excerpt the user supplied, or secondary commentary), how it was read (raw text, a fetched summary, the user's words), the edition or episode, the locator, what you did **not** read, your confidence, the spoiler ceiling, and whether the reference is `hard` or `soft`. Never cite a chapter, page or timecode that came only from secondary commentary or from memory; mark anything you could not access `not read`. Samples are original and in this world's language, never excerpts. A hard reference may not be dropped silently; a soft one may be set aside with a one-line reason. The lint (`L-CARD-*`, `L-REF-*`) checks the shape.

# Technique card template

Copy this block once per technique. One card is one **atom**: a technique small enough to apply and to check. Keep each card under sixteen lines.

```
## <short name of the technique>

- Id: <creator-slug>.<aspect>.<n>        Binding: hard | soft
- Status: proposed        (the user approves or rejects it on the review page; a rejection adds a `- Review note:` line: revise the card, set it back to proposed, delete the note)
- Effect: what the reader or player experiences (one sentence).
- Mechanism: the steps by which the writing causes it (concrete: where attention goes, what is withheld, how a term is introduced, rhythm).
- Test: one question an editor can ask of a draft to check the technique is present.
- In this world: how it would appear here.
- Plain: an original passage of this moment without the technique (at most ~60 words, in the world's language).
- Applied: the same moment with the technique (original; no source names, scenes or signature phrasing).
- Avoid: what would turn it into imitation or into the opposite effect.
- Evidence: <title>, <edition or episode>, <locator>, read / partly read / secondary / not read. Confidence: high / medium / low.
- Used by: <role ids>
```

An exemplar file starts with these lines, then the passage:

```
status: proposed        (the user changes this to approved)
role: fiction-writer
purpose: what this passage demonstrates
```
