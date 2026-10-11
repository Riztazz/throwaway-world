---
name: design-world-bible
description: Use when the user wants a world bible assembled, a bounded worldbuilding plan routed, or a coherent batch reviewed across lore, original fiction, and persistent MMO narrative.
metadata:
  type: workflow
  family: world-bible-skills
  stage: assembly
compatibility: []
---

# Design: World Bible

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill routes and assembles; it does not grant permission to write anywhere the mode forbids.

## Use when / not when
Use when: the request spans several disciplines, a full-world request needs a staged plan, or a batch of pages needs one coherence check.
Not when: one discipline covers it. Open that skill directly (a place is `design-location-bible`, a date is `design-history-timeline`). A single place or scene does not need the whole bible.

## Before you write
1. Read `INDEX.md`, `decisions/INBOX.md` and the pages the request touches. Reuse the premise, medium and constraints already supplied; do not repeat answered interviews.
2. Note which target pages are protected (`accepted`, or a core-rule type: magic system, tone and premise, cosmology, history, economy). Pages blocked by an open decision stay unwritten until the user answers it.
3. Ask only what the world has not answered, in facts and consequences: what must stay true, what is deliberately unknown, who needs to read the result.

## Procedure
1. Write a short brief: deliverable, scope, audience and disclosure level, and the revision you are working from. Honor the active world's documented preferences; do not treat one world's choices as universal.
2. Pick one lead discipline and, for consequential work, one review lens. They are responsibilities, not extra agents. Use a reviewer only if one is available and worth it; otherwise state your own review separately.
3. Route to the outputs you need, reading only those skills' entrypoints: reference analysis and synthesis; foundations (tone, magic, geography, history, economy); culture and institutions; creatures, people and places; atlas; description, evidence and documents; fiction and dialogue; hooks and quests; knowledge, systems and state; live arcs, events and catch-up.
4. Require each draft to separate established facts, new proposals, deliberate unknowns and open decisions. Do not stop all drafting because one upstream page is missing.
5. Run a scoped coherence check: numbers and dates, causal order, physical rules, names and aliases, source versions, who knows what, shared consequences, broken links. Use `design-canon-continuity` for impact and `design-narrative-qa` for deliverable tests.
6. Record each contradiction with the pages, the evidence, a proposed resolution and an owner. Never pick between competing facts silently.
7. Assemble a navigable index that links the separate pages. Do not copy the whole canon into one document. Review status never means accepted.
8. State the checks you actually performed. Do not claim player testing, runtime import, visual inspection or source coverage you did not do.

## Output
For a full request:

```markdown
# <World> bible index
## Tone & Premise      <link to the page; one line>
## Medium / Output Form
## Layers              <one line per layer with its page link and status>
## Coherence Audit     <numeric and fact audit, invariant check, contradiction log>
## Acceptance Criteria <observable checks>
```

For a bounded request return only a routing note, the requested artifact, the change and its dependents, and the relevant findings.

## Worked example
Request in lock mode: "Check the harbor pages for contradictions before I write scenes there." Read the index, the three harbor pages, the ledger and the inbox. Report, with nothing written: two pages give different crane counts (6 and 9); one dock is called the Gantry in one page and the Hoist in another; a toll appears in the economy page but in no ledger entry. For each: both page paths, the evidence, a proposed fix and who decides. List what is undefined (no page for the harbor master) as gaps, not as errors.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Running every discipline for a small request | One lead, one review lens, only the entrypoints needed |
| Inventing the missing upstream page so drafting can continue | Mark the gap as a deliberate unknown or a bounded proposal and ask |
| Resolving a contradiction by choosing a side | Record both with evidence; the user or the page's owner decides |
| Writing into a page blocked by an open decision | Skip it and say which decision blocks it |
| Reporting "reviewed" as "accepted" | Only the user marks accepted |
| One giant document duplicating canon | An index linking separate pages |

## Acceptance
- The artifact traces to relevant canon, proposals and open decisions.
- Dependencies and disclosure limits are stated, and unresolved findings stay visible.
- Disciplines that were not needed produced nothing speculative.
- STUDIO output follows the handoff: a top-level H1 page, metadata in the manifest, no page frontmatter, no invented type keys.
