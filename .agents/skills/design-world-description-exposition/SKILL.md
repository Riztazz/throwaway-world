---
name: design-world-description-exposition
description: Use when the user wants unfamiliar places, cultures, history or ideas made understandable through situated description, selective exposition, or an original prose style brief.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: World Description & Exposition

> Binding rules live in `rules/` (modes, protected pages, decisions, page format; stories: `rules/STORIES.md`). Ask the task mode first. Description makes canon readable; it never adds consequential canon.

## Use when / not when
Use when: a place, culture, history or idea must be made understandable through situated description, with finished prose as the deliverable.
Not when: traces in a place (`design-environmental-storytelling`), reveal routes (`design-knowledge-revelations`), a whole story's architecture (`design-fiction-drafting`).

## Before you write: look
1. Read the world's `voice.md` and the reference cards the loader gives your role (`py -3 .world-design/library/tools/context.py prepare --project . --role fiction-writer`). They are the style source, with the chain voice, category cards, role cards. Cards describe transferable techniques in this world's terms; they do not name authors to imitate (card format: [paraphrased study](references/malazan-description-study.md)).
2. Look up every place, person, object and institution you will describe in `INDEX.md` and with `canon_index.py facts`. Use the exact names and values. If the passage is for a story, its folder is `drafts/stories/<slug>/`.
3. **Description cannot explain what the world leaves open.** If the subject has a deliberately unexplained cause (a `Deliberately Unexplained` section, an `Unknown:` line), the narrator, character or document may *offer* a cause, attributed to a person who could believe it and contradicted or doubted somewhere in the text. The prose may not assert one as the truth. Say, in a note outside the text, which unknown you left open.
4. Read open decisions about the subject.
5. Ask in facts: who is looking and what do they want right now, what must the reader understand to follow the action, what may stay mysterious.

## Procedure
1. Make an original **style brief** from `voice.md` and the cards: viewpoint distance, narrator knowledge, sensory selection, rhythm, density, register, metaphor domain, exposition tolerance. If none exists, derive one from the request and say it is task-local.
2. Set a comprehension target: what must be understood now, what can be inferred, what may stay mysterious. Unfamiliar names alone are not difficulty.
3. Put perception in a body with a task: what this person notices because of work, danger, memory, status or need. Their judgment is not objective fact.
4. Explain unfamiliar ideas by concrete consequence (what a rule changes in labour, travel, obligation, safety, relationships) before or with the term.
5. Layer history through evidence: repairs over older work, reused names and materials, inherited law, absences, ritual, contested accounts. Choose causal details, not a catalogue of old proper nouns.
6. Control revelation and vocabulary load: known anchors, timely clarification, recurrence, perspective gaps. Keep unknowns without withholding a referent the next action needs.
7. Draft the finished prose, matched to the form: prose may dwell; dialogue needs motive; a tooltip needs instant orientation.
8. **Write a fact sheet** for the passage (`factsheets.md`): layout and distances, who is present, appearance facts. Any invented distance or object that others must agree with is tagged `{{new: type, "name"}}` and logged in `inventions.md` (stories), or listed as a proposal (non-story).
9. Cold-read check: who, where, what pressure is clear; what each new term means functionally; which uncertainty is deliberate. Claim a reader test only if one happened.

## Output
```markdown
## Passage
<finished original prose>

## Fact sheet
layout and distances | who is present | appearance facts | tagged new facts

## Notes (outside the text)
style brief used | what was left open on purpose | proposals
```

## Worked example
Request in explore mode: "Describe the market at Greywick at dawn, for a scene where a stranger arrives." The index shows Greywick, its guild hall and the tide table. Style brief from `voice.md`: close third, low density, no metaphors from the sea (the voice file bans them). The stranger notices the crates stacked against a wall that was clearly higher once (history by evidence), and the guild officer who checks hands, not faces. Fact sheet: the market is forty paces wide, the hall on the east side, four people named. New: a brazier-seller, `{{new: person, "the brazier-seller"}}`, logged as story-local. The cause of the flood line on the wall is not stated.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Explaining a cause the world leaves open | Attribute it, contradict it, or leave it |
| An encyclopaedia paragraph in the middle of action | Concrete consequence in the character's attention |
| Imitating a named author | Use the world's voice file and technique cards |
| No fact sheet | Add it in the same change |
| An invented distance or place with no tag | Tag it and log it |

## Acceptance
- The audience can follow the action and the unfamiliar ideas through concrete relations; chosen mystery stays deliberate.
- Details express viewpoint and history; the prose follows an original brief.
- A fact sheet exists, new facts are tagged or listed, and no deliberate unknown was resolved.
