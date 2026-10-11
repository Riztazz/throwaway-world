---
name: design-game-systems
description: Use when the user wants a game system specified in prose: core loop, rules, resources, abilities, items, progression shape or economy flows, as a design document with no balance numbers; narrative reactions use design-narrative-systems.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Game Systems

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A system spec is a design document; it does not rewrite pages, settle open decisions or break the world's rules.

## Use when / not when
Use when: how a mechanic works must be written down: the core loop, a resource and where it comes from and goes, an ability or item class, the shape of progression, how a magic cost or an economy flow shows up in play.
Not when: reusable narrative reactions (`design-narrative-systems`), who owns shared state (`design-persistent-world-state`), a quest (`design-quest-narrative`), the world's physical or magical rules themselves (`design-magic-system-fusion`), trade and prices in the fiction (`design-economy-trade`).

## Before you write
1. Read the world's rule pages first (magic, physical rules, economy) and `decisions/INBOX.md`. A mechanic may not contradict an invariant: if a power the spec needs is forbidden (reach, storage, a free resource), **name the invariant** and offer a version inside it, or ask whether the user wants to change the rule (a protected change).
2. **No balance numbers.** Do not state damage, costs, drop rates, XP curves, cooldowns or stat values. Describe amounts in ordinal or relative terms ("scarce", "a few uses before rest", "costs more than it returns when rushed"). If the user gives numbers, record them as user-given; never invent or "suggest" values.
3. Find out whether the game is single-player or online (`.world-design/world.json`, `intake.products`, or ask). Online adds shared-state and concurrency questions; single-player adds what the world does when the player is absent.
4. A spec is not a page type. Save it as `design/systems/<slug>.md`, starting from `design/systems/_template.md` when the world has it. The lint warns (`L-SYSTEM-NUMBERS`) about a value next to a balance word; mark a value the user gave with `user-given:`, or link the world page it comes from. A page update is a separate, proposed change.
5. Ask in facts: what the player does, what it costs, what they get, how it fails, how it ends.

## Procedure
1. State the player-facing purpose: what the system is for and which pillar or tone it serves. If it serves none, say so.
2. Write the **loop**: trigger, player action, system response, feedback, cost or reward, and what makes the player do it again. One loop per spec; split specs rather than stacking loops.
3. List **resources and flows**: each resource with its sources and sinks, who or what in the world produces and consumes it, and why that is plausible here. A source with no world cause or a sink with no purpose is a defect.
4. State the **rules** as if-then lines with their edge cases: what happens on refusal, failure, interruption, simultaneous actions, empty and full states, and recovery.
5. Describe **progression shape**: what changes over time (access, capability, standing, knowledge), in ordinal steps and in what order they open, not in values.
6. Tie it to the world: which magic cost, institution or economy rule it depends on, and what in the world visibly changes when it is used. Link the pages.
7. For an online game add: what is personal, party or shared; what happens when two players act at once; how a late joiner enters. Do not decide authority of shared state (hand to `design-persistent-world-state`).
8. List **tuning parameters**: each named, with the direction it pushes the experience and what it trades off, but with no value. These are for the user or the engine team.
9. List **open questions and proposed canon additions** separately from the spec. Check the spec against every accepted decision it touches.

## Output
```markdown
# <System>
Purpose and pillar:
Loop: trigger / action / response / feedback / cost or reward / why again
| resource | sources (world cause) | sinks (purpose) | notes |
Rules (if-then, with edge cases: refusal, failure, interruption, empty, full, recovery):
Progression shape (ordinal steps, no values):
World ties (pages, invariants it respects):
Online only: personal / party / shared; concurrency; late join
Tuning parameters (named, direction, trade-off, no values):
Open decisions this depends on: <ids, or none>
Proposed canon additions: <list>
```

## Worked example
Request in extend mode: "Specify how drawing water works as a mechanic in the desert game." The magic page fixes `::reach:: 0 paces` and says every draw is repaid by an equal pour. Loop: stand on a source, call, receive water, owe the pour. The spec does not let the player draw from afar; it makes the owed pour the cost and shows what happens if the player is out of water to return (the call fails and a debt mark appears with the Compact's clerks, per the economy page). Resources: water (source: the aquifer under the Basin; sink: pours, trade, tolls), debt marks (source: failed pours; sink: payment). Tuning parameters: how fast debt accumulates (pushes toward planning versus panic; trades against recovery time). No amounts appear anywhere.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Inventing damage, XP or drop-rate values | Ordinal wording; list the parameter without a value |
| A power the world's rules forbid | Name the invariant; offer a version inside it or ask |
| A resource with no source in the world | Give it a cause or remove it |
| Several loops in one spec | One loop per spec; split |
| Deciding shared-state authority | Hand to persistent-state design; list it as an open contract |

## Acceptance
- The loop, flows, rules and failure cases are complete and contain no balance numbers.
- No invariant, accepted decision or open question is contradicted or settled.
- Parameters are named with direction and trade-off; open questions are listed apart from the spec.
