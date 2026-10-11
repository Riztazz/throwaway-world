---
name: design-trivia-flavor
description: Use when the user wants ambient texture, sayings, codex entries, letters, chronicles, signs, or other in-world texts; actual live events and quests use dedicated skills.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Trivia, Flavor & In-world Documents

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. Texture is free; a claim that others will rely on is not texture.

## Use when / not when
Use when: ambient detail, sayings, a codex entry, a letter, a sign or a chronicle is wanted, with a situated author and audience.
Not when: a multiplayer event (`design-live-events`), essential clue paths (`design-knowledge-revelations`), broader explanatory scenes (`design-world-description-exposition`).

## Before you write
1. Search `INDEX.md` for every proper noun the text will mention. Open what the world says about each.
2. **A name the world uses but never defines stays undefined.** If the request asks for the signers, date or clauses of something that has only been cited (an agreement, a treaty, a founding), those are consequential facts: do not write them as established. Offer a few lines that use only what the world states, and a short list of *bounded proposals* clearly labelled as such for the user to pick from, or ask first. Never put an invented date, signatory or clause into a line a player will read as true without that label.
3. Read open decisions and follow the newer accepted ones.
4. Incidental flavour is not a page type; it goes to `design/flavor/<slug>.md`, or into the trivia page's sections if the user wants it in `world/`.
5. Ask in facts: who is speaking, to whom, when, and what must the reader learn from it.

## Procedure
1. Choose **incidental flavour** or **document / codex** mode.
2. Incidental: concrete ambient happenings, sayings, food, objects, customs. Stay inside established rules; attribute rumours. Do not turn a festival into a consequential event by accident.
3. Document: purpose, author or institution, audience, provenance, bias. List the facts it conveys with sources, or mark them proposals. State whether the text is authoritative or diegetic.
4. Decide what the author would know, omit, distort or stress. A dated letter may be out of date without the bible being wrong.
5. Draft to the medium: sign, item text, log, chronicle, letter, entry. Required actions stay plain; ambiguity belongs in optional interpretation.
6. Review each addition for consequence. When it becomes a cause, a rule, an institution, an essential clue or a runtime change, promote it to the right entry with provenance; the flavour exception stops there.
7. For reference-derived text use original wording and keep a provenance note.

## Output
Incidental mode, the trivia page's sections:

```markdown
## World Events (ambient, current)
## Trivia & Flavor
```

Document mode: the finished text plus a note outside the public text: author, audience, date, truth status, and the source of each consequential fact. Proposals are labelled `[proposed]` inline or in the note.

## Worked example
Request in explore mode: "Ten tavern lines about the Salt Pact: who signed it, when, what it says." The world cites the Pact in two pages and defines nothing else. Write six lines using only what is stated (it sets the road tariff, the Throne holds the gate) and four *rumour* lines clearly attributed to drinkers ("they say it was signed at the dry well, though nobody agrees"). Beneath them, a list for the user: *signers, date and clauses are undefined; here are three options for each, with what each would clash with.* No line states a date or signatory as fact.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Writing the signers, date and clauses of a cited-only agreement as fact | Use what is stated; attribute the rest as rumour; list proposals |
| A rumour that the bible later has to honour | Label it, and keep it deletable |
| A document with no author or audience | State both; choose what they would omit |
| A bulleted template forced on a letter | Write the letter as a letter |
| Flavour that quietly becomes a cause | Promote it with provenance |

## Acceptance
- Flavour can be removed without breaking a causal fact; a document's author and purpose explain its claims.
- Consequential claims have a source or a proposal label; undefined things stay undefined.
