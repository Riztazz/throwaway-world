---
name: design-geography-ecology
description: Use when the user wants physical regions, climate, water, resources, habitats, or ecological constraints for a world; atlas drawing is a separate handoff.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Geography & Ecology

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill adds craft, not permissions.

## Use when / not when
Use when: a region's water, barriers, resources, climate and ecology need defining or checking.
Not when: how a people live there (`design-culture-everyday-life`), who rules it (`design-faction-culture`), drawing it (`design-cartographer`), assembling one place (`design-location-bible`).

## Before you write
1. Read `INDEX.md`, the neighbouring regions, the map's gazetteer and scale, and the physical-rules page. The magic or physical-rules page is protected: it fixes what powers can do and how far. A region that needs a rule to be different (water drawn across distance, power stored, effects through stone) is a protected change. Say which invariant blocks it and offer a version that fits.
2. Read open decisions about the region.
3. Ask in facts: what water exists and where it goes, what blocks travel, what can be grown, mined or caught, what the seasons do, what depends on the neighbours.

## Procedure
1. Set scale, neighbours, climate and seasons, water supply and drainage. Record uncertain positions; do not invent fixed geography from an attractive layout.
2. Trace **Water -> Barriers -> Resources -> Culture** as material opportunity and pressure: settlement, movement, production, food, building materials, practical adaptation. History, trade and technology can produce different responses to the same terrain.
3. Describe habitats and ecology: producers, consumers, disturbance, seasonal movement, depletion and recovery. Check any magical dependency against the actual invariants, not genre habit.
4. Use a **Biome theme** only as a descriptive organising idea. Not every feature or resident must match it.
5. Check distances, drainage, resource access and dependence on adjacent regions. Keep physical barriers apart from political ones.
6. If an accepted position, extent or barrier changes, update the atlas in the same change or mark it stale with the correction.

## Output
Use the geography page's section names:

```markdown
# <Region>
::biome:: <biome>

## Water
## Barriers
## Resources
## Culture
## Biome theme
## Magic-invariant check
- INV-n <rule>: <how this region respects it>
```

Add climate, ecology, scale and neighbour constraints, sources and proposals as needed.

## Worked example
Request in explore mode: "A high ridge where callers can pull water up from the aquifer under the next oasis." The magic page fixes `::calling-reach:: 0 paces` (a calling moves water only from under the caller's feet). Report that the ridge cannot draw from the neighbouring oasis. Offer what fits: a ridge with its own seep line, where callers working at the foot of the cliff reach water the oasis does not, and a boundary dispute over which side the seep belongs to. The Magic-invariant check cites the reach rule. The magic page is unchanged.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Letting a power reach farther than the rules allow | Name the invariant; offer a fitting version |
| Terrain as a people's personality | Terrain gives options; history and trade choose |
| Every feature matching one biome | Treat the theme as description only |
| Fixed positions from a pretty layout | Mark positions as uncertain |
| An atlas left out of date after a change | Update it or mark it stale |

## Acceptance
- A reader can trace a settlement, route and livelihood to material conditions, and an ecological consequence of a change.
- Geographic constraint and cultural choice are separate.
- The magic-invariant check is filled in, and no protected page changed without quoted authorization.
