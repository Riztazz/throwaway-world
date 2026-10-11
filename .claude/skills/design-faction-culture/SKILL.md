---
name: design-faction-culture
description: Use when the user wants factions, institutions, politics, authority, goals, obstacles, contacts, or meaningful relationships between powers.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Faction & Culture

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill adds craft, not permissions.

## Use when / not when
Use when: an institution that acts in the world needs a page, or powers need real relationships. One faction is a valid task; there is no minimum count and no all-to-all hostility.
Not when: everyday life of a community (`design-culture-everyday-life`), a person (`design-character-bible`), runtime reputation (`design-narrative-systems`).

## Before you write
1. Search `INDEX.md` for the faction, its region, its rivals and the places it holds. Open those pages and the history and economy pages that explain its resources.
2. Factions marked `accepted` are protected. You may link to them; giving one a new seat, territory or controller is a protected change. Stop and ask once, naming the page, the exact change and the pages that depend on it (`rules/INVENTION.md`). A request like "give them more power" is a task, not authorization.
3. Read open decisions about the faction. A page blocked by an open decision gets no ruling written on that question.
4. Ask in facts: what does it want, what blocks it, how is it paid for, who can overrule it, who inside disagrees, how does an ordinary person meet it.

## Procedure
1. Define membership, legitimacy, governance, jurisdiction, material base, coercion and accountability where they matter.
2. Fill **Goals**, **Obstacles** and **Player Connections**: concrete aims, why they stay unresolved, and how someone meets, helps, resists or negotiates with the institution.
3. **Mechanic Ownership Map** names who controls or contests which world resources and institutions, and any narrative-system duties already chosen. It is an app heading, not licence to invent class locks or balance.
4. Tie motives to established facts. Missing founding or resource facts go in a short proposals list; they do not block the draft.
5. Build a scoped relationship graph: parties, cooperation, friction or dependence, stake, evidence, direction, instability. Leave out pairs with no real relationship. Factions can disagree internally.
6. Describe **Culture** as institutional practice, symbols and membership variation. Check class, generation, dissent and overlapping loyalties.
7. When territory changes, update an existing atlas or mark it stale.

## Output
Use the faction page's section names:

```markdown
# <Faction>
<what it is and what it wants, in two sentences>

::region:: <region page>
::color:: <hex>

## Goals
## Obstacles
## Player Connections
## Mechanic Ownership Map
## Cites
## Culture
```

A relationship table lists only meaningful edges: `party A | party B | kind | stake | evidence`.

## Worked example
Request in explore mode: "A river-toll brotherhood on the Calder." The index shows the Calder, a trade road and the Mercers' Hall (a faction page, accepted). Write the **Calder Wardens**: Goals (keep the ford open for a fee), Obstacles (the Hall wants free passage, the upland reeves want a share), Player Connections (carters buy a stamped token; fugitives bribe a ferryman), Culture (they swear at low water and share a salted meal). Relationship edges: Hall (friction over the fee, evidence: the Hall's tariff page), reeves (dependence). The Hall's page is linked and unchanged. Proposed: the founding year.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Making a faction a culture, species or whole region | Members, rules and leaders; culture is one section |
| Everyone hates everyone | Only edges with a stake and evidence |
| Moving seats, territory or control on an accepted faction page | Ask once with the exact change and dependents |
| Resolving a rival's open decision to fit the plot | Leave the question open and say which decision blocks it |
| A faction with no way for an ordinary person to meet it | Fill Player Connections with a concrete encounter |

## Acceptance
- A reader can say how the institution sustains itself, what it wants, what blocks it and how people meet it.
- Each relationship has a stake and evidence; dissent is not erased by the faction label.
- No protected page was changed without quoted authorization.
