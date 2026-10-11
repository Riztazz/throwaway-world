---
name: design-reference-analysis
description: Use when the user wants evidence-based analysis of books, film, manga, anime, animation, manhwa, webtoons, or adaptations to extract transferable craft and worldbuilding techniques.
metadata:
  type: workflow
  family: world-bible-skills
  stage: reference
compatibility: []
---

# Design: Reference Analysis

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. Analysis is evidence about technique; it never becomes this world's canon and it never overrides it.

## Use when / not when
Use when: accessible works, excerpts or adaptations should be studied for a transferable technique or effect.
Not when: combining influences into an original proposal (`design-reference-synthesis`), a prose style brief (`design-world-description-exposition`).

## Before you write
1. Say what you can actually access: full text, an excerpt, a chapter or episode, a summary, a review, the user's recollection. If you have not read or seen the part in question, say **unread** for it. Do not describe a scene as if you had it open.
2. Read the world's own rules before you propose any transfer. A technique that depends on a power, reach or resource this world's invariants forbid (for instance, effects at a distance when the magic page sets reach to zero) **does not transfer as is**: record the technique, state which invariant blocks the transfer, and offer a version that fits, or ask whether the user wants to change the rule (a protected change).
3. Check `authoring/references/` for existing cards on the same work and reuse or extend them.
4. Ask only if missing evidence stops the specific analysis: which edition, which part, what effect matters, spoiler ceiling.

## Procedure
1. Inventory sources with version, language or translation, adaptation and coverage. A summary does not give full-work coverage.
2. Keep continuities apart: novel, manga, anime and webtoon changes get separate rows.
3. Record observations with page, chapter, episode, timecode or panel locators when you have them. Never invent a locator. Label secondary reporting.
4. Label each statement: **direct observation**, **interpretation**, **secondary report**, or **proposal**. Attribute disagreement to versions or sources.
5. Extract desired effect, demonstrated technique, medium dependence, possible original adaptation, and costs. Cover exposition, pacing, institutions, agency, image sequence, viewpoint, sound or mechanics only as the request needs.
6. Consider competing explanations and limited cases. An admired effect may rely on a medium that a persistent game or a short scene lacks.
7. Quote at most a few words where needed; otherwise paraphrase with a locator. User excerpts may be analysed but do not license imitation.
8. If evidence is unavailable, say what is missing and continue with what is accessible.

## Output
```markdown
## Source inventory
| source | version / language | coverage | access |
## Technique cards
- Effect: <what the reader feels>
- Technique: <how, with locator or "unread">
- Observation type: direct / interpretation / secondary / proposal
- Medium dependence:
- Transfer to this world: <fits / blocked by INV-n / needs a rule change the user decides>
- Cost and uncertainty:
```

## Worked example
Request in explore mode: "I like how a famous desert saga lets its water-sensers dry whole oases from far away. Analyze that and show how we could use it." Say the saga is **unread** unless the user supplies passages; record the technique as the user describes it (secondary report). The world's magic page fixes `::reach:: 0 paces`. Transfer: blocked by that invariant. Offer what fits: water-sensers who *locate* an aquifer by standing on it, with scarcity and rights conflicts carrying the same dramatic weight; or ask whether the user wants an exception to the invariant. Nothing is written to a world page.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Describing a scene you have not read | Mark it unread; use the user's account as a secondary report |
| Importing a power the world's rules forbid | Name the invariant; offer a fitting version |
| Quotations and plot summary | A few words at most; techniques, not plot |
| Merging novel and adaptation continuities | Separate rows |
| Treating analysis as lore | It is evidence only |

## Acceptance
- Every substantive conclusion has a locator or an explicit limit.
- Observation, interpretation and proposal are visibly different.
- Each transfer states whether it fits the world's invariants.
