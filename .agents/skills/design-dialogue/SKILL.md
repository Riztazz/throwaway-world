---
name: design-dialogue
description: Use when the user wants character dialogue, conversations, NPC barks, dialogue variants, or voice revision for fiction and multiplayer narrative.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Dialogue & Barks

> Binding rules live in `rules/` (modes, protected pages, decisions, page format; stories: `rules/STORIES.md`). Ask the task mode first. This skill adds craft, not permissions.

## Use when / not when
Use when: spoken lines, conversations, barks or dialogue variants are wanted, for fiction or for a game.
Not when: branching and reactivity contracts (`design-narrative-systems`), the quest's objectives (`design-quest-narrative`), broader prose edits (`design-narrative-editing`).

## Before you write
1. Search `INDEX.md` for each speaker, their faction and the place. Read the speakers' pages and the voice file `voice.md` if the world has one. Dialogue is not a page type: write it to `design/dialogue/<slug>.md` (or the story folder for fiction), never into `world/`.
2. Check what the speakers can know. Lines must not state a fact the world has not set. A fact the scene needs and the bible lacks is a bounded proposal, labelled, or a question.
3. Open decisions about the speaker's status or the event they discuss: do not write around them as if settled.
4. Ask in facts: what each speaker wants from the other, what they will not say, who else is listening, how long the lines may be, where they are delivered (text box, bark, voiced).

## Procedure
1. Fix each speaker's want, what they can say openly, and what the speech changes. Vary register, vocabulary, rhythm and avoidance without caricature.
2. Draft in context: speech works with action, silence and response. Fiction may use subtext. A required quest instruction names the actor, the action, the target or place, and the next step, plainly.
3. Keep knowledge boundaries. Write state variants only against conditions that were supplied or proposed; no NPC thanks every player for a shared achievement.
4. For barks give the trigger intent, audience, priority, repetition and expiry as design requirements, not implemented behaviour.
5. Skip what everyone already knows unless a motive makes the explanation credible. Clarify for the newcomer rather than hiding every unfamiliar term.
6. For branches record each option's intent and consequence; options must truthfully signal commitment. Flavour variation is separate from state change.
7. Note localization context where it matters: speaker, variable meaning, plural and gender, text expansion. Do not claim translation or accessibility testing.

## Output
A scene, or a table with stable ids:

```markdown
| id | speaker | condition / trigger | line | knowledge tier | delivery note |
|---|---|---|---|---|---|
| gate-01 | clerk | caravan reaches the lane | "Count your drays, then count them again." | public | flat, tired |
```

No engine-specific syntax is invented. New facts the lines depend on are listed beneath the table as proposals.

## Worked example
Request in explore mode: "A bark for the guard at the east stair when a stranger climbs at night, and a short exchange if the player answers." The index shows the stair, the Watch faction and a curfew in the city page. Write three barks (warning, second warning, let-through) with the trigger intent and a cooldown requirement, plus a four-line exchange where the guard asks for a lantern pass, which the Watch page names. Not written: the pass's colour (the page is silent), which goes into the proposals list.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Inventing a rule or name so a line lands | List it as a proposal or ask |
| Everyone explains what they both know | Cut it unless a motive carries it |
| An NPC thanks each player for the shared outcome | Write the line against the shared state |
| Copying a source character's catchphrase | Build from the speaker's want and status |
| Writing dialogue into `world/` | Dialogue lives in `design/` or the story folder |

## Acceptance
- Speech reflects each speaker's motive and knowledge; required actions are clear.
- Variants cannot contradict established state; unknown facts are proposals.
- Runtime and localization needs are listed as handoffs, not claimed as verified.
