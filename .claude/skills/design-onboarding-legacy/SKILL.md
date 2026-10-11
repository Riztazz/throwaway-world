---
name: design-onboarding-legacy
description: Use when the user wants newcomers or returning players oriented to an evolving world, missed events, older story access, recap, or historical replay without contradictory current canon.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Onboarding, Catch-up & Legacy

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill explains the world to players; it never decides an open question for them.

## Use when / not when
Use when: newcomers or returning players need orientation, a recap, or access to older events without the present contradicting the past.
Not when: disclosure pacing (`design-knowledge-revelations`), state scopes and replay (`design-persistent-world-state`), arc continuity (`design-live-narrative-roadmap`).

## Before you write
1. Read the pages for the present situation, the history ledger and the decisions. Open `decisions/INBOX.md`.
2. **A recap states only what is settled.** If a fact the recap would mention is under an open decision (who holds a right, who owns a string, who won), write it as open: "not yet decided" with the two readings. Never pick a side to make the recap read smoothly, and never write it into a page.
3. A replaced decision is not a source; follow the newer accepted one.
4. A recap or entry matrix is not a page type. Save it as `design/onboarding/<slug>.md`.
5. Ask in facts: who is the audience (new, returning, veteran), what must they be able to do next, what changed since they left, what is no longer true.

## Procedure
1. Name the cohorts and their starting states. Use real progress or knowledge data if it exists; never infer attendance from an account date.
2. Orient first: where the player is, what changed, what they can do now, which context is essential. Layer optional history so onboarding is not an encyclopaedia.
3. Pick the delivery: short recap, witnesses, surviving traces, a chronology or codex, guided rediscovery, or clearly historical presentation. Use supported systems or label the proposal.
4. Say honestly what is gone or changed. A destroyed district or dead NPC stays in the record without appearing alive.
5. Keep learning about an event, replaying it, and having taken part separate. An absent player did not author the outcome.
6. Plan for out-of-order exposure, stale dialogue, partial quests and the spoiler ceiling. Offer a fallback when an old prerequisite no longer exists.
7. Walk a newcomer and a returning veteran through the current state on paper. Usability claims need observed tests.
8. Treat legacy access as intent until the delivery contract confirms it.

## Output
```markdown
| cohort | starting state | must know now | next action | optional history | access path |
```

Then the recap text (short), the legacy access plan, how obsolete content is handled, and a list of things still open or needing a system.

## Worked example
Request in explore mode: "Recap for players returning after the winter update: who runs the Saltway ferries now?" The index shows the ferry guild and a pending decision on whether the Harbourmaster or the guild holds the ferry licence. Write the recap: ferries run, tolls are paid as before (settled by an accepted decision), and the licence is "under dispute between the Harbourmaster and the guild, not yet decided". Put the two readings in the open-items list for the user. A veteran who sided with the guild last season gets a line about their own part; a newcomer does not.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Naming a licence holder because the recap needs one | Write it as open and list both readings |
| Dumping all history on a newcomer | Orient first, layer the rest |
| Granting an absent player credit for an outcome | Separate learning, replay and participation |
| Resurrecting dead NPCs in a replay | Present it as history |
| Promising legacy access the system may not support | Mark it as intent |

## Acceptance
- New and returning players can state the present stakes and their next action.
- Historical access keeps past outcomes; knowledge, participation and current reality are not conflated.
- Open questions stay open in the text and are listed for the user.
