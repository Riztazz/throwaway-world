---
name: design-reference-synthesis
description: Use when the user wants multiple references combined into an original world or narrative approach, with preference weights, provenance, compatibility and tradeoffs.
metadata:
  type: workflow
  family: world-bible-skills
  stage: reference
compatibility: []
---

# Design: Reference Synthesis

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A synthesis is a proposal; it never overrides the world's rules and it never becomes canon until the user says so.

## Use when / not when
Use when: several references, or one reference plus the world's own aims, should become an original design with provenance, weights and tradeoffs.
Not when: studying a work (`design-reference-analysis`), formalising powers (`design-magic-system-fusion`), writing scenes (`design-fiction-drafting`).

## Before you write
1. Read the technique cards (`authoring/references/`) and the world's rules. Run each candidate idea against the physical-rules page and the invariants first. An idea that needs a rule the world forbids (storing or carrying a power, reach beyond the limit, a resource the economy cannot supply) **does not carry over unchanged**: name the invariant, then offer a version inside the rules or ask whether the user wants to change it (a protected change).
2. Read accepted decisions and open questions that the blend would touch.
3. Mark any reference you have not read as **unread**; build only on evidence you have.
4. Ask in facts: which effect matters most, what weights the user wants (equal weights only if asked), what must not appear.

## Procedure
1. State the order of authority: the user's current instructions, accepted canon not being revised, chosen goals, then source-derived options. A canon revision needs an impact record.
2. Extract functional principles: the pressure, constraint, revelation pattern or social consequence that produces the effect. Drop source proper nouns and distinctive expression.
3. Build a compatibility matrix against tone, rules, geography, agency, length and shared-state needs. Similar motifs can carry incompatible assumptions.
4. Develop one coherent candidate, or a few materially different ones if a choice is open. Show how the mechanisms change each other; do not stack every feature.
5. Redesign causes, actors, institutions, vocabulary and sequence for this world. Renaming is not synthesis; no source plot order or iconic scene.
6. Keep a provenance ledger: idea, reference evidence, transformation, fit with canon, new consequence, status.
7. Test costs and failure cases: a borrowed reveal may hide essential actions; a solo-hero mechanic may break a shared world; a gate may clash with the no-hard-instance preference.
8. Hand bounded additions to the owning disciplines. Drafting may proceed around open options.

## Output
```markdown
## Synthesis brief
Weights and rationale:
Selected mechanisms:
## Compatibility and tradeoffs
| idea | fits | blocked by (INV-n / decision) | version that fits |
## Provenance ledger
| idea | evidence | transformation | canon fit | consequence | status |
## Proposed rules and relationships
## Canon change list (needs the user)
```

## Worked example
Request in explore mode: "Blend the bottled-lantern folklore of a seafaring saga with our tide-power and propose how light can be bottled and shipped." The tide-power page fixes `::storage:: none` (D-0002). Report the clash: bottled light is stored power. Fitting versions: light that is *made where it burns* (lamp-trimmers who ship wicks, glass and the tide-table that tells when to light them), or folklore about bottled light that is *attributed belief* in the world, with the real practice mundane. Provenance: folklore motif (secondary report; saga unread) -> transformed into a trade in trimming tools. The power page is unchanged; an exception to `storage` is left for the user to authorize.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Carrying over a mechanism the world's rules forbid | Name the invariant; offer a fitting version or ask |
| Renaming a source scene | Redesign causes and sequence |
| Equal weights by default | Weights the user gave, or a reasoned proposal |
| Building on a work you have not read | Mark it unread; rely on the user's account as secondary |
| Treating the blend as lore | It is a proposal with a change list |

## Acceptance
- Causality and vocabulary are original, and references support technique, not expression.
- Each addition fits the user's priorities or exposes a concrete decision.
- Every conflict with an invariant is named; no protected page changed.
