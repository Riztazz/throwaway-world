---
name: design-tone-premise
description: Use when the user wants a world premise, tone, player fantasy, reader experience, or testable design pillars before or during worldbuilding.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Tone & Premise

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. The premise page is a core-rule type and therefore protected: this skill adds craft, not permission to edit it.

## Use when / not when
Use when: a premise, tone, player fantasy or set of testable pillars is being established, or a proposed addition needs testing against the pillars.
Not when: world rules (`design-magic-system-fusion`), combining references (`design-reference-synthesis`), prose style (`design-world-description-exposition`).

## Before you write
1. Read the existing premise page, `voice.md`, the accepted decisions about tone and scope, and `decisions/INBOX.md`. Read the history and cosmology pages the new tone would touch.
2. **Changing an existing premise page or a pillar is a protected change, even when the page is only a draft.** A request to "rework the tone", "make it grimmer", or "update the tone page" is a task, not authorization. Stop and ask once: name the page, the exact change (what the premise would say instead), and the pages that depend on it. Offer the rewrite as a proposal in `design/` for the user to read first.
3. A new tone rule must not state something the world leaves open as fact. A grimmer premise that says "the guilds secretly cause the Still Days" settles a deliberate unknown; keep the unknown as a rumour or a rival reading, or ask the user to decide the cause.
4. Ask in facts: what keeps happening in this world, who suffers or benefits, what a scene must never do, what the audience feels at the end of a session.

## Procedure
1. State the central situation and the recurring pressure in one or two sentences. Show what is distinct by its consequences, not by borrowed features.
2. Describe player agency in a shared world, or the experience of following one viewpoint. No assumption that every player is the exclusive saviour.
3. Set tone guardrails: how humour, horror, intimacy, violence and ambiguity fit. No single mood is mandatory in every scene.
4. Write three to eight pillars, each with a practical content test and a counterexample. Keep themes apart from physical invariants.
5. If references were supplied, keep their weights and send evidence questions to `design-reference-analysis`. Genre conventions are options, not facts.
6. Separate unresolved choices from approved premise.

## Output
Use the premise page's section names:

```markdown
# <World> premise
## Premise
## Player Fantasy / Reader Experience
## Tone Guardrails
## Design Pillars
- <pillar> | test: <what a scene must do> | counterexample: <what breaks it>
```

Plus the output form and an optional list of unresolved decisions.

## Worked example
Request in edit mode: "Tighten the premise so the harbour feels more claustrophobic." The premise page is a draft but protected by type. Do not edit. Write a proposal in `design/premise-claustrophobic.md`: the new Tone Guardrails line ("rooms are small, sky is rarely visible, exits cost something") and a replacement pillar with its test and counterexample. Ask: "May I change `tone-premise.md` to this? It affects the location pages that cite the premise." Wait for the user's words before touching the page.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Editing the premise page because it is only a draft | It is protected by type; propose and ask |
| A grimmer tone that settles a deliberate unknown | Keep it as rumour or a rival reading |
| Pillars with no test | Add a content test and a counterexample |
| A theme stated as a law of physics | Keep themes apart from invariants |
| One mood in every scene | Guardrails allow range |

## Acceptance
- A writer can state the central pressure, pick a fitting tone for a scene and test an addition against the pillars.
- No protected page changed without quoted authorization; open questions are listed, not settled.
