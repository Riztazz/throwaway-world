---
name: design-character-bible
description: Use when the user wants named NPCs or fiction characters, their histories, motives, voices, relationships, and allegiances as lore rather than combat builds.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Character Bible

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill adds craft, not permissions.

## Use when / not when
Use when: a named person needs a history, motives, a voice and relationships, as an NPC or a fiction character.
Not when: scene dialogue (`design-dialogue`), a story arc (`design-fiction-drafting`), an NPC's shared state changes (`design-persistent-world-state`), or any combat build.

## Before you write
1. Search `INDEX.md` for the person's name, family, employer and the places they live. Reuse an existing person before inventing a second one.
2. Read the faction and location pages they belong to. An `accepted` faction or location is protected: you may link to it, and you may not change what it says about them.
3. Read open decisions about the person or their institution. A person whose affiliation is under an open decision gets no affiliation written.
4. Ask in facts: what do they want and what does it cost them, whom do they owe, what do they know that others do not, what would they never do.

## Procedure
1. Define allegiance (or a principled lack of one), circumstances, personal history, desire, fear, obligation and a contradiction or vulnerability.
2. Tie the person to specific events or local circumstances where it matters. A small character need not have witnessed a famous war; missing history may be a staged proposal.
3. Describe appearance through material life, habit and action. Keep author facts, self-description and other people's biased judgements apart.
4. Set the voice: vocabulary, rhythm, register, omissions, status behaviour. Original traits, not imitation of a source character.
5. Map only the relationships that matter: what each wants from the other, who knows more, where the leverage is, how it could change.
6. For a persistent NPC, separate shared-life facts from individual conversations. Deaths, appointments and departures are state decisions, not biography.
7. If the world gives an innate or learned power, a lore character may have it consistently. That is not class eligibility, damage or an unlock.

## Output
Use the character page's section names:

```markdown
# <Name>
<who they are in two sentences>

::faction:: <faction page>
::role:: <role>

## Allegiance
## Personal history
## Appearance
## Voice / personality
```

Knowledge boundaries and spoiler-sensitive facts go in a separate section or file, not in the public description.

## Worked example
Request in explore mode: "Make me the apprentice at the toll bridge." The index shows the Corbel Toll Office (a faction page, accepted) and a bridge location. Write **Ilse Brann**, apprentice clerk. Allegiance: the Office, by contract, not belief. History: orphaned by a ferry sinking before the bridge, which is why she counts boats twice. Appearance: ink-stained cuffs, a borrowed coat sized for the senior clerk. Voice: exact, apologises before refusing. Relationship: owes the senior clerk her place; wants to be the one who finds the Office's missing ledger. Not written: who sold the ledger (open decision), and nothing the accepted Office page already fixes about its rates.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| A person who is only their job | Give a want, a fear and one contradiction |
| Claiming they saw a famous event | Check the dates; propose, do not assert |
| Changing the faction page to suit the character | Link to it; a protected page stays as it is |
| Copying a source character's catchphrases | Build the voice from this world's speech |
| Letting each player author the shared biography | Shared facts are canon; conversations are individual |

## Acceptance
- Choices follow specific wants and pressures, and the voice separates the person from their role.
- History and powers fit established lore; private knowledge is not in player-facing text.
- No protected page was changed, and every new fact is marked established or proposed.
