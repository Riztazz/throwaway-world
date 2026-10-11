---
name: design-knowledge-revelations
description: Use when the user wants mystery, clues, lore discovery, spoiler boundaries, reveal pacing, or how different readers and players learn contested world facts.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Knowledge & Revelations

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill plans discovery; it does not decide what is true.

## Use when / not when
Use when: a mystery, a spoiler boundary, reveal order or the way different audiences learn a contested fact needs a plan.
Not when: the concrete evidence in a place (`design-environmental-storytelling`), the explanatory prose (`design-world-description-exposition`), authoritative flags and shared state (`design-persistent-world-state`).

## Before you write
1. Search `INDEX.md` and open the pages that hold the truth you are planning to reveal. Find every page that marks something deliberately unknown (a `Deliberately Unexplained` section, an `Unknown:` line, a decision that leaves it open).
2. **A deliberately unknown cause is not yours to solve.** A reveal map for it records the clues, the competing readings and the confirmation level; it does not supply the answer. If the user wants it solved, that is a decision for them, recorded with their words.
3. Read open decisions that touch the mystery.
4. A knowledge map is not a page type. Save it as `design/knowledge/<slug>.md`.
5. Ask in facts: what must the audience understand to act, what is optional, who might learn it out of order, who already knows.

## Procedure
1. Separate author truth, attributed accounts, deliberately unknown matters, audience interpretation and runtime knowledge flags. Do not solve source-stated unknowns to fill a table.
2. For each revelation state the starting assumption, evidence, plausible inference, alternate reading, confirmation level and consequence. A reveal changes understanding or choices; it is more than a name.
3. Plan the order and the redundancy. Required, actionable information needs a reliable route; optional lore can reward attention and stay incomplete.
4. Account for players who arrive out of order, return later, hear a spoiler or miss a live event. Receiving information is not proof of participation or ownership.
5. Set access conditions and what an NPC can know. In fiction, tell narrator facts from viewpoint assumptions; in game text avoid confirmations of an obsolete state.
6. Test the failure cases on paper: missed clue, reordered evidence, interrupted dialogue, conflicting testimony, content finished before onboarding. Give a fallback explanation that keeps chosen ambiguity.
7. Send concrete evidence to `design-environmental-storytelling`, explanation to `design-world-description-exposition`, and authoritative state to `design-persistent-world-state`.

## Output
```markdown
| fact or unknown | status (author truth / attributed / deliberately unknown) | knowledge tier | evidence routes | gates and order | inference limit | required or optional | late-access path |
```

Plus a short "if the audience misses it" paragraph per required item. An audience-facing reveal draft only on request, and never one that resolves a deliberate unknown.

## Worked example
Request in explore mode: "Plan how players learn why the old beacon went dark." The history ledger states the cause is deliberately unexplained and two chronicles disagree. Build the map with three clue routes (a keeper's log, soot patterns in the lamp room, a ferryman's account), tag the chronicles as attributed and conflicting, and set the confirmation level to "plausible, never confirmed". Required: that the beacon went dark during the third winter (reliable via the ledger and a quest instruction). Optional: the clues. Missed-clue fallback: a harbour clerk summarises both readings. The cause is not written anywhere in the map.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Solving the mystery because the plan needs an ending | Record readings and confirmation level; leave the unknown |
| Every clue required | Required facts get a reliable route; lore stays optional |
| Treating "heard it" as "took part" | Knowledge and shared state are separate |
| A reveal that only names a name | State the consequence for choices |
| One path to essential information | Give redundancy for missed or reordered clues |

## Acceptance
- Essential comprehension survives expected misses and reordering.
- Optional mystery stays productive, and no deliberate unknown is resolved.
- A player's knowledge is never silently treated as a shared physical change.
