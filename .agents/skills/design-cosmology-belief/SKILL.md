---
name: design-cosmology-belief
description: Use when the user wants religions, cosmologies, rituals, sacred duties, taboos, or conflicting beliefs distinguished from the world's actual rules.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Cosmology & Belief

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A cosmology page is a core-rule type and therefore protected: this skill adds craft, not permission to edit one.

## Use when / not when
Use when: a community's beliefs, rituals, taboos or sacred duties need a page, or in-world belief must be told apart from the world's actual rules.
Not when: physical rules (`design-magic-system-fusion`), political power (`design-faction-culture`), how players discover the truth (`design-knowledge-revelations`).

## Before you write
1. Search `INDEX.md` for the community, the institution and any existing cosmology page. Open the physical-rules page: belief may be wrong about it, but your fact tags must not contradict it.
2. In explore mode write a new page. Changing an existing cosmology page, or contradicting one of its fact lines, is a protected change: stop and ask once, naming the page and the change (`rules/INVENTION.md`).
3. Read open decisions about the institution or the event the belief explains.
4. Ask in facts: who practises it and who does not, what does it cost them (time, money, a taboo), who gains from the official version, what do believers disagree about.

## Procedure
1. Name the adherents and the variations. Do not give a whole region or faction one religion.
2. Cover **Creation**, **Death and afterlife**, **Gods (or their absence)**, **Sacred and taboo** to the depth the task needs. A tradition may leave a question open.
3. Tag each claim as author fact, attributed belief or report, or deliberately unknown. A reported miracle is evidence of the report, not proof.
4. Design ritual by purpose, participants, timing, materials, obligations, exclusions and practical effect. Include daily practice and disagreement next to doctrine.
5. Describe **Institutions**: who interprets, teaches, funds, enforces or contests. A social prohibition is not a physical inability to use a power.
6. Link to the relevant places and events, and check the fact tags against the actual invariants while leaving contradictory readings in the world.
7. Allow exploitation, reform, syncretism, scepticism and ordinary devotion; do not flatten a tradition into its worst institution.

## Output
Use the cosmology page's section names:

```markdown
# <Belief or tradition>
<who holds it, in two sentences>

## Creation
## Death and afterlife
## Gods (or their absence)
## Sacred and taboo
## Belief-vs-fact tags
- claim | author fact / attributed belief / deliberately unknown | who says so
## Cites
## Institutions
```

## Worked example
Request in explore mode: "What do the river-folk believe about the Long Flood?" The index shows a flood in the history ledger (cause listed as unexplained) and a river guild. Write the **Silt Reckoning**: the flood was a debt called in by the river, and a share of every catch is returned each autumn. Tags: the flood happened (author fact, from the ledger); it was a debt (attributed belief, river-folk); why it began (deliberately unknown, matching the ledger). Ritual: the Returning, with who attends and who is excluded (debtors to the guild). Institutions: the guild's tally-priests, who also fix the share, and a dissenting sect that refuses the share. The ledger page is not edited.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Belief that is always secretly false | Beliefs may be accurate, mistaken or open; tag each |
| A miracle stated as fact | Record it as a report with who made it |
| One religion per region | Name adherents and variations |
| Settling the cause the history page leaves unexplained | Keep it unknown and tag it so |
| Editing the existing cosmology page to add a rite | New page, or ask for authorization naming the page |

## Acceptance
- A reader can tell what is true from what specific people claim, and how the practice shapes daily life.
- Different members have a reason for different readings.
- No protected page or fact line was changed without quoted authorization.
