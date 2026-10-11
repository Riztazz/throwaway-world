---
name: design-narrative-editing
description: Use when the user wants developmental, scene, exposition, dialogue or line editing of original fiction and narrative text while preserving intent, canon and an original style brief.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Narrative Editing

> Binding rules live in `rules/` (modes, protected pages, decisions, page format; stories: `rules/STORIES.md`). Ask the task mode first. Editing a draft is not permission to change canon. **Before you reply, read `INDEX.md` and the pages behind every date, count, name and title in the draft** (reading is allowed in every mode, including `lock`); a reply that has not read them is incomplete, however short the edit.

## Use when / not when
Use when: a draft of original fiction or narrative text needs a developmental, scene, exposition, dialogue or line edit, and the user wants the edited text or a critique.
Not when: first drafts (`design-fiction-drafting`), settling which canon fact is right (`design-canon-continuity`), readiness and behaviour review (`design-narrative-qa`).

## Before you write
1. Read the draft, its intended form and effect, and the style brief or `voice.md`. Ask for the edit level if it was not given; otherwise choose a bounded pass and say which.
2. **Check every fact the draft states against the bible**, not only the ones you change: dates, counts, names, titles, who holds what. If the draft disagrees with a page, or two pages disagree with each other, say so, give both values with their sources, and ask which stands. Do not pick silently and do not edit a protected page to fit the draft.
3. Read decisions that touch the subject; a replaced decision is not a source.
4. Ask in facts: what should the reader feel at the end, what must stay, what is deliberate roughness.

## Procedure
1. Choose the level: developmental structure, scene causality and viewpoint, exposition and dialogue, line rhythm and clarity, or copy consistency. Honour a given level.
2. Developmental: desire and opposition, choices and consequences, change, pacing, promises and payoffs. Separate experiment from demonstrable failure.
3. Scene: orientation, pressure, turn, viewpoint, knowledge. Clarify action without explaining away deliberate ambiguity.
4. Exposition: unfamiliar concepts gain concrete meaning; history supports the scene; a required quest instruction stays explicit.
5. Line: keep voice, register, rhythm and deliberate roughness. Not every speaker is polished and not every sentence short. Use the original style brief, never a reference author's signature.
6. Propose consequential fact changes and new implications; never retcon quietly. Do not call an in-world biased claim an author error without checking attribution.
7. Apply the requested changes with a short rationale for major ones. If a structural choice cannot be settled, complete the independent edits and name the choice.
8. Other reviews belong to `design-narrative-qa`.

## Output
```markdown
## Edited text
<the revised draft>

## What changed and why
<three to six bullets, major edits only>

## Facts checked
| the draft states | page you checked | agrees or conflicts |

## Facts to confirm
| the draft says | the bible says (page) | needs your decision |
```

Every date, count, name and title the draft states gets a row in Facts checked, with the page you read. A row that conflicts also goes in Facts to confirm. An edit that carries a figure forward without a row for it is a defect, even when the figure looks harmless.

If critique was requested instead, a prioritised report: structural findings first, then material notes. No sentence-by-sentence commentary unless asked.

## Worked example
Request in edit mode: "Tighten this harbour-master's speech; it should read well aloud." The draft says "for the forty years since the Quay Charter". The index gives the charter at 63 AM in the ledger and at 61 AM on the quay's page, with the current year 103 AM. Edit for breath and rhythm, keep the speaker's blunt cadence, and leave the number out of the edited line. Under Facts to confirm: charter year differs (63 AM vs 61 AM), so "forty years" is unsettled; ask which stands. Neither page is edited.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Fixing the number to whichever page you saw first | Report both values and ask |
| Reading "keep its facts" as "do not check them" | It means do not invent or change them; still check each against the bible and report a disagreement instead of keeping it silently |
| Editing the sentence and never reading the page behind its date | Read the page, then fill Facts checked |
| Polishing every voice to the same register | Keep deliberate roughness and distinct speech |
| A generic critique when an edit was requested | Deliver the edited text |
| Quietly retconning a lore detail to improve a scene | Propose it under Facts to confirm |
| Imitating a reference author's signature style | Use the world's style brief |

## Acceptance
- The edit serves the stated effect and form and keeps deliberate voice and ambiguity.
- Demonstrable problems are fixed; consequential lore changes are visible, not hidden.
- Conflicting facts are reported with both sources; no protected page changed.
