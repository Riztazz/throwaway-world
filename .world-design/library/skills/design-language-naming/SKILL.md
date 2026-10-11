---
name: design-language-naming
description: Use when the user wants consistent personal names, place names, terminology, honorifics, or naming drift across communities; not a full language treatise.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Language & Naming

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill adds craft, not permissions.

## Use when / not when
Use when: names, terms, honorifics or aliases need a consistent system, or a new name must fit an existing convention.
Not when: a full grammar (only if asked), customs (`design-culture-everyday-life`), actual dialogue (`design-dialogue`), cultural review (`design-narrative-qa`).

## Before you write
1. **Search the index for the name first.** A name the world already uses, even in passing, is not new: reuse it, do not invent a second one. Say where it appears and what the world says about it.
2. A name for a place, person or thing that has no page, no location and no definition does not create one. Provide the name and the system, mark anything else (where it is, what it is) as unknown, and ask.
3. Read the existing naming page, the communities concerned and their migration or contact history. Naming pages are not protected, but changing an established name that other pages use is an `edit` with dependents.
4. Ask in facts: who uses these names, in which register, what language contact explains the sounds, what must stay unchanged.

## Procedure
1. State **Covers**: who uses the convention, where, in which register. A place can hold several traditions.
2. Define concise **Phonology**, **Place-name structure** and **Personal-name structure** with sample morphemes, meanings, title order and name changes.
3. Track endonyms, exonyms, titles, nicknames and disputed terms. Spelling variants are aliases of one stable identity.
4. Explain **Drift at barriers** through migration, trade, prestige, administration, diaspora and revival. A barrier can encourage divergence; it does not prove languages differ.
5. Show how to generate a new name and one plausible irregular historical name. Avoid accidental real or source proper nouns and invented etymology for real languages.
6. For localization, note pronunciation, transliteration, text expansion and sorting. Do not claim native-speaker approval without a review.
7. List **Consulted by**: who uses the spec. It helps them; it is never a prerequisite.

## Output
Use the naming page's section names:

```markdown
# <Culture or region> naming
::culture:: <culture>

## Covers
## Phonology
## Place-name structure
## Personal-name structure
## Drift at barriers
## Consulted by
```

A short alias glossary when aliases matter: `canonical | alias | who uses it | register`.

## Worked example
Request in extend mode: "Name the fishing village at the mouth of the Tarn and three of its lanes." The index shows no village at the mouth and a naming page for the Tarn communities (short two-syllable place names, a genitive suffix `-ar`, lanes named for the trade). Offer the name **Tarnmouth** if the page's pattern fits, or **Ostar** (an older `-ar` form) as an alternative, and lanes **Net Lane**, **Salter's Rise**, **Lamp Stair**. State what is not decided: whether the village exists in canon and where on the shore. Ask before it gets a page.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| A second name for something the world already names | Search first; reuse the existing name |
| A name that quietly creates a place, size or ruler | Name only; mark the rest unknown and ask |
| Geography as the only cause of sound change | Add contact, trade, prestige and administration |
| Invented etymology for a real language | Use original roots or say it is unreviewed |
| Changing an established name without listing dependents | Edit mode, with the pages that use it |

## Acceptance
- A writer can make and tell apart new names, and trace the important aliases.
- Variation is explained without making geography the only cause.
- No existing name was replaced, and no place was created by being named.
