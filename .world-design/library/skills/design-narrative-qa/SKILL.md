---
name: design-narrative-qa
description: Use when the user wants actionable review or test cases for quest clarity, narrative behavior, representation, accessibility/localization, or implementation handoffs; select only relevant modes.
metadata:
  type: workflow
  family: world-bible-skills
  stage: review
compatibility: []
---

# Design: Narrative QA

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). A review is read-only: it reports and never edits the artifact or the bible. Ask the task mode first (usually `lock`).

## Use when / not when
Use when: an artifact's observable contract needs review: quest clarity, branch and state behaviour, representation, access and localization, implementation handoff, or continuity and leaks.
Not when: editing the text (`design-narrative-editing`), deciding which fact stands (`design-canon-continuity`), implementation and player tests (separate authorised work).

## Before you write
1. Read the artifact and the pages it relies on. Pick the one or two lenses that fit the task and risk; one focused lens is usually enough.
2. **Compare every checkable fact in the artifact with the bible**, including facts the bible states twice. When two pages disagree, list both values with page paths; you do not choose and you do not edit.
3. Note protected pages and open decisions that touch the artifact, so findings say what cannot be changed without the user.
4. State the evidence you have (text only, a render, a test run). Say what you could not check.

## Procedure
1. Select the lens: **behaviour**, **culture and representation**, **access and localization**, **implementation handoff**, or **continuity and disclosure**.
2. Behaviour: goal and action clarity, cause and effect, branch commitments, missing or reordered clues, failure and re-entry, repetition, party differences, late join, stale shared state. Write concrete cases with expected results.
3. Culture: attributed versus narrator claims, internal variation, stereotype, whose agency is erased, exoticization, borrowed real-world cues. No claim of lived-experience review without one.
4. Access: reliance on colour, audio or timing alone, essential information, readable language and length, captions, variable context, plural and gender, translation expansion, glossary. Text inspection is not assistive-technology testing.
5. Handoff: conditions, events, state scopes, ids and import format against a real interface. If none is available, return questions and unverified assumptions; invent no schema.
6. Continuity: conflicts and leaks in the deliverable. Baseline and retcon impact go to `design-canon-continuity`.
7. For each finding give the evidence locator, impact, severity, a reproducible case where it applies, and a concrete fix or decision. Keep confirmed defect, credible risk and preference apart.
8. Retest only changed cases and state what was actually run.

## Output
```markdown
| # | lens | locator | evidence | expected / observed | impact | severity | proposed action | status |
```

Then behaviour cases (`given / when / expected`) and a coverage note: what was inspected, tested, inferred, and left unverified. A clean review lists its coverage and limits; it does not claim universal quality.

## Worked example
Request in lock mode: "Review the Vael Ferry quest text before it goes in." The quest tells players to "ask the ferrywoman at the east pier"; the location page puts the ferrywoman at the west pier, and the history page and the person's page give different years for the ferry's founding (31 AM and 36 AM). Findings: (1) required-action locator wrong, a confirmed defect, severity high, fix: decide the pier; (2) founding year conflict, both values cited, decision for the user; (3) the clue is colour-only ("the red lamp"), access risk, add a second cue. Coverage: text only, no render, no test play.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Picking one of two conflicting pages | List both values with paths and ask who decides |
| Fixing the artifact while reviewing | Report; editing is a separate task |
| Running every lens on every artifact | One or two lenses that fit the risk |
| "Looks fine" with no coverage note | State what you inspected and could not check |
| Calling a text review a player test or a localization check | Label the evidence you actually had |

## Acceptance
- Findings are evidence-backed and actionable, and the lenses match the task.
- A reader can tell what was inspected, tested, inferred or left unverified.
- Nothing in the artifact or the bible was changed.
