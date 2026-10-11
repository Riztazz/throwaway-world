---
name: design-canon-continuity
description: Use when the user wants canon registration, contradiction review, revision impact, retcon proposals, or continuity checks across world lore, fiction and released MMO content.
metadata:
  type: workflow
  family: world-bible-skills
  stage: review
compatibility: []
---

# Design: Canon & Continuity

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill reports and proposes; only the user accepts a change to protected canon.

## Use when / not when
Use when: contradictions must be found or fixed, a revision's impact traced, a retcon proposed, or new content registered against the baseline.
Not when: routing a multi-skill request (`design-world-bible`), runtime transitions (`design-persistent-world-state`), behaviour review of a deliverable (`design-narrative-qa`).

## Before you write
1. Read `INDEX.md`, `ledger/stale.md`, the fact lines involved (`canon_index.py facts --key <key>`) and the pages that link to and from them.
2. **Know what is protected** before choosing a fix: `accepted` pages and the core-rule types (magic system, tone and premise, cosmology, history, economy). When two pages disagree, the protected or higher-status page is the reference *for the proposal*; it is still only a proposal until the user says so.
3. Read decisions that touch the claim; a replaced decision is not a source.
4. Ask in facts: which claim matters most to scenes now, who decides, and what the user wants to keep.

## Procedure
1. Classify each important claim: author truth, attributed belief or report, audience knowledge, runtime state, future plan, released canon. Keep draft, reviewed, accepted and superseded as a separate axis.
2. Normalise ids, aliases, dates, scope and source revision. Two legitimate in-world accounts differ from two incompatible author facts.
3. Register only consequential additions and links for new artifacts. Incidental flavour needs no citation until content depends on it.
4. For a change to accepted material inspect direct dependants and reverse dependents (maps, characters, documents, quests, state, released text) and record retrieval limits.
5. Check timeline, ages, travel, numbers, physical invariants, motives and disclosure. Do not resolve source-stated unknowns.
6. Offer bounded resolutions: edit the draft, clarify attribution, update dependents, revise canon deliberately, or leave open. Never pick a winner silently, and early build order is not a reason to forbid revision.
7. **Edit the lower-status page to match, never the protected one.** If the fix is to edit a protected or `accepted` page, stop and ask once, naming the page, the change and the dependents. For a lower-status draft page, the edit may go ahead in edit mode, with a change record (`ledger/changes/`) and a refreshed `INDEX.md`.
8. Keep a dated contradiction log: evidence, revisions, severity, proposed action, owner, status, verification. A detected issue is not yet a confirmed defect.
9. After a story draft, list the consequential facts it established that the bible lacks in the story's `backflow.md` (fact, where, target page or field, dependents). Contradictions with protected pages are questions, not rows. Everything stays `proposed` for the user's batch review.
10. Return the proposed baseline and what needs acceptance. Do not claim a draft is accepted, a runtime change deployed, or a player's history migrated.

## Output
```markdown
## Baseline
## Claims and status
| claim | layer | status | source |
## Contradictions
| id | pages and values | evidence | severity | proposed resolution | owner |
## Impact
direct: ... reverse: ...
## Changes needing acceptance
## Remaining unknowns
```
Public-text edits are shown apart from author-only material.

## Worked example
Request in edit mode: "The guildhall's founding year differs between two pages; fix it." The guild page (draft) says 58, the ledger (history, protected) says 61, and nothing else mentions it. Treat 61 as the reference: edit the draft guild page's fact line and prose to 61, add a change record with the dependents (two pages link to the guild), refresh the index, and say plainly that 61 comes from the protected ledger and is a judgement from page status, not a decision the user made. The ledger is untouched. If the user prefers 58, the change is theirs to authorize on the ledger.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Editing the protected page to fit the draft | Edit the lower-status page; ask before touching the protected one |
| Choosing silently between two values | Cite both pages and say which you used and why |
| Calling a judgement a decision | Say it is page status, not the user's choice |
| Skipping the change record | Add a `ledger/changes/` entry (fields between `---` fences, per the template) and refresh the index |
| Inventing a cause for a deliberate unknown | Keep it unknown |

## Acceptance
- Another writer can identify the authoritative revision, see what remains proposed, and follow each revision to its dependents.
- Every chosen value cites its source and basis; no protected page changed without quoted authorization.
