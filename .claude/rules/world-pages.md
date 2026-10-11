---
paths:
  - "world/**"
  - "manifest.json"
---

<!-- Generated from rules/PAGES.md by the bootstrapper; do not edit. Loaded when a matching file is read or edited. -->

# Writing world pages

Applies to every agent that creates or edits a file in `world/`. The format comes from `docs/WORLD-HANDOFF.md`; the type table is `templates/world/types.json`. Everything else (drafts, stories, decisions, ledger, quests, dialogue) lives outside `world/`.

## Checklist for a page

1. File name is a slug ending `.md` (`haldren.md`, `iron-pact.md`): lowercase letters and digits, words joined by single dashes, starting with a letter. Two things with one name get different slugs (`aldric-of-torn.md`).
2. The first line is `# Name`. No YAML frontmatter, ever.
3. Use the type's sections as `##` headings, in the type's order. Omit a section only if the user said it does not apply; an empty section is better than a missing one.
4. One page per character, location, faction, region, creature and belief system. Keep pages short. Split a page when it grows a second subject other pages would link to.
5. Link with plain relative links to the exact file name, no `./`, no folder: `[the Combine](the-combine.md)`, optionally `#heading-slug`. Link only to pages in `world/`: a decision, change record or ledger entry is not a page, so cite it as text (`D-0005`), never as a link. Link what the page builds on: a faction links its region and the events that made it; a location links its region, its controlling faction and the people found there.
6. Plain markdown only: no HTML, images, wikilinks (`[[x]]`), task lists, footnotes, reference-style links, autolinks or link titles. Do not link to picture or map files; mention them by file name.
7. UTF-8, no byte-order mark, LF line endings, one trailing newline.
8. The page's type, `status` (`draft` unless a person reviewed it), `summary` (one or two plain sentences) and cross-entry fields go in `manifest.json`, not in the page. Fields that name another page take its file name.
9. Add the row to `manifest.json` in the same change, and run `py -3 tools/canon_lint.py` before you hand back.

## Marking what kind of statement it is

Pages hold the world as the author knows it. Keep other layers visible in plain prose:

| Layer | How to write it |
|---|---|
| Established fact | A plain sentence. |
| Key fact other pages will rely on | A `::key:: value` line (for example `::founded:: 1031 CR`). Keys are slugs. Keep one fact per line. |
| Attributed belief or claim | Say who holds it: "The Combine's annalists hold that ..." |
| Deliberate unknown | A line starting `Unknown:` and what is deliberately left open. |
| Future plan | A line starting `Planned:` (never present a plan as history). |
| Runtime or player state | Not in pages. Put it in `design/`. |

## Descriptive prose carries a fact sheet

Any passage that describes a place, person or object for a reader ships with a short fact sheet beside it (layout and distances, who is present, appearance facts) in the same change, in `drafts/` or `design/` next to the prose, not inside `world/`. The user should be able to check the description against the sheet without imagining it.
