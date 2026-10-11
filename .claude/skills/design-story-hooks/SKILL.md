---
name: design-story-hooks
description: Use when the user wants grounded story or quest seeds from unresolved world tensions; excludes objective graphs, scene outlines, rewards and event scripts.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Story Hooks

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A hook is a seed; it never settles what the world leaves open.

## Use when / not when
Use when: unresolved tensions in the world should become grounded seeds a writer or quest designer can grow.
Not when: objectives and branches (`design-quest-narrative`), scene outlines (`design-fiction-drafting`), future shared consequences (`design-live-narrative-roadmap`).

## Before you write
1. Read the pages that hold the tension and the pages that cite them. Note what the world states, what it marks deliberately unexplained, and what is under an open decision.
2. **A hook may rest on a deliberate unknown but may not answer it.** A request to base a hook "on what truly caused X" when X is deliberately unexplained is a request for the answer: do not supply it. Write hooks that grow from the unknown: competing accounts, an anomaly that fits more than one reading, someone who profits from either answer. Say that you did this and why, and offer to record a cause only if the user decides one.
3. Read open decisions; a hook may use the dispute but not its result.
4. Hooks are drafted as pages of type `story-hook` only in extend or explore mode; otherwise save to `design/hooks/<slug>.md`.
5. Ask in facts: who is stuck, what do they want, who benefits from the delay, how does an ordinary person run into it.

## Procedure
1. Pick a specific unsettled cause, want or dependency. Open the actual entry at the working revision.
2. **Cites**: the facts that drive the tension. A missing link may be a labelled bounded proposal.
3. **Who cares**: why it stays unresolved and how someone meets the pressure.
4. **What changes on resolution**: concrete stakes and more than one plausible direction. Keep participant agency; no exclusive chosen hero.
5. Make hooks distinct. Do not repeat one resource dispute under several names. Rank only if asked.
6. Stop at the seed. Objectives go to `design-quest-narrative`; scenes to `design-fiction-drafting`; shared futures to `design-live-narrative-roadmap`.

## Output
Use the hook page's section names:

```markdown
# <Hook>
::location:: <location page>

## Cites
## Who cares
## What changes on resolution
```

An encounter premise is optional. No minimum number of hooks.

## Worked example
Request in explore mode: "Three hooks about the Dark Winter, each resting on what truly caused the lamps to fail." The ledger says the cause is deliberately unexplained and two chronicles disagree. Write three hooks that start from the gap: (1) a lamp-wright's ledger that fits both chronicles, wanted by the guild that profits from either; (2) a village that burned its own beacon that winter and says so only when drunk; (3) an auditor who is paid to prove the cause and has been told which answer to find. Each cites the ledger and the chronicles. None states a cause. A note to the user: the true cause is theirs to set.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Supplying the cause because the prompt asks for it | Write from the gap; say the cause is the user's to set |
| Three hooks about one dispute | Differentiate them |
| An objective list or a scene outline | Stop at the seed |
| Naming the winner of an open decision | Use the dispute, not the result |
| A chosen hero as the only resolver | Keep several routes for participants |

## Acceptance
- A writer can name the tension, the interested parties and a consequential choice.
- Hooks are grounded in cited facts and leave room for the plot or quest.
- No deliberate unknown is answered and no open decision is settled.
