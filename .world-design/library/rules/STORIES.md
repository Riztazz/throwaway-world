# Writing stories around the world

Applies to every role that writes fiction, dialogue or descriptive scenes for a story. It adds the story-specific parts of [INVENTION.md](INVENTION.md); everything there still applies. Stories are drafts: they live in `drafts/stories/<slug>/` and never in `world/`.

## One folder per story

Copy `drafts/stories/_template/` to `drafts/stories/<slug>/`. It holds:

| File | Purpose |
|---|---|
| `story.md` | status (`draft` or `final`), form (`short`, `novella` or `novel`), optional `series` and `book`, viewpoint contract, premise, continuity notes and the resume checkpoint |
| `outline.md` | the causal outline: want, opposition, stakes, turns, ending |
| `scenes.md` | the scene or chapter ledger: viewpoint, want, conflict, change, who knows what, status |
| `timeline.md` | story events in order, and what each character knows when |
| `inventions.md` | every world-level thing the story invented, and what happened to it |
| `backflow.md` | consequential facts the story established that the bible lacks, as proposals for the user's batch review |
| `factsheets.md` | a short sheet for each descriptive passage: layout and distances, who is present, appearance facts |
| `prose/` | the scenes themselves, one file per scene or chapter |

Short stories use the same structure; a novella adds chapters in `scenes.md` and per-chapter continuity in `story.md`. A novel and a series use the extra files below. To resume after a break read `story.md`, `scenes.md` and `timeline.md` first, not the whole prose.

## Novels and series

A story with `form: novel` also has, copied from `drafts/stories/_template-novel/`, `chapters.md` (the chapter ledger, grouped by act: viewpoint, time and place, what happens, facts established, open threads) and `continuity.md` (the running state of characters, objects, places, dates and reader knowledge, one section per act). Update both at the end of every chapter. A fact is not true in the story until `continuity.md` holds it with the chapter that set it, and every new chapter is checked against that file before it is drafted. To resume, read `story.md`, `chapters.md` and the latest act of `continuity.md`, not the prose. Reconcile inventions per act (the section below), and `final` still needs every tag and row closed.

A series lives in `drafts/series/<series>/`, copied from `drafts/series/_template/`: `series.md` (premise and arc, the books, **what readers know at the end of each book**, standing facts) and `continuity.md` (state carried from book to book). A book names its series with `series: <slug>` and `book: <n>` in `story.md`; the lint refuses a book whose series folder has no `series.md`. A series fact that the bible should hold goes through back-flow like any other; a fact only the series established stays in `series.md` and is not canon. A later book may not contradict an earlier book's `continuity.md` without the user's decision recorded.

## Before drafting: look

1. Read the outline and list the world facts it needs: places, institutions, rules, history, people.
2. Look each one up in `INDEX.md` and with `canon_index.py facts --key <key>`. Reuse what exists, with the exact names and values the pages give.
3. Read the open decisions that affect those pages. A blocking decision stops work on what depends on it.

## While drafting: invent, but never silently

Sort every new detail by who else would need to agree with it:

| Zone | Example | What you do |
|---|---|---|
| **Story-local** | a minor cook, a cup, a remark nothing else depends on | Write it. No record. |
| **World-level addition** | a new river, road, village, minor institution, minor character that contradicts nothing protected | Look it up first; reuse an existing one if there is one. Otherwise invent it, tag it in the prose as `{{new: river, "the Lathe"}}`, and add a row to `inventions.md` with status `open`. Keep writing. |
| **Touches protected canon** | anything that changes or contradicts an `accepted` page, a core-rule page (magic, premise, cosmology, history, economy) or a fact line | Stop that scene. State the question and continue with other scenes. If you are a subagent, return the question to the coordinator. |

The tag is `{{new: <type>, "<name>"}}` where `<type>` is a short lowercase word (`river`, `village`, `guild`, `person`). One row per distinct item.

## Descriptive passages carry a fact sheet

Every passage that describes a place, person or object for a reader gets an entry in `factsheets.md` in the same change: the layout and distances, who is present, the appearance facts. The sheet is what the user checks the prose against.

## Reconcile before the story is final

The canon custodian (or the bible specialist who owns the type) walks `inventions.md`. For each `open` row, search the bible for an existing equivalent, then do exactly one:

1. **replace**: swap the invented item for the existing one in the prose, remove the tag, set the row to `replaced` and name the page.
2. **promote**: file a change record proposing a page for it (class T1b or T2), have the right specialist draft the page as `draft`, remove the tag, set the row to `promoted` and name the page. Promotion never creates an `accepted` page; the user reviews proposals in a batch.
3. **demote**: it turned out to be story-local; remove the tag, set the row to `demoted`.

Reconciliation can run per scene, per chapter or per story. A story may be set `final` only when no tag remains in the prose and no row is `open`. The lint refuses a final story that breaks either condition, and refuses any tag that has no row.

## After the story: back-flow

After a draft (and again after reconciliation), the custodian reads the prose against `INDEX.md` and lists in `backflow.md` each consequential fact the story established that the bible does not hold: a motive, a rule, a date, a relationship, a changed state. Facts already in the bible, and story-local detail, are not listed. Each row names where it appears, the page or `::field::` it would belong to, and the dependents (pages linking to or from it). A fact that contradicts a protected page is not a proposal: stop and ask (T3). Rows stay `proposed` until the user's batch review; the custodian may then file them as change records or draft pages (`filed`), but never as `accepted`. This is separate from `inventions.md`, which tracks things the story named, not facts it established.
