---
name: design-cartographer
description: Use when the user wants to create or update an SVG atlas, world map, regional map, borders, or gazetteer consistent with the world's physical geography.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Cartographer

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. The map file and its manifest rows follow the handoff in `docs/WORLD-HANDOFF.md`; this skill adds craft, not permissions.

## Use when / not when
Use when: drawing or updating a world, regional or island map, its legend and scale, or its gazetteer.
Not when: the physical facts are missing (`design-geography-ecology`), a fact on an accepted page would change (`design-canon-continuity`), or the request is a gameplay camera, grid or renderer brief (a later production document).

## Before you write
1. Read `INDEX.md`, the geography and location pages, the cartography page if one exists, and the manifest's `maps` and `assets` rows. Open the existing SVG when you are updating one.
2. Collect what the text actually fixes: positions, distances, widths, directions, counts. Everything else you draw is a layout choice.
3. A name the world mentions but never defines (no page, no place in the geography) is **not drawn as a place**. Do not turn it into an island, town or region, and do not give it a size or a direction. List it in the gazetteer under "Named but not placed", say what the world says about it, and ask where it belongs.
4. Pages marked `accepted` and core-rule pages are protected (`rules/INVENTION.md`). You may show them as they are; you may not move, rename or reassign them on the map.
5. Ask in facts, not pictures: which places must be on this map, what scale the user cares about, and what the map is for (players, writers, both).

## Procedure
1. Set a `viewBox`, an orientation, and the distance unit. One SVG unit is one world unit; write the scale. If no real distance is known, say the scale is approximate.
2. Draw one top-level `<g>` per layer (land, water, routes, settlements, titles). Every shape sits inside a layer.
3. Mark each place a page should open as a direct child of a layer group with `data-id` (a unique slug) and `aria-label` (the name), and no `id`. Draw its shapes inside it. A `<text>` with the same words in that layer becomes its label.
4. Record each placement as **fixed** (the text constrains it) or **chosen** (layout proposal). A chosen position is not canon.
5. Show faction control and named locations only where entries exist. Mark contested or claimed control as such. A page blocked by an open decision gets no holder drawn.
6. Write the SVG once, then validate once: `py -3 .world-design/library/tools/svg_check.py world/world-map.svg --world . --map world-map.svg` (in the library itself, `py -3 tools/svg_check.py`). Fix errors. Treat label warnings as hints: they come from estimated text widths, not a render.
7. Say exactly which checks ran. If you have not seen the map rendered, say so.
8. When an existing atlas depends on a changed fact, update it with that change, or mark it stale and name the elements.

## Output
Files, in the world folder, with nothing else in `world/` but pages, pictures and maps:

```text
world/world-map.svg          the map (no pattern, gradient, filter, mask, marker, text-on-path, <image>, <script>)
manifest.json                assets row {"file":"world-map.svg","mediaType":"image/svg+xml"}
                             maps row   {"svg":"world-map.svg","places":{"<data-id>":"<page>.md"}}
world/<cartography>.md       type cartography, sections: Map Gazetteer, Legend, Scale
```

Gazetteer rows: `place | type | position (fixed or chosen) | source page and revision | uncertainty`. If the mode does not allow writing in `world/` yet, put the files in `design/map/` and give the exact manifest rows as a proposal.

## Worked example
Request in extend mode: "Map the Harrow Marches and show the toll cairn at Corbel." The index shows the Marches page, a ridge, a river, and Corbel mentioned in two pages with no page of its own and no position. Draw the ridge and river, mark the Marches as fixed from the page, and give the crossing a chosen position labelled in the legend. Do not draw Corbel: list it under "Named but not placed" with the two sentences that mention it, and ask which ridge side it is on. Validate once, report the check result, and state that the layout was not viewed.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Drawing a mentioned-but-undefined name as a new island, town or region | Leave it off the map, list it under "Named but not placed", and ask |
| Treating every drawn position as established | Mark fixed vs chosen in the gazetteer and the legend |
| Leaving the SVG in a side folder because it is unclear where it goes | `world/` takes map files; register them in the manifest |
| Validating with the old label script only | Run `svg_check` against the manifest; labels are hints |
| Claiming the layout is clean because no checker complained | Say it was not rendered unless you rendered it |
| Colouring a faction onto a place whose owner is an open decision | Show it as disputed, with no holder |

## Acceptance
- Fixed constraints match the text; chosen and uncertain placements are identifiable.
- No place appears on the map that the world does not define.
- `svg_check` reports no errors; the report says what was and was not verified.
- The cartography page states the scale and the legend, and the manifest rows match the SVG's `data-id` values.
