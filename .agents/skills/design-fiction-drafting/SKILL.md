---
name: design-fiction-drafting
description: Use when the user wants an original short story, novella, chapter, scene, or fiction outline in an established or emerging world; excludes quest objective graphs.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Fiction Drafting

> Binding rules live in `rules/` (modes, protected pages, decisions; stories: `rules/STORIES.md`). Ask the task mode first. A story is a draft in `drafts/stories/<slug>/`, never a page in `world/`.

## Use when / not when
Use when: an original short story, novella, chapter, scene or outline is wanted in this world. An outline is a valid deliverable; do not replace a request for prose with planning alone.
Not when: quest objective graphs (`design-quest-narrative`), dialogue-only work (`design-dialogue`), editing an existing draft (`design-narrative-editing`).

## Before you write: look
1. Copy `drafts/stories/_template/` to `drafts/stories/<slug>/` if the story has no folder. To resume, read `story.md`, `scenes.md` and `timeline.md` first, not the whole prose.
2. List the world facts the outline needs: places, institutions, rules, history, people. Look each up in `INDEX.md` and with `canon_index.py facts --key <key>`. Use the exact names and values the pages give.
3. **Follow the newer accepted decision.** If a decision was replaced (who inherits, how tolls are paid, who rules), use the replacement everywhere, including in a character's assumptions. A character may *believe* the old rule only if the story says it is an outdated belief.
4. Read open decisions. A blocking decision stops the scenes that depend on it; write the others.
5. Read `voice.md` and the matching reference cards. Ask in facts, never pictures: what the character wants and what stops them, what the ending must do, what the reader knows that the character does not.

## Procedure
1. State the story question, the character's desire, the opposition, the stakes and the change. A hook is a seed; turn it into a causal problem.
2. Match the form. A short story needs concentrated pressure, a small cast and a decisive turn. A novella sustains evolving relationships and a few strands; do not pad with novel-scale subplots. A novel needs its chapter ledger and continuity ledger kept up to date per act, and a series its own series file (`rules/STORIES.md`, "Novels and series"); deliver ordered, complete chapters and never present a fragment as a finished novel.
3. Outline: opening pressure, complications, choices, turns, ending. Keep a supplied outline's intent and diagnose its gaps.
4. Plan each scene by viewpoint, immediate want, conflict, change and consequence into the next. Quiet scenes count when they do dramatic work.
5. **While drafting, invent but never silently** (zones from `rules/STORIES.md`):
   - *Story-local* (a minor cook, a cup): write it, no record.
   - *World-level addition* (a river, road, village, minor institution or person that contradicts nothing protected): look it up first and reuse an equivalent; otherwise write it, tag it `{{new: river, "the Lathe"}}`, and add an `open` row to `inventions.md`.
   - *Touches protected canon* (an `accepted` page, a core-rule page or a fact line): stop that scene, state the question, continue with the others.
6. Every descriptive passage gets an entry in `factsheets.md`: layout and distances, who is present, appearance facts. Invented distances are tagged like any other new fact.
7. Let the world in through action, perception and consequence. Dialogue follows motive and register; mystery does not excuse unorientable action. Keep a character's belief apart from the narrator's assertion.
8. Check causality, emotional progression, viewpoint knowledge, chronology and payoff. If one response cannot hold the work, deliver complete ordered sections and a remaining plan; never call a fragment a finished novella.
9. The story may be set `final` only when no `{{new: ...}}` tag remains and no `inventions.md` row is `open`.

## Output
The requested outline or prose in `prose/`, updated `scenes.md`, `timeline.md`, `inventions.md` and `factsheets.md`, plus questions that arose outside the story. Editorial notes stay out of the narrative.

## Worked example
Request in explore mode: "A scene where the new harbourmaster inspects the grain quay." The index shows the quay, the harbour office and an accepted decision that the harbourmaster is *elected* each seventh year (an earlier decision of inheritance was replaced). Write the scene with her campaign banner still in the office, and a clerk who remembers her predecessor losing the vote; not an heir. A new grain-weigher's lane gets `{{new: lane, "Weigher's Rise"}}` and an open row. Fact sheet: the quay is eleven paces wide, the office at the east end, three people present. The story stays `draft`.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Using a replaced rule because the old page text still shows it | Check decision status; follow the newer one |
| Writing a new river or village without a tag | Tag it and add a row; keep writing |
| A scene that changes an accepted page or a fact line | Stop that scene and ask |
| Description with no fact sheet | Add the sheet in the same change |
| Calling a fragment a finished novella | Deliver ordered complete sections and say what remains |
| Using an author's signature phrases | Build from `voice.md` and the cards |

## Acceptance
- The form and length requested are delivered; choices have consequences; each scene changes something.
- Every new world-level detail is tagged and logged; no protected page or fact line contradicts the prose.
- Replaced decisions are not followed; unfinished sections are named honestly.
