---
paths:
  - "ledger/**"
---

<!-- Generated from rules/INVENTION.md by the bootstrapper; do not edit. Loaded when a matching file is read or edited. -->

# Invention and editing rules

Applies to every role, every provider, every world. These rules exist so agents never *silently* invent, overwrite or contradict canon. They do **not** limit invention: in `explore` mode you may create anything; the only cost is a log line.

## 1. Ask first

1. At the start of a task, ask the user for the **mode** (`explore`, `extend`, `edit`, `lock`). Do not infer it. If the task packet already contains `mode:`, use it (this is how evals and delegated workers run).
2. For a **new deliverable**, interview before drafting. Ask in facts, function, cost, history and relations ("what does it cost, who controls it, what changed it"). Never ask the user to picture, imagine or describe how something looks.
3. A subagent cannot ask the user. It returns the question to the coordinator and stops that part of the work.
4. Assume only what the user told you not to ask about. Label every other assumption as a proposal (section 5).

## 2. Words used below

| Term | Meaning |
|---|---|
| Page | A file in `world/` with a row in `manifest.json`. |
| Protected | Pages with manifest `status: accepted`, **plus** every page of a core-rule type: `magic-system`, `tone-premise`, `cosmology`, `history`, `economy` (even while `draft`). |
| Dependent | A page that links to the page being changed (reverse link). Query with the index tool. |
| Fact line | A `::key:: value` line in a page. Treat a change to a protected page's fact line as a change to canon. |

## 3. What kind of change is it?

| Class | What it is | Record required | May you do it? |
|---|---|---|---|
| **T0 retrieve** | You use existing canon. | None. Cite the page you used. | Always. |
| **T1 local** | Story-local detail nothing else must agree with (a minor cook, a cup, a one-off remark). | None. | Always. |
| **T1b additive** | A new world-level thing that contradicts no protected page and no fact line: a river, road, village, minor institution, minor character. | One line in `ledger/log.md` (stories: one line in the story's `inventions.md` plus a `{{new: type, "name"}}` tag in the text). | Yes, after you looked it up first (section 6) and found no existing equivalent. |
| **T2 consequential** | New content that other pages will depend on or that shapes the world (a faction's goal, a new rule of how something works, a historical event). | A change record with status `proposed`, listing expected dependents. | Yes as a proposal. It is not canon until integrated or accepted. |
| **T3 protected** | Any edit to, or contradiction of, a protected page or its fact lines. | A full change record with the user's exact authorizing words, dependents and what stays unchanged. | **Only after the user explicitly authorizes it.** Otherwise stop and ask. |

If two classes seem to fit, take the higher one.

**What counts as T3 authorization.** The user's own words that name the protected page or fact line and say the change may be made, given after you told them it is protected. A task request ("add X to the timeline") is not authorization, even when it names the page. Ask once: the page, the exact change, the pages that depend on it. Then wait, and quote the answer in the change record. The authorization covers that change only: when the user approves a checkpoint (`canon_index.py snapshot`), the T3 records written so far are spent, and a later change to the same protected page needs a new question and a new record.

## 4. Modes

| Mode | You may | You may not |
|---|---|---|
| `explore` | Create new pages and new content freely (T0-T2). Add links *from* your new pages. | Edit any existing page. |
| `extend` | Add new pages and add links or new sections around existing non-protected pages (T0-T2). | Change or delete existing text; touch protected pages. |
| `edit` | Change existing non-protected pages, each with a change record. | Touch protected pages without T3 authorization. |
| `lock` | Read, analyze and report. | Write anything in the target set. |

Nothing in any mode lets you set `status: accepted`. Only the user does that.

## 5. Records (small on purpose)

- **Log line** (`ledger/log.md`): `YYYY-MM-DD | <page-or-story> | T1b | <what> | <role>`.
- **Change record** (`ledger/changes/<id>.md`, template in `templates/world/ledger/changes/_template.md`; the fields are YAML frontmatter between two `---` lines, summary below them, and a record without the fences fails the lint): id, mode, tier (exactly `T1b`, `T2` or `T3`; there is no `T1` record: use `T1b` for the smallest edit), pages (page file names such as `salt-throne.md`; the lint also accepts the bare slug), dependents, status (`proposed`, `integrated`, `accepted`, `rejected`), authority (T3), summary of at most five lines.
- A **proposal** is a change record with status `proposed`. Content from a proposal may sit in `drafts/` or in `world/` as `draft`; it must never be described as established canon.
- Task packets are needed only when you delegate to a subagent.

## 6. Read before you write (`extend` and `edit` always; `explore` when the topic overlaps existing pages)

1. Open `INDEX.md` (generated from the manifest) and search it for the names and ideas your task touches. Look for existing equivalents before inventing: a second river, a second guild with another name, a duplicate rule.
2. Open only the pages that matter, plus the pages they link to and the pages that link to them.
3. Read the decisions that affect those pages (`decisions/`; see `rules/DECISIONS.md`) and `decisions/INBOX.md`.
4. Reuse what exists. Invent only what is genuinely missing, and use the lowest class in section 3 that fits.
5. Work by other agents in `drafts/` or `design/` is readable context. Cite its path. It is **not** canon until the user promotes it into `world/`.

## 7. Stop and ask when

- an open decision marked `blocking` affects the pages you would touch;
- your work would be T3 (protected page or fact line);
- two sources of canon disagree and the task needs one of them;
- a missing fact would materially change the result and the user has not told you to assume.

Everything else: proceed, label assumptions as proposals, and keep going.

## 8. Never

- Rename or delete a page that other pages link to. Set it `superseded` and add the replacement.
- Present a proposal, draft or reviewer opinion as accepted canon.
- Mark anything `accepted`.
- Merge two characters, places or factions that share a name; disambiguate the slug instead.
- Write into `world/` anything that is not a page, picture or map (see `docs/WORLD-HANDOFF.md`).

## 9. Canon custodian integration (the only auto-accept)

The canon custodian may integrate a proposal into `world/` with `status: reviewed` (never `accepted`) when **all** hold: the class is T1b or T2; no protected page links to the page being changed (a protected page is not a dependent of a *new* page, and a new page that merely links to protected pages is fine); no core-rule type is involved; and the batch is at most 10 pages. Everything else waits for the user's batch review.

## 10. Finish with this check

1. Which mode did I use, and did I stay inside it?
2. Is every new world-level thing logged or proposed, and does every proposal list its dependents?
3. Did I touch a protected page or fact line? If yes, where is the user's authorization?
4. Did I look in `INDEX.md` before inventing anything?
5. Did I mark anything `accepted`? (It must be no.)
6. What did I leave open for the user, and is it in `decisions/INBOX.md`?

## What checks these rules

| Rule | Checked by |
|---|---|
| Protected page or fact line changed with no change record naming authority | `tools/canon_lint.py` (A4), compared with `ledger/page-hashes.json` |
| `edit` or `lock` violations | change record `mode` vs what changed (lint) |
| Unresolved `{{new:` tag in a story marked final | lint |
| Open blocking decision touching changed pages | lint |
| The same event fact (`::toll-war-ended::`) with different values on two pages; an event that ends before it begins | lint warnings `L-FACT-CONFLICT` and `L-FACT-ORDER` (event keys only: `<subject>-<event verb>`; generic per-page keys such as `founded` or `born` are not compared). Report both values and ask; never pick one silently |
| Invention without an index lookup, prose-level drift, contradictions between differently named keys | evals (Phase B) and the custodian, not the lint |
