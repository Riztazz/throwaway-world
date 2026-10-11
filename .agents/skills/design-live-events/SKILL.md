---
name: design-live-events
description: Use when the user wants a consequential multiplayer narrative event with phases, participation, shared outcomes, failure/re-entry paths and lasting evidence; excludes release scheduling.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Live Events

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. An event is a proposal for future content: it does not write outcomes onto pages or decide open questions.

## Use when / not when
Use when: players experience a consequential event together, with phases, participation routes, shared outcomes, failure and re-entry, and lasting evidence.
Not when: ambient happenings (`design-trivia-flavor`), one player's objectives (`design-quest-narrative`), serial arcs (`design-live-narrative-roadmap`), state authority (`design-persistent-world-state`).

## Before you write
1. Read the pages for the event's cause, area and actors, and `decisions/INBOX.md`.
2. **An event cannot settle an open question.** If the stakes are under an open decision (who keeps a lighthouse, who holds a lease, who wins a title), the outcome is not written into the event or onto the page. Build the event around the question: the vote, the contest or the petition runs, and its result is a *proposal for the user's decision*, shown as pending in any text. Name the decision that blocks the result.
3. Read accepted decisions and follow the newer ones.
4. An event brief is not a page type. Save it as `design/events/<slug>.md`.
5. Ask in facts: why now, who gains and loses, how people can take part, what happens if nobody does, what remains afterwards.

## Procedure
1. Say why the event occurs now, what is at stake and which shared facts can change. Tie it to causes in the world.
2. Structure phases by fictional triggers, player opportunities and state transitions. Time windows are design requirements, not a release calendar.
3. Explain contribution routes and credit: solo, organised groups, late joiners, non-combat help. A collective outcome has no exclusive chosen hero.
4. Specify success, failure, partial outcome, stall, abandonment and recovery. The story must not need every event to succeed.
5. Align authoritative transitions, concurrency and repeat participation with `design-persistent-world-state`. Hearing about an event is not taking part.
6. Plan the aftermath: changed places and routines, witnesses, documents, lingering tension, access for absent and returning players. Replay is not the present world.
7. Check legibility amid crowds and interruption: current phase, goal, communication, state-compatible lines. Record delivery limits.
8. Honour the project's no-hard-instance preference where it applies. Register the plan as proposed future content.

## Output
```markdown
# <Event>
Cause / stakes / what can change:
| phase | trigger | player opportunities | state transition |
Participation and credit:
Outcomes: success / partial / failure / stalled
Aftermath and evidence:
Re-entry and legacy:
Decision this event depends on: <id, or none>  (result is pending until the user decides)
Unresolved state contracts:
```

## Worked example
Request in explore mode: "An event where players decide who keeps the Saltgate beacon, and record the winner on its page." The page's keeper is under open decision D-0005. Build the event as a three-day petition: guild and town delegations collect pledges at the quay; phase two is a public count; phase three is the Council's hearing. The result is "recommendation submitted: pending the user's decision on D-0005". The beacon page is not edited. Aftermath: both delegations leave lanterns at the stair, and a returning player gets a recap that says the keeper is still undecided.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Writing the winner on the page | Result is a proposal pending the user's decision |
| An event that only works if everyone succeeds | Specify failure, stall and recovery |
| One hero owns a shared outcome | Credit by route and scope |
| Replay treated as the current world | Present as history |
| A release date or schedule | Phases and triggers only |

## Acceptance
- Each phase has a clear opportunity and a coherent outcome; concurrent play cannot create incompatible canon.
- Absence and failure have a continuation and lasting evidence.
- Open decisions stay open in every text the event produces.
