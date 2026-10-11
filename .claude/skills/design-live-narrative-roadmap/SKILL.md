---
name: design-live-narrative-roadmap
description: Use when the user wants causal future arcs, serial fiction continuations, or evolving MMO narrative waves; excludes release calendars, monetization and detailed quest scripts.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Live Narrative Roadmap

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A roadmap is a set of proposals about the future; none of it is released canon and none of it edits a page.

## Use when / not when
Use when: continuation should follow from consequences, as ordered causal waves.
Not when: one event (`design-live-events`), a quest (`design-quest-narrative`), runtime authority (`design-persistent-world-state`), catch-up (`design-onboarding-legacy`), or any release calendar or monetization.

## Before you write
1. Read the pages for the pressures the arc draws on, the history ledger, and `decisions/INBOX.md`.
2. **Planned changes to protected pages are proposals, listed, not made.** When an arc has a power seize a place, break an agreement or change a ruling body, and those pages are `accepted` or core-rule types, do not edit them and do not describe the change as having happened. List each page the wave would change, the exact change, and its dependents, as a proposal that needs the user's authorization in their own words. The roadmap itself may be a new page (type `roadmap`).
3. Open questions stay open: a wave may be built around a decision pending; its branches show both outcomes.
4. Mark author-only plans apart from released canon; a forecast is not a fact players may cite.
5. Ask in facts: what is unresolved now, who acts, what happens if nobody does, how far ahead the plan needs to look.

## Procedure
1. Pick a bounded set of unresolved causes and possible outcomes. Not all lore layers need to exist.
2. For each wave write **Draws from**, **What changes**, **What it seeds**, **Invariant check**. An arc may end without seeding another.
3. Track actors' choices, consequences and alternatives if an event succeeds, fails or is not attempted. Shared physical change is separate from personal knowledge and participation.
4. Pace revelations and recurring threads. Plan for new, returning and absent players: surviving evidence, summaries, alternate discovery, legacy access after irreversible change.
5. Keep only the horizon the current decisions justify. State uncertainty and revision triggers.
6. Respect the project's no-hard-instance preference where it applies.

## Output
Use the roadmap page's section names, one block per wave:

```markdown
# <Arc>
::wave:: 1

## Draws from
## What changes
## What it seeds
## Invariant check
```

Add a branch table (success / failure / not attempted), knowledge and legacy notes, and a list **Page changes needing authorization**: `page | exact change | dependents | status: proposed`. Dates are fictional-causal only.

## Worked example
Request in explore mode: "Three waves where the Lowland Crown takes Harl Bridge and breaks the Ferrymen's Compact, with the page updates for each wave." The Compact page is accepted and the history ledger is protected. Write the three waves as a new roadmap page: pressure from the toll dispute (wave 1), a contested crossing (wave 2), and the Compact's collapse as one branch (wave 3), with the other branch being a negotiated seat. The list *Page changes needing authorization* names the Compact page and the ledger with each change; none is applied. Each wave's Invariant check cites the rules it respects.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Writing the planned conquest onto the protected page | List it as a proposal and ask |
| One path as if the event must succeed | Branches for success, failure and not attempted |
| A cliffhanger every wave | End an arc when it ends |
| A forecast phrased as history | Mark it a plan, not canon |
| A release calendar | Fictional causality only |

## Acceptance
- Each wave follows specific established pressures and accounts for changed shared state.
- Later content has coherent entry points; future facts cannot be mistaken for released history.
- Protected-page changes appear only as proposals awaiting quoted authorization.
