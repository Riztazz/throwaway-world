---
name: design-quest-narrative
description: Use when the user wants an actual quest's actions, objectives, branches, dialogue needs and consequences for a persistent online RPG; hooks alone use design-story-hooks.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Quest Narrative

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A quest is a design document; it does not rewrite pages or decide open questions.

## Use when / not when
Use when: a quest's objectives, branches, dialogue and evidence needs, and consequences must be specified.
Not when: only a seed is wanted (`design-story-hooks`), the lines (`design-dialogue`), reusable reactivity (`design-narrative-systems`), state authority (`design-persistent-world-state`).

## Before you write
1. Read the pages for the quest's place, actors and stakes, then `decisions/INBOX.md`.
2. **A quest cannot settle an open question.** If the plot turns on something under an open decision (who gets a lease, who holds a right), do not write the winner into the text or onto the pages. Write the branch as a *player choice that submits a proposal*, an outcome marked pending, or a version that resolves after the user decides. Name the blocking decision.
3. **Follow the newer accepted decision.** If an old decision was replaced, use the new rule everywhere in the quest, including what the player hands over or does.
4. The quest is not a page type. Save it as `design/quests/<slug>.md`. A page update is a separate, proposed change.
5. Ask in facts: what the player is trying to achieve, what it costs, what happens on refusal or failure, who else is affected.

## Procedure
1. State the player's goal, stakes, entry conditions and reason to act. Allow several reasons to join; the player need not be the one chosen hero.
2. Make an objective graph or ordered list. Each objective names actor, action, target or destination, evidence of completion and next step. Interpretation may stay mysterious; the required action may not.
3. Define choices as commitments with consequences, including refusal, failure, interruption and return. Promise no world change the runtime cannot support.
4. Separate personal progress and knowledge, group participation, and shared physical state. Say who owns credit, how concurrent attempts coexist, and what happens when another group moves first.
5. List dialogue, document and evidence needs, the spoiler tier and a fallback orientation. Do not require one ambient clue that is easy to miss.
6. Check expected cases: new and returning player, party at different progress, repeat attempt, late join, disconnect, missing NPC or object, world change mid-quest.
7. Respect the project's stated preference on hard instances where it applies. Repeatability does not need a separate physical world.
8. Describe reward and consequence as intent, not currency or gear numbers. Proposed facts and branches are separate from released canon.

## Output
```markdown
# <Quest>
Goal / stakes / entry:
| id | actor | action | target or place | completion evidence | next |
Choices and consequences (incl. refusal, failure, return):
Dialogue, document and evidence needs:
Scoped state effects (personal / group / shared):
Open decisions this quest depends on: <decision ids, or none>
Proposed canon additions: <list>
```

## Worked example
Request in explore mode: "Quest where the player delivers the harvest tax at the Mill Gate." The accepted decision says taxes are paid in sealed tally-sacks, and the old rule (paid in grain) is superseded. Objectives: collect the sealed sack from the reeve, carry it to the gate clerk, bring back the stamped receipt. The grain version appears nowhere. The gate's keeper is under open decision D-0006 (Crown or town), so the clerk is described by function, not allegiance, and the final choice is a player submission marked pending. No page is edited.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Naming the winner of an open question | Pending branch; name the decision that blocks it |
| Using a superseded rule because the page text still shows it | Check decision status; follow the newer one |
| Promising a permanent world change | Say what the runtime must support |
| One missable clue for essential progress | Reliable route for required steps |
| Every player is the chosen hero | Several motives; scoped credit |

## Acceptance
- A player can tell what to do next; each branch has a coherent consequence and a way back.
- Concurrency and progress differences are handled or listed as open contracts.
- No open question is settled and no replaced rule is followed.
