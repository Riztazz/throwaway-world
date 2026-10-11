---
name: design-environmental-storytelling
description: Use when the user wants an established event or world fact conveyed through discoverable physical, social, or sensory traces rather than direct explanation.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Environmental Storytelling

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A trace invites an inference; it must never settle what the world leaves open.

## Use when / not when
Use when: an established event or fact should reach the player through traces in a place: remnants, repairs, absences, changed routines.
Not when: a new history ledger (`design-history-timeline`), a visual or camera brief (a later production document), broader situated description (`design-world-description-exposition`).

## Before you write
1. Read the pages for the fact, the place and the people who would have left traces. Find the cause behind the trace in the bible.
2. **A trace may point toward a cause only if the world states one.** If the cause is marked deliberately unexplained (a `Deliberately Unexplained` section, an `Unknown:` line, an open decision), design traces that fit several readings and prove none: damage that fits more than one cause, accounts that disagree, a repair with no recorded reason. Do not leave a clue that only one explanation fits.
3. Read open decisions about the place. A trace of who holds a place under an open decision shows the dispute, not a holder.
4. Evidence is not a page type. Save it as `design/traces/<slug>.md`; a new page is a separate proposal.
5. Ask in facts: what happened, when, who was there, who has been back since, what the observer can perceive and what they need to learn.

## Procedure
1. **Cites**: name the cause or attributed account behind the trace. If absent, stage a bounded proposal; do not hide an invented fact behind suggestive detail.
2. **The index**: derive the remnants, repairs, absences, changed routines, materials, reused space or social behaviour that the fact plausibly caused.
3. Layer age and interference: weathering, reuse, concealment, propaganda, restoration, competing histories. State what the evidence supports and what it cannot prove.
4. **Placement**: where and when an observer meets it, and what they can actually perceive. Do not dictate camera or rendering.
5. Optional traces must survive being missed. For a necessary deduction, route redundant routes to `design-knowledge-revelations` and the action to `design-quest-narrative`; a clue is never the only blocker.
6. Check timing and persistence: before and after the event, stale client knowledge, restoration, one player consuming a shared object. Record runtime needs as a handoff.

## Output
```markdown
## Cites
## The index
- trace | what it shows | what it cannot prove | age or interference
## Placement
Optional or required: ...
Alternate readings: ...
Missing-fact proposals: ...
```

## Worked example
Request in explore mode: "Traces at the sluice house of what happened the night the lamps failed." The ledger marks the cause as deliberately unexplained and two accounts disagree. Traces: a scorched lintel (fits fire or a lightning strike), a mended shutter with new nails (someone returned), a log with the night's page torn out (hidden, or lost). Cites: the ledger entry and both accounts. The alternate readings are listed; no trace names a culprit. Optional: yes; the fact that the lamps failed that night is delivered by a required instruction elsewhere. Nothing is written to the ledger.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| A clue that only one explanation fits for a deliberate unknown | Traces that fit several readings |
| Inventing the cause and hiding it in props | Cite a world fact or label a proposal |
| Evidence that proves more than it can | State what it cannot prove |
| An optional clue that blocks the quest | Route essential information elsewhere |
| A holder shown for a disputed place | Show the dispute |

## Acceptance
- An observer can form a plausible inference without the evidence proving more than it supports.
- Deliberate unknowns stay unknown; missing optional detail cannot make a quest incomprehensible.
- Required clues have an explicit handoff.
