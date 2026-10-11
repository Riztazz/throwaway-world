---
name: design-location-bible
description: Use when the user wants a named settlement, landmark, district, or place assembled from geography, control, history, inhabitants, and present life.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Location Bible

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill adds craft, not permissions.

## Use when / not when
Use when: a settlement, landmark, district or place needs one page that joins its terrain, control, history and present life.
Not when: finished descriptive prose (`design-world-description-exposition`), traces (`design-environmental-storytelling`), quests (`design-quest-narrative`), or a camera brief.

## Before you write
1. Read `INDEX.md`, the place's page if it exists, its region, and the pages that mention it. Open the faction pages that hold it.
2. Pages marked `accepted` are protected. A location page that is `accepted` can be added to in extend mode (new sections, new links) but its existing text, fact lines and controller are not changed without authorization naming the page and the change.
3. **Follow the newer accepted decision** for anything the place does (how tolls are paid, who runs it). Ignore a replaced rule even if an older page still shows it; if a page contradicts the newer decision, report it.
4. Read open decisions about the place; a controller under an open decision stays undecided in the text.
5. Ask in facts: who uses it, who controls it in practice, what happens there in a day, what the visitor must hand over or do.

## Procedure
1. Assemble **Region / terrain**: access, distances, neighbours, water and local resources. Use the naming rules.
2. Explain **Control**: who administers, owns, contests or informally runs the place. Keep legal title apart from practical power.
3. In **History here**, connect a few past causes to surviving fabric, habits, absences or disputes. Not every site carries an ancient catastrophe.
4. Identify **Present figures** and current life: work, movement, food and shelter, routines, visitors, hazards, competing uses. Retrieve only the people and institutions this place needs.
5. Record encounterable evidence and the viewpoints that pick different details. Description need not reveal every author-only secret.
6. Stage bounded missing facts with owner and consequences. A place may propose a bridgekeeper or an old toll without the whole bible; consequential additions are registered.
7. Update the atlas for accepted position or control changes, or flag what is stale.

## Output
Use the location page's section names:

```markdown
# <Place>
::region:: <region page>
::controlled-by:: <faction page, or undecided>

## Region / terrain
## Control
## History here
## Present figures
```

Add current life, discoverable details, disclosure notes and proposals as needed. Any new procedure is labelled *proposed* until the user accepts it.

## Worked example
Request in extend mode: "Add to the Heron Stair entry how the toll is collected, step by step." The entry is accepted. A later accepted decision says tolls are paid in stamped tally-clays, not coin (the older coin rule is replaced). Append a new section after the existing text: the clerk counts, the carter shows a clay stamped at the lower house, the stair-warden notches the clay, the clay is kept by the upper office. Mark the steps as proposed. Leave the existing text alone, and report that the older coin line on the neighbouring market page is stale.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Using the replaced payment rule | Check decision status; follow the newer one |
| Editing existing text on an accepted page | Extend with new sections; ask before changing existing text |
| Naming a controller under an open decision | Write `undecided` |
| An ancient catastrophe behind every site | A few causes tied to what survives |
| Treating the entry as a rendering specification | Terrain and use, not camera |

## Acceptance
- A reader can locate the place, say who uses and controls it, and tie one present feature to a cause.
- Every consequential fact is established or clearly proposed; the entry can support a scene.
- No protected text changed without quoted authorization; no replaced rule followed.
